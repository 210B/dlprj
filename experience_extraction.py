from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

with open("prompts/experience_extraction_baseprompt.txt", "r", encoding="utf-8") as f:
    base_prompt = f.read()

with open("prompts/White Rabbit.txt", "r", encoding="utf-8") as f:
    summary_prompt = f.read()

all_experience = []

full_prompt = f"Context:\n\"\"\"\n{summary_prompt.strip()}\n\"\"\"{base_prompt.strip()}\n\n"
# 프롬프트 요청
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "user", "content": full_prompt}
    ]
    #,n=3
)

for j, choice in enumerate(response.choices):
    content = choice.message.content.strip()
    print(f"\n--- Result {j+1} ---\n{content}\n")

# 최종 JSONL 파일 저장
output_path = "data/experience_extraction/experience.jsonl"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    for experience in all_experience:
        json_line = json.dumps(experience, ensure_ascii=False)
        f.write(json_line + "\n")