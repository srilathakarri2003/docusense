# DocuSense — Offline Extractive Document Summarizer

A backend that summarizes long PDFs, DOCX, and TXT files **without any LLM API calls**.  
Every output sentence is copied verbatim from the source — no hallucinations, fully auditable, free to run.

## How it works

```
Document → Section Detection → Per-Section TF-IDF + TextRank → Three-tier Output
```

1. **Parse** — PyMuPDF / python-docx extracts text with page numbers
2. **Segment** — Regex heuristics detect headings and split into sections
3. **Rank** — Each section is independently ranked via TF-IDF cosine similarity + NetworkX PageRank
4. **Output** — Three layers: executive summary · per-section summaries · key facts (numbers/dates/currencies)

> Every sentence in the output carries the page number it came from.

## Why not an LLM?

| | This project | LLM-based |
|---|---|---|
| Cost | Free | Per-token cost |
| Latency (100-page doc) | ~2s | 30–120s |
| Hallucination risk | Zero (extractive) | Always present |
| Deterministic | Yes | No |
| Offline | Yes | No |

**Known tradeoff:** Heading detection is regex/heuristic-based. Unusual formatting may cause incorrect section splits — deliberate scope decision.

## Stack

- **FastAPI** — REST API
- **PyMuPDF** — PDF text + page number extraction
- **scikit-learn** — TF-IDF vectorization
- **NetworkX** — PageRank-based sentence ranking (TextRank)
- **NLTK** — Sentence tokenization
- **python-docx** — DOCX support

## Quickstart

```bash
git clone https://github.com/yourusername/docusense.git
cd docusense
pip install -r requirements.txt
python -m nltk.downloader punkt
uvicorn app.main:app --reload
```

API docs at `http://localhost:8000/docs`

## API

### `POST /summarize`

```json
// Request (multipart/form-data)
file: <PDF | DOCX | TXT>
top_n: 3          // sentences per section (default: 3)
min_section_len: 2 // min sentences to summarize a section (default: 2)

// Response
{
  "executive_summary": "...",
  "sections": [
    {
      "heading": "Introduction",
      "summary": ["sentence (p.1)", "sentence (p.2)"],
      "page_range": [1, 3]
    }
  ],
  "key_facts": [
    { "sentence": "Revenue grew 42% in Q3.", "page": 7, "section": "Financial Results" }
  ],
  "metadata": {
    "filename": "report.pdf",
    "total_pages": 24,
    "sections_detected": 8,
    "processing_time_ms": 1840
  }
}
```

### `GET /health`
Returns `{ "status": "ok" }`

## Project structure

```
docusense/
├── app/
│   ├── main.py          # FastAPI app + routes
│   ├── api/
│   │   └── routes.py    # /summarize endpoint
│   ├── core/
│   │   ├── parser.py    # PDF/DOCX/TXT extraction
│   │   ├── segmenter.py # Heading detection + section splitting
│   │   └── ranker.py    # TF-IDF + TextRank ranking
│   ├── models/
│   │   └── schemas.py   # Pydantic request/response models
│   └── utils/
│       └── text.py      # Key-fact detection, cleaning helpers
├── tests/
│   ├── test_parser.py
│   ├── test_segmenter.py
│   └── test_ranker.py
├── sample_docs/         # Test PDFs/DOCX for manual testing
├── requirements.txt
├── .gitignore
└── README.md
```

## Running tests

```bash
pytest tests/ -v
```
