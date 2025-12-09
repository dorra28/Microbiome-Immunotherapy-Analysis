#!/bin/bash

# Microbiome Immunotherapy Analysis Workflow

echo "Starting workflow..."

# Step 1: Preprocess data
python src/preprocess.py --input data/microbiome_data.csv --output data/processed_data.csv

# Step 2: Analyze and model
python src/analyze.py --input data/processed_data.csv --output results/model.pkl --report results/analysis_report.txt

# Step 3: Visualize
python src/visualize.py --input results/model.pkl --output results/plots/

echo "Workflow complete. Results in 'results/' directory."
