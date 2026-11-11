---
name: pair-capability-verify-done
description: "Checks Definition of Done criteria against a PR or work item. Reads universal DoD from quality-standards guidelines and project-specific criteria from adoption files. Already-passing criteria are skipped. Invocable independently or composed by /pair-process-review."
version: 0.4.1
author: Foomakers
---

# /pair-capability-verify-done — Definition of Done Checker

Validate a work item against Definition of Done criteria. Two sources of truth:

- **[definition-of-done.md](../../../.pair/knowledge/guidelines/quality-assurance/quality-standards/definition-of-done.md)** — universal DoD checklist (18 criteria covering requirements, code standards, testing, security, performance, accessibility, deployment, documentation).
- **Adoption files** [`.pair/adoption/tech/`](../../../.pair/adoption/tech) — project-specific criteria derived from adopted architecture, tech-stack, and way-of-working decisions.

Only check criteria that are not already passing.

## Arguments

| Argument | Required | Description                                                                                                                                                                    |
| -------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `$scope` | No       | Limit checking to specific areas: `requirements`, `code-quality`, `testing`, `security`, `performance`, `accessibility`, `deployment`, `documentation`, `all` (default: `all`) |
| `$story` | No       | Story ID to load acceptance criteria from PM tool. If omitted, checks universal DoD only.                                                                                      |

## Algorithm

Execute each criterion group in order. For every criterion, follow the **check → skip → act → verify** pattern.

### Step 1: Load DoD Criteria

1. **Check**: Read [definition-of-done.md](../../../.pair/knowledge/guidelines/quality-assurance/quality-standards/definition-of-done.md) and extract the DoD checklist.
2. **Skip**: If `$scope` is set, filter to only the matching criterion group.
3. **Act**: Build the working checklist. If `$story` is provided, prepend story-specific acceptance criteria from the PM tool.
4. **Verify**: Checklist loaded. If definition-of-done.md is not found, warn and proceed with adoption-only criteria.

### Step 2: Requirements & Acceptance Criteria

1. **Check**: Are all story acceptance criteria met? (Requires `$story` to be set.)
2. **Skip**: If no `$story` provided, or all AC already verified — mark PASS and move to Step 3.
3. **Act**: For each AC, evaluate whether the current code/PR satisfies it. Report unmet criteria.
4. **Verify**: All AC met, or unmet criteria reported.

### Step 3: Code Standards

1. **Check**: Does the code follow adopted code design guidelines and technical standards?
2. **Skip**: If already verified (e.g., by a prior /pair-capability-verify-quality run in the same session) — mark PASS.
3. **Act**: Check code against [code-design guidelines](../../../.pair/knowledge/guidelines/code-design/README.md) and [technical standards](../../../.pair/knowledge/guidelines/technical-standards/README.md). Report non-conformities.
4. **Verify**: Standards met or non-conformities reported.

### Step 4: Architecture & ADR Compliance

1. **Check**: Does the solution align with adopted [architecture](../../../.pair/adoption/tech/architecture.md)? Are relevant ADRs followed?
2. **Skip**: If no architectural changes in the PR — mark PASS.
3. **Act**: Cross-reference changes against architecture adoption and existing ADRs in `adoption/tech/adr/`. Report gaps.
4. **Verify**: Compliant or gaps reported. Missing ADR is a **HALT condition** for the composing skill.

### Step 5: Testing

1. **Check**: Are tests written per [testing strategy](../../../.pair/knowledge/guidelines/testing/test-strategy/README.md)? Do all tests pass?
2. **Skip**: If already verified by /pair-capability-verify-quality in the same session — mark PASS.
3. **Act**: Verify test existence for new/modified modules (1:1 mapping). Check test quality (behavior-based, not implementation-based). Report gaps.
4. **Verify**: Testing criteria met or gaps reported.

### Step 6: Security

1. **Check**: Are security considerations identified and practices followed?
2. **Skip**: If no security-relevant changes in the PR — mark PASS.
3. **Act**: Check against [security guidelines](../../../.pair/knowledge/guidelines/quality-assurance/security/security-guidelines.md). Look for: hardcoded secrets, injection vulnerabilities, improper data handling, missing input validation.
4. **Verify**: Secure or issues reported.

### Step 7: Performance

1. **Check**: Do performance benchmarks meet standards?
2. **Skip**: If no performance-relevant changes — mark PASS.
3. **Act**: Check for obvious performance issues: N+1 queries, unbounded loops, missing pagination, large bundle imports.
4. **Verify**: Performance criteria met or issues reported.

### Step 8: Documentation

1. **Check**: Is documentation updated for changed functionality?
2. **Skip**: If no public API or behavior changes — mark PASS.
3. **Act**: Check for: updated READMEs, inline documentation for complex logic, updated adoption files if decisions changed.
4. **Verify**: Documentation current or gaps reported.

### Step 9: Manual Test Validation (Optional)

1. **Check**: Does the project have a manual test suite (look for `qa/` directory with `CP*.md` files at project root)?
2. **Skip**: If no manual test suite exists — mark SKIPPED. If `$scope` excludes `manual-testing` — mark SKIPPED.
3. **Act**: Check if a manual test report exists for the current version in `.tmp/manual-test-reports/` with overall result PASS. Do NOT execute tests — only check for an existing report.
4. **Verify**: Report exists and PASS → mark PASS. Report exists and FAIL → mark FAIL with summary of failures. No report → mark SKIPPED with note: "No manual test report found for this version. Run `/pair-capability-execute-manual-tests` to generate one."

## Output Format

Present results as:

```text
DEFINITION OF DONE REPORT:
├── Requirements:  [PASS | FAIL — N unmet AC | SKIPPED — no $story]
├── Code Standards: [PASS | FAIL — N issues | SKIPPED]
├── Architecture:  [PASS | FAIL — N gaps | HALT — missing ADR | SKIPPED]
├── Testing:       [PASS | FAIL — N gaps | SKIPPED]
├── Security:      [PASS | FAIL — N issues | SKIPPED]
├── Performance:      [PASS | FAIL — N issues | SKIPPED]
├── Documentation:    [PASS | FAIL — N gaps | SKIPPED]
└── Manual Testing:   [PASS | FAIL — N failures | SKIPPED — no suite or no report]

RESULT: [ALL CRITERIA MET | N criteria failing | HALT — reason]
```

## Composition Interface

When composed by `/pair-process-review`:

- **Input**: /pair-process-review invokes `/pair-capability-verify-done` during the completeness phase (Phase 4).
- **Output**: Returns the DoD report. /pair-process-review incorporates findings into the review output.
  - HALT conditions (missing ADR) propagate to /pair-process-review.
  - FAIL criteria become review findings.
  - SKIPPED criteria are noted but do not block.

When invoked **independently**:

- Run all criteria groups (or scoped groups if `$scope` is provided).
- Report results. This skill only reads and reports — it does not modify code.

## Graceful Degradation

- If [definition-of-done.md](../../../.pair/knowledge/guidelines/quality-assurance/quality-standards/definition-of-done.md) is not found, warn and check only adoption-derived criteria.
- If adoption files are missing, warn and check only universal DoD criteria.
- If `$story` is not provided, skip requirements/AC check and evaluate only universal criteria.
- If specific guideline files are not found (e.g., security guidelines), skip that criterion group and report: "[Area]: SKIPPED — guidelines not found."
- If /pair-capability-verify-quality already ran in the same session, reuse its results for code standards and testing criteria (avoid duplicate work).
- If no manual test suite exists (`qa/` directory not found), Step 9 is SKIPPED — this is expected for projects without a manual test suite.
- If a manual test report exists but is for a different version, mark SKIPPED with note about version mismatch.

## Notes

- This skill is **read-only** — it inspects code and configuration but never modifies files.
- Criteria evaluation is contextual: only changes in the PR/work item are assessed, not the entire codebase.
- SKIPPED criteria (no relevant changes) are distinct from PASS (verified and conformant).
- HALT on missing ADR: if architectural changes lack an ADR, this is escalated to the composing skill. /pair-capability-verify-done itself does not create ADRs — that is /record-decision's responsibility.
