
class HardBrainTrial:
    def __init__(self):

        # the initial starting conditions of the (somewhat) randomly initialized
        # balls and robots
        self.ball_loc, self.ball_color, self.robot_loc = None, None, None
        
        # sensor and motor data
        self.sensorLog = []
        self.motorLog = []

        # a dictionary to store as keys the names of CBIM trials,
        # and as values the 'HAMMER-TIMED' motor actions associated with each
        # CBIM trial
        self.hammerMotors = {}

        # a dictionary to store as keys the names of CBIM trials,
        # and as values the error associated with each trial's 'HAMMER-TIMED'
        # motor actions
        self.error = {}

    def addHammerMotors(self, cbim_trial_name, hammerMotors):
        """
        Adds a CBIM trial name and its corresponding 'HAMMER-TIMED' motor
        actions to the hammerMotors dictionary
        """
        self.hammerMotors[cbim_trial_name] = hammerMotors

    def saveTrialToFile(self, name):
        """
        Pickles the trial
        """
        import pickle
        fp = open(name + ".pickle", 'w')
        pickle.dump(self, fp)
        fp.close()

    def computeTotalError(self):
        """
        Returns the error between the motorLog and the HAMMER-TIMED motors
        for each cbim trial in the form [[<cbim_trial1_name>, <error>],
                                         [<cbim_trial2_name>, <error>], ... ]
        """
        for cbim_trial in self.hammerMotors.keys():
            self.error[cbim_trial] = \
                           self.computeTrialError(self.hammerMotors[cbim_trial])

    def computeTrialError(self, hammerMotors_trial):
        """
        Returns the error between the HAMMER-TIMED motors of a particular trial
        and self.motorLog
        """
        return sum([(hammerMotors_trial[i][0]-self.motorLog[i][0])**2 + \
                    (hammerMotors_trial[i][1]-self.motorLog[i][1])**2 \
                    for i in range(len(hammerMotors_trial))])

    def printError(self):
        """
        Prints the name of each CBIM trial along with the error of the trial's
        HAMMER-TIMED actions
        """
        for cbim_trial in self.error.keys():
            print "Error for ", cbim_trial, ": ", self.error[cbim_trial]




