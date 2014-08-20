from nltk.corpus import stopwords
import nltk
import string
import numpy as np
from progressbar import *
from pandas import read_csv, DataFrame, Series
import matplotlib.pyplot as plt

class dataset:
    def __init__(self):
        self.tf_idf = DataFrame()
        self.df = DataFrame()
        self.cdb = DataFrame()
        self.topWords = DataFrame()
        self.descStat = DataFrame()
        self.regResults = []

    def create(self, paths, countryNames, saveFile="", clean=True,
               stopwordsPath="../data/stopwords.csv", displayProgress=True):
        cnt = 0

        if(displayProgress):
            bar = self.initProgressBar("Generating csv dataset...", len(paths))

        self.df = DataFrame(countryNames, columns=["country_id"])
        self.df['tot_terms'] = 0
        for p in paths:

            if(displayProgress):
                bar.update(cnt)

            c = loadConstitution(p)
            frequencies = getFrequency(c)
            self.df.loc[cnt, 'tot_terms'] = len(frequencies.keys())

            for word in frequencies.keys():
                if word not in self.df.columns:
                    self.df[word] = 0

                self.df[word][cnt] = frequencies[word]

            cnt += 1

        if(displayProgress):
            bar.finish()

        if(saveFile != ""):
            print "Saving dataset to csv file..."
            self.df.to_csv(saveFile, index=False)

        if(clean):
            self.clean(stopwordsPath)

    def load(self, path, stopwords="../data/stopwords.csv", clean=True,
             displayProgress=False):
        self.df = read_csv(path)
        if clean:
            self.clean(stopwords, displayProgress)

    def clean(self, stopwordsPath, displayProgress=False):
        if displayProgress:
            bar = self.initProgressBar("Cleaning dataset...",
                                       len(self.df.columns))

        with open(stopwordsPath, 'r+') as swFile:
            stopwords = swFile.read().split(',')
        numbers = [str(n) for n in range(10)]

        i = 0
        for c in self.df.columns:
            if c[0] in numbers or c in stopwords or not self.df[c].any > 0:
                self.df = self.df.drop(c, axis=1)

            if displayProgress:
                bar.update(i)
                i += 1

        if displayProgress:
            bar.finish()

    def initProgressBar(self, message, maxBar):
        widgets = ['Progress: ', Percentage(), ' ',
                   Bar(marker=RotatingMarker())]
        print(message)
        return ProgressBar(widgets=widgets, maxval=maxBar).start()

    def buildTFIDFTable(self):
        self.tf_idf = DataFrame()

        tf = self.df.ix[:, 2:]
        for r in range(len(self.df)):
            tf.loc[r, :] = tf.loc[r, :] / self.df.loc[r, 'tot_terms']

        idf = np.log((len(self.df.index)-2) /
                     (self.df[self.df.ix[:, 2:] > 0].sum(axis=0))+1)
        self.tf_idf = tf*idf

        if('country_id' in self.tf_idf.columns):
            self.tf_idf = self.tf_idf.drop('country_id', axis=1)
        if'tot_terms' in self.tf_idf.columns:
            self.tf_idf = self.tf_idf.drop('tot_terms', axis=1)

    def setClusters(self, cdb):
        self.cdb = cdb

    def getCluster(self, c_id, clusterCol='kmeans'):
        if c_id not in self.cdb[clusterCol]:
            raise KeyError("Selected cluster not in dataset")

        return self.cdb[self.cdb[clusterCol] == c_id]

    def getTopWords(self, countries, thresh=10, tf_idf=False):
        tw = DataFrame()
        for r in range(len(self.df)):
            if self.df.loc[r, 'country_id'] in countries:
                if tf_idf:
                    tw = tw.append(self.tf_idf.loc[r, :])
                else:
                    tw = tw.append(self.df.loc[r, :])

        return tw.mean().order(ascending=False)[:thresh]

    def getWordAvg(self, countries, word, tf_idf=False):
        w = 0
        for r in range(len(self.df)):
            if self.df.loc[r, 'country_id'] in countries:
                if tf_idf:
                    w += self.tf_idf.loc[r, word]
                else:
                    w += self.df.loc[r, word]
        return w/len(countries)

    def buildTopWordsTable(self, clusterCol="kmeans", thresh=10,
                           addOverall=True, raw=True):
        if len(self.cdb) == 0:
            raise Exception("Cluster database not initialized")

        labels = list(set(self.cdb[clusterCol]))

        self.topWords = DataFrame({'cluster': labels})
        for l in labels:
            countries = [c for c in self.getCluster(l)['country']]
            tw = self.getTopWords(countries, thresh, tf_idf=(not raw))
            idx = self.topWords[self.topWords['cluster'] == l].index

            for w in tw.index:
                if w not in self.topWords.columns:
                    self.topWords[w] = 0
                self.topWords.loc[idx, w] = tw[w]

        for r in range(len(self.topWords)):
            countries = [c for c in self.getCluster(self.topWords.loc[r,
                                                    'cluster'])['country']]
            for w in self.topWords.columns:
                if w != 'cluster' and self.topWords.loc[r, w] == 0:
                    self.topWords.loc[r, w] = self.getWordAvg(countries, w,
                                                              tf_idf=(not raw))

    def buildDescStatTable(self, clusterCol="kmeans",
                           cols=['fh_score', 'LJI', 'fragility'],
                           na_cols=['fragility']):
        if len(self.cdb) == 0:
            raise Exception("Cluster database not initialized")

        labels = list(set(self.cdb[clusterCol]))
        col_labels = sum([[c + '_mean', c + '_median', c + '_std'] for c in cols], [])
        self.descStat = DataFrame(columns=['cluster'] + col_labels)

        for l in labels:
            row = [l]
            cluster = self.getCluster(l)

            for c in cols:
                if c in na_cols:
                    row.append(cluster[cluster[c] != 'NA'][c].mean())
                    row.append(cluster[cluster[c] != 'NA'][c].median())
                    row.append(cluster[cluster[c] != 'NA'][c].std())
                else:
                    row.append(cluster[c].mean())
                    row.append(cluster[c].median())
                    row.append(cluster[c].std())

            self.descStat.loc[l] = row

    def regressionResults(self):
        if not self.regResults:
            raise Error("Tried to access regression results before running\
                            regressions")

        for r in self.regResults:
            print r.summary()

    def makePlots(self, save=False):
        if not self.cdb:
            raise Error("Tried to build plots with empty cluster table")

        plt.figure(1)
        self.cdb.boxplot(column="fh_score", by="kmeans")
        if save:
            plt.savefig("../output/img/FH.png")

        plt.figure(2)
        self.cdb.boxplot(column="LJI", by="kmeans")
        if save:
            plt.savefig("../output/img/LJ).png")

        plt.figure(3)
        self.cdb[self.cdb['fragility'] != 'NA'].boxplot(column="fragility",
                                                        by="kmeans")
        if save:
            plt.savefig("../output/img/SFI).png")

        if not save:
            plt.show()

    def showPlots(self):
        self.makePlots()


def loadConstitution(path):
    with open(path, "r") as constitution:
        text = constitution.read().lower()
        noPunctuation = text.translate(None, string.punctuation)
        tokens = nltk.word_tokenize(noPunctuation)
        filtered = [t for t in tokens if t not in stopwords.words("english")]
        return tokens


def getFrequency(tokens):
    freq = nltk.FreqDist(tokens)
    return freq
