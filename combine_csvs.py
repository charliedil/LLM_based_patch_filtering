import pandas as pd

df = pd.read_csv("msr_val.csv")
labels = []
total = 0
for i in range(1,6):
    df1 = pd.read_csv("msr_val_"+str(i)+"_out.csv")
    labels.extend(df1["pred"])
    print(len(df1))
    total+=len(df1)
print(len(df)//5)
print(labels)
print(total)
df["label"] = labels
