#!/usr/bin/env python3
"""
Semantic Similarity Analysis
==============================
Computes cross-lingual semantic similarity between LLM responses
using multilingual sentence-transformers.

Uses: paraphrase-multilingual-MiniLM-L12-v2 (supports 50+ languages)

Usage:
    python scripts/similarity_analysis.py
    python scripts/similarity_analysis.py --models llama3-8b
"""

import json
import argparse
import itertools
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
RESPONSES_DIR = ROOT_DIR / "results" / "responses"
OUTPUT_CSV = ROOT_DIR / "results" / "similarity_scores.csv"
INTERESTING_OUT = ROOT_DIR / "results" / "interesting_cases.md"

LANGUAGES = ["en", "ru", "zh", "kz"]
LANG_NAMES = {"en": "English", "ru": "Russian", "zh": "Chinese", "kz": "Kazakh"}
LANG_PAIRS = list(itertools.combinations(LANGUAGES, 2))

# Multilingual model — supports EN, RU, ZH and partially KZ
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def load_model():
    """Load the multilingual sentence-transformer model."""
    from sentence_transformers import SentenceTransformer
    print(f"  Loading model: {MODEL_NAME}")
    print(f"  (First run downloads ~500MB, subsequent runs use cache)")
    model = SentenceTransformer(MODEL_NAME)
    return model


def compute_cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    dot = np.dot(vec_a, vec_b)
    norm = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if norm == 0:
        return 0.0
    return float(dot / norm)


def discover_models() -> list[str]:
    """Find all available response files."""
    if not RESPONSES_DIR.exists():
        return []
    models = []
    for path in RESPONSES_DIR.glob("*_responses.json"):
        model_key = path.stem.replace("_responses", "")
        models.append(model_key)
    return sorted(models)


def load_responses(model_key: str) -> dict:
    """Load responses and organize by (question_id, language)."""
    path = RESPONSES_DIR / f"{model_key}_responses.json"
    if not path.exists():
        return {}, {}

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    lookup = {}
    questions = {}
    for entry in data.get("responses", []):
        if entry.get("error") or not entry.get("answer"):
            continue
        key = (entry["question_id"], entry["language"])
        lookup[key] = entry["answer"]
        questions[entry["question_id"]] = {
            "category": entry["category"],
            "question": entry.get("question", ""),
        }

    return lookup, questions


def run_similarity_analysis(model_keys: list[str] | None = None):
    """Run semantic similarity analysis across language pairs."""
    if not model_keys:
        model_keys = discover_models()

    if not model_keys:
        print("❌ No response files found. Run query_llms.py first.")
        return

    print(f"\n{'='*60}")
    print(f"  Semantic Similarity Analysis")
    print(f"{'='*60}")
    print(f"  Model: {MODEL_NAME}")
    print(f"  Language pairs: {len(LANG_PAIRS)}")
    print(f"{'='*60}\n")

    model = load_model()
    all_results = []
    all_interesting = []

    for model_key in model_keys:
        responses, questions = load_responses(model_key)
        if not responses:
            print(f"  ⚠️  No responses for: {model_key}")
            continue

        print(f"\n  🔍 Analyzing: {model_key}")

        # Get all unique question IDs
        question_ids = sorted(set(qid for (qid, _) in responses.keys()))

        # Encode all responses
        print(f"  Encoding {len(responses)} responses...")
        all_texts = []
        all_keys = []
        for key, text in responses.items():
            all_texts.append(text)
            all_keys.append(key)

        embeddings = model.encode(all_texts, show_progress_bar=True, batch_size=32)
        embedding_lookup = {key: emb for key, emb in zip(all_keys, embeddings)}

        # Compute pairwise similarity
        for qid in tqdm(question_ids, desc=f"  Computing similarity"):
            question_info = questions.get(qid, {})

            for lang_a, lang_b in LANG_PAIRS:
                key_a = (qid, lang_a)
                key_b = (qid, lang_b)

                if key_a not in embedding_lookup or key_b not in embedding_lookup:
                    continue

                sim = compute_cosine_similarity(
                    embedding_lookup[key_a], embedding_lookup[key_b]
                )

                result = {
                    "model": model_key,
                    "question_id": qid,
                    "category": question_info.get("category", ""),
                    "lang_pair": f"{lang_a}-{lang_b}",
                    "lang_a": lang_a,
                    "lang_b": lang_b,
                    "similarity": round(sim, 4),
                }
                all_results.append(result)

                # Track interesting cases (low similarity = high divergence)
                if sim < 0.75:
                    all_interesting.append({
                        **result,
                        "question": question_info.get("question", ""),
                        "answer_a": responses.get(key_a, "")[:300],
                        "answer_b": responses.get(key_b, "")[:300],
                    })

    if not all_results:
        print("\n❌ No valid response pairs found for similarity analysis.")
        return

    # Save results
    df = pd.DataFrame(all_results)
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n  📁 Similarity scores saved to: {OUTPUT_CSV}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"  Similarity Summary")
    print(f"{'='*60}\n")

    for model_key in df["model"].unique():
        model_df = df[df["model"] == model_key]
        print(f"  🤖 {model_key}")

        # Average similarity per language pair
        pair_stats = model_df.groupby("lang_pair")["similarity"].agg(
            ["mean", "std", "min"]
        ).round(4)

        print(f"\n  {'Language Pair':<15} {'Mean Sim':>10} {'Std':>10} {'Min':>10}")
        print(f"  {'─'*45}")
        for pair, row in pair_stats.iterrows():
            print(f"  {pair:<15} {row['mean']:>10.4f} {row['std']:>10.4f} "
                  f"{row['min']:>10.4f}")

        # Average similarity per category
        cat_stats = model_df.groupby("category")["similarity"].agg(
            ["mean", "std"]
        ).round(4)

        print(f"\n  {'Category':<15} {'Mean Sim':>10} {'Std':>10}")
        print(f"  {'─'*35}")
        for cat, row in cat_stats.iterrows():
            print(f"  {cat:<15} {row['mean']:>10.4f} {row['std']:>10.4f}")

    # Generate interesting cases report
    if all_interesting:
        _write_interesting_cases(all_interesting, df)

    print(f"\n✅ Similarity analysis complete!\n")


def _write_interesting_cases(cases: list[dict], full_df: pd.DataFrame):
    """Write the interesting divergent cases to markdown."""
    # Sort by similarity (most divergent first)
    cases.sort(key=lambda x: x["similarity"])
    top_cases = cases[:15]

    lines = [
        "# 🔍 Interesting Cross-Lingual Divergence Cases\n",
        "These cases show the most significant semantic divergence between",
        "LLM responses across different languages. A lower similarity score",
        "indicates greater divergence in meaning or framing.\n",
        "**Threshold**: similarity < 0.75 (out of 1.0)\n",
        f"**Total divergent cases found**: {len(cases)}\n",
        "---\n",
    ]

    for i, case in enumerate(top_cases, 1):
        lang_a_name = LANG_NAMES.get(case["lang_a"], case["lang_a"])
        lang_b_name = LANG_NAMES.get(case["lang_b"], case["lang_b"])

        lines.append(f"## Case {i}: Q{case['question_id']} "
                     f"({case['category']}) — {case['lang_pair']}")
        lines.append(f"**Similarity Score**: {case['similarity']:.4f}")
        lines.append(f"**Model**: {case['model']}\n")
        lines.append(f"### Question ({lang_a_name})")
        lines.append(f"> {case['question']}\n")
        lines.append(f"### Response in {lang_a_name}")
        lines.append(f"```\n{case['answer_a']}\n```\n")
        lines.append(f"### Response in {lang_b_name}")
        lines.append(f"```\n{case['answer_b']}\n```\n")

        # Analysis
        lines.append("### Analysis")
        if case["similarity"] < 0.5:
            lines.append("⚠️ **High divergence** — the model provides substantially "
                        "different answers depending on language.")
        elif case["similarity"] < 0.65:
            lines.append("🟡 **Moderate divergence** — notable differences in framing, "
                        "detail, or perspective.")
        else:
            lines.append("🟢 **Mild divergence** — subtle but detectable differences.")
        lines.append("")
        lines.append("---\n")

    # Summary statistics
    lines.append("## Summary Statistics\n")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total divergent cases (sim < 0.75) | {len(cases)} |")
    lines.append(f"| High divergence cases (sim < 0.50) | "
                f"{sum(1 for c in cases if c['similarity'] < 0.5)} |")
    lines.append(f"| Most divergent language pair | "
                f"{min(cases, key=lambda x: x['similarity'])['lang_pair']} |")

    # Category breakdown
    from collections import Counter
    cat_counts = Counter(c["category"] for c in cases)
    lines.append(f"\n### Divergent Cases by Category\n")
    lines.append(f"| Category | Count |")
    lines.append(f"|----------|-------|")
    for cat in ["factual", "opinion", "commonsense"]:
        lines.append(f"| {cat} | {cat_counts.get(cat, 0)} |")

    INTERESTING_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(INTERESTING_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  📁 Interesting cases saved to: {INTERESTING_OUT}")


def main():
    parser = argparse.ArgumentParser(
        description="Compute semantic similarity across languages"
    )
    parser.add_argument(
        "--models", nargs="+", default=None,
        help="Model keys to analyze (default: all available)",
    )
    args = parser.parse_args()
    run_similarity_analysis(args.models)


if __name__ == "__main__":
    main()
