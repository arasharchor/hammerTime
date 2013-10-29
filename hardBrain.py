from pyrobot.brain import Brain
import os
from hammerTimeTrain import *  # Import the task here
from hardBrainTrial import *
from time import sleep, time


# Define the robot's brain class

import os

class HardBrain(Brain):
   def setup(self):
      self.steps = 0
      self.camera = self.robot.camera[0]
 
      self.task=TrainHammerTime(self.robot)
      self.past_sensors = []
      self.counter = 0

      self.num_trials = input("Number of trials: ")
      self.trial_counter = 0
      self.trial = HardBrainTrial()

      os.system("if [ -d 'hardBrainTrials' ]; then rm -rf hardBrainTrials; fi")
      os.mkdir('hardBrainTrials')
      os.chdir('hardBrainTrials')
 
   def step(self):
      """
      filterResults has the following format
         [area of biggest blob, ((x1, y1, x2, y2, area) ...)]
      where the second component is a list of bounding box info
      for each blob of the matched color in descending order by
      size of area.
      """

      time_started = time()

      # on the first time step, add the starting locations of the puck and robot to self.trial
      if self.counter == 0:
         robotX, robotY, heading = self.robot.simulation[0].getPose("Pioneer1")
         red_puckX, red_puckY, heading = self.robot.simulation[0].getPose("redball")
         green_puckX, green_puckY, heading = self.robot.simulation[0].getPose("greenball")

         if red_puckX >= 3.625:
            # the red puck is currently in the robot's "pen"
            self.trial.ball_loc = (red_puckX, red_puckY)
            self.trial.ball_color = "red"
         else:
            # the green puck is currently in the robot's "pen"
            self.trial.ball_loc = (green_puckX, green_puckY)
            self.trial.ball_color = "green"

         self.trial.robot_loc = (robotX, robotY)

      if self.robot.stall or (self.counter > 4 and self.checkSensors()):
         print "Robot stalled. Trial ending..."
                  
         self.trial.saveTrialToFile("hardBrainTrial" + str(self.trial_counter))

         if self.trial_counter < self.num_trials:
            self.trial_counter += 1
            print "Continuing with trial %d..." % self.trial_counter
            self.counter = 0
            self.task.resetEnvironment()
         else:
            self.pleaseStop()
            self.robot.move(0, 0)

            print "Experiment complete!"

         self.trial = HardBrainTrial()
            
         
      else:
         results = self.robot.camera[0].filterResults

         # find the index i of the largest non-zero blob in results
         
         i = None
         if len(results) > 0:
            for index in range(len(results)-1,-1,-1):
               if sum(results[index][0]) > 0:
                  i = index
                  break

            if i != None and sum(results[i][0]) > 0:
                # have a blob in sight
                x1, y1, x2, y2, area = results[i][0]
                centerX = (x1 + x2)/2
                diff = (centerX - (self.camera.width/2))
                if abs(diff) < (.05 * self.camera.width):
                   # puck is straight ahead
                   motors = [0.3, 0]
                elif diff < 0:
                   # puck is to the left
                   motors = [0.2, 0.3] 
                else:
                   # puck is to the right
                   motors = [0.2, -0.3]
            else:
               # no blob in sight
               motors = [0, 0.5]
         else:
            # no match for blobify
            motors = [0, 0.5]

         self.trial.motorLog.append(motors)
        
         sensors = self.task.getSensors()
         self.trial.sensorLog.append(sensors)

         if len(self.past_sensors) ==4:
             del self.past_sensors[0]
         self.past_sensors.append(sensors[0])

         self.robot.move(motors[0], motors[1])

         time_ended = time()
         step_duration = time_ended - time_started
         #print step_duration
         #self.sleep
         self.counter += 1


   def checkSensors(self):
      """
      Used to check to see whether or not the robot has stalled (i.e. run into a wall)
      Computes the difference between each successive element in self.past_sensors.
      Returns True if the maximum difference is < .005, and False otherwise.
      """
      max_diff = -1
      for index, sensors in enumerate(self.past_sensors[:-1]):
         curr_diff = abs(sensors - self.past_sensors[index+1])
         if curr_diff > max_diff:
            max_diff = curr_diff
      if max_diff < .004:
         return True
      return False

# Create a brain for the robot
def INIT(engine):
   return HardBrain('HardBrain', engine)

if __name__ == '__main__':
    os.system('pyrobot -s PyrobotSimulator -w babblingWorld.py -r PyrobotRobot60000.py -b hardBrain.py')

