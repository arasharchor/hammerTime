import os
import system
import pickle
from hardBrainTrial import *

def main():
    # assumes that all files in the dir are pickled trial classes
    os.chdir('./hardBrainTrials')
    dirlist = os.listdir('./')
    for trialname in dirlist:
        trial = pickle.load(open(trialname, "rb"))

        print len(trial.motorLog)
        print trial.hammerMotors.keys()
    # print trial.error
 

main()
