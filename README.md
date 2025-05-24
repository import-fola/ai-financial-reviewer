# AI Financial Reviewer

A project that uses AI to analyze and review financial data and statements.

## Features
- Financial document analysis (CSV, PDF, PNG/JPG)
- Automated extraction, transformation, and upload to Google Sheets
- Model-agnostic LLM/OCR (Claude, GPT-4, Gemini, etc.)
- Google OAuth authentication
- Data preview and confirmation before upload
- Deduplication and formula propagation
- Observability with structured logs and Sentry

## Tech Stack
- Python 3.12
- Streamlit (Frontend)
- FastAPI (Backend)
- gspread, Google-auth (Sheets integration)
- OpenAI (`openai`), Anthropic Claude (`anthropic`), Google Gemini (`google-genai`) (LLM/OCR)
- pdfplumber, pytesseract (fallback extractors)
- Sentry (error tracking)

> **Note:**
> - For full feature support (including vision/multimodal), the project uses the official SDKs for each provider: `openai` (OpenAI), `anthropic` (Claude), and `google-genai` (Gemini).
> - You may also use OpenAI-compatible endpoints (e.g., via OpenRouter or provider endpoints) for basic text tasks, but some advanced features may not be available.

## Project Structure

```
ai_financial_reviewer/
│
├── app.py                # Main entrypoint (to be replaced by Streamlit UI)
├── src/
│   ├── auth.py           # Google OAuth, token management
│   ├── upload.py         # File upload, validation, queue
│   ├── extract/
│   │   ├── base_llm_extractor.py
│   │   ├── gpt4_extractor.py
│   │   ├── claude_extractor.py
│   │   ├── gemini_extractor.py
│   │   ├── pdf_extractor.py
│   │   ├── image_extractor.py
│   ├── transform.py      # Schema mapping, deduplication
│   ├── sheets.py         # Google Sheets API, append, lock, formula fill
│   ├── llm.py            # LLM category suggestion
│   ├── observability.py  # Logging, Sentry
│   └── utils.py
├── input_data/           # Sample/test files
├── requirements.txt
├── README.md
└── ...
```

## Setup Instructions

1. **Clone the repository**

```bash
git clone <repo-url>
cd ai_financial_reviewer
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

- Create a `.env` file with your Google OAuth and LLM API keys for OpenAI, Anthropic, and Gemini (google-genai).

4. **Run the application**

- For Streamlit UI:
  ```bash
  streamlit run app.py
  ```
- For FastAPI backend:
  ```bash
  uvicorn src.main:app --reload
  ```

## Sample Data

Sample files for CSV, PDF, and PNG are in the `input_data/` directory for testing extraction and upload.

---

Created by Folajimi Odukomaiya
