import os
import subprocess
from multiprocessing import Pool

def copy_folder_batch(args):
    folder, source_dir, destination_path = args
    try:
        source_path = f"{source_dir}/{folder}"
        cmd = f"rsync -a {source_path} {destination_path}/"
        subprocess.run(cmd, shell=True, check=True)
        print(f"Copied: {folder}")
    except subprocess.CalledProcessError as e:
        print(f"Error copying {folder}: {str(e)}")

def parallel_copy(folder_list, source_dir, destination_path):  
    num_threads = int(os.environ.get('SLURM_NTASKS', 48))
    print(f"Using {num_threads} parallel processes")
    args_list = [(folder, source_dir, destination_path) for folder in folder_list]
    with Pool(processes=num_threads) as pool:
        pool.map(copy_folder_batch, args_list)

def main():

    source_dir = r'/ifs/groups/rosenMRIGrp/kr3288/extended/fna_grouped_by_species_tax' 
    
    destination_path = r'/ifs/groups/rosenMRIGrp/kr3288/extended/bench'
    
    folder_list = [f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))]
    
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
        
    print(f"Found {len(folder_list)} folders to copy")
    parallel_copy(folder_list, source_dir, destination_path)

if __name__ == "__main__":
    main()