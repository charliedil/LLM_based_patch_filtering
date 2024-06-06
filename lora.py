import html
import requests
import re
class lora:
    def __init__(self,url):
        self.url = url
    def run(self,history):
        prompt = ""
        all_messages = [h["content"] for h in history]
        for message in all_messages:
            prompt+=message

        response = requests.post(self.url, json={"prompt":prompt})
        print(response.status_code)
        assistant_message = response.json()['output']
        assistant_message = assistant_message.split("### Response:\n")[1]
        history.append({"role":"assistant", "content":assistant_message})
        return assistant_message, history

