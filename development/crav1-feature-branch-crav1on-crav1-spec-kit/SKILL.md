---
name: crav1-feature-branch
description: >-
  Create or check out feat/<slug> (one branch for spec+build) or spec/<slug>
  (specify-only; build later on feat/<slug>). Use on brownfield specify or
  before implement if still on the default branch. Prompt; never silent
  checkout. Do not push. Do not open a PR.
disable-model-invocation: true
icon: git-branch
color: blue
---

# Feature branch

Get this change **off the default branch**. Prompt; do not silently `git checkout -b`. Do not push. Do not open a pull request unless they **explicitly** ask in this chat.

Other skills follow this file (drop-in: `.cursor/skills/crav1/crav1-feature-branch/SKILL.md`; plugin: sibling `skills/crav1-feature-branch/SKILL.md`). Standalone command: `/crav1-feature-branch`.

## Detect

Run git (PATH fallback if needed). If not a repo, skip.

- Current branch: `git branch --show-current`
- Default branch: `git symbolic-ref refs/remotes/origin/HEAD` (e.g. `origin/main`) if that exists; else `main`, else `master`, else `develop`
- Slug: from the spec folder they @, else the slug this specify pass is about to write, else ask
- Dirty: `git status --porcelain` ignoring `agent-tools/`

**Skip** (no prompt) when any of these is true:

- No git repo, or no commits yet (empty greenfield)
- Already on `feat/<slug>` or `spec/<slug>` for **this** slug
- Already on a non-default branch they chose (leave it). Exception: they are on `spec/<slug>` and this is a **build** skill — see **Build on a spec-only branch**
- They already answered this prompt in this chat (`stay` / branch created)
- Parent passed `branch: already-done`

## Prompt (questions tool; first option is the default)

**Specify** (spark / ideas / intake, before writing spec files):

1. **`feat/<slug>`** — one branch for this spec **and** later build (default, **first/top**)
2. **`spec/<slug>`** — specify-only. Merge this to the default branch (PR in GitKraken or your git host when they want). Build later on `feat/<slug>` from that default so another feature can be specified while this one is built
3. **Stay** on the current branch
4. **Other** — they name the branch

Intake (several slugs): one branch for the dump. Slug = short landscape kebab, or `system` if unnamed. Options are `feat/<that>` vs `spec/<that>`.

**Build** (implement / complete-task / complete-tasks, before the first code change or worker):

1. **`feat/<slug>`** — create/check out from the **current default** (default, **first/top**). Use this after a spec-only branch is on default, or when still on default
2. **Stay**
3. **Other**

Do not offer `spec/<slug>` on a build prompt.

If the working tree is dirty (other than `agent-tools/`), **do not checkout**. Tell them `/crav1-finalize-commit` (or stash themselves). Re-ask branch after the tree is clean.

## Checkout

Only after they pick a branch name that is not “stay”:

```text
git checkout -b <name>
```

If `<name>` already exists: `git checkout <name>` (do not `-B`, do not reset).

Never `git push`. Never create a PR. Never commit as part of this skill.

Then continue the parent skill on the new branch (write spec, or start the worker).

## Build on a spec-only branch

If they start implement / complete-task / complete-tasks while **on `spec/<slug>`**:

Stop. Do not write application code on a specify-only branch.

Offer:

1. Wait until `spec/<slug>` is on the default branch, then `/crav1-feature-branch` → `feat/<slug>` (recommended)
2. Convert: rename/check out `feat/<slug>` from here and treat it as the one-branch flow (spec+build together)
3. Stay and specify more (no code)

## Spec-first (after plan)

When `/crav1-plan-from-spec` has written `plan.md` / `tasks.md` on `spec/<slug>` (or they chose specify-only earlier):

- Next: `/crav1-finalize-commit` (no push), then **they** open a PR for this branch when they want the spec on default
- Do **not** start `/crav1-implement-task` on `spec/<slug>`
- After that PR is merged (they say so): `/crav1-feature-branch` with this slug → `feat/<slug>` from default, then implement / complete-task

If they planned on `feat/<slug>` (one-branch default), skip spec-first. Implement on the same branch.

## Hard rules

- Prompt; never silent checkout.
- `feat/<slug>` is the default one-branch flow. `spec/<slug>` is the optional specify-then-build split.
- No push, no PR, no `git commit` in this skill.
- Do not throw away uncommitted work.
- Do not create branches in an empty repo with no commits.
