import pandas as pd
from os.path import join
import argparse

# Set up command-line arguments
parser = argparse.ArgumentParser(description="Process a validation dataset and assign group IDs.")
parser.add_argument('--db_dir', type=str, required=True, help="Directory containing the database files.")
parser.add_argument('--input', type=str, required=True, help="Path to the input CSV file.")
parser.add_argument('--output', type=str, required=True, help="Path to save the output CSV file.")

args = parser.parse_args()

# Use command-line arguments
DB_DIR = args.db_dir
INPUT = args.input
OUTPUT = args.output

# Process the dataset
df = pd.read_csv(INPUT, index_col=0)

name2groupdid = {}
counter = 0
groups = []

for idx, r in df.iterrows():
    fname = r["func_name"]
    if not fname in name2groupdid:
        name2groupdid[fname] = counter
        counter += 1
    groups.append(name2groupdid[fname])

df = df[["idb_path", "fva"]]
df.insert(2, "group", groups)

df.to_csv(OUTPUT)
