from glob import glob
import os
import nltk

def Stopword():
    dir = '../data/stopwords/'

    if not os.path.exists(dir):
        os.makedirs(dir)
        print("Stopword Removal -> Running...")
    else:
        print("Stopword Removal -> exists, Skipping...\n")
        return True

    files = glob("../data/sentence_tokenize/*.txt")

    stopwords = nltk.corpus.stopwords.words('english')

    for path in files:
        head, tail = os.path.split(path)

        with open(path, "r") as fr:
            with open(os.path.join(dir, tail), "w+") as fw:
                tokens = fr.read()
                tokens = tokens.split(' ')
                final = [word for word in tokens if word not in stopwords]
                fw.writelines("%s " % token for token in final)
    print("Stopword Removal -> Done\n")
    return True
