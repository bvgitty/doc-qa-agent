"""Command line: python -m rag_agent --docs docs "your question"
Leave out the question to chat interactively."""
import argparse
import os

from dotenv import load_dotenv

from rag_agent.chunker import chunk_documents
from rag_agent.generator import answer
from rag_agent.loader import load_documents
from rag_agent.retriever import BM25Retriever


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ask questions about your documents.")
    parser.add_argument("question", nargs="?",
                        help="question to ask (omit for chat mode)")
    parser.add_argument("--docs", default="docs",
                        help="folder of .md/.txt/.pdf files")
    parser.add_argument("-k", type=int, default=4,
                        help="number of chunks to retrieve")
    parser.add_argument("--show-sources", action="store_true",
                        help="print retrieved chunks")
    args = parser.parse_args()

    load_dotenv(override=True)  # read .env; it wins over system variables
    if not os.environ.get("ANTHROPIC_API_KEY"):
        parser.error("set the ANTHROPIC_API_KEY environment variable first")

    docs = load_documents(args.docs)
    if not docs:
        parser.error(f"no .md, .txt or .pdf files found in '{args.docs}'")
    chunks = chunk_documents(docs)
    retriever = BM25Retriever(chunks)
    print(f"Loaded {len(docs)} documents as {len(chunks)} chunks.\n")

    def ask(question: str) -> None:
        results = retriever.search(question, k=args.k)
        if not results:
            print("No relevant passages found.\n")
            return
        if args.show_sources:
            for chunk, score in results:
                print(f"  [{chunk.source}#{chunk.index}] score={score:.2f}")
            print()
        print(answer(question, [chunk for chunk, _ in results]), "\n")

    if args.question:
        ask(args.question)
        return
    print("Ask a question (or type 'quit').")
    while (question := input("> ").strip()).lower() not in {"quit", "exit", "q"}:
        if question:
            ask(question)


if __name__ == "__main__":
    main()
