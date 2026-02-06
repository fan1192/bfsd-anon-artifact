#!/bin/bash

# Ensure a dataset name is provided as a command-line argument
if [ -z "$1" ]; then
    echo "Usage: $0 <Dataset_Name>"
    exit 1
fi

# Store the dataset name from the argument
DATASET_NAME=$1



# Delete all folders that contain $DATASET_NAME in their name
sudo find . -type d -name "*$DATASET_NAME*" -exec rm -rf {} +


# Measure time for training, testing, and validation
start_train=$(date +%s)

# Training data processing

docker run --rm \
    -v $(pwd)/../../DBs/${DATASET_NAME}/features/validation/acfg_disasm_${DATASET_NAME}_validation:/input \
    -v $(pwd):/output \
    -it asm2vec /code/i2v_preprocessing.py -d -w4 -a2v -i /input -o /output/a2v_preprocessing_${DATASET_NAME}-training

# docker run --rm \
#     -v $(pwd)/../../DBs/${DATASET_NAME}/features/training/acfg_disasm_${DATASET_NAME}_training:/input \
#     -v $(pwd):/output \
#     -it asm2vec /code/i2v_preprocessing.py -d -w4 -d2v -i /input -o /output/d2v_preprocessing_${DATASET_NAME}-training

end_train=$(date +%s)
train_time=$(( end_train - start_train ))

start_test=$(date +%s)

# Testing data processing

docker run --rm \
    -v $(pwd)/../../DBs/${DATASET_NAME}/features/testing/acfg_disasm_${DATASET_NAME}_testing:/input \
    -v $(pwd)/a2v_preprocessing_${DATASET_NAME}-training:/training_data \
    -v $(pwd):/output \
    -it asm2vec /code/i2v_preprocessing.py -w4 -a2v -i /input -v /training_data/vocabulary.csv -o /output/a2v_preprocessing_${DATASET_NAME}-testing

# # docker run --rm \
# #     -v $(pwd)/../../DBs/${DATASET_NAME}/features/testing/acfg_disasm_${DATASET_NAME}_testing:/input \
# #     -v $(pwd)/d2v_preprocessing_${DATASET_NAME}-training:/training_data \
# #     -v $(pwd):/output \
# #     -it asm2vec /code/i2v_preprocessing.py -d -w4 -d2v -i /input -v /training_data/vocabulary.csv -o /output/d2v_preprocessing_${DATASET_NAME}-testing

end_test=$(date +%s)
test_time=$(( end_test - start_test ))

start_validation=$(date +%s)

# Validation data processing

# docker run --rm \
#     -v $(pwd)/../../DBs/${DATASET_NAME}/features/validation/acfg_disasm_${DATASET_NAME}_validation:/input \
#     -v $(pwd)/a2v_preprocessing_${DATASET_NAME}-training:/training_data \
#     -v $(pwd):/output \
#     -it asm2vec /code/i2v_preprocessing.py -w16 -a2v -i /input -v /training_data/vocabulary.csv -o /output/a2v_preprocessing_${DATASET_NAME}-validation

# docker run --rm \
#     -v $(pwd)/../../DBs/${DATASET_NAME}/features/validation/acfg_disasm_${DATASET_NAME}_validation:/input \
#     -v $(pwd)/d2v_preprocessing_${DATASET_NAME}-training:/training_data \
#     -v $(pwd):/output \
#     -it asm2vec /code/i2v_preprocessing.py -d -w4 -d2v -i /input -v /training_data/vocabulary.csv -o /output/d2v_preprocessing_${DATASET_NAME}-validation

end_validation=$(date +%s)
validation_time=$(( end_validation - start_validation ))

# Print out the time spent
echo "Time spent on training: ${train_time} seconds"
echo "Time spent on testing: ${test_time} seconds"
echo "Time spent on validation: ${validation_time} seconds"
