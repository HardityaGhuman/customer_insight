# Customer Insight Dashboard

Customer Insight Dashboard is a Streamlit based application for analyzing customer reviews and converting unstructured feedback into structured business insights.

The project focuses on building a reliable review analysis pipeline rather than UI polish or model experimentation.

---

## Live Demo

https://customerinsight-vekjyeergmiwq4efckdnhs.streamlit.app/

---

## What the App Does

- Accepts customer reviews via:
  - Manual text input
  - CSV or Excel file upload
- Analyzes reviews to determine:
  - Overall sentiment distribution
  - Common customer pain points
  - Positive drivers
  - Key themes
  - Urgency level
  - Actionable recommendations
- Allows exporting results as:
  - CSV
  - Excel
  - Markdown
  - JSON (for programmatic use)

---

## Implementation Notes

- Review analysis is performed using a Large Language Model (Google Gemini)
- The model is treated as an external dependency and not a source of truth
- Outputs are constrained to a predefined JSON schema
- Invalid or failed model responses fall back to a simple heuristic analysis
- All downstream components operate on structured data only

---

## Tech Stack

- Streamlit  
- Google Gemini (`gemini-2.5-flash`)  
- Pandas  
- openpyxl  

---

## Project Status

Phase 1 complete.  
The core analysis pipeline is stable and designed to be extended with additional automation or agent-based logic.