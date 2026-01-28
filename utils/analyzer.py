import google.generativeai as genai
import streamlit as st
import json


# ---------------- CONFIG ----------------

def configure_gemini():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return True
    except Exception as e:
        st.error(f"Gemini configuration failed: {e}")
        return False


# ---------------- UTILS ----------------

def extract_json(text: str):
    """
    Safely extract first JSON object from model output.
    """
    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == -1:
        raise json.JSONDecodeError("No JSON object found", text, 0)

    return json.loads(text[start:end])


# ---------------- LLM ANALYSIS ----------------

def analyze_reviews(reviews_text, model_name="gemini-2.5-flash", max_retries=1):
    """
    Phase-1 reasoning unit.
    Returns structured JSON or None.
    """

    if not configure_gemini():
        return None

    model = genai.GenerativeModel(model_name)

    base_prompt = f"""
SYSTEM INSTRUCTION:
You are a strict JSON generator.

You MUST return a single valid JSON object.
Any non-JSON output is a failure.

Return EXACTLY this schema:

{{
  "sentiment_distribution": {{
    "positive": number,
    "negative": number,
    "neutral": number
  }},
  "top_pain_points": [string],
  "top_positive_drivers": [string],
  "key_themes": [string],
  "urgency": "low" | "medium" | "high",
  "recommended_actions": [string]
}}

Rules:
- Percentages must sum to 100
- All lists must contain at least one item
- urgency must be one of: low, medium, high
- Do NOT include explanations, markdown, or comments

Customer reviews:
{reviews_text}
"""

    prompt = base_prompt
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            response = model.generate_content(prompt)
            return extract_json(response.text)

        except Exception as e:
            last_error = str(e)
            prompt = base_prompt + f"""

IMPORTANT:
Your previous response failed with the following error:
{last_error}

Return ONLY valid JSON. No explanation.
"""

    st.error("LLM returned invalid JSON after retry.")
    return None


# ---------------- FALLBACK ----------------

def quick_sentiment_analysis(reviews_text):
    """
    Deterministic heuristic baseline.
    Model-independent.
    """

    positive_words = [
        "good", "great", "excellent", "love", "amazing",
        "best", "happy", "satisfied"
    ]
    negative_words = [
        "bad", "poor", "terrible", "hate", "worst",
        "disappointed", "awful", "horrible"
    ]

    text = reviews_text.lower()
    pos = sum(text.count(w) for w in positive_words)
    neg = sum(text.count(w) for w in negative_words)

    if pos + neg == 0:
        return 34, 33, 33

    positive = int((pos / (pos + neg)) * 100)
    negative = int((neg / (pos + neg)) * 100)
    neutral = 100 - positive - negative

    return positive, negative, neutral


# ---------------- ORCHESTRATION ----------------

def analyze_with_fallback(reviews_text):
    """
    Phase-1 orchestrator.
    Always returns contract-valid data.
    """

    analysis = analyze_reviews(reviews_text)

    if analysis is not None:
        return analysis, "llm"

    # Heuristic fallback (contract-safe)
    positive, negative, neutral = quick_sentiment_analysis(reviews_text)

    fallback = {
        "sentiment_distribution": {
            "positive": positive,
            "negative": negative,
            "neutral": neutral
        },
        "top_pain_points": ["Insufficient data for detailed pain points"],
        "top_positive_drivers": ["General customer feedback"],
        "key_themes": ["Mixed feedback"],
        "urgency": "medium",
        "recommended_actions": ["Collect more customer feedback"]
    }

    return fallback, "heuristic"