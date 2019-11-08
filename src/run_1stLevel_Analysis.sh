#!/bin/bash

# Generate the subject list to make modifying this script
# to run just a subset of subjects easier.

for id in `seq -w 1 5` ; do
    subj="sub-0$id"
    echo "===> Starting processing of $subj"
    echo
    cd $subj/func
        #Check whether the file subjList.txt exists; if not, create it
        if [ ! -f designList.txt ]; then
                ls -d design_run?? > designList.txt
        fi

        #Loop over all subjects and format timing files into FSL format
        for designFile in `cat designList.txt` ; do
                echo "===> Starting feat for "+designFile
                feat designFile

    # Go back to the directory containing all of the subjects, and repeat the loop
    cd ../../
done

echo
