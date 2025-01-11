#!/bin/bash
main_dir="/ifs/groups/rosenMRIGrp/kr3288/extended"
taxa=("phylum" "class" "order" "family")
kmer_size=("3" "6" "9" "12" "15")
trials=("trial_1" "trial_2" "trial_3" "trial_4" "trial_5")
for taxa_ in "${taxa[@]}"; do
   for kmer in "${kmer_size[@]}"; do
	   for trial_ in "${trials[@]}"; do
		   python3 script_generatorv2.py jelly_${taxa_}_${kmer}-mers_${trial_}.sh "/ifs/groups/rosenMRIGrp/kr3288/jellyfish_gen_new_UPDATED.bash /ifs/groups/rosenMRIGrp/kr3288/extended/${taxa_}_testing/${kmer}-mers/training_data/${trial_} ${kmer} false" /ifs/groups/rosenMRIGrp/kr3288/extended_jelly_all
	done
   done
done