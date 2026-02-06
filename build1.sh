#!/bin/bash

# Check if a dataset name argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <dataset-name>"
  exit 1
fi

DATASET_NAME=$1
DATASET_NUMBER="${DATASET_NAME##*-}"

# Get project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

########################################
# IDBs directory
########################################

TARGET_DIR="$PROJECT_ROOT/IDBs/${DATASET_NAME}"

if [ -d "$TARGET_DIR" ]; then
  sudo rm -rf "$TARGET_DIR"/*
else
  sudo mkdir -p "$TARGET_DIR"
fi

########################################
# Generate IDBs
########################################

cd "$PROJECT_ROOT/IDA_scripts"
python3 generate_idbs.py --db${DATASET_NUMBER}

########################################
# Generate flowcharts
########################################

cd "$PROJECT_ROOT/IDA_scripts/IDA_flowchart"
sudo find . -type f -name "*${DATASET_NAME}*" -exec rm -rf {} +
python3 cli_flowchart.py \
    -i "$PROJECT_ROOT/IDBs/${DATASET_NAME}" \
    -o "flowchart_${DATASET_NAME}.csv"

########################################
# DBs directory
########################################

TARGET_DIR="$PROJECT_ROOT/DBs/${DATASET_NAME}"

if [ -d "$TARGET_DIR" ]; then
  sudo rm -rf "$TARGET_DIR"/*
else
  sudo mkdir -p "$TARGET_DIR"
fi

sudo cp \
  "$PROJECT_ROOT/IDA_scripts/notebooks/${DATASET_NAME}_creation.ipynb" \
  "$PROJECT_ROOT/DBs/${DATASET_NAME}/"
