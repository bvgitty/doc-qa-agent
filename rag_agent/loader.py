"""Load documents (.md, .txt, .pdf) from a folder."""
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

SUPPORTED = {".md", ".txt", ".pdf"}


@dataclass
class Document:
    source: str  # file name, used for citations
    text: str


def read_file(path: Path) -> str:
    """Return the text of one file."""
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return path.read_text(encoding="utf-8")


def load_documents(folder: str) -> list[Document]:
    """Load every supported file in folder (and its subfolders)."""
    docs = []
    for path in sorted(Path(folder).rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED:
            text = read_file(path).strip()
            if text:
                docs.append(Document(source=path.name, text=text))
    return docs
