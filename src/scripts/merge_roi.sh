
cd ../../data/sourcedata

for id in `seq -w 1 5` ; do
    echo $PWD
    subj="sub-0$id"
    echo "===> Starting ROI merging for $subj"
    echo
    cd $subj/anat
        declare -a StringArray=("FFA" "hV4" "HVC" "LOC" "PPA" "V1d" "V1v" "V2d" "V2v" "V3d" "V3v")
        for val in ${StringArray[@]}; do
            fslmaths $subj"_mask_LH_"$val -add $subj"_mask_RH_"$val -bin $subj"_mask_"$val
        done
        declare -a StringArray=("V1" "V2" "V3")
        for val in ${StringArray[@]}; do
            fslmaths $subj"_mask_"$val"d" -add $subj"_mask_"$val"v" -bin $subj"_mask_"$val
        done
    cd ../..
done