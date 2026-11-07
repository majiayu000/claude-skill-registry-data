---
name: cost-review
description: Use for the monthly cost review of the platform, to see where the compute and the storage money goes, per job, pipeline and table, and what to cut.
argument-hint: "[period]"
---

# Cost review

The job: where the money goes, per job, per pipeline and per table, and what to do about it. It proposes, it stops and deletes nothing.

Input: the period, the last month by default.

## Steps

1. Read the billing and usage records of the period: compute per job and pipeline, storage per table.
2. The top 10 jobs by cost, and what each one produces.
3. The cost per run of each scheduled pipeline, against the previous period.
4. The storage bill: what the storage costs per month, and the part spent on tables nobody reads. The list of those tables comes from the big-review skill.
5. Idle spend: clusters and warehouses that ran with nothing to do, and jobs that ran for nobody.
6. The spikes: which day, which job, and which change caused it.
7. Proposals, each with the saving per month and the risk, in order of the saving.
8. Give the result as one web page.

## Output

One HTML file: the cost of the period on top, the top jobs, the cost per run, the storage bill, the idle spend, the spikes, and the proposals last.

## Reads

- the billing and usage records, the run records, the query logs, the catalog

## Writes

- the web page only

## Never

- Never deletes a table, never stops a job, never changes a cluster: it proposes.
