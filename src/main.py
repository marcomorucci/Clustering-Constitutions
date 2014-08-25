#! /usr/bin/env python
"""
This module contains a function to run the main analysis.
to get a list of parameters for the function do help(main.run_analysis)
"""

from dataset import *
from analyze import *
from scores import *
from pandas import DataFrame, read_csv
import numpy as np
import progressbar
import matplotlib.pyplot as plt
np.random.seed(543)

# default paths for datafiles, modify if files are moved from data directory.
in_urls = {
    "names": "../data/state_names.txt",
    "constitutions": "data/state_urls.txt",
    "fh": "../data/fh.xls",
    "lji": "../data/lji.xls",
    "sfi": "../data/sfi.xls",
    "stopwords": "../data/stopwords.csv",
    "gdp": "../data/gdp.xls",
    "dataset": "../output/dataset.csv",
    "map": "../data/world_map/world_map"
}

out_urls = {
    "dataset": "../output/dataset.csv",
    "clusters": "../output/clusters.csv",
    "tf_idf": "../output/tf_idf.csv",
    "top_words": "../output/top_words.csv",
    "desc_stat": "../output/desc_stat.csv",
    "reg_results": "../output/reg_results.txt",
    "plots": "../output/img/",
    "multi_results": "../output/multi_results.csv"
}

if __name__ == "__main__":
    run_analysis()
    pass


def run_analysis(load=True, load_urls=in_urls, save_urls=out_urls,
                 lsa_components=150, clusters_amt=5, build_topwords=True,
                 top_words_amt=20, multiple=True, n_runs=50,
                 print_results=True, save_results=True,
                 display_progress=False
                 ):

    """
    Runs the steps for the main analysis producing and saving the outputs

    Keyword arguments:
    load -- bool, wether to load the frequencies dataset from a file, if False,
            creates the dataset from the constitutions files (default: True)
    urls -- dict containing urls for the data files, the keys must be the
            same as the default. (default: file_urls)
    lsa_components -- the number of components for the lsa analysis
    clusters_amt -- int, the number of clusters to generate
    build_topwords -- bool, wheter to build the topwords table (TAKES TIME!)
    top_words_amt -- int, the amount of most used words per cluster to save
    multiple -- bool, whether to run the clustering multiple times and
                    generate multiple regression table.
    n_runs -- int, how many times to do the clustering and calculate regression
              coefficients.
    print_results -- bool, wheter to print results to the std output.
    save_results -- bool, wheter to save the results of the analysis
    display_progress -- bool, whether to display a progress bar for
                        some operations, requires progressbar.py installed.

    Returns:
    A Dataset object containing the results of the analysis do help(Dataset)
    for usage instructions.
    """

    # Create frequencies dataset from constitutions files.
    if not load:
        with open(urls['constitutions']) as url_file:
            paths = url_file.read().splitlines()
            # Starting from the constitution names, generate urls
            for p in paths:
                paths[paths.index(p)] = "../constitutions/" + p.rstrip('\n') \
                    + ".txt"
        # Load default names for countries
        with open(state_names) as name_file:
            names = name_file.read().splitlines()

        d = Dataset()
        d.create(paths, names, save_urls['dataset'], True,
                 load_urls['stopwords'], display_progress)

    # Load dataset from previously saved version
    if load:
        print "Loading dataset..."
        d = Dataset()
        d.load(urls['dataset'], load_urls['stopwords'], True,
               display_progress)

    # Build custom tf_idf table
    d.build_tfidf_table()
    if save_results:
        d.tf_idf.to_csv(save_urls['tf_idf'])
    print "Obtaining democracy scores..."

    fh = load_workbook(load_urls['fh'])

    # Political rights
    pr = get_fh_scores(fh, scoreCol=115)
    # Civil liberties
    cl = get_fh_scores(fh, scoreCol=116)

    pr = clean_scores(pr, state_names)
    cl = clean_scores(cl, state_names)

    # Create combined FH score from pr and cl.
    # Country order is maintained by sorting.
    fhs = [(pr[v] + cl[v])/2 for v in sorted(pr.keys())]

    # FH category
    fhc = getFHScores(fh)
    fhc = cleanScores(fhc, state_names)
    fhc = convertScores(fhc)
    fhv = [fhc[v] for v in sorted(fhc.keys())]

    print "Running clustering analysis..."
    e, h, k = runKmeans(d, nComponents=lsa_components, nClusters=clusters_amt)

    if print_results:
        print "Cluster homogeneity score (silhouette score):", h
        print "Variance explained by LSA reduction:", e

    # Create DataFrame with clusters and dep. vars.
    clusters = DataFrame({"country": d.df['country_id'],
                         "kmeans": k, "fh_category": fhv, "fh_score": fhs})

    print "Obtaining Judicial Independence scores..."
    lji = read_csv(load_urls['lji'])
    lji = cleanLJIScores(lji)

    # Add lji scores to cluster DB country by country.
    # This is done because there are more countries in the LJI DB than we
    # have constitutions for.
    clusters['LJI'] = 0
    for i in lji.country:
        v = lji.loc[lji[lji.country == i].index, 'LJI']
        clusters.loc[clusters[clusters['country'] == i].index, 'LJI'] = \
            float(v)

    print "Obtaining State Fragility scores..."
    fs = getFragilityScores(load_urls['sfi'])

    # The frag. scores are intialized to NA because they are missing for some
    # of the countries in our constitutions db.
    clusters['fragility'] = 'NA'
    # Add fragility scores to the clusters, country by country.
    for r in range(len(clusters)):
        country = clusters.loc[r, 'country']
        if country in fs:
            clusters.loc[r, 'fragility'] = float(fs[country])

    # Add the clusters db to the dataset object
    d.cdb = clusters

    if build_topwords:
        print "Generating most used words table..."
        d.build_topwords_table(thresh=top_words_amt)
        if save_results:
            d.top_words.to_csv(save_urls['top_words'])
        if print_results:
            print d.top_words

    print "Generating descriptive statistics table..."
    d.build_descstat_able()
    if save_results:
        d.desc_stat.to_csv(save_urls['desc_stat'])
    if print_results:
        print d.desc_stat

    print "Loading gdp..."
    wb = loadWorkbook(load_urls['gdp'])
    gdp = getGDP(wb)
    gdp = cleanScores(gdp, state_names)
    # Country-GDP association is preserved by sorting.
    gdpv = [float(gdp[k]) for k in sorted(gdp.keys())]
    d.cdb['gdp'] = gdpv
    if save_results:
        d.cdb.to_csv(save_urls['clusters'])

    print "Running regressions..."
    formulas = [
        "fh_score ~ C(kmeans)",
        "LJI ~ C(kmeans)",
        "fragility ~ C(kmeans)",
        "fh_score ~ C(kmeans) + np.log(gdp)",
        "LJI ~ C(kmeans) + fh_score + np.log(gdp)",
        "fragility ~ C(kmeans) + fh_score + np.log(gdp)",
    ]
    results = runRegressions(d, formulas)

    if save_results:
        with open(save_urls['reg_results'], 'sw') as file:
            for r in results:
                file.write(str(r.summary()))

    if print_results:
        for r in results:
            print r.summary()

    print "Building plots.."
    d.make_plots(save=save_results)
    build_multiple_hist(d.top_words, save=save_results,
                        save_path=out_urls['plots'])
    plot_cluster_map(d.cdb, map_path=load_urls['map'],
                     save=save_results, save_path=save_urls['plots'])

    if print_results:
        plt.show()

    if multiple:
        print "running multiple clustering tests..."
        kmeans_res = run_multiple(d, f)
        rand_res = run_multiple(d, f, random=True)

        rand_mods = split_results(rand_mods)
        kmeans_mods = split_results(kmeans_mods)

        rand_coeffs = [count_coefficients(m) for m in rand_mods]
        kmeans_coeffs = [count_coefficients(m) for m in kmeans_mods]

        d.multi_results['mod'] = range(6)
        d.multi_results['kmeans'] = kmeans_coeffs
        d.multi_results['random'] = rand_coeffs

        if print_results:
            print d.multi_results

        if save_results:
            d.multi_results.to_csv(save_urls['multi_results'], index=False)

    return d
