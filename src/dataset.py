from nltk.corpus import stopwords
import nltk
import string
import numpy as np
from pandas import read_csv, DataFrame, Series
import matplotlib.pyplot as plt
from progress import *


class Dataset:
    """
    This class holds an object that stores all the tables and the results
    of the analysis.

    To access them once the analysis is over do:
    data = Dataset()
    data.df: for the raw word frequency data
    data.cdb for the table holding clusters and dep. vars.
    data.top_words for the table of most used words.
    data.desc_stat for a table of descriptive statistics for each cluster
    data.reg.results for the regression results stored as statsmodels
                     regressionResults objects

    You can show plots and print reg. results by doing
    data.show_plots()
    data.regression_results()
    """

    def __init__(self):
        self.tf_idf = DataFrame()
        self.df = DataFrame()
        self.cdb = DataFrame()
        self.top_words = DataFrame()
        self.desc_stat = DataFrame()
        self.reg_results = []
        self.multi_results = DataFrame()

    def create(self, paths, country_names, save_file="", clean=True,
               stopwords_path="../data/stopwords.csv", display_progress=False):

        # Create progress bar, Pbar class will handle import and
        # wheter or not to display.
        bar = Pbar(displayProgress)
        bar.create("Generating csv dataset...", len(paths))

        # Init database with as many rows as there are countries
        self.df = DataFrame(countryNames, columns=["country_id"])
        self.df['tot_terms'] = 0

        # A countre to keep track of which row we are on
        cnt = 0
        for p in paths:

            bar.update(cnt)

            c = load_constitution(p)
            frequencies = get_frequency(c)

            # Add number of words to each constitution
            self.df.loc[cnt, 'tot_terms'] = len(frequencies.keys())

            for word in frequencies.keys():
                # Initialize all words that have not appeared in other
                # constitutions to frequency 0
                if word not in self.df.columns:
                    self.df[word] = 0

                self.df[word][cnt] = frequencies[word]

            cnt += 1

        bar.finish()

        if(saveFile != ""):
            print "Saving dataset to csv file..."
            self.df.to_csv(saveFile, index=False)

        if(clean):
            self.clean(stopwordsPath, display_progress)

    def load(self, path, stopwords="../data/stopwords.csv", clean=True,
             display_progress=False):
        self.df = read_csv(path)
        if clean:
            self.clean(stopwords, display_progress)

    def clean(self, stopwords_path, display_progress=False):
        bar = Pbar("Cleaning dataset...", len(self.df.columns))

        with open(stopwordsPath, 'r+') as sw_file:
            stopwords = sw_file.read().split(',')

        numbers = [str(n) for n in range(10)]
        i = 0
        for c in self.df.columns:
            # Remove all words which meet the following conditions
            if c[0] in numbers or c in stopwords or not self.df[c].any > 0:
                self.df = self.df.drop(c, axis=1)

            bar.update(i)
            i += 1

        bar.finish()

    def build_tfidf_table(self):
        self.tf_idf = DataFrame()

        # Exclude country name and total words from data
        tf = self.df.ix[:, 2:]

        # To create the tf term, divide each row by the number of words
        # that appear in that country's constitution.
        for r in range(len(self.df)):
            tf.loc[r, :] = tf.loc[r, :] / self.df.loc[r, 'tot_terms']

        # To create idf, divide the number of documents by the number
        # of documents containing each word.
        # The operation here is vectorized using numpy arrays.
        # The number of documents containing each word is obtained by summing
        # a vector of bools where the documents in which the word has freq. > 0
        # are labeled true.
        idf = np.log(len(self.df.index) /
                     (self.df[self.df.ix[:, 2:] > 0].sum(axis=0))+1)

        self.tf_idf = tf*idf

        # Drop country and tot words columns from table in case they are still
        # there.
        if('country_id' in self.tf_idf.columns):
            self.tf_idf = self.tf_idf.drop('country_id', axis=1)
        if'tot_terms' in self.tf_idf.columns:
            self.tf_idf = self.tf_idf.drop('tot_terms', axis=1)

    def get_cluster(self, c_id, clusterCol='kmeans'):
        if c_id not in self.cdb[clusterCol]:
            raise KeyError("Selected cluster not in dataset")

        return self.cdb[self.cdb[clusterCol] == c_id]

    def get_topwords(self, countries, thresh=10, tf_idf=False):
        tw = DataFrame()
        for r in range(len(self.df)):
            if self.df.loc[r, 'country_id'] in countries:
                if tf_idf:
                    tw = tw.append(self.tf_idf.loc[r, :])
                else:
                    tw = tw.append(self.df.loc[r, :])

        return tw.mean().order(ascending=False)[:thresh]

    def get_word_avg(self, countries, word, tf_idf=False):
        w = 0
        for r in range(len(self.df)):
            if self.df.loc[r, 'country_id'] in countries:
                if tf_idf:
                    w += self.tf_idf.loc[r, word]
                else:
                    w += self.df.loc[r, word]
        return w/len(countries)

    def build_topwords_table(self, cluster_col="kmeans", thresh=10, raw=True):
        if len(self.cdb) == 0:
            raise Exception("Cluster database not initialized")

        # get themnames of all the clusters created
        labels = list(set(self.cdb[clusterCol]))

        self.top_words = DataFrame({'cluster': labels})
        for l in labels:
            countries = [c for c in self.get_cluster(l)['country']]
            tw = self.get_topwords(countries, thresh, tf_idf=(not raw))
            idx = self.top_words[self.top_words['cluster'] == l].index

            for w in tw.index:
                if w not in self.top_words.columns:
                    self.top_words[w] = 0
                self.top_words.loc[idx, w] = tw[w]

        for r in range(len(self.top_words)):
            countries = [c for c in self.get_cluster(self.top_words.loc[r,
                                                     'cluster'])['country']]
            for w in self.top_words.columns:
                if w != 'cluster' and self.top_words.loc[r, w] == 0:
                    self.top_words.loc[r, w] = self.get_word_avg(countries, w,
                                                            tf_idf=(not raw))

    def build_descstat_table(self, cluster_col="kmeans",
                             cols=['fh_score', 'LJI', 'fragility'],
                             na_cols=['fragility']):
        if len(self.cdb) == 0:
            raise Exception("Cluster database not initialized")

        labels = list(set(self.cdb[clusterCol]))
        # This weird list comprehension creates the labels for each colums of
        # the descstat table by pasting strings.
        col_labels = sum([[c + '_mean', c + '_median', c + '_std']
                          for c in cols], [])
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

    def regression_results(self):
        if not self.reg_results:
            raise Error("Tried to access regression results before running\
                            regressions")

        for r in self.reg_results:
            print r.summary()

    def make_plots(self, save=False):
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

    def show_plots(self):
        self.make_plots()


def load_constitution(path):
    with open(path, "r") as constitution:
        text = constitution.read().lower()
        no_punctuation = text.translate(None, string.punctuation)
        tokens = nltk.word_tokenize(no_punctuation)
        filtered = [t for t in tokens if t not in stopwords.words("english")]
        return tokens


def get_frequency(tokens):
    freq = nltk.FreqDist(tokens)
    return freq
