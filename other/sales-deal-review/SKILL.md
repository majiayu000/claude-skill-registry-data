---
name: sales-deal-review
description: Review one closed deal — won, lost or no decision — with the seller's account and the buyer's account kept separate, causes rated by how well the buyer's own words support them, and what to repeat or change. Use when a deal has ended and the seller wants to learn from it, even if it never went through the earlier steps. Not for patterns across many deals; see /sales-win-loss.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: sales
  phase: 6
  artifact: 06-review.md
---

# Review

Learn from the closed deal in "$ARGUMENTS", as `references/win-loss.md` describes: the seller's view and the buyer's view are different evidence.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"sales-deal-review","workflow":"sales","phase":6,"project":"<project>","event":"skipped","artifact":"06-review.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 6 (Review) of the Deal Cycle workflow (`sales`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `sales` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own; this one has no gate, since it needs no earlier artifact.

Before you start work, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"sales-deal-review","workflow":"sales","phase":6,"project":"<project>","event":"started","artifact":"06-review.md","note":""}`.

None required: a deal can end at any phase, and many deals worth reviewing never went through this workflow. Read whichever of `.singularskills/sales/<project>/01-qualify.md` to `05-close.md` exist.

## Process

1. **Get the outcome and both accounts:** won, lost or no decision; the seller's account (notes, the user's own view); and the buyer's account, from an interview, email or debrief the user supplies. Ask once for the buyer's account if none was given.

2. **With no buyer account,** write **no buyer input** at the top of the review, keep every cause as seller-reported, and offer a short neutral interview guide (open "what" and "why" questions, as `references/win-loss.md` lists).

3. **Lay out both accounts side by side:** what the seller thinks happened and what the buyer said, never merged. Quotes from the buyer drop people's names.

4. **Rate each cause** by how well the buyer's own words support it: **confirmed by the buyer**, **seller-reported only**, or **contradicted by the buyer**. A reason only the seller gave is not reported as the cause. When "price" is a reason, check it against what the buyer said before accepting it.

5. **Compare with the plan:** where the earlier artifacts exist, which unknowns from qualification turned out to matter, and where the deal left the plan.

6. **What to repeat and what to change,** each with an owner.

7. **Write the artifact** to `.singularskills/sales/<project>/06-review.md` with sections **Outcome**, **Seller's account**, **Buyer's account** (or **no buyer input**), **Causes**, **Against the plan** and **Lessons**.

## Output

The review written to `.singularskills/sales/<project>/06-review.md`. Present a summary to the user highlighting:
- The outcome and the causes the buyer confirmed
- Any seller-reported cause the buyer contradicted
- The one thing to change on the next deal

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"sales-deal-review","workflow":"sales","phase":6,"project":"<project>","event":"finished","artifact":"06-review.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `none`, as this phase has no gate):

```yaml
---
skill: sales-deal-review
workflow: sales
phase: 6
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
