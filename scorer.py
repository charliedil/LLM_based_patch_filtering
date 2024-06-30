import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
def score():
    df = pd.read_csv("thing_zs_out.csv")
    df2 = pd.read_csv("thing.csv")

    pred = list(df["pred"].values)
    gt = list(df2["label"].values)

    assert len(pred)== len(gt)

    precision = precision_score(gt, pred)
    recall = recall_score(gt, pred)
    f1 = f1_score(gt, pred)
    acc = accuracy_score(gt, pred)
    print(f'Precision: {precision:.2f}')
    print(f'Recall: {recall:.2f}')
    print(f'F1 Score: {f1:.2f}')
    print(f'Acc Score {acc:.2f}')

score()
