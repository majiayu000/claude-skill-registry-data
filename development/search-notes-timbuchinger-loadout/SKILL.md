---
name: search-notes
description: Always use this skill at the start of a task to check whether relevant information already exists. Use when users ask to recall, search memories, or subscribe to updates. Triggers on "recall", "search memories", "list keys", "share", "subscribe to", or any persistent storage request.
---

Also use when:

- Unsure how to proceed
- Working with internal services, products, or processes
- Knowledge required is not publicly available
- The task relates to a specific repo, environment, or system

Treat this skill as:

> Your internal memory lookup

---

## What this skill does

Performs a **hybrid search (dense + sparse)** over stored notes.

Uses the **Qdrant MCP server** via the **`qdrant-search-notes`** tool.

The tool performs:

- Dense semantic search
- Sparse keyword search
- Result fusion using Reciprocal Rank Fusion (RRF)

---

## Collection

Search is always performed against `notes-hybrid`.

---

## How to search effectively

### 1. Construct the query

Use a natural language description of what you are trying to do.

Examples:

- restart a stuck kubernetes deployment
- internal api endpoint for resetting user passwords
- terraform s3 lifecycle drift issues

This query is used for:

- Dense embedding generation
- Sparse keyword extraction

---

### 2. Apply filters when appropriate

Use filters to narrow results when the domain is known.

Common filters:

- type = cli
- tool = kubectl / aws / terraform
- language = bash
- source = repo:infra

Example:

```json
{
  "must": [
    { "key": "type", "match": { "value": "cli" } },
    { "key": "tool", "match": { "value": "kubectl" } }
  ]
}
```

---

### 3. Interpret results carefully

- Prefer notes with clear context
- Prefer newer notes if multiple exist
- Refine and re-run search if results are close but incomplete

---

## Tool usage

Use the **qdrant-search-notes** MCP tool with:

- Query text
- Optional payload filters
- Result limit (typically 5–10)

The tool:

- Executes dense and sparse searches
- Fuses results using RRF
- Returns ranked, agent-readable notes

---

## Agent reminder

Before inventing a solution, **check memory first**.

If no relevant note exists and you learn something new:

1. Complete the task
2. Immediately use **add-note** to store the new knowledge
