#!/bin/bash

set -e

# Check if a dataset name argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <dataset-name>"
  exit 1
fi

DATASET_NAME=$1

# Resolve paths relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # .../Models/Zeek
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"              # repo root

DBS_DIR="$PROJECT_ROOT/DBs"
PREPROCESS_DIR="$SCRIPT_DIR/Preprocessing"
ZEEK_INTERMEDIATE_DIR="$PREPROCESS_DIR/zeek_intermediate"
FEATURES_DIR="$DBS_DIR/${DATASET_NAME}/features"

# Optional: avoid root-owned outputs from docker
DOCKER_USER_ARGS=(-u "$(id -u):$(id -g)")

########################################
# Clean old outputs (no sudo)
########################################

find "$SCRIPT_DIR/NeuralNetwork" -type d -name "*${DATASET_NAME}*" -exec rm -rf {} +
find "$ZEEK_INTERMEDIATE_DIR" -type d -name "*${DATASET_NAME}*" -exec rm -rf {} +

########################################
# Helper to run one split
########################################

run_split () {
  local split="$1"   # training | validation | testing

  local in_dir="$FEATURES_DIR/${split}/acfg_disasm_${DATASET_NAME}_${split}"
  local out_dir="$ZEEK_INTERMEDIATE_DIR/${DATASET_NAME}_${split}"
  local out_json="$FEATURES_DIR/${split}/zeek_${DATASET_NAME}_${split}.json"

  mkdir -p "$out_dir"

  docker run --rm "${DOCKER_USER_ARGS[@]}" \
    -v "$in_dir:/input" \
    -v "$out_dir:/output" \
    -v "$PREPROCESS_DIR:/code" \
    zeek \
    /code/zeek.py process /input /output --workers-num 10

  # Copy zeek.json produced in intermediate folder into DBs/features/<split>/
  cp "$out_dir/zeek.json" "$out_json"
}

########################################
# TRAINING
########################################
start=$(date +%s)
run_split "training"
end=$(date +%s)
time1=$(( end - start ))

########################################
# VALIDATION
########################################
start=$(date +%s)
run_split "validation"
end=$(date +%s)
time2=$(( end - start ))

########################################
# TESTING
########################################
start=$(date +%s)
run_split "testing"
end=$(date +%s)
time3=$(( end - start ))

########################################
# Print timing
########################################
echo "Time for ${DATASET_NAME}_training: ${time1} seconds"
echo "Time for ${DATASET_NAME}_validation: ${time2} seconds"
echo "Time for ${DATASET_NAME}_testing: ${time3} seconds"
