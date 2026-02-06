# How to run the models with new dataset

## Prepare Binaries

From only binaries, build the binaries into the hierarchical structure that Binaries/Dataset-1 has

```bash
./build1.sh Dataset-1

**Go and run ./DBs/Dataset-1/Dataset-1_creation.ipynb

./build2.sh Dataset-1
```

If you don't have IDA Pro, you can download the DBs from the link provided.

## Run the models on the datasets
follow the REAME.md in each model's directory

## Analyze results
run fetch_results.sh in /Results first

then run some notebooks to prepare some of the models' outputs

Then run the AUC notebook

