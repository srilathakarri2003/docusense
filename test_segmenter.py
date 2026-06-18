from app.core.segmenter import is_heading, segment_sections


def test_heading_all_caps():
    assert is_heading("EXECUTIVE SUMMARY") is True

def test_heading_titled():
    assert is_heading("1. Background and Motivation") is True

def test_not_heading_period():
    assert is_heading("This is a normal sentence with a period.") is False

def test_not_heading_too_long():
    assert is_heading("A" * 101) is False

def test_segment_two_sections():
    sents = [
        {"text": "Introduction", "page": 1},
        {"text": "This project solves a real problem.", "page": 1},
        {"text": "Methodology", "page": 2},
        {"text": "We used TF-IDF and PageRank.", "page": 2},
    ]
    sections = segment_sections(sents)
    assert len(sections) == 2
    assert sections[0]["heading"] == "Introduction"
    assert sections[1]["heading"] == "Methodology"
