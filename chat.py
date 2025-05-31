from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
modelId = os.getenv("MODEL_ID")
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model=modelId,
    messages=[
        {"role": "system", "content": "You are White Rabbit of Alice's Adventures in Wonderland."},
        {"role": "user", "content": "Why are you always late?"}
    ]
)

print(response.choices[0].message.content)