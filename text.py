"""
Key-fact extraction: surfaces sentences with numbers, percentages, dates, currency.
Executive summary: top N sentences from across all sections.
"""
import re

KEY_FACT_RE = re.compile(
    r'(\b\d{1,3}(?:,\d{3})*(?:\.\d+)?%?\b'
    r'|\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\b'
    r'|\b\d{4}\b|\$[\d,]+)',
    re.IGNORECASE,
)


def extract_key_facts(sentences: list[dict], section: str = "Document") -> list[dict]:
    facts = [
        {"sentence": s["text"], "page": s["page"], "section": section}
        for s in sentences
        if KEY_FACT_RE.search(s["text"])
    ]
    return facts[:20]


def build_executive_summary(top_sentences: list[dict], top_n: int = 5) -> str:
    return " ".join(s["text"] for s in top_sentences[:top_n])
