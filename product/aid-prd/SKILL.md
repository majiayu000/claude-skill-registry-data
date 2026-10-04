---
name: aid-prd
description: AID Phase 1 - PRD creation. Use for user stories, acceptance criteria, scoping features, transitioning from discovery to tech spec.
---

# Phase 1: PRD

Applies when: Discovery complete, problem validated, stakeholders identified.
Done when: PRD complete, user stories with acceptance criteria, scope defined.
Purpose: Define what will be built with clarity for unambiguous development.

## Deliverables

1. PRD Document - Readable by technical and non-technical
2. User Stories - "As a [role], I want [capability] so that [benefit]"
3. Acceptance Criteria - **Gherkin format (REQUIRED)**, executable specifications
4. Feature Files - Saved to `features/` directory as `.feature` files
5. Scope Definition - In-scope and out-of-scope explicit
6. Traceability - Every requirement links to research or flagged as assumption

Gherkin is REQUIRED because acceptance criteria become the tests; no PRD-to-QA translation step. Gherkin syntax reference: `cucumber-bdd` skill. Deeper guides: `references/user-stories-guide.md`, `references/acceptance-criteria-patterns.md`, `references/prd-template-extended.md`.

## User Story Format

```markdown
### US-001: [Title]
**Research Backing**: [PROJECT]-A-INT-XXX OR ASSUMPTION - [rationale]

**As a** [role]
**I want** [capability]
**So that** [benefit]

**Priority:** [Must Have | Should Have | Could Have | Won't Have]
**Complexity:** [XS | S | M | L | XL]
```

## Acceptance Criteria (Gherkin - REQUIRED)

Save as: `features/[feature-area]/[story-slug].feature`

```gherkin
# Research: [PROJECT]-A-INT-XXX
# PRD: US-001
@[feature-tag] @[priority-tag]
Feature: [Story Title]
  """
  WHY: [Copy the "So that" benefit here]
  """

  As a [role]
  I want [capability]
  So that [benefit]

  Background:
    Given [shared preconditions for all scenarios]

  @smoke @happy-path
  Scenario: [Happy path - main success]
    Given [precondition/context]
    And [additional setup if needed]
    When [user action]
    Then [expected outcome]
    And [additional verification]

  @error-handling
  Scenario: [Error case - validation failure]
    Given [precondition]
    When [invalid action]
    Then [error handling]
    And [user guidance shown]

  @edge-case
  Scenario: [Edge case - boundary condition]
    Given [edge condition]
    When [action]
    Then [expected behavior at boundary]
```

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Implementation in requirements | Keep focused on outcomes |
| Untestable criteria | "Should load in <2s" not "be fast" |
| Missing error cases | Define what happens when things fail |
| Scope creep | Explicit acknowledgment for additions |
| Orphan requirements | Link to research or flag assumption |

## Phase Gate Checklist

### Document Quality
- [ ] PRD document complete
- [ ] User stories follow proper format
- [ ] Scope explicitly defined (in AND out)
- [ ] Dependencies identified
- [ ] Every requirement has research ID OR assumption flag
- [ ] Traceability matrix updated

### Acceptance Criteria (Gherkin) ⭐ REQUIRED
- [ ] Every user story has acceptance criteria in **Gherkin format**
- [ ] Feature files saved to `features/` directory
- [ ] Each story has at least 2 scenarios: happy path + error case
- [ ] All scenarios have appropriate @tags (@critical, @smoke, etc.)
- [ ] Research backing noted as comment in feature files
- [ ] `npm run cucumber:dry` passes (validates Gherkin syntax)

### Validation Command
```bash
npm run cucumber:dry   # Must pass before advancing to Phase 2
```

## PRD Template

```markdown
# [Feature] PRD

## 1. Overview
### Problem Statement
[Problem] **Research**: [ID]

### Goals
[Goals] **Research**: [ID]

### Non-Goals
[Excluded items]

## 2. User Stories
[Stories with research backing]

## 3. Scope
### In Scope
| Item | Research Backing |
|------|------------------|

### Out of Scope
| Item | Rationale |
|------|-----------|

## 4. Dependencies
## 5. Success Metrics
## 6. Assumptions Log
| ID | Assumption | Risk | Validation Plan |
## 7. Open Questions
```

## Role Guidance

| Role | Focus |
|---|---|
| PM | Own PRD, user stories, acceptance criteria |
| Dev | Review feasibility, identify edge cases |
| QA | Review testability, identify scenarios |
| Tech Lead | Validate fit, flag non-functionals |

## Handoff to Tech Spec

- Approved PRD
- Prioritized user stories
- Complete acceptance criteria
- Dependencies identified
- Traceability matrix

Save to: `docs/prd/YYYY-MM-DD-[feature].md`
