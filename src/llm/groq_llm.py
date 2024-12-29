# Placeholder for Groq LLM API calls
import os
from groq import Groq

def generate_response(user_text, model_name, history, system_prompt, groq_api_key):
    """Sends the prompt to Groq's LLM API and returns the response."""
    try:
        client = Groq(api_key=groq_api_key)
        messages = [
            { "role": "system", "content": system_prompt, }
      ]
        for message in history:
            if message.type == "human":
                messages.append({"role":"user", "content": message.content})
            elif message.type == "ai":
                messages.append({"role":"assistant", "content": message.content})
        messages.append({"role":"user", "content": user_text})

        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model_name,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

def get_available_models():
    """Returns a list of available Groq LLM models."""
    # Placeholder for implementation
    return ["llama3-8b-8192", "llama3-70b-8192", "llama3.1-8b-8192", "llama3.1-70b-8192", "llama3.2-8b-8192", "llama3.2-70b-8192", "llama3.3-8b-8192", "llama3.3-70b-8192" ]