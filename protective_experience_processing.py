import pandas as pd
import re
import json

df = pd.read_csv('data/protective_experience/protective_experience.csv')  # 파일명에 맞게 수정하세요

speaker_map = {
    "Lily": "user",
    "White Rabbit": "assistant"
}

pattern = r"^\**\s*([A-Za-z ]+)\s*\(speaking\)\s*(.*)$"

jsonl_lines = []

for idx, row in df.iterrows():
    dialogue_text = row['Dialogue']
    lines = dialogue_text.strip().split('\n')
    messages = [{"role": "system", "content": "I want you to act like White Rabbit from Alice's Adventures in Wonderland."}]
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            speaker = match.group(1).strip()
            text = match.group(2).strip()
            if speaker in speaker_map:
                role = speaker_map[speaker]
                messages.append({"role": role, "content": text})
    if len(messages) > 1:
        jsonl_line = json.dumps({"messages": messages}, ensure_ascii=False)
        jsonl_lines.append(jsonl_line)

with open('data/finetuning/fine_tune_data.jsonl', 'w', encoding='utf-8') as f:
    for line in jsonl_lines:
        f.write(line + '\n')

