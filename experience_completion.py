from openai import OpenAI
import json
import os
import csv
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

with open("prompts/experience_completion.txt", "r", encoding="utf-8") as f:
    base_prompt = f.read().strip()

all_experience = []

csv_path = "data/experience_extraction/experience.csv"

with open(csv_path, "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        location = row["Location"].strip()
        background = row["Status"].strip()

        full_prompt = (
            f"The setting is provided only for your reference and must NOT be included in your answer.\n\n"
            f"- Location: {location}\n"
            f"- Status: {background}\n\n"
            f"{base_prompt}\n\n"
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )

        content = response.choices[0].message.content.strip()
        content = content.replace('\n\n', '\n')
        print(f"\n--- Location: {location} ---\n{content}\n")

        all_experience.append({
            "Location": location,
            "Status": background,
            "Dialogue": content
        })


output_path = "data/experience_completion/complete_experience.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Location", "Status", "Dialogue"])  # 헤더

    for experience in all_experience:
        writer.writerow([
            experience["Location"],
            experience["Status"],
            experience["Dialogue"]
        ])