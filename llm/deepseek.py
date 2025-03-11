import html
import requests

class deepseek:
    def __init__(self,url):
        self.url = url
    def run(self,history):
    
        headers={"Content-Type": "application/json"}
        data = {
            "model":"deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
            "prompt":"\n".join([v["content"] for v in history]),
            "temperature":0,
            "max_tokens":1024
            # all possible request body params here: https://platform.openai.com/docs/api-reference/chat/create
        }
        response = requests.post(self.url, headers=headers,json=data, verify=False)
        print(response.json())
        assistant_message = response.json()['choices'][0]['text']
        history.append({"role":"assistant", "content":assistant_message})
        return assistant_message, history

