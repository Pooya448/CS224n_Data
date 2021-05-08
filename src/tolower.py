from glob import glob
import random
import os

def Lower():
    dir = '../data/tolower/'

    if not os.path.exists(dir):
        os.makedirs(dir)
        print("ToLower -> Running...")
    else:
        print("ToLower -> exists, Skipping...\n")
        return True

    files = glob("../data/clean/dialogue/*.txt")

    for path in files:
        head, tail = os.path.split(path)

        with open(path, "r") as fr:
            with open(os.path.join(dir, tail), "w+") as fw:
                corpus = fr.read()
                fw.write(corpus.lower())

    print("ToLower -> Done\n")
    return True
