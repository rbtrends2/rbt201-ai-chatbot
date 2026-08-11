"""Typed API and domain models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Citation(BaseModel):
    """A source excerpt supporting an answer."""

    source: str
    title: str
    excerpt: str


class ChatRequest(BaseModel):
    """A user question submitted to the chatbot."""

    question: str = Field(min_length=2, max_length=1000)


class ChatResponse(BaseModel):
    """A cited answer returned by the chatbot."""

    answer: str
    citations: list[Citation]
    grounded: bool
    provider: str


class KnowledgeSource(BaseModel):
    """Public metadata for a knowledge source."""

    source: str
    title: str
