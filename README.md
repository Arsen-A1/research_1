# 🌍 Cross-Lingual LLM Bias Explorer

> **research by Arsen Bakhitbekov**  
> *Exploring the "Personality Split" of AI across English, Russian, Chinese, and Kazakh.*

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](app.py)

## 🎯 Project Overview
As a multilingual researcher (KZ/RU/EN/ZH), I noticed that LLMs don't just translate — they fundamentally shift their tone, safety standards, and intellectual depth when switching languages. 

This project investigates **Behavioral Divergence** in open-source models (Llama 3, Jais 30B) to answer:
*   **Do models "know less" in Kazakh?** (Spoiler: Yes, Jais provides 50% shorter answers.)
*   **Are models "more scared" in Russian?** (Spoiler: Llama 3 hedges nearly 7x more on opinion topics.)
*   **Does culture leak into commonsense?** (How do models explain "democracy" or "traditional medicine" across borders?)

## 📊 Key Findings

### 1. The "Underrepresented Tax"
For **Jais 30B**, querying in Kazakh yields significantly degraded responses compared to English, despite the same underlying model knowledge.

![Response Length](results/figures/response_length_jais-30b.png)

### 2. The "Safety Curtain"
**Llama 3** behaves like a different person in Russian. It becomes hyper-cautious, adding safety disclaimers to 73% of opinion responses, whereas in English, it discusses the same topics freely.

![Confidence Analysis](results/figures/confidence_analysis_llama3-8b.png)

## 🚀 Interactive Demo
I built a **Streamlit App** to let you explore these biases firsthand.
1.  **Select a Topic**: Choose from 50 questions (Politics, Culture, Science).
2.  **Compare**: See the model's "split personality" side-by-side.
3.  **Analyze**: View real-time confidence scores.

To run locally:
```bash
pip install -r requirements.txt
streamlit run app.py
```
## 🧠 Methodology
- **Models**: Llama 3.1 8B, Llama 3.3 70B, Jais 30B (Arabic/English hybrid).
- **Dataset**: 50 curated questions (Factual, Opinion, Commonsense) translated into EN, RU, ZH, KZ.
- **Metrics**: 
    - `Response Length` (Verbosity bias)
    - `Confidence Score` (Hedging bias)
    - `Semantic Similarity` (Multilingual embeddings via BERT)

## 🙋‍♂️ About Me
**Arsen Bakhitbekov** | NIS PhM Almaty
I am an aspiring AI researcher passionate about making NLP equitable for all languages. I am currently building a startup for language learning and researching low-resource NLP.
*Aiming for the MBZUAI AIR Program to further explore cross-cultural AI alignment.*

## 🙏 Acknowledgements
Special thanks to **Yerdaulet Damir (MBZUAI '30)** for his technical mentorship and guidance on LLM architectures throughout this research project.
