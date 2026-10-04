---
name: lore
description: Search and ingest knowledge from Lore, a research repository with citations
version: "1.0"
user-invocable: false
---

# Lore Knowledge Base

Lore is a research knowledge repository you have access to via MCP tools. It stores documents, meeting notes, interviews, and decisions with full citations — not just summaries, but the original content linked back to its source. Use it to ground your answers in evidence and to preserve important context from your conversations.

## When to Ingest Content into Lore

Push content into Lore using the `ingest` tool whenever you encounter information worth preserving:

- **After conversations**: When a user shares meeting notes, interview transcripts, or important documents, ingest them so they're searchable later.
- **External content**: When you fetch content from Slack, Notion, GitHub, email, or other systems, ingest the relevant parts into Lore.
- **Decisions and context**: When important decisions are made or context is shared that future conversations will need.

Always include:
- `source_url`: The original URL (Slack permalink, Notion page URL, GitHub issue URL) for citation linking.
- `source_name`: A human-readable label like "Slack #product-team" or "GitHub issue #42".
- `project`: The project this content belongs to.

Ingestion is idempotent — calling `ingest` with the same content twice is safe and cheap (returns immediately with `deduplicated: true`).

## When to Search Lore

Before answering questions about past decisions, user feedback, project history, or anything that might already be documented:

1. **Use `search`** for quick lookups. Pick the right mode:
   - `hybrid` (default): Best for most queries
   - `keyword`: For exact terms, names, identifiers
   - `semantic`: For conceptual queries ("user frustrations", "pain points")

2. **Use `research`** only when the question requires cross-referencing multiple sources or synthesizing findings. It costs 10x more than `search` — don't use it for simple lookups.

3. **Use `get_source`** with `include_content=true` when you need the full original text of a specific document.

## When to Retain Insights

Use `retain` (not `ingest`) for short, discrete pieces of knowledge:
- Key decisions: "We chose X because Y"
- Synthesized insights: "3/5 users mentioned Z as their top issue"
- Requirements: "Must support SSO for enterprise"

## Citation Best Practices

When presenting information from Lore, always cite your sources:
- Reference the source title and date
- Quote directly when possible
- If a `source_url` is available, link to the original

## Example Workflows

**User asks about past decisions:**
1. `search("authentication approach decisions", project: "my-app")`
2. Review results, get full source if needed: `get_source(source_id, include_content: true)`
3. Present findings with citations

**User shares meeting notes:**
1. `ingest(content: "...", title: "Sprint Planning Jan 15", project: "my-app", source_type: "meeting", source_name: "Google Meet", participants: ["Alice", "Bob"])`
2. Confirm ingestion to user

**User asks a broad research question:**
1. `research(task: "What do users think about our onboarding flow?", project: "my-app")`
2. Present the synthesized findings with citations
