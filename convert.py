import pandas as pd
import re
import nvdlib
import time


def msr_to_format(input_file, output_file, recovery=False):
    tot_not_found = 0
    df = pd.read_csv(input_file)#insert path here
    rows = []
    if recovery:
        rows = pd.read_csv(output_file, index_col=0).values.tolist()
    prev_len = len(rows)
    i=0
    j=0
    for index, row in df.iterrows():
        if row["target"]==1 and i>=prev_len:
            print(index)
            desc=""
            i+=1
            fixed_func = row["vul_func_with_fix"]
            patch = row["patch"]
            cve_id = row["CVE ID"]
            print(cve_id)
            if not pd.isna(cve_id) and ", " not in str(cve_id):
                r = nvdlib.searchCVE(cveId=cve_id)[0]
                desc = r.descriptions[0].value
                time.sleep(1)
            elif ", " in str(cve_id):
                cve_ids = str(cve_id).split(", ")
                for c in cve_ids:
                    r=nvdlib.searchCVE(cveId=c)[0]
                    desc+=r.descriptions[0].value
                    time.sleep(1)
            else:
                desc = row["commit_message"]
            added = []
            removed= []
            hunks= re.split(r'@@.*?@@', patch)
            add_flag = False
            remove_flag = False
            for line in fixed_func.split("\n"):
                if add_flag:
                    added.append("+"+line[2:])
                    add_flag=False
                if remove_flag:
                    removed.append("-"+line)
                    remove_flag=False
                if line == "//fix_flaw_line_below:":
                    add_flag=True
                if line == "//flaw_line_below:":
                    remove_flag=True
            found = False
            the_hunk = None
            for hunk in hunks:
                    all_add = all(line in hunk.split("\n") for line in added)
                    all_remove = all(line in hunk.split("\n") for line in removed)
                    if all_add and all_remove:
                        found=True
                        the_hunk = hunk
            if not found:
                the_hunks = []
                for hunk in hunks:
                    for line in added:
                        if line in hunk.split("\n") and hunk not in the_hunks:
                            the_hunks.append(hunk)
                    for line in removed:
                        if line in hunk.split("\n") and hunk not in the_hunks:
                            the_hunks.append(hunk)
                for hunk in the_hunks:
                    rows.append([j, hunk, desc,1])
                    df2 = pd.DataFrame(rows, columns=["desc_id", "content", "desc", "label"])
                    df2.to_csv(output_file)
                j+=1
            else:
                rows.append([j,the_hunk,desc,1])
                df2 = pd.DataFrame(rows,columns=["desc_id","content","desc","label"] )
                df2.to_csv(output_file) #change path
                j+=1
        elif row["target"]==1:
            i+=1


    df = pd.DataFrame(rows,columns=["desc_id","content","desc","label"] )
    df.to_csv(output_file)
def format_to_msr(input_file, output_file, adj_file):
    df = pd.read_csv(output_file)
    df2 = pd.read_csv(input_file)
    thing = df["pred"].tolist()
    df2["label"] = thing
    df2.to_csv(adj_file)
