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

BASE="$PROJECT_ROOT/DBs/${DATASET_NAME}/features"

########################################
# Clean old outputs
########################################

rm -f "$SCRIPT_DIR/"*"${DATASET_NAME}"*

########################################
# Run Catalog1 plugin
########################################

start=$(date +%s)

python3 "$SCRIPT_DIR/cli_catalog1.py" \
  -j "$BASE/testing/selected_testing_${DATASET_NAME}.json" \
  -o "$SCRIPT_DIR/${DATASET_NAME}_catalog1.csv"

end=$(date +%s)
time1=$(( end - start ))

echo "Time for testing_${DATASET_NAME}_catalog1.csv: $time1 seconds"
