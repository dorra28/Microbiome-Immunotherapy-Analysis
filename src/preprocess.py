import argparse
import pandas as pd
from Bio import SeqIO  # For potential sequence handling, though not used here
import numpy as np

def preprocess_data(input_path, output_path):
    # Load data
    df = pd.read_csv(input_path, index_col=0)
    
    # Assume last column is 'Response'
    features = df.iloc[:, :-1]
    labels = df.iloc[:, -1]
    
    # Normalize to relative abundance
    features = features.div(features.sum(axis=1), axis=0)
    
    # Filter low-prevalence features (e.g., present in <10% samples)
    prevalence = (features > 0).sum(axis=0) / len(features)
    features = features.loc[:, prevalence > 0.1]
    
    # Handle missing values
    features = features.fillna(0)
    
    # Recombine with labels
    processed_df = pd.concat([features, labels], axis=1)
    
    # Save
    processed_df.to_csv(output_path)
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess microbiome data")
    parser.add_argument("--input", required=True, help="Input CSV path")
    parser.add_argument("--output", required=True, help="Output CSV path")
    args = parser.parse_args()
    preprocess_data(args.input, args.output)
