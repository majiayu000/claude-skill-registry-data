---
name: research-plan-implement
description: Execute a structured Research-Plan-Implement (RPI) workflow with GO/NO-GO gates and artifact generation at each phase. Use for non-trivial features that.
---

# Research-Plan-Implement (RPI) Workflow

A structured three-phase workflow that separates research, planning, and implementation into distinct phases with explicit GO/NO-GO gates between them. Each phase produces durable artifacts that serve as the contract for the next phase, reducing rework and ensuring alignment before code is written.

## When to Use This Skill

Use this skill for:

- New features that touch multiple modules or services
- Changes with unclear scope that need research before committing to an approach
- High-risk modifications where a wrong approach would be costly to reverse
- Cross-team features that benefit from documenting the plan before implementation
- Any task where you want written artifacts to track what was decided and why
- Onboarding scenarios where the developer is unfamiliar with the codebase area

**Trigger phrases**: "research first", "RPI workflow", "research-plan-implement", "investigate before coding", "create a plan document", "multi-phase workflow", "need research artifacts", "document the approach"

## What This Skill Does

Provides a complete RPI workflow including:

- **Research Phase**: Systematic codebase exploration with a GO/NO-GO feasibility recommendation
- **Planning Phase**: Multi-perspective planning (product, UX, engineering) consolidated into a single plan
- **Implementation Phase**: Phase-by-phase execution with test gates and deviation tracking
- **Artifact Generation**: Structured Markdown documents at each phase for auditability
- **Quality Gates**: Explicit GO/NO-GO checkpoints between each phase

## Instructions

### Step 1: Create REQUEST.md

Before starting any research, document the request clearly. This becomes the single source of truth for what needs to be built.

**Create the artifact folder**:

```
rpi/{feature-slug}/
  REQUEST.md
```

**REQUEST.md Template**:

```markdown
# Feature Request: {Feature Name}

## User Story
As a [role], I want to [action] so that [benefit].

## Acceptance Criteria
1. [Criterion 1: specific, testable condition]
2. [Criterion 2: specific, testable condition]
3. [Criterion 3: specific, testable condition]

## Constraints
- [Technical constraint, e.g., must work with existing auth system]
- [Performance constraint, e.g., response time under 200ms]
- [Compatibility constraint, e.g., must support Node 18+]

## Out of Scope
- [Explicitly excluded items to prevent scope creep]

## Priority
[High / Medium / Low]

## Requested By
[Name or team]

## Date
[YYYY-MM-DD]
```

### Step 2: Research Phase

Explore the codebase systematically to determine feasibility and identify the best approach. The research phase answers: "Can we do this, and what is the best way?"

**Research Activities**:

1. **Explore existing patterns**: Read files that implement similar functionality. Identify conventions for naming, file organization, error handling, and testing.
2. **Map dependencies**: Trace imports and call chains to understand what the change will touch. List external libraries, internal modules, and shared utilities involved.
3. **Identify risks**: Look for technical debt, deprecated APIs, known issues, or architectural constraints that could block or complicate the work.
4. **Check for existing solutions**: Search for prior attempts, related PRs, or existing utilities that partially solve the problem.
5. **Estimate complexity**: Based on findings, classify the work as Small (1-2 files, < 1 hour), Medium (3-10 files, 1-4 hours), or Large (10+ files, 4+ hours).

**Produce RESEARCH.md**:

```markdown
# Research: {Feature Name}

## Summary
[2-3 sentence overview of findings]

## Codebase Exploration

### Relevant Files
| File | Purpose | Relevance |
|------|---------|-----------|
| [path] | [what it does] | [why it matters for this feature] |

### Existing Patterns
- [Pattern 1: how similar features are implemented]
- [Pattern 2: conventions to follow]

### Dependencies
- **External**: [libraries]
- **Internal**: [modules]
- **Shared**: [utilities, types, configs]

## Risks
| Risk | Severity | Mitigation |
|------|----------|------------|
| [risk description] | High/Medium/Low | [how to address] |

## Prior Art
- [Existing solutions, related PRs, or partial implementations found]

## Complexity Estimate
**Classification**: [Small / Medium / Large]
**Rationale**: [why]

## GO/NO-GO Recommendation

**Recommendation**: GO / NO-GO

**Rationale**: [detailed explanation]

**Conditions** (if GO): [any prerequisites that must be met before planning]

**Alternative** (if NO-GO): [what to do instead]
```

**Research Phase Gate**:

| Criterion | Required | Check |
|-----------|----------|-------|
| All acceptance criteria are feasible | Yes | Research findings |
| No blocking risks without mitigations | Yes | Risk table |
| Complexity estimate provided | Yes | Complexity section |
| GO/NO-GO recommendation stated | Yes | Recommendation section |

If the research phase produces a NO-GO recommendation, stop here. Document the rationale and discuss with the requester before proceeding.

### Step 3: Planning Phase

Only proceed if the Research phase gave a GO recommendation. The planning phase produces a consolidated plan from three perspectives.

**Perspective 1: Product (pm.md)**

```markdown
# Product Perspective: {Feature Name}

## User Impact
- [How this affects end users]
- [Expected behavior changes]

## Success Metrics
- [Metric 1: how to measure success]
- [Metric 2: how to measure success]

## Rollout Strategy
- [Feature flag? Gradual rollout? Big bang?]

## Documentation Needs
- [User-facing docs to update]
- [Internal docs to update]
```

**Perspective 2: UX (ux.md)**

```markdown
# UX Perspective: {Feature Name}

## Interaction Flows
1. [Step-by-step user flow for primary path]
2. [Step-by-step user flow for error path]

## Accessibility Considerations
- [Keyboard navigation]
- [Screen reader compatibility]
- [Color contrast requirements]

## Edge Cases
- [What happens when input is empty?]
- [What happens when the user is offline?]
- [What happens with very large inputs?]
```

**Perspective 3: Engineering (eng.md)**

```markdown
# Engineering Perspective: {Feature Name}

## Architecture
- [Where this fits in the system]
- [New components vs. modifications to existing]

## Implementation Phases
### Phase 1: [Name]
- Files: [list]
- Changes: [description]
- Tests: [what to test]
- Estimated effort: [time]

### Phase 2: [Name]
- Files: [list]
- Changes: [description]
- Tests: [what to test]
- Estimated effort: [time]

## Testing Strategy
- Unit tests: [scope]
- Integration tests: [scope]
- Manual testing: [checklist]

## Migration / Backward Compatibility
- [Breaking changes?]
- [Migration steps?]
- [Deprecation timeline?]
```

**Consolidate into PLAN.md**:

```markdown
# Plan: {Feature Name}

## Overview
[1-paragraph summary combining all three perspectives]

## Acceptance Criteria (from REQUEST.md)
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

## Implementation Phases
[Copied from eng.md with any adjustments from pm.md and ux.md]

## Testing Strategy
[From eng.md]

## Rollout Strategy
[From pm.md]

## Risk Mitigations
[From RESEARCH.md, updated with any new insights from planning]

## Estimated Total Effort
[Sum of phase estimates]

## Approval
- [ ] Product perspective reviewed
- [ ] UX perspective reviewed
- [ ] Engineering perspective reviewed
- [ ] Plan approved by [approver]
```

**Planning Phase Gate**:

| Criterion | Required | Check |
|-----------|----------|-------|
| All three perspectives documented | Yes | pm.md, ux.md, eng.md exist |
| Implementation phases are ordered and testable | Yes | eng.md phases |
| Every acceptance criterion maps to a test | Yes | Testing strategy |
| Risk mitigations updated from research | Yes | PLAN.md risks |
| Plan approved by human | Yes | Approval checkbox |

### Step 4: Implementation Phase

Only proceed if the Plan is approved. Execute the plan phase-by-phase with test gates between each phase.

**Implementation Workflow**:

```
For each phase in PLAN.md:
  1. Announce: "Starting Phase N: {name}"
  2. Implement the changes listed for this phase
  3. Run tests (existing + new)
  4. If tests fail: fix before moving to next phase
  5. Log progress in IMPLEMENT.md
  6. If deviating from plan: document why in IMPLEMENT.md
```

**IMPLEMENT.md Template**:

```markdown
# Implementation: {Feature Name}

## Status: [In Progress / Complete]

### Phase 1: {Name}
**Status**: [Not Started / In Progress / Complete / Blocked]
**Started**: [timestamp]
**Completed**: [timestamp]

**Changes Made**:
- [file]: [what changed]
- [file]: [what changed]

**Tests**:
- [x] Existing tests pass
- [x] New tests added: [list]
- [x] All tests pass

**Deviations from Plan**:
- [None / description of deviation and rationale]

### Phase 2: {Name}
...
```

**Implementation Phase Gate** (after all phases complete):

| Criterion | Required | Check |
|-----------|----------|-------|
| All phases complete | Yes | IMPLEMENT.md status |
| All tests pass | Yes | Test runner output |
| No unresolved deviations | Yes | Deviations documented and justified |
| Code compiles and lints cleanly | Yes | Build and lint output |

### Step 5: Verification

After implementation is complete, verify that every acceptance criterion from REQUEST.md is satisfied.

**Verification Checklist**:

```markdown
## Verification: {Feature Name}

### Acceptance Criteria Check
| # | Criterion | Met? | Evidence |
|---|-----------|------|----------|
| 1 | [criterion text] | Yes/No | [test name or manual check] |
| 2 | [criterion text] | Yes/No | [test name or manual check] |
| 3 | [criterion text] | Yes/No | [test name or manual check] |

### Final Checks
- [ ] All tests pass
- [ ] No lint errors
- [ ] Documentation updated (if required by pm.md)
- [ ] No TODO items left in code
- [ ] Changes reviewed against PLAN.md

### Result
**Verdict**: PASS / FAIL
**Notes**: [any observations]
```

**Complete Folder Structure**:

```
rpi/{feature-slug}/
  REQUEST.md        # What we are building (Step 1)
  RESEARCH.md       # What we learned (Step 2)
  pm.md             # Product perspective (Step 3)
  ux.md             # UX perspective (Step 3)
  eng.md            # Engineering perspective (Step 3)
  PLAN.md           # Consolidated plan (Step 3)
  IMPLEMENT.md      # Execution log (Step 4)
  VERIFY.md         # Final verification (Step 5)
```

## Best Practices

- **Do not skip the research phase** even for seemingly simple tasks; research often reveals hidden complexity
- **Keep artifacts concise** but complete; they are working documents, not formal reports
- **Update IMPLEMENT.md in real-time** rather than retroactively; this catches deviations early
- **Treat NO-GO as a valid and valuable outcome** of the research phase; it prevents wasted effort
- **Use the perspective documents** (pm.md, ux.md, eng.md) selectively; for purely technical changes, the UX perspective may be a single line noting "no user-facing changes"
- **Store RPI folders in a consistent location** (e.g., project root `rpi/` or `.claude/rpi/`) so they are easy to find and reference
- **Delete or archive RPI folders** after the feature is merged to avoid stale artifacts accumulating
- **Reference artifact file paths** in commit messages and PR descriptions so reviewers can trace the decision history

## Related Skills

- `plan-before-code` - Lighter-weight planning for simpler tasks
- `workflow-orchestrator` - General multi-phase workflow patterns
- `task-coordinator` - Breaking tasks into coordinated subtasks
- `quality-gate-definitions` - Reusable gate criteria for each phase transition

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: Research-Plan-Implement methodology, multi-perspective planning patterns
