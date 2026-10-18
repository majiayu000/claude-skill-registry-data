---
name: writing-great-skills
description: Deprecated compatibility reference for legacy manifests that write and edit skills. Prefer writing-for-agents for new work.
disable-model-invocation: true
---

# Writing Great Skills

Deprecated compatibility skill. New manifests use `writing-for-agents`.

A skill wrangles predictability out of a stochastic system. Predictability means the agent follows the same process every run, not that it produces the same output.

Bold terms are defined in [GLOSSARY.md](GLOSSARY.md).

## Invocation

Two invocation modes trade different costs:

- **Model-invoked**: keep a `description` so the agent can discover and use the skill. This spends **context load** every turn.
- **User-invoked**: set `disable-model-invocation: true`; the human must remember and request it. This spends **cognitive load**, not context.

Use model invocation only when the agent or another skill must reach the skill on its own. Use user invocation when human judgement should be the router.

## Description

A model-invoked **description** must state what triggers the skill.

- Front-load the leading word users and other skills will actually use.
- Keep one trigger per branch.
- Remove identity prose already obvious from the skill body.
- Prune synonyms that describe the same branch.

## Information Hierarchy

Put material where the agent needs it:

1. **Steps** in `SKILL.md`: ordered actions with checkable completion criteria.
2. **Reference** in `SKILL.md`: rules or definitions every branch needs.
3. Disclosed **reference**: linked files loaded only when a branch needs them.

Inline what every branch needs. Disclose what only some branches need. If a required pointer is missed in practice, sharpen the pointer before inlining the whole reference.

## Splitting

Split skills only when the split earns its cost:

- By invocation: create a model-invoked skill when a distinct leading word should trigger it independently.
- By sequence: split steps when visible later steps cause premature completion of the current step.

Do not split merely for tidiness. Do not merge separate invocation branches just to reduce file count.

## Pruning

Keep each behavior in one source of truth.

Check each sentence:

- Does it change agent behavior?
- Is it still relevant?
- Is it duplicated elsewhere?
- Is a stronger leading word enough?

Delete no-ops instead of polishing them.
