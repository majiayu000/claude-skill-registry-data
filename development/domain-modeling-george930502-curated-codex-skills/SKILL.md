---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline — challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `CONTEXT.md` for vocabulary is not this skill — that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

Before the first glossary write, read [`CONTEXT-FORMAT.md`](CONTEXT-FORMAT.md)
for file placement, single/multi-context routing, and format. Create files only
when the first resolved term needs them.

Before asking the user to decide anything, read
[`../grilling/NATIVE-INPUT.md`](../grilling/NATIVE-INPUT.md) and use that native
input contract. This applies whether this skill runs alone or through another
skill; never substitute a prose question.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in
`CONTEXT.md`, surface the conflict immediately and present the viable meanings
as one native decision.

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term
and present the materially distinct meanings as one native decision.

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you
find a contradiction, surface the evidence and present the viable resolutions
as one native decision.

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

When a candidate durable decision arises, read
[`ADR-FORMAT.md`](ADR-FORMAT.md) and create an ADR only when its three-part gate
passes.

Completion criterion: every resolved domain term is recorded once, code/docs
contradictions are surfaced, and only qualifying decisions become ADRs.
