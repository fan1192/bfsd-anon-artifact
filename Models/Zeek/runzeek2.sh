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
NN_DIR="$SCRIPT_DIR/NeuralNetwork"

# Optional: avoid root-owned outputs from docker
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
  -v "$NN_DIR:/code" \
  zeekneuralnetwork \
  /code/zeek_nn.py \
    --train \
    --num_epochs 10 \
    -c "/code/model_checkpoint_${DATASET_NAME}" \
    --dataset "${DATASET_NAME}" \
    -o "/code/${DATASET_NAME}_training"

end=$(date +%s)
time1=$(( end - start ))

########################################
# TEST
########################################

start=$(date +%s)

docker run --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/input" \
  -v "$NN_DIR:/code" \
  zeekneuralnetwork \
  /code/zeek_nn.py \
    --test \
    --dataset "${DATASET_NAME}" \
    -c "/code/model_checkpoint_${DATASET_NAME}" \
    -o "/code/${DATASET_NAME}_testing"

end=$(date +%s)
time3=$(( end - start ))

########################################
# Print timing
########################################

echo "Time for ${DATASET_NAME}_training: ${time1} seconds"
echo "Time for ${DATASET_NAME}_testing: ${time3} seconds"
