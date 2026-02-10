---
name: plot-idea
description: >-
  Create a plan for review: idea branch, plan file, and draft PR.
  Part of the Plot workflow. Use on /plot-idea.
globs: []
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/skills
  version: 1.0.0-beta.1
compatibility: Designed for Claude Code and Cursor. Requires git and gh CLI.
---

# Plot: Create Idea

Create a plan for review: idea branch, plan file, and draft PR.

**Input:** `$ARGUMENTS` in the format `<slug>: <title description>`

Example: `/plot-idea sse-backpressure: Handle SSE client disconnects gracefully`

## Setup

Add a `## Plot Config` section to the adopting project's `CLAUDE.md`:

    ## Plot Config
    - **Project board:** <your-project-name> (#<number>)  <!-- optional, for `gh pr edit --add-project` -->
    - **Branch prefixes:** idea/, feature/, bug/, docs/, infra/
    - **Plan directory:** docs/plans/
    - **Archive directory:** docs/archive/

### 1. Parse Input

If `$ARGUMENTS` is empty or missing:
- Look at the conversation context for clues about what the user wants to plan
- If obvious, propose: "It looks like you want to plan `<slug>: <title>`. Shall I proceed?"
- Otherwise ask: "What's the idea? Usage: `/plot-idea <slug>: <title>`"

Extract `slug` and `title` from `$ARGUMENTS`:
- Everything before the first `:` is the slug (trimmed, lowercase, hyphens only)
- Everything after is the title (trimmed)
- If no `:` found, treat the entire input as the slug and ask for a title
- If slug contains invalid characters (spaces, uppercase, etc.), normalize it and confirm with the user

### 2. Pre-flight Checks

- Warn if working tree has uncommitted changes (offer to stash)
- Verify `gh auth status` has project scope
- Check that branch `idea/<slug>` does not already exist (if it does, ask whether to check it out or pick a new name)

### 3. Create Branch

```bash
git fetch origin main
git checkout -b idea/<slug> origin/main
```

### 4. Create Plan File

Write `docs/plans/<slug>.md` with this template:

```markdown
# <title>

> <title as one-line summary>

## Status

- **Phase:** Draft
- **Type:** feature | bug | docs | infra

## Changelog

<!-- Release note entry. Written during planning, refined during implementation. -->

- <user-facing change description>

## Motivation

<!-- Why does this matter? What problem does it solve? -->

## Design

### Approach

<!-- How will this be implemented? Key architectural decisions. -->

### Open Questions

- [ ] ...

## Branches

<!-- Branches to create when approved: -->
<!-- - `type/name` — description -->

- `feature/<slug>` — <description>

## Notes

<!-- Session log, decisions, links -->
```

Ask the user what **Type** to use (feature, bug, docs, infra). If the title makes it obvious, propose it and confirm.

### 5. Commit and Push

```bash
git add docs/plans/<slug>.md
git commit -m "plot: <title>"
git push -u origin idea/<slug>
```

### 6. Create PR

Create a **draft** PR (plan is still being written/refined):

```bash
gh pr create \
  --draft \
  --title "Plan: <title>" \
  --body "$(cat <<'EOF'
## Plan

See [`docs/plans/<slug>.md`](../blob/idea/<slug>/docs/plans/<slug>.md) on this branch.

Refine the plan, then mark ready for review with `gh pr ready`. Once reviewed, run `/plot-approve <slug>` to merge and start implementation.

---
*Created with `/plot-idea`*
EOF
)"
```

### 7. Add to Project Board

Read the `## Plot Config` section from `CLAUDE.md` for the project board name. If configured:

```bash
gh pr edit <number> --add-project "<project board name>"
```

If no project board is configured, skip this step.

### 8. Summary

Print:
- Branch: `idea/<slug>`
- Plan file: `docs/plans/<slug>.md`
- PR URL (draft)
- Next steps:
  1. Refine the plan (especially the **Branches** section)
  2. When ready for review: `gh pr ready <number>`
  3. After review: `/plot-approve <slug>`
