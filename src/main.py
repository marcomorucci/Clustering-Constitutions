import sys
sys.path.insert(0, '/Library/Python/2.7/site-packages')
import os

os.chdir('/Users/marco/Copy/projects/constitutions/src')
print "working directory:", os.getcwd()

from download_constitutions import *
from build_datasets import *
from analyze import *
from prepare_scores import *
from pandas import DataFrame, read_csv
import numpy as np

np.random.seed(543)

if __name__ == "__main__":
    pass


def run_analysis(load=True, state_urls="../data/state_urls.txt",
                 state_names="../data/state_names.txt", scoresPath="../data/fh.xls",
                 displayProgress=False):
    if not load:
        with open(state_urls) as urlFile:
            paths = urlFile.read().splitlines()
            for p in paths:
                paths[paths.index(p)] = "../constitutions/" + p.rstrip('\n') + ".txt"
        with open(state_names) as nameFile:
            names = nameFile.read().splitlines()

        d = dataset()
        d.create(paths, names, "../output/dataset.csv", True, True)

    if load:
        print "Loading dataset..."
        d = dataset()
        d.load("../output/dataset.csv", "../data/stopwords.csv", True, displayProgress)

    d.buildTFIDFTable()

    print "Obtaining democracy scores..."

    fh = loadWorkbook(scoresPath)
    pr = getFHScores(fh, scoreCol=115)
    cl = getFHScores(fh, scoreCol=116)
    pr = cleanScores(pr, state_names)
    cl = cleanScores(cl, state_names)
    fhs = [(pr[v] + cl[v])/2 for v in sorted(pr.keys())]
    fhc = getFHScores(fh)
    fhc = cleanScores(fhc, state_names)
    fhc = convertScores(fhc)
    fhv = [fhc[v] for v in sorted(fhc.keys())]

    print "Running clustering analysis..."

    k = runKmeans(d, nComponents=150, nClusters=5)

    clusters = DataFrame({"country": d.df['country_id'],
                         "kmeans": k, "fh_category": fhv, "fh_score": fhs})

    print "Obtaining Judicial Independence scores..."
    lji = read_csv("../data/judicial_independence.csv")
    lji = cleanLJIScores(lji)
    clusters['LJI'] = 0
    for i in lji.country:
        v = lji.loc[lji[lji.country == i].index, 'LJI']
        clusters.loc[clusters[clusters['country'] == i].index, 'LJI'] = float(v)

    print "Obtaining State Fragility scores..."
    fs = getFragilityScores("../data/fragility.xls")

    clusters['fragility'] = 'NA'
    for r in range(len(clusters)):
        country = clusters.loc[r, 'country']
        if country in fs:
            clusters.loc[r, 'fragility'] = float(fs[country])

    d.setClusters(clusters)

    print "Generating most used words table..."
    d.buildTopWordsTable(thresh=20)
    print d.topWords

    print "Generating descriptive statistics table..."
    d.buildDescStatTable()
    print d.descStat

    wb = loadWorkbook("../data/gdp.xls")
    gdp = getGDP(wb)
    gdp = cleanScores(gdp, state_names)
    gdpv = [float(gdp[k]) for k in sorted(gdp.keys())]
    d.cdb['gdp'] = gdpv

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
    for r in results:
        print r.summary()
    return d
