import os
import system
import sys
import glob
import random

def main():
  """
  Randomly displays a given number of error graphs. If no number is given, all the error
  files in the given directory are graphed
  """
  num_models_to_graph = None
  if len(sys.argv) == 3:
      directory = sys.argv[1]
      num_models_to_graph = int(sys.argv[2])
  elif len(sys.argv) == 2:
      directory = sys.argv[1]
  else:
      print "Error. Use the following format:\tpython graph_error.py <directory> <number_graphs>"
      return
      
  os.chdir(directory)
  # a list of all the error files 
  inverse_files = glob.glob(os.path.join(".", "*INV.err"))

  if num_models_to_graph == None:
      num_models_to_graph = len(inverse_files)

  
  #list_dir = os.listdir(". *.err")
  forward_files = glob.glob(os.path.join(".", "*FWD.err"))

  inverse_command = ""
  forward_command = ""
  for i in range(num_models_to_graph):
      inverse_error = random.choice(inverse_files)
      inverse_command += (inverse_error + " ")
      inverse_files.remove(inverse_error)

      forward_error = random.choice(forward_files)
      forward_command += (forward_error + " ")
      forward_files.remove(forward_error)

  os.system("xgraph -P " + inverse_command + " &")
  os.system("xgraph -P " + forward_command + " &")
   
main()
