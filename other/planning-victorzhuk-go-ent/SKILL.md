---
name: planning
description: Task decomposition, planning methodology, and triage. Covers feasibility assessment, phased planning, and dependency management.
triggers:
  - plan
  - decompose
  - breakdown
  - task
  - triage
---

## Role

Planning specialist for breaking work into actionable tasks, assessing feasibility, and creating phased implementation plans.

## Triage Decision Tree

```
Clear + Simple (low complexity)
  -> Proceed directly to implementation

Clear + Complex (medium/high)
  -> Design architecture first, then decompose

Unclear requirements
  -> Request clarification (list specific questions)

Needs research
  -> Flag unknowns, investigate before planning

Out of scope / infeasible
  -> Explain why, suggest alternatives
```

### Quick Assessment Checklist

- Is the request clear and actionable?
- Are there obvious blockers?
- What's the rough complexity? (low/medium/high)
- Does it need research or clarification?
- Is it in scope for the project?

### Triage Output

```
Triage Assessment

Clarity: {clear|unclear|needs-clarification}
Complexity: {low|medium|high}
Blockers: {none|list}
Research needed: {yes|no}

Decision: {proceed|clarify|escalate|reject}
Rationale: {brief explanation}
```

## Planning Process

### 1. Understand Requirements
- What problem are we solving?
- Who are the users/consumers?
- What are success criteria?
- Performance requirements?
- Security considerations?
- Constraints (time, resources, compatibility)?

### 2. Analyze Codebase
- Check existing patterns: `rg "func New" internal/repository/`
- Review directory structure: `fd --type d --max-depth 2 . internal/`
- Understand affected components

### 3. Design Solution
- Follow Clean Architecture / DDD patterns
- Consider scalability and failure modes
- Document trade-offs

### 4. Create Implementation Plan

```markdown
# Implementation Plan: [Feature]

## Overview
Brief description, business value.

## Architecture
- Pattern: Clean Architecture / DDD
- Layers affected: Domain, UseCase, Repository, Transport

## Steps

### Phase 1: Domain
1. Entity `internal/domain/entity/xxx.go`
2. Contract `internal/domain/contract/xxx.go`

### Phase 2: Repository
Files: repo.go, models.go, mappers.go, schema.go

### Phase 3: UseCase
Request/Response DTOs, business logic

### Phase 4: Transport
Handler, DTOs, validation

### Phase 5: DI & Testing
```

## Task Decomposition Guidelines

### Task Size
- Each task completable in <4 hours
- Good: "Create User entity" (1-2h), "Implement repository layer" (2-3h)
- Too small: "Add email field" (30min) — merge with related tasks
- Too large: "Build entire auth system" (days) — split further

### Dependencies
- Only add explicit dependencies when tasks MUST wait
- Use clear numbering: 1.1, 1.2, 1.3 (sequential)
- Cross-reference: "Depends on: 1.2"

### Grouping
- Group by layer: Domain -> Repository -> UseCase -> Transport
- Group by phase: Design -> Implementation -> Testing -> Deployment

### Task Format

```markdown
# Tasks: [Feature/Change Name]

## Dependencies
T1.1 -> T1.2 -> T1.3

## Phase 1: [Name]
- [ ] **1.1** Task description
- [ ] **1.2** Task description

## Phase 2: [Name]
- [ ] **2.1** Task description

## Validation
- [ ] Each task completable in <4h
- [ ] Dependencies are clear and correct
- [ ] No gaps in task numbering
```

## Estimation Guidelines

- Domain: 2-4h per entity
- Repository: 4-6h per concept
- UseCase: 2-3h per operation
- Transport: 2-3h per endpoint
- Testing: 50% of implementation
- Integration: 2-4h

## Risk Assessment

For complex plans, evaluate:
- Breaking changes
- Performance implications
- Security considerations
- Migration complexity
- Rollback plan
