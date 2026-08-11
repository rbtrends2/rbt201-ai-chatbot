"""RAG orchestration service."""

from __future__ import annotations

from collections.abc import Sequence

from app.knowledge import DocumentChunk, retrieve
from app.models import ChatResponse, Citation
from app.providers import AnswerProvider


class RAGService:
    """Retrieve relevant context and produce a cited answer."""

    def __init__(
        self,
        documents: tuple[DocumentChunk, ...],
        provider: AnswerProvider,
        max_context_chars: int = 6000,
    ) -> None:
        self._documents = documents
        self._provider = provider
        self._max_context_chars = max_context_chars

    @property
    def documents(self) -> tuple[DocumentChunk, ...]:
        """Return the loaded documents."""
        return self._documents

    async def answer(self, question: str) -> ChatResponse:
        """Answer a question using only retrieved context."""
        context = retrieve(question, self._documents)
        if not context:
            return ChatResponse(
                answer=(
                    "I could not find relevant information in the demo "
                    "knowledge base. Try a question about RAG, citations, "
                    "privacy, or Azure deployment."
                ),
                citations=[],
                grounded=False,
                provider="none",
            )

        bounded_context = self._bound_context(context)
        answer = await self._provider.answer(question, bounded_context)
        citations = [
            Citation(
                source=chunk.source,
                title=chunk.title,
                excerpt=chunk.text[:240],
            )
            for chunk in bounded_context
        ]
        return ChatResponse(
            answer=answer,
            citations=citations,
            grounded=True,
            provider=self._provider.name,
        )

    def _bound_context(
        self,
        context: Sequence[DocumentChunk],
    ) -> tuple[DocumentChunk, ...]:
        """Keep retrieved context within the configured character budget."""
        selected: list[DocumentChunk] = []
        used_chars = 0
        for chunk in context:
            if used_chars + len(chunk.text) > self._max_context_chars:
                break
            selected.append(chunk)
            used_chars += len(chunk.text)
        return tuple(selected)
