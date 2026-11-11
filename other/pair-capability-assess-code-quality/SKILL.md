---
name: pair-capability-assess-code-quality
description: "Assesses code quality using resolution cascade (Argument > Adoption > Assessment). Applies quality score formula from code-metrics guidelines. Produces quality report with complexity, size, coverage, and maintainability metrics. Idempotent: detects existing report, checks staleness. Invocable independently or composed by /pair-process-review."
version: 0.4.1
author: Foomakers
---

# /pair-capability-assess-code-quality — Code Quality Assessment

Evaluate code quality using objective metrics from [code-metrics.md](../../../.pair/knowledge/guidelines/code-design/quality-standards/code-metrics.md). Produces a quality report with complexity, size, coverage, duplication, and maintainability scores. Includes actionable recommendations for improvement.

## Arguments

| Argument | Required | Description                                                                                       |
| -------- | -------- | ------------------------------------------------------------------------------------------------- |
| `$scope` | No       | Limit assessment to specific metric group: `complexity`, `size`, `coverage`, `duplication`, `maintainability`, `all` (default: `all`) |
| `$path`  | No       | Limit assessment to a specific file, directory, or package. If omitted, assesses the full codebase. |

## Algorithm

### Step 1: Resolution Cascade

#### Path A — Existing Recent Report

1. **Check**: Is there an existing quality report for this codebase? (Check conversation context, CI artifacts, or previous assessment output.)
2. **Skip**: If no existing report, go to Path B.
3. **Act**: Check staleness:
   - Has the codebase changed since the last assessment? (Use `git diff --stat` since last assessment date or commit.)
   - If no changes → confirm existing report is still valid. Exit.
   - If changes exist → report is stale. Present summary of changes and proceed to Path B.

   > Existing quality report found ([date]). [N files changed since last assessment.]
   > Re-assess? (Recommended — codebase has changed.)

4. **Verify**: If confirmed valid → exit. If stale or re-assessment requested → proceed to Path B.

#### Path B — Full Assessment

1. **Act**: Proceed to Step 2.

### Step 2: Read Quality Metrics Guidelines

1. **Act**: Read [code-metrics.md](../../../.pair/knowledge/guidelines/code-design/quality-standards/code-metrics.md) for:
   - Complexity metrics: cyclomatic complexity, cognitive complexity, nesting depth
   - Size metrics: lines of code, function length, class/module size, file size
   - Quality metrics: test coverage, code duplication, maintainability index
   - Thresholds per metric (e.g., cyclomatic complexity 1-5 = simple, 16+ = refactor needed)
2. **Verify**: Guidelines loaded. If not found, use built-in thresholds.

### Step 3: Collect Metrics

For each metric group in scope, follow **check → skip → act → verify**.

#### 3.1: Complexity Metrics

1. **Act**: Analyze code for:
   - **Cyclomatic complexity** per function: count decision points (if, else, switch, for, while, catch, &&, ||)
   - **Cognitive complexity**: weight nested conditions higher than flat ones
   - **Maximum nesting depth**: deepest level of nested control structures
2. **Act**: Classify per function:
   - Simple (1-5), Moderate (6-10), Complex (11-15), Very Complex (16+)
3. **Verify**: Complexity metrics collected.

#### 3.2: Size Metrics

1. **Act**: Measure:
   - **Lines of code** per file (excluding blank lines and comments)
   - **Function length**: lines per function (threshold: > 50 lines = warning)
   - **File size**: lines per file (threshold: > 300 lines = warning)
   - **Module count**: total modules/files in the project or scope
2. **Verify**: Size metrics collected.

#### 3.3: Test Coverage

1. **Act**: Run the test suite with coverage reporting (e.g., `vitest --coverage`, `jest --coverage`).
2. **Act**: Collect coverage metrics:
   - **Line coverage**: % of lines executed by tests (target: 70-90%)
   - **Function coverage**: % of functions called by tests (target: 80-90%)
   - **Branch coverage**: % of branches taken by tests (target: 60-75%)
3. **Verify**: Coverage metrics collected. If coverage tool not available, skip with warning.

#### 3.4: Code Duplication

1. **Act**: Scan for duplicated code blocks:
   - Exact duplicates (copy-paste)
   - Near-duplicates (structural similarity > 80%)
   - Duplication ratio: duplicated lines / total lines
2. **Act**: Classify: Low (< 3%), Moderate (3-5%), High (> 5%)
3. **Verify**: Duplication metrics collected.

#### 3.5: Maintainability Index

1. **Act**: Calculate composite maintainability score (0-100) based on:
   - Average complexity (lower is better)
   - Average function length (shorter is better)
   - Test coverage (higher is better)
   - Duplication ratio (lower is better)
2. **Act**: Classify:
   - **Excellent** (80-100): Well-maintained, easy to modify
   - **Good** (60-79): Generally maintainable, minor improvements possible
   - **Fair** (40-59): Maintenance challenges, targeted refactoring recommended
   - **Poor** (0-39): Significant maintenance burden, systematic improvement needed
3. **Verify**: Maintainability index calculated.

### Step 4: Generate Report

1. **Act**: Compile all metrics into a quality report.
2. **Act**: Identify **hotspots** — files or functions that exceed multiple thresholds.
3. **Act**: Generate **recommendations** ordered by impact:
   - Each recommendation references the metric, current value, threshold, and suggested action.

### Step 5: Present Report

1. **Act**: Present the report to the developer with recommendations.
2. **Verify**: Developer acknowledges. No action required — this is informational.

## Output Format

```text
CODE QUALITY REPORT:
├── Scope:           [$scope — $path or full codebase]
├── Complexity:      [avg cyclomatic: N | N functions > 10 | max nesting: N]
├── Size:            [N files | avg lines: N | N files > 300 lines | N functions > 50 lines]
├── Test Coverage:   [line: N% | function: N% | branch: N% | SKIPPED]
├── Duplication:     [ratio: N% — Low/Moderate/High]
├── Maintainability: [score: N/100 — Excellent/Good/Fair/Poor]
└── Hotspots:        [N files flagged]

HOTSPOTS:
1. [file] — [metric: value, metric: value] — [recommendation]
2. ...

RECOMMENDATIONS:
1. [priority] [metric] — [current] → [target]: [action]
2. ...

RESULT: [Quality score: N/100 | Assessed | Confirmed existing]
```

## Composition Interface

When composed by `/pair-process-review`:

- **Input**: /pair-process-review may invoke `/pair-capability-assess-code-quality` during the technical review phase.
- **Output**: Returns the quality report. /pair-process-review incorporates metrics and hotspots into review findings.
  - Poor maintainability or high complexity may inform review recommendations.
  - Metrics are informational — they do not HALT the review.

When invoked **independently**:

- Full interactive flow. Developer receives the report and decides on improvement actions.
- This skill is **read-only** — it inspects code and runs tests (coverage) but does not modify files.

## Graceful Degradation

- If [code-metrics.md](../../../.pair/knowledge/guidelines/code-design/quality-standards/code-metrics.md) is not found, use built-in thresholds (cyclomatic > 10, function > 50 lines, file > 300 lines, coverage > 70%).
- If coverage tools are not available, skip test coverage metrics and note: "Coverage: SKIPPED — no coverage tool detected."
- If duplication detection is not feasible (no tool), use heuristic scanning for obvious copy-paste patterns.
- If the codebase is too large for full analysis, limit to changed files (PR scope) and note: "Partial analysis — limited to changed files."

## Notes

- This skill is **read-only** — it inspects code, runs coverage (via existing test commands), but never modifies files.
- **Idempotent**: re-invocation checks staleness of existing report. If codebase unchanged → confirms existing report. If changed → re-assesses only.
- **Resolution cascade**: Path A (existing recent report) → Path B (full assessment). Follows the same cascade pattern as other assess-* skills.
- Metrics are **health indicators, not absolute quality measures**. Context matters: business logic naturally has higher complexity, and metric targets should align with team capabilities.
- Quality assessment is most valuable as a **trend** — individual snapshots matter less than improvement direction over time.
- The maintainability index is a composite heuristic — it provides a single number for quick assessment but the component metrics offer more actionable insights.
