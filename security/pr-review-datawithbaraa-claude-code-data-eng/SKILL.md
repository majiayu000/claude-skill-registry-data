---
name: pr-review
description: Use before a pull request or another change goes in, on a file, the current diff or a branch, to review it pass by pass against the project's own standards, with pushback.
argument-hint: "[branch, diff or file]"
---

# Pull request review

The job: review one change in fixed passes, in this order, and report every finding with its fix. It never edits.

Input: a file, the current diff, or a branch before its merge.

## Steps

1. Scope the change: the files, the lines and the purpose of the change.
2. Security: secrets in the code, access rights, personal data that reaches the consumers.
3. Correctness: data types, money, the numbers the change produces, and the same result on a rerun or a backfill.
4. Tests: the change comes with tests, they cover the edge cases, and they pass.
5. Contract: the grain, the columns and the types against the data contracts of the consumers.
6. Portability: absolute paths and anything else that only runs on one machine.
7. Duplication: code that already exists in the project.
8. Architecture and performance: how it connects to the warehouse, what it loads into memory, what it scans.
9. Documentation: the runbook and the data contract for anything new.
10. Style: the project's code style.
11. For every finding: the risk, the file and line, the rule from the standards, and the suggested change.
12. The verdict: approve, or changes requested. Give the result as one web page.

## Pushback

A finding the author declines stays in the report as declined, with the reason given. It is never dropped and never quietly downgraded.

## Output

One HTML file, like [references/pr-review.html](references/pr-review.html): the change and its verdict on top, then every finding with the code, the rule and the suggested change, high risk first. Read it for the layout before you write the page.

## Reads

- the change, the standards, the tests, the data contracts of the consumers

## Writes

- the web page only

## Never

- Never edits the change, never pushes, never merges.
