
```bash
docker build NeuralNetwork/ -t hermessim
```

## Part 1 Lifting
1. dataset_info_csv + acfg => cfg_summary

```bash
python lifting/dataset_summary.py \
    --cfg_summary dbs/Dataset-1/cfg_summary/testing \
    --dataset_info_csv dbs/Dataset-1/testing_Dataset-1.csv \
    --cfgs_folder dbs/Dataset-1/features/testing/acfg_features_Dataset-1_testing
```
2. lift binaries

```bash
python lifting/pcode_lifter.py \
    --cfg_summary ./dbs/Dataset-1/cfg_summary/testing \
    --output_dir ./dbs/Dataset-1/features/testing/pcode_raw_Dataset-1_testing \
    --graph_type ALL \
    --verbose 1 \
    --nproc 32
```

## Preprocess

run preprocess/preprocess_all.sh

## Training + Inferring

```bash
python model/main.py \
    --inputdir dbs \
    --config ./model/configures/e02_repr.json \
    --dataset=one
```

