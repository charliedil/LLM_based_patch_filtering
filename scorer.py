import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix
def score(inp, out):
    #df = pd.read_csv("thing_modcot_out.csv")
    #df2 = pd.read_csv("thing.csv")

    pred = list(inp["pred"].values)
    gt = list(out["label"].values)

    assert len(pred)== len(gt)

    precision = precision_score(gt, pred)
    recall = recall_score(gt, pred)
    f1 = f1_score(gt, pred)
    acc = accuracy_score(gt, pred)

    print(confusion_matrix(gt, pred))
    print(f'Precision: {precision:.2f}')
    print(f'Recall: {recall:.2f}')
    print(f'F1 Score: {f1:.2f}')
    print(f'Acc Score {acc:.2f}')

