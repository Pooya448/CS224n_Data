import contractions
from glob import glob
import os
import nltk

def Wtokenize():
    dir = '../data/word_tokenize/'

    if not os.path.exists(dir):
        os.makedirs(dir)
        print("Word Tokenize -> Running...")
    else:
        print("Word Tokenize -> exists, Skipping...\n")
        return True

    files = glob("../data/contractions/*.txt")

    for path in files:
        head, tail = os.path.split(path)

        with open(path, "r") as fr:
            with open(os.path.join(dir, tail), "w+") as fw:
                corpus = fr.read()
                corpus = corpus.replace("\n", " ")
                tokens = nltk.word_tokenize(corpus)
                fw.writelines("%s " % token for token in tokens)
    print("Word Tokenize -> Done\n")
    return True
