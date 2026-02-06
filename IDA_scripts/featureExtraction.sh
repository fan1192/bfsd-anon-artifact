#!/bin/bash

set -e

# Check if the user provided an argument
if [ -z "$1" ]; then
    echo "Please provide a dataset name as an argument (e.g., Dataset-2, Dataset-4)."
    exit 1
fi

DATASET=$1

# Get directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

BASE="$PROJECT_ROOT/DBs/${DATASET}/features"

########################################
# ACFG Disassembly
########################################

python3 "$SCRIPT_DIR/IDA_acfg_disasm/cli_acfg_disasm.py" \
    -j "$BASE/testing/selected_testing_${DATASET}.json" \
    -o "$BASE/testing/acfg_disasm_${DATASET}_testing"

python3 "$SCRIPT_DIR/IDA_acfg_disasm/cli_acfg_disasm.py" \
    -j "$BASE/training/selected_training_${DATASET}.json" \
    -o "$BASE/training/acfg_disasm_${DATASET}_training"

python3 "$SCRIPT_DIR/IDA_acfg_disasm/cli_acfg_disasm.py" \
    -j "$BASE/validation/selected_validation_${DATASET}.json" \
    -o "$BASE/validation/acfg_disasm_${DATASET}_validation"

########################################
# ACFG Feature Extraction
########################################

python3 "$SCRIPT_DIR/IDA_acfg_features/cli_acfg_features.py" \
    -j "$BASE/testing/selected_testing_${DATASET}.json" \
    -o "$BASE/testing/acfg_features_${DATASET}_testing"

python3 "$SCRIPT_DIR/IDA_acfg_features/cli_acfg_features.py" \
    -j "$BASE/training/selected_training_${DATASET}.json" \
    -o "$BASE/training/acfg_features_${DATASET}_training"

python3 "$SCRIPT_DIR/IDA_acfg_features/cli_acfg_features.py" \
    -j "$BASE/validation/selected_validation_${DATASET}.json" \
    -o "$BASE/validation/acfg_features_${DATASET}_validation"
