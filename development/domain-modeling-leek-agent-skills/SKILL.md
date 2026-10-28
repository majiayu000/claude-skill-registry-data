---
name: domain-modeling
description: "Build and sharpen a project's domain model: challenge terms against the glossary, resolve fuzzy language, stress-test concepts with concrete scenarios, and record GLOSSARY.md entries and ADRs the moment decisions land. Use when pinning down domain terminology or a ubiquitous language, recording an architectural decision, or when another skill (grilling, wayfinder, to-spec) needs the domain model maintained."
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. Merely *reading* `GLOSSARY.md` for vocabulary is not this skill, that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.

Runs alongside `grilling` sessions (`grill-with-docs` is the front door that pairs the two), `wayfinder` grilling tickets, and `to-spec` synthesis: anywhere terms get decided. It's supporting work, not a pipeline stage: it never prints the pipeline end-of-session block, whether nested or run directly, the invoking skill (or the user's next step) owns routing.

## File structure

Most repos have a single context:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-single-db-multi-tenancy.md
│       └── 0002-money-as-integer-minor-units.md
└── app/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives: in a Laravel modular monolith that's the module root:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                              ← system-wide decisions
└── app/Domain/                           ← or modules/, app-modules/, follow the repo
    ├── Ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                     ← context-specific decisions
    └── Billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

Create files lazily: only when you have something to write. No `GLOSSARY.md`? Create one when the first term is resolved. Found the old `CONTEXT.md` / `CONTEXT-MAP.md` instead? Before the first write, `git mv` it to `GLOSSARY.md` / `GLOSSARY-MAP.md` and fix the map's links. No `docs/adr/`? Create it when the first ADR is needed. Formats: [references/glossary-format.md](references/glossary-format.md) and [references/adr-format.md](references/adr-format.md).

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately: "Your glossary defines 'cancellation' as X, but you seem to mean Y, which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. Where `AskUserQuestion` is available, put the candidates as options: your recommendation first, each option's description saying what choosing it commits the model to; otherwise ask the same shape in chat. "You're saying 'account', is that the Customer or the User?" is a click-to-answer decision, not an open-ended essay prompt.

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force precision about the boundaries between concepts: "A Customer with two Subscriptions cancels one mid-cycle, what happens to the Invoice already issued?"

### Cross-reference with code

When the user states how something works, check whether the code agrees. In a Laravel codebase the model lives in more places than prose, check the glossary term against:

- Eloquent model and relationship names (`app/Models`, `HasMany` method names)
- Table and column names in migrations
- Enum cases (`app/Enums`)
- Policy names and ability strings
- Filament resource/page labels and navigation names
- Route names, job names, event names

If you find a contradiction, surface it: "Your code cancels entire Orders (`Order::cancel()`), but you just said partial cancellation is possible, which is right?" When a term is resolved *against* the code's current naming, the rename is real **build** work, record the *decision* here, and leave the rename itself for the spec (or a `tickets/` ticket once one exists), never as a `wayfinder` decision-map ticket, which holds only things decided, not things built. Never silently absorb it.

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Don't batch these up: capture them as they happen. Use the format in [references/glossary-format.md](references/glossary-format.md). If sessions may run in parallel, re-read `GLOSSARY.md` immediately before writing and add only your entry, so a concurrent edit isn't clobbered.

`GLOSSARY.md` must stay totally devoid of implementation details. It is a glossary, not a spec, a scratch pad, or a home for implementation decisions.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [references/adr-format.md](references/adr-format.md).
