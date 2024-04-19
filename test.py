from openai import OpenAI
import requests
from os import environ

client = OpenAI(api_key=environ.get("OPEN_AI_KEY"))

prompt = "Hi"
RawAnswer = "I do not have enough information to answer this question."

input = prompt +"this is the raw answer use it in your response: "+ RawAnswer

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": """You are an interview process assistant for Gitlab, mention this when greeted.
            You role is to answer questions about our hiring processes, working at Gitlab, company culture, values, onboarding and more!""",
        },
        {"role": "user", "content": input},
    ],
)

result = response.choices[0].message.content
print(result)