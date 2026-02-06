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

DBS_DIR="$PROJECT_ROOT/DBs"
NN_DIR="$SCRIPT_DIR/NeuralNetwork"
PREPROCESS_DIR="$SCRIPT_DIR/Preprocessing"
INSTR_EMB_DIR="$SCRIPT_DIR/Pretraining/${DATASET_NAME}_training"

########################################
# Clean old outputs (no sudo)
########################################

find "$NN_DIR" -type d -name "*${DATASET_NAME}*" -exec rm -rf {} +

########################################
# TRAIN
########################################

start=$(date +%s)

docker run --rm \
  -v "$DBS_DIR:/input" \
  -v "$INSTR_EMB_DIR:/instruction_embeddings" \
  -v "$PREPROCESS_DIR:/preprocessing" \
  -v "$NN_DIR:/output" \
  -v "$NN_DIR/s2v.py:/code/s2v.py" \
  -v "$NN_DIR/core:/code/core" \
  gnn-s2v-neuralnetwork \
  /code/s2v.py \
    --train \
    --network_type rnn \
    --features_type asm --max_instructions 200 \
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

docker run --rm \
  -v "$DBS_DIR:/input" \
  -v "$INSTR_EMB_DIR:/instruction_embeddings" \
  -v "$PREPROCESS_DIR:/preprocessing" \
  -v "$NN_DIR:/output" \
  -v "$NN_DIR/s2v.py:/code/s2v.py" \
  -v "$NN_DIR/core:/code/core" \
  gnn-s2v-neuralnetwork \
  /code/s2v.py \
    --validate \
    --network_type rnn \
    --features_type asm --max_instructions 200 \
    --dataset "${DATASET_NAME}" \
    -c "/output/model_checkpoint_${DATASET_NAME}" \
    -o "/output/${DATASET_NAME}_validation"

end=$(date +%s)
time2=$(( end - start ))

########################################
# TEST
########################################

start=$(date +%s)

docker run --rm \
  -v "$DBS_DIR:/input" \
  -v "$INSTR_EMB_DIR:/instruction_embeddings" \
  -v "$PREPROCESS_DIR:/preprocessing" \
  -v "$NN_DIR:/output" \
  -v "$NN_DIR/s2v.py:/code/s2v.py" \
  -v "$NN_DIR/core:/code/core" \
  gnn-s2v-neuralnetwork \
  /code/s2v.py \
    --test \
    --network_type rnn \
    --features_type asm --max_instructions 200 \
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
