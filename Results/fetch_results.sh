#!/bin/bash
set -e

# Check if a dataset name argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <dataset-name>"
  exit 1
fi

DATASET_NAME=$1

# Resolve paths relative to this script (Results/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

DBS_DIR="$PROJECT_ROOT/DBs"
MODELS_DIR="$PROJECT_ROOT/Models"
RESULTS_DIR="$PROJECT_ROOT/Results"

DATA_DIR="$RESULTS_DIR/data/${DATASET_NAME}"

# Utility: ensure directory exists, and optionally clean csv files
ensure_dir_clean_csv () {
  local dir="$1"
  mkdir -p "$dir"
  rm -f "$dir"/*.csv 2>/dev/null || true
}

# Utility: copy 4 csv files from src dir to dst dir, optionally rename *_sim.csv -> *_<TAG>.csv
copy_4_csvs_with_tag () {
  local src_dir="$1"
  local dst_dir="$2"
  local tag="$3"   # e.g., Massarelli / Gemini / SAFE / Zeek ; empty means no rename
  if [ ! -d "$src_dir" ]; then
    echo "❌ Source directory does not exist: $src_dir"
    return 0
  fi

  local csv_count
  csv_count=$(find "$src_dir" -maxdepth 1 -type f -name "*.csv" | wc -l | tr -d ' ')
  if [ "$csv_count" -ne 4 ]; then
    echo "⚠️ Expected 4 CSV files in $src_dir, but found $csv_count. Skipping copy."
    return 0
  fi

  mkdir -p "$dst_dir"

  for file in "$src_dir"/*.csv; do
    local filename newname
    filename=$(basename "$file")
    newname="$filename"

    if [[ -n "$tag" && "$filename" == *_sim.csv ]]; then
      newname="${filename/_sim.csv/_${tag}.csv}"
    fi

    cp "$file" "$dst_dir/$newname"
    echo "✅ Copied $filename → $newname"
  done
}

# Utility: clean a directory (no sudo)
clean_dir () {
  local dir="$1"
  if [ -d "$dir" ]; then
    rm -rf "$dir"
  fi
  mkdir -p "$dir"
}

########################################
# Prepare destination folders
########################################

ensure_dir_clean_csv "$DATA_DIR"

########################################
# Asm2Vec embeddings.csv
########################################

ASM2VEC_SRC="$MODELS_DIR/Asm2vec/asm2vec_inference_${DATASET_NAME}-testing/embeddings.csv"
ASM2VEC_DST="$RESULTS_DIR/data/raw_results/Asm2vec/${DATASET_NAME}_asm2vec"
mkdir -p "$ASM2VEC_DST"
rm -f "$ASM2VEC_DST"/*.csv 2>/dev/null || true

if [ -f "$ASM2VEC_SRC" ]; then
  cp "$ASM2VEC_SRC" "$ASM2VEC_DST/"
  echo "Asm2Vec ✅ embeddings.csv copied to $ASM2VEC_DST"
else
  echo "Asm2Vec ❌ File not found: $ASM2VEC_SRC"
fi

########################################
# Catalog1: copy ${DATASET_NAME}*.csv
########################################

CATALOG1_SRC="$MODELS_DIR/Catalog1"
CATALOG1_DST="$RESULTS_DIR/data/raw_results/Catalog1/${DATASET_NAME}"

shopt -s nullglob
catalog_files=("$CATALOG1_SRC"/${DATASET_NAME}*.csv)
shopt -u nullglob

if [ ${#catalog_files[@]} -eq 0 ]; then
  echo "Catalog1: No '${DATASET_NAME}*.csv' files found in $CATALOG1_SRC. Skipping copy."
else
  ensure_dir_clean_csv "$CATALOG1_DST"
  cp "${catalog_files[@]}" "$CATALOG1_DST/"
  echo "Catalog1 ✅ Copy completed."
fi

########################################
# Model outputs copied into Results/data/${DATASET_NAME}
########################################

# Massarelli
copy_4_csvs_with_tag \
  "$MODELS_DIR/GNN-s2v-Massarelli/NeuralNetwork/${DATASET_NAME}_testing" \
  "$DATA_DIR" \
  "Massarelli"

# Gemini
copy_4_csvs_with_tag \
  "$MODELS_DIR/GNN-s2v-Gemini/NeuralNetwork/${DATASET_NAME}_testing" \
  "$DATA_DIR" \
  "Gemini"

# SAFE
copy_4_csvs_with_tag \
  "$MODELS_DIR/SAFE/NeuralNetwork/${DATASET_NAME}_testing" \
  "$DATA_DIR" \
  "SAFE"

# Trex (no renaming in your original script)
TREX_SRC="$MODELS_DIR/Trex/NeuralNetwork/${DATASET_NAME}_testing-trex"
if [ -d "$TREX_SRC" ]; then
  trex_csv_count=$(find "$TREX_SRC" -maxdepth 1 -type f -name "*.csv" | wc -l | tr -d ' ')
  if [ "$trex_csv_count" -ne 4 ]; then
    echo "Trex ⚠️ Expected 4 CSV files in $TREX_SRC, but found $trex_csv_count. Skipping copy."
  else
    cp "$TREX_SRC"/*.csv "$DATA_DIR/"
    echo "Trex ✅ Copy complete."
  fi
else
  echo "❌ Source directory does not exist: $TREX_SRC"
fi

# Zeek
copy_4_csvs_with_tag \
  "$MODELS_DIR/Zeek/NeuralNetwork/${DATASET_NAME}_testing" \
  "$DATA_DIR" \
  "Zeek"

########################################
# Hermessim cleanup: delete subfolders with no .pkl inside their immediate subfolders
########################################

HERMES_BASE="$MODELS_DIR/hermessim/outputs"

if [ -d "$HERMES_BASE" ]; then
  for folder in "$HERMES_BASE"/*/; do
    [ -d "$folder" ] || continue

    has_pickle=false
    for sub in "$folder"*/; do
      if compgen -G "$sub"*.pkl > /dev/null; then
        has_pickle=true
        break
      fi
    done

    if [ "$has_pickle" = false ]; then
      echo "🗑 Deleting $folder (no pickle files found in subfolders)"
      rm -rf "$folder"
    else
      echo "✅ Keeping $folder (pickle file found)"
    fi
  done
fi

########################################
# Hermessim: copy *${DATASET_NAME}*.pkl into raw_results folder
########################################

HERMES_SRC="$MODELS_DIR/hermessim/outputs"
HERMES_DST="$RESULTS_DIR/data/raw_results/Hermessim/${DATASET_NAME}_hermessim"

mkdir -p "$HERMES_DST"
rm -f "$HERMES_DST"/*.csv 2>/dev/null || true

found_any=false
while IFS= read -r -d '' pkl_file; do
  echo "📦 Found: $pkl_file"
  cp "$pkl_file" "$HERMES_DST/"
  found_any=true
done < <(find "$HERMES_SRC" -type f -name "*${DATASET_NAME}*.pkl" -print0)

if [ "$found_any" = true ]; then
  echo "Hermessim ✅ Copy complete. Files saved to $HERMES_DST"
else
  echo "Hermessim ⚠️ No pickle files with '${DATASET_NAME}' found in $HERMES_SRC"
fi
