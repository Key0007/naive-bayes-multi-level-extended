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
    lookup = pd.read_csv('/ifs/groups/rosenMRIGrp/kr3288/extended/new_extended_lineage.csv')
    lookup = lookup.fillna('')
    lookup = lookup.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    lookup = lookup[['Species_ID', taxa]]
    lookup = lookup.drop_duplicates() # !!!!!!!!! drop same species
    return lookup

def output_modifier(csv_file_path):

    taxa = csv_file_path.split('/')[-1].split("_")[2]
    TRIAL_MAP = create_trial_map(taxa.lower())
    lookup = create_lookup(taxa.lower())

    with open('/ifs/groups/rosenMRIGrp/kr3288/eeee.json', 'r') as j:
        dict_ = json.load(j)
    
    l = {value: key for key, values in dict_.items() for value in values}

    mod_path = f"/ifs/groups/rosenMRIGrp/kr3288/extended/{taxa}_modified"
    os.makedirs(mod_path, exist_ok=True) 

    df = pd.read_csv(csv_file_path, names=['NCBI RefSeq', 'Predicted Species_ID', 'Logarithmic probability'])
    mask = df['NCBI RefSeq'].apply(lambda x: not re.match(r'^\d+$', str(x)))
    df = df[mask]
    # convert to strings
    lookup['Species_ID'] = lookup['Species_ID'].astype(str)
    df['Predicted Species_ID'] = df['Predicted Species_ID'].astype(str)

    df = pd.merge(
        df,
        lookup[['Species_ID', taxa]],
        left_on='Predicted Species_ID',
        right_on='Species_ID',
        how='left'
    )

    df = df.rename(columns={taxa: f'Predicted {taxa}'})
    df = df.drop(columns='Species_ID')

    actual_species = [l.get(element, '') for element in df['NCBI RefSeq']]

    df["Actual Species"] = actual_species
    df["Actual Species"] = df["Actual Species"].str.strip()

    df = pd.merge(
        df,
        lookup[['Species_ID', taxa]],
        left_on='Actual Species',
        right_on='Species_ID',
        how='left'
    )

    df = df.rename(columns={taxa: f'Actual {taxa}'})
    df = df.drop(columns='Species_ID')

    df['NCBI RefSeq striped'] = df['NCBI RefSeq'].str.split('_').str[:2].str.join('_')

    trial_number = csv_file_path.split("/")[-1].split("_")[2]
    target_list = TRIAL_MAP.get(trial_number, '')

    df['Known/Unknown'] = df['NCBI RefSeq striped'].apply(lambda x: 'Known' if x in target_list else 'Unknown')
    
    df['Accurate Prediction'] = (df[f"Predicted {taxa}"] == df[f"Actual {taxa}"])

    df = df.drop(columns='NCBI RefSeq striped')

    output_filename = os.path.basename(csv_file_path)

    df.to_csv(f'{mod_path}/mod_{output_filename}', index=False)


if __name__ == "__main__":

    all_csv_paths = []

    for trial in ['trial_1', 'trial_2', 'trial_3', 'trial_4', 'trial_5']:
        for kmer in ['3', '6', '9', '12', '15']:
            for taxa in ['Phylum', 'Class', 'Order', 'Family']:
                path = os.path.join(f'/ifs/groups/rosenMRIGrp/kr3288/extended/{taxa}_testing/{kmer}-mers/classification_results', f'{trial}_{taxa}_{kmer}mers.csv')
                all_csv_paths.append(path)


    num_threads = int(os.environ.get('SLURM_NTASKS', 48))
    
    with Pool(processes=num_threads) as pool:
        pool.map(output_modifier, all_csv_paths)
