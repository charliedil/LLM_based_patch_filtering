import pandas as pd

dupl_counter = 0
total_counter = 0
merged = []
headers = ["desc_id","content", "desc", "label" ]
for i in range(1,6):
    df = pd.read_csv("msr_val_"+str(i)+".csv")
    for index, row in df.iterrows():
        desc_id = row["desc_id"]
        total_counter+=1
        if len(merged)== desc_id:
            merged.append([[desc_id, row["content"], row["desc"],row["label"]]])
        elif row["content"] == merged[desc_id][len(merged[desc_id])-1][1]:
            print("duplicate")
            dupl_counter+=1
        elif row["content"] != merged[desc_id][len(merged[desc_id])-1][1]:
            merged[desc_id].append([desc_id, row["content"], row["desc"], row["label"]])
        else:
            print("something went wrong")
            exit()
##need to output to file here

print("Duplicates: "+str(dupl_counter))
print("Total before: "+str(total_counter))
print("Total after removal: "+str(total_counter-dupl_counter))

