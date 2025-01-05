"""Script for dataset structure"""

import json
import os

import pandas as pd

CSV_PATH = "./data/dataset/cat_samples.csv"
data = pd.read_csv(CSV_PATH)

ROOT_DIR = "data"
audioset_dir = os.path.join(ROOT_DIR, "dataset/audioset")
metadata_dir = os.path.join(ROOT_DIR, "dataset/metadata")
datafiles_dir = os.path.join(metadata_dir, "datafiles")
testset_subset_dir = os.path.join(metadata_dir, "testset_subset")
valset_subset_dir = os.path.join(metadata_dir, "valset_subset")

os.makedirs(audioset_dir, exist_ok=True)
os.makedirs(datafiles_dir, exist_ok=True)
os.makedirs(testset_subset_dir, exist_ok=True)
os.makedirs(valset_subset_dir, exist_ok=True)

train_data = []
test_data = []
val_data = []

for i, row in data.iterrows():
    datapoint = {"wav": row["audio"], "caption": row["caption"]}
    if i % len(data) == 10:
        test_data.append(datapoint)
    elif i % len(data) == 1:
        val_data.append(datapoint)
    else:
        train_data.append(datapoint)

train_metadata = {"data": train_data}
with open(
    os.path.join(datafiles_dir, "audiocaps_train_label.json"), "w", encoding="utf8"
) as f:
    json.dump(train_metadata, f, indent=4)

test_metadata = {"data": test_data}
with open(
    os.path.join(testset_subset_dir, "audiocaps_test_nonrepeat_subset_0.json"),
    "w",
    encoding="utf8",
) as f:
    json.dump(test_metadata, f, indent=4)

val_metadata = {"data": val_data}
with open(
    os.path.join(valset_subset_dir, "audiocaps_val_label.json"), "w", encoding="utf8"
) as f:
    json.dump(val_metadata, f, indent=4)

dataset_root_metadata = {
    "audiocaps": "data/dataset/audioset",
    "metadata": {
        "path": {
            "audiocaps": {
                "train": "data/dataset/metadata/datafiles/audiocaps_train_label.json",
                "test": "data/dataset/metadata/testset_subset/audiocaps_test_nonrepeat_subset_0.json",
                "val": "data/dataset/metadata/valset_subset/audiocaps_val_label.json",
            }
        }
    },
}
with open(os.path.join(metadata_dir, "dataset_root.json"), "w", encoding="utf8") as f:
    json.dump(dataset_root_metadata, f, indent=4)

print("Dataset structured successfully!")
