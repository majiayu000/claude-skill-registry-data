---
name: big-review
description: Use once a month, or when the platform feels slow, heavy or cluttered, to review the whole platform from the query logs and the repo, and propose improvements with effort and risk.
argument-hint: "[period]"
---

# Big review

The job: one review of the whole platform, from what the consumers use to what nobody uses, every proposal with its effort and risk. It changes nothing.

Input: the period, the last month by default, with at least 90 days of query logs for the unused data.

## Steps

1. Usage: the most read tables, the slowest queries, and the rows scanned against the rows needed.
2. Unused data: the tables and columns nobody read in the last 90 days, checked against the month-end, quarter-end and year-end jobs, the stale tables, and the storage they take.
3. Dead code: the functions, parameters and SQL that nothing uses.
4. Code health: duplicated logic, outdated documents and the longest functions.
5. Data quality: the checks per layer, and the layers without any.
6. Proposals: each one with the effort and the risk, in order of priority. A table is deprecated first and dropped only after its owner agrees.
7. Give the result as one web page.

## Output

One HTML file, like [references/big-review.html](references/big-review.html): the numbers on top, one section per step with a chart or a table, the proposals last. Read it for the layout before you write the page.

## Reads

- the query logs, the catalog, the pipeline code, the documents

## Writes

- the web page only

## Never

- Never changes anything: it proposes, the data engineer decides.
