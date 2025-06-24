# Utils/Chatbot.py
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv() 

# Load your Groq API key from environment variable
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

def get_bot_response(prompt):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # You can also use: llama3-70b-8192 or mixtral-8x7b-32768
            messages=[
                {"role": "system", "content": "You are a helpful AI medical assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()
# client = OpenAI(api_key="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")

# def get_bot_response(prompt):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",  # or "gpt-4"
#         messages=[
#             {"role": "system", "content": "You are a helpful medical assistant."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.choices[0].message.content
