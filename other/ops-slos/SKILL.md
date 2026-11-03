---
name: ops-slos
description: Define SLOs for a service — an SLI per critical user journey as good events over valid events, a target and window, the error budget computed, and an error budget policy for what each level of consumption triggers. Use when a team needs to decide how reliable a service must be and what happens when it is not. Not for customer support response targets; see /support-service-levels.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: ops
  phase: 2
  artifact: 02-slos.md
---

# SLOs

Decide how reliable each critical journey of "$ARGUMENTS" must be, and what the team does when it is not, as `references/slos-and-alerting.md` describes.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"ops-slos","workflow":"ops","phase":2,"project":"<project>","event":"skipped","artifact":"02-slos.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 2 (SLOs) of the Reliability Cycle workflow (`ops`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `ops` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ops-slos","workflow":"ops","phase":2,"project":"<project>","event":"refused","artifact":"02-slos.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"ops-slos","workflow":"ops","phase":2,"project":"<project>","event":"started","artifact":"02-slos.md","note":""}`.

Read `.singularskills/ops/<project>/01-inventory.md` for the services, tiers and critical journeys.

## Process

1. **Pick the journeys:** the critical user journeys of the tier 1 and tier 2 services in `01-inventory.md`.

2. **Define an SLI per journey** as **good events ÷ valid events**: availability, latency at a percentile and threshold, correctness or freshness, whichever users notice. Say exactly which events count as valid (excluding health checks and bots) and where the data comes from.

3. **Set the SLO:** the target and the window (a rolling 28 or 30 days unless the business needs calendar months), each labelled `target`. Set the target where users would start to notice failures; raise it above what the service already achieves only if the team can afford the work. With past data, compute current attainment and say so.

4. **Compute the error budget** with a script written to `.singularskills/ops/<project>/` and included beside the result: 1 − target, in time over the window and in failed requests per thousand. Scripts read the user's files where they keep them and write results under `.singularskills/`.

5. **Write the error budget policy:** what each level of budget consumption triggers (for example normal releases under 50%, a reliability check from 50% to 100%, and a freeze on all changes except P0 and security fixes once the budget is spent), who decides exceptions, and how disputes are settled. Mark it a **draft** until the user records who agreed it (service owners, product owner, on-call).

6. **Write the artifact** to `.singularskills/ops/<project>/02-slos.md` with sections **SLIs**, **SLOs**, **Error budgets**, **Error budget policy** (with its status, draft or agreed, and who agreed) and **Current attainment** (`computed` or `not measured`).

## Output

The SLOs written to `.singularskills/ops/<project>/02-slos.md`. Present a summary to the user highlighting:
- Each SLO and its error budget in minutes
- What the policy freezes and when
- Who still has to agree the policy

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"ops-slos","workflow":"ops","phase":2,"project":"<project>","event":"finished","artifact":"02-slos.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: ops-slos
workflow: ops
phase: 2
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
