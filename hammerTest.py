from pyrobot.brain import Brain
import os
import pickle
import hardBrainTrial
from math import *
from time import *

class hammerTest(Brain):
  def setup(self):
    os.chdir("./hardBrainTrials")
    self.hardTrial_list = sorted(os.listdir("./"))
    self.oldHardList = sorted(os.listdir("./"))
    for i in range(len(self.hardTrial_list)):
      self.hardTrial_list[i] = pickle.load(open("./" + self.hardTrial_list[i], "rb"))
    self.curr_trial = self.hardTrial_list[0]
    self.curr_trial_index = 0
    self.curr_motors = self.curr_trial.motorLog
    self.cbim_trials = sorted(self.curr_trial.hammerMotors.keys())
    self.cbim_trials_index = 0
    self.counter = 0
    self.updateWorld()
    #self.motorPos = []
    #self.fileName = self.outFile = ""

  
  def step(self):
    """
    TO SAVE .dat FILES for graphing errors (only needed once)

    if self.curr_motors == self.curr_trial.motorLog:
      self.motorPos.append(self.robot.simulation[0].getPose("Pioneer1")[:-1])
    else:
      if self.counter == 0:
        self.fileName = self.oldHardList[self.curr_trial_index].strip('.pickle') + '__' + self.cbim_trials[self.cbim_trials_index].strip('/') + ".dat"
        self.outFile = open('./'+self.fileName,"wb")
      cbim_XY = self.robot.simulation[0].getPose("Pioneer1")[:-1]
      distDiff = sqrt((self.motorPos[self.counter][0] - cbim_XY[0])**2 + (self.motorPos[self.counter][1] - cbim_XY[1])**2)
      self.outFile.write(str(self.counter)+" "+str(distDiff)+'\n')
      if self.counter == len(self.curr_motors) - 1:
        self.outFile.close()
    """
    self.robot.move(self.curr_motors[self.counter][0],\
                    self.curr_motors[self.counter][1])
    if self.cbim_trials_index == 2:
      print [self.curr_motors[self.counter][0],self.curr_motors[self.counter][1]]
    if self.counter ==  len(self.curr_motors) - 1:      
      if self.curr_motors == self.curr_trial.motorLog: 
        print self.oldHardList[self.curr_trial_index].strip('.pickle'), self.cbim_trials[self.cbim_trials_index]
        self.curr_motors = self.curr_trial.hammerMotors[\
                           self.cbim_trials[self.cbim_trials_index]\
                           ]
        self.updateWorld()
        self.counter = 0

      elif self.cbim_trials[self.cbim_trials_index] != self.cbim_trials[-1]: 
        self.cbim_trials_index += 1
        self.curr_motors = self.curr_trial.hammerMotors[\
                           self.cbim_trials[self.cbim_trials_index]\
                           ]
        print self.oldHardList[self.curr_trial_index].strip('.pickle'), self.cbim_trials[self.cbim_trials_index]
        self.updateWorld()
        self.counter = 0
      elif self.curr_trial_index != len(self.hardTrial_list) - 1:     
        self.curr_trial_index += 1
        print self.oldHardList[self.curr_trial_index].strip('.pickle'), "actual_motorLog"
        self.curr_trial = self.hardTrial_list[self.curr_trial_index]
        self.updateWorld()
        if self.oldHardList[self.curr_trial_index].strip('.pickle')[-2:] in ['11','16','18','24','29','33','42','l7']:
          self.pleaseStop()
        self.counter = 0
        self.cbim_trials_index = 0
        self.curr_motors = self.curr_trial.motorLog
        self.motorPos = []
        
      else:
        print "DONE!"
    else:
      self.counter += 1

    
  def updateWorld(self):
    self.robot.simulation[0].setPose("Pioneer1",\
                                     self.curr_trial.robot_loc[0],\
                                     self.curr_trial.robot_loc[1],\
                                     3.14)
    greenX = self.robot.simulation[0].getPose("greenball")[0]
    redX = self.robot.simulation[0].getPose("redball")[0]
    if redX > greenX:
      self.robot.simulation[0].setPose("redball",\
                                       self.curr_trial.ball_loc[0],\
                                       self.curr_trial.ball_loc[1],\
                                       0)
    else:
      self.robot.simulation[0].setPose("greenball",\
                                       self.curr_trial.ball_loc[0],\
                                       self.curr_trial.ball_loc[1],\
                                       0)
    sleep(1)


def INIT(engine):
  return hammerTest('hammerTest',engine)

if __name__ == "__main__":
  os.system('pyrobot -s PyrobotSimulator -w projectWorld.py -r PyrobotRobot60000.py -b hammerTest.py')
