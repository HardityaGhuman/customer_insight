import google.generativeai as genai
import streamlit as st
import re

def configure_gemini():
    """Configure Gemini AI with API key"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return True
    except Exception as e:
        st.error(f"Error configuring Gemini: {e}")
        return False

def analyze_reviews(reviews_text, model_name="gemini-2.5-flash"):
    """Analyze customer reviews using Gemini AI"""
    
    if not configure_gemini():
        return None
    
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
    You are an expert customer insights analyst. Analyze the following customer reviews and provide:

    1. **Overall Sentiment**: (Positive/Negative/Mixed) with percentage breakdown
    2. **Top 5 Customer Pain Points**: Specific issues mentioned
    3. **Top 5 Positive Drivers**: What customers love
    4. **Key Themes**: Main topics discussed (3-5 themes)
    5. **Actionable Recommendations**: 3 specific business actions
    6. **Urgency Level**: (Low/Medium/High) based on sentiment intensity

    Format your response clearly with headers and bullet points.

    Customer Reviews:
    {reviews_text}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error analyzing reviews: {e}")
        return None

def extract_sentiment_score(analysis_text):
    """Extract sentiment percentages from analysis"""
    # Simple regex to find percentage patterns
    positive_match = re.search(r'positive[:\s]+(\d+)%', analysis_text, re.IGNORECASE)
    negative_match = re.search(r'negative[:\s]+(\d+)%', analysis_text, re.IGNORECASE)
    
    positive = int(positive_match.group(1)) if positive_match else 70
    negative = int(negative_match.group(1)) if negative_match else 30
    
    return positive, negative

def quick_sentiment_analysis(reviews_text):
    """Quick sentiment classification without full analysis"""
    positive_words = ['good', 'great', 'excellent', 'love', 'amazing', 'best', 'happy', 'satisfied']
    negative_words = ['bad', 'poor', 'terrible', 'hate', 'worst', 'disappointed', 'awful', 'horrible']
    
    reviews_lower = reviews_text.lower()
    
    positive_count = sum(reviews_lower.count(word) for word in positive_words)
    negative_count = sum(reviews_lower.count(word) for word in negative_words)
    
    total = positive_count + negative_count
    if total == 0:
        return 50, 50
    
    positive_pct = int((positive_count / total) * 100)
    negative_pct = 100 - positive_pct
    
    return positive_pct, negative_pct