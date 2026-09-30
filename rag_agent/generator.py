"""Ask Claude to answer a question using only the retrieved chunks."""
import os

import anthropic

from rag_agent.chunker import Chunk

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = (
    "You answer questions using ONLY the provided context excerpts. "
    "Cite the sources you used in square brackets, like [notes.md#2]. "
    "If the context does not contain the answer, say you don't know."
)


def build_prompt(question: str, chunks: list[Chunk]) -> str:
    """Put the retrieved excerpts and the question into one message."""
    context = "\n\n".join(
        f"[{c.source}#{c.index}]\n{c.text}" for c in chunks
    )
    return f"Context excerpts:\n\n{context}\n\nQuestion: {question}"


def answer(question: str, chunks: list[Chunk], client=None) -> str:
    """Send the prompt to Claude and return its answer text."""
    client = client or anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    response = client.messages.create(
        model=os.environ.get("RAG_MODEL", DEFAULT_MODEL),
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(question, chunks)}],
    )
    return response.content[0].text
