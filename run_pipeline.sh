#!/bin/bash
set -e

# Configuration
VENV_DIR=".venv"
MODELS=("llama3-8b" "llama3-70b")
LANGUAGES=("en" "ru" "zh" "kz")

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Setup Virtual Environment
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${BLUE}🔨 Creating virtual environment...${NC}"
    uv venv $VENV_DIR
fi

echo -e "${BLUE}📦 Installing dependencies...${NC}"
source $VENV_DIR/bin/activate
uv pip install -r requirements.txt

# 2. Query LLMs
echo -e "${BLUE}🤖 Querying LLMs...${NC}"
python scripts/query_llms.py --models "${MODELS[@]}" --languages "${LANGUAGES[@]}"

# 3. Import Manual Responses (Jais)
echo -e "${BLUE}📥 Importing manual responses...${NC}"
python scripts/parse_manual.py

# 4. Analyze Responses
echo -e "${BLUE}📊 Analyzing responses...${NC}"
python scripts/analyze_responses.py

# 4. Semantic Similarity
echo -e "${BLUE}🔍 Computing semantic similarity...${NC}"
python scripts/similarity_analysis.py

# 5. Visualize
echo -e "${BLUE}🎨 Generating visualizations...${NC}"
python scripts/visualize.py

echo -e "${GREEN}✅ Pipeline complete! Check results/ folder.${NC}"
