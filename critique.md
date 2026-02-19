# Research Critique & Self-Reflection

> *Note for Admissions*: This document outlines my critical analysis of my own work. I believe scientific rigor requires acknowledging limitations honestly.

## 1. Methodology Vulnerabilities

### Sample Size (N=50)
**Weakness**: 50 questions is too small to claim statistical significance for "general" model behavior.
**Impact**: Our findings on "Russian safety bias" could be skewed by just 5-10 specific political questions in our set. 
**Improvement**: A robust evaluation would need N=1000+, likely using an automated dataset like XNLI or creating a larger synthetic benchmark.

### Auto-Metrics Limitations
**Weakness**: Our "Confidence Score" relies on regex keywords (e.g., counting "important to note", "I cannot").
**Impact**: A model might be confident but polite, using "soft" language that our script misinterprets as hedging.
**Improvement**: Use **Logit Analysis**. Accessing the model's internal probability scores for the generated tokens would give a mathematical measure of uncertainty, rather than a linguistic one.

### Translation Bias
**Weakness**: The questions were translated from English.
**Impact**: "TranslationArtifacts" — the Russian/Kazakh questions might "sound translated," which could confuse the model or trigger lower-quality responses not because of the *language* but because of the *phrasing*.
**Improvement**: Use **Native Composition**. Have native speakers write questions directly in the target language to capture true cultural intent.

## 2. Evaluation Validity

**Did we evaluate "Right"?**
We used **Multilingual Embeddings** (`paraphrase-multilingual-MiniLM-L12-v2`) to measure semantic similarity. This is the industry standard for this task. However:
- **Challenge**: If a model answers *correctly* in both languages but uses different cultural metaphors, the semantic similarity might be low (which looks "bad" but is actually "good cultural adaptation").
- **Verdict**: Our metric measures *consistency*, not necessarily *quality*. We should clarify that "high divergence" isn't always a failure mode; sometimes it's a feature.

## 3. Product Value (The "Product" aspect)

**Is this just a script?**
To transform this from "scripts" to a "product":
- The **Streamlit App** helps significantly. It bridges the gap between code and user experience.
- **Visualizations**: The heatmaps are good, but they are static.
- **Future Feature**: A "Live Bias Checker" where a user types a prompt and we instantly show how 3 models might treat it differently.
