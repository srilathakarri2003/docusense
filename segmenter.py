"""
Splits a flat sentence list into sections using heading-detection heuristics.
Heading signals: short, title/ALL-CAPS, no terminal punctuation, optional numbering.
Tradeoff: regex-based, not ML — unusual formatting may cause splits to fail.
"""
import re

HEADING_PATTERN = re.compile(r'^(\d+[\.\)]\s+)?[A-Z][^\.\?!]{0,80}$')


def is_heading(text: str) -> bool:
    t = text.strip()
    if len(t) > 100 or t.endswith(('.', '?', '!')):
        return False
    if t.isupper() and len(t.split()) <= 8:
        return True
    if HEADING_PATTERN.match(t) and t[0].isupper():
        return True
    return False


def segment_sections(sentences: list[dict]) -> list[dict]:
    sections = []
    current_heading = "Document"
    current_sentences = []

    for s in sentences:
        if is_heading(s["text"]):
            if current_sentences:
                sections.append({"heading": current_heading, "sentences": current_sentences})
            current_heading = s["text"]
            current_sentences = []
        else:
            current_sentences.append(s)

    if current_sentences:
        sections.append({"heading": current_heading, "sentences": current_sentences})

    return sections
