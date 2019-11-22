from utils import save_load_obj
from tqdm import tqdm
import numpy as np
import os
from nilearn.input_data import NiftiMasker
from nilearn import image
import glob
import warnings
warnings.filterwarnings('ignore')


class FinalDataPrep:
    def __init__(self):
        self.data_dir = "/home/krutika/Git/fmri-preprocess/data"
        self.ROIs = ["FFA", "hV4", "HVC", "LOC", "PPA", "V1", "V2", "V3"]
        self.num_of_subjs = 5
        self.num_of_img_per_run = 50
        self.destination_dir = os.path.join(self.data_dir, "final_data")
        if not os.path.isdir(self.destination_dir):
            os.mkdir(self.destination_dir)
        self.image_details = {}
        with open("/home/krutika/Data/ds001246-download/stimulus_ImageNetTraining.tsv", "r") as imges_details_file:
            content = imges_details_file.read()
            rows = content.split("\n")
            rows = [row.split("\t") for row in rows]
            for row in rows:
                self.image_details[row[3]] = {
                    "image_name": row[0],
                    "stimulus_id": row[1],
                    "category": row[2]
                }

    def get_training_dirs(self, subj):
        return [os.path.join(self.data_dir, subj, "ses-perceptionTraining01", "func"),
                os.path.join(self.data_dir, subj,
                             "ses-perceptionTraining02", "func"),
                os.path.join(self.data_dir, subj,
                             "ses-perceptionTraining03", "func"),
                os.path.join(self.data_dir, subj,
                             "ses-perceptionTraining04", "func"),
                os.path.join(self.data_dir, subj, "ses-perceptionTraining05", "func")]

    def run(self):
        for i in tqdm(range(1, self.num_of_subjs+1)):
            subj = "sub-0"+str(i)
            file_name = os.path.join(self.destination_dir, subj+".pkl")
            if not os.path.isfile(file_name):
                self.dirs = self.get_training_dirs(subj)
                final_data = {}
                final_data["roi_names"] = self.ROIs
                final_data["roi_data"] = {}

                for roi_name in tqdm(self.ROIs):
                    final_tstat = np.array([])
                    final_pe = np.array([])
                    final_cope = np.array([])
                    image_names = np.empty((1200), dtype="<U20")
                    category = np.empty((1200), dtype="<U10")
                    stimulus_id = np.empty((1200), dtype="<U20")

                    for _dir in self.dirs:
                        if os.path.isdir(_dir):
                            names = glob.glob(_dir+"/*.feat")
                            for feat_folder in names:
                                run_timingfiles_path = os.path.join(
                                    _dir,  feat_folder.split("_")[-2])
                                timing_files = glob.glob(
                                    run_timingfiles_path + "/*.txt")
                                timing_files.sort()
                                for num in range(1, self.num_of_img_per_run+1):
                                    tstat_addr = os.path.join(feat_folder, "stats",
                                                              "tstat"+str(num)+".nii.gz")
                                    pe_addr = os.path.join(feat_folder, "stats",
                                                           "pe"+str(2*num - 1)+".nii.gz")
                                    cope_addr = os.path.join(feat_folder, "stats",
                                                             "cope"+str(num)+".nii.gz")
                                    mask_addr = os.path.join(
                                        self.data_dir, "sourcedata", subj, "anat", subj+"_mask_"+roi_name+".nii.gz")
                                    mask = image.load_img(mask_addr)
                                    masker = NiftiMasker(
                                        mask_img=mask, standardize=True)
                                    tstat = masker.fit_transform(tstat_addr)
                                    pe = masker.fit_transform(pe_addr)
                                    cope = masker.fit_transform(cope_addr)

                                    if final_tstat.shape[0] == 0:
                                        final_tstat = np.zeros(
                                            (1200, tstat.shape[1]))
                                        final_pe = np.zeros(
                                            (1200, pe.shape[1]))
                                        final_cope = np.zeros(
                                            (1200, cope.shape[1]))
                                    ind = int(
                                        timing_files[num-1].split("/")[-1].split(".")[0]) - 1
                                    final_tstat[ind] = tstat
                                    final_pe[ind] = pe
                                    final_cope[ind] = cope
                                    image_names[ind] = self.image_details[str(
                                        ind+1)]["image_name"]
                                    category[ind] = self.image_details[str(
                                        ind+1)]["category"]
                                    stimulus_id[ind] = self.image_details[str(
                                        ind+1)]["stimulus_id"]

                    final_data["roi_data"][roi_name] = {}
                    final_data["roi_data"][roi_name]["tstat"] = final_tstat
                    final_data["roi_data"][roi_name]["cope"] = final_cope
                    final_data["roi_data"][roi_name]["pe"] = final_pe
                    final_data["stimulus_id"] = stimulus_id
                    final_data["category"] = category
                    final_data["image_name"] = image_names

                save_load_obj.save_obj(final_data, file_name)


FinalDataPrep().run()
