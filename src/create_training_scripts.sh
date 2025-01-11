#!/bin/bash
main_dir="/ifs/groups/rosenMRIGrp/kr3288/extended"
taxa=("phylum" "class" "order" "family")
kmer_size=("3" "6" "9" "12" "15")
trials=("trial_1" "trial_2" "trial_3" "trial_4" "trial_5")
for taxa_ in "${taxa[@]}"; do
   for kmer in "${kmer_size[@]}"; do
	   for trial_ in "${trials[@]}"; do
			   python3 script_generatorv2.py train-${taxa_}-${trial_}.sh "singularity exec --bind /ifs/groups/rosenMRIGrp/kr3288:/mnt nbc_cross_validation_env_latest.sif NB.run train /mnt/extended/${taxa_}_testing/${kmer}-mers/training_data/${trial_} -s /mnt/extended/${taxa_}_testing/${kmer}-mers/training_models/${trial_} -k ${kmer} -m 180000 -t 48" /ifs/groups/rosenMRIGrp/kr3288/extended/${taxa_}_testing/${kmer}-mers/training_scripts
	done
   done
done