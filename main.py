from exp import baseline_prompting, gen_knowledge_prompting, sep_gen_knowledge_prompting
from llama import llama
import sys
import pandas as pd
def main():
    print(sys.argv)
    if len(sys.argv) != 6:
        print("Please provide 5 arguments: node port inputfile outputfile prompt")
        print("prompt options: baseline, gen_know")
        exit()
    node = sys.argv[1]
    port = sys.argv[2]
    inp = sys.argv[3]
    out = sys.argv[4]
    prompt = sys.argv[5]
    llama_uri = f"http://athena{node}:{port}/v1/chat/completions"
    llama_model = llama(llama_uri)
    thing = pd.read_csv(inp)
    rows = []
    header = []
    for index, row in thing.iterrows():
        content = row["content"]
        desc = row["desc"]
        bugfix = row["label"]
        if prompt=="baseline":
            header = ["content", "label", "pred"]
            pred = baseline_prompting(llama_model, content, desc, bugfix)
            rows.append([content, bugfix, pred])
        elif prompt=="gen_know":
            header = ["content", "label", "pred", "summary", "score"]
            pred, summary, score =sep_gen_knowledge_prompting(llama_model, content, desc, bugfix)
            rows.append([content, bugfix, pred, summary, score])

    thing2 = pd.DataFrame(rows, columns=header)
    thing2.to_csv(out)
if __name__ == "__main__":
    main()
