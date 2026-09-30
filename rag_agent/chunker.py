"""Split documents into small, overlapping chunks."""
from dataclasses import dataclass

from rag_agent.loader import Document


@dataclass
class Chunk:
    source: str
    index: int  # position of the chunk within its document
    text: str


def chunk_text(text: str, size: int = 150, overlap: int = 30) -> list[str]:
    """Split text into chunks of `size` words; neighbours share `overlap` words."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    words = text.split()
    chunks = []
    step = size - overlap
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + size]))
        if start + size >= len(words):
            break
    return chunks


def chunk_documents(docs: list[Document], size: int = 150, overlap: int = 30) -> list[Chunk]:
    """Chunk every document, keeping track of where each chunk came from."""
    return [
        Chunk(source=doc.source, index=i, text=piece)
        for doc in docs
        for i, piece in enumerate(chunk_text(doc.text, size, overlap))
    ]
