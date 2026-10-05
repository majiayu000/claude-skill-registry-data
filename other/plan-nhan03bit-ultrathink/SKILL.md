---
name: plan
description: Create phased implementation plans with risks, assumptions, milestones, and verification criteria
layer: hub
category: workflow
triggers:
  - "/plan"
  - "create a plan"
  - "plan this out"
  - "make an implementation plan"
  - "how should we build this"
inputs:
  - goal: High-level description of what needs to be built or accomplished
  - constraints: Time, tech stack, resource, or scope constraints (optional)
  - context: Relevant codebase state, prior decisions, or domain knowledge (optional)
outputs:
  - plan: Structured multi-phase implementation plan with milestones
  - risks: Identified risks with mitigation strategies
  - assumptions: Explicit assumptions that underpin the plan
  - verification: Success criteria for each phase
linksTo:
  - plan-validate
  - scout
  - research
  - brainstorm
linkedFrom:
  - cook
  - team
  - ship
preferredNextSkills:
  - plan-validate
  - scout
  - kanban
fallbackSkills:
  - brainstorm
  - research
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - Creates plan document in working memory
  - May trigger codebase exploration via scout
---

# Plan Skill

## Purpose

Create structured, phased implementation plans that transform vague goals into actionable sequences of work. Plans produced by this skill are designed to be validated (via `plan-validate`), tracked (via `kanban`), and executed (via `cook` or `team` orchestrators).

A good plan is not a wish list. It is a contract with reality that names its own assumptions and failure modes.

## Workflow

### Phase 1: Goal Decomposition

1. **Clarify the objective** -- Restate the user's goal in precise, testable terms. If the goal is ambiguous, ask exactly one round of clarifying questions (max 3 questions).
2. **Identify scope boundaries** -- What is IN scope vs. OUT of scope. Be explicit.
3. **Map constraints** -- Technical (stack, APIs, infra), temporal (deadlines), resource (single dev vs. team), and quality (MVP vs. production-grade).

### Phase 2: Reconnaissance

4. **Invoke scout if needed** -- If the plan requires understanding existing code, trigger `scout` to map the relevant codebase areas.
5. **Invoke research if needed** -- If the plan involves unfamiliar technology or domain, trigger `research` to gather context.
6. **Inventory existing assets** -- What already exists that can be reused? What must be built from scratch?

### Phase 3: Plan Construction

7. **Define phases** -- Break work into 2-5 sequential phases. Each phase must be independently deliverable (produces a working state).
8. **For each phase, specify:**
   - **Goal**: What this phase accomplishes
   - **Tasks**: Ordered list of concrete work items
   - **Dependencies**: What must exist before this phase starts
   - **Deliverables**: Tangible outputs (files, endpoints, components)
   - **Verification**: How to confirm this phase is complete and correct
   - **Estimated complexity**: Low / Medium / High
9. **Identify cross-cutting concerns** -- Testing strategy, error handling, accessibility, performance targets.

### Phase 4: Risk Assessment

10. **List assumptions** -- Every assumption the plan relies on. Mark each as `verified` or `unverified`.
11. **Identify risks** -- Things that could go wrong. For each risk:
    - **Likelihood**: Low / Medium / High
    - **Impact**: Low / Medium / High
    - **Mitigation**: Concrete action to reduce risk
    - **Contingency**: What to do if the risk materializes
12. **Flag unknowns** -- Things you do not know and cannot estimate. These are not risks; they are gaps that need research.

### Phase 5: Output

13. **Format the plan** using the template below.
14. **Recommend next steps** -- Typically `plan-validate` to stress-test the plan, or `kanban` to begin tracking.

## Plan Template

```markdown
# Plan: [Title]

## Objective
[One sentence. Testable.]

## Scope
- **In scope**: ...
- **Out of scope**: ...

## Constraints
- [constraint 1]
- [constraint 2]

---

## Phase 1: [Name] (Complexity: Low/Med/High)
**Goal**: ...
**Dependencies**: None | [list]
**Tasks**:
1. [ ] Task description
2. [ ] Task description
**Deliverables**: [list of concrete outputs]
**Verification**: [how to confirm completeness]

## Phase 2: [Name] (Complexity: Low/Med/High)
...

---

## Assumptions
| # | Assumption | Status |
|---|-----------|--------|
| A1 | ... | Unverified |
| A2 | ... | Verified |

## Risks
| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| R1 | ... | Medium | High | ... |

## Unknowns
- [thing we do not know yet]

## Recommended Next Steps
- [ ] Validate plan with `plan-validate`
- [ ] Create kanban board with `kanban`
```

## Usage

### Basic
```
/plan Build a REST API for user authentication with JWT tokens
```

### With constraints
```
/plan Build a REST API for user authentication
Constraints: Next.js API routes, Prisma ORM, PostgreSQL, must support OAuth2 Google login, 2-day timeline
```

### With context
```
/plan Add real-time notifications to the existing chat feature
Context: We already have WebSocket infrastructure in /lib/ws.ts, using Socket.io v4
```

## Examples

### Example 1: Simple feature plan

**Input**: "Plan adding dark mode to the app"

**Output structure**:
- Phase 1: CSS variable system and theme context (Low complexity)
- Phase 2: Component migration to CSS variables (Medium complexity)
- Phase 3: Persistence and system preference detection (Low complexity)
- Assumptions: Tailwind is in use (verify), no existing CSS variable system
- Risk: Third-party components may not respect CSS variables (Medium likelihood, Medium impact)

### Example 2: Complex system plan

**Input**: "Plan migrating from REST to GraphQL"

**Output structure**:
- Phase 1: Schema definition and resolver scaffolding (Medium)
- Phase 2: Parallel deployment -- GraphQL alongside REST (High)
- Phase 3: Client migration -- component by component (High)
- Phase 4: REST deprecation and cleanup (Medium)
- Assumptions: All REST endpoints are documented, client code is centralized
- Risks: N+1 query problems, breaking mobile clients, auth middleware compatibility

## Guidelines

- **Prefer small phases** -- A phase should take hours to a day, not weeks.
- **Every phase must be testable** -- If you cannot describe how to verify it, the phase is too vague.
- **Name your assumptions** -- The most dangerous assumptions are the ones you do not realize you are making.
- **Do not plan what you do not understand** -- If a phase involves unknowns, the first task in that phase should be research.
- **Plans are living documents** -- They will change. Build in review points between phases.
- **Bias toward action** -- A good-enough plan executed today beats a perfect plan next week.
