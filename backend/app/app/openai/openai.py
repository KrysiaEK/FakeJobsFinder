import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def request(prompt, message = None) -> dict:
    messages = [
        {'role': 'system', 'content': prompt},
    ]
    if message is not None:
        messages.append({'role': 'user', 'content': message})
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = messages,
        temperature = 0
    )
    text = response['choices'][0]['message']["content"]
    try:
        return json.loads(text)
    except:
        brace_count = 0
        closing_brace_index = -1
        for i, char in enumerate(text):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    closing_brace_index = i
                    break
        if closing_brace_index < 1:
            print("OpenAI returned:", text)
            raise
        return json.loads(text[:closing_brace_index+1])
