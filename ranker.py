"""
TF-IDF + TextRank sentence ranking (per section).
Each section is ranked independently — short but important sections
(e.g. an executive summary or scope statement) aren't drowned out by long ones.
"""
import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rank_sentences(sentences: list[dict], top_n: int = 3) -> list[dict]:
    texts = [s["text"] for s in sentences]
    if len(texts) == 1:
        return sentences[:top_n]

    try:
        tfidf = TfidfVectorizer(stop_words="english").fit_transform(texts)
    except ValueError:
        return sentences[:top_n]

    sim = cosine_similarity(tfidf)
    np.fill_diagonal(sim, 0)

    scores = nx.pagerank(nx.from_numpy_array(sim), max_iter=200)
    top_idx = sorted(
        [i for i, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]]
    )
    return [sentences[i] for i in top_idx]
