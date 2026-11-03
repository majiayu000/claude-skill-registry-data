---
name: analytics-metrics
description: Define the metrics that answer a team's questions — a metric tree of primary, input and guardrail metrics, each with formula, grain, inclusions, window, segments, source, owner and known traps. Use when the user needs agreed definitions before anyone builds a dashboard or analysis. Not for the financial ratios of a set of statements; see /finance-ratios.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: analytics
  phase: 2
  artifact: 02-metrics.md
---

# Metrics

Define the metrics for "$ARGUMENTS" so that everyone who computes one gets the same number.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"analytics-metrics","workflow":"analytics","phase":2,"project":"<project>","event":"skipped","artifact":"02-metrics.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 2 (Metrics) of the Decision Analytics Cycle workflow (`analytics`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `analytics` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"analytics-metrics","workflow":"analytics","phase":2,"project":"<project>","event":"refused","artifact":"02-metrics.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"analytics-metrics","workflow":"analytics","phase":2,"project":"<project>","event":"started","artifact":"02-metrics.md","note":""}`.

Read `.singularskills/analytics/<project>/01-questions.md` for the decisions and the priority questions.

## Process

1. **Find metrics already defined:** read `.singularskills/support/<project>/` and `.singularskills/finance/<project>/` artifacts and the user's existing reports. A metric defined there is referenced by its name and file, never redefined; note any conflicting definitions of the same name.

2. **Build the metric tree** as `references/metric-definitions.md` describes: for each decision area, one primary metric, the input metrics that drive it, and the guardrails that must not get worse. Keep the tree to about a dozen metrics.

3. **Define each metric** with every field of the template in `references/metric-definitions.md`: name, question, formula (in words and pseudo-SQL), unit and grain, inclusions and exclusions, window, segments, source, owner and traps. Where a field is unknown, write `<unknown: …>` and list it under Open questions.

4. **Check every question is covered:** each priority question from `01-questions.md` maps to at least one metric, and each metric answers at least one question. Drop metrics that answer none.

5. **Name the traps** that apply to each metric from the list in `references/metric-definitions.md`: moving denominators, averages of averages, Simpson's paradox, survivorship, time zones and late data, definition drift.

6. **Write the artifact** to `.singularskills/analytics/<project>/02-metrics.md` with sections:
   - **Metric tree** — primary, inputs and guardrails per decision area
   - **Definitions** — one block per metric, every template field
   - **Referenced metrics** — metrics defined elsewhere, with their file
   - **Coverage** — question → metric mapping

## Output

The metric definitions written to `.singularskills/analytics/<project>/02-metrics.md`. Present a summary to the user highlighting:
- The primary metric for each decision area
- The guardrails
- Every `<unknown: …>` field and conflicting definition

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"analytics-metrics","workflow":"analytics","phase":2,"project":"<project>","event":"finished","artifact":"02-metrics.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: analytics-metrics
workflow: analytics
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
