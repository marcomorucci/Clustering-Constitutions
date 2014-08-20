import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import scale, Normalizer
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.metrics import silhouette_score
from progressbar import *
import statsmodels.formula.api as sm


def preprocess(data, nComponents, use_tf_idf=True):
    if use_tf_idf:
        d = data.tf_idf.as_matrix()
    else:
        d = data.df.as_matrix()
    svd = TruncatedSVD(n_components=nComponents)
    X = svd.fit_transform(d)
    norm = Normalizer()
    print "Variance explained after LSA:", \
        round(svd.explained_variance_ratio_.sum()*100, 2), '%'
    return norm.fit_transform(d)


def runAgglomerative(data, nClusters=3, aff="euclidean", dist="ward",
                     preProcess=True, nComponents=100):
    if preProcess:
        X = preprocess(data, nComponents)
    else:
        X = data
    est = AgglomerativeClustering(nClusters, affinity=aff, linkage=dist)
    fit = est.fit(X)
    return fit.labels_


def runKmeans(data, runs=50, KMeans_Init='k-means++', nClusters=3,
              preProcess=True, nComponents=100, displayProgress=False):

    if displayProgress:
        widgets = ['Progress: ', Percentage(), ' ',
                   Bar(marker=RotatingMarker())]
        bar = ProgressBar(widgets=widgets, maxval=maxBar).start()

    print "Preprocessing data..."
    if preProcess:
        X = preprocess(data, nComponents)
    else:
        X = data

    print "Clustering data..."
    est = KMeans(init=KMeans_Init, n_clusters=nClusters, n_init=1)

    labels = []
    best = 0
    for i in range(runs):

        if displayProgress:
            bar.update(i)

        labs = est.fit(X).labels_
        h = silhouette_score(X, labs, metric="euclidean")
        if h > best:
            best = h
            labels = labs

    if displayProgress:
        bar.finish()

    print "Cluster homogeneity score (silhouette score):", best
    return labels


def runRegressions(data, formulas, save=True):
    results = []
    c_frag = data.cdb[data.cdb['fragility'] != 'NA']
    c_frag[['fragility']] = c_frag['fragility'].astype(float)

    for f in formulas:
        if 'fragility' in f:
            r = sm.ols(formula=f, data=c_frag).fit()
        else:
            r = sm.ols(formula=f, data=data.cdb).fit()
        results.append(r)

    if save:
        with open("../output/regression_results.txt", 'w') as file:
            for r in results:
                file.write(str(r.summary()))

    data.regResults = results

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


def saveTopWords(tw, path):
    f = open(path, 'w')
    cnt = 0
    for r in len(tw):
        for c in tw.columns:
            f.write(str(tw.loc[r, c]))
    f.close()


def buildMultipleHistPlot(cdb):
    plt.clf
    colors = ['b', 'g', 'r', 'y', 'c']

    for i in range(len(cdb)):
        y = cdb.loc[i, 'state':]/cdb.loc[i, 'tot_terms']
        x = np.array(range(36))
        plt.bar(x, y, alpha=0.8, label=str(i),
                color=colors[i], width=0.8, align="center")

    plt.xticks(range(36), cdb.columns[2:], rotation="vertical")
    plt.legend(loc="best")
    plt.show()
