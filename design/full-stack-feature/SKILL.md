---
name: full-stack-feature
model: reasoning
description: Meta-skill for orchestrating end-to-end feature development from persona research through deployed, tested code — coordinating skills, commands, and agents across every stage. Use when building a new feature end-to-end, coordinating frontend + backend work, or needing a structured approach from research to production.
---

# Full-Stack Feature Orchestration (Meta-Skill)

Coordinate the entire lifecycle of a feature — from understanding who it's for, through design, implementation, testing, and documentation. This meta-skill routes to the right skill, command, or agent at each stage and enforces stage gates so nothing ships half-baked.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install full-stack-feature
```


---

## When to Use

- Building a new feature end-to-end — you need the full pipeline from research to production
- Frontend + backend work together — the feature spans UI, API, and data layers
- User research should inform implementation — you want personas and specs before writing code
- Coordinating multiple skills — you're unsure which skill or command to invoke at each step
- Onboarding a new feature area — you need a structured approach, not ad hoc implementation
- Teaching a junior developer — walk through the complete feature development process

---

## Orchestration Flow

Every feature moves through eight stages. Small features skip stages (see Complexity Assessment below); large features complete all of them.

```
 1. Persona Research
        ↓
 2. Feature Specification
        ↓
 3. UX/UI Design
        ↓
 4. API Design
        ↓
 5. Frontend Implementation
        ↓
 6. Backend Implementation
        ↓
 7. Testing
        ↓
 8. Documentation
```

---

## Stage Details

### Stage 1 — Persona Research

Understand who the feature is for before designing anything. Define the target user, their goals, pain points, and the journey this feature supports.

**Invoke:** `/create-persona` command → `ai/commands/docs/create-persona.md`
**Skill:** `persona-docs` → `ai/skills/writing/persona-docs/SKILL.md`

**Output:** Persona document describing the target user, their context, and success criteria for this feature.

### Stage 2 — Feature Specification

Translate persona insights into a concrete feature spec — scope, acceptance criteria, edge cases, and technical constraints.

**Invoke:** `feature-specification` skill → `ai/skills/meta/feature-specification/SKILL.md`

**Output:** Feature spec with user stories, acceptance criteria, out-of-scope items, and technical notes.

### Stage 3 — UX/UI Design

Design the interface informed by the persona and spec. Choose the right visual style, layout, and interaction patterns.

**Output:** Component hierarchy, layout decisions, style selections, and responsive behavior plan.

### Stage 4 — API Design

Define the contract between frontend and backend. Design endpoints, request/response shapes, error codes, and authentication requirements.

**Command:** `/create-api-route` → `ai/commands/development/create-api-route.md`

**Output:** API contract (OpenAPI spec or typed route definitions) with validation rules and error handling.

### Stage 5 — Frontend Implementation

Build the UI components, pages, and client-side logic. Use the appropriate framework skill for the project's stack.

**Command:** `/create-component` → `ai/commands/development/create-component.md`

**Output:** Working UI components wired to the API contract, with loading/error states and responsive layout.

### Stage 6 — Backend Implementation

Build the API routes, business logic, data access layer, and background jobs.

**Command:** `/new-feature` → `ai/commands/development/new-feature.md`

**Output:** Implemented API routes, data models, migrations, and business logic passing unit tests.

### Stage 7 — Testing

Validate the feature across unit, integration, and end-to-end layers. Verify acceptance criteria from Stage 2.

**Command:** `/test-feature` → `ai/commands/development/test-feature.md`

**Output:** Passing test suite covering happy paths, edge cases, and error scenarios from the spec.

### Stage 8 — Documentation

Generate user-facing docs, API references, and internal technical documentation.

**Command:** `/generate-docs` → `ai/commands/documentation/generate-docs.md`

**Output:** Updated README, API docs, component storybook entries, and changelog.

---

## Skill Routing Table

| Stage | Primary Skill | Command | Agent |
|-------|--------------|---------|-------|
| 1. Persona Research | `persona-docs` | `/create-persona` | — |
| 2. Feature Spec | `feature-specification` | — | — |
| 3. UX/UI Design | UI/UX skill | — | — |
| 4. API Design | `api-design-principles` | `/create-api-route` | `ai/agents/api/` |
| 5. Frontend | Framework skill (Next.js, React, etc.) | `/create-component` | — |
| 6. Backend | `api-development`, `database-migration-patterns` | `/new-feature` | `ai/agents/migration/` |
| 7. Testing | `testing-workflow`, `e2e-testing-patterns` | `/test-feature` | `ai/agents/testing/` |
| 8. Documentation | — | `/generate-docs` | — |

---

## Stage Gate Checks

Each stage must pass its gate before proceeding. Gates prevent wasted work by catching gaps early.

| Gate | Required Before | Criteria | Blocking? |
|------|----------------|----------|-----------|
| Persona defined | Stage 2 | Target user identified with goals and pain points | Yes |
| Spec approved | Stage 3 | Acceptance criteria written, scope defined, edge cases listed | Yes |
| Design reviewed | Stage 4 | Component hierarchy defined, responsive plan in place | Yes |
| API contract locked | Stage 5 + 6 | Endpoints defined, request/response types agreed, error codes set | Yes |
| Frontend renders | Stage 6 | UI components display with mock data, loading/error states work | No (parallel OK) |
| Backend passes tests | Stage 7 | All API routes return expected responses, validations enforced | Yes |
| Tests pass | Stage 8 | Unit + integration + E2E tests green, acceptance criteria verified | Yes |
| Docs complete | Deploy | API documented, user-facing docs updated, changelog entry added | Yes |

---

## Vertical Slice Strategy

Start with the thinnest possible end-to-end slice, then widen.

**Phase 1 — Thin Slice**
Build one happy path through all layers: a single user action from UI click to database write and back. This proves the architecture works and gives stakeholders something to demo.

```
Example: "User can create a new project"
  UI:      One form with a name field and submit button
  API:     POST /api/projects { name: string }
  DB:      INSERT INTO projects (name) VALUES ($1)
  Test:    E2E test: fill form → submit → see project in list
```

**Phase 2 — Widen**
Add validation, error handling, edge cases, and secondary flows. Each addition follows the same vertical path — never build an entire layer in isolation.

**Phase 3 — Polish**
Loading states, optimistic updates, animations, accessibility, performance optimization, and comprehensive error messages.

---

## Complexity Assessment

Not every feature needs all eight stages. Use this table to determine which stages to include.

| Feature Size | Examples | Stages to Include | Estimated Time |
|-------------|----------|-------------------|----------------|
| **Trivial** | Rename a label, fix copy, adjust spacing | 5 only | < 1 hour |
| **Small** | Add a filter, new form field, simple toggle | 4 → 5 → 6 → 7 | 2-4 hours |
| **Medium** | New CRUD entity, dashboard widget, search feature | 2 → 3 → 4 → 5 → 6 → 7 | 1-3 days |
| **Large** | New user-facing feature area, multi-page flow | All 8 stages | 1-2 weeks |
| **Epic** | New product vertical, major redesign, platform migration | All 8 + ADR + phased rollout | 2-6 weeks |

### How to Assess Complexity

1. **Count the layers touched** — UI only (trivial), UI + API (small), UI + API + DB (medium+)
2. **Count the user flows** — one path (small), 2-3 paths (medium), many paths with branching (large)
3. **Check for unknowns** — known patterns (smaller), new integrations or unfamiliar tech (bump up one size)
4. **Consider blast radius** — isolated change (smaller), cross-cutting concern (bump up one size)

---

## Coordination Patterns

### Frontend and Backend in Parallel

Once the API contract is locked (Stage 4 gate), frontend and backend can proceed simultaneously:

- **Frontend** uses mock data matching the API contract types
- **Backend** implements against the same contract with unit tests
- **Integration** happens when both sides are ready — contract guarantees compatibility

### Handoff Points

Use the `/handoff-and-resume` command when:

- Switching between frontend and backend work
- Pausing mid-feature and resuming later
- Passing work to another developer or agent

### Progress Tracking

Use the `/progress` command to check which stage you're in and what remains.

---

## NEVER Do

1. **NEVER skip persona research for user-facing features** — building without understanding the user leads to features nobody wants
2. **NEVER start coding before the API contract is defined** — frontend and backend will diverge, causing costly rework at integration
3. **NEVER build an entire layer before connecting it end-to-end** — always use vertical slices to prove the architecture first
4. **NEVER skip stage gates to move faster** — gates exist to catch problems when they're cheap to fix, not after they've compounded
5. **NEVER treat testing as a separate phase you can cut** — tests are part of implementation, not an afterthought bolted on at the end
6. **NEVER ship without documentation** — undocumented features become maintenance burdens that slow down every future change
