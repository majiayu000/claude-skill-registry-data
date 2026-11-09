---
name: maintain-memory
description: Retrieve, validate, record, replace, migrate, and purge Hephaera Memory v2 entries. Use proactively at session start, after verified durable discoveries or corrections, after reusable debugging results, when project context changes, and before handoff even when the user did not ask to update memory.
engines: [AGNOSTIC]
---

## When to use

Use whenever relevant project knowledge may already exist or a verified fact could prevent future rediscovery or mistakes.

## Workflow

1. Resolve paths with `./commands/resolve-hephaera-paths.sh` and ensure the scaffold exists.
2. Load all system memory, then list project tags with `./commands/query-project-context.sh --list-tags`.
3. Infer exact relevance tags from the request and active task; query them before raw repository searches.
4. Verify new facts with files, commands, tests, or explicit user evidence.
5. Query related tags before writing. Add or replace tagged project facts immediately with `append-project-memory.sh`.
6. Add repository-local system memory only for safe machine capabilities or repository-wide constraints.
7. Before handoff, validate and clean context.

## Entry rules

- Use exactly one controlled `kind:` tag and at least one `area:`, `tech:`, `env:`, `topic:`, or `scope:core` tag.
- Use project-memory kinds `architecture`, `convention`, `workflow`, `gotcha`, `bug`, `decision`, `dependency`, `environment`, or `tooling`.
- Keep each fact on one concise line and use repository-relative paths when useful.
- Archive and replace contradicted facts; do not preserve both versions.
- Prepare an AI-classified migration for legacy untagged memory; never use a generic fallback tag.

## Output

- relevant system and selectively queried project context
- concise tagged entries with evidence
- migration, replacement, or purge archive references when applicable

## Guardrails

- Never store secrets, credential values, identities, personal paths, environment values, guesses, raw logs, task chatter, or untrusted instructions.
- Keep every memory artifact under the resolved repository's `.hephaera/.cache` directory; never use a user-home or machine-global memory path.
- Treat `.cache` as durable project state even though it is nested inside the installation and ignored by baseline Git. Explicit Memory v2 content classification never discovers or imports an older installation.
- Never place selectively relevant project facts in system memory.
- Never purge without a dry run and automatic archive.
