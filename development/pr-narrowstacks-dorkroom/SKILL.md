---
name: pr
description: Dorkroom pull request conventions — scope and size, the repo PR template, labels, and screenshots. Use when opening, splitting, or describing a pull request.
user_invocable: true
---

# Pull Requests in Dorkroom

The hard requirements (template, labels, screenshots) live in the root
`CLAUDE.md` under "Pull Requests". This skill covers how to shape the PR itself.

## Scope and size

One PR does one thing and can merge on its own. Aim for under 200 changed lines,
and treat 500+ as a signal to split.
When a feature is bigger than that, split it along seams that each build and
pass `bun run test` on their own (e.g. logic in `packages/logic`, then the UI
that consumes it) and stack them, each based on the previous branch.

Keep unrelated fixes out, even small ones spotted along the way. Mention them in
"Additional Notes" or open an issue instead.

## Description

Start from `.github/PULL_REQUEST_TEMPLATE.md`; don't retype it, because it
changes. Fill every section:

- **Changes Made**: what changed and why, specific enough that a reviewer knows
  where to start in a multi-file diff.
- **Type of Change / Testing / Checklist**: tick only what is actually true.
- **Screenshots**: the `pr-screenshots` skill, or the one-line "no rendered
  output" statement.
- **Breaking changes**: call out anything that affects `@dorkroom/api` npm
  consumers, the public REST API, or persisted user data (localStorage keys,
  the iOS film log).

## Labels

Use only existing labels (`gh label list`): one type label plus the area labels
that apply, plus `claude`. Don't create labels (no `large`, no `wip`) without
asking.

## Before opening

Run `bun run test` and `bun run format`, and review your own diff for leftover
debug code and unrelated changes.
