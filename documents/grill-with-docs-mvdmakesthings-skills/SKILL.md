---
name: grill-with-docs
description: Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions.
version: 0.2.0
---

<what-to-do>

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

Once decisions have crystallised, do a downstream consistency sweep: check whether any resolved decision contradicts existing downstream artifacts — the PRD, open tickets, README, sibling ADRs. Surface each conflict and offer to reconcile. Don't wait for the user to notice.

</what-to-do>

<supporting-info>

## Domain awareness

During codebase exploration, also look for existing documentation:

### File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Explain things simply

When you ask a question, or explain something, do so as simply as possible. Use simple language and avoid jargon. If you need to use a technical term, explain what it means in plain English.

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./references/CONTEXT-FORMAT.md).

**Deferred-write fallback.** If inline writes are blocked (e.g., plan mode is active) or the resolved decision describes behavior that doesn't exist in code yet, record the resolved terms in the active working artifact (plan file, scratch doc) with explicit markers, and defer the CONTEXT.md/ADR writes to implementation time. Do not write a glossary entry that describes future behavior as if it already exists — that creates doc/code drift. When deferring, tell the user: "I'm holding these term updates — remind me to apply them to CONTEXT.md once this is built."

`CONTEXT.md` should be devoid of process and wiring details, but it *should* name the mechanisms the team talks about out loud. One-line test: a noun the team says in conversation belongs here; a code path does not. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./references/ADR-FORMAT.md).

**Amending vs. superseding.** When a resolved decision evolves an *existing* ADR, prefer an in-place dated amendment (append a new section: "## Amendment — YYYY-MM-DD") if the core decision still stands. Create a superseding ADR only if the core decision flips. This keeps the history readable without orphaning the original record.

### Update linear if needed

If you make a decision that has implications for implementation, update the relevant issue in the project or issue within linear. Update the docs as you go, don't batch them up for later.
</supporting-info>