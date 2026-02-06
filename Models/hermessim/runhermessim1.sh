#!/bin/bash

set -e

# Check if a dataset name argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <dataset-name>"
  exit 1
fi

DATASET_NAME=$1

# Resolve paths relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"          # .../Models/hermessim
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"                     # repo root

DBS_DIR="$PROJECT_ROOT/DBs"
BIN_DIR="$PROJECT_ROOT/Binaries"

LIFTING_DIR="$SCRIPT_DIR/lifting"
PREPROCESS_DIR="$SCRIPT_DIR/Preprocessing"

# Host-side directories that we create/remove
CFG_SUMMARY_DIR="$DBS_DIR/${DATASET_NAME}/cfg_summary"
FEATURES_DIR="$DBS_DIR/${DATASET_NAME}/features"
PCODE_INPUTS_DIR="$PREPROCESS_DIR/inputs/${DATASET_NAME}_pcode"

# Optional: run docker as current user to avoid root-owned outputs
DOCKER_USER_ARGS=(-u "$(id -u):$(id -g)")

########################################
# TRAINING
########################################
start=$(date +%s)

rm -rf "$CFG_SUMMARY_DIR/training"
mkdir -p "$CFG_SUMMARY_DIR/training"

docker run --gpus all --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/dbs" \
  -v "$LIFTING_DIR:/lifting" \
  hermessim \
  python3 /lifting/dataset_summary.py \
    --cfg_summary "/dbs/${DATASET_NAME}/cfg_summary/training" \
    --dataset_info_csv "/dbs/${DATASET_NAME}/training_${DATASET_NAME}.csv" \
    --cfgs_folder "/dbs/${DATASET_NAME}/features/training/acfg_features_${DATASET_NAME}_training"

rm -rf "$FEATURES_DIR/training/pcode_raw_${DATASET_NAME}_training"
mkdir -p "$FEATURES_DIR/training/pcode_raw_${DATASET_NAME}_training"

docker run --gpus all --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/dbs" \
  -v "$LIFTING_DIR:/lifting" \
  -v "$BIN_DIR:/binaries" \
  hermessim \
  python3 /lifting/pcode_lifter.py \
    --cfg_summary "/dbs/${DATASET_NAME}/cfg_summary/training" \
    --output_dir "/dbs/${DATASET_NAME}/features/training/pcode_raw_${DATASET_NAME}_training" \
    --graph_type ALL \
    --verbose 1 \
    --nproc 32

rm -rf "$PCODE_INPUTS_DIR"
mkdir -p "$PCODE_INPUTS_DIR"

docker run --gpus all --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/dbs" \
  -v "$PREPROCESS_DIR:/preprocess" \
  -v "$BIN_DIR:/binaries" \
  hermessim \
  python3 /preprocess/preprocess/preprocessing_pcode.py \
    --training \
    --freq-mode -f both -s "${DATASET_NAME}_training" \
    -i "/dbs/${DATASET_NAME}/features/training/pcode_raw_${DATASET_NAME}_training" \
    -o "/preprocess/inputs/${DATASET_NAME}_pcode"

end=$(date +%s)
time1=$(( end - start ))

########################################
# VALIDATION
########################################
start=$(date +%s)

rm -rf "$CFG_SUMMARY_DIR/validation"
mkdir -p "$CFG_SUMMARY_DIR/validation"

docker run --gpus all --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/dbs" \
  -v "$LIFTING_DIR:/lifting" \
  hermessim \
  python3 /lifting/dataset_summary.py \
    --cfg_summary "/dbs/${DATASET_NAME}/cfg_summary/validation" \
    --dataset_info_csv "/dbs/${DATASET_NAME}/validation_${DATASET_NAME}.csv" \
    --cfgs_folder "/dbs/${DATASET_NAME}/features/validation/acfg_features_${DATASET_NAME}_validation"

rm -rf "$FEATURES_DIR/validation/pcode_raw_${DATASET_NAME}_validation"
mkdir -p "$FEATURES_DIR/validation/pcode_raw_${DATASET_NAME}_validation"

docker run --gpus all --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/dbs" \
  -v "$LIFTING_DIR:/lifting" \
  -v "$BIN_DIR:/binaries" \
  hermessim \
  python3 /lifting/pcode_lifter.py \
    --cfg_summary "/dbs/${DATASET_NAME}/cfg_summary/validation" \
    --output_dir "/dbs/${DATASET_NAME}/features/validation/pcode_raw_${DATASET_NAME}_validation" \
    --graph_type ALL \
    --verbose 1 \
    --nproc 32

docker run --gpus all --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/dbs" \
  -v "$PREPROCESS_DIR:/preprocess" \
  -v "$BIN_DIR:/binaries" \
  hermessim \
  python3 /preprocess/preprocess/preprocessing_pcode.py \
    --freq-mode -f both -s "${DATASET_NAME}_validation" \
    -i "/dbs/${DATASET_NAME}/features/validation/pcode_raw_${DATASET_NAME}_validation" \
    -o "/preprocess/inputs/${DATASET_NAME}_pcode"

docker run --gpus all --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/dbs" \
  -v "$PREPROCESS_DIR:/preprocess" \
  -v "$BIN_DIR:/binaries" \
  hermessim \
  python3 /preprocess/preprocess/generate_validation.py \
    --db_dir /dbs \
    --input "/dbs/${DATASET_NAME}/validation_${DATASET_NAME}.csv" \
    --output "/dbs/${DATASET_NAME}/pairs/validation/validation_functions.csv"

end=$(date +%s)
time2=$(( end - start ))

########################################
# TESTING
########################################
start=$(date +%s)

rm -rf "$CFG_SUMMARY_DIR/testing"
mkdir -p "$CFG_SUMMARY_DIR/testing"

docker run --gpus all --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/dbs" \
  -v "$LIFTING_DIR:/lifting" \
  hermessim \
  python3 /lifting/dataset_summary.py \
    --cfg_summary "/dbs/${DATASET_NAME}/cfg_summary/testing" \
    --dataset_info_csv "/dbs/${DATASET_NAME}/testing_${DATASET_NAME}.csv" \
    --cfgs_folder "/dbs/${DATASET_NAME}/features/testing/acfg_features_${DATASET_NAME}_testing"

rm -rf "$FEATURES_DIR/testing/pcode_raw_${DATASET_NAME}_testing"
mkdir -p "$FEATURES_DIR/testing/pcode_raw_${DATASET_NAME}_testing"

docker run --gpus all --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/dbs" \
  -v "$LIFTING_DIR:/lifting" \
  -v "$BIN_DIR:/binaries" \
  hermessim \
  python3 /lifting/pcode_lifter.py \
    --cfg_summary "/dbs/${DATASET_NAME}/cfg_summary/testing" \
    --output_dir "/dbs/${DATASET_NAME}/features/testing/pcode_raw_${DATASET_NAME}_testing" \
    --graph_type ALL \
    --verbose 1 \
    --nproc 32

docker run --gpus all --rm "${DOCKER_USER_ARGS[@]}" \
  -v "$DBS_DIR:/dbs" \
  -v "$PREPROCESS_DIR:/preprocess" \
  -v "$BIN_DIR:/binaries" \
  hermessim \
  python3 /preprocess/preprocess/preprocessing_pcode.py \
    --freq-mode -f both -s "${DATASET_NAME}_testing" \
    -i "/dbs/${DATASET_NAME}/features/testing/pcode_raw_${DATASET_NAME}_testing" \
    -o "/preprocess/inputs/${DATASET_NAME}_pcode"

end=$(date +%s)
time3=$(( end - start ))

########################################
# Print timing
########################################
echo "Time for ${DATASET_NAME}_training: ${time1} seconds"
echo "Time for ${DATASET_NAME}_validation: ${time2} seconds"
echo "Time for ${DATASET_NAME}_testing: ${time3} seconds"
