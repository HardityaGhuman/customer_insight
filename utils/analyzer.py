import google.generativeai as genai
import streamlit as st
import json


def configure_gemini():
    """Configure Gemini AI with API key"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return True
    except Exception as e:
        st.error(f"Error configuring Gemini: {e}")
        return False


def analyze_reviews(reviews_text, model_name="gemini-2.5-flash", max_retries=1):
    """
    Phase-1 reasoning function.

    Behavior:
    - Tries LLM reasoning
    - Retries once on failure
    - Returns None if all attempts fail
    """

    if not configure_gemini():
        return None

    model = genai.GenerativeModel(model_name)

    prompt = f"""
You are a data processing function.

Return ONLY valid JSON with the following structure:

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
- Do NOT include explanations, markdown, or extra text

Customer reviews:
{reviews_text}
"""

    for attempt in range(max_retries + 1):
        try:
            response = model.generate_content(prompt)
            raw_text = response.text

            # Phase-1 contract enforcement
            data = json.loads(raw_text)
            return data

        except json.JSONDecodeError:
            if attempt == max_retries:
                st.error("LLM returned invalid JSON after retry.")
            continue

        except Exception as e:
            if attempt == max_retries:
                st.error(f"LLM error after retry: {e}")
            continue

    return None


def extract_sentiment_score(analysis_data):
    """
    Extract sentiment scores from structured analysis output.
    """
    sentiment = analysis_data["sentiment_distribution"]
    return sentiment["positive"], sentiment["negative"]


def quick_sentiment_analysis(reviews_text):
    """
    Deterministic heuristic sentiment fallback.
    Used ONLY if LLM reasoning fails.
    """
    positive_words = [
        "good", "great", "excellent", "love", "amazing",
        "best", "happy", "satisfied"
    ]
    negative_words = [
        "bad", "poor", "terrible", "hate", "worst",
        "disappointed", "awful", "horrible"
    ]

    reviews_lower = reviews_text.lower()

    positive_count = sum(reviews_lower.count(word) for word in positive_words)
    negative_count = sum(reviews_lower.count(word) for word in negative_words)

    total = positive_count + negative_count
    if total == 0:
        return 50, 50

    positive_pct = int((positive_count / total) * 100)
    negative_pct = 100 - positive_pct

    return positive_pct, negative_pct


def analyze_with_fallback(reviews_text):
    """
    Phase-1 orchestration:
    - Try LLM reasoning
    - If it fails, use heuristic fallback
    """

    analysis = analyze_reviews(reviews_text)

    if analysis is not None:
        return analysis, "llm"

    # LLM failed → heuristic fallback
    positive, negative = quick_sentiment_analysis(reviews_text)

    fallback_analysis = {
        "sentiment_distribution": {
            "positive": positive,
            "negative": negative,
            "neutral": 100 - positive - negative
        },
        "top_pain_points": [],
        "top_positive_drivers": [],
        "key_themes": [],
        "urgency": "medium",
        "recommended_actions": []
    }

    return fallback_analysis, "heuristic"