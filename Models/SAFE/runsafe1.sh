#!/bin/bash

set -e

# Check if a dataset name argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <dataset-name>"
  exit 1
fi

DATASET_NAME=$1

# Resolve paths relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"     # .../Models/SAFE
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"                # repo root

FEATURES_DIR="$PROJECT_ROOT/DBs/${DATASET_NAME}/features"
PRETRAIN_DIR="$SCRIPT_DIR/Pretraining"
PREPROCESS_DIR="$SCRIPT_DIR/Preprocessing"

# Optional: avoid root-owned files from docker outputs
DOCKER_USER_ARGS=(-u "$(id -u):$(id -g)")

########################################
# Clean old outputs (no sudo)
########################################

find "$PRETRAIN_DIR" -type d -name "*${DATASET_NAME}*" -exec rm -rf {} +
find "$PREPROCESS_DIR" -type d -name "*${DATASET_NAME}*" -exec rm -rf {} +

########################################
# TRAINING: SAFE pretraining + preprocessing
########################################

start=$(date +%s)

docker run --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$FEATURES_DIR/training/acfg_disasm_${DATASET_NAME}_training:/input" \
  -v "$PRETRAIN_DIR:/output" \
  safe-pretraining \
  /code/safe_pretraining.py \
    -i /input \
    -o "/output/${DATASET_NAME}_training"

docker run --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$FEATURES_DIR/training/acfg_disasm_${DATASET_NAME}_training:/input" \
  -v "$PRETRAIN_DIR/${DATASET_NAME}_training:/instruction_embeddings" \
  -v "$PREPROCESS_DIR:/code" \
  safe-preprocessing \
  /code/safe_preprocessing.py \
    -i /input \
    -o "/code/${DATASET_NAME}_training"

end=$(date +%s)
time1=$(( end - start ))

########################################
# VALIDATION: preprocessing (reuse training embeddings)
########################################

start=$(date +%s)

docker run --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$FEATURES_DIR/validation/acfg_disasm_${DATASET_NAME}_validation:/input" \
  -v "$PRETRAIN_DIR/${DATASET_NAME}_training:/instruction_embeddings" \
  -v "$PREPROCESS_DIR:/code" \
  safe-preprocessing \
  /code/safe_preprocessing.py \
    -i /input \
    -o "/code/${DATASET_NAME}_validation"

end=$(date +%s)
time2=$(( end - start ))

########################################
# TESTING: preprocessing (reuse training embeddings)
########################################

start=$(date +%s)

docker run --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$FEATURES_DIR/testing/acfg_disasm_${DATASET_NAME}_testing:/input" \
  -v "$PRETRAIN_DIR/${DATASET_NAME}_training:/instruction_embeddings" \
  -v "$PREPROCESS_DIR:/code" \
  safe-preprocessing \
  /code/safe_preprocessing.py \
    -i /input \
    -o "/code/${DATASET_NAME}_testing"

end=$(date +%s)
time3=$(( end - start ))

########################################
# Print timing
########################################

echo "Time for ${DATASET_NAME}_training: ${time1} seconds"
echo "Time for ${DATASET_NAME}_validation: ${time2} seconds"
echo "Time for ${DATASET_NAME}_testing: ${time3} seconds"
