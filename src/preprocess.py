import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

from raw import Raw
from clean import Clean
from tolower import Lower
from contraction import Contraction
from word_tokenize import Wtokenize
from sentence_tokenize import Stokenize
from stopword import Stopword
from lemmatize import Lemmatize
from stemmer import Stem

import subprocess

def Preprocess(phase=8, force=False):

    if force:
        parent_dir = "../data/"
        subprocess.call(["rm", "-rf", f"{parent_dir}"])

    status = -1

    if phase >= 0:
        raw_status = Raw()
        if raw_status:
            status += 1

    if phase >= 1 and status == 0:
        clean_status = Clean()
        if clean_status:
            status += 1

    if phase >= 2 and status == 1:
        lower_status = Lower()
        if lower_status:
            status += 1

    if phase >= 3 and status == 2:
        contractions_status = Contraction()
        if contractions_status:
            status += 1

    if phase >= 4 and status == 3:
        wtokenize_status = Wtokenize()
        if wtokenize_status:
            status += 1

    if phase >= 5 and status == 4:
        stokenize_status = Stokenize()
        if stokenize_status:
            status += 1

    if phase >= 6 and status == 5:
        stopword_status = Stopword()
        if stopword_status:
            status += 1

    if phase >= 7 and status == 6:
        lemm_status = Lemmatize()
        if lemm_status:
            status += 1

    if phase >= 8 and status == 7:
        stem_status = Stem()
        if stem_status:
            status += 1

    return status
