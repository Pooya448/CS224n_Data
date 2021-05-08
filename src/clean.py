from glob import glob
import random
import os
import subprocess

def Clean():

    parent_dir = '../data/clean/'
    dialog_path = os.path.join(parent_dir, "dialogue") + os.path.sep
    corpora_path = os.path.join(parent_dir, "corpora") + os.path.sep

    par_flag = os.path.exists(parent_dir)
    di_flag = os.path.exists(dialog_path)
    cor_flag = os.path.exists(corpora_path)


    if par_flag and di_flag and cor_flag:
        print("Clean -> already done, Skipping...\n")
        return True
    else:
        subprocess.call(["rm", "-rf", f"{parent_dir}"])
        os.makedirs(dialog_path)
        os.makedirs(corpora_path)
        print("Clean -> Running...")

    files = glob("../data/raw/*.txt")
    random.shuffle(files)

    n_episodes = len(files)
    assert n_episodes == 228, "Some episodes are missing from the data."

    Chandler = []
    Phoebe = []
    Monica = []
    Rachel = []
    Ross = []
    Joey = []

    All = []
    dialogues = {}
    corpora = {}

    for file_path in files:
        with open(file_path, "r") as fp:
            for _, line in enumerate(fp):

                if line.startswith("Chandler:"):
                    Chandler.append(line[10:])
                    All.append(line[10:])

                elif line.startswith("Phoebe:"):
                    Phoebe.append(line[8:])
                    All.append(line[8:])

                elif line.startswith("Monica:"):
                    Monica.append(line[8:])
                    All.append(line[8:])

                elif line.startswith("Rachel:"):
                    Rachel.append(line[8:])
                    All.append(line[8:])

                elif line.startswith("Ross:"):
                    Ross.append(line[6:])
                    All.append(line[6:])

                elif line.startswith("Joey:"):
                    Joey.append(line[6:])
                    All.append(line[6:])

    dialogues['CHANDLER'] = ''.join(Chandler)
    dialogues['PHOEBE']= ''.join(Phoebe)
    dialogues['MONICA']= ''.join(Monica)
    dialogues['RACHEL']= ''.join(Rachel)
    dialogues['ROSS']= ''.join(Ross)
    dialogues['JOEY']= ''.join(Joey)
    dialogues['ALL']= ''.join(All)

    Chandler = list(map(str.strip, Chandler))
    Phoebe = list(map(str.strip, Phoebe))
    Monica = list(map(str.strip, Monica))
    Rachel = list(map(str.strip, Rachel))
    Ross = list(map(str.strip, Ross))
    Joey = list(map(str.strip, Joey))
    All = list(map(str.strip, All))

    corpora['CHANDLER'] = ' '.join(Chandler)
    corpora['PHOEBE']= ' '.join(Phoebe)
    corpora['MONICA']= ' '.join(Monica)
    corpora['RACHEL']= ' '.join(Rachel)
    corpora['ROSS']= ' '.join(Ross)
    corpora['JOEY']= ' '.join(Joey)
    corpora['ALL']= ' '.join(All)

    for key, character in dialogues.items():
        with open(f"{dialog_path}{key}.txt", 'w+') as fp:
            fp.write(character)

    for key, corpus in corpora.items():
        with open(f"{corpora_path}{key}.txt", 'w+') as fp:
            fp.write(corpus)

    print("Clean -> Done\n")
    return True
