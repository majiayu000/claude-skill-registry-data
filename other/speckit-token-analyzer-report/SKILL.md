---
name: speckit-token-analyzer-report
description: Generate token analysis report from captured data
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: token-analyzer:commands/speckit.token-analyzer.report.md
---

# Generate Token Analysis Report

Aggregate all runs for a scenario, generate an analysis report with summary tables, per-step breakdowns, quality scores, and optimization recommendations.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

The user input should include:
- **report-name** (required): Label for this report (e.g., `greeting-analysis`)
- **--runs** (optional): Comma-separated list of run labels to include. If omitted, include all runs.
- **--format** (optional): Output format — `markdown` (default) or `json`

## Prerequisites

1. Verify `.specify/token-analysis/runs/` exists and contains at least one run.
2. If `--runs` is specified, verify each listed run exists.
3. If no runs exist, inform the user to run `speckit.token-analyzer.baseline` first.

## Execution

### Step 1: Collect Run Data

For each run (or the specified subset), load:
- `metadata.json` — scenario, preset, integration, timestamp
- `summary.json` — aggregated token metrics
- `steps/*.json` — per-step token data

### Step 2: Generate Run Summary

Aggregate all step data for the report:

**Bash:**
```bash
.specify/extensions/token-analyzer/scripts/bash/generate-report.sh --json --run-label "{run-label}"
```

**PowerShell:**
```powershell
.specify/extensions/token-analyzer/scripts/powershell/generate-report.ps1 -Json -RunLabel "{run-label}"
```

### Step 3: Cross-Run Analysis

If multiple runs are included, compute:
- Mean and standard deviation for each metric across runs
- Identify the top-3 token consumers (which commands, which sections)
- Variance analysis: is the 3-run variance < 15%? (success criterion from plan.md)

### Step 4: Render Report

Use the template at `.specify/extensions/token-analyzer/templates/report-template.md` to structure the output. Fill in all placeholder sections.

## Output

Display the report and save to `.specify/token-analysis/comparisons/{report-name}.md`:

```
## Token Analysis Report: {report-name}

Generated: {timestamp}
Runs included: {count}

### Summary

| Run | Preset | Total Tokens | Input | Output | Quality |
|-----|--------|-------------|-------|--------|---------|
| {label} | {preset} | {total} | {input} | {output} | {score} |
| ... | ... | ... | ... | ... | ... |

### Per-Command Breakdown

| Command | Avg Input | Avg Output | Avg Total | Std Dev |
|---------|-----------|------------|-----------|---------|
| specify | {n} | {n} | {n} | {n} |
| plan | {n} | {n} | {n} | {n} |
| tasks | {n} | {n} | {n} | {n} |

### Token Attribution (Estimates)

| Component | Avg Tokens | % of Input |
|-----------|-----------|------------|
| Command template | {n} | {%} |
| Artifact template | {n} | {%} |
| Hook preamble | {n} | {%} |
| Accumulated context | {n} | {%} |

### Quality Scores

| Run | Completeness | Depth | Cross-Ref | Actionability | Format | Overall |
|-----|-------------|-------|-----------|---------------|--------|---------|
| {label} | {n} | {n} | {n} | {n} | {n} | {n} |

### Recommendations

{Analysis based on data patterns — e.g., which commands are heaviest,
 where cache hits are low, which optimization strategies to try next}

Report saved to: `.specify/token-analysis/comparisons/{report-name}.md`
```