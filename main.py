from exp import baseline_prompting, gen_knowledge_prompting, sep_gen_knowledge_prompting
from llama import llama
from gpt import gpt
import sys
import pandas as pd
def main():
    print(sys.argv)
    if len(sys.argv) != 6:
        print("Please provide 5 arguments: uri inputfile outputfile prompt model")
        print("prompt options: baseline, gen_know")
        exit()
    uri = sys.argv[1]
    inp = sys.argv[2]
    out = sys.argv[3]
    prompt = sys.argv[4]
    model = sys.argv[5]
    llm = None
    if model == "llama":
        llm = llama(uri)
    elif model == "gpt":
        llm = gpt()
    thing = pd.read_csv(inp)
    rows = []
    header = []
    for index, row in thing.iterrows():
        content = row["content"]
        desc = row["desc"]
        bugfix = row["label"]
        if prompt=="baseline":
            header = ["content", "label", "pred"]
            pred = baseline_prompting(llm, content, desc, bugfix)
            rows.append([content, bugfix, pred])
        elif prompt=="gen_know":
            header = ["content", "label", "pred", "summary", "score"]
            try: 
                pred, summary, score =gen_knowledge_prompting(llm, content, desc, bugfix)
                rows.append([content, bugfix, pred, summary, score])
            except:
                thing2 = pd.DataFrame(rows, columns=header)
                thing2.to_csv(out)
                exit()


    thing2 = pd.DataFrame(rows, columns=header)
    thing2.to_csv(out)
if __name__ == "__main__":
    main()
