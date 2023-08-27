import openai, os

openai.api_key = os.environ.get('OPEN_AI_KEY')

def ask_gpt3(chat_history, system_message=None, temperature=None, top_p=None):
    messages = []
    
    # If there's a system message, prepend it to the list
    if system_message:
        messages.append({"role": "system", "content": system_message})
    
    # Extend with the chat history
    messages.extend(chat_history)
    
    payload = {
        "model": "gpt-3.5-turbo",  # Or make the model dynamic based on config
        "messages": messages,
        "max_tokens": 1500
    }
    
    if temperature:
        payload["temperature"] = temperature
    if top_p:
        payload["top_p"] = top_p
    
    response = openai.ChatCompletion.create(**payload)
    return response.choices[0].message.content.strip()


