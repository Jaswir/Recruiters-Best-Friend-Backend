from openai import OpenAI
import requests
from os import environ

client = OpenAI(api_key=environ.get("OPEN_AI_KEY"))

prompt = "Hi"

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": """You are an interview process assistant for Gitlab. """,
        },
        {"role": "user", "content": prompt},
    ],
)

result = response.choices[0].message.content
print(result)