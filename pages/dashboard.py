import streamlit as st
import pandas as pd

from utils.analyzer import analyze_with_fallback
from utils.exporter import (
    export_to_csv,
    export_to_excel,
    create_markdown_report,
)

# ---------------- PAGE SETUP ----------------

st.set_page_config(
    page_title="Customer Insight Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Customer Insight Dashboard")

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.header("Input Options")
    input_method = st.radio(
        "Choose input method:",
        ["Text Input", "Upload CSV/Excel"]
    )

# ---------------- SESSION STATE ----------------

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "analysis_source" not in st.session_state:
    st.session_state.analysis_source = None

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
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx"]
    )

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success(f"Loaded {len(df)} rows")
            st.dataframe(df.head(), use_container_width=True)

            review_column = st.selectbox(
                "Select column containing reviews:",
                df.columns
            )

            if review_column:
                reviews_input = "\n".join(
                    df[review_column].astype(str).tolist()
                )
                st.session_state.reviews_text = reviews_input
                st.info(
                    f"Loaded {len(df)} reviews from column '{review_column}'"
                )

        except Exception as e:
            st.error(f"Error loading file: {e}")

# ---------------- ANALYSIS ----------------

analyze_button = st.button(
    "Analyze Reviews",
    type="primary",
    use_container_width=True
)

if analyze_button and reviews_input.strip():
    with st.spinner("Analyzing reviews..."):
        analysis, source = analyze_with_fallback(reviews_input)

        if analysis:
            st.session_state.analysis_result = analysis
            st.session_state.analysis_source = source
            st.success("Analysis complete!")
        else:
            st.error("Analysis failed completely.")

# ---------------- RESULTS ----------------

if st.session_state.analysis_result:
    st.markdown("---")

    analysis = st.session_state.analysis_result
    source = st.session_state.analysis_source
    sentiment = analysis["sentiment_distribution"]

    if source == "heuristic":
        st.warning(
            "LLM analysis failed. Displaying heuristic fallback results."
        )

    # ---------------- SENTIMENT OVERVIEW ----------------

    st.subheader("Sentiment Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Positive", f"{sentiment['positive']}%")
    col2.metric("Negative", f"{sentiment['negative']}%")
    col3.metric("Neutral", f"{sentiment['neutral']}%")

    st.markdown(f"**Urgency Level:** {analysis['urgency'].capitalize()}")

    # ---------------- INSIGHTS ----------------

    st.markdown("---")
    st.subheader("Key Themes")
    for theme in analysis["key_themes"]:
        st.write(f"- {theme}")

    st.subheader("Top Customer Pain Points")
    for point in analysis["top_pain_points"]:
        st.write(f"- {point}")

    st.subheader("What Customers Like")
    for driver in analysis["top_positive_drivers"]:
        st.write(f"- {driver}")

    st.subheader("Recommended Actions")
    for action in analysis["recommended_actions"]:
        st.write(f"- {action}")

    # ---------------- EXPORT ----------------

    st.markdown("---")
    st.subheader("Export Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        csv_data = export_to_csv(
            analysis,
            st.session_state.reviews_text
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
            analysis,
            st.session_state.reviews_text
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
            analysis,
            st.session_state.reviews_text
        )
        st.download_button(
            "Download Report (MD)",
            markdown_data,
            file_name=f"report_{pd.Timestamp.now():%Y%m%d_%H%M%S}.md",
            mime="text/markdown",
            use_container_width=True,
        )

else:
    st.info(
        "Enter reviews above and click **Analyze Reviews** to get started!"
    )