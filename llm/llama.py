import html
import requests

class llama:
    def __init__(self,url):
        self.url = url
    def run(self,history):
    
        headers={"Content-Type": "application/json"}
        data = {
            "mode":"instruct",#you can also do "chat". I prefer instruct, it's more formal. If you do chat, system messages do not work for some reason
            "character":"Example",
            "messages":history,
            "temperature":0
            # all possible request body params here: https://platform.openai.com/docs/api-reference/chat/create
        }
        response = requests.post(self.url, headers=headers,json=data, verify=False)
        assistant_message = response.json()['choices'][0]['message']['content']
        history.append({"role":"assistant", "content":assistant_message})
        return assistant_message, history

