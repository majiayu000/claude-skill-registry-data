---
name: tool-usage-policy-browsing-corpus
description: >
  Tool usage guidelines for corpus research agents. Covers parallel tool
  calling, search strategy, and the search-then-fetch workflow for the
  static document corpus.
---

# Tool Usage Policy (Corpus Browsing)

## General

- Call multiple tools in a single response when they are independent.
- Prefer specialized tools over shell commands:
  - `read_file` instead of cat/head/tail

## Corpus Research Workflow

Use these tools for effective corpus research:

1. **`web_search`** — Search the document corpus for relevant text chunks.
   Returns scored snippets (~1200-1400 chars each). Use this to discover
   relevant information and assess what documents to investigate further.
2. **`web_fetch`** — Retrieve the full text of a document from the corpus.
   Pass a **descriptive search query** (NOT a URL) describing what document
   you want to read. Returns the complete document text (~2500-7200 chars).
   Use when search snippets aren't sufficient and you need the full context.
3. **`calculator`** — Evaluate numeric expressions. NEVER calculate mentally.

### Search-Then-Fetch Principle

- Use `web_search` first to find relevant chunks and identify promising documents.
- When you need more context than the snippets provide, use `web_fetch` with
  a targeted query to retrieve the full document text.
- `web_fetch` searches the corpus independently — it does NOT take URLs.
  Describe what you want to read in the query.

## Search Strategy

- Start with broad queries to understand the landscape, then narrow down.
- Use multiple search queries when the topic has different facets or
  terminology — do not rely on a single query.
- If the first search returns no useful results, rephrase the query using
  synonyms or alternative keywords before giving up.

## Source Attribution

- Include evidence from the corpus for every factual claim.
- When multiple sources conflict, note the discrepancy and cite all sides.

## Do Not Guess

- Do NOT claim a fact without supporting evidence from the corpus — if you
  cannot find evidence, say so explicitly.
- Cross-check key numbers or dates across multiple document chunks when possible.

## Sharing Results (Swarm Mode)

- Post search findings to `#key-findings` or `#discoveries`.
- Include a brief summary of what you found and why it's relevant.
