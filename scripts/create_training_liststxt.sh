#!/bin/bash
taxa=("phylum" "class" "order" "family")
trials=("trial_1" "trial_2" "trial_3" "trial_4" "trial_5")
for taxa_ in "${taxa[@]}"; do
   for trial_num in "${trials[@]}"; do
       find /ifs/groups/rosenMRIGrp/kr3288/extended/${taxa_}_testing/15-mers/training_data/${trial_num} -name "*.fna" -printf "%f\n" >> /ifs/groups/rosenMRIGrp/kr3288/extended/training_lists/${taxa_}_${trial_num}.txt
   done
done