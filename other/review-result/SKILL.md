---
name: review-result
description: Machine-readable findings count that closes every review or QA report for the task board.
---

# Review Result Marker

A review or QA pass moves the session's tasks into the task board's **In Review** column. The board
learns the outcome only from this marker; without it the cards show **result not read** and stay in
review. Design: `docs/specs/task-board.md` § In Review.

## Rule

The last line of the final report of any review or QA pass is exactly:

```
<!-- review-result: findings=N -->
```

| Field | Value |
|-------|-------|
| `N` | Number of findings the user must act on: every blocking or non-blocking defect, gap or failed check you reported. `0` means the work passed |

- Emit it once, after the **Ran on:** table, as the final line.
- Count what you reported, not what you considered: a finding you dropped as speculative is not counted.
- A pass that could not run (missing environment, nothing to review) emits no marker — say why instead.
- Parallel reviewers each emit their own marker; the board sums the markers of distinct reports. A report counts once, by its last marker, so never repeat a marker earlier in the same report.
- A routing-only pass (`code-reviewer` in router mode, which only delegates) emits no marker: the specialists it spawns each emit theirs.
- Do not emit it from a pass that is not a review or QA of work done (planning, implementation, docs).
