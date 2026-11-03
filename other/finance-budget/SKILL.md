---
name: finance-budget
description: Allocate the forecast into department budgets with headcount plans, spending authority levels, variance thresholds and a budget owner per department. Use when the user has a forecast and needs to decide how much each team can spend and who approves what.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: finance
  phase: 4
  artifact: 04-budget.md
---

# Budget

Allocate the budget for "$ARGUMENTS". Break down the forecast into departmental budgets with spending limits, approval thresholds, and accountability.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"finance-budget","workflow":"finance","phase":4,"project":"<project>","event":"skipped","artifact":"04-budget.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 4 (Budget) of the FP&A workflow (`finance`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `finance` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"finance-budget","workflow":"finance","phase":4,"project":"<project>","event":"refused","artifact":"04-budget.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"finance-budget","workflow":"finance","phase":4,"project":"<project>","event":"started","artifact":"04-budget.md","note":""}`.

Read `.singularskills/finance/<project>/03-forecast.md`. If this file does not exist, tell the user:

> Phase 3 (Forecast) has not been completed for "<project>". Run `/finance-forecast <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context:**
   - Read `.singularskills/finance/<project>/02-plan.md` for strategic objectives
   - Read `.singularskills/finance/<project>/03-forecast.md` for expense projections

2. **Define budget structure:**
   - List all departments or cost centers
   - Categorize expenses: personnel, tools/software, marketing, infrastructure, professional services, other
   - Determine budget period (monthly, quarterly, annual)

3. **Allocate by department:**
   - For each department:
     - Personnel costs (headcount x compensation)
     - Non-personnel costs (tools, travel, contractors, etc.)
     - Growth investments vs maintenance spend
   - Ensure allocations sum to the forecast total
   - Identify which departments have the most budget flexibility

4. **Set guardrails:**
   - Define spending authority levels (who can approve what amounts)
   - Set variance thresholds that trigger review (e.g., >10% over budget)
   - Identify protected vs discretionary line items
   - Define the reallocation process

5. **Create accountability framework:**
   - Assign a budget owner to each department
   - Define reporting cadence (monthly actuals vs budget)
   - Set up variance explanation requirements

6. **Write the artifact** to `.singularskills/finance/<project>/04-budget.md` with sections:
   - **Budget Summary** — total budget by period, split by department
   - **Department Budgets** — detailed allocation per department
   - **Headcount Budget** — planned hires, timing, and cost
   - **Spending Guardrails** — authority levels, thresholds, protected items
   - **Accountability** — owners, reporting cadence, variance rules

## Output

The budget written to `.singularskills/finance/<project>/04-budget.md`. Present a summary highlighting:
- Total budget and department breakdown
- Largest budget categories
- Key guardrails and approval thresholds
- Headcount plan

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"finance-budget","workflow":"finance","phase":4,"project":"<project>","event":"finished","artifact":"04-budget.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: finance-budget
workflow: finance
phase: 4
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
