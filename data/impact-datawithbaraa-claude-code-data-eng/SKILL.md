---
name: impact
description: Use before you change a table, a column or a function, to see what it is built from, what depends on it, who reads it, which checks cover it, and the safe order of the change.
argument-hint: "[table, column or function]"
---

# Impact

The job: the answer to "if I change this, what breaks", before the change is made.

Input: the table, the column or the function to change.

## Steps

1. Name the thing to change: a table, a column, a function or a file.
2. Upstream: everything it is built from, layer by layer.
3. Downstream: every table, view, report, test and job that reads it, found in the SQL and the code, never from memory.
4. The consumers: who queried the downstream tables in the last period, from the query logs, by role and team.
5. The checks and the tests that cover it, and the ones that will break.
6. The blast radius in numbers: tables, data products, consumers, queries, checks.
7. The safe order of the change: what to change first, what to rebuild, what to compare, and whom to tell.
8. Give the result as one web page, with the graph and the lists.

## Output

One HTML file, like [references/impact.html](references/impact.html): the numbers on top, the graph with the thing to change lit, upstream and downstream, then the consumers, the checks and the safe order of the change. Read it for the layout before you write the page.

## Reads

- the SQL, the code, the data contracts, the query logs, the checks and the tests

## Writes

- the web page only

## Never

- Never makes the change.
- Never guesses a dependency: a dependency is one found in the code or in the logs.
