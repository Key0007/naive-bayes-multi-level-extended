#!/bin/bash
mkdir /ifs/groups/rosenMRIGrp/kr3288/extended_create_training_data
main_dir="/ifs/groups/rosenMRIGrp/kr3288/extended"
taxa=("phylum" "class" "order" "family")
trials=("trial_1" "trial_2" "trial_3" "trial_4" "trial_5")
for taxa_ in "${taxa[@]}"; do
   for trial_num in "${trials[@]}"; do
       python3 script_generatorv2.py ${taxa_}_$trial_num.sh "conda run -n myenv python3 everything_extended1.py $taxa_ $trial_num" /ifs/groups/rosenMRIGrp/kr3288/extended_create_training_data
   done
done