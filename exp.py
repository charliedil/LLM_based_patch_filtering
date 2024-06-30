import pandas as pd
import json
import re
def fewshot_prompting(llm, content, desc, bugfix):
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
{"ans":"yes"}
Input:
     'transparent': (0, 0, 0, 0),
 }
 
-RGBA = re.compile(r'rgba\([ \n\r\t]*(.+?)[ \n\r\t]*\)')
-RGB = re.compile(r'rgb\([ \n\r\t]*(.+?)[ \n\r\t]*\)')
+RGBA = re.compile(r'rgba\((.+?)\)')
+RGB = re.compile(r'rgb\((.+?)\)')
 HEX_RRGGBB = re.compile('#[0-9a-f]{6}')
 HEX_RGB = re.compile('#[0-9a-f]{3}')
Output:
{"ans":"no"}
Input:
 module.exports = function killport(port) {
   return (new Promise(function(resolve, reject) {
+    if (!/^\d+$/.test(port)) throw new Error('port must be a number.');
     var cmd = 'lsof -i:' + port; 
     cp.exec(cmd, function(err, stdout, stderr){
       // do not check `err`, if no process found
Output:
{"ans":"yes"}
Following the same format above from the examples, identify if the following input contains a bugfix. Do not provide any other information. Do not explain. Provide your answer in this format: {"ans":"<Answer>"}
"""
    flag = 0
    pred=0
    while flag!=3:
        history=[]
        history.append({"role":"user", "content":fewshot_prompt_string+"\n"+content})
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
            print(history)
            print(result)
            print(str(e)+"retrying")
            flag+=1
    return pred
def mod_gen_knowledge_prompting(llm, content, desc, bugfix):
    fewshot_prompt_string = """Description: 'I believe the Beider Morse Phonetic Matching algorithm was added in Commons Codec 1.6\n\nThe BMPM algorithm is an EVOLVING algorithm that is currently on version 3.02 though it had been static since version 3.01 dated 19 Dec 2011 (it was first available as opensource as version 1.00 on 6 May 2009).\n\nI can see nothing in the Commons Codec Docs to say which version of BMPM was implemented so I am not sure if the problem with the algorithm as coded in the Codec is simply an old version or whether there are more basic problems with the implementation.\n\nHow do I determine the version of the algorithm that was implemented in the Commons Codec?\n\nHow do we ensure that the algorithm is updated if/when the BMPM algorithm changes?\n\nHow do we ensure that the algorithm as coded in the Commons Codec is accurate and working as expected?'
Hunk:
-        assertEquals(encode(args, false, ""Angelo""), ""AnElO|AnSelO|AngElO|AngzelO|AnkselO|AnzelO"");
+        assertEquals(encode(args, false, ""Angelo""), ""YngYlo|Yngilo|angYlo|angilo|anilo|anxilo|anzilo|ongYlo|ongilo|onilo|onxilo|onzilo"");
Knowledge: This hunk modifies an assertion in a unit test for the encode() method. It adds more comparisons against different variations of the name “Angelo”, which are the result of different phonetic encoding schemes. This change is a change to a test.

Description: "My project, which is associated with the Grid, uses limited proxy certificates for digital signature. I.e., the signing application holds a user's permanent certificate, signed by a CA and a proxy certificate signed with the permanent certificate. The application signs a message using the proxy certificate and includes both the proxy and permanent certificates in the message header as a WS-Security direct reference to a BinarySecurityToken. The service has the CA certificate with which the user's permanent certficate was signed. Therefore, to establish trust, the service has to chain back from the proxy to the permanent certificate and then to the CA certificate.\n\nWSSignEnvelope includes both certificates correctly but WSSecurityEngine fails when checking the chain of trust. WSSecurityEngine..processSecurityHeader() only adds one certificate to the results passed back to WSDoAllReceiver; it ignores the intermediate certificate in the chain."
Hunk: 
-     * get a byte array given an array of X509 certificates.
+     * Get a byte array given an array of X509 certificates.
Knowledge: This is modifying the capitalization of the word “get” in a Java comment. This change is a change to a comment.

Description: Under high load commons-dbcp (or commons-pool) exhibits thread safety issues and begins throwing various exceptions. I don't yet know the cause of the issue but it looks like a connection maybe handed out to multiple threads concurrently. Here's a few examples of the exceptions we are getting:\n\n{noformat}\njvm 1    | Caused by: java.sql.SQLException: Attempted to use PooledConnection after closed() was called.\njvm 1
Hunk:
- * 
+ *
  *      http://www.apache.org/licenses/LICENSE-2.0
- * 
+ *
Knowledge:
Knowledge: This is adding a single space to the left to the asterisks in a Java comment. This is a change to the whitespace.

Description: Hello,\nWe are been using Ofbiz with DBCP based implementation.\nOfbiz uses a Head revision of DBCP (package org.apache.commons.dbcp.managed is the same as current TRUNK) and geronimo-transaction-1.0.\n\nWe are having recurrent OutOfMemory which occur on a 2 days basis.\nI analyzed the Heap Dump and I think have found the source of the problem:\nThe Heap Dump shows a Retained Heap of 400Mo by org.apache.commons.dbcp.managed.TransactionRegistry#xaResources field.\n\nAfter analyzing more deeply, the leak seems to come from what is stored in xaResources through\nxaResources.put(connection, xaResource);\n\nValues inside weak Hash map  will never be removed since XAResource holds a STRONG reference on key (connection) through:\norg.apache.commons.dbcp.managed.LocalXAConnectionFactory$LocalXAResource through:\npublic LocalXAResource(Connection localTransaction) {\n            this.connection = localTransaction;\n        }\n\n\nFound in WeakHashMap javadoc:\nImplementation note: The value objects in a WeakHashMap are held by ordinary strong references. >>>>>>>>>>>>>Thus care should be taken to ensure that value objects do not strongly refer to their own keys <<<<<<<<, either directly or indirectly, since that will prevent the keys from being discarded. Note that a value object may refer indirectly to its key via the WeakHashMap itself; that is, a value object may strongly refer to some other key object whose associated value object, in turn, strongly refers to the key of the first value object. One way to deal with this is to wrap values themselves within WeakReferences before inserting, as in: m.put(key, new WeakReference(value)), and then unwrapping upon each get. \n\nPhilippe Mouawad\nhttp://www.ubik-ingenierie.com'
Hunk:
-import javax.transaction.xa.XAResource;
-import javax.transaction.TransactionManager;
-import javax.transaction.Transaction;
-import javax.transaction.SystemException;
-import javax.transaction.Status;
Knowledge:
The hunk removes several import statements related to transaction management and XA resources in a Java class. The import statements are not relevant to the problem description, so this is an unrelated code change.

Desctiption: Calling stopSpyStream on TelnetClient sets spyStream to null without regard to whether _spyRead or _spyWrite are being invoked on another thread. \n\nResulting NPE in _spyRead/_spy_Write is caught in TelnetInputStream.run() which goes on to close the stream.\n\nMay be able to fix by taking local copy of spyStream (which ought also to be volatile) in both of _spyRead and _spyWrite. E.g. for _spyRead:\n\n    void _spyRead(int ch)\n    {\n        OutputStream _spyStream = spyStream;\n        \n        if (_spyStream != null)\n        {\n            try\n            {\n                if (ch != '\\r')\n                {\n                    _spyStream.write(ch);\n                    if (ch == '\\n')\n                    {\n                        _spyStream.write('\\r');\n                    }\n                    _spyStream.flush();\n                }\n            }\n            catch (IOException e)\n            {\n                spyStream = null;\n            }\n        }\n    }
Hunk:
-                    spyStream.write(ch);
-                    spyStream.flush();
+                    spy.write(ch);
+                    spy.flush();
Knowledge:
This change is renaming the variable spyStream to spy. It is reflecting a change in name to a variable, so it is a refactoring code change.

Description:
http://redline-rpm.org/ creates CPIO archives with a non-zero file mode on the trailer. This causes an IllegalArgumentException when reading the file. I've attached a patch and test archive to fix this.
Hunk: 
-        return (this.mode & S_IFMT) == C_ISBLK;
+        return CpioUtil.fileType(mode) == C_ISBLK;
Knowledge:
This hunk replaces the bitwise operation for file type checking in CPIO archives with a utility method call to CpioUtil.fileType(), addressing the IllegalArgumentException exceptions caused by non-zero file modes.
"""
    summaries = []
    for i in range(3):
        history=[]
        history.append({"role":"system", "content":"Your job is to generate knowledge for a given hunk and description of the patch it is from"})
        history.append({"role":"user", "content":fewshot_prompt_string+"\nDescription: "+desc+"\nHunk:\n"+content})

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
            history.append({"role":"user", "content":"The following code hunk is part of a larger commit intended to fix the following bug. Code hunks that only contain changes to whitespace, documentation, tests are not bug fixes. Code hunks that perform regactoring or unrelated changes do not qualify as bugfixes. Evaluate the code hunk below and determine if it contains a fix to the described bug.\nDescription: "+desc+"\nKnowledge: "+summaries[i]+"\n Please respond with \"yes\" or \"no\" and a confidence score on a scale from 0 to 1. Do not provider any more information or explanations. Format your response as follows: {\"ans\":<Answer>, \"conf\":<Confidence Score>}"})
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

def zeroshot_prompting(llm, content, desc, bugfix):
    fewshot_prompt_string = f"Bug description: {desc}\n\nThe following code hunk is part of a larger commit intended to fix the above bug. Code hunks that only contain changes to whitespace, documentation, tests are not bug fixes. Code hunks that perform refactoring or unrelated changes do not qualify as bugfixes.\n\nEvaluate the code hunk below and determine if it contains a fix to the described bug:"
    rows = []
    header = ["content","label", "pred"]
    #for index, row in thing.iterrows():
        #content = row["content"]
       # desc = row["desc"]
       # bugfix = row["label"]
    history=[]
    history.append({"role":"user", "content":fewshot_prompt_string+"\n\n"+content+"\nPlease respond with \"yes\" or \"no\" only. Do not provide any more information or explanations. Format your response as follows: {\"ans\":\"<Answer>\"}"})
    flag=0
    pred=0
    while flag!=3:
        history=[]
        history.append({"role":"user", "content":fewshot_prompt_string+"\n\n"+content+"\nPlease respond with \"yes\" or \"no\" only. Do not provide any more information or explanations. Format your response as follows: {\"ans\":\"<Answer>\"}"})
 
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

def baseline_prompting(llm, content, desc, bugfix):
    fewshot_prompt_string = "The code hunks provided are from a larger commit for a bugfix. Not every hunk contains the actual bugfix. Does the following code hunk contain a bugfix:"
    rows = []
    header = ["content","label", "pred"]
    #for index, row in thing.iterrows():
        #content = row["content"]
       # desc = row["desc"]
       # bugfix = row["label"]
    history=[]
    flag=0
    pred=0
    while flag!=3:
        history=[]
        history.append({"role":"user", "content":fewshot_prompt_string+"\n"+content+"\nPlease answer yes or no. Do not provide any more information. DO NOT EXPLAIN. Provide answer in this format {\"ans\":\"<Answer>\"}"})
        result, history = llm.run(history)
        print(result)
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
def cot_prompting(llm, content, desc, bugfix):
    fewshot_prompt_string = "Below is a hunk from a patcg fixing a software vulnerability. Not all hunks in the patch are actually relevant to fixing the vulnerability. Please provide a summary of the changes that were implemented within the hunk. FInally answer with yes or no whetehr it is relevant to fixing a vulnerability. Provide your response in json format: {\"summary\":\"<Summary>\",\"ans\":\"<Answer>\"}"
    rows = []
    header = ["content","label", "pred"]
    #for index, row in thing.iterrows():
        #content = row["content"]
       # desc = row["desc"]
       # bugfix = row["label"]
    history=[]
    history.append({"role":"user", "content":fewshot_prompt_string+"\nInput:\n"+content})
    flag=0
    pred=0
    while flag!=3:
        history=[]
        history.append({"role":"user", "content":fewshot_prompt_string+"\n"+content})
        result, history = llm.run(history)
        try:
            result = re.findall(r'\{[^{}]*\}', result)[0]
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
 


 

        

