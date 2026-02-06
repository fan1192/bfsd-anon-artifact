#!/bin/bash

set -e

# Check if a dataset name argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <dataset-name>"
  exit 1
fi

DATASET_NAME=$1

# Resolve paths relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # .../Models/Trex
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"              # repo root

FEATURES_DIR="$PROJECT_ROOT/DBs/${DATASET_NAME}/features"
PREPROCESS_DIR="$SCRIPT_DIR/Preprocessing"

# Optional: avoid root-owned outputs
DOCKER_USER_ARGS=(-u "$(id -u):$(id -g)")

########################################
# Clean old preprocessing outputs
########################################

find "$PREPROCESS_DIR" -type d -name "*${DATASET_NAME}*" -exec rm -rf {} +

########################################
# TESTING (training/validation currently disabled)
########################################

start=$(date +%s)

docker run --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$FEATURES_DIR/testing/acfg_disasm_${DATASET_NAME}_testing:/input" \
  -v "$PREPROCESS_DIR:/output" \
  trex-preprocessing \
  /code/generate_function_traces.py \
    -i /input \
    -o "/output/${DATASET_NAME}_testing-trex"

end=$(date +%s)
time3=$(( end - start ))

########################################
# Print timing
########################################

echo "Time for ${DATASET_NAME}_testing: ${time3} seconds"
