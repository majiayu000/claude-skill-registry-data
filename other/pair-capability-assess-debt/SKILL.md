---
name: pair-capability-assess-debt
description: "Assesses technical debt using resolution cascade (Argument > Adoption > Assessment). Categorizes debt (code, design, test, documentation, infrastructure), applies prioritization formula (impact x effort), proposes remediation priority. Idempotent: detects existing assessment. Invocable independently or composed by /pair-process-review."
version: 0.4.1
author: Foomakers
---

# /pair-capability-assess-debt — Technical Debt Assessment

Detect, categorize, and prioritize technical debt items. Applies the prioritization framework from [technical-debt.md](../../../.pair/knowledge/guidelines/code-design/quality-standards/technical-debt.md) guidelines. Produces a debt report with categorized items, severity, impact/effort scoring, and remediation recommendations.

## Arguments

| Argument | Required | Description                                                                                                                                      |
| -------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `$scope` | No       | Limit assessment to specific categories: `code`, `design`, `test`, `documentation`, `infrastructure`, `all` (default: `all`)                    |
| `$choice`| No       | Pre-identified debt item to assess (e.g., `"missing error handling in API layer"`). Skips detection, goes directly to categorization and scoring. |

## Composed Skills

| Skill              | Type       | Required                                         |
| ------------------ | ---------- | ------------------------------------------------ |
| `/pair-capability-record-decision` | Capability | No — only if remediation requires a decision     |

## Algorithm

### Step 1: Resolution Cascade

#### Path A — Argument Override ($choice provided)

1. **Check**: Is `$choice` provided?
2. **Skip**: If not provided, go to Path B.
3. **Act**: Accept the pre-identified debt item. Skip detection (Step 2). Proceed directly to Step 3 (categorization) with the single item.
4. **Verify**: Item accepted.

#### Path B — Existing Assessment

1. **Check**: Is there an existing debt assessment for this codebase/PR? (Look for a recent debt report in the conversation context or PR comments.)
2. **Skip**: If no existing assessment, go to Path C.
3. **Act**: Present the existing assessment:

   > Existing debt assessment found ([N items], [date]).
   > Re-assess? (Only if explicitly requested by developer.)

4. **Verify**: If developer confirms existing → exit. If re-assessment requested → proceed to Path C.

#### Path C — Full Assessment

1. **Act**: Proceed to Step 2 (detection).

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

### Step 5: Compose Decision (if needed)

1. **Check**: Do any High severity items require an architectural decision to remediate?
2. **Skip**: If no decisions needed → proceed to output.
3. **Act**: Compose `/pair-capability-record-decision` for each decision-worthy item:
   - `$type: architectural` (if it changes architecture) or `$type: non-architectural` (if it's a tooling/process change)
   - `$topic: debt-remediation-[item]`
4. **Verify**: Decisions recorded.

## Output Format

```text
TECH DEBT ASSESSMENT:
├── Items Found:  [N total]
├── Categories:   Code: [N] | Design: [N] | Test: [N] | Docs: [N] | Infra: [N]
├── Severity:     High: [N] | Medium: [N] | Low: [N]
└── Decisions:    [N recorded | none needed]

PRIORITIZED ITEMS:
 # | Severity | Category | Impact | Effort | Score | Description | Location
---|----------|----------|--------|--------|-------|-------------|----------
 1 | High     | [cat]    | [1-5]  | [1-5]  | [N]   | [desc]      | [file:line]
 2 | ...

REMEDIATION PLAN (High severity):
1. [item] — [strategy] (est. [effort])
2. ...

RESULT: [N items assessed, N high-priority, N decisions recorded]
```

## Composition Interface

When composed by `/pair-process-review`:

- **Input**: /pair-process-review invokes `/pair-capability-assess-debt` during the completeness phase (Phase 4).
- **Output**: Returns the debt assessment report. /pair-process-review incorporates findings into review output.
  - High severity items may influence the review decision (TECH-DEBT verdict).
  - Items are informational — they do not HALT the review.
  - Remediation recommendations inform CHANGES-REQUESTED if critical debt is introduced.

When invoked **independently**:

- Full interactive flow. Scan codebase or specified scope for debt.
- Report findings with categorization and prioritization.
- This skill is **read-only** when detecting — it does not modify code. Decision recording via `/pair-capability-record-decision` is the only write action.

## Graceful Degradation

- If adoption files are missing, skip design and infrastructure categories — report only code-level debt (code smells, duplication, test gaps, documentation).
- If [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) is not found, skip infrastructure dependency checks.
- If [architecture.md](../../../.pair/adoption/tech/architecture.md) is not found, skip design debt detection for architectural violations.
- If `/pair-capability-record-decision` is not installed, warn and skip decision recording.
- If guidelines are not found, use built-in heuristics for detection (complexity thresholds, naming patterns, test file presence).

## Notes

- This skill **replaces the stub implementation** from [#100](https://github.com/foomakers/pair/issues/100). Full categorization, prioritization formula, and remediation recommendations are now included.
- **Resolution cascade**: Path A (pre-identified item) → Path B (existing assessment) → Path C (full scan). Follows the same pattern as other assess-* skills.
- **Idempotent**: re-invocation on an already-assessed codebase confirms the existing assessment. Re-assessment only on explicit developer request.
- **Read-only for detection** — this skill inspects code but never modifies files directly. The only write action is decision recording via `/pair-capability-record-decision`.
- Prioritization formula `Impact × (6 - Effort)` favors quick wins: high-impact items with low effort get the highest scores.
- Debt is contextual — the same pattern may be acceptable in a prototype but unacceptable in production code. Severity assessment considers the project's maturity and risk tolerance.
