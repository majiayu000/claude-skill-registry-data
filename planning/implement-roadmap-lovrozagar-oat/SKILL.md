---
name: implement-roadmap
description: >-
  Run a locked roadmap in order. Use for /implement-roadmap. Writes each missing
  plan, then /implement-plan. Refuses a draft.
---
# implement-roadmap

You run the roadmap in this session. Format: `.rulesync/reference/roadmap-format.md`.

Refuse `status: draft`. Say it is not locked and stop. Do not write a plan.

Accept `locked` or `in-progress`. Set `in-progress` when you start. Same session. Do not spawn a subagent per slice.

For each open slice, in order:

1. If `Location` is absent, run `/write-plan` from that slice's Title, Goal, and Why. Read the roadmap's `## Previous mistakes` first and put each entry that touches this slice in the plan's Watch-outs. The lock is the approval: do not stop for plan approval. `/write-plan` picks the type and the `commit:` subject. If it hits a plan-shaping question, stop and leave the roadmap `locked` or `in-progress`.
2. Set `Location` to the absolute plan path `/write-plan` reported. Do not write a second plan when Location is already set.
3. Run `/implement-plan` on that plan. Do not stop between slices.
4. Mark the slice `[x]` only after that plan's Verify is done.
5. Read that plan's `## Previous mistakes`. For each entry that changes a Decision, the Order, or a later slice's Goal or Why, add `- slice: {what plan N found} → {what changed in the roadmap}` to the roadmap and make that change in the same save. Earlier entries stay.

A failed program Verify adds `- verify: …` to the roadmap. Stop on a blocker, a failed Verify, or a plan-shaping question.

When every slice and Verify are `[x]`, promote before `done`: the roadmap lives in `.tmp/` and is lost with it. For each roadmap entry that will happen again after this program, run `node .rulesync/scripts/lessons.mjs match` on the files involved, then `hit` the matching lesson with `--evidence "roadmap {n}"` or write a new one (`.rulesync/reference/lessons.md`). Then set `status: done`.

A slice's Why stays on the roadmap. Do not add a Why heading to the child plan.
