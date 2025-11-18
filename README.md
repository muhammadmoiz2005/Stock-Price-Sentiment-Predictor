# Real-Time Stock Sentiment & AI Chatbot Predictor

**Contents**
- Streamlit dashboard combining live price (Binance), sentiment analysis, ML prediction, and OpenAI-powered chatbot.
- Safe defaults allow running the app with sample data even if API keys are not set.

## Setup (local)

1. Clone or extract the project.
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill keys (optional for live data):
   ```bash
   cp .env.example .env
   ```
5. Run Streamlit:
   ```bash
   streamlit run app.py
   ```

## Notes
- If you do not have Binance keys, the app will use historical CSV or sample data.
- If you do not have an OpenAI key, chatbot feature will warn and operate in offline fallback mode.
- Do NOT commit `.env` to public repositories.
