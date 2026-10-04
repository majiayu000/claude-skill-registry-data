---
name: speckit-token-analyzer-compare
description: Compare token consumption between two runs
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: token-analyzer:commands/speckit.token-analyzer.compare.md
---

# Compare Token Consumption

Load two runs (or a run vs a saved baseline), compute deltas for all token metrics, and generate a comparison report.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

The user input should include:
- **comparison-name** (required): Label for this comparison (e.g., `standard-vs-lean`)
- **--baseline** (required): Run label or baseline name to use as the reference
- **--variant** (required): Run label to compare against the baseline

## Prerequisites

1. Verify the baseline exists at either:
   - `.specify/token-analysis/runs/{baseline}/summary.json` (a run), OR
   - `.specify/token-analysis/baselines/{baseline}.json` (a saved baseline)

2. Verify the variant exists at:
   - `.specify/token-analysis/runs/{variant}/summary.json`

3. If either is missing, list available runs and baselines and ask the user to specify valid labels.

## Execution

### Step 1: Load Data

Load the summary JSON for both the baseline and variant runs.

### Step 2: Compute Deltas

For each shared metric, compute:
- **Absolute delta**: `variant_value - baseline_value`
- **Percentage change**: `(variant_value - baseline_value) / baseline_value * 100`

Key metrics to compare:
- `total_input_tokens`
- `total_output_tokens`
- `total_tokens`
- `cache_read_tokens` (if available)
- `average_quality_score`
- Per-command breakdowns

### Step 3: Compute Efficiency Ratio

```
baseline_efficiency = baseline_quality / (baseline_tokens / 1000)
variant_efficiency  = variant_quality  / (variant_tokens / 1000)
efficiency_improvement = (variant_efficiency - baseline_efficiency) / baseline_efficiency * 100
```

### Step 4: Generate Comparison Report

Use the report template at `.specify/extensions/token-analyzer/templates/report-template.md` as a guide. Generate the comparison report as markdown.

Save the report to:
```
.specify/token-analysis/comparisons/{comparison-name}.md
```

### Step 5: Accept/Reject Recommendation

Apply the acceptance criteria from plan.md:
- **Accept** if: token reduction > 10% AND quality delta > -0.1 AND efficiency ratio improves
- **Reject** if: any criterion fails
- **Review** if: borderline (token reduction 5–10% or quality delta between -0.1 and -0.15)

## Output

Display the comparison summary:

```
## Comparison: {comparison-name}

### {baseline} → {variant}

| Metric | Baseline | Variant | Delta | Change |
|--------|----------|---------|-------|--------|
| Input tokens | {n} | {n} | {±n} | {±%}% |
| Output tokens | {n} | {n} | {±n} | {±%}% |
| Total tokens | {n} | {n} | {±n} | {±%}% |
| Quality score | {n} | {n} | {±n} | {±%}% |
| Efficiency | {n} | {n} | {±n} | {±%}% |

### Per-Command Breakdown

| Command | Baseline Tokens | Variant Tokens | Reduction |
|---------|----------------|----------------|-----------|
| specify | {n} | {n} | {%}% |
| plan | {n} | {n} | {%}% |
| tasks | {n} | {n} | {%}% |

### Recommendation: {ACCEPT / REJECT / REVIEW}

{Rationale based on acceptance criteria}

Report saved to: `.specify/token-analysis/comparisons/{comparison-name}.md`
```