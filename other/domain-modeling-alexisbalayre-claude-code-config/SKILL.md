---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing `docs/glossary.md`, or recording or editing an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `docs/glossary.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

This repo keeps its domain model under `docs/`. There is no `CONTEXT.md` or `CONTEXT-MAP.md`; never create one.

```
/
├── AGENTS.md                  ← repo-wide agent rules
└── docs/
    ├── glossary.md            ← the domain language (one table)
    ├── conventions/           ← naming and coding rules, per area
    ├── adr/                   ← decisions (template in README.md)
    ├── explanation/           ← rationale behind a subsystem
    └── reference/
        └── architecture.md    ← system shape: components, flows, layout
```

Before a session, skim the glossary and any ADRs already filed for the area. For *why*/*how* questions that span several components, delegate to the `architecture-explainer` subagent rather than re-reading docs in the main context.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `docs/glossary.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees (`docs/reference/architecture.md` maps where each component lives). If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update the glossary inline

When a term is resolved, update `docs/glossary.md` right there. Don't batch these up: capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

The glossary should be totally devoid of implementation details. Do not treat it as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else. What resolves outside the glossary goes where it already lives:

- **Naming or structure rule?** The relevant doc in `docs/conventions/`.
- **Rationale for how a subsystem works?** The relevant `docs/explanation/<topic>.md`.
- **System shape has drifted from reality?** `docs/reference/architecture.md`.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
