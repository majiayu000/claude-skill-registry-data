---
name: pair-capability-analyze-code-quality
description: "Produces an objective code quality report — complexity, size, coverage, duplication, maintainability score — for a repo or package, with actionable recommendations. Composed by /pair-process-review; invoke directly for a report on demand ('code quality report', 'how maintainable is this'). Output-only: writes nothing, never blocks."
version: 0.5.0
author: Foomakers
---

# /pair-capability-analyze-code-quality — Code Quality Analysis

Evaluate code quality using objective metrics from [code-metrics.md](../../../.pair/knowledge/guidelines/code-design/quality-standards/code-metrics.md). Produces a quality report with complexity, size, coverage, duplication, and maintainability scores. Includes actionable recommendations for improvement. **Output-only**: this skill inspects code and runs coverage but writes no files — it never mutates adoption, code, or the PM tool.

## Arguments

| Argument | Required | Description                                                                                       |
| -------- | -------- | ------------------------------------------------------------------------------------------------- |
| `$scope` | No       | Limit analysis to specific metric group: `complexity`, `size`, `coverage`, `duplication`, `maintainability`, `all` (default: `all`) |
| `$path`  | No       | Limit analysis to a specific file, directory, or package. If omitted, analyzes the full codebase. |

## Algorithm

### Step 1: Resolution Cascade

Read [resolution cascade](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/resolution-cascade.md) for the generic Path A/B/C mechanics — this skill uses the **report-skill variant** and has no override argument, so it starts directly at the [idempotency](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md) check (no Path A/Argument-Override).

- **Existing-state check (Path B)**: an existing quality report for this codebase (conversation context, CI artifacts, prior output). Staleness test: has the codebase changed since the last analysis (`git diff --stat` since last analysis date/commit)? No changes → confirm and exit. Changes exist → present the delta and proceed to full analysis.
- **Full-analysis path (Path C)**: proceed to Step 2.

### Step 2: Read Quality Metrics Guidelines

1. **Act**: Read [code-metrics.md](../../../.pair/knowledge/guidelines/code-design/quality-standards/code-metrics.md) for:
   - Complexity metrics: cyclomatic complexity, cognitive complexity, nesting depth
   - Size metrics: lines of code, function length, class/module size, file size
   - Quality metrics: test coverage, code duplication, maintainability index
   - Thresholds per metric (e.g., cyclomatic complexity 1-5 = simple, 16+ = refactor needed)
2. **Verify**: The thresholds for every metric group in `$scope` are known from code-metrics.md (or the Graceful Degradation built-in defaults) before Step 3 collects metrics against them.

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
2. **Verify**: Report presented. No side effects — this step is purely informational output, not a decision point, so there is nothing to confirm.

## Output Format

Follows the [Report Shape](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/output-shapes.md#report-shape).

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

RESULT: [Quality score: N/100 | Analyzed | Confirmed existing]
```

## Composition Interface

When composed by `/pair-process-review`:

- **Input**: /pair-process-review may invoke `/pair-capability-analyze-code-quality` during the technical review phase.
- **Output**: Returns the quality report. /pair-process-review incorporates metrics and hotspots into review findings.
  - Poor maintainability or high complexity may inform review recommendations.
  - Metrics are informational — the review always proceeds regardless of score.

When invoked **independently**:

- Full interactive flow. Developer receives the report and decides on improvement actions.

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (guideline missing → fall back to built-in thresholds: cyclomatic > 10, function > 50 lines, file > 300 lines, coverage > 70%) for the standard scenarios. Additional cases:

- If coverage tools are not available, skip test coverage metrics and note: "Coverage: SKIPPED — no coverage tool detected."
- If duplication detection is not feasible (no tool), use heuristic scanning for obvious copy-paste patterns.
- If the codebase is too large for full analysis, limit to changed files (PR scope) and note: "Partial analysis — limited to changed files."

## Notes

- This skill is **read-only / output-only** — it only inspects code and runs coverage (via existing test commands); files, adoption, and the PM tool stay untouched. A finding worth tracking is promoted deliberately to the backlog via `/pair-capability-write-issue` — always a manual, selective act.
- **Idempotent** — see [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md). This skill's check: staleness of the existing report (Step 1) — unchanged codebase confirms it, changed codebase re-analyzes.
- Metrics are **health indicators, not absolute quality measures**. Context matters: business logic naturally has higher complexity, and metric targets should align with team capabilities.
- Quality analysis is most valuable as a **trend** — individual snapshots matter less than improvement direction over time.
- The maintainability index is a composite heuristic — it provides a single number for quick analysis but the component metrics offer more actionable insights.
