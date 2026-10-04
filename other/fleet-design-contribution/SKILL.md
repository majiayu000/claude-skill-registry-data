---
name: fleet-design-contribution
description: How architect produces design_input contributions — pattern selection, SRP verification, dependency direction, phase-appropriate depth
user-invocable: false
---

# Architect Design Contribution

## Why This Matters

Without architecture steps before executing, engineers make too many mistakes.
The architect's design_input is a REQUIREMENT — the engineer MUST follow it.
Not a suggestion. Not a recommendation. The blueprint.

## When This Applies

The brain creates a `design_input` contribution task when a story/epic enters
REASONING stage. You produce the design and deliver it via `fleet_contribute`
so the engineer sees it in context during WORK stage.

## Step 1: Gather Context

Call `arch_design_contribution(task_id)` — your group call that gathers:
- Verbatim requirement
- Task description
- Delivery phase (determines design depth)
- Existing analysis/investigation artifacts

## Step 2: Assess the Problem Shape

Before choosing a pattern, understand what KIND of problem this is:

| If the problem is about... | Consider... |
|---------------------------|-------------|
| Complex object construction | Builder pattern |
| Decoupling communication between components | Mediator pattern |
| Reacting to events/changes | Observer pattern |
| Varying algorithm by context | Strategy pattern |
| Simplifying a complex subsystem | Facade pattern |
| Adapting incompatible interfaces | Adapter pattern |
| Separating concerns (data access) | Repository pattern |
| Separating domain from infrastructure | Onion / Hexagonal architecture |
| Configuration-driven behavior | Registry / Factory pattern |

Don't force a pattern. Simple problems get simple solutions. A utility
function is fine when a utility function is all you need.

## Step 3: Phase-Appropriate Design Depth

**The PO decides phases. The architect adapts depth to phase.**

| Phase | Design Depth |
|-------|-------------|
| poc | Simple working structure. Can be single-file. Focus on proving the concept works. |
| mvp | Proper separation of concerns. Domain vs infrastructure. Clean interfaces between modules. |
| staging | Full onion layering. Testable boundaries everywhere. Integration patterns defined. Error handling strategy. |
| production | Production architecture. Scalable. Maintainable. Documented. Performance considered. |

A POC does NOT need an onion architecture. A production feature does NOT
get away with everything in one file.

## Step 4: Produce Design Input

Your design_input must contain:

### 1. Architecture Pattern
Which pattern and WHY. Not just "use repository pattern" — explain what problem
it solves in THIS context.

### 2. File Structure
Where things go. Module names. Directory structure. The engineer should know
exactly which files to create/modify.

```
fleet/core/auth.py         — domain logic (JWT validation, token generation)
fleet/infra/auth_client.py — infrastructure (HTTP calls to auth service)
fleet/mcp/tools.py         — add fleet_auth_check tool
fleet/tests/core/test_auth.py — unit tests
```

### 3. SRP Verification
Does each proposed module have ONE responsibility? If a module does two things,
split it. Call it out explicitly.

### 4. Domain Boundaries
What's core (domain logic, no external deps) vs infrastructure (HTTP, database,
filesystem). Dependencies point INWARD — infra depends on core, never reverse.

### 5. Dependency Direction
All dependencies point inward. Draw the arrow:
`tools.py → core/auth.py ← infra/auth_client.py`
Core never imports from infra. Tools import from core.

### 6. Integration Constraints
How this connects to existing systems. What interfaces must be respected.
What would break if done wrong.

### 7. What to AVOID
Anti-patterns for this specific work. Common mistakes engineers make with
this kind of task. Things that look right but create coupling.

## Step 5: Deliver

```
fleet_contribute(
  task_id=TARGET_TASK_ID,
  contribution_type="design_input",
  content=YOUR_DESIGN
)
```

## What Makes This "Expert" Level

- You don't just pick a pattern — you explain WHY for THIS problem
- You reference SPECIFIC files and line numbers in the existing codebase
- You identify what would go WRONG without architecture guidance
- You adapt depth to the delivery phase — no overengineering POC, no underengineering production
- Your file structure is concrete — the engineer can create the files immediately
- You catch SRP violations before they exist
- You verify dependency direction proactively

## After Delivery

The engineer receives your design_input in their context. During review,
fleet-ops can check: did the implementation follow the architect's design?
If the engineer deviated, that's a review finding.
