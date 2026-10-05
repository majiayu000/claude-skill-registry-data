---
name: flow-memory
description: Curate durable PWDEV Flow project decisions, lessons, and conventions. Use when the user asks to capture, list, show, link, supersede, or select project memory, or when an approved workflow decision should persist across phases.
---

# Curate project memory

Read [memory](../../references/memory.md), [artifacts](../../references/artifacts.md), and [safety](../../references/safety.md) before changing memory.

## Route operations

- `capture <decision|lesson|convention> <statement>`;
- `list [type|scope]`;
- `show <name>`;
- `link <name-a> <name-b>`;
- `supersede <name> <reason> [replacement]`;
- `select <phase-or-task>`.

Infer the operation only when the user's intent is unambiguous. Listing, showing, and selecting are read-only. Capture, link, and supersede modify only `.planning/flow/memory/`.

## Capture

1. Confirm the statement is durable, project-specific, supported by evidence, and not already represented.
2. Reject temporary task state, speculation, secrets, personal data, and copied conversation history.
3. Choose the exact type, scope, confidence, source, invalidation condition, and related entries.
4. Write the entry using [memory](../../references/memory.md) and update `MEMORY.md` without duplicating the body.

## Link and supersede

Relations are symmetric: update both existing entries and the index. Supersede rather than delete by default; retain reason, date, and replacement. Ask before irreversible deletion if the user explicitly requests removal.

## Selection

Select direct matches, then one relation hop. Explain why every selected entry is relevant and flag contradictions. Never let memory override current user instructions or `AGENTS.md`.

## Output

Return operation, affected or selected paths, index status, contradictions, and next action.
