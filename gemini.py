import os
import google.generativeai as genai
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-001')

chat_sessions = {}
SYSTEM_PROMPT = "You are a helpful assistant that answers concisely and clearly.Always give the answers Short and Sweet"


def ask_gemini(prompt):
    chat = model.start_chat(history=[
        {'role': 'user', 'parts': [SYSTEM_PROMPT]},
        {'role': 'model', 'parts': ["Okay, I understand. I'm ready to help."]}
    ])
    response = chat.send_message(prompt)
    return response.text


if __name__=="__main__":
    response = ask_gemini("How are you??")
    print(response)