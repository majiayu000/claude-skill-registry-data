---
name: quality
description: Use to see which checks failed or warned, what was quarantined, how fresh the tables are, and whether each table is safe to use today.
argument-hint: "[date or period]"
---

# Quality

The job: say what the checks stopped and why, and whether each table can be trusted today. It reads, it never changes a check.

Input: a date or a period, the last month by default.

## Steps

1. The status of the runs: succeeded or failed, the check that failed a run, and the tasks that were skipped.
2. Every check, layer by layer: passed, warned or failed, with the table and the rows it affects.
3. The quarantine: every stopped file and row, with the rule it broke.
4. Freshness: when every table the consumers read was last rebuilt, against its service level.
5. The reconciliation with the source, when the project has one: the counts and the totals on both sides.
6. The checks that fail most, and the ones that warn every day and nobody looks at anymore.
7. The checks that never failed: when each one was last tested with bad data, so you know it still works.
8. The verdict per table: safe to use, use with care, or do not use, with the reason.
9. Give the result as one web page.

## Output

One HTML file, like [references/quality.html](references/quality.html): the numbers of the period, the verdict per table, when the data was ready, every check on every day, the checks that failed most, the quarantine per day and the stale tables. Read it for the layout before you write the page.

## Reads

- the run records, the check results, the quarantine, the reconciliation

## Writes

- the web page only

## Never

- Never changes a check, never reruns a job, never releases a quarantined row.
