---
name: finance-scenario
description: Model best, base and worst-case financial scenarios for one decision, with the variables that differ, projections for each, decision triggers and contingency plans. Use when the user faces a decision under uncertainty and wants to see the range of outcomes before choosing. Not for a full multi-year model with valuation; see /finance-model.
metadata:
  argument-hint: "[project] [--skip-checks]"
---

# Scenario

Model financial scenarios for "$ARGUMENTS". Build structured best/base/worst-case projections to understand the range of possible outcomes and prepare contingency plans.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"finance-scenario","workflow":"finance","phase":null,"project":"<project>","event":"skipped","artifact":"<artifact file>","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

None — utility skill, run anytime. Works best when financial data exists in `.singularskills/finance/<project>/`.

## Process

1. **Gather context:**
   - If prior phase artifacts exist, read them for baseline data
   - Ask the user what decision or question the scenarios should inform
   - Determine the time horizon for the scenarios

2. **Define scenario parameters:**
   - Identify the 5-8 key variables that drive outcomes (revenue growth, churn, ARPU, hiring pace, etc.)
   - For each variable, define best/base/worst values with rationale
   - Reference `references/financial-model-template.md` for scenario table structure

3. **Build three scenarios:**
   - **Best case:** optimistic but plausible assumptions
   - **Base case:** most likely outcome based on current trajectory
   - **Worst case:** pessimistic but survivable assumptions
   - For each: project revenue, expenses, cash flow, and runway

4. **Analyze implications:**
   - What decisions change between scenarios?
   - At what point does the worst case become dangerous?
   - What early warning signals distinguish which scenario is unfolding?
   - What contingency actions should be prepared?

5. **Write the artifact** to `.singularskills/finance/<project>/scenario.md` with sections:
   - **Scenario Question** — what decision this analysis informs
   - **Variable Assumptions** — table of inputs per scenario
   - **Scenario Projections** — financial outcomes per scenario
   - **Decision Triggers** — signals that indicate which scenario is playing out
   - **Contingency Plans** — actions to take in each scenario

## Output

The scenario analysis written to `.singularskills/finance/<project>/scenario.md`. Present a summary highlighting:
- Range of outcomes (worst to best)
- Key differentiating variables
- Decision triggers and contingency plans

End the artifact with this paragraph, verbatim:

> **Not financial or tax advice.** This artifact is generated analysis for review by a qualified accountant or financial professional before any filing, reporting or decision relies on it.
