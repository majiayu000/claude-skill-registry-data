---
name: queue-audit-read
kind: pattern
rule: queue-audit
description: Pattern of rule queue-audit. Load when the work queue audit has printed lines — running it, and the move that answers each kind of line.
---
<!-- rt-kit v0.34.0 · patterns/queue-audit-read.github.md · cbaed2fa70f3 · правится надстройкой, не здесь -->

# Reading the work queue audit

Pattern of the rule `queue-audit`. What must be true — the law `docs/constitution/delivery.md`.

## When to use

- The audit printed lines before a push, on taking a task or after a known merge.
- A line names a PR or a task, and the move for it is not obvious from the line.

## Running it

```bash
npm run check:board
```

Exit code 0 and no lines — the queue matches. Exit code 1 — every line is a discrepancy, and each
names its own move. The summary lines at the end are not discrepancies: they count what was read
and what was filtered out.

## What answers which line

| The line says                                        | The move                                                      |
| ---------------------------------------------------- | ------------------------------------------------------------- |
| a PR is open and its task is not in review           | `npm run task:move -- <номер> in-review`                      |
| a task is in review and has no open PR               | open the PR, or move the task back to work                    |
| the branch lags behind its base by N commits         | merge the base into the branch and push                       |
| the PR conflicts with the main branch                | merge the main branch in, resolve, push                       |
| no run on the tip                                    | a new commit, or close and reopen the PR as the line says     |
| a run pushed out of the queue                        | read that run's output, then rerun it — both commands are in the line |
| a draft with a green run                             | `gh pr ready <номер>`                                         |
| the PR has no reviewer                               | request the reviewer by a REST call                           |
| the last run of the main branch is red               | fix the main branch before new work                           |
| a task and its epic name each other one way only     | link the task as a sub-issue, or name it in the epic plan     |

## Common misses

- **A rerun instead of the move.** The second run prints the same line: a line is answered by its
  move.
- **A summary line read as a discrepancy.** The count of PRs with a base other than the main branch
  is not a discrepancy: it names what the host does not do for them.
