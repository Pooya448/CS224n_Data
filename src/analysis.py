from glob import glob
import os
import nltk
from string import punctuation

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

    n_dial = {}
    n_sents= {}
    n_words = {}
    n_dist_words = {}
    n_comm = {}
    uncommons = {}
    most_freq = {}
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
            n_comm[key] = (n_common, n_uncommon)
            uncommons[key] = un_comm

            fd = nltk.FreqDist(uncommon_corpus)
            ffd = dict((word, freq) for word, freq in fd.items() if not word in punctuation and not word.isdigit())
            freq10 = sorted(ffd.items(), key=lambda x: x[1], reverse=True)[:9]
            most_freq[key] = freq10
            f.write(f"{key} -> Most Frequent: {freq10}\n\n")

            fd = nltk.FreqDist(ts)
            ffd = dict((word, freq) for word, freq in fd.items() if not word in punctuation and not word.isdigit())
            histogram[key] = ffd

        f.write("\n\n")
