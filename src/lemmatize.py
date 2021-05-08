from glob import glob
import os
import nltk

def Lemmatize():
    dir = '../data/lemmatize/'

    if not os.path.exists(dir):
        os.makedirs(dir)
        print("Lemmatization -> Running...")
    else:
        print("Lemmatization -> exists, Skipping...\n")
        return True

    files = glob("../data/stopwords/*.txt")

    wordnet_lemmatizer = nltk.stem.WordNetLemmatizer()

    for path in files:
        head, tail = os.path.split(path)

        with open(path, "r") as fr:
            with open(os.path.join(dir, tail), "w+") as fw:
                tokens = fr.read()
                tokens = tokens.split(' ')
                final = [wordnet_lemmatizer.lemmatize(word) for word in tokens]
                fw.writelines("%s " % token for token in final)
    print("Lemmatization -> Done\n")
    return True
