from rag_agent.chunker import Chunk
from rag_agent.retriever import BM25Retriever, tokenize

CHUNKS = [
    Chunk("git.md", 0, "git rebase replays commits onto a new base"),
    Chunk("git.md", 1, "git revert adds a new commit that undoes an old one"),
    Chunk("pages.md", 0, "GitHub Pages hosts a static website from a repository"),
]


def test_tokenize_lowercases_and_drops_punctuation():
    assert tokenize("Hello, GitHub Pages!") == ["hello", "github", "pages"]


def test_best_match_comes_first():
    top_chunk, _ = BM25Retriever(CHUNKS).search(
        "how does revert work?", k=1)[0]
    assert top_chunk.text.startswith("git revert")


def test_unrelated_query_returns_nothing():
    assert BM25Retriever(CHUNKS).search("banana smoothie") == []


def test_k_limits_results():
    assert len(BM25Retriever(CHUNKS).search("git commit", k=1)) == 1
