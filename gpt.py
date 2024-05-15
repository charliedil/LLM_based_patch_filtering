import html
import requests
import time
import api_keys
class gpt:
    def __init__(self):
        self.url = "https://api.openai.com/v1/chat/completions"
    def run(self,history):
    
        headers={"Content-Type": "application/json", "Authorization": "Bearer "+ api_keys.get_gpt_key()}
        data = {
            "model":"gpt-4",
            "messages":history
            # all possible request body params here: https://platform.openai.com/docs/api-reference/chat/create
        }
        response = requests.post(self.url, headers=headers,json=data, verify=False)
        print(response)
        time.sleep(1)
        assistant_message = response.json()['choices'][0]['message']['content']
        history.append({"role":"assistant", "content":assistant_message})
        print(assistant_message, history)
        return assistant_message, history
