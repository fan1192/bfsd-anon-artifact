#!/bin/bash

set -e

# Check if a dataset name argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <dataset-name>"
  exit 1
fi

DATASET_NAME=$1

# Resolve paths relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"      # .../Models/hermessim
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"                 # repo root

DBS_DIR="$PROJECT_ROOT/DBs"
LIFTING_DIR="$SCRIPT_DIR/lifting"
OUT_DIR="$SCRIPT_DIR/outputs"
NN_DIR="$SCRIPT_DIR/NeuralNetwork"
PREPROCESS_DIR="$SCRIPT_DIR/Preprocessing"

mkdir -p "$OUT_DIR"

start=$(date +%s)

docker run --rm --gpus all \
  -u "$(id -u):$(id -g)" \
  -v "$DBS_DIR:/dbs" \
  -v "$LIFTING_DIR:/lifting" \
  -v "$OUT_DIR:/outputs" \
  -v "$NN_DIR:/neuralnetwork" \
  -v "$PREPROCESS_DIR:/preprocessing" \
  hermessim \
  python3 /neuralnetwork/model/main.py \
    --inputdir /dbs \
    --config "/neuralnetwork/model/configures/e00_major_${DATASET_NAME}.json" \
    --dataset "${DATASET_NAME}" \
    --outputdir /outputs

end=$(date +%s)
time1=$(( end - start ))

echo "Time for ${DATASET_NAME}_training and testing: ${time1} seconds"
