"""Find the chunks most relevant to a question, using the BM25 ranking formula."""
import math
import re
from collections import Counter

from rag_agent.chunker import Chunk


def tokenize(text: str) -> list[str]:
    """Lowercase words, ignoring punctuation."""
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25Retriever:
    """Classic keyword search: rewards chunks that contain the question's
    rarer words, several times, without being overly long."""

    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1, self.b = k1, b
        self.tokens = [tokenize(c.text) for c in chunks]
        self.avg_len = sum(len(t) for t in self.tokens) / max(len(chunks), 1)
        # document frequency: in how many chunks does each word appear?
        df = Counter(word for toks in self.tokens for word in set(toks))
        n = len(chunks)
        self.idf = {w: math.log(1 + (n - f + 0.5) / (f + 0.5))
                    for w, f in df.items()}

    def score(self, query_words: list[str], i: int) -> float:
        counts = Counter(self.tokens[i])
        length = len(self.tokens[i])
        total = 0.0
        for word in query_words:
            if word not in counts:
                continue
            tf = counts[word]
            norm = tf + self.k1 * (1 - self.b + self.b * length / self.avg_len)
            total += self.idf[word] * tf * (self.k1 + 1) / norm
        return total

    def search(self, query: str, k: int = 4) -> list[tuple[Chunk, float]]:
        """Return the top k (chunk, score) pairs, best first. Zero scores are dropped."""
        words = tokenize(query)
        scored = [(self.chunks[i], self.score(words, i))
                  for i in range(len(self.chunks))]
        scored = [pair for pair in scored if pair[1] > 0]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return scored[:k]
