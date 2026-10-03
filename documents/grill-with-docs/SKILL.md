---
name: grill-with-docs
description: Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions.
---

<what-to-do>

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

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

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

</supporting-info>

---

## Intent-Driven OpenSpec Adapter

In intent-driven OpenSpec projects this skill is **not optional** at its schema gates.

Use it automatically when creating either of these artifacts:

- `openspec/changes/<change>/grill.md` — pre-design grill after proposal/specs and before `design.md`.
- `openspec/changes/<change>/design-review.md` — post-design grill after `design.md` and before `adr.md` / `test-plan.md` / `tasks.md`.

Do not ask the user whether to run grill at those gates. Ask the user only when a material uncertainty cannot be resolved by reading repository context. Ask exactly one question at a time, include your recommended answer and rationale, then wait for the user's answer before asking the next question.

### Context mapping

For this overlay, use these project context locations:

- `CONSTITUTION.md` — persistent project rules, MCP/external-system policy, secret handling, documentation sources, verification rules, and additional AI instructions.
- `CONTEXT.md` — glossary/domain language only. No implementation details, policy, architecture decisions, specs, or scratch notes.
- `CONTEXT-MAP.md` — optional multi-context map. If present, use it to find the relevant context-local `CONTEXT.md` and ADR files. If the relevant context is unclear, ask one clarifying question.
- `ARCHITECTURE.md` — current architecture snapshot.
- `adr/` — top-level durable ADR history for this overlay. This replaces upstream examples that use `docs/adr/` for system-wide decisions.
- `openspec/changes/<change>/` — change-local artifacts.

Create or update `CONTEXT.md` lazily when a project-specific term is resolved. Do not create glossary entries for general programming concepts.

### OpenSpec artifact output

For `grill.md`, record:

- context read;
- plan summary;
- question loop with recommended answers and resolutions;
- resolved terms and `CONTEXT.md` updates;
- OpenSpec artifact updates applied or required;
- ADR candidates;
- `Open Questions: None` before design can proceed, unless an explicit one-time override is recorded.

For `design-review.md`, record the same structure focused on stress-testing the technical design. If findings require changes to proposal/specs/grill/design/context/ADR planning/test planning, update those files or block the next gate until they are updated.
