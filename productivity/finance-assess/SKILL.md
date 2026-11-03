---
name: finance-assess
description: Assess a business's historical financials — consolidate and validate the data, summarize revenue and cost structure, and set baseline metrics such as gross margin, burn and runway. Use when the user wants to start financial planning and needs to know where the numbers stand today. Not for a ratio check or a quick monthly look from the books; see /finance-ratios or /bookkeeping-report.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: finance
  phase: 1
  artifact: 01-assess.md
---

# Assess

Consolidate and validate financial data for "$ARGUMENTS". Gather historical financials, verify data integrity, and establish the baseline from which all planning begins.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"finance-assess","workflow":"finance","phase":1,"project":"<project>","event":"skipped","artifact":"01-assess.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Assess) of the FP&A workflow (`finance`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `finance` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise, unless the user named this skill, ask one question, since this is the first phase of its workflow: "Just this step, or the whole FP&A workflow?" End your turn and wait; on the whole workflow, hand off the same way; on just this step, continue here.

**Recall.** Before you ask the user anything, look for what this repository already holds about `<project>`: if a tool is available whose description says it searches or maps this repository (a memory or repo-map server such as `repo_map` or `entities`), query it for `<project>` and this phase's subject and read what it returns, keeping only results from this repository; in every case also list `.singularskills/*/<project>/` and read the **Decisions** and **Open questions** of any artifact there, and the lines of `.singularskills/log.jsonl` whose `project` is `<project>`. After the frontmatter and title, add a `## Recalled` section of at most ten lines naming what you found and where (path or tool), or the single line `Nothing recalled: no earlier artifacts, log lines or memory results for <project>.` Ask the user only what this did not answer. The trail's shape is described in `references/memory/trail.md`, bundled with this skill.

Before you start work, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"finance-assess","workflow":"finance","phase":1,"project":"<project>","event":"started","artifact":"01-assess.md","note":""}`.

None — this is the first phase.

## Process

1. **Ask financial data questions:**
   - What type of business is this? (SaaS, e-commerce, services, marketplace, hardware)
   - What stage? (pre-revenue, early-stage, growth, mature)
   - What financial data is available? (P&L, balance sheet, cash flow, bank statements)
   - What period does the data cover?
   - What accounting method? (cash vs accrual)
   - What currency and fiscal year?

2. **Consolidate data sources:**
   - List all revenue streams and categorize them
   - List all cost categories (fixed, variable, one-time)
   - Identify the chart of accounts or cost centers
   - Note any data gaps or inconsistencies

3. **Validate and reconcile:**
   - Cross-check revenue against bank deposits or invoices
   - Verify expense categories are consistent across periods
   - Flag any anomalies, one-time items, or restatements
   - Calculate basic trends (MoM, YoY growth rates)

4. **Establish baseline metrics:**
   - Monthly Recurring Revenue (MRR) or equivalent
   - Gross margin
   - Burn rate and runway
   - Headcount and revenue per employee

5. **Write the artifact** to `.singularskills/finance/<project>/01-assess.md` with sections:
   - **Business Profile** — type, stage, accounting method, fiscal year
   - **Data Sources** — what data was provided and its quality
   - **Revenue Summary** — streams, trends, seasonality
   - **Cost Summary** — fixed vs variable, major categories
   - **Baseline Metrics** — key financial indicators
   - **Data Gaps** — missing information and impact on planning

## Output

The assessment written to `.singularskills/finance/<project>/01-assess.md`. Present a summary highlighting:
- Business profile and stage
- Revenue and cost structure overview
- Key baseline metrics
- Critical data gaps to resolve

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"finance-assess","workflow":"finance","phase":1,"project":"<project>","event":"finished","artifact":"01-assess.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `none`, as this phase has no gate):

```yaml
---
skill: finance-assess
workflow: finance
phase: 1
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
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
