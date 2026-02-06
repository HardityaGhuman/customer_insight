# Customer Insight Dashboard

Customer Insight Dashboard is a Streamlit based application for analyzing customer reviews and converting unstructured feedback into structured business insights.

The project focuses on building a **reliable, extensible analysis pipeline** rather than UI polish or model experimentation.

---

## Live Demo

https://customerinsight-kuamgpzt4v4dmearadxzus.streamlit.app/

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
- Persists decisions and system state for auditability
- Allows exporting results as:
  - CSV
  - Excel
  - Markdown
  - JSON (for programmatic use)

---

## Architecture Overview

The system is built in progressive phases with clear control boundaries:

- **LLM**: Used only for reasoning and structured intent generation
- **Code**: Validates outputs, enforces rules, and executes actions
- **Storage**: Acts as the source of truth for decisions and state

### Phase Breakdown

- **Phase 1 — Analysis**
  - Converts raw reviews into structured insights
  - Enforces strict JSON schemas
  - Includes deterministic fallback when the model fails

- **Phase 2 — Decision Making**
  - Uses structured analysis to derive issue category and escalation level
  - Validates all decisions deterministically
  - Separates reasoning from execution

- **Phase 3.1 — Persistence & State**
  - Introduces SQLite backed persistence
  - Stores:
    - Decision logs (audit trail)
    - Current system state (issue counts, escalation status)
  - Ensures system behavior is consistent across restarts
  - LLMs are never used for memory or state

---

## Tech Stack

- Streamlit
- Google Gemini (`gemini-2.5-flash`)
- Pandas
- openpyxl
- SQLite

---

## Project Status

Phase 3.1 complete.

The system now includes:
- Structured analysis
- Deterministic decision-making
- Persistent state and audit logs

The project is designed to be extended with stronger consistency guarantees, automation, and controlled agentic behavior in later phases.