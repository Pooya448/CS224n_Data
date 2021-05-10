from glob import glob
import os
import nltk
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import matplotlib.pyplot as plt
import subprocess

def Convert(tup):
    di = {}
    for a, b in tup:
        di[a] = b
    return di.copy()

def bar_chart(d, title, xl, yl, rotate=False, dir="../analysis/charts/", hist=False):


    if not os.path.exists(dir):
        os.makedirs(dir)

    x = [k for k, v in d.items() if k != 'ALL']
    y = [v for k, v in d.items() if k != 'ALL']

    c = ['green', 'blue', 'purple', 'brown', 'teal', 'red']

    plt.bar(x, y, color=c)
    plt.title(title)

    if not hist:
        plt.xlabel(xl)
    else:
        plt.xlabel([])

    plt.ylabel(yl)

    if rotate != False:
        plt.xticks(rotation = rotate)
        plt.tight_layout()


    path = dir + title.lower().replace(' ', '_') + ".png"
    plt.savefig(path)
    plt.close()

def freq_chart(d, option):

    if option == 0:
        type = 'Frequent Uncommon'
    if option == 1:
        type = 'RNF'
    if option == 2:
        type = 'TF-IDF'
    if option == 3:
        type = 'Histogram'

    for label, f in d.items():
        if label == 'ALL':
            continue

        dd = Convert(f)

        dir = f"../analysis/charts/{type}/"

        if option == 3:
            title = f"{type} - {label}"
            bar_chart(dd, title, 'Label', 'Word', 90, dir, True)
        else:
            title = f"Top 10 By {type} - {label}"
            bar_chart(dd, title, 'Label', 'Word', 90, dir)




def setup():
    tokens = {}
    files = glob("../data/lemmatize/*.txt")

    for path in files:
        head, tail = os.path.split(path)
        key = tail.split('.')[0]

        with open(path, "r") as fr:
                tk = fr.read()
                tk = tk.split(' ')
                tokens[key] = tk

    dialogues = {}
    files = glob("../data/clean/dialogue/*.txt")

    for path in files:
        head, tail = os.path.split(path)
        key = tail.split('.')[0]
        with open(path, "r") as fr:
                lines = fr.readlines()
                dialogues[key] = lines

    corpora = {}
    files = glob("../data/clean/corpora/*.txt")

    for path in files:
        head, tail = os.path.split(path)
        key = tail.split('.')[0]
        with open(path, "r") as fr:
                cor = fr.read()
                corpora[key] = cor

    sentences = {}
    files = glob("../data/sentence_tokenize/*.txt")

    for path in files:
        head, tail = os.path.split(path)
        key = tail.split('.')[0]
        with open(path, "r") as fr:
                sents = fr.readlines()
                sentences[key] = sents

    return tokens, dialogues, sentences, corpora

def Analyze():

    parent_dir = "../analysis/"
    subprocess.call(["rm", "-rf", f"{parent_dir}"])

    n_dial = {}
    n_sents= {}
    n_words = {}
    n_dist_words = {}
    n_comm = {}
    n_uncomm = {}
    uncommons = {}
    commons = {}
    most_freq = {}
    top_tfidf = {}
    top_rnf = {}
    histogram = {}

    tokens, dialogues, sentences, corpora = setup()

    rep = "../analysis/analysis_report.txt"
    dir = "../analysis/"
    if not os.path.exists(dir):
        os.makedirs(dir)

    ### N unit
    with open(rep, 'a+') as f:
        f.write("N Units:\n")
        for key, ds in dialogues.items():
            n = len(ds)
            f.write(f"{key} -> {n}\n")
            n_dial[key] = n
        f.write("\n\n")

    ### N Sentence
    with open(rep, 'a+') as f:
        f.write("N Sentence:\n")
        for key, sents in sentences.items():
            n = len(sents)
            f.write(f"{key} -> {n}\n")
            n_sents[key] = n
        f.write("\n\n")

    ### N Words/Distinct/Common/Uncommon words
    with open(rep, 'a+') as f:
        f.write("N Words:\n")
        for key, ts in tokens.items():
            if key == 'ALL':
                continue

            n = len(ts)
            distinct = set(ts)
            n_dist = len(distinct)

            prin = []
            for k, v in tokens.items():
                if key != k and k != 'ALL':
                    prin += v


            un_comm = set(ts).difference(set(prin))
            comm = set(ts).intersection(set(prin))

            uncommon_corpus = [word for word in ts if word in un_comm]

            n_common = len(comm)
            n_uncommon = len(un_comm)

            f.write(f"{key} -> Word: {n}, Distinct: {n_dist}, Common: {n_common}, Uncommon: {n_uncommon}\n\n")
            n_words[key] = n
            n_dist_words[key] = n_dist
            n_comm[key] = n_common
            n_uncomm[key] = n_uncommon
            uncommons[key] = un_comm
            commons[key] = comm

            fd = nltk.FreqDist(uncommon_corpus)
            ffd = dict((word, freq) for word, freq in fd.items() if not word in punctuation and not word.isdigit())
            freq10 = sorted(ffd.items(), key=lambda x: x[1], reverse=True)
            most_freq[key] = freq10[:10]
            f.write(f"{key} -> Most Frequent: {freq10}\n\n")

            fd = nltk.FreqDist(ts)
            ffd = dict((word, freq) for word, freq in fd.items() if not word in punctuation and not word.isdigit())
            ffds = sorted(ffd.items(), key=lambda x: x[1], reverse=True)
            histogram[key] = ffds

        f.write("\n\n")

    with open(rep, 'a+') as f:
        f.write("TFIDF:\n")



        tfidf_corpora = [' '.join(c) for k, c in tokens.items() if k != 'ALL']
        vectorizer = TfidfVectorizer(analyzer='word',stop_words= 'english')

        tfidf_wm = vectorizer.fit_transform(tfidf_corpora)
        tfidf_tokens = vectorizer.get_feature_names()
        columns = [key for key, cc in tokens.items() if key != 'ALL']

        df = pd.DataFrame(data = tfidf_wm.T.toarray(), index = tfidf_tokens, columns = columns)

        for label in columns:

            top_df = df.nlargest(10, label)[label]
            top_tuples = list(top_df.iteritems())

            top_tfidf[label] = top_tuples.copy()

            f.write(f"\n\t{label}:\n")
            for t in top_tuples:
                f.write(f"\t{t[0]} -> {t[1]}\n")

        f.write("\n\nRNF:\n")
        for label in columns:
            rnfs = []

            pcorpus = []
            for k, v in tokens.items():
                if k != label and k != 'ALL':
                    pcorpus += v

            for word in commons[label]:
                l1c = tokens[label].count(word)
                l2c = pcorpus.count(word)

                l1n = len(tokens[label])
                l2n = len(pcorpus)

                rnf = (l1c / l1n) / (l2c / l2n)

                rnfs.append((word, rnf))

            rnfs.sort(key=lambda tup: tup[1], reverse=True)
            tops = rnfs[:10]

            top_rnf[label] = tops

            f.write(f"\n\t{label}:\n")
            for t in tops:
                f.write(f"\t{t[0]} -> {t[1]}\n")

        ### Visualize

        bar_chart(n_dial, 'Units per Label', 'Label', 'Dialogue')

        bar_chart(n_sents, 'Sentence per Label', 'Label', 'Sentence')

        bar_chart(n_words, 'Words per Label', 'Label', 'Word')

        bar_chart(n_dist_words, 'Distinct words per Label', 'Label', 'Word')

        bar_chart(n_comm, 'Common words per Label', 'Label', 'Word')

        bar_chart(n_uncomm, 'Uncommon words per Label', 'Label', 'Word')

        freq_chart(most_freq, 0)

        freq_chart(top_rnf, 1)

        freq_chart(top_tfidf, 2)

        freq_chart(histogram, 3)
