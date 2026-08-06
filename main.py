from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

model = init_chat_model(
    model="gemini-3-flash-preview",
    model_provider="google-genai", 
    api_key=api_key)

result = model.invoke("What colour is an orange?")
reply = result.content[0]["text"]
print(reply)