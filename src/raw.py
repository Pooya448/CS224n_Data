import os
import subprocess

def Raw():
    path = '../data/raw/'

    if not os.path.exists(path):
        os.makedirs(path)
        print("Raw -> Running...")
    else:
        print("Raw -> exists, Skipping...\n")
        return True

    code = subprocess.call(["chmod", "755", "download.sh"])
    if code == 0:
        fcode = subprocess.call(["bash", "download.sh"])

    print("Raw -> Done\n")
    return fcode == 0
