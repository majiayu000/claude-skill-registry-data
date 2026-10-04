---
name: sdlc-verify
description: Verify implemented TriStar feature against requirements, run test analysis, check edge cases, and invoke domain-specific verification (fraud detection, context matching). Produces scored verification report.
allowed-tools: Read, Grep, Glob, Bash, Skill
---

# SDLC Verify Skill

## Prime Directive

**"Verify, don't validate."**

Validation checks if something conforms to a format. Verification checks if something actually works as intended. This skill does verification - it checks that the implementation satisfies the requirements, handles edge cases, and passes domain-specific checks.

## Arguments

- `--feature=<name>` (required) - Feature name matching existing artifacts

## Prerequisites

- `docs/artifacts/<feature>/problem_spec.md` must exist
- `docs/artifacts/<feature>/design_spec.md` must exist
- `docs/artifacts/<feature>/implementation_plan.md` must exist
- Implementation code must exist (source files from the implementation plan)

## Process

### Step 1: Load Artifacts

Read all feature artifacts:
1. `docs/artifacts/<feature>/problem_spec.md` - Requirements and acceptance criteria
2. `docs/artifacts/<feature>/design_spec.md` - Component design and API contracts
3. `docs/artifacts/<feature>/implementation_plan.md` - Expected files and wave plan
4. `docs/artifacts/<feature>/code_review.md` - Code review findings (if exists)

### Step 2: Aggregate Review Results

If code_review.md exists, extract:
- Outstanding critical/major findings that need verification
- Positives that confirm good implementation
- Any concerns flagged during review

### Step 3: Verify Component Wiring

For each component in the implementation plan:
1. Check that the file exists at the expected path
2. Check that imports and dependencies are correctly wired
3. Verify that the component exports match the design spec interface
4. Check that inter-layer communication follows the 3-layer pattern (Designer -> Hub -> Scout)

### Step 4: Build Requirement Coverage Matrix

For each requirement from problem_spec.md:
- Map to implemented files
- Check that all acceptance criteria have corresponding test cases
- Mark each AC as: COVERED (test exists) / PARTIAL (test exists but incomplete) / MISSING (no test)

### Step 5: Run Test Analysis

Using Bash, attempt to:
1. Run existing unit tests: `npm test` (frontend) and `pytest tests/unit/` (backend)
2. Run integration tests if available: `pytest tests/integration/ -m integration`
3. Collect coverage metrics
4. Report pass/fail/skip counts

If tests cannot run (missing dependencies, not yet set up), note this and assess test FILE existence instead.

### Step 6: Check Edge Cases

For each edge case from the problem spec:
1. Is there a test that covers this edge case?
2. Does the implementation code handle this scenario?
3. Grep for relevant boundary conditions in the code

### Step 7: Domain Verification (TriStar-Specific)

Invoke domain-specific skills via the Skill tool:

**Fraud Detection Verification:**
```
Skill: loyalty-fraud-detection
```
Verify that the implemented feature:
- Checks all relevant risk flags before offer approval
- Blocks activation when severity === 'critical'
- Correctly calculates over-discounting threshold (>30%)
- Handles frequency abuse detection (>3/day)
- Handles offer stacking detection (>2 concurrent)

**Context Matching Verification:**
```
Skill: semantic-context-matching
```
Verify that the implemented feature:
- Scores GPS proximity correctly (scale per tristar-patterns.md)
- Weights context signals appropriately
- Activates only when composite score > 60
- Handles missing signals gracefully
- Respects rate limiting (1/hr/member, 24h dedup, quiet hours)

**Domain Verification Gate:** If either domain skill flags severity === 'critical', the overall verification FAILS regardless of other scores.

### Step 8: Generate Recommendations

Based on findings, generate actionable recommendations:
- Critical: Must fix before shipping
- Major: Should fix before shipping
- Minor: Can fix in a follow-up

### Step 9: Calculate Score

**Score Formula:** 60% requirement coverage + 40% test pass rate

- **Requirement Coverage** (0-100): percentage of ACs marked COVERED
- **Test Pass Rate** (0-100): percentage of tests passing (or file existence if tests cannot run)

**Quality Gates:**
- Score >= 80: PASS - Feature is verified and ready for risk assessment
- Score >= 60, < 80: CONDITIONAL_PASS - Feature can proceed but has gaps
- Score < 60: FAIL - Feature needs more work before proceeding

**Override:** Domain verification failure (critical severity) forces FAIL regardless of score.

### Step 10: Save Verification Report

Save to: `docs/artifacts/<feature>/verification_report.md`

## Output Format

```markdown
# Verification Report: <feature-name>

## Summary
- **Date**: <date>
- **Score**: <N>/100 (Req Coverage: M%, Test Rate: K%)
- **Decision**: PASS / CONDITIONAL_PASS / FAIL
- **Domain Verification**: PASS / FAIL

## Requirement Coverage Matrix

| REQ ID | Description | ACs | Covered | Partial | Missing |
|--------|-------------|-----|---------|---------|---------|
| REQ-001 | ... | 3 | 2 | 1 | 0 |

## Component Wiring Verification

| COMP-ID | File | Exists | Imports OK | Interface OK |
|---------|------|--------|------------|-------------|
| COMP-001 | src/... | YES | YES | YES |

## Test Results

| Test Suite | Tests | Pass | Fail | Skip | Coverage |
|------------|-------|------|------|------|----------|
| Frontend Unit | N | N | N | N | N% |
| Backend Unit | N | N | N | N | N% |
| Integration | N | N | N | N | N% |

## Edge Case Verification

| EC ID | Scenario | Test Exists | Code Handles |
|-------|----------|-------------|-------------|
| EC-001 | ... | YES/NO | YES/NO |

## Domain Verification

### Fraud Detection
- Over-discounting check: PASS/FAIL
- Cannibalization check: PASS/FAIL
- Frequency abuse check: PASS/FAIL/N/A
- Offer stacking check: PASS/FAIL/N/A
- Critical severity blocking: PASS/FAIL

### Context Matching
- GPS scoring: PASS/FAIL/N/A
- Signal weighting: PASS/FAIL/N/A
- Activation threshold (>60): PASS/FAIL/N/A
- Missing signal handling: PASS/FAIL/N/A
- Rate limiting: PASS/FAIL/N/A

## Recommendations

### Critical
1. <recommendation>

### Major
1. <recommendation>

### Minor
1. <recommendation>

## Score Breakdown
| Component | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Req Coverage | 60% | M | M*0.6 |
| Test Rate | 40% | K | K*0.4 |
| **Total** | | | **N** |

## Quality Gate Decision
**<DECISION>**: <rationale>
```

## Reference Files

- `references/verification-steps.md` - Detailed verification procedures for dual-stack
- `references/verification-checklist.md` - TriStar-specific verification checklist
