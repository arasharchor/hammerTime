from pyrobot.brain.conx import *

class Expert:
    def __init__(self, inputVectorSize, targetVectorSize, timeWindow, smoothing, name):
        self.inputs = []
        self.targets = []
        self.trace = []
        self.errors = []
        self.timeWindow = timeWindow
        self.smoothing = smoothing
        self.inputVectorSize = inputVectorSize
        self.targetVectorSize = targetVectorSize
        self.name = name
        
        self.nnet = Network()
        self.nnet.addLayer("input", self.inputVectorSize)
        self.nnet.addLayer("output", self.targetVectorSize)
        self.nnet.connect("input", "output")
        self.nnet.resetEpoch = 1
        self.nnet.resetLimit = 1
        self.nnet.momentum = 0
        self.nnet.epsilon = 0.5

    def trainExpert(self):
        """
        Train the expert's most recent exemplar.
        """
        self.nnet.step(input = self.inputs[-1], output = self.targets[-1])

    def trainExpertOnAll(self):
        """
        Train the expert on all exemplars.
        """
        self.nnet.setInputs(self.inputs)
        self.nnet.setOutputs(self.targets)
        self.nnet.train()

    def askExpert(self, input):
        """
        Find out what the expert predicts for the given input.
        """
        self.nnet['input'].copyActivations(input)
        self.nnet.propagate()
        return self.nnet['output'].activation

    def getTargets(self):
        return self.targets

    def storeError(self, error, step):
        """
        Errors are stored with the most recent at the head of the list.
        """
        self.errors.insert(0, error)
        n = self.timeWindow + self.smoothing
        if len(self.errors) > n:
            self.trace.append((step, sum(self.errors[:n])/float(n)))

    def makeErrorGraph(self):
        if len(self.trace) == 0:
            return
        fp = open(self.name + ".err", "w")
        for step, err in self.trace:
            fp.write("%d %.6f\n" % (step, err))
            fp.flush()
        fp.close()

    def learningProgress(self):
        """
        Returns the learning progress which is an approximation of
        the first derivative of the error.
        """
        if len(self.errors) < (self.timeWindow + self.smoothing + 1):
            return 0
        decrease = self.meanErrorRate(0) - self.meanErrorRate(self.timeWindow)
        return  -1 * decrease

    def meanErrorRate(self, start):
        """
        Returns the average error rate over self.smoothing steps
        starting from the given start index.
        """
        result = 0
        end = start + self.smoothing + 1
        if end > len(self.errors):
            return 0
        for i in range(start, end, 1):
            result += self.errors[i]
        return result / float(self.smoothing + 1)

    def addExemplar(self, input, target):
        """
        Adds the given input and target to the appropriate lists.
        """
        self.inputs.append(input)
        self.targets.append(target)

    def exemplarsToStr(self):
        if len(self.inputs) < 5:
            return ""
        result = ""
        for i in range(1,5):
            result += "Input: "
            for inVal in self.inputs[-i]:
                result += "%.3f " % inVal
            result += "\n"
            result += "Target: "
            for tarVal in self.targets[-i]:
                result += "%.3f " % tarVal
            result += "\n"
        return result

    def saveExpertToFile(self, filename):
        import pickle
        self.name = filename
        basename = filename.split('.')[0]
        filename += ".pickle"
        fp = open(filename, 'w')
        pickle.dump(self, fp)
        fp.close()





