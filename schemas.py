from pydantic import BaseModel
from typing import Any


class SectionSummary(BaseModel):
    heading: str
    summary: list[str]
    page_range: list[int]


class KeyFact(BaseModel):
    sentence: str
    page: int
    section: str = "Document"


class SummaryResponse(BaseModel):
    executive_summary: str
    sections: list[SectionSummary]
    key_facts: list[KeyFact]
    metadata: dict[str, Any]
