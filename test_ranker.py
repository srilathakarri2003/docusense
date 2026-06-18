from app.core.ranker import rank_sentences

SENTS = [
    {"text": "The company reported a 42% increase in revenue.", "page": 1},
    {"text": "Weather is unpredictable during monsoon season.", "page": 1},
    {"text": "Revenue growth was driven by enterprise software sales.", "page": 2},
    {"text": "The team expanded to three new markets in Asia.", "page": 2},
    {"text": "Operational costs decreased by 15% year-over-year.", "page": 3},
]

def test_returns_top_n():
    assert len(rank_sentences(SENTS, top_n=3)) == 3

def test_reading_order_preserved():
    result = rank_sentences(SENTS, top_n=3)
    pages = [r["page"] for r in result]
    assert pages == sorted(pages)

def test_single_sentence():
    result = rank_sentences([{"text": "Only one sentence here today.", "page": 1}], top_n=3)
    assert len(result) == 1
