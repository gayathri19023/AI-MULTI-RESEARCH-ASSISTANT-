# AI Multi-Agent Research Assistant

An end-to-end college project that coordinates specialized agents to collect web and academic sources, analyze uploaded documents, compare evidence, assess source-derived claims, identify potential gaps, generate citations, and export a structured report.

## Features

- LangGraph workflow: manager, web, academic, document, data, comparison, fact-checking, gap, citation, and report agents.
- Live web search through DuckDuckGo Instant Answers and academic search through Semantic Scholar when available.
- Clearly labelled local Demo Mode for offline demonstrations; it never claims sample data is live research.
- PDF, DOCX, and TXT document extraction with validation and a 10 MB file limit.
- SQLite history using SQLAlchemy with sessions, sources, documents, agent results, claims, gaps, and reports tables.
- Transparent status, source cards, claim table, comparisons, citations, and PDF/DOCX download in Streamlit.

## Project Structure

`app.py` is the Streamlit interface. `agents/` contains specialized stages, `workflows/` contains the LangGraph graph, `services/` owns integrations and exports, `database/` owns SQLite persistence, `utils/` contains shared validation, and `tests/` provides smoke coverage.

## Installation on Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

Use Python 3.11 or newer. The app initializes `data/research.db` automatically.

## Environment Variables

Set `OPENAI_API_KEY` only if extending the agents with an LLM provider. `SEARCH_API_KEY` is reserved for alternate search providers. No secret is hard-coded or stored in SQLite. `DEMO_MODE=true` enables the local sample dataset.

## Using the Application

1. Open **New Research** and enter a question.
2. Select Demo Mode for a key-free demonstration or disable it for public API searches.
3. Optionally upload PDF, DOCX, or TXT evidence.
4. Review results, agent status, sources, fact checks, comparisons, potential gaps, and citations.
5. Download the structured report as PDF or DOCX. Potential gaps and claim statuses are intentionally cautious; full-text validation is not implied by metadata.

## Testing

```powershell
pytest -q
python -m compileall .
```

## Troubleshooting

- If public search is unavailable, use Demo Mode and read the clearly displayed warning.
- Configure keys in `.env`; never paste them into source code.
- A scanned or image-only PDF may have no extractable text. Upload a text-readable PDF or OCR it first.

## Future Enhancements

Add authenticated search providers, source full-text retrieval where licensed, human claim-review workflows, and user accounts.

## HOW TO RUN THE PROJECT

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```
