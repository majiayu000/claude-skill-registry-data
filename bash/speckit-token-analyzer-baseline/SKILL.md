---
name: speckit-token-analyzer-baseline
description: Capture baseline token metrics for a test scenario
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: token-analyzer:commands/speckit.token-analyzer.baseline.md
---

# Capture Token Baseline

Orchestrate a test scenario run, capture token metrics from CLI JSON responses, estimate input tokens from templates, and save results as a named baseline.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

The user input should include:
- **run-label** (required): A short name for this run (e.g., `standard-specify-greeting`)
- **--scenario** (optional): Description of the test scenario
- **--commands** (optional): Comma-separated list of commands to measure (e.g., `specify,plan,tasks`)
- **--preset** (optional): Which preset to use (e.g., `lean`, `standard`)

If only a run-label is provided, capture metrics for the most recent command execution.

## Prerequisites

1. Verify the data directory exists. If not, create it:
   ```bash
   mkdir -p .specify/token-analysis/runs .specify/token-analysis/baselines .specify/token-analysis/comparisons
   ```

2. Check if a run with this label already exists at `.specify/token-analysis/runs/{run-label}/`. If so, warn the user and ask whether to overwrite.

## Execution

### Step 1: Initialize Run Metadata

Create `.specify/token-analysis/runs/{run-label}/metadata.json`:

```json
{
  "run_label": "{run-label}",
  "scenario": "{scenario description}",
  "preset": "{preset name or 'standard'}",
  "integration": "{detected integration}",
  "timestamp": "{ISO 8601 timestamp}",
  "commands": ["{list of commands to capture}"]
}
```

### Step 2: Estimate Input Tokens (Layer 2)

For each command in the run, estimate the input token count from the command template:

**Bash:**
```bash
.specify/extensions/token-analyzer/scripts/bash/estimate-tokens.sh --json "{path-to-command-template}"
```

**PowerShell:**
```powershell
.specify/extensions/token-analyzer/scripts/powershell/estimate-tokens.ps1 -Json "{path-to-command-template}"
```

Record the estimates in the step JSON under the `estimates` field.

### Step 3: Capture CLI Token Data (Layer 1)

After each command executes, parse the CLI JSON response for token fields:

**Bash:**
```bash
.specify/extensions/token-analyzer/scripts/bash/capture-tokens.sh --json --run-label "{run-label}" --step "{command-name}" < "{cli-response-file}"
```

**PowerShell:**
```powershell
.specify/extensions/token-analyzer/scripts/powershell/capture-tokens.ps1 -Json -RunLabel "{run-label}" -Step "{command-name}" < "{cli-response-file}"
```

This writes a per-step JSON file to `.specify/token-analysis/runs/{run-label}/steps/{command}.json`.

### Step 4: Score Output Quality

For each command that produced an artifact, score the output quality:

**Bash:**
```bash
.specify/extensions/token-analyzer/scripts/bash/score-quality.sh --json "{artifact-path}" --command "{command-name}"
```

**PowerShell:**
```powershell
.specify/extensions/token-analyzer/scripts/powershell/score-quality.ps1 -Json "{artifact-path}" -Command "{command-name}"
```

### Step 5: Generate Summary

Aggregate all step data into a run summary:

**Bash:**
```bash
.specify/extensions/token-analyzer/scripts/bash/generate-report.sh --json --run-label "{run-label}"
```

**PowerShell:**
```powershell
.specify/extensions/token-analyzer/scripts/powershell/generate-report.ps1 -Json -RunLabel "{run-label}"
```

### Step 6: Save as Baseline (Optional)

If the user requests saving as a baseline, copy the summary to baselines:

```bash
cp .specify/token-analysis/runs/{run-label}/summary.json .specify/token-analysis/baselines/{run-label}.json
```

## Output

Report the captured metrics to the user:

```
## Token Capture Complete: {run-label}

| Metric | Value |
|--------|-------|
| Commands captured | {count} |
| Total input tokens | {sum} |
| Total output tokens | {sum} |
| Total tokens | {grand total} |
| Estimated input tokens | {estimate sum} |
| Estimate accuracy | {actual/estimate ratio}% |
| Average quality score | {mean quality} |

Data saved to: `.specify/token-analysis/runs/{run-label}/`
```

If saved as baseline, also note:
```
Baseline saved to: `.specify/token-analysis/baselines/{run-label}.json`
```