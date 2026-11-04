---
name: write-roadmap
description: "Write an ordered program of plans under docs/roadmaps/. Use for /write-roadmap. Stops for lock. Does not implement."
---
# write-roadmap

You author the roadmap. First read `principle-sequence-verifiable-units` and follow it. Persist under `docs/roadmaps/` via Write (hook runs `.rulesync/scripts/persist-roadmap.mjs`). Copy the shape below. All boxes `[ ]`. Status stays `draft` until the user locks it.

Before you ask the user, read `principle-never-block-on-the-human`. Ask only when the user alone can answer.

Two or more slices. One slice is `/write-plan`: say so and stop. Do not write a file.

Research until every slice is defensible. Ask only what changes the program. Then write the draft and stop.

On lock, set `status: locked` on the same file and stop. Do not run `/write-plan` or `/implement-plan` from this skill.

Report the serial, the path, the slice titles in order, and the top risk. Stop for the lock.

## Shape

`ROADMAP_NAME:` is 3–6 words. The hook turns it into the slug and the frontmatter. Do not invent `serial`, `created`, or `source`.

```
ROADMAP_NAME: auth program

# auth-program

## Goal
Ship auth as two plans. The second plan waits on the first. Names stay reserved.

## Context
- Init owns reserved names

## Decisions
- D1. Fetch stays upstream. Rejected: a vendored snapshot.

## Order
1 [ ] Title: auth types
      Goal: Reserved names list the new skills.
      Why: Later slices add skills. This slot keeps init and INDEX together.
2 [ ] Title: commit diff pass
      Goal: Commit skills strip narrating comments.
      Why: Every later land goes through commit.

## Watch-outs
- (none)

## Verify
3 [ ] Verify
3.1 [ ] both child plans have finished Verify
```

## Row rules

- Headings, this order only: Goal, Context, Decisions, Order, Watch-outs, Verify. No other `##`.
- Goal is 1–3 sentences.
- Context, Decisions, and Watch-outs are bullets. Each decision names the rejected alternative.
- Each slice is `N [ ] Title: {2–6 words}` then indented `Goal:` and `Why:`. Those lines are not checkboxes.
- Slice Goal is one sentence: what that plan ships.
- Slice Why is one or two sentences: why this slot, and what it unlocks.
- Omit `Location` on a draft. `/implement-roadmap` fills it with the plan path (`.tmp/grunt/plans/{file}` or absolute).
- No Type. No Commit. Those go on the child plan.
- Verify is 1–5 leaves, `N.M [ ]`, same grammar as a plan.
