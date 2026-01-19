import streamlit as st
import pandas as pd
from utils.analyzer import analyze_reviews, extract_sentiment_score
from utils.exporter import export_to_csv, export_to_excel, create_markdown_report

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("Customer Insight Dashboard")

# Sidebar for input options
with st.sidebar:
    st.header("Input Options")
    input_method = st.radio("Choose input method:", ["Text Input", "Upload CSV/Excel"])

# Initialize session state
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "reviews_text" not in st.session_state:
    st.session_state.reviews_text = ""

reviews_input = ""

# ---------------- INPUT ----------------
if input_method == "Text Input":
    reviews_input = st.text_area(
        "Enter customer reviews (one per line):",
        height=200,
        placeholder=(
            "Example:\n"
            "Great product, very satisfied!\n"
            "Shipping was too slow.\n"
            "Excellent customer service!"
        ),
    )
    st.session_state.reviews_text = reviews_input

else:
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success(f"Loaded {len(df)} reviews")
            st.dataframe(df.head(), use_container_width=True)

            review_column = st.selectbox(
                "Select column containing reviews:", df.columns
            )

            if review_column:
                reviews_input = "\n".join(df[review_column].astype(str).tolist())
                st.session_state.reviews_text = reviews_input
                st.info(
                    f"Loaded {len(df)} reviews from column '{review_column}'"
                )

        except Exception as e:
            st.error(f"Error loading file: {e}")

# ---------------- ANALYSIS ----------------
analyze_button = st.button(
    "Analyze Reviews", type="primary", use_container_width=True
)

# 🔒 Hardcoded model (no dropdown)
model_choice = "gemini-2.5-flash"

if analyze_button and reviews_input.strip():
    with st.spinner("Analyzing your reviews..."):
        analysis = analyze_reviews(reviews_input, model_choice)

        if analysis:
            st.session_state.analysis_result = analysis
            st.success("Analysis complete!")
        else:
            st.error("Analysis failed. Please check your API key.")

# ---------------- RESULTS ----------------
if st.session_state.analysis_result:
    st.markdown("---")

    positive_pct, negative_pct = extract_sentiment_score(
        st.session_state.analysis_result
    )

    # ---------------- ANALYSIS TEXT ----------------
    st.markdown("## AI-Generated Insights")
    st.markdown(st.session_state.analysis_result)

    # ---------------- EXPORT ----------------
    st.markdown("---")
    st.markdown("## Export Results")

    col1, col2, col3 = st.columns(3)

    sentiment_data = {
        "positive": positive_pct,
        "negative": negative_pct,
    }

    with col1:
        csv_data = export_to_csv(
            st.session_state.analysis_result,
            st.session_state.reviews_text,
        )
        st.download_button(
            "Download CSV",
            csv_data,
            file_name=f"analysis_{pd.Timestamp.now():%Y%m%d_%H%M%S}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:
        excel_data = export_to_excel(
            st.session_state.analysis_result,
            st.session_state.reviews_text,
            sentiment_data,
        )
        st.download_button(
            "Download Excel",
            excel_data,
            file_name=f"analysis_{pd.Timestamp.now():%Y%m%d_%H%M%S}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    with col3:
        markdown_data = create_markdown_report(
            st.session_state.analysis_result,
            st.session_state.reviews_text,
            sentiment_data,
        )
        st.download_button(
            "Download Report (MD)",
            markdown_data,
            file_name=f"report_{pd.Timestamp.now():%Y%m%d_%H%M%S}.md",
            mime="text/markdown",
            use_container_width=True,
        )

else:
    st.info("Enter reviews above and click **Analyze Reviews** to get started!")