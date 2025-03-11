from exp import zeroshot_prompting, mod_gen_knowledge_prompting, mod_fewshot_prompting, mod_cot_prompting
from llm.llama import llama
from llm.gpt import gpt
from llm.deepseek import deepseek
from scorer import score
import sys
import pandas as pd
import argparse
from convert import msr_to_format, format_to_msr
def main():
    parser = argparse.ArgumentParser(prog="LLMBasedPatchFiltering")
    parser.add_argument("uri", help="Where is Llama being hosted. if using GPT, just put 0 for this")
    parser.add_argument("inp", help="input file. If preprocess is true, thsi should be the original data. if not, this should be the processed data file")
    parser.add_argument("out", help="output file")
    parser.add_argument("prompt", help="zeroshot, gen_know, cot, fewshot")
    parser.add_argument("model", help="gpt, llama, or deepseek. If using codellama, specify llama")
    parser.add_argument("rq", help="which rq are you running. IF 2, model should be gpt", type=int)
    parser.add_argument("-of", "--output_final", help="Final output file (required for RQ2, not used for RQ1)", type=str)
    parser.add_argument("-p", "--preprocess", action="store_true", help="Are we running on the original data? if this is true, inp will be the original data. otherwise it will be the processed data. if this is specified, preprocessing will be done on the original data to generate the new preprocessed input file first before prompting at all.")
    parser.add_argument("-rp", "--preprocess_recovery", action="store_true", help="If preprocessing was interrupted, use this flag to resume. preprocess must be true")
    parser.add_argument("-cp", "--checkpoint", action="store_true", help="If filtering with prompts is interrupted, use this to resume from a checkpoint")
    args = parser.parse_args()


    uri = args.uri
    inp = args.inp
    original_inp = inp
    out = args.out
    final_out = args.output_final
    prompt = args.prompt
    model = args.model
    rq = args.rq
    preprocess = args.preprocess
    preprocess_recovery = args.preprocess_recovery
    checkpoint_bool = args.checkpoint
    llm = None
    prev_desc_id = None
    prev_pred = None
    if model == "llama":
        llm = llama(uri)
    elif model == "gpt":
        llm = gpt()
    elif model == "deepseek":
        llm =deepseek(uri)
    else:
        print("Model should be gpt, llama, or deepseek")
        exit(1)
    if rq==2:
        if model!="gpt":
            print("If rq2, model should be gpt")
            exit(1)
        if final_out is None:
            print("If RQ2, -o argument must be specified")
            exit(1)
        if preprocess:
            msr_to_format(inp, inp.split(".")[0]+"_out.csv", preprocess_recovery)
            inp = inp.split(".")[0]+"_out.csv"
        

    thing = pd.read_csv(inp)
    ## recover checkpoint, comment out for now if no checkpoint
    if checkpoint_bool:
        checkpoint = pd.read_csv(out, index_col=0)
    rows = [] # uncomment if no checkpoint
    if checkpoint_bool:
        rows = checkpoint.values.tolist()
    prev_num_rows = len(rows)
    header = []
    for index, row in thing.iterrows():
        content = row["content"]
        desc = row["desc"]
        bugfix = row["label"]
        if prompt=="zeroshot":
            header = ["content", "label", "pred"]
            if index>=prev_num_rows:
                try:
                    pred = zeroshot_prompting(llm, content, desc)
                    rows.append([content, bugfix, pred])
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)
                except Exception as e:
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)
                    print("FAILED"+str(e))
                    exit(1)

        elif prompt=="gen_know":
            header = ["content", "label", "pred", "summary", "score"]
            if index>=prev_num_rows:
                if rq==2: # we do things slightly differently if we're computingfor rq2
                    try:
                        desc_id = row["desc_id"]
                        if desc_id==prev_desc_id and prev_pred==1:
                            rows.append([content, bugfix, prev_pred, "", -1])
                            thing2 = pd.DataFrame(rows, columns=header)
                            thing2.to_csv(out)
                        else:
                            pred, summary, scorea =mod_gen_knowledge_prompting(llm, content, desc)
                            rows.append([content, bugfix, pred, summary, scorea])
                            thing2 = pd.DataFrame(rows, columns=header)
                            thing2.to_csv(out)

                            prev_desc_id = desc_id
                            prev_pred = pred
                    except Exception as e:
                        thing2 = pd.DataFrame(rows, columns=header)
                        thing2.to_csv(out)
                        print("FAILED"+str(e))
                        exit(1)


                else:
                    try:
                        pred, summary, scorea=mod_gen_knowledge_prompting(llm, content, desc)
                        rows.append([content, bugfix, pred, summary,scorea])
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
                    pred = mod_fewshot_prompting(llm, content, desc)
                    rows.append([content, bugfix, pred])
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)
                except Exception as e:
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)
                    print(f"FAILED {e}")
                    exit(1)
        elif prompt=="cot":
            header = ["content", "label", "pred"]
            if index >= prev_num_rows:
                try:
                    pred = mod_cot_prompting(llm, content, desc)
                    rows.append([content, bugfix, pred])
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)
                except Exception as e:
                    thing2 = pd.DataFrame(rows, columns=header)
                    thing2.to_csv(out)
                    print(f"FAILED {e}")
                    exit(1)

    thing2 = pd.DataFrame(rows, columns=header)
    thing2.to_csv(out)
    if rq==1:
        score(thing, thing2)
    else:
        format_to_msr(original_inp, out,final_out)
if __name__ == "__main__":
    main()
