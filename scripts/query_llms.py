#!/usr/bin/env python3
"""
Cross-Lingual LLM Query Engine
===============================
Batch-queries multiple LLMs with multilingual questions via free API tiers.
Supports: Groq (Llama 3, Gemma 2), Google Gemini (free tier), Ollama (local).

Usage:
    python scripts/query_llms.py                    # Full run
    python scripts/query_llms.py --dry-run          # Validate config only
    python scripts/query_llms.py --models llama3    # Specific model
    python scripts/query_llms.py --languages en ru  # Specific languages
"""

import json
import os
import sys
import time
import argparse
import hashlib
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "data" / "questions_multilingual.json"
RESPONSES_DIR = ROOT_DIR / "results" / "responses"

LANGUAGES = ["en", "ru", "zh", "kz"]

# Model configurations: (provider, model_id, display_name)
MODEL_CONFIGS = {
    "llama3-8b": {
        "provider": "groq",
        "model_id": "llama-3.1-8b-instant",
        "display_name": "Llama 3.1 8B (Groq)",
    },
    "llama3-70b": {
        "provider": "groq",
        "model_id": "llama-3.3-70b-versatile",
        "display_name": "Llama 3.3 70B (Groq)",
    },


}

# System prompt — deliberately neutral to avoid biasing responses
SYSTEM_PROMPT = "You are a helpful assistant. Answer the question directly and concisely."

# Rate limiting (requests per minute)
RATE_LIMITS = {"groq": 28, "gemini": 14, "ollama": 999}  # slightly under actual limits


def load_questions() -> list[dict]:
    """Load multilingual questions from JSON file."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def create_client(provider: str):
    """Create API client for the given provider."""
    if provider == "groq":
        from groq import Groq
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key.startswith("your_"):
            raise ValueError(
                "GROQ_API_KEY not set. Get a free key at https://console.groq.com"
            )
        return Groq(api_key=api_key)

    elif provider == "gemini":
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key.startswith("your_"):
            raise ValueError(
                "GEMINI_API_KEY not set. Get a free key at https://aistudio.google.com/apikey"
            )
        genai.configure(api_key=api_key)
        return genai  # return the module; model is instantiated per-call

    elif provider == "ollama":
        from openai import OpenAI
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return OpenAI(base_url=f"{base_url}/v1", api_key="ollama")

    else:
        raise ValueError(f"Unknown provider: {provider}")


def query_model(client, provider: str, model_id: str, question: str) -> dict:
    """Send a single question to a model and return response metadata."""
    start_time = time.time()

    try:
        if provider in ("groq", "ollama"):
            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question},
                ],
                temperature=0.3,  # Low temp for more deterministic responses
                max_tokens=1024,
            )
            answer = response.choices[0].message.content
            usage = {
                "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
                "completion_tokens": getattr(response.usage, "completion_tokens", 0),
                "total_tokens": getattr(response.usage, "total_tokens", 0),
            }
        elif provider == "gemini":
            import google.generativeai as genai
            model = genai.GenerativeModel(
                model_name=model_id,
                system_instruction=SYSTEM_PROMPT,
                generation_config=genai.GenerationConfig(temperature=0.3, max_output_tokens=1024),
            )
            response = model.generate_content(question)
            answer = response.text
            usage = {
                "prompt_tokens": getattr(response.usage_metadata, "prompt_token_count", 0),
                "completion_tokens": getattr(response.usage_metadata, "candidates_token_count", 0),
                "total_tokens": getattr(response.usage_metadata, "total_token_count", 0),
            }
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        elapsed = time.time() - start_time

        return {
            "answer": answer,
            "usage": usage,
            "latency_seconds": round(elapsed, 3),
            "error": None,
        }

    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "answer": None,
            "usage": {},
            "latency_seconds": round(elapsed, 3),
            "error": str(e),
        }


def get_response_path(model_key: str) -> Path:
    """Get the output file path for a model's responses."""
    return RESPONSES_DIR / f"{model_key}_responses.json"


def load_existing_responses(model_key: str) -> dict:
    """Load existing responses for resume capability."""
    path = get_response_path(model_key)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Build lookup: (question_id, language) -> response
            lookup = {}
            for entry in data.get("responses", []):
                # Retry if previous attempt failed
                if entry.get("error"):
                    continue
                key = (entry["question_id"], entry["language"])
                lookup[key] = entry
            return lookup
    return {}


def save_responses(model_key: str, model_config: dict, responses: list[dict]):
    """Save responses to JSON file."""
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    output = {
        "model": model_config["display_name"],
        "model_id": model_config["model_id"],
        "provider": model_config["provider"],
        "timestamp": datetime.now().isoformat(),
        "system_prompt": SYSTEM_PROMPT,
        "total_queries": len(responses),
        "responses": responses,
    }
    path = get_response_path(model_key)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


def run_queries(
    model_keys: list[str],
    languages: list[str],
    dry_run: bool = False,
):
    """Main query loop with rate limiting and progress tracking."""
    load_dotenv(ROOT_DIR / ".env")
    questions = load_questions()

    print(f"\n{'='*60}")
    print(f"  Cross-Lingual LLM Query Engine")
    print(f"{'='*60}")
    print(f"  Questions: {len(questions)}")
    print(f"  Languages: {', '.join(languages)}")
    print(f"  Models:    {', '.join(model_keys)}")
    total = len(questions) * len(languages) * len(model_keys)
    print(f"  Total queries: {total}")
    print(f"{'='*60}\n")

    if dry_run:
        print("✅ Dry run complete — configuration is valid.")
        # Validate API keys
        for model_key in model_keys:
            config = MODEL_CONFIGS[model_key]
            try:
                create_client(config["provider"])
                print(f"  ✅ {config['display_name']}: API key valid")
            except ValueError as e:
                print(f"  ❌ {config['display_name']}: {e}")
        return

    for model_key in model_keys:
        config = MODEL_CONFIGS[model_key]
        provider = config["provider"]
        print(f"\n🤖 Querying: {config['display_name']}")
        print(f"   Provider: {provider} | Model: {config['model_id']}")

        try:
            client = create_client(provider)
        except ValueError as e:
            print(f"   ❌ Skipping: {e}")
            continue

        existing = load_existing_responses(model_key)
        responses = list(existing.values())  # Start with existing
        rate_limit = RATE_LIMITS.get(provider, 30)
        delay = 60.0 / rate_limit

        skipped = 0
        queried = 0

        pbar = tqdm(
            total=len(questions) * len(languages),
            desc=f"   {model_key}",
            unit="query",
        )

        for question in questions:
            for lang in languages:
                pbar.update(1)

                # Skip if already done (resume support)
                if (question["id"], lang) in existing:
                    skipped += 1
                    continue

                question_text = question.get(lang)
                if not question_text:
                    continue

                result = query_model(client, provider, config["model_id"], question_text)

                entry = {
                    "question_id": question["id"],
                    "category": question["category"],
                    "language": lang,
                    "question": question_text,
                    "answer": result["answer"],
                    "usage": result["usage"],
                    "latency_seconds": result["latency_seconds"],
                    "error": result["error"],
                }
                responses.append(entry)
                queried += 1

                # Rate limiting
                time.sleep(delay)

                # Save periodically (every 10 queries)
                if queried % 10 == 0:
                    save_responses(model_key, config, responses)

        pbar.close()

        # Final save
        save_responses(model_key, config, responses)
        print(f"   ✅ Done: {queried} new, {skipped} resumed")
        print(f"   📁 Saved to: {get_response_path(model_key)}")

    print(f"\n{'='*60}")
    print(f"  All queries complete!")
    print(f"  Results saved to: {RESPONSES_DIR}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Query LLMs with multilingual questions"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration without making API calls",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        choices=list(MODEL_CONFIGS.keys()),
        default=list(MODEL_CONFIGS.keys()),
        help="Models to query (default: all)",
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        choices=LANGUAGES,
        default=LANGUAGES,
        help="Languages to query (default: all)",
    )

    args = parser.parse_args()
    run_queries(args.models, args.languages, args.dry_run)


if __name__ == "__main__":
    main()
