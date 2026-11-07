---
name: migration
description: Use when an old estate of jobs and tables has to move to a new platform, to inventory it, rate it, and write the migration plan with scenarios, acceptance numbers, the parallel run and the rollback.
argument-hint: "[old estate]"
---

# Migration

The job: from the old estate to a migration plan with scenarios, acceptance numbers, a parallel run and a rollback. It plans, it migrates nothing.

Input: the folder, the inventory or the documentation of the old estate.

## Steps

1. Inventory the old estate: jobs, tables, schedules, owners, consumers.
2. Explain every job in three plain lines: inputs, logic, output.
3. Draw the lineage of the old estate.
4. Rate each job: risk, size, value, dead or alive.
5. Propose the cut list, with the reason for each.
6. Gather the requirements for the new platform.
7. Compare at least two target platforms on the requirements.
8. Propose the migration type per job: lift and shift, re-platform, re-engineer.
9. Design the target: where each kept job lands.
10. Map old to new, one row per old output.
11. Propose the order, in waves, the smallest proven one first.
12. Three scenarios: best, expected, worst, with effort and risk.
13. Define the acceptance numbers, per output, with the tolerance.
14. Plan the parallel run: old and new side by side, every output compared, for how long, before the cutover.
15. Plan the history load, the cutover, the rollback and the decommission of the old jobs.
16. Write the migration plan, decisions marked open for the data engineer.

## Output

One migration plan: the inventory and its ratings, the cut list, the target, the waves, the scenarios, the acceptance numbers, the parallel run, the cutover and the rollback, with the open decisions marked.

## Reads

- the old estate, the knowledge of the new platform

## Writes

- the migration plan

## Never

- Never migrates anything: it plans.
