#!/bin/bash

set -e

# Check if a dataset name argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <dataset-name>"
  exit 1
fi

DATASET_NAME=$1

# Resolve paths relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

RESULTS_DIR="$PROJECT_ROOT/Results/data/raw_results/FunctionSimSearch"
FSS_INPUT_DIR="$SCRIPT_DIR/IDA_fss/fss_${DATASET_NAME}_testing"
OUT_DIR="$RESULTS_DIR/${DATASET_NAME}"

########################################
# Clean previous outputs (no sudo)
########################################

mkdir -p "$RESULTS_DIR"
find "$RESULTS_DIR" -type d -name "*${DATASET_NAME}*" -exec rm -rf {} +

mkdir -p "$OUT_DIR"

########################################
# Run Docker simhasher
########################################

start=$(date +%s)

docker run --rm \
  -v "$FSS_INPUT_DIR:/input" \
  -v "$OUT_DIR:/output" \
  fss /fss_simhasher.py

end=$(date +%s)
time1=$(( end - start ))

echo "Time for fss_${DATASET_NAME}_testing: ${time1} seconds"
