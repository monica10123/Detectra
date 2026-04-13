import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

all_texts = []
all_labels = []

# ---------------- UCI SMS DATASET ----------------
with open(os.path.join(DATASET_DIR, "sms_spam.txt"), encoding="latin-1") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 2:
            label = 1 if parts[0] == "spam" else 0
            text = parts[1]

            all_texts.append(text)
            all_labels.append(label)

print("Loaded UCI dataset")

# ---------------- KAGGLE SMS DATASET ----------------
kaggle_path = os.path.join(DATASET_DIR, "spam_kaggle.csv")

if os.path.exists(kaggle_path):
    df_kaggle = pd.read_csv(kaggle_path)

    for _, row in df_kaggle.iterrows():
        text = str(row["Message"])
        label = 1 if row["Category"] == "spam" else 0

        all_texts.append(text)
        all_labels.append(label)

    print("Loaded Kaggle dataset")

# ---------------- CREATE DATAFRAME ----------------
df = pd.DataFrame({
    "text": all_texts,
    "label": all_labels
})

print("\nFINAL DATA DISTRIBUTION:")
print(df["label"].value_counts())

df.to_csv("final_dataset.csv", index=False)

print("\nDataset saved as final_dataset.csv")