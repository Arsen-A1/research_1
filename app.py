import streamlit as st
import pandas as pd
import json
import plotly.express as px
from pathlib import Path

# --- Configuration ---
st.set_page_config(
    page_title="Cross-Lingual LLM Bias Explorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Data Loading ---
@st.cache_data
def load_data():
    questions_path = Path("data/questions_multilingual.json")
    with open(questions_path, "r") as f:
        questions = json.load(f)
    
    # Load responses for available models
    models = ["llama3-8b", "llama3-70b", "jais-30b"]
    responses = {}
    for model in models:
        path = Path(f"results/responses/{model}_responses.json")
        if path.exists():
            with open(path, "r") as f:
                responses[model] = json.load(f)
    
    # Load analysis summary
    analysis_path = Path("results/analysis_summary.csv")
    if analysis_path.exists():
        analysis_df = pd.read_csv(analysis_path)
    else:
        analysis_df = pd.DataFrame()

    return questions, responses, analysis_df

questions, responses, analysis_df = load_data()

# --- Sidebar ---
with st.sidebar:
    st.title("🌍 LLM Cross-Lingual Explorer")
    st.markdown("### By Arsen Bakhitbekov")
    st.info(
        "**Research Question:** Do LLMs change their personality when they change language?\n\n"
        "Exploring behavioral divergence in Llama 3 and Jais across English, Russian, Chinese, and Kazakh."
    )
    
    selected_model = st.selectbox(
        "Select Model to Analyze",
        options=list(responses.keys()),
        index=1, # Default to 70b
        format_func=lambda x: responses[x]["model"]
    )

    st.divider()
    st.markdown("[View Portfolio](https://github.com/arsenbakhitbekov)")

# --- Main Page ---

st.header(f"Analyzing: {responses[selected_model]['model']}")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["🔍 Interactive Probe", "📊 Visualizations", "📝 Methodology & Critique"])

with tab1:
    st.subheader("Probe the Model")
    st.markdown("Select a question to see how the model answers in different languages side-by-side.")
    
    # Filter questions by category
    categories = ["All"] + sorted(list(set(q["category"] for q in questions)))
    selected_category = st.selectbox("Filter by Category", categories)
    
    filtered_questions = questions
    if selected_category != "All":
        filtered_questions = [q for q in questions if q["category"] == selected_category]
    
    selected_q_id = st.selectbox(
        "Select Question",
        options=[q["id"] for q in filtered_questions],
        format_func=lambda x: f"Q{x}: {next(q['en'] for q in questions if q['id'] == x)}"
    )
    
    # Get the specific question object
    q_obj = next(q for q in questions if q["id"] == selected_q_id)
    
    # Display Question
    st.markdown(f"**Question (EN):** {q_obj['en']}")
    
    # metrics for this question
    if not analysis_df.empty:
        q_stats = analysis_df[
            (analysis_df["model"] == selected_model) & 
            (analysis_df["question_id"] == selected_q_id)
        ]
    
    # Columns for languages
    cols = st.columns(4)
    languages = ["en", "ru", "zh", "kz"]
    flags = {"en": "🇬🇧", "ru": "🇷🇺", "zh": "🇨🇳", "kz": "🇰🇿"}
    
    model_responses = responses[selected_model]["responses"]
    
    for idx, lang in enumerate(languages):
        with cols[idx]:
            st.markdown(f"### {flags[lang]} {lang.upper()}")
            
            # Find the answer
            ans = next(
                (r for r in model_responses if r["question_id"] == selected_q_id and r["language"] == lang),
                None
            )
            
            if ans:
                st.info(ans["question"])
                st.write(ans["answer"])
                
                if not analysis_df.empty:
                    lang_stat = q_stats[q_stats["language"] == lang]
                    if not lang_stat.empty:
                        wc = lang_stat.iloc[0]["answer_length_words"]
                        conf = lang_stat.iloc[0]["confidence_score"]
                        st.caption(f"Length: {wc} words | Confidence: {conf:.2f}")
            else:
                st.warning("No response found.")

with tab2:
    st.subheader("Global Metrics")
    
    # Helper to load image
    def show_plot(filename, caption):
        path = Path(f"results/figures/{filename}")
        if path.exists():
            st.image(str(path), caption=caption, use_column_width=True)
        else:
            st.warning(f"Plot {filename} not found.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Verbosity Asymmetry")
        st.write("Does the model speak less in certain languages?")
        show_plot(f"response_length_{selected_model}.png", "Response Length Distribution")
        
    with col2:
        st.markdown("### Confidence & Safety")
        st.write("Does the model hedge more in certain languages?")
        show_plot(f"confidence_analysis_{selected_model}.png", "Confidence Scores")

    st.markdown("### Cross-Lingual Semantic Similarity")
    st.write("Do the answers actually mean the same thing?")
    show_plot(f"similarity_heatmap_{selected_model}.png", "Semantic Similarity Heatmap")

with tab3:
    st.markdown("""
    ## Research Methodology
    We queried 50 questions across 3 categories (Factual, Opinion, Commonsense) in 4 languages.
    
    ### Critical Evaluation (Weaknesses)
    As a young researcher, it is important to be honest about limitations:
    1.  **Sample Size**: 50 questions is small. A true benchmark needs 1000+.
    2.  **Translation Quality**: We relied on manual translation. Ideally, native speakers should verify every nuance.
    3.  **Prompt Sensitivity**: We used a single system prompt. Models might behave differently with "You are a Russian expert".
    4.  **Auto-Metrics**: "Confidence" is a heuristic based on keywords. Real confidence requires internal logit analysis.
    
    ### Future Work
    - Expand to 500+ questions using automated translation + verification.
    - Test "System Prompting" to fix the Jais Kazakh verbosity issue.
    - Analyze "Safety Refusals" specifically to see if models refuse to answer political topics in RU/ZH.
    """)
