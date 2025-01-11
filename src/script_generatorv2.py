import sys
import os

def generate_script(script_name, command, target_path):
    # Create the content of the bash script
    script_content = f"""#!/bin/bash
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

{command}

end=`date +%s`
runtime=$((end-start))
echo "run time: $runtime"
"""

    # Write the content to a file
    with open(script_name, 'w') as script_file:
        script_file.write(script_content)

    # Make the script executable
    os.chmod(script_name, 0o755)

    # Move the script to the target path
    target_file = os.path.join(target_path, script_name)
    os.rename(script_name, target_file)

    print(f"Script '{script_name}' has been generated and moved to '{target_file}'")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 script_generator.py <script_name> <command> <target_path>")
        sys.exit(1)

    script_name = sys.argv[1]
    command = sys.argv[2]
    target_path = sys.argv[3]

    generate_script(script_name, command, target_path)