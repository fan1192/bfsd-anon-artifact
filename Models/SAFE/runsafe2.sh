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

DBS_DIR="$PROJECT_ROOT/DBs"
IDBS_DIR="$PROJECT_ROOT/IDBs"
NN_DIR="$SCRIPT_DIR/NeuralNetwork"
PREPROCESS_DIR="$SCRIPT_DIR/Preprocessing"
INSTR_EMB_DIR="$SCRIPT_DIR/Pretraining/${DATASET_NAME}_training"

# Optional: avoid root-owned outputs
DOCKER_USER_ARGS=(-u "$(id -u):$(id -g)")

########################################
# Clean old outputs (no sudo)
########################################

find "$NN_DIR" -type d -name "*${DATASET_NAME}*" -exec rm -rf {} +

########################################
# TRAIN
########################################

start=$(date +%s)

docker run --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/input" \
  -v "$INSTR_EMB_DIR:/instruction_embeddings" \
  -v "$PREPROCESS_DIR:/preprocessing" \
  -v "$NN_DIR:/output" \
  -v "$NN_DIR/safe_nn.py:/code/safe_nn.py" \
  -v "$NN_DIR/core:/code/core" \
  -v "$IDBS_DIR:/IDBs" \
  safe-neuralnetwork \
  /code/safe_nn.py \
    --train \
    --num_epochs 5 \
    --dataset "${DATASET_NAME}" \
    -c "/output/model_checkpoint_${DATASET_NAME}" \
    -o "/output/${DATASET_NAME}_training"

end=$(date +%s)
time1=$(( end - start ))

########################################
# VALIDATE
########################################

start=$(date +%s)

docker run --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/input" \
  -v "$INSTR_EMB_DIR:/instruction_embeddings" \
  -v "$PREPROCESS_DIR:/preprocessing" \
  -v "$NN_DIR:/output" \
  -v "$NN_DIR/safe_nn.py:/code/safe_nn.py" \
  -v "$NN_DIR/core:/code/core" \
  -v "$IDBS_DIR:/IDBs" \
  safe-neuralnetwork \
  /code/safe_nn.py \
    --validate \
    --dataset "${DATASET_NAME}" \
    -c "/output/model_checkpoint_${DATASET_NAME}" \
    -o "/output/${DATASET_NAME}_validation"

end=$(date +%s)
time2=$(( end - start ))

########################################
# TEST
########################################

start=$(date +%s)

docker run --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/input" \
  -v "$INSTR_EMB_DIR:/instruction_embeddings" \
  -v "$PREPROCESS_DIR:/preprocessing" \
  -v "$NN_DIR:/output" \
  -v "$NN_DIR/safe_nn.py:/code/safe_nn.py" \
  -v "$NN_DIR/core:/code/core" \
  -v "$IDBS_DIR:/IDBs" \
  safe-neuralnetwork \
  /code/safe_nn.py \
    --test \
    --dataset "${DATASET_NAME}" \
    -c "/output/model_checkpoint_${DATASET_NAME}" \
    -o "/output/${DATASET_NAME}_testing"

end=$(date +%s)
time3=$(( end - start ))

########################################
# Print timing
########################################

echo "Time for ${DATASET_NAME}_training: ${time1} seconds"
echo "Time for ${DATASET_NAME}_validation: ${time2} seconds"
echo "Time for ${DATASET_NAME}_testing: ${time3} seconds"
