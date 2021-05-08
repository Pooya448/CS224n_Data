import contractions
from glob import glob
import os
import nltk

def Stokenize():
    dir = '../data/sentence_tokenize/'

    if not os.path.exists(dir):
        os.makedirs(dir)
        print("Sentence Tokenize -> Running...")
    else:
        print("Sentence Tokenize -> exists, Skipping...\n")
        return True

    files = glob("../data/contractions/*.txt")

    for path in files:
        head, tail = os.path.split(path)

        with open(path, "r") as fr:
            with open(os.path.join(dir, tail), "w+") as fw:
                corpus = fr.read()
                corpus = corpus.replace("\n", " ")
                tokens = nltk.sent_tokenize(corpus)
                fw.writelines("%s\n" % token for token in tokens)
    print("Sentence Tokenize -> Done\n")
    return True
