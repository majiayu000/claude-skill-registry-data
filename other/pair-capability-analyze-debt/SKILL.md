---
name: pair-capability-analyze-debt
description: "Produces a technical debt report — categorized items (code, design, test, documentation, infrastructure), prioritized by impact x effort. Composed by /pair-process-review; invoke directly to catalog and prioritize debt on demand. Output-only: writes no files, creates no backlog items, never blocks a PR."
version: 0.5.0
author: Foomakers
---

# /pair-capability-analyze-debt — Technical Debt Analysis

Detect, categorize, and prioritize technical debt items. Applies the prioritization framework from [technical-debt.md](../../../.pair/knowledge/guidelines/code-design/quality-standards/technical-debt.md) guidelines. Produces a debt report with categorized items, severity, impact/effort scoring, and remediation recommendations. **Output-only**: this skill returns a report — it writes no files, creates no PM-tool items, and there is **no `$mode:scan`** and **no auto-conversion** of debt into backlog cards. Technical debt **never blocks a PR**.

## Arguments

| Argument | Required | Description                                                                                                                                      |
| -------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `$scope` | No       | Limit analysis to specific categories: `code`, `design`, `test`, `documentation`, `infrastructure`, `all` (default: `all`)                    |
| `$choice`| No       | Pre-identified debt item to analyze (e.g., `"missing error handling in API layer"`). Skips detection, goes directly to categorization and scoring. |

## Composed Skills

This skill is **output-only** — it composes no skill and writes no files. No auto-creation of tech-debt items. A debt item worth scheduling is promoted **deliberately** to the backlog by a human/agent via `/pair-capability-write-issue` with the `tech-debt` label (see [Composition Interface](#composition-interface)) — a manual, selective act, never a 100% auto-conversion.

## Algorithm

### Step 1: Resolution Cascade

Read [resolution cascade](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/resolution-cascade.md) for the generic Path A/B/C mechanics — this skill uses the **report-skill variant**, where Path B is an [idempotency](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md) check against a recent output rather than an adoption file.

- **Path A delta**: override argument is `$choice` (a pre-identified debt item). On accept, skip detection (Step 2) and proceed directly to Step 3 with the single item.
- **Path B delta**: existing-state check is a recent debt report in conversation context or PR comments. Re-analysis only on explicit developer request.
- **Path C delta**: proceed to Step 2 (detection).

### Step 2: Detect Debt Items

Scan the codebase or PR changes for debt indicators per category. Follow **check → skip → act → verify** for each.

#### 2.1: Code Debt

1. **Check**: Scan for code-level debt indicators:
   - Code smells: `TODO`, `FIXME`, `HACK`, `WORKAROUND` comments
   - Duplicated code blocks or patterns across modules
   - Functions exceeding complexity thresholds (cyclomatic complexity > 10)
   - Deep nesting (> 3 levels)
   - Long functions (> 50 lines) or large files (> 300 lines)
2. **Skip**: If no code debt found → record category as clean.
3. **Act**: Flag each item with location and preliminary severity.

#### 2.2: Design Debt

1. **Check**: Scan for design-level debt:
   - Violations of adopted [architecture](../../../.pair/adoption/tech/architecture.md) patterns
   - Tight coupling between modules that should be independent
   - Missing abstractions (repeated patterns that should be extracted)
   - God objects or utility catch-all modules
   - Layer boundary violations
2. **Skip**: If no design debt found → record category as clean.
3. **Act**: Flag each item.

#### 2.3: Test Debt

1. **Check**: Scan for testing gaps:
   - Modules without corresponding test files (violating 1:1 mapping)
   - Tests with no assertions or weak assertions
   - Missing edge case coverage
   - Implementation-coupled tests (mocking internals instead of behavior)
   - Skipped or disabled tests (`xit`, `xdescribe`, `.skip`)
2. **Skip**: If no test debt found → record category as clean.
3. **Act**: Flag each item.

#### 2.4: Documentation Debt

1. **Check**: Scan for documentation gaps:
   - Public APIs without documentation
   - Complex logic without explanatory comments
   - Outdated README or adoption files
   - Missing ADR/ADL for significant decisions
2. **Skip**: If no documentation debt found → record category as clean.
3. **Act**: Flag each item.

#### 2.5: Infrastructure Debt

1. **Check**: Scan for infrastructure issues:
   - Dependencies not listed in [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) or with known vulnerabilities
   - Outdated dependency versions (major version behind)
   - Missing or broken CI/CD quality gates
   - Configuration drift from adopted infrastructure
2. **Skip**: If no infrastructure debt found → record category as clean.
3. **Act**: Flag each item.

### Step 3: Categorize and Score

For each detected item, apply the prioritization formula:

1. **Act**: Assess **Impact** (1-5):
   - 1: Cosmetic — no effect on functionality
   - 2: Minor — slight inconvenience, easy workaround
   - 3: Moderate — affects maintainability or developer velocity
   - 4: Significant — affects reliability, security, or user experience
   - 5: Critical — active risk to system correctness or security

2. **Act**: Assess **Effort** (1-5):
   - 1: Trivial — < 1 hour, simple fix
   - 2: Small — 1-4 hours, straightforward
   - 3: Medium — 1-2 days, moderate complexity
   - 4: Large — 3-5 days, significant refactoring
   - 5: Epic — > 1 week, architectural change

3. **Act**: Calculate **Priority Score**: `Impact × (6 - Effort)` (higher = fix first)
   - High impact + low effort = highest priority (quick wins)
   - High impact + high effort = scheduled remediation
   - Low impact + low effort = opportunistic fixes
   - Low impact + high effort = defer or accept

4. **Act**: Assign **Severity** based on priority score:
   - **High** (score ≥ 15): Address in current or next sprint
   - **Medium** (score 8-14): Plan remediation within 2-3 sprints
   - **Low** (score ≤ 7): Address opportunistically

### Step 4: Generate Remediation Recommendations

1. **Act**: For each High severity item, propose a remediation approach:
   - Specific refactoring strategy (e.g., "Extract method", "Introduce interface", "Strangler fig pattern")
   - Estimated effort
   - Risk assessment for the remediation itself
2. **Act**: For Medium items, provide general guidance.
3. **Act**: For Low items, note for tracking only.

### Step 5: Return the Report

1. **Act**: Return the debt report (see Output Format) to the caller or developer. **This skill writes nothing** — no adoption file, no code change, no PM-tool item.
2. **Act**: If a High-severity item is worth scheduling, recommend that the developer promote it **deliberately** to the backlog via `/pair-capability-write-issue` (`$type` per template, `tech-debt` label). This is always a manual, selective decision made by the developer.
3. **Verify**: Report returned. No side effects.

## Output Format

Follows the [Report Shape](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/output-shapes.md#report-shape).

```text
TECH DEBT ANALYSIS (output-only — no files or issues created):
├── Items Found:  [N total]
├── Categories:   Code: [N] | Design: [N] | Test: [N] | Docs: [N] | Infra: [N]
├── Severity:     High: [N] | Medium: [N] | Low: [N]
└── Promotion:    [none | suggested: N items for deliberate /write-issue promotion]

PRIORITIZED ITEMS:
 # | Severity | Category | Impact | Effort | Score | Description | Location
---|----------|----------|--------|--------|-------|-------------|----------
 1 | High     | [cat]    | [1-5]  | [1-5]  | [N]   | [desc]      | [file:line]
 2 | ...

REMEDIATION PLAN (High severity):
1. [item] — [strategy] (est. [effort])
2. ...

RESULT: [N items analyzed, N high-priority — report only, nothing created/blocked]
```

## Composition Interface

When composed by `/pair-process-review`:

- **Input**: /pair-process-review invokes `/pair-capability-analyze-debt` during the completeness phase (Phase 4).
- **Output**: Returns the debt report. /pair-process-review incorporates findings into review output (the Tech Debt section).
  - Debt items are **informational** — the review and PR always proceed regardless of what's found.
  - Items worth tracking are promoted deliberately (after review) via `/pair-capability-write-issue` with the `tech-debt` label — /pair-process-review itself only reports them.

When invoked **independently**:

- Full interactive flow. Scan codebase or specified scope for debt.
- Report findings with categorization and prioritization.

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (guideline missing → fall back to built-in heuristics: complexity thresholds, naming patterns, test file presence; adoption file missing → skip the categories that depend on it) for the standard scenarios. Additional cases:

- If [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) is not found, skip infrastructure dependency checks.
- If [architecture.md](../../../.pair/adoption/tech/architecture.md) is not found, skip design debt detection for architectural violations.

## Notes

- **Idempotent** — see [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md). This skill's check: existing analysis for the codebase/PR (Step 1, Path B).
- Prioritization formula `Impact × (6 - Effort)` favors quick wins: high-impact items with low effort get the highest scores.
- Debt is contextual — the same pattern may be acceptable in a prototype but unacceptable in production code. Severity assessment considers the project's maturity and risk tolerance.
