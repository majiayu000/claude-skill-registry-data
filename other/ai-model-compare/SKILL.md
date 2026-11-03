---
name: ai-model-compare
description: Compare two or more models for an AI feature on the team's own test results — pass rate per check, cost per use and latency — and recommend one with the trade-off stated. Use when a team has run its test set on several models and must pick one. Not for choosing the overall approach; see /ai-approach.
metadata:
  argument-hint: "<results file> [project]"
---

# Model compare

Compare the models in "$ARGUMENTS" on the team's own results and recommend one.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

The results: per model, per test case, the pass or fail verdict for each check, the cost and the latency, as a file or a paste. Never use benchmark scores or prices from memory; compare only what the team ran. When `$ARGUMENTS` or the request names a project, use that name as `<project>` whether or not its folder exists yet in `.singularskills/ai/`. With no project named: with exactly one folder there, use it; with several, ask which; with no folder at all, read none and continue.

Read `.singularskills/ai/<project>/01-define.md` for the budgets and `.singularskills/ai/<project>/06-evaluate.md` for the checks and the launch bar, when they exist.

## Process

1. **Compute per model** with a script: pass rate per check with the number of cases, cost per use (mean and 90th percentile), and latency (median and 90th percentile). Work in a scratch location outside `.singularskills/`; this skill writes no file. Without a way to run code, show the raw counts per model and check, label rates `not computed`, and compare from the counts.

2. **Check the differences are real:** with fewer than about 50 cases per check, say a difference of a few points may be noise.

3. **Compare against the budgets and the bar:** which models meet every check's bar within the latency and cost budgets.

4. **Recommend one,** with the trade-off stated (for example, "B passes 4 points more on faithfulness for 3× the cost"), and what would change the choice.

## Output

In chat: the recommendation first, then a table of models against checks, cost and latency, and the trade-off. This skill writes no file.
