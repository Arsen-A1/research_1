import json
import os
import re

DATA_FILE = "data/questions_multilingual.json"
OUTPUT_FILE = "results/responses/jais-30b_responses.json"
RAW_DIR = "results/responses/manual_raw"

os.makedirs(RAW_DIR, exist_ok=True)

with open(DATA_FILE, "r") as f:
    questions = json.load(f)

# Structure: {"question_id": ..., "language": ..., "answer": ...}
responses = []

for lang in ["en", "ru", "zh", "kz"]:
    raw_path = os.path.join(RAW_DIR, f"jais_{lang}.txt")
    if not os.path.exists(raw_path):
        print(f"Skipping {lang} (file not found: {raw_path})")
        continue

    with open(raw_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse Q<id>: Answer or Q<id>. Answer
    # Matches:
    # Q1: Answer text...
    # or
    # Q1:
    # Answer text...
    # or
    # 1. Answer text...
    pattern = re.compile(r"(?:Q)?(\d+)[:\.]\s*(.*)", re.MULTILINE)
    
    # Split content into blocks based on "Q<number>:" or similar pattern
    # The regex above is good for single-line, but for multi-line we need to be more robust
    # Let's iterate line by line to build the mapping
    
    answer_map = {}
    current_qid = None
    current_answer_lines = []
    
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for new question start
        match = re.match(r"^(?:Q)?(\d+)[:\.]\s*(.*)", line)
        if match:
            # Save previous question if exists
            if current_qid is not None:
                answer_map[current_qid] = "\n".join(current_answer_lines).strip()
            
            # Start new question
            current_qid = int(match.group(1))
            current_answer_lines = []
            if match.group(2):
                current_answer_lines.append(match.group(2))
        elif current_qid is not None:
            # Continue current answer
            # Skip lines that look like "A:" or "Answer:"
            if re.match(r"^(?:A|Answer)[:\.]\s*", line):
                 line = re.sub(r"^(?:A|Answer)[:\.]\s*", "", line)
            current_answer_lines.append(line)
            
    # Save the last question
    if current_qid is not None:
        answer_map[current_qid] = "\n".join(current_answer_lines).strip()

    print(f"Found {len(answer_map)} answers for {lang}")
    
    for q in questions:
        qid = q["id"]
        answer = answer_map.get(qid)
        if answer:
            responses.append({
                "question_id": qid,
                "category": q["category"],
                "language": lang,
                "question": q[lang],
                "answer": answer,
                "usage": {},
                "latency_seconds": 0,
                "error": None
            })

# Save JSON
output_data = {
    "model": "Jais 30B (MBZUAI)",
    "model_id": "jais-30b-chat",
    "provider": "manual",
    "responses": responses
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"Saved {len(responses)} responses to {OUTPUT_FILE}")
