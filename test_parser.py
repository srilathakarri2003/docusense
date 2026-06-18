from app.core.parser import _from_txt


def test_txt_extracts_sentences():
    sample = b"This is the first sentence. Here is another one. And a third sentence follows."
    result = _from_txt(sample)
    assert len(result) >= 1
    assert all("text" in r and "page" in r for r in result)

def test_txt_filters_short():
    sample = b"Hi. This sentence is long enough to pass the filter threshold."
    result = _from_txt(sample)
    # "Hi." should be filtered (< 20 chars)
    assert all(len(r["text"]) > 20 for r in result)
