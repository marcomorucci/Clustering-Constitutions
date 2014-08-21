import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import scale, Normalizer
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.metrics import silhouette_score
from progress import *
import statsmodels.formula.api as sm
from pandas import DataFrame

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


def run_kmeans(data, KMeans_Init='k-means++', n_clusters=3,
               pre_process=True, n_components=100, displayProgress=False):

    print "Preprocessing data..."
    if pre_process:
        X = preprocess(data, n_components)
    else:
        X = data

    print "Clustering data..."
    est = KMeans(init=KMeans_Init, n_clusters=n_clusters, n_init=1)

    labels = []

    if displayProgress:
        bar.update(i)

    labs = est.fit(X).labels_
    h = silhouette_score(X, labs, metric="euclidean")

    print "Cluster homogeneity score (silhouette score):", h
    return h, labs


def run_regressions(data, formulas):
    results = []
    c_frag = data[data['fragility'] != 'NA']
    c_frag[['fragility']] = c_frag['fragility'].astype(float)

    for f in formulas:
        if 'fragility' in f:
            r = sm.ols(formula=f, data=c_frag).fit()
        else:
            r = sm.ols(formula=f, data=data).fit()
        results.append(r)

    return results


def run_multiple(data, formulas, mod_vars=["C(kmeans)[T.1]", "C(kmeans)[T.2]",
                 "C(kmeans)[T.3]", "C(kmeans)[T.4]", "fh_score", "np.log(gdp)"],
                 n_runs=50, n_clusters=5, n_components=150,
                 display_progress=False):

    cols = {"run": range(n_runs), "silhouette": 0}

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

    bar = Pbar(display_progress)

    for i in range(n_runs):
        h, labs = run_kmeans(data, n_clusters=n_clusters,
                             n_components=n_components)
        results.loc[i, 'silhouette'] = h

        d = data.cdb
        d['kmeans'] = labs
        reg_results = run_regressions(data.cdb, formulas)

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
