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

# Project root is two levels up
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

BASE="$PROJECT_ROOT/DBs/${DATASET}/features"

# Paths to clear
OUT_TESTING="${BASE}/testing/acfg_disasm_${DATASET}_testing"
OUT_TRAINING="${BASE}/training/acfg_disasm_${DATASET}_training"
OUT_VALIDATION="${BASE}/validation/acfg_disasm_${DATASET}_validation"

echo "Clearing old output directories..."

for DIR in "$OUT_TESTING" "$OUT_TRAINING" "$OUT_VALIDATION"; do
    if [ -d "$DIR" ]; then
        echo "Removing existing directory: $DIR"
        rm -rf "$DIR"
    fi
    echo "Recreating: $DIR"
    mkdir -p "$DIR"
done

echo "Output directories ready."

########################################
# Run ACFG disassembly
########################################

python3 "$SCRIPT_DIR/cli_acfg_disasm.py" \
    -j "${BASE}/testing/selected_testing_${DATASET}.json" \
    -o "$OUT_TESTING"

python3 "$SCRIPT_DIR/cli_acfg_disasm.py" \
    -j "${BASE}/training/selected_training_${DATASET}.json" \
    -o "$OUT_TRAINING"

python3 "$SCRIPT_DIR/cli_acfg_disasm.py" \
    -j "${BASE}/validation/selected_validation_${DATASET}.json" \
    -o "$OUT_VALIDATION"
