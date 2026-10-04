---
name: migrate-then-delete
description: "Use when introducing a new internal API while old callers still exist. Move every caller and delete the old API in the same change. No compatibility layer left behind. Only for APIs nothing outside your deploy depends on."
disable-model-invocation: true
kind: principle
---

# Migrate, then delete

Once a new API is the right design, move the callers over and delete the old one in the same change. Don't leave the old path alive because some internal callers haven't moved yet. Move them.

Keeping both paths means two ways to do everything, cleanup that never happens, and a codebase that only grows.

## How

- **List every caller first.** Grep for it. Know the full set before you start.
- **Move them all, then delete.** Same PR, or same stack of PRs. The old API doesn't survive the change.
- **Adapters are a temporary exception, not a design.** If you need one to land the change in pieces, give it a deletion date and a follow-up that removes it. An adapter with no removal plan is the old path with a new name.
- **Tests follow the new contract.** Update tests to assert the new API. Delete tests that only guarded how the old one worked inside. A pile of tests protecting a deleted implementation isn't coverage, it's weight.

## When this applies

Only when nothing outside your deploy depends on the old shape.

- Internal APIs and internal call sites. Yes.
- Anything a version you didn't deploy can read: a public API, a stored format, a queue message, a config file an agent mid-task is holding. No. That's data. Data changes go add first, migrate, then remove, with both versions working in between.

The test: can a process you don't control call it or read it? If yes, it's not internal, and this rule doesn't apply.
