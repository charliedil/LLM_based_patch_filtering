"""rq2"""
import pandas as pd
import re
import pylcs



file_path = '../val.csv'
chunk_size = 1000
thing = []
# Create a generator to read the CSV file in chunks
chunk_generator = pd.read_csv(file_path, chunksize=chunk_size) # chunks for parsing the big dataset
tot = 0 #total number of functions that aren't found
tottot = 0# total number of functions
tototot=0
for chunk in chunk_generator: #for each chunk
    for index, row in chunk.iterrows():
        func_after = row["vul_func_with_fix"]#get columns
        patch = row["patch"]
        vul = row["target"]
        if vul == 1: #if it's vulnerable
            tottot +=1
            func_name = func_after.split("\n")[0][:80] #get the truncated name
            if func_name not in patch: #if it's not in the patch, we need to get creative
                hunk_texts = []
                infunc = False
                for hunk in list(filter(None, re.split(r"(@@.*?\n)",patch))): #get individual hunks
                    if not hunk.startswith("@@"):
                        lines = hunk.split("\n") # get the lines
                        search_text = "" #search text, build from patches
                        for l in range(len(lines)):
                            if lines[l].startswith("+"): # add the plus lines
                                search_text+=lines[l][1:]
                            elif not lines[l].startswith("-"): # add everything ese
                                search_text+=lines[l]
                            if l!=len(lines)-1 and not lines[l].startswith("-"): #new lines
                                search_text+="\n"
                        if search_text in func_after:# if it's in te function
                            infunc=True
                        hunk_texts.append(search_text)# add the hunk texts into here
                if not infunc: #if we didn't find it
                    tototot+=1
                    biggest_subseq_length= 0 #subsequence time
                    biggest_subseq_t = ""
                    for t in hunk_texts:
                        sl = pylcs.lcs_sequence_length(func_after, t)
                        if sl>biggest_subseq_length:
                            biggest_subseq_length = sl
                            biggest_subseq_t=t
                    normalized_subseq_length = biggest_subseq_length/len(biggest_subseq_t)
                    if normalized_subseq_length<.75:
                        thing.append(normalized_subseq_length)
                        print(normalized_subseq_length)
                        print("FUNCTION----------------")
                        print(func_after)
                        print("patch--------------------")
                        print(biggest_subseq_t)
                        print("-------------------------")
                        tot+=1
print(tot)
print(tottot)
print(min(thing))
print(tototot)
