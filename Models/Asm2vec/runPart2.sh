#!/bin/bash

# Ensure a dataset name is provided as a command-line argument
if [ -z "$1" ]; then
    echo "Usage: $0 <Dataset_Name>"
    exit 1
fi

# Store the dataset name from the argument
DATASET_NAME=$1


# Measure time for training, testing, and validation
start_train=$(date +%s)

# Training

docker run --rm \
    -v $(pwd)/a2v_preprocessing_${DATASET_NAME}-training:/input \
    -v $(pwd):/output \
    -it asm2vec /code/i2v.py -d --asm2vec --train -e1 -w4 --inputdir /input/ -o /output/asm2vec_train_${DATASET_NAME}-training

end_train=$(date +%s)
train_time=$(( end_train - start_train ))

start_validation=$(date +%s)
# Validation
# docker run --rm \
#     -v $(pwd)/a2v_preprocessing_${DATASET_NAME}-validation:/input \
#     -v $(pwd)/asm2vec_train_${DATASET_NAME}-training:/checkpoint \
#     -v $(pwd):/output \
#     -it asm2vec /code/i2v.py -d --asm2vec --inference -e1 -w4 --inputdir /input/ -c /checkpoint -o /output/asm2vec_inference_${DATASET_NAME}-validation

end_validation=$(date +%s)
validation_time=$(( end_validation - start_validation ))

start_test=$(date +%s)
# Testing
docker run --rm \
    -v $(pwd)/a2v_preprocessing_${DATASET_NAME}-testing:/input \
    -v $(pwd)/asm2vec_train_${DATASET_NAME}-training:/checkpoint \
    -v $(pwd):/output \
    -it asm2vec /code/i2v.py -d --asm2vec --inference -e1 -w4 --inputdir /input/ -c /checkpoint -o /output/asm2vec_inference_${DATASET_NAME}-testing

end_test=$(date +%s)
test_time=$(( end_test - start_test ))


# Print out the time spent
echo "Time spent on training: ${train_time} seconds"
echo "Time spent on testing: ${test_time} seconds"
echo "Time spent on validation: ${validation_time} seconds"
