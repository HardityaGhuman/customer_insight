# Customer Insight Dashboard

Customer Insight Dashboard is a Streamlit-based application for analyzing customer reviews and converting unstructured feedback into structured business insights.

The project focuses on building a **reliable, extensible analysis pipeline** rather than UI polish or model experimentation.

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
- Automatically derives internal decisions:
  - Issue category (e.g. delivery, product, support)
  - Escalation level (monitor / review / escalate)
- Logs decisions for auditability and downstream automation
- Allows exporting results as:
  - CSV
  - Excel
  - Markdown
  - JSON (for programmatic use)

---

## Implementation Notes

- Review analysis is performed using a Large Language Model (Google Gemini)
- The model is treated as an external dependency, not a source of truth
- All LLM outputs are constrained to a predefined JSON schema
- Invalid or failed model responses fall back to a deterministic heuristic analysis
- All downstream components operate on structured data only
- The system is structured in multiple phases:
  - **Phase 1**: Review analysis and insight extraction
  - **Phase 2**: Decision-making based on structured analysis (categorization and escalation)
- Decision logic is separated from analysis logic and executed deterministically
- Decisions are logged and exportable, but are not surfaced in the UI by default

---

## Tech Stack

- Streamlit  
- Google Gemini (`gemini-2.5-flash`)  
- Pandas  
- openpyxl  

---

## Project Status

Phase 1 and Phase 2 complete.  
The system includes a stable analysis layer and a decision layer, and is designed to be extended with persistent memory, automation, or agent-based workflows.