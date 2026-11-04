---
name: review-plan
description: Review a plan in a fresh agent before approval. Use for /review-plan.
---
# review-plan

You review one plan under `.tmp/grunt/plans/` that someone else wrote. You start with no context from the writing session, and that is the point: judge the file, not the reasoning behind it. Format: `.rulesync/reference/plan-format.md`. Lessons: `.rulesync/reference/lessons.md`.

Slash `/review-plan {n|path}` only. Not a session flag. `/write-plan` runs it in a fresh agent after every write or revision. Run it yourself on any plan.

Read-only. Write nothing: not the plan, not a lesson, not a journal. The writer applies what it accepts and bumps the plan's `reviews` count in that save.

Rounds repeat: the first runs after `/write-plan`, another after each revision, and anyone can run one by hand. The count proves a round ran and was settled, not that it was good. A plan cannot move to `in-progress` until `reviews` is at least 1.

Scripts already enforce the format, the append-only `## Previous mistakes`, and the lesson citations. Do not re-check those. Check what a script cannot:

1. Read the plan in full.
2. Read its `## Previous mistakes`. Flag any leaf that brings a recorded mistake back.
3. Run `node .rulesync/scripts/lessons.mjs match` on the absolute paths the plan names. Read each matched lesson. Flag a lesson cited in Watch-outs that no leaf acts on.
4. Read each principle skill the plan names. Flag a leaf that goes against it.
5. Check the type row in `.rulesync/reference/scope.md` ## Types: a missing failing-test leaf, a missing Read leaf, or a named check dropped without a reason.
6. Flag a leaf that needs more planning before someone can do it: an open choice, a vague target, or a path that does not exist.
7. Flag a file the Steps must change that no leaf or allowlist names, and a caller or consumer the change can break that no leaf covers.

Reply with at most 10 findings, most severe first, one line each: `{leaf id or section}: {problem}; {fix}`. With nothing to flag, reply `no findings`. No praise and no summary.
