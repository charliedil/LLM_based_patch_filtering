import pandas as pd

df = pd.read_csv("../prompting_for_patch_datasets/linevul_data/val.csv")
df = df[df["target"]==1]
print(df["patch"].isna().sum())
print(df.shape[0])
