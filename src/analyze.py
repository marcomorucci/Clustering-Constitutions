"""
This module contains helper functions to perform various analyses
on the datasets created.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import scale, Normalizer
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.metrics import silhouette_score
from progress import *
import statsmodels.formula.api as sm
from pandas import DataFrame
from random import randrange


def preprocess(data, n_components, use_tf_idf=True):
    """
    Preproecess the data for clustering by running SVD and
    normalizing the results. This process is also known as
    LSA.

    arguments:
    data -- Dataset, if tf_idf is Truethe object must contain a
            tf_idf table alongside a raw frequencies dataframe.
    n_components -- int, the number of components to use for the SVD
                    a minimum of 100 is recommended.
    use_tf_idf -- bool, whether to use the tf-idf frequencies for the
                  preprocessing.

    returns:
    e -- float, a measure of variance explained by the SVD.
    X -- np.array, an array with the data reduced to n_components.
    """
    if use_tf_idf:
        d = data.tf_idf.as_matrix()
    else:
        d = data.df.as_matrix()
    svd = TruncatedSVD(n_components=n_components)
    X = svd.fit_transform(d)
    norm = Normalizer()

    # Record a measure of explained variance
    e = svd.explained_variance_ratio_.sum()*100
    return e, norm.fit_transform(d)


def run_kmeans(data, kmeans_Init='k-means++', n_clusters=3,
               pre_process=True, n_components=100):
    """
    Runs the kmeans clustering on the data.

    arguments
    data -- Dataset, an object storing either a raw frequency DataFrame or a
            tf_idf table DataFrame.
    KMeans_Init -- string, either k-means++ or random for kmeans initialization
    n_clusters -- int, the amount of clusters to generate.
    pre_process -- bool, whether to run preprocessing on the data.
                   Do help(preprocess) for info on what preprocessing does.
    n_components -- int, the amount of components SVD should reduce the data to

    returns:
    e -- float, a measure of explained variance by the SVD
    h -- float, a measure of cluster purity (silhouette coefficient)
    labs -- list, n_samples long list of cluster labels, each associated
            with one country.
    """
    print "Preprocessing data..."
    if pre_process:
        e, X = preprocess(data, n_components)
    else:
        X = data
        e = 0

    print "Clustering data..."
    est = KMeans(init=kmeans_Init, n_clusters=n_clusters, n_init=1)

    labels = []

    if displayProgress:
        bar.update(i)

    labs = est.fit(X).labels_
    h = silhouette_score(X, labs, metric="euclidean")

    return e, h, labs


def run_regressions(data, formulas):
    """
    Run len(formulas) regressions on the clustered data.

    arguments:
    data -- Dataset, a dataset with the cdb field initialized to
            a DataFrame containing clusters and dep.vars.
    formulas --  a list of strings of the type 'dep_var ~ ex_var + ...'"
                 see statsmodels documentation for details.

    returns:
    a list of RegressionResults objects each one containing the results of
    one regression model. See statsmodels documentation for additional info.
    """
    results = []

    # We need to create an additional dataset for the fragility dep.var.
    # because scores from some countries are missing (marked as 'NA')
    # if we feed the statsmodels.ols function data with nas, it throws
    # errors.
    c_frag = data[data['fragility'] != 'NA']
    c_frag[['fragility']] = c_frag['fragility'].astype(float)

    for f in formulas:
        if 'fragility' in f:
            r = sm.ols(formula=f, data=c_frag).fit()
        else:
            r = sm.ols(formula=f, data=data).fit()
        results.append(r)

    return results


def random_clusters(n_clusters, n_samples):
    """
    Creates n_samples random labels ranging from 0 to n_clusters.

    arguments:
    n_clusters -- int, how many different kinds of labels to create.
    n_samples --  int, how many labels to create.

    returns:
    A list of n_clusters labels.
    """
    return [randrange(n_clusters) for s in range(n_samples)]


def run_multiple(data, formulas, random=False,
                 mod_vars=["C(kmeans)[T.1]", "C(kmeans)[T.2]",
                 "C(kmeans)[T.3]", "C(kmeans)[T.4]", "fh_score", "np.log(gdp)"],
                 n_runs=50, n_clusters=5, n_components=150,
                 display_progress=False):

    """
    Runs clustering and regressions multiple times.

    arguments:
    data -- Dataset, a dataset with df and tf_idf both initialized.
    formulas -- list, formulas for regressions, see
                statsmodels documentation for more info.
    random -- bool, whether to assign the clusters at random
    mod_vars -- list, a list of strings with all the variables
                of the regression, with the same names as the ols output.
    n_runs -- int, how many runs to perform.
    n_clusters -- int, how many clusters to generate.
    n_components -- int, how many components proprocessing should reduce
                    the data to.
    display_progress -- bool, whether to display a progress bar.

    returns:
    A pandas DataFrame object, storing runs in the rows and model
    coefficients in the columns
    """

    # Generate column headers and initialize all columns to 0
    cols = {"run": range(n_runs), "silhouette": 0, "LSA": 0}

    for c in mod_vars:
        for m in range(len(formulas)):
            cols[str(m) + "_beta_" + str(c)] = 0
            cols[str(m) + "_std_" + str(c)] = 0
            cols[str(m) + "_p_" + str(c)] = 0

    for m in range(len(formulas)):
            cols[str(m) + "_intercept"] = 0
            cols[str(m) + "_std_intercept"] = 0
            cols[str(m) + "_p_intercept"] = 0
            cols[str(m) + "_adj_r2"] = 0
            cols[str(m) + "_f-score"] = 0
            cols[str(m) + "_f-pval"] = 0

    results = DataFrame(cols)

    # Init progress bar
    bar = Pbar(display_progress)

    # Run the multiple regressions
    for i in range(n_runs):
        if random:
            labs = random_clusters(n_clusters=n_clusters, data=data)
            e = 0
            h = 0
        else:
            e, h, labs = run_kmeans(data, n_clusters=n_clusters,
                                    n_components=n_components)
        results.loc[i, 'silhouette'] = h
        results.loc[i, 'LSA'] = e
        # The only data column that changes after a rerun are the clusters
        d = data.cdb
        d['kmeans'] = labs

        reg_results = run_regressions(data.cdb, formulas)

        # Nicely put each result in a column in the output table.
        for r in reg_results:
            m = str(reg_results.index(r))
            for c in mod_vars:
                if c not in r.params.keys():
                    continue
                results.loc[i, m + "_beta_" + c] = r.params[c]
                results.loc[i, m + "_std_" + c] = r.bse[c]
                results.loc[i, m + "_p_" + c] = r.pvalues[c]

            results.loc[i, m + "_intercept"] = r.params[0]
            results.loc[i, m + "_std_intercept"] = r.bse[0]
            results.loc[i, m + "_p_intercept"] = r.pvalues[0]
            results.loc[i, m + "_adj_r2"] = r.rsquared_adj
            results.loc[i, m + "_f-score"] = r.fvalue
            results.loc[i, m + "_f-pval"] = r.f_pvalue

        bar.update(i)

    bar.finish()

    return results


def saveCountryClusters(c, path):
    a = max(len(c[0]), len(c[1]), len(c[2]), len(c[3]), len(c[4]))
    f = open(path, 'w')

    for i in range(a):
        row = []
        for k in c.keys():
            if i < len(c[k])-1:
                row.append(list(c[k])[i])
            else:
                row.append(' ')
        f.write(' & '.join(row))
        f.write('\\\\ \n')

    f.close()


def split_results(results, n_mods=6, n_cols=24):
    """
    Divides multiple analysis results into separate models.

    arguments:
    results --  DataFrame, the output of the run_multiple function.
    n_mods --  int, how many different models to split the data in.
    n_cols --  int, how many columns pertain to each model.

    returns:
    A list of DataFrame, each one containing only one model.
    """

    lower, upper = 0, 24
    mods = []
    for m in range(n_mods):
        mod = results.ix[:, lower:upper]
        # Take model index out of comlumn names
        mod.columns = [c[2:] for c in mod.columns]
        mods.append(mod)
        lower = upper
        upper += n_cols

    return mods


def get_sig_coeff(mod, sig, n_sig=1,
                  coeffs=['p_C(kmeans)[T.1]', 'p_C(kmeans)[T.2]',
                          'p_C(kmeans)[T.3]', 'p_C(kmeans)[T.4]']):
    """
    Counts how many runs had significant coefficients for the
    model passed in.

    mod -- DataFrame, a model such as one entry in the list returned by
           the split_results fcn.
    sig -- float, the significance level to consider.
    coeffs -- list, a list of strings containing the column names of the
              coefficients to check for significance.
    n_sig -- the number of coefficients that have to be significant to
             be included in the final result.

    returns:
    A DataFrame with all columns included in the passed mod, but only
    the rows for which n_sig coefficients are considered significant at sig.
    """
    cond = []
    for r in range(len(mod)):
        sig_so_far = 0
        # This is basically an 'or' condition unpacked.
        for c in coeffs:
            if mod.loc[r, c] < sig:
                sig_so_far += 1
                break

        if sig_so_far >= n_sig:
            cond.append(True)
        else:
            cond.append(False)

    return mod.loc[cond, :]


def build_multiple_hist(cdb, save=False, save_path="../output/img/"):
    """
    Creates a stacked histogram with the frequency of the most used words
    for each cluster.

    arguments:
    cdb --  DataFrame, the top_words table built by the Dataset class.
    save -- bool, save the figure?
    save_path -- path to save the image in, will NOT check if directory
                 exists before saving and will NOT create new folders.

    returns:
    nothing.
    """

    plt.clf()
    plt.figure(figsize=(12, 10), dpi=200)
    plt.grid(True)
    colors = {0: 'b', 1: 'g', 2: 'r', 3: 'y', 4: 'c'}
    # Don't know why this is the right order.
    labels = ['0', '1', '4', '3', '2']

    # To plot lower values above higher ones sort each
    # column in descending order and add it to the plot one at
    # a time.
    for x in np.arange(2, len(cdb.columns)):
        for y in sorted(cdb.ix[:, x], reverse=True):
            idx = cdb[cdb.ix[:, x] == y].index[0]
            cluster = cdb.loc[idx, 'cluster']
            color = colors[cluster]
            plt.barh(x, y, color=color, align="center", linewidth=0)

    plt.yticks(range(2, len(cdb.columns)), cdb.columns[2:])
    plt.legend(labels, loc="best")
    plt.tight_layout()

    if save:
        plt.savefig(save_path + "multi_hist.png")


def plot_cluster_map(cdb, map_path="../data/world_borders/world_borders"):
    from matplotlib.collections import LineCollection
    from matplotlib import cm
    from mpl_toolkits.basemap import Basemap
    import shapefile

    plt.clf()
    # Custom adjust of the subplots
    ax = plt.subplot(111)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.05,
                        wspace=0.15, hspace=0.05)
    m = Basemap(resolution='c', projection='merc')
    m.drawcountries(linewidth=0.5)
    m.drawcoastlines(linewidth=0.5)

    r = shapefile.Reader(map_path)
    shapes = r.shapes()
    records = r.records()

    for record, shape in zip(records, shapes):
        lons, lats = zip(*shape.points)
        data = np.array(m(lons, lats)).T

    if len(shape.parts) == 1:
        segs = [data, ]
    else:
        segs = []
        for i in range(1, len(shape.parts)):
            index = shape.parts[i-1]
            index2 = shape.parts[i]
            segs.append(data[index:index2])
        segs.append(data[index2:])

    lines = LineCollection(segs, antialiaseds=(1,))
    lines.set_facecolors(cm.jet(np.random.rand(1)))
    lines.set_edgecolors('k')
    lines.set_linewidth(0.1)
    ax.add_collection(lines)

    plt.show()
