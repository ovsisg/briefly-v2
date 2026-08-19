import requests
import os
from dotenv import load_dotenv
from send_email import send_email
from langchain.chat_models import init_chat_model


load_dotenv()

news_api_key = os.getenv("NEWS_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

url = (
    "https://newsapi.org/v2/top-headlines?"
    "category=business&"
    "language=en&"
    "pageSize=8&"
    "sortBy=publishedAt&apiKey=" + news_api_key
)

request = requests.get(url)
content = request.json()
articles = content["articles"]

model = init_chat_model(
    model="gemini-3-flash-preview",
    model_provider="google-genai", 
    api_key=google_api_key)

prompt = f"""
    You're a business news summariser.
    Write a short paragraph analysing these news articles.
    Focus on the most important stories and explain why they matter and how they could affect businesses, markets, or consumers.
    Mention key companies, industries, or trends where relevant.
    Do not add information that is not in the articles.
    Do not use Markdown formatting.
    Here are the news articles:
    {articles}
"""

result = model.invoke(prompt)
reply = result.content[0]["text"]
reply = reply.replace("**", "")

print(reply)

body = "Subject: Latest Business News\n\n" + reply + "\n\n"

body = body.encode("utf-8")
send_email(body)