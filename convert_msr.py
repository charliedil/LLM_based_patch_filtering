import pandas as pd
import re
import nvdlib
import time
tot_not_found = 0
df = pd.read_csv("../val.csv")#insert path here
rows = []
i=0
for index, row in df.iterrows():
    if row["target"]==1:
        fixed_func = row["vul_func_with_fix"]
        patch = row["patch"]
        cve_id = row["CVE ID"]
        print(cve_id)
        r = nvdlib.searchCVE(cveId=cve_id)[0]
        desc = r.descriptions[0].value
        time.sleep(1)
        added = []
        removed= []
        hunks= re.split(r'^@@.*?@@', patch)
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
            """print(hunks)
            print(added)
            print(removed)
            print(fixed_func)"""
            print("uhoh")
            tot_not_found+=1
        else:

            rows.append([the_hunk,desc,1])


df = pd.DataFrame(rows,columns=["content","desc","label"] )
pd.to_csv("msr_val.csv",df) #change path
print(tot_not_found)
        
        



