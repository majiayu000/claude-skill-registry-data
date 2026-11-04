---
name: write-roadmap
description: "Write an ordered program of plans under .tmp/grunt/roadmaps/. Use for /write-roadmap. Stops for y, which locks and runs it."
---
# write-roadmap

You author the roadmap. First read `principle-sequence-verifiable-units` and follow it. Persist under `.tmp/grunt/roadmaps/` via Write (hook runs `.rulesync/scripts/persist-roadmap.mjs`). Copy the shape below. All boxes `[ ]`. Status stays `draft` until the user replies `y`.

Before you ask the user, read `principle-never-block-on-the-human`. Ask only when the user alone can answer.

Two or more slices. One slice is `/write-plan`: say so and stop. Do not write a file.

Research until every slice is defensible. Ask only what changes the program. Then write the draft and stop.

After each save, spawn a fresh host agent whose prompt is only `/review-roadmap {n}` and the roadmap's absolute path (on Claude Code the `claude` agent type; grunt is not the reviewer). Accept or reject each finding with a reason. Apply accepted ones to the same file and add one `- review: …` entry each to `## Previous mistakes`. Bump `reviews` by one in the save that settles the round, even with no findings: send a bare `reviews: {n}` line above `ROADMAP_NAME:`. The save denies a lower count.

On feedback, revise the same file (a Write of the saved path updates it in place), add a `- feedback: …` entry for what the user rejected and what changed, and run `/review-roadmap` again. Never edit or drop an earlier entry.

On `y`, set `status: locked` on the same file, then run `/implement-roadmap {n}`. The save denies the lock while `reviews` is 0. Do not run `/write-plan` or `/implement-plan` from this skill.

Report the serial, the absolute path, the slice titles in order, the top risk, and the review findings you rejected with why. Stop and end the reply with exactly one line, `Reply "y" to run roadmap {n}.`, using the queue form from `/write-plan` when other reviewed plans or roadmaps wait. Ask for approval no other way.

## Shape

`ROADMAP_NAME:` is 3–6 words. The hook turns it into the slug and the frontmatter. Do not invent `serial`, `created`, or `source`.

````
ROADMAP_NAME: auth program

# auth-program

## Goal
Ship auth as two plans. The second plan waits on the first. Names stay reserved.

## Usage
Before:

```console
$ grunt init
reserved skills: commit, review
```

After:

```console
$ grunt init
reserved skills: commit, review, auth-types
```

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

## Previous mistakes
(none)
````

## Row rules

- Headings, this order only: Goal, Usage, Context, Decisions, Order, Watch-outs, Verify, Previous mistakes. No other `##`.
- Usage shows what a person or agent types and sees once the program lands, as `/write-plan` describes.
- Previous mistakes is `(none)` on a new roadmap, then one `- {feedback|verify|review|premise|slice}: {what was wrong} → {what changed}` line per entry, optional ` (lesson: {slug})`. Append-only.
- Goal is 1–3 sentences.
- Context, Decisions, and Watch-outs are bullets. Each decision names the rejected alternative.
- Each slice is `N [ ] Title: {2–6 words}` then indented `Goal:` and `Why:`. Those lines are not checkboxes.
- Slice Goal is one sentence: what that plan ships.
- Slice Why is one or two sentences: why this slot, and what it unlocks.
- Omit `Location` on a draft. `/implement-roadmap` fills it with the absolute plan path.
- No Type. No Commit. Those go on the child plan.
- Verify is 1–5 leaves, `N.M [ ]`, same grammar as a plan.
