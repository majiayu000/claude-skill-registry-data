---
name: finance-forecast
description: Project monthly revenue, expenses and cash flow from the plan's drivers, with runway, break-even timing and whether KPI targets are reachable. Use when the user has planning assumptions and asks what revenue, burn and cash will look like over the coming months or years. Not for splitting spend by department; see /finance-budget.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: finance
  phase: 3
  artifact: 03-forecast.md
---

# Forecast

Project the financial forecast for "$ARGUMENTS". Build a driver-based model that translates planning assumptions into monthly revenue, expense, and cash flow projections.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"finance-forecast","workflow":"finance","phase":3,"project":"<project>","event":"skipped","artifact":"03-forecast.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 3 (Forecast) of the FP&A workflow (`finance`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `finance` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"finance-forecast","workflow":"finance","phase":3,"project":"<project>","event":"refused","artifact":"03-forecast.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"finance-forecast","workflow":"finance","phase":3,"project":"<project>","event":"started","artifact":"03-forecast.md","note":""}`.

Read `.singularskills/finance/<project>/02-plan.md`. If this file does not exist, tell the user:

> Phase 2 (Plan) has not been completed for "<project>". Run `/finance-plan <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context:**
   - Read `.singularskills/finance/<project>/01-assess.md` for baseline data
   - Read `.singularskills/finance/<project>/02-plan.md` for assumptions and KPI targets

2. **Build revenue forecast:**
   - Model each revenue stream separately
   - Apply growth assumptions (new customers, churn, expansion, pricing changes)
   - Account for seasonality and ramp periods
   - Calculate monthly and annual totals
   - Reference `references/financial-model-template.md` for revenue model structure

3. **Build expense forecast:**
   - Project fixed costs (rent, salaries, subscriptions)
   - Project variable costs tied to revenue drivers
   - Include planned headcount additions and timing
   - Account for one-time costs (equipment, setup, legal)

4. **Build cash flow forecast:**
   - Map revenue to cash collections (considering payment terms)
   - Map expenses to cash payments
   - Include capital expenditures and financing
   - Calculate monthly net cash flow and ending balance
   - Determine runway and break-even timing

5. **Validate against KPIs:**
   - Check if the forecast achieves the KPI targets from the plan
   - Identify gaps and what would need to change
   - Note dependencies and risks

6. **Write the artifact** to `.singularskills/finance/<project>/03-forecast.md` with sections:
   - **Revenue Forecast** — monthly projections by stream
   - **Expense Forecast** — monthly projections by category
   - **Cash Flow Forecast** — monthly cash in, cash out, net, balance
   - **Key Metrics Over Time** — MRR, gross margin, burn rate, runway
   - **KPI Achievement** — projected vs target values
   - **Forecast Risks** — key sensitivities and downside scenarios

## Output

The forecast written to `.singularskills/finance/<project>/03-forecast.md`. Present a summary highlighting:
- Revenue trajectory and growth rate
- Burn rate and runway
- Whether KPI targets are achievable
- Top forecast risks

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"finance-forecast","workflow":"finance","phase":3,"project":"<project>","event":"finished","artifact":"03-forecast.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: finance-forecast
workflow: finance
phase: 3
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

End the artifact with this paragraph, verbatim:

> **Not financial or tax advice.** This artifact is generated analysis for review by a qualified accountant or financial professional before any filing, reporting or decision relies on it.
