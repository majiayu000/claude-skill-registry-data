---
name: create-branch
description: >-
    Create a new git branch for a piece of work the canonical way — branch off an up-to-date main
    by default (or an explicitly named base branch), update main first, and name it by the
    high-level change only, never by internal scaffolding like batch numbers, plan numbers, or task
    IDs. Use whenever you start new work, cut a branch, or are unsure what to name a branch in
    plainworks.
---

# Creating a branch for plainworks work

A branch and its eventual PR must read as a **standalone unit of change** to a reviewer who has no knowledge of how the work was planned. Two rules make that true: branch off the right, up-to-date base, and name the branch after the actual change — nothing else.

## Golden rule: update main, then branch off it

Unless the request explicitly says to build on another branch, refresh remote refs, fast-forward `main`, and base new work on the latest `main`. Never branch off a stale local `main` or whatever happens to be checked out.

```bash
git fetch origin --prune                # refresh remote refs first — always
git switch main && git pull --ff-only   # update main before branching
git switch -c <branch-name> main
```

If (and only if) the request says to stack on top of another branch, base on that branch and keep it current:

```bash
git fetch origin --prune
git switch -c <branch-name> origin/<base-branch>
```

Check the working tree with `git status` first. Uncommitted changes follow you onto the new branch — usually what you want when you have already started editing, but confirm it is intentional rather than dragging along unrelated edits.

## Naming: describe the change, not internal details

- **Prefix with your username**, then a short kebab-case summary of the change: `kbukum/<short-change-summary>` (e.g. `kbukum/channel-sse-reconnect`, `kbukum/auth-bff-cookie-seam`).
- Name by the actual change: the package/capability touched and the outcome.
- Short, lowercase, hyphen-separated; no spaces, no `wip`, no trailing noise.

**Never** put internal, sequencing, or local-only information in the name:

- ❌ plan/batch/step numbers: `step-08-auth`, `batch-5`, `phase2`
- ❌ ticket scaffolding that isn't the change itself
- ❌ session-, machine-, or tool-local detail

If you catch yourself writing `step-8-...`, ask "what does this change actually do?" and name it that. Each branch stands alone; there is no "step 8" from a reviewer's perspective.

## After the branch exists

This skill **creates the branch and leaves the edits uncommitted** — the maintainer commits and pushes, and opens a PR (in **draft**) only when explicitly asked. Do not commit, push, or open a PR as part of creating the branch.
