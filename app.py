import streamlit as st

st.set_page_config(
    page_title="Customer Insight AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    .feature-box {
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">Customer Insight AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Transform Customer Feedback into Actionable Business Intelligence</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### Dashboard
    Analyze customer reviews with AI-powered sentiment analysis and visualizations
    """)
    if st.button("Go to Dashboard →", use_container_width=True):
        st.switch_page("pages/dashboard.py")

st.markdown("---")

# Features showcase
st.markdown("## Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    - **AI-Powered Analysis**: Using Google Gemini AI
    - **Bulk Upload**: Analyze CSV/Excel files
    """)

with col2:
    st.markdown("""
    - **Export Reports**: Download insights as PDF
    - **Actionable Insights**: Get specific recommendations
    """)

st.markdown("---")
st.markdown("### Quick Start")
st.info("Navigate to **Dashboard** from the sidebar to begin analyzing customer reviews!")