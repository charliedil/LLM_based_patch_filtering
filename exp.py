import pandas as pd
import json
import re
def mod_gen_knowledge_prompting(llm, content, desc):
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

Description: Calling stopSpyStream on TelnetClient sets spyStream to null without regard to whether _spyRead or _spyWrite are being invoked on another thread. \n\nResulting NPE in _spyRead/_spy_Write is caught in TelnetInputStream.run() which goes on to close the stream.\n\nMay be able to fix by taking local copy of spyStream (which ought also to be volatile) in both of _spyRead and _spyWrite. E.g. for _spyRead:\n\n    void _spyRead(int ch)\n    {\n        OutputStream _spyStream = spyStream;\n        \n        if (_spyStream != null)\n        {\n            try\n            {\n                if (ch != '\\r')\n                {\n                    _spyStream.write(ch);\n                    if (ch == '\\n')\n                    {\n                        _spyStream.write('\\r');\n                    }\n                    _spyStream.flush();\n                }\n            }\n            catch (IOException e)\n            {\n                spyStream = null;\n            }\n        }\n    }
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
    for i in range(1):#changed to 1 here for cost savings
        history=[]
        history.append({"role":"system", "content":"Your job is to generate Knowledge for a given Hunk using the Description."})
        history.append({"role":"user", "content":fewshot_prompt_string+"\nDescription: "+desc+"\nHunk:\n"+content+"\nKnowledge:\n"})

        result, history = llm.run(history)
        summaries.append(result)
    max_ans = ""
    max_score = 0
    max_summary = 0
    for i in range(1):#changed tro 1 here for cost savings
        flag = 0
        while(flag!=3):
            history = []
            history.append({"role":"system", "content":"Using the knowledge provided, answer the question given"})
            history.append({"role":"user", "content":"The following knowledge is derived from a code hunk that is part of a larger commit intended to fix the following bug. Code hunks that only contain changes to whitespace, documentation, tests are not bug fixes. Code hunks that perform refactoring or unrelated changes do not qualify as bugfixes. Using the knowledge given, determine if the code hunk contains a fix to the described bug.\nDescription: "+desc+"\nKnowledge: "+summaries[i]+"\n Please respond with \"yes\" or \"no\" and a confidence score on a scale from 0 to 1. Do not provide any more information or explanations. Format your response as follows: {\"ans\":<Answer>, \"conf\":<Confidence Score>}"})
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
def mod_fewshot_prompting(llm, content, desc):
    fewshot_prompt_string = """
The following code hunk is part of a larger commit intended to fix the above bug. Code hunks that only contain changes to whitespace, documentation, tests are not bug fixes. Code hunks that perform refactoring or unrelated changes do not qualify as bugfixes.

Evaluate the code hunk below and determine if it contains a fix to the described bug. Please respond with \"yes\" or \"no\" only. Do not provide any more information or explanations. Format your response as follows: {\"ans\":\"<Answer>\"}


Description: 'I believe the Beider Morse Phonetic Matching algorithm was added in Commons Codec 1.6\n\nThe BMPM algorithm is an EVOLVING algorithm that is currently on version 3.02 though it had been static since version 3.01 dated 19 Dec 2011 (it was first available as opensource as version 1.00 on 6 May 2009).\n\nI can see nothing in the Commons Codec Docs to say which version of BMPM was implemented so I am not sure if the problem with the algorithm as coded in the Codec is simply an old version or whether there are more basic problems with the implementation.\n\nHow do I determine the version of the algorithm that was implemented in the Commons Codec?\n\nHow do we ensure that the algorithm is updated if/when the BMPM algorithm changes?\n\nHow do we ensure that the algorithm as coded in the Commons Codec is accurate and working as expected?'
Hunk:
-        assertEquals(encode(args, false, ""Angelo""), ""AnElO|AnSelO|AngElO|AngzelO|AnkselO|AnzelO"");
+        assertEquals(encode(args, false, ""Angelo""), ""YngYlo|Yngilo|angYlo|angilo|anilo|anxilo|anzilo|ongYlo|ongilo|onilo|onxilo|onzilo"");
{”ans”:”no”}

Description: "My project, which is associated with the Grid, uses limited proxy certificates for digital signature. I.e., the signing application holds a user's permanent certificate, signed by a CA and a proxy certificate signed with the permanent certificate. The application signs a message using the proxy certificate and includes both the proxy and permanent certificates in the message header as a WS-Security direct reference to a BinarySecurityToken. The service has the CA certificate with which the user's permanent certficate was signed. Therefore, to establish trust, the service has to chain back from the proxy to the permanent certificate and then to the CA certificate.\n\nWSSignEnvelope includes both certificates correctly but WSSecurityEngine fails when checking the chain of trust. WSSecurityEngine..processSecurityHeader() only adds one certificate to the results passed back to WSDoAllReceiver; it ignores the intermediate certificate in the chain."
Hunk: 
-     * get a byte array given an array of X509 certificates.
+     * Get a byte array given an array of X509 certificates.
{“ans”:”no”}

Description: Under high load commons-dbcp (or commons-pool) exhibits thread safety issues and begins throwing various exceptions. I don't yet know the cause of the issue but it looks like a connection maybe handed out to multiple threads concurrently. Here's a few examples of the exceptions we are getting:\n\n{noformat}\njvm 1    | Caused by: java.sql.SQLException: Attempted to use PooledConnection after closed() was called.\njvm 1
Hunk:
- * 
+ *
  *      http://www.apache.org/licenses/LICENSE-2.0
- * 
+ *
{“ans”:”no”}

Description: Hello,\nWe are been using Ofbiz with DBCP based implementation.\nOfbiz uses a Head revision of DBCP (package org.apache.commons.dbcp.managed is the same as current TRUNK) and geronimo-transaction-1.0.\n\nWe are having recurrent OutOfMemory which occur on a 2 days basis.\nI analyzed the Heap Dump and I think have found the source of the problem:\nThe Heap Dump shows a Retained Heap of 400Mo by org.apache.commons.dbcp.managed.TransactionRegistry#xaResources field.\n\nAfter analyzing more deeply, the leak seems to come from what is stored in xaResources through\nxaResources.put(connection, xaResource);\n\nValues inside weak Hash map  will never be removed since XAResource holds a STRONG reference on key (connection) through:\norg.apache.commons.dbcp.managed.LocalXAConnectionFactory$LocalXAResource through:\npublic LocalXAResource(Connection localTransaction) {\n            this.connection = localTransaction;\n        }\n\n\nFound in WeakHashMap javadoc:\nImplementation note: The value objects in a WeakHashMap are held by ordinary strong references. >>>>>>>>>>>>>Thus care should be taken to ensure that value objects do not strongly refer to their own keys <<<<<<<<, either directly or indirectly, since that will prevent the keys from being discarded. Note that a value object may refer indirectly to its key via the WeakHashMap itself; that is, a value object may strongly refer to some other key object whose associated value object, in turn, strongly refers to the key of the first value object. One way to deal with this is to wrap values themselves within WeakReferences before inserting, as in: m.put(key, new WeakReference(value)), and then unwrapping upon each get. \n\nPhilippe Mouawad\nhttp://www.ubik-ingenierie.com'
Hunk:
-import javax.transaction.xa.XAResource;
-import javax.transaction.TransactionManager;
-import javax.transaction.Transaction;
-import javax.transaction.SystemException;
-import javax.transaction.Status;
{“ans”:”no”}

Description: Calling stopSpyStream on TelnetClient sets spyStream to null without regard to whether _spyRead or _spyWrite are being invoked on another thread. \n\nResulting NPE in _spyRead/_spy_Write is caught in TelnetInputStream.run() which goes on to close the stream.\n\nMay be able to fix by taking local copy of spyStream (which ought also to be volatile) in both of _spyRead and _spyWrite. E.g. for _spyRead:\n\n    void _spyRead(int ch)\n    {\n        OutputStream _spyStream = spyStream;\n        \n        if (_spyStream != null)\n        {\n            try\n            {\n                if (ch != '\\r')\n                {\n                    _spyStream.write(ch);\n                    if (ch == '\\n')\n                    {\n                        _spyStream.write('\\r');\n                    }\n                    _spyStream.flush();\n                }\n            }\n            catch (IOException e)\n            {\n                spyStream = null;\n            }\n        }\n    }
Hunk:
-                    spyStream.write(ch);
-                    spyStream.flush();
+                    spy.write(ch);
+                    spy.flush();
{“ans”:”no”}

Description:
http://redline-rpm.org/ creates CPIO archives with a non-zero file mode on the trailer. This causes an IllegalArgumentException when reading the file. I've attached a patch and test archive to fix this.
Hunk: 
-        return (this.mode & S_IFMT) == C_ISBLK;
+        return CpioUtil.fileType(mode) == C_ISBLK;
{“ans”:”yes”}

    """
    flag = 0
    pred=0
    while flag!=3:
        history=[]
        history.append({"role":"user", "content":fewshot_prompt_string+"\nDescription: "+desc+"\nHunk:\n"+content})
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
    return pred

def zeroshot_prompting(llm, content, desc):
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
def mod_cot_prompting(llm, content, desc):
    fewshot_prompt_string = """The following code hunk is part of a larger commit intended to fix the above bug. Code hunks that only contain changes to whitespace, documentation, tests are not bug fixes. Code hunks that perform refactoring or unrelated changes do not qualify as bugfixes.

Please provide a summary of the changes that were implemented within the hunk. Based on the summary, answer with yes or no whether it is relevant to fixing a bug. Provide your response in json format: {\"summary\":\"<Summary>\",\"ans\":\"<Answer>\"}
    
    """
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
 

        

