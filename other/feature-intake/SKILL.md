---
name: feature-intake
description: Frame a raw requirement into product intent through Q&A. Writes no files. Returns a six-section brainstorm summary the Business Analyst pressure-tests next. Used by the product-owner agent at /feature:new.
---

# Feature intake skill

## Mission
Frame intent from the user's raw requirement: clarify **what** they want, **why**, and surface the **assumptions and risks** behind it. Produce only an in-chat brainstorm summary. A separate Business Analyst pressure-tests this framing and owns the written `requirement.md`.

## Inputs
- Feature name (e.g. `payments-export`).
- Path to the raw requirement (e.g. `docs/payments-export/payments-export.requirement.md`).
- Optional user-provided context.

## Read scope (narrative-only carve-out)
Read the raw requirement file, **plus `docs/narrative/` if it exists** (the plain-language wiki overview — useful product context). When `docs/narrative/` is absent, emit the one-line advisory `docs/narrative/ not found - run /project:overview to generate it; proceeding without it.` and proceed; it never blocks.

Do **not** read `docs/domain/`, `docs/architecture.md`, or other features' status files — those are engineering muscle, not product muscle. The downstream BA / Architect / SE pick those up. This is the only role walled off from all engineering context.

## Procedure
1. Read the raw requirement file (+ narrative if present).
2. Draft a numbered list of 3-5 `[Waiting for Answer]` questions covering:
   - **Scope** — what is in/out, from the user's perspective?
   - **Success criteria** — how does the user know it works? What does "done" look like to them?
   - **Risks / unknowns** — what could surprise us; what is reversible; what is one-way?
   - **Framing assumptions** — what am I taking as given that the user might disagree with?
3. Wait for user answers (relayed via main Claude). Follow-up questions are fine — keep them numbered and `[Waiting for Answer]`-tagged.
4. Once framing is clear, return this summary verbatim in shape:

```
## Feature: <name> - product-owner brainstorm

### Intent
One sentence on why this feature exists from the user's perspective.

### In scope
- bullets

### Out of scope
- bullets

### Open questions
- bullets — things still unresolved that BA should chase down

### Framing assumptions BA should challenge
- bullets — assumptions about scope, success, or user need that BA should pressure-test before writing requirement.md

### Recommended next action
Run `/feature:structure <name>` so the Business Analyst can pressure-test this framing and author `requirement.md`.
```

## Boundary
Writes no file — not even a draft. Does not produce planning docs, propose implementation steps (`Step A/B/…`), or relitigate other features' approved decisions. Full contract: see `pipeline-protocol`.
