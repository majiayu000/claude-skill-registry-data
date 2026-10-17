---
name: grill-with-docs
disable-model-invocation: true
description: Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (GLOSSARY.md, ADRs) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions.
---

<what-to-do>

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Map it as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for my answers before the next round.

Format each question like so:

```
**Q1** - **<question title>**: <question body, may be multiple paragraphs, including multiple choices>

Recommended: <your recommended answer>
```

Each round of answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never mine. When a frontier question needs a fact from the codebase, the docs, or the environment, dispatch a subagent to find it rather than asking me. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait — ask the rest of the frontier now. The _decisions_ are mine — put each one to me and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on the plan until I confirm we have reached a shared understanding.

</what-to-do>

<supporting-info>

## Domain awareness

During codebase exploration, also look for existing documentation:

### File structure

Most repos have a single glossary:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple glossaries. The map points to where each one lives:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

Create files lazily — only when you have something to write. If no `GLOSSARY.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

### Other docs

A repo often has more markdown than `GLOSSARY.md` and ADRs — design notes, architecture overviews, runbooks, RFCs, often under `docs/`. Don't read them wholesale; that burns context. Instead, when a grilling question touches a topic, `rg` the docs for the relevant terms and read only the hits. Treat what you find as context to challenge against, not law — only `GLOSSARY.md` and ADRs are authoritative. If a doc contradicts the plan, surface it like any other conflict.

## During the session

### Challenge against the language

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your language defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Probe the technical shape

The design tree is not only domain language — technical decisions are branches too, and they belong on the frontier as soon as their prerequisites settle. Make sure the tree covers:

- **Libraries and dependencies** — most features need no new dependency; check first whether the project's existing dependencies or the framework's built-ins already cover it, and if so just confirm that. But when the plan touches a problem the ecosystem has solved (auth, validation, jobs, uploads, …) and nothing in the project covers it, identify the idiomatic candidates for the stack and put the choice to the user with a recommendation. Never let the session end with "we'll use some library" implied but unnamed.
- **Structure and placement** — where the new code lives, which existing modules it touches, whether it follows an existing pattern in the repo or introduces a new one.
- **Data and contracts** — schema changes, API shapes, and integration points the plan implies.

As with facts, the research is yours: dispatch a subagent to survey the project's dependencies and the candidate libraries, then bring back a concrete choice for the user to make.

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Don't batch these up — capture them as they happen. Use the format in `${CLAUDE_SKILL_DIR}/GLOSSARY-FORMAT.md`.

Keep it devoid of implementation details. Do not treat `GLOSSARY.md` as a spec or scratch pad — it holds canonical terms and nothing else; everything else lives in ADRs or code.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in `${CLAUDE_SKILL_DIR}/ADR-FORMAT.md`.

</supporting-info>
