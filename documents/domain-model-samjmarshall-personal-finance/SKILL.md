---
name: domain-model
description: Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions.
disable-model-invocation: true
model: opus
effort: xhigh
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Pre-filtered work from /brainstorm

If invoked against a brainstorm design doc, read these appendix sections before grilling:

- `## ADR Candidates` — pre-filtered decisions from the brainstorm session. Offer each as a Proposed ADR candidate; act on the user's selections per the regular ADR writing rules below.
- `## Terminology TODO` — terms sharpened during the brainstorm. Update `CONTEXT.md` per the rules below.

As each entry is resolved, remove it from its appendix section. For resolved ADR candidates, append a link to the new ADR under a `## Related ADRs` footer in the design doc. Drop the appendix heading when its section is empty. Then continue with a normal grilling pass — the brainstorm may have missed candidates.

## Domain awareness

During codebase exploration, also look for existing documentation:

### File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── adr001-event-sourced-orders.md
│       └── adr000-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── server/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── app/
|       ├── (login)/
│       |    ├── CONTEXT.md
│       |    └── docs/adr/
|       ├── (application)/
|            ├── CONTEXT.md
│            └── docs/adr/
```

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

Don't couple `CONTEXT.md` to implementation details. Only include terms that are meaningful to domain experts.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR.

When all three hold, pick the template that matches the shape of the decision:

- **[ADR-TEMPLATE-IN-DEPTH.md](./ADR-TEMPLATE-IN-DEPTH.md)** when the session surfaced ≥2 genuine alternatives that were weighed side-by-side.
- **[ADR-TEMPLATE-SIMPLE.md](./ADR-TEMPLATE-SIMPLE.md)** when the decision is real but there was effectively one path with a constraint or two.

See [ADR-FORMAT.md](./ADR-FORMAT.md) for the full writing guide, frontmatter spec, and anti-patterns.
