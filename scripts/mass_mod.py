import os
import re
import json
import pandas as pd
from multiprocessing import Pool

def get_training_list(taxa, trial):

    file_path = f'/ifs/groups/rosenMRIGrp/kr3288/extended/training_lists/{taxa}_{trial}.txt'
    with open(file_path, 'r') as t:
        lines = t.readlines()
        return [line.strip('\n')[1:] for line in lines]
    
def create_trial_map(taxa):

    TRIAL_MAP = {
        '1': [],
        '2': [], 
        '3': [],
        '4': [],
        '5': []
    }

    for trial in ['trial_1', 'trial_2', 'trial_3', 'trial_4', 'trial_5']:
        TRIAL_MAP[trial[-1:]] = get_training_list(taxa, trial)

    return TRIAL_MAP


def create_lookup(taxa):
    return (
        pl.read_csv('/Users/key/extended/new_extended_lineage.csv')
        .fill_null('')
        .with_columns(
            pl.col(pl.Utf8).str.strip_chars()
        )
        .select(['Species_ID', taxa])
        .unique()
    )

def output_modifier(csv_file_path):

def output_modifier(csv_file_path):
    # Extract taxa and set up paths/mappings
    taxa = csv_file_path.split('/')[-1].split("_")[2]
    TRIAL_MAP = create_trial_map(taxa)
    lookup = create_lookup(taxa.capitalize())
    
    # Load JSON dictionary
    with open('/ifs/groups/rosenMRIGrp/kr3288/eeee.json', 'r') as j:
        dict_ = json.load(j)
    
    l = {value: key for key, values in dict_.items() for value in values}
    
    # Create directory
    mod_path = f"/ifs/groups/rosenMRIGrp/kr3288/extended/{taxa}_modified"
    os.makedirs(mod_path, exist_ok=True)

    # Read and process CSV
    df = (
        pl.read_csv(
            csv_file_path,
            has_header=False,
            new_columns=['NCBI RefSeq', 'Predicted Species_ID', 'Logarithmic probability']
        )
        .filter(~pl.col('NCBI RefSeq').cast(str).str.contains(r'^\d+$'))
        .with_columns([
            pl.col('Predicted Species_ID').cast(str)
        ])
    )

    # First merge operation
    df = (
        df.join(
            lookup.select(['Species_ID', pl.col(taxa.capitalize())]),
            left_on='Predicted Species_ID',
            right_on='Species_ID',
            how='left'
        )
        .drop('Species_ID')
        .rename({taxa.capitalize(): f'Predicted {taxa.capitalize()}'})
    )

    # Add actual species
    df = (
        df.with_columns([
            pl.col('NCBI RefSeq').map_dict(l, default='').alias('Actual Species'),
        ])
        .with_columns([
            pl.col('Actual Species').str.strip_chars()
        ])
    )

    # Second merge operation
    df = (
        df.join(
            lookup.select(['Species_ID', pl.col(taxa.capitalize())]),
            left_on='Actual Species',
            right_on='Species_ID',
            how='left'
        )
        .drop('Species_ID')
        .rename({taxa.capitalize(): f'Actual {taxa.capitalize()}'})
    )

    # Process NCBI RefSeq and add Known/Unknown
    df = (
        df.with_columns([
            pl.col('NCBI RefSeq')
                .str.split('_')
                .list.slice(0, 2)
                .list.join('_')
                .alias('NCBI RefSeq striped')
        ])
        .with_columns([
            pl.col('NCBI RefSeq striped')
                .map_dict({k: 'Known' for k in TRIAL_MAP.get(trial_number, '')}, default='Unknown')
                .alias('Known/Unknown')
        ])
    )

    # Add accuracy column and final processing
    df = (
        df.with_columns([
            (pl.col(f"Predicted {taxa}") == pl.col(f"Actual {taxa}"))
                .alias('Accurate Prediction')
        ])
        .drop('NCBI RefSeq striped')
    )

    # Save output
    output_filename = os.path.basename(csv_file_path)
    df.write_csv(f'{mod_path}/mod_{output_filename}')


if __name__ == "__main__":

    all_csv_paths = []

    for trial in ['trial_1', 'trial_2', 'trial_3', 'trial_4', 'trial_5']:
        for kmer in ['3', '6', '9', '12', '15']:
            for taxa in ['phylum', 'class', 'order', 'family']:
                path = os.path.join(f'/ifs/groups/rosenMRIGrp/kr3288/extended/{taxa}_testing/{kmer}-mers/classification_results', f'{trial}_{taxa}_{kmer}mers.csv')
                all_csv_paths.append(path)


    num_threads = int(os.environ.get('SLURM_NTASKS', 48))
    
    with Pool(processes=num_threads) as pool:
        pool.map(output_modifier, all_csv_paths)
