from expert import *
import os
import system
import pickle

def main():

  if len(sys.argv) == 2:
    model_dir = sys.argv[1]
  else:
    print "\nError: Use the following syntax:\n \
        read_models.py <model_directory>\n"
    return


  inverse_models = []
  forward_models = []


  os.chdir("./" + model_dir)

  '''
  list_dir = os.listdir("./")
  for i in range(len(list_dir)): # number models
    IMfilename = "R" + str(i) + "INV.py"
    FMfilename = "R" + str(i) + "FWD.py"
    if IMfilename in list_dir:
      inverse_models.append(pickle.load(open(IMfilename,"rb")))
      forward_models.append(pickle.load(open(FMfilename,"rb")))
  '''
  i = 0
  dirlist = os.listdir('.')
  #while 'R' + str(i) + 'INV.pickle' not in dirlist:
    #i += 1
  #im = pickle.load(open('R' + str(i) + 'INV.pickle', "rb"))
  im = pickle.load(open('R3INV.pickle', "rb"))
  print im.name
  print im.meanErrorRate(0)

main()
