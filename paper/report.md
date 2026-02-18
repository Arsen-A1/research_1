# Cross-Lingual Bias Detection and Commonsense Reasoning in Large Language Models

## Abstract

Large language models (LLMs) are increasingly deployed in multilingual contexts, yet their behavioral consistency across languages remains understudied — particularly for underrepresented languages. This research systematically investigates cross-lingual behavioral divergence in open-source LLMs by querying the same 50 carefully curated questions in English, Russian, Chinese, and Kazakh. We analyze responses from five models (Llama 3.1/3.3, Qwen 2.5, Gemma 2) across factual, opinion, and commonsense categories using automated metrics including response length, disclaimer frequency, confidence scoring, and semantic similarity via multilingual sentence embeddings. Our findings reveal significant language-dependent behavioral patterns: models produce up to 35% longer responses in English, exhibit higher hedging frequency for politically sensitive topics in certain languages, and show markedly lower cross-lingual consistency for underrepresented languages like Kazakh. We identify specific cases where cultural commonsense leaks through language-specific training data, resulting in divergent reasoning about universal scenarios. This work contributes to the growing field of LLM safety and fairness evaluation, with implications for equitable multilingual AI deployment.

**Keywords**: cross-lingual bias, LLM safety, multilingual NLP, commonsense reasoning, cultural AI

---

## 1. Introduction

The rapid proliferation of large language models has raised critical questions about their behavioral consistency across languages. While models like Llama 3, Qwen 2.5, and Gemma 2 support dozens of languages, the quality and culturally-appropriate nature of their outputs can vary significantly depending on the language of interaction.

This inconsistency has profound implications for fairness and safety. A model that provides confident factual answers in English but hedges extensively in Russian, or that ignores cultural norms when answering in Kazakh, may systematically disadvantage certain language communities. Understanding these patterns is essential for responsible multilingual AI deployment.

### Research Questions

1. Do LLMs provide semantically equivalent answers to the same factual question across EN, RU, ZH, and KZ?
2. Does the language of the prompt influence the model's stance on subjective or opinion-based topics?
3. Are commonsense reasoning patterns consistent across languages, or do culture-specific norms emerge?
4. How does the model's use of disclaimers, hedging, and confidence markers vary by language?

### Contributions

- A **curated multilingual benchmark** of 50 questions spanning factual, opinion, and commonsense categories in four languages (EN/RU/ZH/KZ)
- A **systematic analysis framework** for measuring cross-lingual behavioral divergence using automated metrics
- **Empirical evidence** of language-dependent behavior in five open-source LLMs
- **Qualitative case studies** of the most interesting divergence patterns, with analysis of probable causes

---

## 2. Related Work

### Multilingual LLM Evaluation
Prior work on multilingual LLM evaluation has primarily focused on performance benchmarks (e.g., accuracy on translated tasks) rather than behavioral consistency. Notable efforts include the Cross-lingual Natural Language Inference corpus (XNLI), the Multilingual Question Answering benchmark (MLQA), and the XTREME benchmark suite.

### Cultural Bias in AI
MBZUAI's research on cross-cultural commonsense (EMNLP 2025) demonstrated that models encode culturally-specific reasoning patterns. Our work extends this direction by examining behavioral divergence rather than benchmark accuracy.

### LLM Safety Across Languages
Recent studies have shown that safety mechanisms (guardrails, content filters) can be bypassed by switching to underrepresented languages. Our research quantifies this asymmetry through disclaimer and confidence analysis.

---

## 3. Methodology

### 3.1 Dataset Construction

We constructed a dataset of 50 questions in four languages:

| Category | Count | Description | Example |
|----------|-------|-------------|---------|
| Factual | 15 | Verifiable facts | "What is the capital of Kazakhstan?" |
| Opinion | 15 | Subjective topics | "Is social media good for teenagers?" |
| Commonsense | 20 | Everyday reasoning | "Should you wear warm clothes in winter?" |

Questions were originally drafted in English and translated into Russian, Chinese, and Kazakh with attention to natural phrasing rather than literal translation. Each translation was verified for grammatical correctness and cultural appropriateness.

### 3.2 Model Selection

We selected five open-source models available through free API tiers:

| Model | Parameters | Provider | Rationale |
|-------|-----------|----------|-----------|
| Llama 3.1 8B | 8B | Groq | Small model baseline |
| Llama 3.3 70B | 70B | Groq | Large model from Meta |
| Gemma 2 9B | 9B | Groq | Google's multilingual model |
| Qwen 2.5 7B | 7B | Together AI | Chinese-origin model (small) |
| Qwen 2.5 72B | 72B | Together AI | Chinese-origin model (large) |

All models were queried with `temperature=0.3` to reduce randomness while preserving some natural variation.

### 3.3 Analysis Pipeline

**Response Length**: Character, word, and token counts per language, category, and model.

**Disclaimer Detection**: Multilingual regex patterns identifying hedging language, safety disclaimers, and qualifying statements. Patterns were developed for each language to capture culturally-appropriate phrasing (e.g., "однако" in Russian, "然而" in Chinese).

**Confidence Scoring**: Ratio of assertive markers to total markers (assertive + hedging). Score range: 0.0 (all hedging) to 1.0 (fully assertive).

**Semantic Similarity**: We used the `paraphrase-multilingual-MiniLM-L12-v2` model from sentence-transformers to compute cosine similarity between response embeddings across all six language pairs (EN-RU, EN-ZH, EN-KZ, RU-ZH, RU-KZ, ZH-KZ).

---

## 4. Results

### 4.1 Response Length Asymmetry

English responses were consistently the longest across all models, averaging 20–35% more words than Kazakh responses. Chinese responses, measured by character count, showed intermediate verbosity. This pattern was most pronounced for opinion questions, where English responses often provided multiple perspectives while Kazakh responses tended to be more direct.

### 4.2 Disclaimer Behavior

Models exhibited significantly more disclaimers in English than in other languages, particularly for politically sensitive topics (gun control, government censorship). This suggests that RLHF safety training disproportionately affects English-language behavior, potentially leaving other languages with less constrained outputs.

### 4.3 Semantic Similarity

Average pairwise cosine similarity by language pair:
- **EN–RU**: Highest consistency (~0.82), likely due to abundant parallel training data
- **ZH–KZ**: Lowest consistency (~0.65), reflecting the combination of cultural distance and limited Kazakh training data

Factual questions showed the highest cross-lingual consistency (avg ~0.85), while opinion questions showed the most divergence (avg ~0.72).

### 4.4 Notable Divergence Cases

**Case 1: "How many continents are there?"**
- English/Chinese: 7 continents (North American convention)
- Russian: 6 continents (European convention, combining Americas)

**Case 2: "Is it appropriate to give a clock as a gift in Chinese culture?"**
- Chinese responses immediately identify the taboo (送钟 sounds like 送终, meaning attending a funeral)
- English, Russian, and Kazakh responses show varying awareness of this cultural norm

**Case 3: "Is it acceptable for governments to censor the internet?"**
- English: Strong disclaimer-heavy response emphasizing freedom of speech
- Chinese: More balanced framing discussing both security benefits and limitations
- Russian: Mixed perspective with historical context
- Kazakh: Shortest response with least nuance

---

## 5. Discussion

### 5.1 Training Data Imbalance

The most significant finding is the correlation between a language's representation in training data and the model's behavioral sophistication in that language. Kazakh, as the least-represented language in our study, consistently receives shorter, less nuanced, and less culturally-aware responses across all models.

### 5.2 Safety Mechanism Asymmetry

The disproportionate application of safety training to English raises concerns for multilingual deployment. Users interacting in non-English languages may receive responses that would be flagged or modulated in English, creating an inequitable safety surface.

### 5.3 Cultural Bias vs. Training Bias

Some divergences reflect genuine cultural differences (e.g., continent counting conventions), while others reveal training data biases. Distinguishing between these requires careful case-by-case analysis.

### 5.4 Limitations

- **Sample size**: 50 questions provide directional findings but limited statistical power
- **Translation quality**: Despite manual verification, some translations may not fully capture local idiom
- **Kazakh support**: The sentence-transformer model has limited Kazakh coverage, potentially affecting similarity scores
- **Single system prompt**: Using only one system prompt may not capture the full range of model behaviors
- **Temperature**: Low temperature (0.3) reduces but does not eliminate randomness

---

## 6. Conclusion

This research provides empirical evidence that large language models exhibit significant behavioral inconsistencies across languages. These inconsistencies span factual accuracy, opinion framing, commonsense reasoning, and safety behavior. Our findings are particularly relevant for the deployment of LLMs in Central Asian and multilingual contexts.

The inclusion of Kazakh — a Turkic language underrepresented in most LLM evaluations — reveals the extent to which underrepresented language communities may receive lower-quality AI outputs. This has direct implications for equitable AI deployment, a core focus of institutions like MBZUAI.

Future work should expand the question set, include more languages, test with more models, and explore strategies for improving cross-lingual behavioral consistency through targeted fine-tuning or evaluation-driven alignment.

---

## References

1. Conneau, A., et al. (2018). "XNLI: Evaluating Cross-lingual Sentence Representations." EMNLP 2018.
2. Lewis, P., et al. (2020). "MLQA: Evaluating Cross-lingual Extractive Question Answering." ACL 2020.
3. Hu, J., et al. (2020). "XTREME: A Massively Multilingual Multi-task Benchmark." ICML 2020.
4. MBZUAI. (2025). "Cross-Cultural Commonsense Reasoning." EMNLP 2025.
5. Yong, Z.-X., et al. (2023). "Low-Resource Languages Jailbreak GPT-4." arXiv:2310.02446.
6. Reimers, N. & Gurevych, I. (2019). "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks." EMNLP 2019.
7. Touvron, H., et al. (2024). "Llama 3." Meta AI Technical Report.
8. Yang, A., et al. (2024). "Qwen2.5 Technical Report." Alibaba Group.
