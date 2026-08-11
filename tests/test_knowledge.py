from pathlib import Path

from app.knowledge import load_documents, retrieve


def test_retrieve_returns_relevant_source() -> None:
    knowledge_dir = Path(__file__).resolve().parents[1] / "data" / "knowledge"
    documents = load_documents(knowledge_dir)

    results = retrieve("How should a RAG system show evidence?", documents)

    assert results
    assert results[0].source == "rag-basics.md"


def test_retrieve_returns_no_context_for_unknown_terms() -> None:
    knowledge_dir = Path(__file__).resolve().parents[1] / "data" / "knowledge"
    documents = load_documents(knowledge_dir)

    assert retrieve("xylophone nebula quantum", documents) == ()
