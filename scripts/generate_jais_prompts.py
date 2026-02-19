import json
import os

DATA_FILE = "data/questions_multilingual.json"
OUTPUT_FILE = "data/jais_prompts_complete.md"

with open(DATA_FILE, "r") as f:
    questions = json.load(f)

with open(OUTPUT_FILE, "w") as f:
    f.write("# Jais Chat Prompts\n\n")
    f.write("Copy each block into Jais Chat (https://jaischat.ai/).\n")
    f.write("Paste the output into a text file named results/responses/jais_raw_<lang>.txt\n\n")
    
    for lang in ["en", "ru", "zh", "kz"]:
        f.write(f"## {lang.upper()} Prompt (Copy This Whole Block)\n\n")
        f.write("```text\n")
        f.write(f"Please answer the following 50 questions in {lang.upper()}. Provide a DETAILED response (2-3 sentences) for each question. Format your answer starting with 'Q<number>: ' followed by the answer. Do not use single words like Yes/No/Neutral.\\n\\n")
        
        for q in questions:
            q_text = q[lang]
            f.write(f"Q{q['id']}: {q_text}\n")
            
        f.write("```\n\n---\n\n")

print(f"Generated {OUTPUT_FILE}")
