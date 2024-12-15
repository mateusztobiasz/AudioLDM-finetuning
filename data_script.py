"""Script for dataset structure"""

import json
import os
import shutil

import pandas as pd
from tqdm import tqdm

CSV_PATH = "audiocaps_cat_dog.csv"
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

# # Copy audio files to the audioset directory
# for audio_file in tqdm(data["audio"]):
#     file_name = os.path.basename(audio_file)
#     new_path = os.path.join(audioset_dir, file_name)
#     os.makedirs(os.path.dirname(new_path), exist_ok=True)
#     try:
#         shutil.copy(audio_file, new_path)
#     except FileNotFoundError as e:
#         print(f"Error copying {audio_file}: {e}")

train_data = []
test_data = []
val_data = []

for i, row in data.iterrows():
    datapoint = {"wav": row["audio"], "caption": row["caption"]}
    if i % 42 == 6:
        test_data.append(datapoint)
    elif i % 42 == 1:
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
