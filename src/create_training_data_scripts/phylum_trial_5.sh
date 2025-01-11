#!/bin/bash
### select the partition "def"
#SBATCH --partition=def
### set email address for sending job status
#SBATCH --mail-user=kr3288@drexel.edu
### account - essentially your research group
#SBATCH --account=rosenMRIPrj
### select number of nodes
#SBATCH --nodes=1
### select number of tasks per node (threads)
#SBATCH --ntasks-per-node=48
### request 2 hours of wall clock time
#SBATCH --time=12:00:00
### memory size required per node (memory)
#SBATCH --mem=185GB
#SBATCH --cpus-per-task=1

. ~/.bashrc
start=`date +%s`

conda run -n myenv python3 everything_extended1.py phylum trial_5

end=`date +%s`
runtime=$((end-start))
echo "run time: $runtime"
