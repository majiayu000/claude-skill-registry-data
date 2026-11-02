---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model. Trigger on ADR phrases (record, write, supersede an ADR).
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline — challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `CONTEXT.md` for vocabulary is not this skill — that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Use the glossary location declared by `AGENTS.md`; this harness defaults to
`.repo-context/CONTEXT.md`, with decisions in `docs/adr/`. Reuse an existing
root `CONTEXT.md` in other repos rather than creating a competing glossary.
If a `CONTEXT-MAP.md` exists at the root, follow its per-context locations.
Layout and selection: [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) § Single vs multi-context repos.

Create files lazily — only when documentation work is authorized and you have
something to write. If no glossary exists, use the declared location or
`.repo-context/CONTEXT.md` when the first term is resolved. If no `docs/adr/`
exists, create it when the first ADR is needed. Below, `CONTEXT.md` means the
selected glossary, not necessarily a root file.

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

When a term is resolved and documentation changes are authorized, update
`CONTEXT.md` using [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md). During analysis-only
work, report proposed terms and decisions without creating or editing files.

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer an ADR when the decision is hard to reverse, surprising without context, AND the result of a real trade-off — all three, or skip it. The full gate, what qualifies, and the format are in [ADR-FORMAT.md](./ADR-FORMAT.md).
