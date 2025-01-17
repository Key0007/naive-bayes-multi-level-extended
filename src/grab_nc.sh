#!/bin/bash
taxa=("phylum" "class" "order" "family")
trials=("trial_1" "trial_2" "trial_3" "trial_4" "trial_5")

for taxa_ in "${taxa[@]}"; do
	   for trial_ in "${trials[@]}"; do
		   cd /ifs/groups/rosenMRIGrp/kr3288/extended/${taxa_}_testing/15-mers/training_data/${trial_}/
           find . -type f -name "*.fna" | while read file; do
                grep '>N' $file >> /ifs/groups/rosenMRIGrp/kr3288/extended/training_lists/${taxa_}_${trial_}.txt
            done
	done
done


