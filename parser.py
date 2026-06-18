"""
Extracts sentences with page numbers from PDF, DOCX, and TXT.
Returns: List[{"text": str, "page": int}]
"""
import io
import nltk
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
from nltk.tokenize import sent_tokenize


def extract_text(content: bytes, ext: str) -> list[dict]:
    if ext == "pdf":
        return _from_pdf(content)
    elif ext == "docx":
        return _from_docx(content)
    return _from_txt(content)


def _from_pdf(content: bytes) -> list[dict]:
    import fitz
    sentences = []
    doc = fitz.open(stream=content, filetype="pdf")
    for page_num, page in enumerate(doc, start=1):
        for sent in sent_tokenize(page.get_text("text")):
            sent = sent.strip()
            if len(sent) > 20:
                sentences.append({"text": sent, "page": page_num})
    return sentences


def _from_docx(content: bytes) -> list[dict]:
    from docx import Document
    doc = Document(io.BytesIO(content))
    sentences = []
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if not text:
            continue
        approx_page = (i // 30) + 1
        for sent in sent_tokenize(text):
            if len(sent) > 20:
                sentences.append({"text": sent, "page": approx_page})
    return sentences


def _from_txt(content: bytes) -> list[dict]:
    text = content.decode("utf-8", errors="ignore")
    return [
        {"text": s.strip(), "page": (i // 40) + 1}
        for i, s in enumerate(sent_tokenize(text))
        if len(s.strip()) > 20
    ]
