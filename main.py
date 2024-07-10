"""rq1"""
from exp import baseline_prompting, gen_knowledge_prompting, sep_gen_knowledge_prompting, fewshot_prompting, cot_prompting, zeroshot_prompting, mod_gen_knowledge_prompting, mod_fewshot_prompting, mod_cot_prompting
from llama import llama
from lora import lora
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
    elif model == "lora":
        llm = lora(uri)
    thing = pd.read_csv(inp)
    ## recover checkpoint, comment out for now if no checkpoint
    #checkpoint = pd.read_csv(out, index_col=0)
    rows = [] # uncomment if no checkpoint
    #rows = checkpoint.values.tolist()
    prev_num_rows = len(rows)
    header = []
    for index, row in thing.iterrows():
        content = row["content"]
        desc = row["desc"]
        bugfix = row["label"]
        if prompt=="baseline":
            header = ["content", "label", "pred"]
            if index>=prev_num_rows:
                try:
                    pred = zeroshot_prompting(llm, content, desc, bugfix)
                    print("pred success")
                    rows.append([content, bugfix, pred])
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)
                except Exception as e:
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)
                    print("FAILED"+str(e))
                    exit()

        elif prompt=="gen_know":
            header = ["content", "label", "pred", "summary", "score"]
            if index>=prev_num_rows:
                try: 
                    pred, summary, score =mod_gen_knowledge_prompting(llm, content, desc, bugfix)
                    rows.append([content, bugfix, pred, summary, score])
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)


                except Exception as e:
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)
                    print("FAILED"+str(e))
                    exit()

        elif prompt=="fewshot":
            header = ["content", "label", "pred"]
            if index>=prev_num_rows:
                try:
                    pred = mod_fewshot_prompting(llm, content, desc, bugfix)
                    rows.append([content, bugfix, pred])
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)
                except Exception as e:
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)
                    print(f"FAILED {e}")
                    exit()
        elif prompt=="cot":
            header = ["content", "label", "pred"]
            if index >= prev_num_rows:
                try:
                    pred = mod_cot_prompting(llm, content, desc, bugfix)
                    rows.append([content, bugfix, pred])
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)
                except Exception as e:
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)
                    print(f"FAILED {e}")
                    exit()

    thing2 = pd.DataFrame(rows, columns=header)
    thing2.to_csv(out)
if __name__ == "__main__":
    main()
