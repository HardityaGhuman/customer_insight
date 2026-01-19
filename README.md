# Customer Insight AI

Customer Insight AI is a lightweight Streamlit application that analyzes customer reviews using large language models to generate structured, actionable business insights.

The project focuses on practical text analysis, real-world data handling, and clear decision-oriented outputs rather than heavy visualizations.

---

## Overview

This application allows users to:
- Input raw customer reviews (text or CSV/Excel)
- Perform AI-powered sentiment analysis using Google Gemini
- Extract key customer pain points and themes
- Generate actionable business recommendations
- Export insights for reporting and documentation

---

## Features

- AI-powered sentiment and feedback analysis
- Text input and CSV/Excel upload support
- Structured insight generation (sentiment, pain points, recommendations)
- Export results as CSV, Excel, or Markdown
- Simple, clean dashboard focused on insights

---

## Tech Stack

- Frontend: Streamlit
- Language Model: Google Gemini (gemini-2.5-flash)
- Data Processing: Pandas
- Exports: CSV, Excel (openpyxl), Markdown

---

## Installation

1. Clone the repository:
   git clone https://github.com/yourusername/customer-insight.git
   cd customer-insight

2. Install dependencies:
   pip install -r requirements.txt

3. Configure API key:

   Create `.streamlit/secrets.toml` and add:
   GEMINI_API_KEY = "your-api-key-here"

4. Run the application:
   streamlit run app.py

5. Open in browser:
   http://localhost:8501

---

## Usage

### Text Input
- Navigate to Dashboard
- Enter customer reviews (one per line)
- Click Analyze Reviews
- View AI-generated insights
- Export results if required

### File Upload
- Upload a CSV or Excel file containing customer reviews
- Select the column containing review text
- Analyze and export insights

---

## Project Structure

customer-insight/
├── app.py
├── pages/
│   └── dashboard.py
├── utils/
│   ├── analyzer.py
│   └── exporter.py
├── .streamlit/
│   └── secrets.toml
├── requirements.txt
└── README.md

---

## Notes

This project is designed to demonstrate:
- Practical NLP usage
- LLM-driven business insight extraction
- End-to-end ML-powered application development

---

## License

MIT License