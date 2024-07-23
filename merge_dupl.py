import pandas as pd
merged = []
headers = ["content","label", "pred", "summary", "score" ]
prev="filler"
for i in range(1,6):
    df = pd.read_csv("datasets/msr_train_"+str(i)+"_out.csv")
    for index, row in df.iterrows():
        content = row["content"]
        label = row["label"]
        pred = row["pred"]
        summary = row["summary"]
        score = row["score"]

        if content !=prev:
            merged.append([content, label, pred, summary, score])
            prev = content
df = pd.DataFrame(merged, columns=headers)
df.to_csv("merged_prev_train.csv")
print("outputted to csv")

##need to output to file here
