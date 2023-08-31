import openai, os

openai.api_key = os.environ.get('OPEN_AI_KEY')

def ask_gpt3(chat_history, model="gpt-3.5-turbo", system_message=None, temperature=None, top_p=None):
    messages = []
    
    # If there's a system message, prepend it to the list
    if system_message:
        messages.append({"role": "system", "content": system_message})
    
    # Extend with the chat history
    messages.extend(chat_history)
    
    payload = {
        "model": model,  # Or make the model dynamic based on config
        "messages": messages,
        "max_tokens": 1500
    }
    
    if temperature:
        payload["temperature"] = temperature
    if top_p:
        payload["top_p"] = top_p
    
    response = openai.ChatCompletion.create(**payload)
    return response.choices[0].message.content.strip()

def summarize_with_gpt3(chat_history, model="gpt-3.5-turbo", system_message="Summarize the following conversation:", temperature=0.7, top_p=0.9):
    """
    Gets a summary of a given chat history using OpenAI.
    """
    # Convert the chat history text into a list of messages
    messages_list = [{"role": "user", "messages": message} for message in chat_history.split("\n") if message]
    
    # Get a response from OpenAI
    response = ask_gpt3(messages_list, model, system_message, temperature, top_p)
    
    return response


