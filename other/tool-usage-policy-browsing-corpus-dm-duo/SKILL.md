---
name: tool-usage-policy-browsing-corpus-dm-duo
description: >
  Tool usage guidelines for corpus research agents running in DM/Duo mode.
  Covers parallel tool calling, the corpus search-then-fetch workflow, and
  sharing results via direct messaging and task-completion summaries.
---

# Tool Usage Policy (Corpus Browsing — DM/Duo)

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

There is NO `pdf_read` tool and NO live-web browsing in this run — all
retrieval goes through the static document corpus via `web_search` /
`web_fetch`. Do not try to fetch external URLs.

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

## Sharing Results (DM/Duo Mode)

Share findings through the two mechanisms you have:

- **`complete_task` summary** — your primary output. Include the answer,
  the corpus evidence you relied on (document titles and the key quoted
  chunks/facts), and any caveats. This is the ONLY signal the orchestrator
  (DM mode) or the main worker (Duo mode) is guaranteed to read.
- **`send_message` to a specific peer** — use when a teammate needs your
  finding to do their work, when you spot an error in their result, or
  when your conclusion rests on a non-obvious assumption a peer should
  know about. Quote the supporting corpus evidence inline in the message body.

Do NOT broadcast (`to='all'`) unless your finding affects every
teammate's work.
