import os
import pickle

    
def main():

    # will assume that the name of the trial is also the name of the directory
    # in which that trial's experts are stored
    cbim_trials = ['25k_limitCandActs', '25k_limitCandActs_errThresh95', '7k_1001']

    os.system("if [ -d 'graph_data' ]; then rm -rf graph_data; fi")
    os.mkdir('graph_data')

    for trial_num, cbim_trial in enumerate(cbim_trials):
        print cbim_trial 
        inverse_models = []
        forward_models = []

        os.chdir(cbim_trial)
        list_dir = os.listdir("./")
        i = 0
        while i < 50:
            IMfilename = "R" + str(i) + "INV.pickle"
            FMfilename = "R" + str(i) + "FWD.pickle"
            if IMfilename in list_dir:
                print IMfilename
                im  = pickle.load(open(IMfilename, "rb"))
                print im.name
                fm = pickle.load(open(FMfilename, "rb"))
                print fm.name
                inverse_models.append(im)
                forward_models.append(fm)
                list_dir.remove(IMfilename)
                list_dir.remove(FMfilename)
            i += 1
        
        invErrReducs = getErrReducs(inverse_models)
        meanInvErrReduc = mean(invErrReducs)

        fwdErrReducs = getErrReducs(forward_models)
        meanFwdErrReduc = mean(fwdErrReducs)
        
        invMeanErrors = getMeanErrors(inverse_models)
        meanInvMeanError = mean(invMeanErrors)

        fwdMeanErrors = getMeanErrors(forward_models)
        meanFwdMeanError = mean(fwdMeanErrors)

        totalMeanErrReduc = (meanFwdErrReduc + meanInvErrReduc)/2.0
        totalMeanError = (meanInvMeanError + meanFwdMeanError)/2.0

        os.chdir('../graph_data')

        if trial_num == 0:
            mier = open('meanInvErrReduc.dat', 'w')
            mfer = open('meanFwdErrReduc.dat', 'w')
            mime = open('meanInvMeanError.dat', 'w')
            mfme = open('meanFwdMeanError.dat', 'w')
            tmer = open('totalMeanErrReduc.dat', 'w')
            tme = open('totalMeanError.dat', 'w')

        mier.write('%d %.6f\n' % (trial_num, meanInvErrReduc))
        mfer.write('%d %.6f\n' % (trial_num, meanFwdErrReduc))
        mime.write('%d %.6f\n' % (trial_num, meanInvMeanError))
        mfme.write('%d %.6f\n' % (trial_num, meanFwdMeanError))
        tmer.write('%d %.6f\n' % (trial_num, totalMeanErrReduc))
        tme.write('%d %.6f\n' % (trial_num, totalMeanError))
        
        mier.flush()
        mfer.flush()
        mime.flush()
        mfme.flush()
        tmer.flush()
        tme.flush()

        fp = open('errReducs_' + cbim_trial, 'w')
        assert(len(fwdErrReducs) == len(invErrReducs))
        for i in range(len(fwdErrReducs)):
            fp.write('%d %.6f %.6f\n' % (i, fwdErrReducs[i], invErrReducs[i]))
            fp.flush()
        fp.close()

        fp = open('meanErrors_' + cbim_trial + , 'w')
        assert(len(fwdMeanErrors) == len(invMeanErrors))
        for i in range(len(fwdMeanErrors)):
            fp.write('%d %.6f %.6f\n' % (i, fwdMeanErrors[i], invMeanErrors[i]))
            fp.flush()
        fp.close()

        os.chdir('..')

        # [[region1_meanError, region1_meanErrReduc], 
        #  [region2_meanError, region2_meanErrReduc],
        #  [...]]
        #regionErrors = []

        # [[error of HAMMER-TIMED motors for hardBrainTrial1, error in distance],
        #  [error of HAMMER-TIMED motors for hardBrainTrial2, error in distance],
        #  [...]]
        # hammerMotorErr = []

    mier.close()
    mfer.close()
    mime.close()
    mfme.close()
    tmer.close()
    tme.close()

    os.chdir('graph_data')
    os.system('xgraph -P meanInvErrReduc.dat meanFwdErrReduc.dat meanInvMeanError.dat meanFwdMeanError.dat totalMeanErrReduc.dat totalMeanError.dat &')
    os.chdir('..')

def getMeanErrors(experts):
    """
    experts is an array of Expert() instances
    Returns an array containing the average error rate of each expert in experts.
    """
    return [mean(expert.errors) for expert in experts]

def getErrReducs(experts):
    """
    Returns the reduction in error for each expert in experts
    """
    return [float(expert.errors[-1] - expert.errors[0]) for expert in experts]

def writeArrayToFile(filename, array):
    """
    Writes a given array to a data file, where the ith line of the file
    is of the form: i array[i]
    """
    fp.open(filename,'w')
    for i, val in enumerate(array):
        fp.write('%d %.6f\n' % (i, val))
        fp.flush()
    fp.close()

def mean(number_array):
    return sum(number_array) / float(len(number_array))


main()
