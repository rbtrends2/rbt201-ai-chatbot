# RBT201 AI Chatbot

A small, public RAG chatbot that answers questions from a curated knowledge
set, cites the supporting sources, and works in demo mode without an AI API
key.

## Why this project exists

This repository demonstrates a complete, customer-facing vertical slice:

- accessible browser interface;
- typed FastAPI API;
- independently testable retrieval;
- provider abstraction with a deterministic fallback;
- source citations;
- tests, CI, Docker, and Azure-friendly configuration.

The bundled knowledge is synthetic and educational. Do not upload confidential
documents to an unreviewed deployment.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows activation:

```text
.venv\Scripts\activate
```

Open `http://127.0.0.1:8000`.

The default `AI_PROVIDER=demo` mode uses retrieval plus a deterministic answer
composer. To use an OpenAI-compatible provider, set the variables in
`.env.example` in a local `.env` file. Never commit that file or expose the
provider key in browser code.

## API

- `GET /api/health` - service and knowledge-base status
- `GET /api/knowledge` - public source metadata
- `POST /api/chat` - retrieve context and generate a cited answer

Example request:

```json
{
  "question": "What makes a RAG answer trustworthy?"
}
```

## Architecture

```text
Browser
  -> FastAPI routes
      -> RAG service
          -> local Markdown knowledge chunks
          -> demo provider or OpenAI-compatible provider
      -> cited response
```

The provider boundary is intentionally small so retrieval, API behavior, and
the demo path can be tested without network calls.

## Testing and quality

```bash
python -m pytest
ruff check .
```

The GitHub Actions workflow runs tests and linting on pushes and pull requests.

## Azure deployment direction

The application is container-ready and can run on Azure App Service or Azure
Container Apps. A production deployment should add:

- Azure Key Vault and Managed Identity for provider credentials;
- Application Insights with redacted structured logs;
- a managed database or Azure AI Search when the knowledge set needs to grow;
- authentication, quotas, retention, and deletion before accepting customer
  documents;
- a budget alert for provider usage.

## Privacy and limitations

- Demo content is not a substitute for professional advice.
- The starter app does not provide multi-user authentication.
- The demo rate limit is intentionally minimal; production deployments should
  use a distributed limiter.
- The bundled retriever is lexical. Replace it with embeddings or Azure AI
  Search when recall requirements justify the additional cost and complexity.

## License

MIT. See [LICENSE](LICENSE).
