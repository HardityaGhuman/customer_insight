import google.generativeai as genai
import streamlit as st
import json

# ---------------- PHASE 2 CONSTANTS ----------------

ALLOWED_CATEGORIES = [
    "delivery",
    "product",
    "support",
    "billing",
    "app",
    "other"
]

ALLOWED_ESCALATION_LEVELS = [
    "none",
    "monitor",
    "review",
    "escalate"
]

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

# ---------------- PHASE 2 DECISION ----------------

def decide_actions(analysis_data, model_name="gemini-2.5-flash"):
    """
    Phase-2 reasoning unit.
    Uses Phase-1 output to decide category and escalation.
    """

    model = genai.GenerativeModel(model_name)

    prompt = f"""
You are a decision-making system.

Based ONLY on the structured analysis below,
decide:

1. issue_category
2. escalation_level

Return ONLY valid JSON in this format:

{{
  "issue_category": {{
    "category": one of {ALLOWED_CATEGORIES},
    "confidence": number between 0 and 1
  }},
  "escalation": {{
    "level": one of {ALLOWED_ESCALATION_LEVELS},
    "reason": string
  }}
}}

Rules:
- Do NOT invent categories
- Do NOT include explanations outside JSON
- Be conservative when confidence is low

Analysis data:
{json.dumps(analysis_data)}
"""

    response = model.generate_content(prompt)
    return extract_json(response.text)

def categorize_issue(category, confidence):
    if category not in ALLOWED_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")

    return {
        "category": category,
        "confidence": confidence
    }

def decide_escalation(level, reason):
    if level not in ALLOWED_ESCALATION_LEVELS:
        raise ValueError(f"Invalid escalation level: {level}")

    return {
        "level": level,
        "reason": reason
    }

import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "decisions.jsonl")


def log_decision(category_data, escalation_data):
    os.makedirs(LOG_DIR, exist_ok=True)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "issue_category": category_data,
        "escalation": escalation_data
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

from utils.state_manager import load_state, save_state

def phase2_process(analysis_data):
    """
    Phase-2 orchestrator:
    - LLM decides
    - Tools validate
    - System logs
    - State is updated
    """

    decision = decide_actions(analysis_data)

    category_data = categorize_issue(
        decision["issue_category"]["category"],
        decision["issue_category"]["confidence"]
    )

    escalation_data = decide_escalation(
        decision["escalation"]["level"],
        decision["escalation"]["reason"]
    )

    # --- LOAD STATE ---
    state = load_state()

    # Update issue count
    category = category_data["category"]
    state["issue_counts"][category] += 1

    # Update escalation state (idempotent)
    if escalation_data["level"] != "none":
        state["escalation"]["has_been_escalated"] = True
        state["escalation"]["level"] = escalation_data["level"]

    # --- SAVE STATE ---
    save_state(state)

    # Log decision (already implemented)
    log_decision(category_data, escalation_data)

    return {
        "category": category_data,
        "escalation": escalation_data,
        "state_snapshot": state
    }