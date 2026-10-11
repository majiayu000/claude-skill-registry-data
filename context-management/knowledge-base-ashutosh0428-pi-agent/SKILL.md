---
name: knowledge-base
description: Ground answers in the project's ingested docs via the search_knowledge tool.
trigger: when the user asks about project docs, or a local knowledge base exists
---
## When to use
The user asks how something in *their* project works and a `search_knowledge`
tool is available (a knowledge base was built with `pi ingest`).

## How
1. Call `search_knowledge` with a focused query before answering from general
   knowledge — the project's own docs are the source of truth.
2. Read the returned chunks; each is tagged with its `[source.md]`.
3. Answer using only what the chunks support, and cite the sources in
   `[brackets]` so the user can verify.
4. If retrieval returns nothing relevant, say the knowledge base doesn't cover
   it — don't fill the gap with guesses.

## Avoid
- Answering project-specific questions from memory when a KB exists.
- Dropping citations — an uncited claim is unverifiable.
- Inventing detail beyond what the retrieved chunks state.

## Done well
Every project-specific claim traces to a cited chunk; gaps are stated honestly
rather than hallucinated.
