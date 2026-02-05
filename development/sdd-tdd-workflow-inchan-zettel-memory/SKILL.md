---
name: sdd-tdd-workflow
description: Guide AI agents through Specification-Driven Development (SDD) + Test-Driven Development (TDD) integrated workflow. Use when implementing complex features, making architectural decisions, or conducting large-scale refactoring that requires clear specifications and test-first development.
---

# SDD + TDD Integrated Workflow

## Overview

This skill guides AI agents through a comprehensive **Specification-Driven Development (SDD)** and **Test-Driven Development (TDD)** integrated workflow: **Spec → Test → Code (STC)**.

The workflow ensures:
- Clear specifications before implementation (RFC/ADR)
- Test cases derived from specifications
- Test-first development (Red-Green-Refactor)
- Validation against specifications
- Iterative refinement

## When to Use This Skill

Apply this workflow based on task complexity:

| Task Type | Apply Workflow |
|----------|----------------|
| Complex new features | ✅ Full SDD+TDD |
| Simple new features | ⚠️ TDD only (skip RFC) |
| Technical decisions | ✅ ADR + TDD |
| Bug fixes | ⚠️ TDD only |
| Large-scale refactoring | ✅ RFC + TDD |
| Small-scale refactoring | ⚠️ TDD only |

**Use this skill when:**
- User explicitly requests SDD/TDD workflow
- Implementing features that affect multiple components
- Making architectural or technology stack decisions
- Refactoring requires specification documentation
- Working on ai-cli-syncer project or similar spec-driven projects

## Core Workflow: 6 Phases

```
Spec → Design Review → Test → Code → Verify → Iterate
```

### Phase 1: Specification (Spec)

**Goal:** Define what to build and why.

**Choose document type:**
- **RFC (Request for Comments)**: New features, user-facing changes, complex refactoring
- **ADR (Architecture Decision Record)**: Technology choices, architectural patterns, data formats

**Key sections to complete:**
- RFC: Summary, Motivation, Technical Design, Test Strategy
- ADR: Context, Considered Options, Decision Outcome, Consequences

**Location:** `docs/specs/rfcs/` or `docs/specs/adrs/`

### Phase 2: Design Review & Breakdown

**Goal:** Analyze spec and create implementation plan.

**Key Activities:**
1. **Requirements Breakdown**: Decompose spec into implementable units
2. **Technical Feasibility**: Evaluate technical viability
3. **Implementation Planning**: Define order, priorities, resources
4. **Risk Identification**: Identify potential issues and mitigation

**Outputs:**
- [ ] Decomposed requirements list
- [ ] Technical feasibility assessment
- [ ] Implementation plan (order, timeline, resources)
- [ ] Risk matrix with mitigation strategies

### Phase 3: Test Definition

**Goal:** Derive test cases from specifications to define success criteria.

**Steps:**
1. Extract Acceptance Criteria from spec's Test Strategy section
2. Write test case descriptions (unit + integration)
3. Document test scenarios (happy path, error handling, edge cases)

**Format:** Given-When-Then structure

### Phase 4: TDD Implementation

**Goal:** Implement using Red-Green-Refactor cycle.

**TDD Cycle:**
1. **Red**: Write failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code while keeping tests passing

**Repeat** for each function/feature.

### Phase 5: Verification

**Goal:** Ensure implementation meets spec and quality standards.

**Checklist:**
- [ ] All tests pass
- [ ] Test coverage ≥ 80%
- [ ] Spec requirements fulfilled
- [ ] Code review completed
- [ ] Manual testing successful

### Phase 6: Iteration

**Goal:** Incorporate feedback and update specs as needed.

**Steps:**
1. Collect feedback (reviews, tests, users)
2. Update spec if implementation discoveries warrant it
3. Update tests to match spec changes
4. Re-verify (return to Phase 5)

## Working with AI Agents

### Requesting SDD+TDD Workflow

**Example prompts:**
```
"Implement the sync command using SDD+TDD workflow from RFC-0001"

"Create an ADR for choosing the configuration format, then implement with TDD"

"Follow SDD+TDD workflow to add user authentication feature"
```

### What the AI Agent Will Do

1. Read and understand the RFC/ADR specification
2. Analyze and break down requirements
3. Create implementation plan and identify risks
4. Derive test cases from Test Strategy section
5. Write tests first (Red)
6. Implement minimal code (Green)
7. Refactor for quality
8. Verify against spec requirements
9. Update spec if needed

### Collaboration Tips

- **Be explicit:** Reference specific RFC/ADR numbers
- **Provide context:** Share relevant spec sections
- **Review checkpoints:** Ask agent to verify spec compliance
- **Iterate openly:** Discuss spec updates during implementation

## Resources

### references/

**full_workflow.md** - Comprehensive workflow documentation including:
- Detailed phase-by-phase instructions
- Workflow diagrams
- Practical implementation examples
- Checklists for each phase
- AI agent collaboration patterns

**When to load:** When detailed guidance is needed for a specific phase, when implementing a complex feature for the first time, or when teaching the workflow to new team members.

---

**Quick Reference:**

| Need | Action |
|------|--------|
| Start new feature | RFC → Design Review → Tests → TDD implement |
| Make tech decision | ADR → Design Review → Tests → TDD implement |
| Understand phases | Read `references/full_workflow.md` |
| Get examples | See "실전 예제" section in full_workflow.md |
| Use checklist | Find phase checklists in full_workflow.md |
