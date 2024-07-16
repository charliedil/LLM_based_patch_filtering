import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix
def score():
    df = pd.read_csv("first_half_code_mmgk.csv")
    df2 = pd.read_csv("first_half.csv")

    pred = list(df["pred"].values)
    gt = list(df2["label"].values)

    df = pd.read_csv("second_half_code_mmgk.csv")
    df2 = pd.read_csv("second_half.csv")

    pred.extend(list(df["pred"].values))
    gt.extend(list(df2["label"].values))
    print(pred)
    assert len(pred)== len(gt)
    print(confusion_matrix(gt, pred))
    precision = precision_score(gt, pred)
    recall = recall_score(gt, pred)
    f1 = f1_score(gt, pred)
    acc = accuracy_score(gt, pred)
    print(f'Precision: {precision:.2f}')
    print(f'Recall: {recall:.2f}')
    print(f'F1 Score: {f1:.2f}')
    print(f"AccL {acc:.2f}")

score()

