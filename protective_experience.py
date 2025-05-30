from openai import OpenAI
import json
import os
import csv
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

with open("prompts/protective_experience.txt", "r", encoding="utf-8") as f:
    base_prompt = f.read()

with open("prompts/White Rabbit.txt", "r", encoding="utf-8") as f:
    summary_prompt = f.read()

all_experience = []

full_prompt = f"Context:\n\"\"\"\n{summary_prompt.strip()}\n\"\"\"{base_prompt.strip()}\n\n"

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": full_prompt}
    ],
    n=3
)

# 응답 처리
for j, choice in enumerate(response.choices):
    content = choice.message.content.strip()
    print(f"\n--- Result {j+1} ---\n{content}\n")

    # 그냥 전체 텍스트를 Dialogue로 저장
    all_experience.append({
        "Dialogue": content
    })

# CSV 저장
output_path = "data/protective_experience/experience.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Dialogue"])

    for experience in all_experience:
        dialogue = experience["Dialogue"]
        writer.writerow([dialogue])