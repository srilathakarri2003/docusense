import time
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from app.core.parser import extract_text
from app.core.segmenter import segment_sections
from app.core.ranker import rank_sentences
from app.utils.text import extract_key_facts, build_executive_summary
from app.models.schemas import SummaryResponse

router = APIRouter()

@router.post("/summarize", response_model=SummaryResponse)
async def summarize(
    file: UploadFile = File(...),
    top_n: int = Query(3, ge=1, le=10, description="Sentences per section"),
    min_section_len: int = Query(2, ge=1, description="Min sentences before summarizing"),
):
    start = time.time()
    content = await file.read()
    filename = file.filename or "document"
    ext = filename.rsplit(".", 1)[-1].lower()

    if ext not in {"pdf", "docx", "txt"}:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: .{ext}")

    sentences = extract_text(content, ext)
    if not sentences:
        raise HTTPException(status_code=422, detail="Could not extract text from document.")

    sections = segment_sections(sentences)
    summarized = []
    all_top = []

    for section in sections:
        if len(section["sentences"]) < min_section_len:
            continue
        top = rank_sentences(section["sentences"], top_n=top_n)
        summarized.append({
            "heading": section["heading"],
            "summary": [f"{s['text']} (p.{s['page']})" for s in top],
            "page_range": [section["sentences"][0]["page"], section["sentences"][-1]["page"]],
        })
        all_top.extend(top)

    key_facts = extract_key_facts(sentences)
    executive_summary = build_executive_summary(all_top, top_n=5)
    elapsed_ms = int((time.time() - start) * 1000)

    return SummaryResponse(
        executive_summary=executive_summary,
        sections=summarized,
        key_facts=key_facts,
        metadata={
            "filename": filename,
            "total_pages": max((s["page"] for s in sentences), default=1),
            "sections_detected": len(summarized),
            "processing_time_ms": elapsed_ms,
        },
    )
