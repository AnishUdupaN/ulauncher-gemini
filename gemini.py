import os
import google.generativeai as genai


def ask_gemini(api_key,prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-001')
    chat_sessions = {}
    SYSTEM_PROMPT = "Always tend answer in words instead of sentences. Always give Concise, Clear, Short and Precise Answers. The maximum length of an answer shall be 40 words. do not give more than that even if the user requests. "
    chat = model.start_chat(history=[
        {'role': 'user', 'parts': [SYSTEM_PROMPT]},
        {'role': 'model', 'parts': ["Okay, I understand. I'm ready to help."]}
    ])
    response = chat.send_message(prompt)
    return response.text


if __name__=="__main__":
    response = ask_gemini("API_KEY","How are you??")
    print(response)