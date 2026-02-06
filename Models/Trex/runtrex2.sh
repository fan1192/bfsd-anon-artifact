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

DBS_DIR="$PROJECT_ROOT/DBs"
PREPROCESS_DIR="$SCRIPT_DIR/Preprocessing"
NN_DIR="$SCRIPT_DIR/NeuralNetwork"

PAIRS_DIR="$DBS_DIR/${DATASET_NAME}/pairs/testing"
TRACES_DIR="$PREPROCESS_DIR/${DATASET_NAME}_testing-trex"

# Optional: avoid root-owned outputs
DOCKER_USER_ARGS=(-u "$(id -u):$(id -g)")

########################################
# Clean old outputs (no sudo)
########################################

find "$NN_DIR" -type d -name "*${DATASET_NAME}*" -exec rm -rf {} +

########################################
# TESTING inference
########################################

start=$(date +%s)

run_one () {
  local pairs_csv="$1"
  docker run --rm "${DOCKER_USER_ARGS[@]}" \
    -v "$PAIRS_DIR:/pairs" \
    -v "$TRACES_DIR:/traces" \
    -v "$NN_DIR:/output" \
    -v "$NN_DIR/trex_inference.py:/code/trex/trex_inference.py" \
    trex-inference \
    conda run --no-capture-output -n trex python3 /code/trex/trex_inference.py \
      --input-pairs "/pairs/${pairs_csv}" \
      --input-traces /traces/trex_traces.json \
      --model-checkpoint-dir checkpoints/similarity/ \
      --data-bin-dir data-bin-sim/similarity/ \
      --output-dir "/output/${DATASET_NAME}_testing-trex"
}

# 4 runs as in your original script
run_one "neg_rank_testing_${DATASET_NAME}.csv"
run_one "neg_testing_${DATASET_NAME}.csv"
run_one "pos_rank_testing_${DATASET_NAME}.csv"
run_one "pos_testing_${DATASET_NAME}.csv"

end=$(date +%s)
time3=$(( end - start ))

echo "Time for ${DATASET_NAME}_testing: ${time3} seconds"
