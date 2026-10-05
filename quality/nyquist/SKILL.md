---
name: mk:nyquist
version: 1.0.0
preamble-tier: 3
description: Test-to-requirement coverage mapping. Reads plan acceptance criteria and test files, produces a coverage gap report showing which requirements have no tests. Use during Phase 2 (Test) or Phase 4 (Review) to verify test completeness. Named after the Nyquist sampling theorem — sufficient test coverage prevents aliased (missed) requirements. NOT for running tests (see mk:testing); NOT for structural code review (see mk:review).
allowed-tools:
  - Read
  - Grep
  - Glob
source: new
keywords:
  - nyquist
  - test-coverage
  - requirement-mapping
  - coverage-gap
  - acceptance-criteria
when_to_use: Use during Phase 2 or Phase 4 to map test coverage to plan acceptance criteria — finds aliased (missed) requirements. NOT for running tests (see mk:testing) or structural code review (see mk:review).
user-invocable: true
owner: research
criticality: medium
status: active
runtime: claude-code
---

# Nyquist — Test-to-Requirement Coverage Mapping

Maps plan acceptance criteria to test files. Identifies coverage gaps where
requirements exist but no corresponding test validates them.

## When to Use

- Phase 2 (Test): After tester writes initial tests, verify all acceptance criteria are covered
- Phase 4 (Review): As part of test coverage dimension, verify no gaps
- User says "check test coverage", "are all requirements tested", "coverage gaps"
- Before Gate 2: verify implementation matches plan

## Workflow

1. **Load plan** — Read `tasks/plans/YYMMDD-name/plan.md`, extract acceptance criteria
2. **Scan tests** — Glob for test files (`**/*.test.*`, `**/*.spec.*`, `**/test_*.*`)
3. **Map criteria → tests** — For each acceptance criterion, search test descriptions/names for matching keywords
4. **Identify gaps** — Criteria with no matching test = coverage gap
5. **Produce report** — Structured output with mapping table and gap list

## Output Format

```markdown
## Nyquist Coverage Report: [Plan Name]

### Requirement-to-Test Mapping

| # | Acceptance Criterion | Test File | Test Name | Status |
|---|---------------------|-----------|-----------|--------|
| 1 | [criterion text] | src/auth.test.ts | "should authenticate user" | COVERED |
| 2 | [criterion text] | — | — | GAP |
| 3 | [criterion text] | src/api.test.ts | "returns 404 for missing" | COVERED |

### Coverage Summary

- **Total criteria:** N
- **Covered:** N (N%)
- **Gaps:** N

### Gap Details

1. **[criterion text]** — No test found. Suggested test: [brief description]
2. **[criterion text]** — No test found. Suggested test: [brief description]

### Recommendation

[PASS — all criteria covered | WARN — N gaps found, suggest adding tests]
```

## Matching Strategy

- **Keyword matching:** Extract key nouns/verbs from acceptance criteria, search in test `describe`/`it`/`test` strings
- **File path matching:** If criterion mentions "auth", search in `**/auth*test*`
- **Fuzzy matching:** If exact match fails, check for semantic equivalents (e.g., "login" ≈ "authenticate")
- **Manual override:** If no match found, ask user to confirm the gap is real (not a naming mismatch)

## Gotchas

<!-- Populate from real failures. Do not predict. -->

## What This Skill Does NOT Do

- Does NOT write tests — that's the tester agent's job
- Does NOT modify plan files — read-only analysis
- Does NOT replace manual review of test quality — only checks existence, not correctness
- Does NOT run tests — only reads test file contents
