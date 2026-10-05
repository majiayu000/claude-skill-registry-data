---
name: to-features
description: Generate FEATURES.md at the repo root by reading CONTEXT.md and docs/adr/, then enumerating the user-facing features the domain implies. Use after /grill-with-docs has settled the domain language and before /to-prd writes per-feature specs. Bridges the product→engineering gap between domain understanding and feature specification — the missing step that mattpocock's chain doesn't cover natively.
---

# to-features

Generate `FEATURES.md` at the repo root by reading `CONTEXT.md` and the ADRs under `docs/adr/`, then enumerating the user-facing features the domain implies. Pairs with `/grill-with-docs` (upstream, produces CONTEXT.md/ADRs) and `/to-prd` (downstream, takes one feature → PRD).

## When to invoke

- After `/grill-with-docs` has produced or refined `CONTEXT.md`.
- Before `/to-prd` runs on any individual feature.
- If `FEATURES.md` already exists, treat this as a **refinement** — propose additions or strikethroughs based on the latest `CONTEXT.md` and ADRs. Never overwrite shipped (strikethrough) features.

## Process

1. **Read `CONTEXT.md`** for domain vocabulary, actors, and invariants.
2. **Read `docs/adr/*.md`** for architectural commitments that constrain what's buildable.
3. **Enumerate user-facing features** the domain implies:
   - One feature per line, kebab-case slug + one-line description.
   - Start with the actor: `user-can-…`, `admin-can-…`, `guest-can-…`.
   - **User-facing**, not internal — "User can reset password" not "Add bcrypt hashing."
   - Don't include implementation details — those land in PRDs downstream.
4. **Surface the list to the user** for review:
   - Anything missing?
   - Should any features be split or merged?
   - Are slugs unambiguous?
5. **Write `FEATURES.md`** at the repo root once approved.
6. (Optional, for local-markdown teams) `mkdir -p .scratch/<feature-slug>/issues` per pending feature to stub the layout downstream stages will fill.

## File format

```markdown
# Features

<!-- One feature per line. Strike through completed features; don't delete. -->

- [ ] user-can-sign-up — A user can create an account with email + password
- [ ] user-can-log-in — A user can sign in to their account
- [x] ~~user-can-reset-password~~ — ~~A user can reset a forgotten password~~ (shipped: #42)
- [ ] user-can-post-photo — A user can upload and share a photo

## Out of scope (rejected)

- ~~user-can-stream-video~~ — Rejected for v1 (see `.out-of-scope/video-streaming.md`)
```

## Discipline: when you finish a feature, strike it through (don't delete)

When a feature ships, mark its line in `FEATURES.md` with strikethrough + a shipped reference (issue number, PR, or tracker ID). Never delete the line. Strikethrough preserves:

- **Institutional memory** — what HAS shipped, not just what's pending.
- **Traceability** — link from `FEATURES.md` to the issue/PR that completed it.
- **Drift resistance** — you can't quietly drop a feature; dropping requires explicitly marking it out of scope (and writing the reason to `.out-of-scope/`).

Transformation on ship:

```
- [ ] user-can-reset-password — A user can reset a forgotten password
                              ↓
- [x] ~~user-can-reset-password~~ — ~~A user can reset a forgotten password~~ (shipped: #42)
```

## Why this skill exists

mattpocock's chain (`/to-prd`, `/to-issues`, `/triage`) is engineering-side — it assumes features come from product thinking that lives outside the toolchain. swe-workflow needs an explicit bridge between domain understanding (the output of `/grill-with-docs`) and per-feature specification (the input of `/to-prd`). That bridge is feature enumeration.

This skill is **engineering-adjacent**: it reads engineering artifacts (`CONTEXT.md`, ADRs), but its output (`FEATURES.md`) is in user-facing language. It's the deliberate seam where product reasoning enters the chain.

## When to skip

If your team handles feature enumeration in an external tool — Linear projects, Notion, Productboard, a shared spreadsheet, anything — skip `/to-features` and use the external source of truth. Pass features directly to `/to-prd`. This skill exists to fill the seam for teams without an existing product backlog convention, or for solo developers who'd rather keep feature tracking in the repo.
