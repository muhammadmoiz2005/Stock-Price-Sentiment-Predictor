import os
from dotenv import load_dotenv
from typing import List, Dict, Tuple

# Load environment variables
load_dotenv()

try:
    import google.generativeai as genai
except Exception:
    genai = None

# Load API key from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if genai and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️ Gemini API Key Not Availabile. Chatbot will use offline fallback mode.")

# --- Initialize system message ---
def init_system_message() -> Dict:
    return {
        "role": "system",
        "content": (
            "You are a concise and safety-aware financial assistant. "
            "Always remind users that you are not a financial advisor."
        )
    }

# --- Main Chat Function ---
def ask_chatbot(user_text: str, history: List[Dict] = None, model_name: str = "gemini-1.5-flash") -> Tuple[str, List[Dict]]:
    """
    Sends user text to Gemini API and returns response + chat history.
    """
    if history is None:
        history = [init_system_message()]
    history.append({"role": "user", "content": user_text})

    # Fallback if Gemini not configured
    if genai is None or not GEMINI_API_KEY:
        reply = offline_fallback(user_text)
        history.append({"role": "assistant", "content": reply})
        return reply, history

    try:
        model = genai.GenerativeModel(model_name)
        # Combine chat history into a single text prompt (Gemini expects text, not role structure)
        conversation_text = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in history
        )
        response = model.generate_content(conversation_text)
        reply = response.text.strip()
        history.append({"role": "assistant", "content": reply})
        return reply, history
    except Exception as e:
        err = f"⚠️ Gemini Chatbot Error: {e}"
        history.append({"role": "assistant", "content": err})
        return err, history


# --- Offline Fallback ---
def offline_fallback(user_text: str) -> str:
    txt = user_text.lower()
    if "price" in txt:
        return "📊 Open the Dashboard tab to view live prices. For predictions, use the Predict button."
    if "sentiment" in txt:
        return "🧠 Sentiment is computed using TextBlob polarity — positive, neutral, or negative labels are shown."
    if "model" in txt:
        return "⚙️ The model predicts short-term up/down movement — demo only, not financial advice."
    return "🤖 I’m running in offline mode. Ask about price, sentiment, or model."
