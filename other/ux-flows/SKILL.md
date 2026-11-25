---
name: ux-flows
description: Maps user flows before screens are built, producing use cases with error paths, Mermaid flow and state diagrams, a screen inventory checked for dead ends and orphans, and a handoff table that feeds writing-plans. Use when planning a multi-screen feature or a sign-up, onboarding or checkout journey, or when asked for user flows, journeys, screen maps or state diagrams.
---

# UX flows

**Announce at start:** "Using opm-design:ux-flows to map use cases, flows and screens before building."

Files go in `docs/ux-flows/<feature>/`, with `<feature>` in kebab-case. `P/` below is
`${CLAUDE_PLUGIN_ROOT}`.

## Size first

A single-screen change gets one use case in `use-cases.md` and one state diagram in `flows.md`, with no inventory and no
handoff. Everything else runs all four steps.

## 1. Use cases

Write `use-cases.md` with `references/use-case-template.md`. Each use case has an ID (`UC-01`),
actors, preconditions, main flow, alternative and error flows, and postconditions. Facts you
were not told become open questions, never guesses.

**Stop. Ask the user to approve the use cases with AskUserQuestion before drawing any diagram.**
Change them and ask again until they approve.

## 2. Diagrams

In `flows.md`, draw for each use case:

- a Mermaid flowchart of the path through screens and decisions
- a state diagram covering idle, loading, success, empty, error and offline where they apply
- a sequence diagram only when the flow calls a backend, with arrows that name the HTTP method
  and path (`POST /api/orders`)

Follow `references/mermaid-patterns.md`: fixed node shapes, at most 20 nodes per diagram,
larger flows split into `[[Sub-flow]]`, and shared `classDef`s.

## 3. Screen inventory

Add a table to `flows.md` with exactly these columns:
`| Screen | Use cases | Key elements | Outgoing links |`. Then run:

    node P/skills/ux-flows/scripts/check-flows.mjs docs/ux-flows/<feature>/flows.md

Fix every `Violation:` line. A dead end gets a way out (back, home or retry). An orphan gets the
use case that reaches it, or is removed. Rerun until it prints `ok:`.

## 4. Handoff

Write `handoff.md` with `references/handoff-template.md`: a From screen / Element / To screen
table, the endpoints from the sequence diagrams, and Open questions. Then offer
`opm:writing-plans`; the handoff is its input.

## Red flags

| Thought | Reality |
|---|---|
| "The error path is obvious" | Write it; unwritten error paths ship broken. |
| "I'll draw while they review the use cases" | Use cases are approved first. |
| "That screen is a dead end on purpose" | Give it a way out: back, home or retry. |
| "One big diagram is clearer" | Over 20 nodes, split into sub-flows. |
