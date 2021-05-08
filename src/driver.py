def quit():
    print("Wrong arguments, terminating...")
    exit()

import sys

args = sys.argv[1:]
n_arg = len(args)

if n_arg == 0:
    phase = 8
    analysis = False
elif n_arg == 1:
    if args[0] == "--analysis":
        phase = 8
        analysis = True
    elif not isinstance(args[0], str) and 0 <= int(args[0]) <= 8:
        phase = int(args[0])
        analysis = False
    else:
        quit()
elif n_arg == 2:
    phase = int(args[0])
    if args[1] == "--analysis":
        analysis = True
    else:
        quit()
else:
    quit()


from preprocess import Preprocess
from analysis import Analyze

current_status = Preprocess(phase=phase, force=False)

req_status = 8
if analysis:

    print(f"Required preprocess stage -> {req_status}")
    print(f"Current preprocess stage -> {current_status}\n")

    if current_status < req_status:
        Preprocess(phase=req_status, force=True)
        print(f"\nReprocessing to stage {req_status} with Force=True\n")

    print("Analysis -> Running...")
    Analyze()
    print("Analysis -> Done\n")

def quit():
    print("Wrong arguments, terminating...")
    exit()
