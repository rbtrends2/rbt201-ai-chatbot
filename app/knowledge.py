"""Small deterministic knowledge loader and lexical retriever."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

WORD_PATTERN = re.compile(r"[a-z0-9][a-z0-9'-]{1,}", re.IGNORECASE)


@dataclass(frozen=True)
class DocumentChunk:
    """A retrievable piece of a Markdown knowledge source."""

    source: str
    title: str
    text: str
    terms: frozenset[str]


def _terms(text: str) -> frozenset[str]:
    """Extract normalized search terms from text."""
    return frozenset(match.group(0).lower() for match in WORD_PATTERN.finditer(text))


def load_documents(directory: Path) -> tuple[DocumentChunk, ...]:
    """Load Markdown paragraphs from a local knowledge directory."""
    chunks: list[DocumentChunk] = []
    for path in sorted(directory.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        title = next(
            (
                line.removeprefix("# ").strip()
                for line in text.splitlines()
                if line.startswith("# ")
            ),
            path.stem.replace("-", " ").title(),
        )
        for block in (part.strip() for part in text.split("\n\n")):
            if not block or block.startswith("#"):
                continue
            chunks.append(
                DocumentChunk(
                    source=path.name,
                    title=title,
                    text=block,
                    terms=_terms(block),
                )
            )
    return tuple(chunks)


def retrieve(
    question: str,
    documents: tuple[DocumentChunk, ...],
    limit: int = 3,
) -> tuple[DocumentChunk, ...]:
    """Return the highest-overlap chunks for a question."""
    query_terms = _terms(question)
    if not query_terms:
        return ()

    ranked = [
        (len(query_terms.intersection(document.terms)), document)
        for document in documents
    ]
    ranked.sort(key=lambda item: (-item[0], item[1].source, item[1].text))
    return tuple(document for score, document in ranked[:limit] if score > 0)
