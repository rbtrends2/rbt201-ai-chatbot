"""FastAPI application for the RBT201 AI chatbot."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.knowledge import load_documents
from app.models import ChatRequest, ChatResponse, KnowledgeSource
from app.providers import (
    DemoProvider,
    OpenAICompatibleProvider,
    ProviderUnavailable,
)
from app.service import RAGService

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge"
settings = get_settings()
documents = load_documents(KNOWLEDGE_DIR)

if settings.ai_provider == "openai_compatible":
    answer_provider = OpenAICompatibleProvider(settings)
else:
    answer_provider = DemoProvider()

rag_service = RAGService(
    documents=documents,
    provider=answer_provider,
    max_context_chars=settings.max_context_chars,
)

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
app.mount("/assets", StaticFiles(directory=STATIC_DIR), name="assets")


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    """Serve the customer-facing application."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
async def health() -> dict[str, object]:
    """Return service readiness without exposing configuration secrets."""
    return {
        "status": "ok",
        "provider": answer_provider.name,
        "knowledge_sources": len(
            {document.source for document in rag_service.documents}
        ),
    }


@app.get("/api/knowledge", response_model=list[KnowledgeSource])
async def knowledge() -> list[KnowledgeSource]:
    """Return public source metadata."""
    sources = {
        document.source: KnowledgeSource(
            source=document.source,
            title=document.title,
        )
        for document in rag_service.documents
    }
    return [sources[source] for source in sorted(sources)]


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Retrieve context and answer a customer question."""
    try:
        return await rag_service.answer(request.question)
    except ProviderUnavailable as exc:
        raise HTTPException(
            status_code=503,
            detail="The AI provider is unavailable. Try demo mode later.",
        ) from exc
