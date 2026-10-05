---
name: workflow-orchestrator
description: Design and execute end-to-end workflows by chaining multiple skills and managing quality gates between phases. Use for complete feature implementations.
---

# Workflow Orchestrator

Specialized expertise in designing and executing complete development workflows, coordinating multiple skills and phases, managing quality gates, and ensuring comprehensive delivery of complex development tasks.

## When to Use This Skill

Use this skill for:

- End-to-end feature implementations
- Complete testing cycles (unit → integration → E2E)
- Comprehensive code review workflows
- Full release preparation processes
- Migration projects with multiple phases
- Any work requiring coordinated skill usage

**Trigger phrases**: "complete workflow", "end-to-end", "full implementation", "comprehensive process", "multi-phase", "quality gates", "release process"

## What This Skill Does

Provides workflow orchestration capabilities including:

- **Workflow Design**: Creating phase-based execution plans
- **Skill Chaining**: Coordinating multiple specialized skills
- **Quality Gates**: Enforcing criteria between phases
- **Rollback Planning**: Handling failures at any phase
- **Progress Monitoring**: Tracking overall workflow status
- **Outcome Verification**: Ensuring complete delivery

## Instructions

### Step 1: Select Appropriate Workflow Template

**Standard Workflow Templates**:

#### Template A: Feature Implementation Workflow
```
┌─────────────────────────────────────────────────────────────────┐
│                  FEATURE IMPLEMENTATION WORKFLOW                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: PLAN          Phase 2: IMPLEMENT       Phase 3: TEST  │
│  ┌─────────────────┐   ┌─────────────────┐   ┌────────────────┐ │
│  │ plan-before-code│──►│ [language skill]│──►│ unit-tests     │ │
│  │ context-analysis│   │ code-quality    │   │ test-cases     │ │
│  └─────────────────┘   └─────────────────┘   └────────────────┘ │
│         │                      │                     │          │
│         ▼                      ▼                     ▼          │
│    ┌─────────┐           ┌─────────┐           ┌─────────┐     │
│    │ Gate 1  │           │ Gate 2  │           │ Gate 3  │     │
│    │Plan OK? │           │Lint OK? │           │Tests OK?│     │
│    └─────────┘           └─────────┘           └─────────┘     │
│                                                                 │
│  Phase 4: REVIEW         Phase 5: DOCUMENT      Phase 6: SHIP  │
│  ┌─────────────────┐   ┌─────────────────┐   ┌────────────────┐ │
│  │ security-review │──►│ docstrings      │──►│ cicd-architect │ │
│  │ code-quality    │   │ user-docs       │   │ pre-commit     │ │
│  └─────────────────┘   └─────────────────┘   └────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Template B: Testing Workflow
```
Phase 1: Setup      Phase 2: Unit       Phase 3: Integration
┌──────────────┐   ┌──────────────┐    ┌──────────────┐
│test-structure│──►│ unit-tests   │───►│ test-cases   │
│mocks-fixtures│   │ code-coverage│    │              │
└──────────────┘   └──────────────┘    └──────────────┘
       │                  │                   │
       ▼                  ▼                   ▼
  [Gate: Setup]     [Gate: 80%+]       [Gate: Pass]
                      Coverage

Phase 4: Performance    Phase 5: Quality    Phase 6: CI/CD
┌──────────────┐       ┌──────────────┐    ┌──────────────┐
│ performance- │──────►│ mutation-    │───►│cicd-         │
│   testing    │       │   testing    │    │ integration  │
└──────────────┘       └──────────────┘    └──────────────┘
```

#### Template C: Code Review Workflow
```
Phase 1           Phase 2          Phase 3         Phase 4
┌─────────┐      ┌─────────┐      ┌─────────┐     ┌─────────┐
│context- │─────►│code-    │─────►│security-│────►│testing- │
│analysis │      │quality  │      │review   │     │review   │
└─────────┘      └─────────┘      └─────────┘     └─────────┘
     │                │                │               │
     ▼                ▼                ▼               ▼
 [Findings]      [Findings]      [Findings]      [Findings]
                                                       │
                          ┌───────────────────────────┘
                          ▼
                   Phase 5: Report
                   ┌─────────────┐
                   │final-report │
                   └─────────────┘
```

### Step 2: Configure Workflow Phases

**Phase Configuration Template**:

```markdown
## Workflow: [Name]

### Phase 1: [Phase Name]
**Skills**: [skill-1], [skill-2]
**Inputs**: [What this phase needs]
**Outputs**: [What this phase produces]
**Quality Gate**:
- Criterion 1: [Requirement]
- Criterion 2: [Requirement]
**On Failure**: [Action - stop/retry/skip]
**Estimated Duration**: [Time]

### Phase 2: [Phase Name]
...
```

**Example Configuration**:

```markdown
## Workflow: New Feature Implementation

### Phase 1: Planning
**Skills**: plan-before-code, context-analysis
**Inputs**: Feature requirements, codebase access
**Outputs**: Implementation plan, file list, risk assessment
**Quality Gate**:
- Plan reviewed and approved
- All dependencies identified
- Testing strategy defined
**On Failure**: Iterate on plan
**Estimated Duration**: 30 minutes

### Phase 2: Core Implementation
**Skills**: code-quality, [language-cleanup]
**Inputs**: Approved plan, identified files
**Outputs**: Working code, no lint errors
**Quality Gate**:
- Code compiles/transpiles
- Linting passes
- Type checks pass
**On Failure**: Fix issues before proceeding
**Estimated Duration**: 2-4 hours

### Phase 3: Testing
**Skills**: unit-tests, test-cases
**Inputs**: Implementation code
**Outputs**: Test suite, coverage report
**Quality Gate**:
- All tests passing
- Coverage >= 80%
- No regressions
**On Failure**: Fix failing tests or implementation
**Estimated Duration**: 1-2 hours

### Phase 4: Security Review
**Skills**: security-review, dependency-security-audit
**Inputs**: Complete implementation
**Outputs**: Security findings, remediation plan
**Quality Gate**:
- No high/critical vulnerabilities
- All findings addressed or documented
**On Failure**: Address security issues
**Estimated Duration**: 30 minutes

### Phase 5: Documentation
**Skills**: docstrings, user-documentation
**Inputs**: Final implementation
**Outputs**: Updated documentation
**Quality Gate**:
- Public APIs documented
- README updated if needed
**On Failure**: Add missing documentation
**Estimated Duration**: 30 minutes

### Phase 6: Deployment Prep
**Skills**: pre-commit-checklist, code-commit-workflow
**Inputs**: Complete, tested, documented code
**Outputs**: Committed code, PR ready
**Quality Gate**:
- All checks passing
- PR description complete
**On Failure**: Address pre-commit issues
**Estimated Duration**: 15 minutes
```

### Step 3: Execute Workflow with Gates

**Execution Template**:

```markdown
## Workflow Execution: [Name]
**Started**: [timestamp]
**Status**: In Progress

### Phase 1: Planning ✅
**Started**: [time] | **Completed**: [time]
**Outcome**: Plan approved

Gate Check:
- [x] Plan reviewed and approved
- [x] All dependencies identified
- [x] Testing strategy defined

Artifacts:
- Implementation plan (see above)
- File list: [files]

### Phase 2: Implementation 🔄
**Started**: [time] | **Status**: In Progress

Current Progress:
- [x] File 1 modified
- [x] File 2 modified
- [ ] File 3 pending
- [ ] File 4 pending

Gate Check (pending):
- [ ] Code compiles
- [ ] Linting passes
- [ ] Type checks pass

### Phase 3: Testing ⏳
**Status**: Waiting for Phase 2

### Phase 4: Security ⏳
### Phase 5: Documentation ⏳
### Phase 6: Deployment ⏳
```

### Step 4: Handle Phase Failures

**Failure Handling Matrix**:

| Failure Type | Phase | Action | Escalation |
|--------------|-------|--------|------------|
| Plan incomplete | Planning | Iterate | Clarify requirements |
| Lint errors | Implementation | Auto-fix or manual | None |
| Test failures | Testing | Fix code or tests | Review design |
| Security issues | Security | Remediate | Risk acceptance |
| Missing docs | Documentation | Add docs | None |
| CI failures | Deployment | Debug and fix | Rollback if needed |

**Rollback Procedures**:

```markdown
## Rollback Plan

### Phase-Specific Rollback

**If Phase 2 (Implementation) fails catastrophically**:
1. Revert all file changes: `git checkout -- [files]`
2. Return to Phase 1 for plan review
3. Document issues encountered

**If Phase 3 (Testing) reveals design flaws**:
1. Keep test code (it's valuable)
2. Return to Phase 1 with new insights
3. Revise plan with test requirements

**If Phase 4 (Security) finds critical issues**:
1. Assess severity and exploitability
2. Option A: Fix and proceed
3. Option B: Rollback to Phase 2

### Full Rollback
If workflow cannot proceed:
1. Document all learnings
2. Revert to pre-workflow state
3. Create follow-up tasks for future attempt
```

### Step 5: Verify Complete Delivery

**Completion Verification**:

```markdown
## Workflow Completion: [Name]

### Delivery Summary
**Started**: [timestamp]
**Completed**: [timestamp]
**Duration**: [total time]

### Phase Results

| Phase | Status | Duration | Notes |
|-------|--------|----------|-------|
| Planning | ✅ | 25m | Plan v2 after first iteration |
| Implementation | ✅ | 3.5h | 8 files modified |
| Testing | ✅ | 1.5h | 94% coverage |
| Security | ✅ | 20m | 0 issues found |
| Documentation | ✅ | 25m | README + API docs |
| Deployment | ✅ | 10m | PR #123 created |

### Deliverables

| Deliverable | Location | Status |
|-------------|----------|--------|
| Implementation | [branch/PR] | Complete |
| Tests | [path] | 45 tests, 94% coverage |
| Documentation | [path] | Updated |
| PR | [link] | Ready for review |

### Quality Summary
- All quality gates passed
- No known issues or technical debt
- [Any follow-up items]

### Lessons Learned
- [What went well]
- [What could improve]
- [Process improvements for next time]
```

## Best Practices

- **Define gates upfront** - Know criteria before starting
- **Don't skip phases** - Each phase adds value
- **Document as you go** - Capture decisions and issues
- **Fail fast** - Catch issues early in workflow
- **Automate checks** - Use CI/CD for gate verification
- **Time-box phases** - Prevent scope creep
- **Review at gates** - Pause and verify before proceeding
- **Plan rollbacks** - Know how to recover at each phase

## Common Patterns

### Pattern 1: Gated Release Workflow

```
Dev Branch → Feature Gate → Staging → QA Gate → Production
     │            │            │          │          │
     ▼            ▼            ▼          ▼          ▼
  All tests    Code review   E2E tests  Sign-off  Monitor
   passing     approved      passing    received   alerts
```

### Pattern 2: Iterative Refinement Workflow

```
Draft → Review → Refine → Review → Final
  │       │        │        │       │
  ▼       ▼        ▼        ▼       ▼
 v0.1    Feedback  v0.2   Approval  v1.0
```

### Pattern 3: Parallel Phase Workflow

```
                    ┌──────────────┐
                    │   Phase 1    │
                    │   (Setup)    │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼─────┐  ┌──────▼─────┐  ┌──────▼─────┐
    │ Phase 2a   │  │ Phase 2b   │  │ Phase 2c   │
    │ (Backend)  │  │ (Frontend) │  │ (Tests)    │
    └──────┬─────┘  └──────┬─────┘  └──────┬─────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                    ┌──────▼───────┐
                    │   Phase 3    │
                    │ (Integration)│
                    └──────────────┘
```

## Skill Coordination Reference

**Skills by Workflow Phase**:

| Phase | Primary Skills | Supporting Skills |
|-------|---------------|-------------------|
| Planning | plan-before-code | context-analysis, task-coordinator |
| Implementation | [language]-cleanup, code-quality | context-manager |
| Testing | unit-tests, test-cases | mocks-fixtures, performance-testing |
| Security | security-review | dependency-security-audit |
| Documentation | docstrings, user-documentation | api-documentation |
| Deployment | cicd-architect | pre-commit-checklist |

## Quality Checklist

- [ ] Workflow template selected and configured
- [ ] All phases defined with clear inputs/outputs
- [ ] Quality gates specified for each phase
- [ ] Failure handling procedures documented
- [ ] Rollback plan established
- [ ] Time estimates assigned
- [ ] Skill coordination planned
- [ ] Completion criteria defined

## Related Skills

- `task-coordinator` - Breaking down phase tasks
- `context-manager` - Maintaining information across phases
- `plan-before-code` - Initial planning phase
- All domain-specific skills used in phases

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Based on**: awesome-claude-code-subagents patterns, workflow orchestration practices
