---
name: refactoring-executor
description: Execute refactoring safely with test-first verification following best practices. Takes refactoring discovery reports as input and performs incremental refactoring with continuous validation. Ensures tests stay green, captures metrics, and generates execution logs. Use after refactoring-discovery analysis to implement recommended improvements. (project, gitignored)
---

# Refactoring Executor

## Overview

Safely execute refactoring based on discovery reports using test-first verification and incremental steps. This skill automates/guides the refactoring process with continuous validation, metric tracking, and rollback capabilities to ensure zero regression.

## When to Use This Skill

Invoke this skill in the following scenarios:

1. **Post-Discovery Refactoring** - After generating a refactoring-discovery report, execute recommended changes
2. **Test-First Code Improvement** - When refactoring requires validation at each step
3. **Safe Incremental Refactoring** - For complex refactoring that needs small, verifiable steps
4. **Metric-Tracked Improvements** - When you need before/after metrics for refactoring effectiveness

## Prerequisites

### Required Tools
- **TypeScript**: tsc, ts-node
- **Testing**: vitest (or jest)
- **Linting**: eslint
- **Optional**: ts-morph (for automated AST-based refactoring)

### Input Requirements
- Refactoring discovery report (markdown format)
- All tests passing (green baseline)
- Clean git working directory (for rollback capability)

## Core Capabilities

### 1. Report-Driven Execution

Parse refactoring discovery reports and execute recommended changes:
- Select target issue by priority
- Generate execution plan with step-by-step actions
- Validate feasibility and estimate effort

### 2. Test-First Verification

Ensure safety through continuous testing:
- Verify baseline (all tests pass before starting)
- Add characterization tests for missing coverage
- Run tests after each incremental change
- Validate types, lints, and performance metrics

### 3. Incremental Safe Steps

Support major refactoring patterns:
- Extract Method/Function
- Extract Class/Module
- Move Method/Field
- Rename Symbol
- Introduce Parameter Object
- Replace Conditional with Polymorphism
- Encapsulate Field/Collection
- Split Phase

### 4. Execution Logging

Track all changes with detailed logs:
- Before/after metrics (test time, bundle size, warnings)
- Each step's validation results
- Rollback points and procedures
- Decision rationale for each change

## Safety Principles

### Never Break Tests
- All tests must stay green throughout refactoring
- If a test fails, immediately revert the last change
- Investigate failure cause before proceeding

### Small Steps, Frequent Validation
- One intent per change (rename → update usages → delete dead code)
- Commit after each successful validation
- Keep diffs reviewable and meaningful

### Characterization Tests First
- Add tests to lock down existing behavior before structural changes
- Cover edge cases and invariants
- Use snapshot tests for complex outputs

### Preserve Contracts
- Maintain existing API contracts
- Keep non-functional requirements (performance, security)
- Document any intentional breaking changes

### Type-Driven Safety
- Use TypeScript's type system as a safety net
- Enable strict mode (strictNullChecks, noImplicitAny)
- Verify no type errors after each step

## Workflow

### 6-Stage Execution Process

#### Stage 1: Parse Report and Select Target

**Inputs**: Refactoring discovery report (markdown)

**Actions**:
1. Parse report to extract issues, priorities, and recommendations
2. Ask user to select target issue (or auto-select highest priority)
3. Analyze dependencies and affected files
4. Verify no scope conflicts or circular dependencies

**Outputs**:
- Selected issue summary
- Affected file list
- Dependency graph

**Safety Checkpoint**:
- [ ] Issue is actionable and well-defined
- [ ] No conflicts with ongoing work
- [ ] Dependencies are manageable

---

#### Stage 2: Pre-Refactoring Validation

**Actions**:
1. Run full test suite and verify all pass
2. Run type checker (`tsc --noEmit`)
3. Run linter (`eslint`)
4. Capture baseline metrics:
   - Test execution time
   - Test count
   - Type error count (should be 0)
   - Lint warning count
   - Bundle size (if applicable)
   - Performance benchmarks (if available)

**Outputs**:
- `execution-plan.md` (from `assets/execution-plan-template.md`)
- Baseline metrics JSON

**Safety Checkpoint**:
- [ ] All tests pass (100% green)
- [ ] No type errors
- [ ] Git working directory is clean
- [ ] Baseline metrics captured

**Rollback**: If validation fails, stop and report issues to user

---

#### Stage 3: Add Characterization Tests

**Actions**:
1. Identify code paths lacking test coverage
2. Add characterization tests using `assets/characterization-test-template.md`:
   - Given: Initial state
   - When: Action/behavior
   - Then: Expected output (capture current behavior)
3. Run new tests to verify they pass
4. Commit characterization tests separately

**Outputs**:
- New test files (e.g., `*.characterization.test.ts`)
- Test coverage report

**Safety Checkpoint**:
- [ ] New tests pass with current implementation
- [ ] Tests cover critical paths affected by refactoring
- [ ] Tests are deterministic (no flakiness)

**Rollback**: Characterization tests are additive; if they fail, it indicates existing bugs

---

#### Stage 4: Execute Incremental Refactoring

**Actions**:
1. Break refactoring into smallest possible steps
2. For each step:
   a. Apply one refactoring pattern (see `references/refactoring-patterns.md`)
   b. Run verification (see Stage 5)
   c. If verification fails, rollback and adjust
   d. If verification passes, commit with descriptive message
   e. Log step results in `execution-log.md`

**Supported Patterns** (detailed in `references/refactoring-patterns.md`):
- **Extract Method**: Extract code block into named function
- **Extract Class**: Split class into focused classes
- **Move Method**: Relocate method to appropriate class
- **Rename Symbol**: Rename for clarity (auto-update references)
- **Introduce Parameter Object**: Group related parameters
- **Replace Conditional with Polymorphism**: Convert switch/if-else to strategy pattern
- **Encapsulate Field**: Add getters/setters for direct field access
- **Split Phase**: Separate computation from side effects

**Outputs**:
- Modified source files
- Git commits (one per step)
- Execution log entries

**Safety Checkpoint** (per step):
- [ ] Tests pass (no regressions)
- [ ] Types are valid (no new type errors)
- [ ] Linter passes (or warnings documented)
- [ ] Behavior unchanged (same outputs)

**Rollback** (per step):
```bash
git reset --hard HEAD~1  # Revert last commit
# Or use git stash if uncommitted
```

---

#### Stage 5: Step Verification

**Actions** (after each incremental change):
1. Run affected tests:
   ```bash
   pnpm vitest --run --reporter=json --filter <scope>
   ```
2. Run type checker:
   ```bash
   pnpm tsc --noEmit
   ```
3. Run linter:
   ```bash
   pnpm eslint --format=json <affected-files>
   ```
4. Optional: Run performance benchmarks
5. Capture metrics and compare to baseline
6. Log results to `execution-log.md`

**Tool Integration** (see `references/tooling-playbook.md`):
- `scripts/verify-step.sh`: Automated verification script
- `scripts/ts-morph-refactors.ts`: AST-based refactoring helpers

**Outputs**:
- Test results (JSON)
- Type checker output
- Lint results
- Step metrics

**Safety Checkpoint**:
- [ ] All tests pass (same or better than baseline)
- [ ] No new type errors
- [ ] Lint warnings same or fewer
- [ ] Performance within acceptable bounds (<5% regression)

**Rollback**: If any check fails, revert the step and document failure cause

---

#### Stage 6: Post-Refactoring Report

**Actions**:
1. Run full test suite and capture final metrics
2. Compare final vs. baseline metrics
3. Generate execution log using `assets/execution-log-template.md`:
   - Summary of changes
   - Steps taken with validation results
   - Before/after metrics comparison
   - Remaining work (if any)
   - Lessons learned
4. Update refactoring discovery report with completion status
5. Create pull request with:
   - Link to execution log
   - Metric improvements
   - Testing evidence

**Outputs**:
- `execution-log.md` (completed)
- Metrics comparison table
- Pull request description

**Safety Checkpoint**:
- [ ] All tests pass
- [ ] Metrics improved or maintained
- [ ] No regressions introduced
- [ ] Documentation updated

---

## Example Usage Scenarios

### Scenario 1: Extract Large Method

**User**: "Execute refactoring for ComparisonRunner.run() method (667 LOC)"

**Process**:
1. **Parse**: Load refactoring-discovery report, select ComparisonRunner issue
2. **Validate**: Run tests (✅), capture baseline (test time: 12.5s, CC: 45)
3. **Characterization Tests**: Add tests for pairing logic, summary generation, statistical analysis
4. **Step 1**: Extract pairing logic → `PairingStrategy` interface
   - Verify: Tests pass ✅, Types valid ✅, Lint clean ✅
   - Commit: "refactor: extract pairing logic to PairingStrategy interface"
5. **Step 2**: Extract summary generation → `SummaryGenerator` class
   - Verify: Tests pass ✅, Types valid ✅, Lint clean ✅
   - Commit: "refactor: extract summary generation to SummaryGenerator"
6. **Step 3**: Extract statistical analysis → `StatisticalAnalyzer` class
   - Verify: Tests pass ✅, Types valid ✅, Lint clean ✅
   - Commit: "refactor: extract statistical analysis to StatisticalAnalyzer"
7. **Step 4**: Refactor ComparisonRunner to use extracted components
   - Verify: Tests pass ✅, Types valid ✅, Lint clean ✅
   - Commit: "refactor: simplify ComparisonRunner using extracted components"
8. **Report**: Generate execution log
   - Before: 667 LOC, CC 45
   - After: 150 LOC (runner), 100 LOC (pairing), 150 LOC (summary), 100 LOC (analyzer)
   - CC reduced: 45 → 8 (runner), 6 (pairing), 8 (summary), 6 (analyzer)
   - Tests: 100% pass, no regressions
   - Time: 3.5 hours actual

---

### Scenario 2: Split Module by Category

**User**: "Execute refactoring for metrics/index.ts (419 LOC, 3 categories)"

**Process**:
1. **Parse**: Load report, select metrics module issue
2. **Validate**: Baseline captured ✅
3. **Characterization Tests**: All metrics already well-tested ✅
4. **Step 1**: Create `metrics/ranking.ts` and move ranking metrics
   - Verify: Tests pass ✅
   - Commit: "refactor: extract ranking metrics to ranking.ts"
5. **Step 2**: Create `metrics/latency.ts` and move latency metrics
   - Verify: Tests pass ✅
   - Commit: "refactor: extract latency metrics to latency.ts"
6. **Step 3**: Create `metrics/events.ts` and move event metrics
   - Verify: Tests pass ✅
   - Commit: "refactor: extract event metrics to events.ts"
7. **Step 4**: Update `metrics/index.ts` to barrel export
   - Verify: Tests pass ✅, no breaking changes ✅
   - Commit: "refactor: convert metrics/index.ts to barrel export"
8. **Report**: Execution log shows clean split, backward compatible

---

## Reference Materials

### Refactoring Patterns (`references/refactoring-patterns.md`)

Detailed step-by-step guides for each supported pattern:
- Prerequisites and applicability conditions
- Incremental transformation steps
- Type safety checklist
- Rollback procedures
- Common pitfalls and solutions

Load this file when executing specific refactoring patterns.

### Safety Checkpoints (`references/safety-checkpoints.md`)

Critical checkpoints throughout the refactoring process:
- Pre-refactoring validation checklist
- Per-step verification requirements
- Rollback triggers and procedures
- Metric threshold definitions

Load this file to ensure all safety gates are enforced.

### Tooling Playbook (`references/tooling-playbook.md`)

Tool integration and usage examples:
- ts-morph scripts for AST-based refactoring
- vitest/jest command examples and failure diagnostics
- eslint integration with JSON output parsing
- tsc type checking with targeted file validation

Load this file when using automated tooling for refactoring.

## Best Practices

### DO:
- ✅ Always start with green tests
- ✅ Add characterization tests before structural changes
- ✅ Make smallest possible changes
- ✅ Commit after each successful validation
- ✅ Capture metrics before and after
- ✅ Document decisions in execution log
- ✅ Use TypeScript's type system as safety net
- ✅ Rollback immediately on failure

### DON'T:
- ❌ Skip test validation
- ❌ Make multiple changes before verifying
- ❌ Ignore type errors
- ❌ Refactor without characterization tests
- ❌ Proceed with failing tests
- ❌ Forget to capture baseline metrics
- ❌ Skip documentation of changes

## Integration with Development Workflow

### With Refactoring Discovery
1. Run refactoring-discovery to generate report
2. Review report and prioritize issues
3. Use refactoring-executor to implement top-priority changes
4. Re-run refactoring-discovery to verify improvements

### With Pull Requests
- Include execution log in PR description
- Link to refactoring discovery report
- Show before/after metrics
- Highlight test coverage improvements

### With CI/CD
- Run verification script in CI pipeline
- Track metrics over time
- Fail builds on metric regressions
- Generate trend reports

## Resources Summary

### References (Load into context as needed)
- `references/refactoring-patterns.md` - Step-by-step guides for each pattern
- `references/safety-checkpoints.md` - Critical validation checkpoints
- `references/tooling-playbook.md` - Tool integration examples

### Assets (Use in execution)
- `assets/execution-plan-template.md` - Plan template with steps and metrics
- `assets/execution-log-template.md` - Log template for tracking execution
- `assets/characterization-test-template.md` - Template for adding behavior tests

### Scripts (Automation helpers)
- `scripts/parse-report.ts` - Parse refactoring discovery reports
- `scripts/ts-morph-refactors.ts` - AST-based refactoring utilities
- `scripts/verify-step.sh` - Automated step verification

These resources ensure safe, documented, and verifiable refactoring execution.
