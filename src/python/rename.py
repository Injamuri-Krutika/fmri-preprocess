import os
import glob


def rename(names):
    for name in names:
        if ":" in name:
            new_name = name.split(":")[-1]
            temp = name.split("/")
            temp[-1] = new_name
            # print("New name: ", "/".join(temp))
            os.rename(name, "/".join(temp))


for i in range(1, 6):
    dirs = ["../data/sub-0"+str(i)+"/ses-perceptionTraining01",
            "../data/sub-0"+str(i)+"/ses-perceptionTraining02",
            "../data/sub-0"+str(i)+"/ses-perceptionTraining03",
            "../data/sub-0"+str(i)+"/ses-perceptionTraining04",
            "../data/sub-0"+str(i)+"/ses-perceptionTraining05"]

    for _dir in dirs:
        if os.path.isdir(_dir):
            names = glob.glob(_dir + "/func/*.tsv")
            rename(names)
