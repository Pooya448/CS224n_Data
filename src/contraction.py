import contractions as con
from glob import glob
import os

def Contraction():
    dir = '../data/contractions/'

    if not os.path.exists(dir):
        os.makedirs(dir)
        print("Contractions -> Running...")
    else:
        print("Contractions -> exists, Skipping...\n")
        return True

    files = glob("../data/tolower/*.txt")

    for path in files:
        head, tail = os.path.split(path)

        with open(path, "r") as fr:
            with open(os.path.join(dir, tail), "w+") as fw:
                corpus = fr.read()
                fixed = con.fix(corpus)
                fw.write(fixed)

    print("Contractions -> Done\n")
    return True
