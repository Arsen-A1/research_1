# Cross-Lingual-LLM-Bias

[![Status](https://img.shields.io/badge/Status-Active_Research-blue.svg)]()
[![Paper](https://img.shields.io/badge/Paper-Pending_Publication-green.svg)]()

**Abstract:** This repository investigates the behavioral divergence and cultural alignment of open-source Large Language Models (LLMs) such as Llama 3 and Jais 30B when prompted in different languages, specifically examining variations in safety filters, personality, and knowledge depth between English, Russian, Kazakh, and Chinese.

<div align="center">
  <img src="similarity_heatmap_llama.png" alt="Project Architecture" width="800">
</div>

## 🌱 Personal Motivation
As a multilingual speaker (Kazakh, Russian, English, Chinese) and an active language learner, I noticed early on that AI systems don't just "translate" thought; they change it depending on the language used. I initiated this research because I want to ensure that non-Western languages aren't penalized by the architectures of modern LLMs. Specifically, working with **Jais 30B** during this project opened my eyes to the incredible potential of region-specific, culturally aligned models. My ultimate goal is to deepen my research into MENA-region NLP and work more extensively with the Jais ecosystem to bridge the linguistic divide in AI.

## 🎯 Research Objectives
- Evaluate how the "safety curtain" shifts in Llama 3 when switching from English to Russian.
- Measure the "underrepresented tax" by analyzing the brevity and depth of Jais 30B responses in Kazakh compared to English.
- Quantify how models explain culturally tied concepts (e.g., "democracy", "traditional medicine") across linguistic borders.

## 🧠 Methodology & Tech Stack
- **Models Evaluated:** Llama 3 (Meta), Jais 30B (Inception Institute of Artificial Intelligence / MBZUAI).
- **Data Engineering:** Custom cross-lingual conversational datasets targeting opinion-based prompts, safety edges, and cultural commonsense.
- **Frameworks:** PyTorch, HuggingFace Transformers, LangChain.

## 📊 Key Findings / Results
- **The "Safety Curtain":** Llama 3 adds safety disclaimers to 73% of opinion responses in Russian, behaving significantly more cautiously than in English.
- **The "Underrepresented Tax":** Jais 30B provides answers that are on average ~50% shorter when queried in Kazakh compared to English, despite possessing the underlying knowledge.

## 📬 Contact & Research Interests
I am actively seeking to expand this research into MENA-region NLP and culturally aligned foundation models. My primary academic aspiration is to join the research community at **MBZUAI** to contribute directly to the development of the **Jais** ecosystem and similar initiatives.

If you are a professor, researcher, or engineer working on multilingual LLM alignment, I would be thrilled to connect.

**Arsen Bakhitbekov** - [bakhitbekovv@gmail.com](mailto:bakhitbekovv@gmail.com)
