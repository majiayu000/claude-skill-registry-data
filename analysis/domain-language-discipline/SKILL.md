---
name: domain-language-discipline
version: "1.0.0"
user-invocable: false
description: "Hard discipline for project domain language: maintain a pure glossary in CONTEXT.md (no implementation details), challenge fuzzy or conflicting terms in-session, create files lazily, keep orthogonal to OpenSpec behavioral contracts. Referenced by PDCA hosts during clarify/analyze when domain terms matter. Triggers — 「领域语言」「CONTEXT.md」「术语表」「统一语言」「领域词汇」 / domain language discipline, project glossary, CONTEXT.md. Do NOT use as a substitute for OpenSpec specs."
---

# Domain Language Discipline

> Internal shared skill. Single source of truth for **project ubiquitous language** as a glossary, orthogonal to OpenSpec. Hosts declare it in `dependencies` and abort if missing — no silent fallback.
>
> **Name note:** intentionally **not** named `domain-modeling` (external skills repo). Use this name only.

## What CONTEXT.md is (and is not)

| Is | Is not |
|----|--------|
| Canonical terms and boundaries (glossary) | Spec, ticket, or task list |
| Pure domain language | Implementation details, APIs, schemas, file paths |
| Orthogonal companion to OpenSpec | Replacement for `openspec/` proposal/specs/design/tasks |

If a root `CONTEXT-MAP.md` exists, treat it as a pointer to multiple context-local `CONTEXT.md` files; otherwise use a single root `CONTEXT.md`.

## Required behavior

1. **Read when domain language is in play** — if `CONTEXT.md` (or mapped files) exists, load relevant terms before sharpening analysis or solutions that hinge on vocabulary.
2. **Challenge conflicts** — when the user (or session) uses a term that conflicts with the glossary, surface the conflict and resolve which meaning is canonical before continuing as if both were fine.
3. **Sharpen fuzzy language** — propose a precise canonical term when language is vague or overloaded; confirm with the user when it is a decision (per `clarifying-question-discipline` if asking).
4. **Update lazily, inline** — when a term is resolved, update `CONTEXT.md` immediately. Create the file only when the first term is recorded. Keep entries free of implementation detail.
5. **ADRs sparingly** — offer an ADR only when hard-to-reverse **and** surprising without context **and** the result of a real trade-off; otherwise skip. ADRs are optional companions, not required by this skill's core loop.

## Forbidden

- Writing OpenSpec requirements, code designs, or API contracts into `CONTEXT.md`
- Treating the glossary as the behavioral source of truth instead of OpenSpec / host sinks
- Renaming this skill to `domain-modeling` inside this repository

## Integration guide

- Hosts: one-line pointer at clarify/analyze when domain terms matter — load this skill; do not paste glossary format tables into hosts.
- Prefer `user-invocable: false`; users reach it through PDCA hosts or explicit load.
- Behavior changes still go to OpenSpec (or the host's artifact sink), not into `CONTEXT.md`.
