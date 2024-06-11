import pandas as pd
from sklearn.metrics import classification_report
def score():
    df = pd.read_csv("thing_code_out.csv")
    df2 = pd.read_csv("thing.csv")

    pred = list(df["pred"].values)
    gt = list(df2["label"].values)

    """df = pd.read_csv("second_half_out.csv")
    df2 = pd.read_csv("second_half.csv")

    pred.extend(list(df["pred"].values))
    gt.extend(list(df2["label"].values))
    """
    assert len(pred)== len(gt)

    report = classification_report(gt, pred)

    print(report)
score()
