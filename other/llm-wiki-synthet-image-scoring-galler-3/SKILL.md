---
name: llm-wiki
description: Use when searching, asking, ingesting, compiling, reviewing, refreshing, validating, or answering from the shared local LLM Wiki (CLI `llmwiki` or MCP server `llmwiki-ro-core`).
capability: "evidence-bound LLM Wiki workflow"
side_effect_level: local_write
approval_required: false
requires_tools: "llmwiki CLI or llmwiki-ro-core MCP server"
output_schema: "Cited answer or structured operation result"
risk_class: medium
---

# LLM Wiki (shared)

Use the installed `llmwiki` CLI or the `llmwiki-ro-core` MCP server. Do **not** edit
`.llmwiki/wiki.db`, object files, or generated `wiki/pages/*.md` directly.

Wiki root (this workstation): `D:\Projects\synthet-llm-wiki`

## Find and answer

1. Prefer MCP tools from `llmwiki-ro-core` when connected.
2. Start with reviewed-only search/ask. Non-reviewed states need an explicit filter and visible labels.
3. Return exact source-revision/evidence citations. If support is inadequate, say so; do not invent facts.

CLI fallback:

```bash
llmwiki --root "D:\Projects\synthet-llm-wiki" search "query" --json
llmwiki --root "D:\Projects\synthet-llm-wiki" ask "question" --json
llmwiki --root "D:\Projects\synthet-llm-wiki" sources --json
```

## Ingest / compile / review

Writes and review require elevated MCP flags (`--allow-writes` / `--allow-review`) or explicit CLI
commands with the user's reviewer identity. Generated facts stay `candidate` until human review.
After canonical changes: `llmwiki --root "D:\Projects\synthet-llm-wiki" validate` then `render`.

Canonical skill and docs live in the wiki repo: `D:\Projects\synthet-llm-wiki` (`AGENTS.md`, `docs/schema.md`).
