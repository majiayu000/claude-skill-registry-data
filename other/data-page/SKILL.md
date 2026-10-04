---
name: data-page
description: Use when building a page, chart, dashboard or write-up whose value is its numbers — spend breakdowns, usage analysis, metrics reports, research findings with figures — for Bryan or anyone he will share it with.
user-invocable: true
---

# Data Page or Analysis

**Read `<project>/.claude/workflow-overrides/data-page.md` first, if it exists.** It replaces or adds steps by name (for example a project's own reconcile script). Every step it does not name runs as written here.

## Size it first

**A fix Bryan named in a comment** (a label, a unit, a colour): make it, re-render the changed view at 430 wide and one desktop width, reply on the thread. Nothing else applies.

**A fix that changes a figure** also runs step 3b on that figure.

**Anything else** runs every step below.

## Steps, and the done-when line each one leaves

Put these on the task row as done-when lines when you start (`rewrite_task` keeps existing line ids), and report each with `report_done_when`. A line is `met` only with the proof named here.

| # | Step | Done-when line | Proof |
|---|---|---|---|
| 1 | Rough pass with Bryan: quick exploratory charts, the figures that stand out, the story in three sentences. File it as a review item and **do not build the polished version until he answers.** | Story agreed with Bryan | The review item, and his answer |
| 2 | Build the polished version against the agreed story. | Built | The page link |
| 3 | Run three reviewers in parallel, each a separate agent: **(a)** every data source and transformation is valid; **(b)** every figure and headline traces to its source, and nothing else; **(c)** a `ux-review` walk that the insights read clearly. A defect sends the page back to step 2. | Sources, figures and clarity reviewed | Each reviewer's report, with defects marked fixed |
| 4 | For a page: render at 1920, 1180 and 430 wide. Fails on a sideways scroll at 430. A markdown write-up skips this line. | Renders at three widths | The three screenshots |
| 5 | Hand off: file the review item. | Filed for review | The review item link |

**Step 1 is a step of the work, not a permission request.** An approved task does not skip it, and neither does Bryan being asleep: file the item, pick up other work, and resume when he answers. If his answer will land after the deadline, say that on the item.

**Your own spot-check does not satisfy 3b.** Recomputing totals by a second method is worth doing, but in 4 of 4 measured runs where the builder's own checks passed, a figures-only reviewer still found defects. The proof is the separate reviewer's report.

## No workspace board?

Put the same lines and proofs in the hand-off message or the PR body, one line each.
