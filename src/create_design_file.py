import os
import glob
from tqdm import tqdm


class Create_Design:
    def run(self):
        design_file = ""
        data_dir = "/home/krutika/Data/ds001246-download/"
        for i in tqdm(range(1, 6)):
            subj = "sub-0"+str(i)
            dirs = [os.path.join(data_dir, subj, "ses-perceptionTraining01"),
                    os.path.join(data_dir, subj, "ses-perceptionTraining02"),
                    os.path.join(data_dir, subj, "ses-perceptionTraining03"),
                    os.path.join(data_dir, subj, "ses-perceptionTraining04"),
                    os.path.join(data_dir, subj, "ses-perceptionTraining05")]
            for _dir in dirs:
                if os.path.isdir(_dir):
                    names = glob.glob(_dir+"/func/*.nii.gz")
                    for file_path in names:
                        # design_file += basic(subj, )
                        run_num = file_path.split("_")[-2]
                        run_timingfiles_path = os.path.join(
                            _dir, "func", run_num)
                        timing_files = glob.glob(
                            run_timingfiles_path + "/*.txt")
                        timing_files.sort()
                        contrast_names = []
                        # timing_files = timing_files[46:]
                        tot_real_EVs = len(timing_files)*2
                        self.num_of_EVs = len(timing_files)
                        design_file += self.basic(subj, file_path,
                                                  len(timing_files), len(timing_files)-1)

                        for i, timing_file in enumerate(timing_files):
                            EV_name = timing_file.split("/")[-1].split(".")[0]
                            if EV_name != "rest":
                                contrast_names += [EV_name]
                            design_file += self.EV_details(i+1,
                                                           EV_name, timing_file)
                        design_file += self.contrast_ftest_details(
                            contrast_names, tot_real_EVs)
                        design_file += self.contrast_orig(contrast_names,
                                                          tot_real_EVs)
                        design_file += self.ftest(len(contrast_names))
                        design_file += self.final()
                        print(run_timingfiles_path, "design_" +
                              run_num+".fsf", contrast_names)
                        with open(os.path.join(_dir, "func", "design_"+run_num+".fsf"), "w") as design:
                            design.write(design_file)

    def basic(self, subj, file_path, num_of_EVs, num_of_contrasts):
        return"\n# FEAT version number\nset fmri(version) 6.00\n\n" +\
            "# Are we in MELODIC?\nset fmri(inmelodic) 0\n\n" +\
            "# Analysis level\n# 1 : First-level analysis\n# 2 : Higher-level analysis\nset fmri(level) 1\n\n" +\
            "# Which stages to run\n# 0 : No first-level analysis (registration and/or group stats only)\n# 7 : Full first-level analysis\n# 1 : Pre-processing\n# 2 : Statistics\nset fmri(analysis) 7\n\n" +\
            "# Use relative filenames\nset fmri(relative_yn) 0\n\n" +\
            "# Balloon help\nset fmri(help_yn) 1\n\n" +\
            "# Run Featwatcher\nset fmri(featwatcher_yn) 1\n\n" +\
            "# Cleanup first-level standard-space images\nset fmri(sscleanup_yn) 0\n\n" +\
            "# Output directory\nset fmri(outputdir) \"\"\n\n" +\
            "# TR(s)\nset fmri(tr) 3.000000\n\n" +\
            "# Total volumes\nset fmri(npts) 178\n\n" +\
            "# Delete volumes\nset fmri(ndelete) 0\n\n" +\
            "# Perfusion tag/control order\nset fmri(tagfirst) 1\n\n" +\
            "# Number of first-level analyses\nset fmri(multiple) 1\n\n" +\
            "# Higher-level input type\n# 1 : Inputs are lower-level FEAT directories\n# 2 : Inputs are cope images from FEAT directories\nset fmri(inputtype) 2\n\n" +\
            "# Carry out pre-stats processing?\nset fmri(filtering_yn) 1\n\n" +\
            "# Brain/background threshold, %\nset fmri(brain_thresh) 10\n\n" +\
            "# Critical z for design efficiency calculation\nset fmri(critical_z) 5.3\n\n" +\
            "# Noise level\nset fmri(noise) 0.66\n\n" +\
            "# Noise AR(1)\nset fmri(noisear) 0.34\n\n" +\
            "# Motion correction\n# 0 : None\n# 1 : MCFLIRT\nset fmri(mc) 1\n\n" +\
            "# Spin-history (currently obsolete)\nset fmri(sh_yn) 0\n\n" +\
            "# B0 fieldmap unwarping?\nset fmri(regunwarp_yn) 0\n\n" +\
            "# EPI dwell time (ms)\nset fmri(dwell) 0.7\n\n" +\
            "# EPI TE (ms)\nset fmri(te) 35\n\n" +\
            "# % Signal loss threshold\nset fmri(signallossthresh) 10\n\n" +\
            "# Unwarp direction\nset fmri(unwarp_dir) y-\n\n" +\
            "# Slice timing correction\n# 0 : None\n# 1 : Regular up (0, 1, 2, 3, ...)\n# 2 : Regular down\n# 3 : Use slice order file\n# 4 : Use slice timings file\n# 5 : Interleaved (0, 2, 4 ... 1, 3, 5 ... )\nset fmri(st) 0\n\n" +\
            "# Slice timings file\nset fmri(st_file) \"\"\n\n" +\
            "# BET brain extraction\nset fmri(bet_yn) 1\n\n" +\
            "# Spatial smoothing FWHM (mm)\nset fmri(smooth) 8.0\n\n" +\
            "# Intensity normalization\nset fmri(norm_yn) 0\n\n" +\
            "# Perfusion subtraction\nset fmri(perfsub_yn) 0\n\n" +\
            "# Highpass temporal filtering\nset fmri(temphp_yn) 1\n\n" +\
            "# Lowpass temporal filtering\nset fmri(templp_yn) 0\n\n" +\
            "# MELODIC ICA data exploration\nset fmri(melodic_yn) 0\n\n" +\
            "# Carry out main stats?\nset fmri(stats_yn) 1\n\n" +\
            "# Carry out prewhitening?\nset fmri(prewhiten_yn) 1\n\n" +\
            "# Add motion parameters to model\n# 0 : No\n# 1 : Yes\nset fmri(motionevs) 0\nset fmri(motionevsbeta) \"\"\nset fmri(scriptevsbeta) \"\"\n\n" +\
            "# Robust outlier detection in FLAME?\nset fmri(robust_yn) 0\n\n" +\
            "# Higher-level modelling\n# 3 : Fixed effects\n# 0 : Mixed Effects: Simple OLS\n# 2 : Mixed Effects: FLAME 1\n# 1 : Mixed Effects: FLAME 1+2\nset fmri(mixed_yn) 2\n\n" +\
            "# Number of EVs\nset fmri(evs_orig) "+str(num_of_EVs)+"\nset fmri(evs_real) "+str(num_of_EVs*2)+"\nset fmri(evs_vox) 0\n\n" +\
            "# Number of contrasts\nset fmri(ncon_orig) "+str(num_of_contrasts)+"\nset fmri(ncon_real) "+str(num_of_contrasts)+"\n\n" +\
            "# Number of F-tests\nset fmri(nftests_orig) 0\nset fmri(nftests_real) 0\n\n" +\
            "# Add constant column to design matrix? (obsolete)\nset fmri(constcol) 0\n\n" +\
            "# Carry out post-stats steps?\nset fmri(poststats_yn) 1\n\n" +\
            "# Pre-threshold masking?\nset fmri(threshmask) \"\"\n\n" +\
            "# Thresholding\n# 0 : None\n# 1 : Uncorrected\n# 2 : Voxel\n# 3 : Cluster\nset fmri(thresh) 3\n\n" +\
            "# P threshold\nset fmri(prob_thresh) 0.05\n\n" +\
            "# Z threshold\nset fmri(z_thresh) 2.3\n\n" +\
            "# Z min/max for colour rendering\n# 0 : Use actual Z min/max\n# 1 : Use preset Z min/max\nset fmri(zdisplay) 0\n\n" +\
            "# Z min in colour rendering\nset fmri(zmin) 2\n\n" +\
            "# Z max in colour rendering\nset fmri(zmax) 8\n\n" +\
            "# Colour rendering type\n# 0 : Solid blobs\n# 1 : Transparent blobs\nset fmri(rendertype) 1\n\n" +\
            "# Background image for higher-level stats overlays\n# 1 : Mean highres\n# 2 : First highres\n# 3 : Mean functional\n# 4 : First functional\n# 5 : Standard space template\nset fmri(bgimage) 1\n\n" +\
            "# Create time series plots\nset fmri(tsplot_yn) 1\n\n" +\
            "# Registration to initial structural\nset fmri(reginitial_highres_yn) 0\n\n" +\
            "# Search space for registration to initial structural\n# 0   : No search\n# 90  : Normal search\n# 180 : Full search\nset fmri(reginitial_highres_search) 90\n\n" +\
            "# Degrees of Freedom for registration to initial structural\nset fmri(reginitial_highres_dof) 3\n\n " +\
            "# Registration to main structural\nset fmri(reghighres_yn) 1\n\n" +\
            "# Search space for registration to main structural\n# 0   : No search\n# 90  : Normal search\n# 180 : Full search\nset fmri(reghighres_search) 180\n\n" +\
            "# Degrees of Freedom for registration to main structural\nset fmri(reghighres_dof) BBR\n\n" +\
            "# Registration to standard image?\nset fmri(regstandard_yn) 1\n\n" +\
            "# Use alternate reference images?\nset fmri(alternateReference_yn) 0\n\n" +\
            "# Standard image\nset fmri(regstandard) \"/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain\"\n\n" +\
            "# Search space for registration to standard space\n# 0   : No search\n# 90  : Normal search\n# 180 : Full search\nset fmri(regstandard_search) 180\n\n" +\
            "# Degrees of Freedom for registration to standard space\nset fmri(regstandard_dof) 12\n\n" +\
            "# Do nonlinear registration from structural to standard space?\nset fmri(regstandard_nonlinear_yn) 0\n\n" +\
            "# Control nonlinear warp field resolution\nset fmri(regstandard_nonlinear_warpres) 10\n\n" +\
            "# High pass filter cutoff\nset fmri(paradigm_hp) 100\n\n" +\
            "# Total voxels\nset fmri(totalVoxels) 36454400\n\n\n" +\
            "# Number of lower-level copes feeding into higher-level analysis\nset fmri(ncopeinputs) 0\n\n" +\
            "# 4D AVW data or FEAT directory (1)\nset feat_files(1) \""+file_path.split(".")[0]+"\"\n\n" +\
            "# Add confound EVs text file\nset fmri(confoundevs) 0\n\n" +\
            "# Subject's structural image for analysis 1\nset highres_files(1) \"/home/krutika/Data/ds001246-download/" + \
            subj+"/ses-anatomy/anat/Subject" + \
            subj.split("0")[-1]+"_T1w_brain\"\n\n"

    # call 1
    def EV_details(self, EV_num, EV_name, timing_file_path):
        ev_details = "# EV "+str(EV_num)+" title\nset fmri(evtitle"+str(EV_num)+") \"" + EV_name + "\"\n\n" \
            + "# Basic waveform shape (EV "+str(EV_num)+")\n" \
            + "# 0 : Square\n# 1 : Sinusoid\n# 2 : Custom (1 entry per volume)\n# 3 : Custom (3 column format)\n# 4 : Interaction\n# 10 : Empty (all zeros)\n" \
            + "set fmri(shape"+str(EV_num)+") 3\n\n" \
            + "# Convolution (EV "+str(EV_num) + ")\n# 0 : None\n# 1 : Gaussian\n# 2 : Gamma\n# 3 : Double-Gamma HRF\n# 4 : Gamma basis functions\n# 5 : Sine basis functions\n# 6 : FIR basis functions\n"\
            + "set fmri(convolve"+str(EV_num)+") 2\n\n"\
            + "# Convolve phase (EV "+str(EV_num)+")\nset fmri(convolve_phase"+str(EV_num)+") 0\n\n"\
            + "# Apply temporal filtering (EV "+str(EV_num)+")\nset fmri(tempfilt_yn"+str(EV_num)+") 1\n\n" \
            + "# Add temporal derivative (EV "+str(EV_num)+")\nset fmri(deriv_yn"+str(EV_num)+") 1\n\n"\
            + "# Custom EV file (EV "+str(EV_num)+")\nset fmri(custom"+str(EV_num)+") \""+timing_file_path+"\"\n\n" \
            + "# Gamma sigma (EV "+str(EV_num)+")\nset fmri(gammasigma"+str(EV_num)+") 3 \n\n" \
            + "# Gamma delay (EV "+str(EV_num) + \
            ")\nset fmri(gammadelay"+str(EV_num)+") 6 \n\n"

        for num in range(self.num_of_EVs+1):
            ev_details += "# Orthogonalise EV " + \
                str(EV_num)+" wrt EV "+str(num) + \
                "\nset fmri(ortho"+str(EV_num)+"."+str(num)+") 0\n\n"
        return ev_details

    def _contrast_ftest_details(self, contrast_name, contrast_num, tot_real_EVs):
        val = "# Display images for contrast_real "+str(contrast_num)+"\nset fmri(conpic_real."+str(contrast_num)+") 1\n\n" +\
            "# Title for contrast_real " + \
            str(contrast_num)+"\nset fmri(conname_real." + \
            str(contrast_num)+") \""+contrast_name+"\"\n\n"
        for i in range(1, tot_real_EVs+1):
            val += "# Real contrast_real vector " + \
                str(contrast_num)+" element "+str(i)+"\n"
            if i == contrast_num*2 - 1:
                val += "set fmri(con_real"+str(contrast_num) + \
                    "."+str(i)+") 1.0\n\n"
            elif i == tot_real_EVs-1:  # TODO
                val += "set fmri(con_real"+str(contrast_num) + \
                    "."+str(i)+") -1.0\n\n"
            else:
                val += "set fmri(con_real"+str(contrast_num) + \
                    "."+str(i)+") 0\n\n"
        return val

    # call2

    def contrast_ftest_details(self, contrast_names, tot_real_EVs):
        contrast_ftest = "# Contrast & F-tests mode\n# real : control real EVs\n# orig : control original EVs\nset fmri(con_mode_old) orig\nset fmri(con_mode) orig\n\n"
        for i, contrast_name in enumerate(contrast_names):
            contrast_ftest += self._contrast_ftest_details(
                contrast_name, i+1, tot_real_EVs)
        return contrast_ftest

    def _contrast_orig(self, contrast_name, contrast_num, total_real_EVs):
        cntrst_orig = "# Display images for contrast_orig " + \
            str(contrast_num)+"\nset fmri(conpic_orig."+str(contrast_num)+") 1\n\n " +\
            "# Title for contrast_orig " + \
            str(contrast_num)+"\nset fmri(conname_orig." + \
            str(contrast_num)+") \""+contrast_name+"\"\n\n"
        for i in range(1, total_real_EVs//2 + 1):
            cntrst_orig += "# Real contrast_orig vector " + \
                str(contrast_num)+" element "+str(i)+"\n"
            if i == contrast_num:
                cntrst_orig += "set fmri(con_orig" + \
                    str(contrast_num)+"."+str(i)+") 1.0\n\n"
            elif i == self.num_of_EVs:  # TODO
                cntrst_orig += "set fmri(con_orig"+str(contrast_num) + \
                    "."+str(i)+") -1.0\n\n"
            else:
                cntrst_orig += "set fmri(con_orig" + \
                    str(contrast_num)+"."+str(i)+") 0\n\n"
        return cntrst_orig

    # call 3

    def contrast_orig(self, contrast_names, tot_real_EVs):
        cntrst_orig = ""
        for i, contrast_name in enumerate(contrast_names):
            cntrst_orig += self._contrast_orig(
                contrast_name, i+1, tot_real_EVs)
        return cntrst_orig

    def _ftest(self, v1, num_of_contrasts):
        val = ""
        for i in range(1, num_of_contrasts+1):
            if i == v1:
                continue
            val += "# Mask real contrast/F-test "+str(v1)+" with real contrast/F-test " + \
                str(i)+"?\nset fmri(conmask"+str(v1)+"_"+str(i)+") 0\n\n"

        return val
    # call 4

    def ftest(self, num_of_contrasts):
        val = "# Contrast masking - use >0 instead of thresholding?\nset fmri(conmask_zerothresh_yn) 0\n\n"

        for i in range(1, num_of_contrasts+1):
            val += self._ftest(i, num_of_contrasts)
        val += "# Do contrast masking at all?\nset fmri(conmask1_1) 0\n\n"
        return val

    # call5

    def final(self):
        return"##########################################################\n# Now options that don't appear in the GUI\n\n# Alternative (to BETting) mask image\nset fmri(alternative_mask) \"\"\n\n" +\
            "# Initial structural space registration initialisation transform\nset fmri(init_initial_highres) \"\"\n\n" + \
            "# Structural space registration initialisation transform\nset fmri(init_highres) \"\"\n\n" +\
            "# Standard space registration initialisation transform\nset fmri(init_standard) \"\"\n\n" +\
            "# For full FEAT analysis: overwrite existing .feat output dir?\nset fmri(overwrite_yn) 0\n"
