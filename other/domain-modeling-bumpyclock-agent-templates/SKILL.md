---
name: domain-modeling
description: Sharpen project domain terms or author glossary and ADR content. Use for terminology decisions, not merely reading existing definitions.
---

# Domain Modeling

Build and sharpen the project's domain model by challenging terms and testing them against concrete scenarios. This skill changes or proposes changes to the model, rather than merely reading `GLOSSARY.md` for vocabulary.

## Requested mode

In discussion or review, return proposed glossary wording and decisions without changing files. Agreement on a term is not by itself permission to edit the repository.

When glossary or ADR edits are authorized, persist resolved terms and qualifying decisions within that scope as they settle. Do not ask again for each entry. Finish with the requested proposals or edits, identifying any material decision still unresolved.

## File structure

Use the repository's existing glossary convention. Read a legacy `CONTEXT.md` or `CONTEXT-MAP.md` when it owns domain vocabulary; do not create a competing glossary or rename it without authorization. For new glossaries, use the names below.

Most repos have a single context:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

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

During authorized editing, create files lazily. Create `GLOSSARY.md` when the first term is resolved, and `docs/adr/` when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Capture resolved terms

Record each resolved term in the requested proposal or authorized `GLOSSARY.md` edit as it settles. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
