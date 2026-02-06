#!/bin/bash

# Exit immediately if a command fails
set -e

# Check if a dataset name argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <dataset-name>"
  exit 1
fi

DATASET_NAME=$1

# Get project root directory (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

########################################
# ACFG Disassembly
########################################

cd "$PROJECT_ROOT/IDA_scripts/IDA_acfg_disasm"
./run.sh "${DATASET_NAME}"

########################################
# ACFG Feature Extraction
########################################

cd "$PROJECT_ROOT/IDA_scripts/IDA_acfg_features"
./run.sh "${DATASET_NAME}"
