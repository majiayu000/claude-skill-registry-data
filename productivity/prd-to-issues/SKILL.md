---
name: prd-to-issues
description: Break a PRD or plan into independently-grabbable, vertically-sliced Markdown issues that an agent can work one-by-one in a ralph loop. Use when the user wants to turn a PRD or plan into issues, tickets, tasks, or work items, or asks to "slice this into issues" or "prep this for a loop".
license: MIT
effort: high
allowed-tools: Read Write Edit Bash Glob Grep Skill
---

# /prd-to-issues

Break a PRD or plan into independently-grabbable issues using **vertical slices** (tracer bullets), then file each as a local Markdown work order in `issues/`. The output is designed to be consumed by a **ralph loop** — an agent that picks the next eligible issue, implements it, and moves it to `issues/done/`, one iteration at a time.

## Issues are work orders, not archival docs

A PRD is durable and abstract on purpose. Issues are the opposite: **ephemeral, concrete work orders** consumed once by the loop and then retired. A fresh-context agent picking up an issue has no memory of this conversation — so be concrete:

- **Name the modules, files, and existing patterns** the agent should touch or copy. Stale pointers are fine; the issue is discarded the moment it's done.
- Reference the **PRD** for *why* and for the broader context; tell the issue *where* and *what*.
- Over-abstracting an issue "for durability" is the main way it becomes unexecutable. Don't.

## Workflow

You may skip steps the conversation already covered — capture, don't re-interview.

### 1. Locate the PRD or plan

The source is a **local Markdown file** (or content already in your context).

- If a PRD/plan is already in context, use it.
- Otherwise look in `prds/` (the `create-a-prd` default) with Glob, or ask the user for the path.
- Read it **in full** before slicing. If it's a raw plan rather than a PRD, it may have no numbered user stories — that's fine, degrade gracefully (see `user_stories` below).

### 2. Explore the codebase (optional)

If you haven't already, explore the repo to understand the current state and — critically — to identify **every integration layer a slice must cut through** (e.g. migration → model → service → route → UI → test). You can't draw a vertical slice without knowing the layers it crosses. Note concrete module names and existing patterns to cite in the issues.

### 3. Draft vertical slices

Break the PRD into **tracer-bullet** issues. Each issue is a thin vertical slice that cuts through **ALL** integration layers end-to-end — NOT a horizontal slice of one layer ("add the model", "add the route" are horizontal; avoid them).

Slicing criteria — every slice must be:

- **End-to-end** — observable behavior, from entry point to persistence and back.
- **One iteration** — completable by a single agent run / one focused PR. If it's too big to finish in one sitting, split it. This is what makes the loop work.
- **Independently grabbable** — implementable on its own once its blockers are done.
- **Typed** `afk` or `human`. `human` slices need a human in the loop (an architectural decision, a design review, a credential). `afk` slices can be implemented and merged without human interaction. **Prefer `afk`** — push `human` work earlier so it unblocks the afk run.

**Numbering is topological.** Order the slices so dependencies always point *backward*: issue `NNN` may only be `blocked_by` issues numbered lower than `NNN`. This makes "lowest-numbered eligible issue" trivially correct for the loop.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice show: **Title**, **Type** (afk/human), **Blocked by**, **User stories covered**.

Ask:

- Does the granularity feel right? Is each slice **one iteration's worth** of work — too coarse, too fine?
- Are the dependency relationships correct?
- Should any slices be merged or split?
- Are the right slices marked `human` vs `afk`?

Iterate until the user approves. If the quiz drags, hand off to `/grill-me` for a tighter loop.

### 5. Create the issue files

Once approved, create one file per slice in **dependency order** in `issues/`, named `NNN-slug.md` (zero-padded number = topological order; slug from the title). Derive **acceptance criteria from the PRD's user stories** — map the criteria already written under each story; don't invent new ones.

Then write `issues/README.md` as an index (a **derived view** — the issue files are the source of truth).

**Do NOT modify the parent PRD.**

<issue-template>

```markdown
---
slice: NNN
title: <short descriptive name>
type: afk            # afk | human
blocked_by: []       # list of slice numbers, e.g. [1, 3]; [] if none
user_stories: []     # PRD story numbers, e.g. [3, 7]; [] for a plan with no stories
prd: prds/prd-<feature-name>.md
---

# <Title>

## What to build

A concise description of this vertical slice — the end-to-end behavior, not a
layer-by-layer plan. Be concrete: name the modules, files, and existing patterns
to touch or copy. Reference the parent PRD for the broader why.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests cover the new behavior through its public interface

## Blocked by

- #NNN <title>   (or "None — can start immediately")

## User stories addressed

- Story 3, Story 7   (from the parent PRD; omit if the source was a plan)
```

</issue-template>

## The ralph-loop contract

Write this contract into `issues/README.md` so the loop and the human both know the rules. Completion is tracked by **file location, not a status field** — zero parsing, atomic with the commit:

- **Todo** = a file in `issues/*.md`. **Done** = a file moved to `issues/done/`.
- Each iteration, the agent takes the **lowest-numbered `afk` issue** in `issues/*.md` whose `blocked_by` are **all already in `issues/done/`**.
- It implements the issue, then `git mv`s the file into `issues/done/` **in the same commit** as the work. If an iteration dies mid-work, nothing moved — the next iteration simply retries it.
- The loop **skips** `human` issues and any issue with unmet blockers, and **stops** when no eligible `afk` issue remains — surfacing the leftover `human`/blocked issues for the user.
- "What's left" is just `ls issues/*.md`. No status to parse, no state to desync.

<index-template>

```markdown
# Issues — <feature name>

Derived from `prds/prd-<feature-name>.md`. **The issue files are the source of
truth; this index is a snapshot.**

## How the loop consumes these

1. Pick the lowest-numbered `afk` issue in `issues/*.md` whose `blocked_by` are all in `issues/done/`.
2. Implement it; `git mv` the file to `issues/done/` in the same commit.
3. Repeat until no eligible `afk` issue remains. `human` and blocked issues are left for review.

## Slices

| # | Title | Type | Blocked by | Stories |
|---|---|---|---|---|
| 001 | <title> | afk | — | 1, 2 |
| 002 | <title> | human | 001 | 3 |
| 003 | <title> | afk | 001 | 4, 5 |
```

</index-template>

After filing, tell the user how many issues were created, which are `human`, and where they live. Suggest pointing the ralph loop at `issues/`.
