#!/usr/bin/env python3
"""
Visualization Module
=====================
Generates publication-quality charts for the cross-lingual LLM bias research.

Charts:
1. Similarity heatmap per model (language × language)
2. Response length comparison across languages
3. Confidence score by language and category
4. Disclaimer frequency comparison
5. Top divergent questions visualization

Usage:
    python scripts/visualize.py
    python scripts/visualize.py --models llama3-8b
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

# Use non-interactive backend for server environments
matplotlib.use("Agg")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT_DIR / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
ANALYSIS_CSV = RESULTS_DIR / "analysis_summary.csv"
SIMILARITY_CSV = RESULTS_DIR / "similarity_scores.csv"

LANGUAGES = ["en", "ru", "zh", "kz"]
LANG_NAMES = {"en": "English", "ru": "Russian", "zh": "Chinese", "kz": "Kazakh"}

# Research paper color palette
COLORS = {
    "en": "#2196F3",  # Blue
    "ru": "#F44336",  # Red
    "zh": "#FF9800",  # Orange
    "kz": "#4CAF50",  # Green
}
CATEGORY_COLORS = {
    "factual": "#42A5F5",
    "opinion": "#EF5350",
    "commonsense": "#66BB6A",
}


def setup_style():
    """Configure matplotlib for publication-quality charts."""
    plt.rcParams.update({
        "figure.dpi": 150,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.grid": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.alpha": 0.3,
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "legend.fontsize": 10,
        "figure.titlesize": 14,
    })
    sns.set_palette("husl")


def plot_similarity_heatmap(sim_df: pd.DataFrame, model_key: str):
    """Plot language-pair similarity as a heatmap."""
    # Build similarity matrix
    matrix = pd.DataFrame(
        np.ones((len(LANGUAGES), len(LANGUAGES))),
        index=[LANG_NAMES[l] for l in LANGUAGES],
        columns=[LANG_NAMES[l] for l in LANGUAGES],
    )

    model_sim = sim_df[sim_df["model"] == model_key]
    for _, row in model_sim.groupby("lang_pair")["similarity"].mean().items():
        pass

    for pair, sim in model_sim.groupby("lang_pair")["similarity"].mean().items():
        lang_a, lang_b = pair.split("-")
        name_a, name_b = LANG_NAMES[lang_a], LANG_NAMES[lang_b]
        matrix.loc[name_a, name_b] = sim
        matrix.loc[name_b, name_a] = sim

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        matrix,
        annot=True,
        fmt=".3f",
        cmap="RdYlGn",
        vmin=0.4,
        vmax=1.0,
        square=True,
        linewidths=2,
        linecolor="white",
        ax=ax,
        cbar_kws={"label": "Cosine Similarity", "shrink": 0.8},
    )
    ax.set_title(f"Cross-Lingual Semantic Similarity — {model_key}", fontweight="bold")
    plt.tight_layout()

    path = FIGURES_DIR / f"similarity_heatmap_{model_key}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  📊 Saved: {path.name}")


def plot_response_length(analysis_df: pd.DataFrame, model_key: str):
    """Plot response length comparison across languages."""
    model_df = analysis_df[analysis_df["model"] == model_key]
    if model_df.empty:
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Box plot by language
    data_by_lang = [
        model_df[model_df["language"] == lang]["answer_length_words"].values
        for lang in LANGUAGES
    ]
    bp = axes[0].boxplot(
        data_by_lang,
        labels=[LANG_NAMES[l] for l in LANGUAGES],
        patch_artist=True,
        medianprops={"color": "black", "linewidth": 2},
    )
    for patch, lang in zip(bp["boxes"], LANGUAGES):
        patch.set_facecolor(COLORS[lang])
        patch.set_alpha(0.7)

    axes[0].set_ylabel("Response Length (words)")
    axes[0].set_title("Response Length by Language")

    # Grouped bar chart by category × language
    categories = ["factual", "opinion", "commonsense"]
    x = np.arange(len(categories))
    width = 0.2

    for i, lang in enumerate(LANGUAGES):
        means = []
        for cat in categories:
            cat_lang = model_df[(model_df["category"] == cat) &
                               (model_df["language"] == lang)]
            means.append(cat_lang["answer_length_words"].mean()
                        if not cat_lang.empty else 0)
        axes[1].bar(x + i * width, means, width,
                   label=LANG_NAMES[lang], color=COLORS[lang], alpha=0.8)

    axes[1].set_xticks(x + width * 1.5)
    axes[1].set_xticklabels([c.capitalize() for c in categories])
    axes[1].set_ylabel("Avg Response Length (words)")
    axes[1].set_title("Response Length by Category × Language")
    axes[1].legend()

    fig.suptitle(f"Response Length Analysis — {model_key}", fontweight="bold", y=1.02)
    plt.tight_layout()

    path = FIGURES_DIR / f"response_length_{model_key}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  📊 Saved: {path.name}")


def plot_confidence_analysis(analysis_df: pd.DataFrame, model_key: str):
    """Plot confidence scores and disclaimer counts."""
    model_df = analysis_df[analysis_df["model"] == model_key]
    if model_df.empty:
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Confidence by language
    categories = ["factual", "opinion", "commonsense"]
    x = np.arange(len(categories))
    width = 0.2

    for i, lang in enumerate(LANGUAGES):
        means = []
        for cat in categories:
            cat_lang = model_df[(model_df["category"] == cat) &
                               (model_df["language"] == lang)]
            means.append(cat_lang["confidence_score"].mean()
                        if not cat_lang.empty else 0)
        axes[0].bar(x + i * width, means, width,
                   label=LANG_NAMES[lang], color=COLORS[lang], alpha=0.8)

    axes[0].set_xticks(x + width * 1.5)
    axes[0].set_xticklabels([c.capitalize() for c in categories])
    axes[0].set_ylabel("Confidence Score (0-1)")
    axes[0].set_title("Model Confidence by Category × Language")
    axes[0].set_ylim(0, 1)
    axes[0].legend()

    # Disclaimer count by language
    disc_data = model_df.groupby("language")["num_disclaimers"].mean()
    lang_labels = [LANG_NAMES[l] for l in LANGUAGES if l in disc_data.index]
    disc_values = [disc_data[l] for l in LANGUAGES if l in disc_data.index]
    color_list = [COLORS[l] for l in LANGUAGES if l in disc_data.index]

    bars = axes[1].bar(lang_labels, disc_values, color=color_list, alpha=0.8)
    axes[1].set_ylabel("Avg Disclaimers per Response")
    axes[1].set_title("Hedging / Disclaimer Frequency")

    # Add value labels on bars
    for bar, val in zip(bars, disc_values):
        axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{val:.2f}", ha="center", fontsize=10)

    fig.suptitle(f"Confidence & Disclaimer Analysis — {model_key}",
                fontweight="bold", y=1.02)
    plt.tight_layout()

    path = FIGURES_DIR / f"confidence_analysis_{model_key}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  📊 Saved: {path.name}")


def plot_similarity_distribution(sim_df: pd.DataFrame, model_key: str):
    """Plot distribution of similarity scores."""
    model_sim = sim_df[sim_df["model"] == model_key]
    if model_sim.empty:
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Distribution by language pair
    pairs = model_sim["lang_pair"].unique()
    for pair in sorted(pairs):
        pair_data = model_sim[model_sim["lang_pair"] == pair]
        axes[0].hist(pair_data["similarity"], bins=15, alpha=0.5, label=pair)

    axes[0].set_xlabel("Cosine Similarity")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title("Similarity Distribution by Language Pair")
    axes[0].legend()
    axes[0].axvline(x=0.75, color="red", linestyle="--", alpha=0.7,
                    label="Divergence threshold")

    # Distribution by category
    for cat in ["factual", "opinion", "commonsense"]:
        cat_data = model_sim[model_sim["category"] == cat]
        axes[1].hist(cat_data["similarity"], bins=15, alpha=0.5,
                    label=cat.capitalize(), color=CATEGORY_COLORS[cat])

    axes[1].set_xlabel("Cosine Similarity")
    axes[1].set_ylabel("Frequency")
    axes[1].set_title("Similarity Distribution by Category")
    axes[1].legend()
    axes[1].axvline(x=0.75, color="red", linestyle="--", alpha=0.7)

    fig.suptitle(f"Semantic Similarity Distributions — {model_key}",
                fontweight="bold", y=1.02)
    plt.tight_layout()

    path = FIGURES_DIR / f"similarity_distribution_{model_key}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  📊 Saved: {path.name}")


def plot_cross_model_comparison(analysis_df: pd.DataFrame, sim_df: pd.DataFrame):
    """Plot comparison across models (if multiple)."""
    models = analysis_df["model"].unique()
    if len(models) < 2:
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Average response length per model per language
    x = np.arange(len(models))
    width = 0.2
    for i, lang in enumerate(LANGUAGES):
        means = []
        for model_key in models:
            model_lang = analysis_df[(analysis_df["model"] == model_key) &
                                     (analysis_df["language"] == lang)]
            means.append(model_lang["answer_length_words"].mean()
                        if not model_lang.empty else 0)
        axes[0].bar(x + i * width, means, width,
                   label=LANG_NAMES[lang], color=COLORS[lang], alpha=0.8)

    axes[0].set_xticks(x + width * 1.5)
    axes[0].set_xticklabels(models, rotation=30, ha="right")
    axes[0].set_ylabel("Avg Words per Response")
    axes[0].set_title("Response Length: Model × Language")
    axes[0].legend()

    # Average similarity per model
    if not sim_df.empty:
        model_sims = sim_df.groupby("model")["similarity"].mean().reindex(models)
        bars = axes[1].bar(models, model_sims.values,
                          color=sns.color_palette("husl", len(models)), alpha=0.8)
        axes[1].set_ylabel("Avg Cosine Similarity")
        axes[1].set_title("Cross-Lingual Consistency by Model")
        axes[1].set_xticklabels(models, rotation=30, ha="right")
        axes[1].set_ylim(0.5, 1.0)

        for bar, val in zip(bars, model_sims.values):
            if not np.isnan(val):
                axes[1].text(bar.get_x() + bar.get_width() / 2,
                            bar.get_height() + 0.005,
                            f"{val:.3f}", ha="center", fontsize=10)

    fig.suptitle("Cross-Model Comparison", fontweight="bold", y=1.02)
    plt.tight_layout()

    path = FIGURES_DIR / "cross_model_comparison.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  📊 Saved: {path.name}")


def run_visualization(model_keys: list[str] | None = None):
    """Generate all plots."""
    setup_style()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Visualization Pipeline")
    print(f"{'='*60}\n")

    # Load data
    analysis_df = None
    sim_df = None

    if ANALYSIS_CSV.exists():
        analysis_df = pd.read_csv(ANALYSIS_CSV)
        print(f"  Loaded analysis: {len(analysis_df)} rows")
    else:
        print(f"  ⚠️  No analysis data found. Run analyze_responses.py first.")

    if SIMILARITY_CSV.exists():
        sim_df = pd.read_csv(SIMILARITY_CSV)
        print(f"  Loaded similarity: {len(sim_df)} rows")
    else:
        print(f"  ⚠️  No similarity data found. Run similarity_analysis.py first.")

    if analysis_df is None and sim_df is None:
        print("\n❌ No data to visualize.")
        return

    # Determine models
    if model_keys:
        models = model_keys
    else:
        models = set()
        if analysis_df is not None:
            models.update(analysis_df["model"].unique())
        if sim_df is not None:
            models.update(sim_df["model"].unique())
        models = sorted(models)

    print(f"  Models: {', '.join(models)}\n")

    for model_key in models:
        print(f"\n  🎨 Generating plots for: {model_key}")

        if analysis_df is not None:
            plot_response_length(analysis_df, model_key)
            plot_confidence_analysis(analysis_df, model_key)

        if sim_df is not None:
            plot_similarity_heatmap(sim_df, model_key)
            plot_similarity_distribution(sim_df, model_key)

    # Cross-model comparison
    if len(models) > 1 and analysis_df is not None:
        print(f"\n  🎨 Generating cross-model comparison")
        plot_cross_model_comparison(
            analysis_df,
            sim_df if sim_df is not None else pd.DataFrame(),
        )

    print(f"\n✅ All visualizations saved to: {FIGURES_DIR}\n")


def main():
    parser = argparse.ArgumentParser(description="Generate research visualizations")
    parser.add_argument(
        "--models", nargs="+", default=None,
        help="Model keys to visualize (default: all available)",
    )
    args = parser.parse_args()
    run_visualization(args.models)


if __name__ == "__main__":
    main()
