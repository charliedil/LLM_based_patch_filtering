import pandas as pd
from random import sample
from sklearn.metrics import classification_report
def extract_mistakes():
    df = pd.read_csv("thing21.csv")
    df2 = pd.read_csv("first_half.csv")

    pred = list(df["pred"].values)
    gt = list(df2["label"].values)
    content = list(df["content"].values)
    chosen_summaries = list(df["chosen_summary"].values)
    desc = list(df["desc"].values)
    df = pd.read_csv("thing22.csv")
    df2 = pd.read_csv("second_half.csv")

    pred.extend(list(df["pred"].values))
    gt.extend(list(df2["label"].values))
    content.extend(list(df["content"].values))
    chosen_summaries.extend(list(df["chosen_summary"].values))
    desc.extend(list(df["desc"].values))
   # assert len(pred)== len(gt)

    #report = classification_report(gt, pred)

   # print(report)
    headers = ["pred", "gt", "desc", "content","summary"]
    all_incorrect = []
    for i in range(len(pred)):
        if pred[i] != gt[i]:
            all_incorrect.append([pred[i], gt[i],desc[i], content[i], chosen_summaries[i]])
    example_incorrect = sample(all_incorrect, 10)

    df = pd.DataFrame(example_incorrect)
    df.to_csv("example.csv")
extract_mistakes()
