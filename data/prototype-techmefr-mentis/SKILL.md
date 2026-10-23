---
name: prototype
description: "Use when a design question is best answered by building something small and throwing it away: whether a state model or a piece of logic holds up against awkward cases, or what a screen should look like. Fixes the question first, picks the shape from it, keeps the prototype visibly disposable, and decides at the end what is lifted into the real code, what is kept as a record and what is never merged."
---

# prototype

A prototype is **throwaway code that answers one question**, and the question decides its shape. This block sits
before `code` (6 of `WORKFLOW.md`) when the open point is "does this feel right" or "what should this look like",
the typed "Prototype" child ticket of `wayfinder` (§2), and ahead of the spec: what a prototype decided does not
become a production decision by default (`skills/spec` §5.16).

## When
- A state machine, a data shape or an API surface looks reasonable on paper and nobody has pushed an awkward case
  through it.
- Several layouts are plausible and the choice is cheaper to make by looking than by arguing.
- Not when the answer is a fact a read of the code or the documentation would give (`wayfinder` research ticket),
  and not as a first draft of the real feature: a prototype that is meant to be kept is simply the feature.

## Steps

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The question, the rules both shapes share | always, first | [`01-question-and-rules.md`](./references/01-question-and-rules.md) |
| 2 | The two shapes: a logic demo, a set of UI variants | the question is chosen and the artefact has to be built | [`02-the-two-shapes.md`](./references/02-the-two-shapes.md) |
| 3 | After the answer: lift, keep, delete | the question has been answered | [`03-after-the-answer.md`](./references/03-after-the-answer.md) |

## Output / checkpoint
The artefact, named as a prototype, and the written answer to the question it was built for (§3). No pipeline
checkpoint; the answer goes into the spec or the ticket that asked.

## Guardrails
- **One question per prototype**, written down where the prototype lives (§1.1).
- **Never merged as it is.** What survives is the validated decision, rewritten under the project's standards
  (§3.1).
- No tests, no real database, no generalisation: the prototype is allowed to be unfit for production because it is
  never going there (§1.2).
- Status 🟡: thin source, one skill file with two branches, never run by us; open points in
  [`origin.md`](./references/origin.md).

## Origin
Rewritten from the `prototype` skill of mattpocock/skills (MIT), read 2026-10-19, with its two branch files;
sources and what was not verified are in [`origin.md`](./references/origin.md).
