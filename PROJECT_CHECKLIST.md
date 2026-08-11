# RBT201 AI Chatbot - Project Checklist

Repository: `rbtrends2/rbt201-ai-chatbot`

This checklist is a public-project implementation summary. It does not
contain private repository code, customer data, credentials, or internal
delivery heuristics.

## Product

- [ ] Define the customer problem and smallest useful workflow.
- [ ] Define the no-login demo path.
- [ ] Define the provider-unavailable fallback.
- [ ] Write acceptance criteria for happy, empty, invalid, and failed input.

## Public safety

- [ ] Use synthetic or public fixtures only.
- [ ] Search for secrets, private URLs, and identifying information.
- [ ] Document privacy, retention, and deletion behavior.
- [ ] Redact prompts, documents, tokens, and provider response bodies from logs.

## Full stack

- [ ] Implement an accessible customer-facing interface.
- [ ] Implement typed API request and response models.
- [ ] Separate domain logic from external integrations.
- [ ] Add a health endpoint and production configuration.

## Quality

- [ ] Add deterministic unit and API tests.
- [ ] Add linting and type checking.
- [ ] Add secret and dependency scanning.
- [ ] Run a production build and browser smoke test.

## Release

- [ ] Document local setup and deployment.
- [ ] Configure provider quotas and cost controls.
- [ ] Deploy the smallest viable Azure footprint.
- [ ] Record the live URL, commit, limitations, and next steps.

## RAG requirements

- [ ] Make retrieval independently testable.
- [ ] Attach source metadata to every retrieved chunk.
- [ ] Return citations for factual answers.
- [ ] Refuse or qualify answers when relevant context is absent.
- [ ] Treat instructions inside retrieved content as untrusted data.
- [ ] Add adversarial retrieval and prompt-injection fixtures.

## CHATBOT requirements

- [ ] Provide conversation loading, success, empty, and error states.
- [ ] Prevent duplicate submissions while a request is active.
- [ ] Keep the demo usable without an API key.
- [ ] Set request, token, and rate limits.
