from glob import glob
import os
import nltk

def Stem():
    dir = '../data/stemming/'

    if not os.path.exists(dir):
        os.makedirs(dir)
        print("Stemming -> Running...")
    else:
        print("Stemming -> exists, Skipping...\n")
        return True

    files = glob("../data/stopwords/*.txt")

    snowball_stemmer = nltk.stem.SnowballStemmer('english')

    for path in files:
        head, tail = os.path.split(path)

        with open(path, "r") as fr:
            with open(os.path.join(dir, tail), "w+") as fw:
                tokens = fr.read()
                tokens = tokens.split(' ')
                final = [snowball_stemmer.stem(word) for word in tokens]
                fw.writelines("%s " % token for token in final)
    print("Stemming -> Done\n")
    return True
