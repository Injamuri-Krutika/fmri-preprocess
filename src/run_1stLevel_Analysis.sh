#!/bin/bash

# Generate the subject list to make modifying this script
# to run just a subset of subjects easier.

for id in `seq -w 1 5` ; do
        subj="sub-0$id"
        echo "===> Starting processing of $subj"
        cd ../data/$subj
        if [ ! -f sessions.txt ]; then
                ls -d ses-perceptionTraining?? > sessions.txt
        fi
        for session_dir in `cat sessions.txt`; do
                cd ./$session_dir/func
                #Check whether the file subjList.txt exists; if not, create it
                if [ ! -f designList.txt ]; then
                        ls -f *.fsf > designList.txt
                fi
                for designFile in `cat designList.txt` ; do
                        echo "===> Starting feat for $designFile"
                        feat $designFile
                done
                cd ../../
        done
        # Go back to the directory containing all of the subjects, and repeat the loop
        cd ../
done