---
name: query
description: Answer questions from Emma's llmwiki vault using its tuned retrieval stack — keyword search, the AutoRAG ask pipeline, and optional LightRAG knowledge-graph context. Use when the user says /query, "ask the wiki", "what does my wiki/vault say about X", or wants an answer grounded in previously ingested vault knowledge rather than the live web.
---

# Query the llmwiki vault

Vault root: `/mnt/c/Users/emmaj/llmwiki`; CLI: `llmwiki` (on PATH; engines in `.rag/`, needs ollama serving qwen2.5:7b + nomic-embed-text).

## Workflow

1. **Locate** — `llmwiki search "<terms>"`: instant keyword scan, returns scored vault paths. Run this first; it tells you whether the vault covers the topic at all.
2. **Read** — open the top hit pages directly (they are small markdown files). For a factual question, reading 1–3 pages usually beats the generator and gives exact quotes plus frontmatter `sources:` for citation.
3. **Ask** — `llmwiki ask "<question>"`: the AutoRAG-tuned pipeline (hybrid BM25+vector retrieval → local LLM). Use for synthesis questions spanning several pages, or when the user wants the pipeline's own answer. Takes ~10–60s.
4. **Graph context** — append `--context` to `ask` when the question is relational ("how does X connect to Y", entity inventories): it adds LightRAG knowledge-graph entities/relations. The graph covers only explicitly-graphed subsets (`llmwiki graph <path>` grows it); absence of graph hits is not absence of knowledge.
5. **Answer honestly** — the pipeline refusing ("context does not contain...") means the vault lacks the page, not that the answer doesn't exist. Say so and offer /ingest to close the gap.

## Notes

- Cite vault pages by relative path (`wiki/concepts/modding/Meatballing.md`) so the user can open them in Obsidian.
- `ask` retrieves from trial-time indexes: pages added since the last tune are invisible to it (but visible to `search`). `search` finds it, `ask` refuses → invoke the `retune` skill; that mismatch is its trigger signature.
- The local 7B generator can smooth over details — for load-bearing claims, verify against the retrieved page text before asserting.
