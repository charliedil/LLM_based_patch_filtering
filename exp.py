import pandas as pd
import json
def few_shot_prompting(llm, content, desc, bugfix):
    fewshot_prompt_string= """Input:
         extent+=image->columns*sizeof(uint32);
 #endif
         strip_pixels=(unsigned char *) AcquireQuantumMemory(extent,
-          sizeof(*strip_pixels));
+          2*sizeof(*strip_pixels));
         if (strip_pixels == (unsigned char *) NULL)
           ThrowTIFFException(ResourceLimitError,"MemoryAllocationFailed");
         (void) memset(strip_pixels,0,extent*sizeof(*strip_pixels));
Output:
yes
Input:
     'transparent': (0, 0, 0, 0),
 }
 
-RGBA = re.compile(r'rgba\([ \n\r\t]*(.+?)[ \n\r\t]*\)')
-RGB = re.compile(r'rgb\([ \n\r\t]*(.+?)[ \n\r\t]*\)')
+RGBA = re.compile(r'rgba\((.+?)\)')
+RGB = re.compile(r'rgb\((.+?)\)')
 HEX_RRGGBB = re.compile('#[0-9a-f]{6}')
 HEX_RGB = re.compile('#[0-9a-f]{3}')
Knowledge:
This hunk simplifies the two regular expressions RGBA and RGB to avoid reDOS attacks. [\n\r\t]* was removed in both, as the expressions could suffer exponential backtracking due to the nondeterministic nature of how regular expression matching is done. By removing this part of the regular expressions, the matches are still the same as the (.+?) still matches any number of characters in the parentheses. This hunk adds .strip() to the match groups for both the RGBA and RGB regular expressions. This strips the whitespace which was just matched in the functions and lets the color values be used easier even if the formatting was not perfect. This does not directly fix the vulnerability, but was more of a result of the patch.
Input:
 module.exports = function killport(port) {
   return (new Promise(function(resolve, reject) {
+    if (!/^\d+$/.test(port)) throw new Error('port must be a number.');
     var cmd = 'lsof -i:' + port; 
     cp.exec(cmd, function(err, stdout, stderr){
       // do not check `err`, if no process found
Knowledge:
This hunk adds a check to verify that the port entered is a number, and if it is not it throws an error. This change fixes how the use of the child_process exec function was used without input sanitization, which lets attackers execute arbritrary commands as the provided port.
Following the same format above from the examples, generate knowledge for the following input:

"""

def gen_knowledge_prompting(llm,content, desc, bugfix):
    fewshot_prompt_string= """Input:
         extent+=image->columns*sizeof(uint32);
 #endif
         strip_pixels=(unsigned char *) AcquireQuantumMemory(extent,
-          sizeof(*strip_pixels));
+          2*sizeof(*strip_pixels));
         if (strip_pixels == (unsigned char *) NULL)
           ThrowTIFFException(ResourceLimitError,"MemoryAllocationFailed");
         (void) memset(strip_pixels,0,extent*sizeof(*strip_pixels));
Knowledge:
This hunk helps prevent potential TIFF related heap based buffer overflow by dynamically allocating two times the amount of pixels in the strip instead of the exact amount. By allocating more space than necessary the heap based buffer overflow vulnerability is able to be prevented and this code no longer results in program crash and denial of service.
Input:
     'transparent': (0, 0, 0, 0),
 }
 
-RGBA = re.compile(r'rgba\([ \n\r\t]*(.+?)[ \n\r\t]*\)')
-RGB = re.compile(r'rgb\([ \n\r\t]*(.+?)[ \n\r\t]*\)')
+RGBA = re.compile(r'rgba\((.+?)\)')
+RGB = re.compile(r'rgb\((.+?)\)')
 HEX_RRGGBB = re.compile('#[0-9a-f]{6}')
 HEX_RGB = re.compile('#[0-9a-f]{3}')
Knowledge:
This hunk simplifies the two regular expressions RGBA and RGB to avoid reDOS attacks. [\n\r\t]* was removed in both, as the expressions could suffer exponential backtracking due to the nondeterministic nature of how regular expression matching is done. By removing this part of the regular expressions, the matches are still the same as the (.+?) still matches any number of characters in the parentheses. This hunk adds .strip() to the match groups for both the RGBA and RGB regular expressions. This strips the whitespace which was just matched in the functions and lets the color values be used easier even if the formatting was not perfect. This does not directly fix the vulnerability, but was more of a result of the patch.
Input:
 module.exports = function killport(port) {
   return (new Promise(function(resolve, reject) {
+    if (!/^\d+$/.test(port)) throw new Error('port must be a number.');
     var cmd = 'lsof -i:' + port; 
     cp.exec(cmd, function(err, stdout, stderr){
       // do not check `err`, if no process found
Knowledge:
This hunk adds a check to verify that the port entered is a number, and if it is not it throws an error. This change fixes how the use of the child_process exec function was used without input sanitization, which lets attackers execute arbritrary commands as the provided port.
Following the same format above from the examples, generate knowledge for the following input:

"""
    #thing = pd.read_csv("first_half.csv")
    rows = []
    header = ["content", "desc", "label", "chosen_summary", "pred"]
   # for index, row in thing.iterrows():
    #    content = row["content"]
     #   desc = row["desc"]
      #  bugfix = row["label"]
    summaries = []
    for i in range(3):
        history=[]
        history.append({"role":"system", "content":"Your job is to generate knowledge for a given input"})
        history.append({"role":"user", "content":fewshot_prompt_string+content})

        result, history = llm.run(history)
        summaries.append(result)
    max_ans = ""
    max_score = 0
    max_summary = 0
    for i in range(3):
        flag = 0
        while(flag!=3):
            history = []
            history.append({"role":"system", "content":"Using the knowledge provided, answer the question given"})
            history.append({"role":"user", "content":"Question: Is this hunk fixing a bug with the description:\n"+desc+"\nHunk:\n"+content+"\nKnowledge:"+summaries[i]+"\nPlease answer yes or no and provide a confidence score on a scale of 0 to 1 be realistic and you have to provide one. Do not provide any more information. DO NOT EXPLAIN. Provide answer in this format {\"ans\":\"<Answer>\", \"conf\":\"<Confidence score>\"}"})
            result, history = llm.run(history)
            try:
                result_json = json.loads(result)
                score = float(result_json["conf"])
                answer = result_json["ans"].lower()
                if answer in ["yes", "no"]:
                    if score>= max_score:
                        max_score = score
                        max_ans = answer
                        max_summary=i
                    flag = 3
                else:
                    print("no ans retrying", result)
                    flag+=1
            except Exception as error:
                print("EXCEPTION retrying", result, error)
                flag+=1
    pred = 0 
    if max_ans=="yes":
        pred=1
        #rows.append([content, desc, bugfix, summaries[i], pred])
    #thing2 = pd.DataFrame(rows, columns=header)
    #thing2.to_csv("thing21.csv")
    return pred, summaries[max_summary], max_score

def sep_gen_knowledge_prompting(llm, content, desc, bugfix):
    #thing = pd.read_csv("first_half.csv")
    rows = []
    header = ["content", "desc", "label", "chosen_summary", "pred"]
   # for index, row in thing.iterrows():
    #    content = row["content"]
     #   desc = row["desc"]
      #  bugfix = row["label"]
    summaries = []
    for i in range(3):
        history=[]
        history.append({"role":"system", "content":"Your job is to generate knowledge for a given input"})
        history.append({"role":"user", "content":"""Input:
            extent+=image->columns*sizeof(uint32);
 #endif
         strip_pixels=(unsigned char *) AcquireQuantumMemory(extent,
-          sizeof(*strip_pixels));
+          2*sizeof(*strip_pixels));
         if (strip_pixels == (unsigned char *) NULL)
           ThrowTIFFException(ResourceLimitError,"MemoryAllocationFailed");
         (void) memset(strip_pixels,0,extent*sizeof(*strip_pixels));"""})
        history.append({"role":"assistant", "content":"""Knowledge: 
            This hunk helps prevent potential TIFF related heap based buffer overflow by dynamically allocating two times the amount of pixels in the strip instead of the exact amount. By allocating more space than necessary the heap based buffer overflow vulnerability is able to be prevented and this code no longer results in program crash and denial of service.
"""})
        history.append({"role":"user", "content":"""Input: 
                 'transparent': (0, 0, 0, 0),
 }

-RGBA = re.compile(r'rgba\([ \n\r\t]*(.+?)[ \n\r\t]*\)')
-RGB = re.compile(r'rgb\([ \n\r\t]*(.+?)[ \n\r\t]*\)')
+RGBA = re.compile(r'rgba\((.+?)\)')
+RGB = re.compile(r'rgb\((.+?)\)')
 HEX_RRGGBB = re.compile('#[0-9a-f]{6}')
 HEX_RGB = re.compile('#[0-9a-f]{3}')"""})
        history.append({"role":"assistant", "content":"""Knowledge: 
            This hunk simplifies the two regular expressions RGBA and RGB to avoid reDOS attacks. [\n\r\t]* was removed in both, as the expressions could suffer exponential backtracking due to the nondeterministic nature of how regular expression matching is done. By removing this part of the regular expressions, the matches are still the same as the (.+?) still matches any number of characters in the parentheses. This hunk adds .strip() to the match groups for both the RGBA and RGB regular expressions. This strips the whitespace which was just matched in the functions and lets the color values be used easier even if the formatting was not perfect. This does not directly fix the vulnerability, but was more of a result of the patch.
"""})
        history.append({"role":"user", "content":"""Input: 
             module.exports = function killport(port) {
   return (new Promise(function(resolve, reject) {
+    if (!/^\d+$/.test(port)) throw new Error('port must be a number.');
     var cmd = 'lsof -i:' + port;
     cp.exec(cmd, function(err, stdout, stderr){
       // do not check `err`, if no process found"""})
        history.append({"role":"assistant", "content":"""Knowledge: 
        This hunk adds a check to verify that the port entered is a number, and if it is not it throws an error. This change fixes how the use of the child_process exec function was used without input sanitization, which lets attackers execute arbritrary commands as the provided port.
"""})
        history.append({"role":"user", "content":"Input: \n"+content})
        print("HISTORY:",str(history))
        result, history = llm.run(history)
        summaries.append(result)
    max_ans = ""
    max_score = 0
    max_summary = 0
    for i in range(3):
        flag = 0
        while(flag!=3):
            history = []
            history.append({"role":"system", "content":"Using the knowledge provided, answer the question given"})
            history.append({"role":"user", "content":"Question: Is this hunk fixing a bug with the description:\n"+desc+"\nHunk:\n"+content+"\nKnowledge:"+summaries[i]+"\nPlease answer yes or no and provide a confidence score on a scale of 0 to 1 be realistic and you have to provide one. Do not provide any more information. DO NOT EXPLAIN. Provide answer in this format {\"ans\":\"<Answer>\", \"conf\":\"<Confidence score>\"}"})
            print("HISTORY:",str(history))
            result, history = llm.run(history)
            try:
                result_json = json.loads(result)
                score = float(result_json["conf"])
                answer = result_json["ans"].lower()
                if answer in ["yes", "no"]:
                    if score>= max_score:
                        max_score = score
                        max_ans = answer
                        max_summary=i
                    flag = 3
                else:
                    print("no ans retrying", result)
                    flag+=1
            except Exception as error:
                print("EXCEPTION retrying", result, error)
                flag+=1
    pred = 0 
    if max_ans=="yes":
        pred=1
        #rows.append([content, desc, bugfix, summaries[i], pred])
    #thing2 = pd.DataFrame(rows, columns=header)
    #thing2.to_csv("thing21.csv")
    return pred, summaries[max_summary], max_score



def baseline_prompting(llm, content, desc, bugfix):
    fewshot_prompt_string = "The code hunks provided are from a larger commit for a bugfix. Not every hunk contains the actual bugfix. Does the following code hunk contain a bugfix:"
    thing = pd.read_csv("first_half.csv")
    rows = []
    header = ["content","label", "pred"]
    #for index, row in thing.iterrows():
        #content = row["content"]
       # desc = row["desc"]
       # bugfix = row["label"]
    history=[]
    history.append({"role":"user", "content":fewshot_prompt_string+"\n"+content+"\nPlease answer yes or no. Do not provide any more information. DO NOT EXPLAIN. Provide answer in this format {\"ans\":\"<Answer>\"}"})
    flag=0
    pred=0
    while flag!=3:
        history=[]
        history.append({"role":"user", "content":fewshot_prompt_string+"\n"+content+"\nPlease answer yes or no. Do not provide any more information. DO NOT EXPLAIN. Provide answer in this format {\"ans\":\"<Answer>\"}"})
        result, history = llm.run(history)
        try:
            result_json = json.loads(result)
            answer = result_json["ans"].lower()
            if answer in ["yes", "no"]:
                if answer=="yes":
                    pred=1
                else:
                    pred=0
                flag = 3
            else:
                print("no answer retrying")
                flag+=1

        except Exception as e:
            print(str(e)+"retrying")
            flag+=1

    #rows.append([content, bugfix, pred])
    #thing2 = pd.DataFrame(rows, columns=header)
    #thing2.to_csv("thing21.csv")
    return pred
 


 

        

