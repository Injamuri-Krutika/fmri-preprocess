import os
import glob
import numpy as np
import shutil


class Make_FSL_Timings:
    def __init__(self):
        self.image_details = {}
        with open("/home/krutika/Data/ds001246-download/stimulus_ImageNetTraining.tsv", "r") as imges_details_file:
            content = imges_details_file.read()
            rows = content.split("\n")
            rows = [row.split("\t") for row in rows]
            for row in rows:
                self.image_details[row[0]] = {
                    "num": row[3],
                    "category": row[2]
                }

    def run(self):

        data_dir = "../data"
        for i in range(1, 6):
            subj = "sub-0"+str(i)
            dirs = [os.path.join(data_dir, subj, "ses-perceptionTraining01"),
                    os.path.join(data_dir, subj, "ses-perceptionTraining02"),
                    os.path.join(data_dir, subj, "ses-perceptionTraining03"),
                    os.path.join(data_dir, subj, "ses-perceptionTraining04"),
                    os.path.join(data_dir, subj, "ses-perceptionTraining05")]
            for _dir in dirs:
                if os.path.isdir(_dir):
                    names = glob.glob(_dir+"/func/*.tsv")
                    for name in names:
                        run = os.path.join(_dir, "func", name.split("_")[-2])
                        self.createTimingFiles(run, name)

    def createTimingFiles(self, run_dir_path, tsv_file_name):
        if not os.path.isdir(run_dir_path):
            os.mkdir(run_dir_path)
            with open(tsv_file_name, "r") as run_file:
                count = 1
                rows = run_file.read().split("\n")
                rows = [row.split("\t") for row in rows]
                for row in rows:
                    if count == 2 or count == 58:
                        file_name = os.path.join(
                            run_dir_path, "rest"+".txt")
                        with open(file_name, "a") as timing_file:
                            timing_file.write(
                                row[0]+" "+row[1]+" 1\n")
                    elif count > 2 and count < 58:
                        file_name = os.path.join(
                            run_dir_path, self.image_details[row[5]]["num"]+".txt")
                        with open(file_name, "a") as timing_file:
                            timing_file.write(
                                row[0]+" "+row[1]+" 1\n")
                    count += 1
        else:
            shutil.rmtree(run_dir_path)
            self.createTimingFiles(run_dir_path, tsv_file_name)


Make_FSL_Timings().run()
