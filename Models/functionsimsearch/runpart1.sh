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
FSS_DIR="$SCRIPT_DIR/IDA_fss"
BASE="$PROJECT_ROOT/DBs/${DATASET_NAME}/features"

########################################
# Clean previous outputs (no sudo)
########################################

find "$FSS_DIR" -type d -name "*${DATASET_NAME}*" -exec rm -rf {} +

########################################
# Run FSS (testing)
########################################

start=$(date +%s)
python3 "$FSS_DIR/cli_fss.py" \
  -j "$BASE/testing/selected_testing_${DATASET_NAME}.json" \
  -o "fss_${DATASET_NAME}_testing" \
  -c
end=$(date +%s)
time1=$(( end - start ))

########################################
# Run FSS (training)
########################################

start=$(date +%s)
python3 "$FSS_DIR/cli_fss.py" \
  -j "$BASE/training/selected_training_${DATASET_NAME}.json" \
  -o "fss_${DATASET_NAME}_training" \
  -c
end=$(date +%s)
time2=$(( end - start ))

########################################
# Run FSS (validation)
########################################

start=$(date +%s)
python3 "$FSS_DIR/cli_fss.py" \
  -j "$BASE/validation/selected_validation_${DATASET_NAME}.json" \
  -o "fss_${DATASET_NAME}_validation" \
  -c
end=$(date +%s)
time3=$(( end - start ))

########################################
# Print timing
########################################

echo "Time for fss_${DATASET_NAME}_testing: ${time1} seconds"
echo "Time for fss_${DATASET_NAME}_training: ${time2} seconds"
echo "Time for fss_${DATASET_NAME}_validation: ${time3} seconds"
