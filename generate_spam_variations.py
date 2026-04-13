import pandas as pd
import random

df = pd.read_csv("final_dataset.csv")

spam_df = df[df["label"] == 1]

def generate_variation(text):
    new_text = text

    prefixes = [
        "URGENT:", "Alert:", "Important:", "Action Required:",
        "Security Notice:", "Immediate Action Needed:"
    ]

    suffixes = [
        "Click now.", "Act immediately.", "Verify now.",
        "Limited time offer.", "Respond now.", "Do not ignore."
    ]

    if random.random() > 0.4:
        new_text = random.choice(prefixes) + " " + new_text

    if random.random() > 0.4:
        new_text = new_text + " " + random.choice(suffixes)

    return new_text


new_samples = []

for _, row in spam_df.iterrows():
    for _ in range(5):   # 🔥 increased
        new_text = generate_variation(row["text"])
        new_samples.append({"text": new_text, "label": 1})

new_df = pd.DataFrame(new_samples)

final_df = pd.concat([df, new_df], ignore_index=True)

final_df.to_csv("final_dataset_augmented.csv", index=False)

print("✅ New dataset created: final_dataset_augmented.csv")
print("Total samples:", len(final_df))