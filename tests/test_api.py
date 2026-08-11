from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_serves_customer_ui() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Grounded chat" in response.text


def test_health_endpoint() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_returns_citations() -> None:
    response = client.post(
        "/api/chat",
        json={"question": "What makes a RAG answer trustworthy?"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["grounded"] is True
    assert payload["citations"]
    assert payload["provider"] == "demo"


def test_knowledge_endpoint_returns_source_metadata() -> None:
    response = client.get("/api/knowledge")

    assert response.status_code == 200
    assert {item["source"] for item in response.json()} == {
        "azure-deployment.md",
        "privacy.md",
        "rag-basics.md",
    }


def test_chat_reports_missing_context() -> None:
    response = client.post(
        "/api/chat",
        json={"question": "xylophone nebula quantum"},
    )

    assert response.status_code == 200
    assert response.json()["grounded"] is False
