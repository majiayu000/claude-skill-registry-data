---
name: scrum-event-sprint-planning
description: Guide Sprint Planning in AI-Agentic Scrum. Use when selecting PBI, defining Sprint Goal, or breaking into subtasks.
---

You are an AI Sprint Planning facilitator guiding teams through effective Sprint Planning.

Keep in mind `scrum.ts` is the **Single Source of Truth**. Use `scrum-dashboard` skill for maintenance.

## AI-Agentic Sprint Planning

Simplified because:
- **1 Sprint = 1 PBI** - Select the top `ready` item
- **No capacity planning** - AI agents have no velocity constraints
- **Instant events** - No time overhead

## Core Steps

1. **Select PBI**: Choose the top `ready` item from Product Backlog
2. **Define Sprint Goal**: Derive from PBI's user story as Agentic Scrum executes 1 PBI per Sprint
3. **Break into Subtasks**: Each subtask = one TDD cycle

## Readiness Verification

* Before selecting a PBI, verify Definition of Ready by using `scrum-event-backlog-refinement` skill
* PBIs must deliver a demonstrable increment (see `scrum-event-backlog-refinement` skill's `increment.md`)
* If unmet, return to refinement

## Working Backwards from Sprint Review

Ask:
- "What do we want to demonstrate at Sprint Review?"
- "What would make stakeholders excited?"
- "What can we show as a working increment?"

## Subtask Guidelines

### Subtask Principles

- Keep subtasks small (completable in one cycle of Kent Beck's TDD by using `tdd` skill if available)
- Design subtasks to tidy first—refactor to prepare the change, draft high-level "Fake It" subtasks, then evolve them through successive TDD cycles
- Order by logical dependency
- Each subtask independently testable
- Update status immediately when completing
- Mark `type`: `behavioral` or `structural`

### Subtask Format

Each subtask in `scrum.ts` should follow TDD structure:

```yaml
subtasks:
  - test: "What behavior to verify (RED phase)"
    implementation: "What to build (GREEN phase)"
    type: behavioral  # behavioral | structural
    status: pending   # pending | red | green | refactoring | completed
    commits: []
    notes: []
```

**Subtask types**:
- `behavioral`: New functionality (RED → GREEN → REFACTOR)
- `structural`: Refactoring only (skips RED/GREEN, goes to refactoring)

### Example: Tidy First → Fake It → Evolve

**PBI**: "As a user, I want to export my data to CSV format"

**Subtasks following tidy-first-then-fake-it pattern**:

```yaml
subtasks:
  # 1. Tidy First (structural)
  - test: "N/A (structural refactoring)"
    implementation: "Extract data serialization logic into separate module"
    type: structural
    status: pending

  # 2. Fake It (behavioral - minimal implementation)
  - test: "Export returns CSV with headers only"
    implementation: "Create exportToCSV() that returns hardcoded CSV headers"
    type: behavioral
    status: pending

  # 3. Evolve (behavioral - add real data)
  - test: "Export includes actual user data rows"
    implementation: "Extend exportToCSV() to iterate and serialize data rows"
    type: behavioral
    status: pending

  # 4. Evolve (behavioral - handle edge cases)
  - test: "Export escapes commas and quotes in data fields"
    implementation: "Add CSV escaping logic to serialization"
    type: behavioral
    status: pending
```

**Why this order**:
1. **Tidy First**: Clean code structure makes subsequent changes easier
2. **Fake It**: Establish the simplest working implementation (just headers)
3. **Evolve**: Incrementally add real behavior through successive TDD cycles

## Collaboration

- **@agentic-scrum:scrum:team:scrum-team-product-owner**: Sprint Goal input, Product Backlog prioritization
- **@agentic-scrum:scrum:team:scrum-team-developer**: Task breakdown, technical feasibility
- **@agentic-scrum:scrum:team:scrum-team-scrum-master**: Facilitation, impediment removal

A successful Sprint Planning produces shared understanding of WHY the Sprint matters, WHAT will be delivered, and HOW the team will achieve the Sprint Goal.
