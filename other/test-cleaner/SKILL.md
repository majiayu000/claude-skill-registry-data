---
name: Test Cleaner
description: Multi-phase test suite optimization with adversarial review
---

# Test Cleaner Skill

## Overview
Analyze, optimize, and clean a project's test suite through a multi-phase workflow with adversarial review. Produces machine-readable output and feeds findings into compound-agent memory.

## Methodology

### Phase 1: Analysis
Spawn multiple analysis subagents in parallel:
- **Cargo-cult detector**: Find fake tests, mocked business logic, trivial assertions
- **Redundancy analyzer**: Identify overlapping/duplicate test coverage
- **Independence checker**: Verify tests don't depend on execution order or shared state
- **Invariant tracer**: Map which invariants each test verifies (Lamport framework)
- **Coverage analyzer**: Identify untested code paths and modules

### Phase 2: Planning
Synthesize analysis results into a refined optimization plan:
- Categorize findings by severity (P1/P2/P3)
- Propose specific changes for each finding
- Estimate impact on test suite speed and coverage
- Iterate with subagents until the plan is comprehensive

### Phase 3: Adversarial Review (CRITICAL QUALITY GATE)
**This is THE KEY PHASE -- the most important phase in the entire workflow. NEVER skip, NEVER rush, NEVER settle for "good enough."**

Expose the plan to two neutral reviewer subagents:
- **Reviewer A** (Opus): Independent critique of the optimization plan
- **Reviewer B** (Sonnet): Independent critique from a different perspective

Both reviewers challenge assumptions, identify risks, and suggest improvements.

**Mandatory iteration loop**: After each reviewer pass, if ANY issues, concerns, or suggestions remain from EITHER reviewer, revise the plan and re-submit to BOTH reviewers. Repeat until BOTH reviewers explicitly approve with ZERO reservations. Do not proceed to Phase 4 until unanimous, unconditional approval is reached.

This is the critical quality gate. Loop as many times as needed. The test suite must be bulletproof before execution begins.

### Phase 4: Execution
Apply the agreed changes:
- Machine-readable output format: `ERROR [file:line] type: description`
- Include `REMEDIATION` suggestions and `SEE` references
- Run targeted test validation using the project's test runner (e.g., `pnpm test` with module/path filters)

### Phase 5: Verification
- Run full test suite (`pnpm test`) and linter (`pnpm lint`) after changes
- Compare before/after metrics (count, duration, coverage)
- Feed findings into compound-agent memory via `ca learn`

## Targeted Test Execution
Adapt test commands to the project's stack:
- **Module isolation**: Run tests for a specific module/path (e.g., `pnpm test` with path filter)
- **Subset testing**: Run a subset of tests for fast feedback (e.g., critical/smoke tests only)
- **Full suite**: Run `pnpm test` for complete validation

## Memory Integration
- Run `ca search "test optimization"` before starting
- After completion, capture findings via `ca learn`
- Feed patterns into CCT system for future sessions

## Common Pitfalls
- Deleting tests without verifying coverage is maintained elsewhere
- Optimizing for speed at the cost of correctness
- Settling for partial approval or cutting the Phase 3 review loop short before BOTH reviewers approve with zero reservations
- Making changes without machine-readable output
- Not feeding results back into compound-agent memory

## Quality Criteria
- All 5 phases completed (analysis, planning, review, execution, verification)
- Both adversarial reviewers approved with zero reservations after iterative refinement
- Machine-readable output format used throughout
- Full test suite passes after changes
- Coverage not degraded
- Findings captured in compound-agent memory
