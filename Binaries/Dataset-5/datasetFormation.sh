#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SOURCE_BASE="$SCRIPT_DIR/source_projects"
OUTPUT_DIR="$SCRIPT_DIR/Dataset-5"

SOURCE_DIRS=()

for variant in A B C D E F; do
    for id in {345..360}; do
        SOURCE_DIRS+=("$SOURCE_BASE/${id}-${variant}")
    done
done

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

for dir in "${SOURCE_DIRS[@]}"; do
    base_dir=$(basename "$dir")
    subfolder="$OUTPUT_DIR/$base_dir"
    mkdir -p "$subfolder"

    for file in "$dir"/*.c; do
        [ -f "$file" ] || continue

        filename=$(basename "$file" .c)
        gcc "$file" -o "$subfolder/$base_dir-$filename"

        if [ $? -eq 0 ]; then
            echo "Compiled $file"
        else
            echo "Failed $file"
        fi
    done
done
