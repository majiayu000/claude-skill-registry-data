---
name: quality-gate-definitions
description: Reusable GO/NO-GO quality gate definitions for multi-phase workflows. Provides predefined gate types, criteria templates, and behavior configuration for.
---

# Quality Gate Definitions

A library of reusable quality gate definitions that can be plugged into any multi-phase workflow. Each gate defines required and optional criteria, automatic and manual checks, and configurable pass/fail behavior. Use these gates as building blocks rather than reinventing checkpoint criteria for every workflow.

## When to Use This Skill

Use this skill for:

- Setting up quality checkpoints in multi-phase development workflows
- Defining GO/NO-GO criteria before implementation, testing, or deployment
- Standardizing quality expectations across team members and projects
- Configuring automated checks that run at phase transitions
- Any workflow where you need explicit approval criteria between phases

**Trigger phrases**: "quality gate", "GO/NO-GO criteria", "gate check", "phase transition criteria", "checkpoint definition", "approval criteria", "gate library", "pass/fail criteria"

## What This Skill Does

Provides quality gate capabilities including:

- **Gate Type Selection**: Choosing the right gate type for each workflow transition
- **Criteria Definition**: Specifying required, optional, automatic, and manual checks
- **Behavior Configuration**: Defining what happens on pass, fail, or partial pass
- **Gate Templates**: Ready-to-use checklists for common gate types
- **Result Tracking**: Reporting templates for gate outcomes and audit trails

## Instructions

### Step 1: Select Gate Type

Choose the appropriate gate type based on where the checkpoint falls in your workflow.

**Gate Type Reference**:

| Gate Type | Placed Between | Primary Purpose |
|-----------|---------------|-----------------|
| Planning Gate | Research and Implementation | Ensure the plan is sound before writing code |
| Implementation Gate | Implementation phases | Verify each phase is complete before starting the next |
| Testing Gate | Implementation and Review | Confirm adequate test coverage and all tests pass |
| Security Gate | Testing and Deployment | Verify no vulnerabilities are introduced |
| Deployment Gate | Staging and Production | Final confirmation before production release |

**Decision Guide**: If your workflow has N phases, you need at most N-1 gates (one between each pair of phases). Start with the highest-risk transition and add gates incrementally. Not every transition needs a formal gate; use judgment.

### Step 2: Define Gate Criteria

For each gate, specify four categories of criteria.

**Criteria Categories**:

| Category | Description | Example |
|----------|-------------|---------|
| **Required** | Must pass for GO. No exceptions. | "All unit tests pass" |
| **Optional** | Should pass. NO-GO only if multiple fail. | "Code coverage above 90%" |
| **Automatic** | Verified by a tool or command. No human needed. | `npm test` exit code 0 |
| **Manual** | Requires human judgment or review. | "Architecture approach is appropriate" |

**Criteria Definition Template**:

```markdown
## Gate: {Gate Name}

### Required Criteria (all must pass)
| # | Criterion | Check Type | How to Verify |
|---|-----------|-----------|---------------|
| R1 | [criterion] | Auto/Manual | [command or process] |
| R2 | [criterion] | Auto/Manual | [command or process] |

### Optional Criteria (aim for all, tolerate 1-2 failures)
| # | Criterion | Check Type | How to Verify |
|---|-----------|-----------|---------------|
| O1 | [criterion] | Auto/Manual | [command or process] |
| O2 | [criterion] | Auto/Manual | [command or process] |
```

### Step 3: Configure Gate Behavior

Define what happens when a gate passes, fails, or partially passes.

**Behavior Options**:

| Outcome | Action | Description |
|---------|--------|-------------|
| **PASS** | Proceed | All required criteria met. Move to next phase. |
| **FAIL (fixable)** | Retry | One or more required criteria failed but can be fixed. Return to current phase, fix, and re-run gate. |
| **FAIL (blocking)** | Stop | A required criterion failed and cannot be fixed within current scope. Escalate to human decision-maker. |
| **PARTIAL** | Conditional proceed | All required criteria met but one or more optional criteria failed. Proceed with documented exceptions. |

**Behavior Configuration Template**:

```markdown
### Gate Behavior: {Gate Name}

**On PASS**:
- Log gate result to {artifact file}
- Announce "Gate {name} PASSED" with summary
- Proceed to Phase {N+1}

**On FAIL (fixable)**:
- Log failure details to {artifact file}
- Return to Phase {N} with specific feedback:
  - Which criteria failed
  - What needs to change
- Re-run gate after fixes (max {N} retries)

**On FAIL (blocking)**:
- Log failure details to {artifact file}
- Stop workflow
- Escalate to {human / team lead / architect}
- Do not proceed until blocker is resolved

**On PARTIAL**:
- Log which optional criteria failed
- Document accepted risk in {artifact file}
- Proceed with acknowledgment
```

### Step 4: Implement Gate Checks

Use the predefined gate library below. Copy the relevant gate template into your workflow and customize the thresholds.

**Gate Library**:

#### Gate: code-compiles

```markdown
## Gate: code-compiles
**Type**: Implementation Gate
**Automation**: Fully automatic

### Required Criteria
| # | Criterion | Command |
|---|-----------|---------|
| R1 | Source compiles without errors | `npm run build` / `cargo build` / `go build ./...` |
| R2 | No type errors | `npx tsc --noEmit` / `mypy .` / `cargo check` |

### On Fail
Return to implementation phase. Compile errors must be fixed before proceeding.
```

#### Gate: lint-passes

```markdown
## Gate: lint-passes
**Type**: Implementation Gate
**Automation**: Fully automatic

### Required Criteria
| # | Criterion | Command |
|---|-----------|---------|
| R1 | Linter reports zero errors | `npm run lint` / `ruff check .` / `cargo clippy` |

### Optional Criteria
| # | Criterion | Command |
|---|-----------|---------|
| O1 | Linter reports zero warnings | Same command, check warning count |

### On Fail
Auto-fix where possible (`--fix` flag). Manual fix for remaining issues.
```

#### Gate: tests-pass

```markdown
## Gate: tests-pass
**Type**: Testing Gate
**Automation**: Fully automatic

### Required Criteria
| # | Criterion | Command |
|---|-----------|---------|
| R1 | All existing tests pass | `npm test` / `pytest` / `cargo test` |
| R2 | All new tests pass | Same command (new tests included in suite) |
| R3 | No test regressions | Compare test count: current >= previous |

### Optional Criteria
| # | Criterion | Command |
|---|-----------|---------|
| O1 | No flaky tests detected | Run test suite twice, compare results |

### On Fail
Fix failing tests or the code that caused them. Do not skip or disable tests to pass the gate.
```

#### Gate: coverage-threshold

```markdown
## Gate: coverage-threshold
**Type**: Testing Gate
**Automation**: Fully automatic

### Required Criteria
| # | Criterion | Command |
|---|-----------|---------|
| R1 | Overall coverage >= {threshold}% | `pytest --cov` / `npx jest --coverage` |
| R2 | New code coverage >= 80% | Coverage diff report |

### Optional Criteria
| # | Criterion | Command |
|---|-----------|---------|
| O1 | No files below 50% coverage | Coverage per-file report |
| O2 | Branch coverage >= {threshold}% | Coverage report with branch analysis |

### On Fail
Add tests for uncovered code paths. Focus on new code first, then existing gaps.
```

#### Gate: no-security-vulns

```markdown
## Gate: no-security-vulns
**Type**: Security Gate
**Automation**: Mostly automatic

### Required Criteria
| # | Criterion | Command |
|---|-----------|---------|
| R1 | No critical/high dependency vulnerabilities | `npm audit` / `pip audit` / `cargo audit` |
| R2 | No hardcoded secrets in diff | Secret scanning tool or manual grep |
| R3 | No new SQL injection vectors | Manual review of database queries |

### Optional Criteria
| # | Criterion | Command |
|---|-----------|---------|
| O1 | No medium dependency vulnerabilities | Same audit command |
| O2 | Security-sensitive changes reviewed by second person | Manual |

### On Fail
Critical and high vulnerabilities are blocking. Update dependencies or refactor code. Medium vulnerabilities are tracked but not blocking.
```

#### Gate: docs-complete

```markdown
## Gate: docs-complete
**Type**: Deployment Gate
**Automation**: Partially automatic

### Required Criteria
| # | Criterion | Check |
|---|-----------|-------|
| R1 | Public API changes have updated docs | Manual review of changed exports |
| R2 | Breaking changes documented in changelog | `grep "BREAKING" CHANGELOG.md` |

### Optional Criteria
| # | Criterion | Check |
|---|-----------|-------|
| O1 | Inline code comments for complex logic | Manual review |
| O2 | README updated if user-facing behavior changed | Manual review |

### On Fail
Add missing documentation before deployment. Prioritize public API docs and breaking change notes.
```

#### Gate: plan-approved

```markdown
## Gate: plan-approved
**Type**: Planning Gate
**Automation**: Manual (human judgment)

### Required Criteria
| # | Criterion | Check |
|---|-----------|-------|
| R1 | Plan addresses all acceptance criteria | Compare plan to request |
| R2 | Implementation phases are ordered and non-overlapping | Review phase list |
| R3 | Testing strategy covers every acceptance criterion | Cross-reference |
| R4 | Risk mitigations are specific and actionable | Review risk table |

### Optional Criteria
| # | Criterion | Check |
|---|-----------|-------|
| O1 | Effort estimate provided for each phase | Review estimates |
| O2 | Rollback strategy documented | Review plan |

### On Fail
Return to planning phase with specific feedback on what needs revision.
```

#### Gate: performance-budget

```markdown
## Gate: performance-budget
**Type**: Deployment Gate
**Automation**: Fully automatic

### Required Criteria
| # | Criterion | Command |
|---|-----------|---------|
| R1 | Response time p95 <= {threshold}ms | Load test or benchmark |
| R2 | Memory usage <= {threshold}MB | Profiler output |
| R3 | Bundle size increase <= {threshold}KB | `du -b dist/` or bundler stats |

### Optional Criteria
| # | Criterion | Command |
|---|-----------|---------|
| O1 | No performance regression vs. baseline | Benchmark comparison |
| O2 | Startup time <= {threshold}ms | Profiler output |

### On Fail
Profile and optimize. If the budget cannot be met, escalate for budget revision with justification.
```

### Step 5: Track Gate Results

Record every gate execution for auditability. This is especially valuable for teams and for post-mortems.

**Gate Result Reporting Template**:

```markdown
# Gate Results: {Workflow Name}

## Summary
| Gate | Result | Date | Attempts |
|------|--------|------|----------|
| plan-approved | PASS | [date] | 1 |
| code-compiles | PASS | [date] | 1 |
| lint-passes | PARTIAL | [date] | 2 |
| tests-pass | PASS | [date] | 1 |
| coverage-threshold | PASS | [date] | 1 |
| no-security-vulns | PASS | [date] | 1 |
| performance-budget | N/A | [date] | - |

## Detailed Results

### Gate: lint-passes (Attempt 1 - FAIL)
**Date**: [timestamp]
**Failed Criteria**:
- R1: 3 lint errors in `src/processor.ts`
**Action Taken**: Auto-fixed 2 errors, manually fixed 1

### Gate: lint-passes (Attempt 2 - PARTIAL)
**Date**: [timestamp]
**Passed Required**: All
**Failed Optional**:
- O1: 2 warnings remaining (cosmetic, documented)
**Decision**: Proceed with documented exceptions

## Exceptions Log
| Gate | Criterion | Accepted Risk | Approved By |
|------|-----------|---------------|-------------|
| lint-passes | O1 (zero warnings) | 2 cosmetic warnings | [name] |
```

## Best Practices

- **Start with fewer gates** and add more as your workflow matures; over-gating slows velocity without proportional quality gains
- **Automate every criterion that can be automated** to reduce human bottlenecks and inconsistency
- **Set thresholds based on your project's current state**, not ideals; a project at 60% coverage should not gate at 90% overnight
- **Review gate definitions quarterly** and adjust thresholds as the project improves
- **Never disable a required criterion to pass a gate**; if a criterion is consistently blocking, either fix the underlying issue or reclassify it as optional with documented rationale
- **Keep gate checks fast** (under 5 minutes each) to avoid workflow stalls
- **Use the PARTIAL outcome** judiciously; it should be the exception, not the norm
- **Share gate results** with the team so everyone knows the quality bar and can see trends over time

## Related Skills

- `workflow-orchestrator` - Orchestrating multi-phase workflows that use these gates
- `task-coordinator` - Coordinating tasks within gated phases
- `plan-before-code` - Planning phase that feeds into the plan-approved gate
- `cross-model-orchestrator` - Multi-model workflows that use gates at model transitions
- `research-plan-implement` - RPI workflow that uses gates between research, plan, and implement phases

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: Quality gate patterns, CI/CD pipeline best practices, multi-phase workflow management
