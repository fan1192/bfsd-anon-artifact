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

PREPROCESS_DIR="$SCRIPT_DIR/Preprocessing"
BASE="$PROJECT_ROOT/DBs/${DATASET_NAME}/features"

########################################
# Clean old preprocessing outputs
########################################

find "$PREPROCESS_DIR" -type d -name "*${DATASET_NAME}*" -exec rm -rf {} +

########################################
# TRAINING
########################################

start=$(date +%s)

docker run --rm \
  -v "$BASE/training/acfg_features_${DATASET_NAME}_training:/input" \
  -v "$PREPROCESS_DIR:/output" \
  gnn-s2v-preprocessing \
  /output/digraph_numerical_features.py \
    -i /input \
    -o "/output/${DATASET_NAME}_training/"

end=$(date +%s)
time1=$(( end - start ))

########################################
# VALIDATION
########################################

start=$(date +%s)

docker run --rm \
  -v "$BASE/validation/acfg_features_${DATASET_NAME}_validation:/input" \
  -v "$PREPROCESS_DIR:/output" \
  gnn-s2v-preprocessing \
  /output/digraph_numerical_features.py \
    -i /input \
    -o "/output/${DATASET_NAME}_validation/"

end=$(date +%s)
time2=$(( end - start ))

########################################
# TESTING
########################################

start=$(date +%s)

docker run --rm \
  -v "$BASE/testing/acfg_features_${DATASET_NAME}_testing:/input" \
  -v "$PREPROCESS_DIR:/output" \
  gnn-s2v-preprocessing \
  /output/digraph_numerical_features.py \
    -i /input \
    -o "/output/${DATASET_NAME}_testing/"

end=$(date +%s)
time3=$(( end - start ))

########################################
# Print timing
########################################

echo "Time for ${DATASET_NAME}_training: ${time1} seconds"
echo "Time for ${DATASET_NAME}_validation: ${time2} seconds"
echo "Time for ${DATASET_NAME}_testing: ${time3} seconds"
