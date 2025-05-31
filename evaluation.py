from openai import OpenAI
import json
import csv
import os
import re
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# List of evaluation file paths
eval_file_paths = [
    ("Baseline", "data/eval/baseline.jsonl"),
    ("Ours", "data/eval/ours.jsonl")
]

# Loop through each dataset
for dataset_name, eval_file_path in eval_file_paths:
    print(f"=== Evaluating Dataset: {dataset_name} ===\n")
    with open(eval_file_path, "r", encoding="utf-8") as f:
        eval_data = [json.loads(line) for line in f]

    # Initialize total scores
    char_total = 0
    logic_total = 0
    world_total = 0

    # Evaluate each sample
    for i, item in enumerate(eval_data, start=1):
        # Convert the conversation into a readable string
        conversation = ""
        for msg in item["messages"]:
            role = msg["role"].capitalize()
            content = msg["content"]
            conversation += f"{role}: {content}\n"

        # Evaluate each category
        for category, prompt_intro in [
            ("Character Consistency", """
Please evaluate the following conversation focusing ONLY on **Character Consistency (0–5 points)**:
- Does the assistant’s response align with the character’s established voice, tone, and personality?
- Does the assistant’s response remain true to the character’s known traits, such as their typical behavior, emotions, and motivations?
- Does the assistant’s response avoid adopting traits or tones that would be out of character (e.g. being overly calm, logical, or inventive if that’s not typical)?
"""),
            ("Logical Consistency", """
Please evaluate the following conversation focusing ONLY on **Logical Consistency (0–5 points)**:
- Is the assistant’s response internally consistent with the character’s established traits, motivations, and situation?
- Does the assistant’s response make sense given its own abilities, limitations, and the context of the world (e.g. the assistant is known for always being late but offers time management tips)?
- Are there contradictions within the assistant’s own statements?
"""),
            ("World Consistency", """
Please evaluate the following conversation focusing ONLY on **World Consistency (0–5 points)**:
- Does the response strictly adhere to the known rules, setting, and lore of Wonderland?
- Does it avoid introducing modern technology (e.g., smartphones) or real-world logic that contradicts Wonderland’s whimsical and fantastical nature?
""")
        ]:
            evaluation_prompt = f"""
You are an expert language model evaluator.

{prompt_intro}

Use the following scoring guide:
- 5: Fully consistent with the character’s established voice, tone, and personality (or logical or world consistency).
- 3: Mostly consistent, with minor deviations.
- 0: Major inconsistencies that clearly contradict the character’s voice, tone, or setting.

Provide a concise explanation for the score and then provide the total score (maximum 5 points).

Here is the conversation to evaluate:
-------------------------------
{conversation}
-------------------------------
Please begin your evaluation.
"""

            # Call the model to evaluate the conversation
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Or your fine-tuned model ID
                messages=[
                    {"role": "system", "content": "You are a helpful and precise evaluation assistant."},
                    {"role": "user", "content": evaluation_prompt}
                ]
            )

            # Get the response content
            evaluation_response = completion.choices[0].message.content

            # Print the evaluation results
            print(f"--- {category} Evaluation Result for {dataset_name} Sample {i} ---")
            print(evaluation_response)

            # Extract score using regex
            score_match = re.search(r"(\d+)", evaluation_response)
            score = int(score_match.group(1)) if score_match else 0

            # Add score to the correct category total
            if category == "Character Consistency":
                char_total += score
            elif category == "Logical Consistency":
                logic_total += score
            elif category == "World Consistency":
                world_total += score

            print("\n--- Score Summary ---")
            print(f"{category} Score: {score} / 5")
            print("\n\n")

    # Calculate total score
    overall_total = char_total + logic_total + world_total

    # Print total scores for the dataset
    print(f"=== Total Scores for {dataset_name} ===")
    print(f"Character Consistency Total: {char_total} / 75")
    print(f"Logical Consistency Total: {logic_total} / 75")
    print(f"World Consistency Total: {world_total} / 75")
    print(f"Overall Total Score: {overall_total} / 225")
    print("\n\n")