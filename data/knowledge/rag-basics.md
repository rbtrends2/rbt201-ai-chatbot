# RAG Basics

Retrieval-augmented generation, or RAG, retrieves relevant source content
before asking a language model to draft an answer. Retrieval gives the model
task-specific context instead of requiring every fact to be stored in model
weights.

Good RAG systems preserve source metadata, limit the context passed to the
model, and show citations so a user can inspect the evidence behind an answer.

A useful fallback is to return a clear source-based summary when the language
model is unavailable. This keeps the product testable and avoids pretending
that an unavailable model produced an answer.
