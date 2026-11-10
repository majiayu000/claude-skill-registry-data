---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `GLOSSARY.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

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

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives. Decisions still get one `docs/adr/` per repo root, never one per context:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← agent-behavior decisions (byro-repo)
├── packages/
│   ├── framework/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← framework decisions (its own repo)
│   └── real-estate/
│       ├── GLOSSARY.md
│       └── docs/adr/                 ← real-estate decisions (its own repo)
```

An ADR goes in the repo its argument concerns. `packages/personal` gets no `docs/adr/`.

Create files lazily: only when you have something to write. If no `GLOSSARY.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Don't batch these up: capture them as they happen. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

Its "What qualifies" list names the kinds of decision that pass. Offer the ADR and write it only after the developer's yes. When the developer rejects a suggestion of yours for a reason that bears weight, offer an ADR recording it, so nobody suggests it again.

### Backlink the issue

When an ADR is written, backlink it from the issue its `Source:` names, by the command and line format in the [issue-tracker doc](../../../docs/agents/issue-tracker.md#commands-for-each-operation), never by hand-editing the body.

### Build principles on ADRs

Principles live in the repo's design doc: `packages/framework/docs/design.md` with its reasoning files for the framework, and `docs/agent-behavior-design.md` for agent behavior. **A principle may rest on one ADR, and gets a reasoning file only for what no single ADR holds** ([ADR 0020](../../../docs/adr/0020-a-principle-may-rest-on-one-adr-and-a-reasoning-file-holds-only-what-no-adr-holds.md)). After writing an ADR:

- **An instance**: when it makes an existing principle's argument, add it to that principle's reasoning without asking, as a link plus one clause on how the ADR makes the argument. A principle whose line linked its one ADR directly gets a reasoning file once it has a second.
- **A new principle**: read every ADR body in the repo's `docs/adr/`; there is no index file. When the new ADR, alone or with past ones, makes an argument no principle covers that decides cases the ADRs don't name, propose a one-line principle citing them. Write its line, and any reasoning file, only after the developer approves.
- **Supersession**: a superseded ADR stops counting. When that leaves a principle with no ADR, bring it to the developer rather than deleting it.
- **Deliberate absence**: each bullet of the deliberate-absence principle names the gap and its reason, so it answers "is this gap deliberate?" without opening the ADR.
- **Cross-repo citations**: a principle may cite an ADR from a repo that uses its library, when the argument concerns the library, by absolute GitHub URL. It never cites a private repo's ADR.
