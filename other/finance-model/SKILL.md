---
name: finance-model
description: Build an integrated multi-year financial model — P&L, best, base and worst cases, valuation by multiples and DCF, and a sensitivity matrix — on top of the plan, forecast and budget. Use when the user is preparing to fundraise or make a major bet and needs a full model with valuation. Not for a quick scenario check on one decision; see /finance-scenario.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: finance
  phase: 5
  artifact: 05-model.md
---

# Model

Build the financial model for "$ARGUMENTS". Create an integrated model with scenario analysis, valuation, and sensitivity testing to support decision-making and fundraising.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"finance-model","workflow":"finance","phase":5,"project":"<project>","event":"skipped","artifact":"05-model.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 5 (Model) of the FP&A workflow (`finance`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `finance` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"finance-model","workflow":"finance","phase":5,"project":"<project>","event":"refused","artifact":"05-model.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"finance-model","workflow":"finance","phase":5,"project":"<project>","event":"started","artifact":"05-model.md","note":""}`.

Read `.singularskills/finance/<project>/04-budget.md`. If this file does not exist, tell the user:

> Phase 4 (Budget) has not been completed for "<project>". Run `/finance-budget <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context:**
   - Read `.singularskills/finance/<project>/01-assess.md` through `04-budget.md` for complete financial picture
   - Reference `references/financial-model-template.md` for scenario table structure

2. **Build integrated P&L model:**
   - Revenue model with driver-based projections
   - COGS and gross profit
   - Operating expenses by category
   - EBITDA and net income
   - Project 3-5 years with monthly detail for year 1

3. **Build scenario models:**
   - **Base case:** aligned with the forecast and budget
   - **Best case:** upside assumptions (faster growth, better margins)
   - **Worst case:** downside assumptions (slower growth, higher costs, churn)
   - For each scenario: revenue, expenses, cash flow, runway, break-even
   - Reference `references/financial-model-template.md` for scenario table format

4. **Valuation analysis** (if applicable):
   - Revenue multiples (based on comparable companies)
   - DCF analysis with WACC assumptions
   - Last-round valuation and implied metrics
   - Cap table impact of future fundraising scenarios

5. **Sensitivity analysis:**
   - Identify the 5-8 variables with the most impact
   - Show how changes in each variable affect key outputs
   - Create tornado chart data (which inputs swing outcomes most)

6. **Write the artifact** to `.singularskills/finance/<project>/05-model.md` with sections:
   - **Integrated P&L** — multi-year income statement
   - **Scenario Analysis** — best/base/worst case summaries
   - **Valuation** — multiples, DCF, and comparable analysis
   - **Sensitivity Matrix** — variable impact on key metrics
   - **Model Assumptions Log** — every input and its source/rationale

## Output

The model written to `.singularskills/finance/<project>/05-model.md`. Present a summary highlighting:
- Base case P&L trajectory
- Scenario range (worst to best)
- Valuation range
- Most sensitive variables

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"finance-model","workflow":"finance","phase":5,"project":"<project>","event":"finished","artifact":"05-model.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: finance-model
workflow: finance
phase: 5
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
