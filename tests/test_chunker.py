import pytest

from rag_agent.chunker import chunk_documents, chunk_text
from rag_agent.loader import Document


def test_short_text_is_one_chunk():
    assert chunk_text("one two three", size=10, overlap=2) == ["one two three"]


def test_chunks_overlap():
    words = " ".join(str(n) for n in range(10))  # "0 1 2 ... 9"
    chunks = chunk_text(words, size=4, overlap=1)
    assert chunks[0] == "0 1 2 3"
    assert chunks[1] == "3 4 5 6"  # starts with the last word of chunk 0


def test_every_word_is_covered():
    words = [str(n) for n in range(23)]
    chunks = chunk_text(" ".join(words), size=5, overlap=2)
    covered = {w for c in chunks for w in c.split()}
    assert covered == set(words)


def test_overlap_must_be_smaller_than_size():
    with pytest.raises(ValueError):
        chunk_text("a b c", size=3, overlap=3)


def test_chunk_documents_keeps_source():
    docs = [Document(source="a.md", text="x " * 20)]
    chunks = chunk_documents(docs, size=10, overlap=0)
    assert [c.source for c in chunks] == ["a.md", "a.md"]
    assert [c.index for c in chunks] == [0, 1]
