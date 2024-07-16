import pandas as pd

df = pd.read_csv("../val.csv")
df = df[df["target"]==1]
print(df["CVE ID"].isna().sum())
print(df.shape[0])
