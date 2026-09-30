from types import SimpleNamespace

from rag_agent.chunker import Chunk
from rag_agent.generator import answer, build_prompt

CHUNKS = [
    Chunk("notes.md", 2, "A fork is a copy of a repository under your account.")]


def test_prompt_contains_citation_label_and_question():
    prompt = build_prompt("What is a fork?", CHUNKS)
    assert "[notes.md#2]" in prompt
    assert "What is a fork?" in prompt


class FakeClient:
    """Stands in for anthropic.Anthropic so tests need no API key or network."""

    def __init__(self):
        self.messages = self
        self.last_call = None

    def create(self, **kwargs):
        self.last_call = kwargs
        return SimpleNamespace(content=[SimpleNamespace(text="A copy [notes.md#2]")])


def test_answer_uses_client_and_returns_text():
    client = FakeClient()
    result = answer("What is a fork?", CHUNKS, client=client)
    assert result == "A copy [notes.md#2]"
    assert "What is a fork?" in client.last_call["messages"][0]["content"]
