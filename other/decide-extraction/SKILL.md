---
name: decide-extraction
description: When to extract an Action class vs inline code. Extraction decisions.
---

# Skill: Extraction

> "If you can name it with VerbNoun, extract it."

## The Decision

**Extract to Action when:**
- You can name it clearly: `CreateOrder`, `SendInvoice`
- 2+ consumers will call it
- Business rules exist beyond CRUD
- It dispatches events or composes other Actions

**Keep inline when:**
- Single CRUD operation with no rules
- One caller, forever
- Would just wrap `Model::create($data)`

## The Heuristic

Ask: *"If I delete this code, what breaks?"*

- **Multiple things** → Action
- **One thing** → Inline

## The Quick Test

| Ask Yourself          | Answer | Use    |
|-----------------------|--------|--------|
| Can name it VerbNoun? | No     | Inline |
| Multiple consumers?   | Yes    | Action |
| Has business rules?   | Yes    | Action |
| Dispatches events?    | Yes    | Action |
| Just wraps CRUD?      | Yes    | Inline |

## Real-World Examples

For concrete examples, see [examples.md](examples.md).
