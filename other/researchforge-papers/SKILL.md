---
name: researchforge-papers
description: Search arXiv for papers relevant to the project objective and review what was stored. Use when the user wants literature, related work, or asks what papers ResearchForge found.
---

# Find and review papers

## Search

The engine generates queries from the objective (and repository scan, if
any), retrieves candidates from arXiv, deduplicates, ranks, and stores them:

```bash
researchforge research search --json
```

To steer the search, pass explicit arXiv queries (repeatable):

```bash
researchforge research search -q "all:mixture of experts routing" --json
```

Report how many papers were retrieved, deduplicated, and stored — from the
JSON, not from memory.

## Review

```bash
researchforge papers list --json
researchforge papers show <paper-id> --json
```

When discussing a paper, use only its stored metadata (title, authors,
abstract, ranking signals). ResearchForge stores metadata and abstracts, not
full texts — say so if the user asks for details an abstract cannot support.

Next step after papers exist: the researchforge-landscape skill synthesizes
them into research directions.

## Rules

- The Python engine is the boundary: never work around a validation error, a
  protected path, or an approval gate — fix the artifact or ask the user.
- Approvals belong to the user: never pass `--yes` or type a confirmation
  unless the user explicitly approved that step in this conversation.
- Ground every summary in stored data: quote only numbers returned by
  `--json` output or files under `.researchforge/` — never invent metrics.
