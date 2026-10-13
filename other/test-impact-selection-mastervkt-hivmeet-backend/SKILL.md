---
name: test-impact-selection
description: 'Select the smallest high-value test set for HIVMeet changes to accelerate feedback loops. Use after code edits to map changed files to critical tests, prioritize by risk, and decide quick/standard/deep test scope.'
argument-hint: 'Describe changed files, module risk, and expected confidence level.'
user-invocable: true
---

# Test Impact Selection

## Purpose
Increase development speed by running the most relevant tests first while preserving confidence.

This skill is project-scoped and specific to HIVMeet.

## Use When
- After implementing a feature or bug fix
- When full test suite is too slow for iteration
- Before PR to justify selected test scope
- During hotfix to balance speed and risk

## Test Scope Modes
- Quick: fastest confidence for local iteration
- Standard: balanced confidence for PR readiness
- Deep: elevated confidence for high-risk changes

## Mandatory Workflow

### 1. Map Change Surface
- List changed files by layer
- Map each file to module capabilities
- Flag shared code and high-blast-radius components

### 2. Assign Risk
- Low: localized UI-only edits
- Medium: state transitions or repository changes
- High: auth/session, shared models, API contract logic

### 3. Select Minimum Viable Test Set
- Pick tests directly covering changed behavior
- Add neighboring tests for shared dependencies
- Add one smoke check for each impacted critical flow

### 4. Add Guard Tests By Risk
- Medium risk: include error-path and empty-state tests
- High risk: include cross-module integration checks and session safety checks

### 5. Execute And Evaluate
- Run selected tests first
- If failures show structural risk, escalate mode (quick -> standard -> deep)
- Record uncovered risk explicitly when skipping broader suite

### 6. Output Contract
1. Changed files and risk rating
2. Selected tests and rationale
3. Results summary (pass/fail)
4. Escalation decision (if any)
5. Remaining untested risk

## Efficiency Heuristics
- Prioritize deterministic tests with high signal
- Prefer focused tests over broad slow suites during inner loop
- Re-run only impacted tests after small incremental fixes

## Notes
- Pair with regression-guard before merge on medium/high risk work
- Language for responses: French
