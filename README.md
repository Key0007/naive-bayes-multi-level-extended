# Multi-Level Taxonomic Novelty Detection with Increased Genomic Depth
This project investigates the performance of a Naive Bayes Classifier (NBC) for taxonomic novelty detection using an expanded genomic database with increased species representation depth.

## Overview
Building upon our [previous work](https://github.com/key-r-code/naive-bayes-multi-level-basic) which analyzed NBC's novelty detection capabilities using k-mer counting on a single-genome-per-species database (4,634 species), this project significantly expands the scope by:

- Utilizing a comprehensive [database](./database/extended_lineage_with_distro.xls) of 58,979 unique species
- Including multiple genomes per taxonomic class (319,554 unique genomes in total)
- Analyzing how increased genomic depth affects classification performance
