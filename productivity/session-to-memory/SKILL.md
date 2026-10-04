---
name: session-to-memory
description: >
  Use at the end of a non-trivial session, when winding down a task, or when
  the user asks to "remember this session" or "save what we learned". Extracts
  retention-worthy knowledge from the current session's conversation history
  and context, then persists it to the active memory provider.
---

## Required `<project-root>/docs` reads

Read these project-root spec files before extracting or persisting session knowledge (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/memory-providers.md`

This skill decides what to extract. `memory-usage` decides when writing is warranted. The active memory-provider skill supplies driver mechanics (tool names, args; see `<project-root>/docs/memory-providers.md` in the project root).

## When to Run

- End of a non-trivial session that produced reusable knowledge.
- User asks to save, remember, or persist the session's learnings.
- Before `handoff` when the session uncovered invariants, pitfalls, or decisions worth keeping beyond the next agent.

Don't run for trivial sessions (single command, one-line answer, no investigation). If nothing cleared the `memory-usage` write bar, say so and stop.

## Inputs

| Source | What to scan |
| --- | --- |
| Conversation history | User requests, decisions, corrections, surprises. |
| Tool output | Errors, root causes, schema facts, command results. |
| Files touched | Paths, patterns, conventions discovered. |
| Active artifacts | Plans, ADRs, PRDs, commits — reference, don't duplicate. |

## Extraction Targets

Pull only what clears the `memory-usage` write bar: reusable, hard-won, non-obvious, not trivially greppable. Discard the rest.

| Category | Keep | Drop |
| --- | --- | --- |
| Invariants | Non-obvious constraints the code enforces | Comments that restate code |
| Conventions | Naming, layout, and patterns the project mandates | Style recoverable from one file |
| Pitfalls | Traps that required real investigation | One-off typos |
| Decisions | Architectural choices with lasting rationale | Reversible preferences |
| Module facts | Shape, seams, ownership, lifecycle | Trivial structure |
| External facts | API quirks, version-specific behavior, rate limits | Public doc defaults |

## Procedure

1. **Survey + Filter** — scan the session's conversation history, tool outputs, and touched file paths. Build a distilled candidate list of `(topic-path, one-line substance, source citation)` entries that clear the `memory-usage` write bar. Discard the rest.
2. **Dedupe** — list existing memories (`memory-usage` workflow step 1; see `<project-root>/docs/memory-providers.md` in the project root). For each candidate, edit the existing entry if it overlaps; write a new entry only if the topic path is absent.
3. **Structure** — name entries with stable slash-separated topic paths (`modules/<name>/<subtopic>`, `pitfalls/<topic>`, `decisions/<topic>`). Cross-reference with `mem:<name>`.
4. **Persist** — hand each write to the active memory-provider skill's driver. The parent owns persistence.
5. **Report** — one line per entry written or edited: `topic-path — verb (wrote|edited) — source citation`. If nothing cleared the bar, say so.

## Output Contract

Return a compact changelog listing entries written/edited with source citations. Do not paste memory bodies.

## Hard Rules

- Never persist conversation state, task progress, or session scratchpads.
- Never duplicate codebase-readable truth — cite the file:line instead.
- Never paste full diffs, logs, or file contents into a memory. Distill.
- Never write secrets, credentials, or PII.
- One topic per entry. Split entries past ~100 lines.
- Edit over delete-and-recreate to keep `mem:` references stable.
- If the active memory provider is unavailable, report `BLOCKED` and stop.
  Don't invent a fallback store.

