# Multi-Level Taxonomic Novelty Detection with Increased Genomic Depth
This project investigates the performance of a Naive Bayes Classifier (NBC) for taxonomic novelty detection using an expanded genomic database with increased species representation depth.

## Overview
Building upon our [previous work](https://github.com/key-r-code/naive-bayes-multi-level-basic) which analyzed NBC's novelty detection capabilities using k-mer counting on a single-genome-per-species database (4,634 species), this project significantly expands the scope by:

- Utilizing a comprehensive [database](./database/extended_lineage.csv) of 58,979 unique species
- Including multiple genomes per taxonomic class (319,554 unique genomes in total)
- Analyzing how increased genomic depth affects classification performance

## Methodology

### Dataset creation

To ensure statistical robustness and balanced representation, we implemented a two-stage filtering process:

1. Initial Filtering

    * Excluded species with fewer than 400 genome representatives
    * This threshold ensures sufficient data for meaningful model training

2. Random Sampling

    * Generated balanced training datasets through random sampling
    * Each trial maintained consistent genome counts across different species configurations
    * Number of species varied between trials due to natural variation in genome availability per species

### k-mer counting

Models are trained on k-mer frequencies. All k-mer count files were generated using Jellyfish. The k-mers used in this project were of length 3, 6, 9, 12 and 15. 

<!-- ### Testing data

[... WIP ...]

### Post-data analysis and ROC/AUC generation

[... WIP ...]

## Results

[.. WIP ...] -->