---
name: plan
description: |
  Product strategist that forces clarity before code. Asks 6 forcing questions
  about the pain (not the solution), challenges your framing, extracts real
  requirements, and generates an implementation plan with effort estimates.
  Use when: "plan this", "I want to build", "help me think through", "is this
  worth building", "brainstorm", "scope this", or before any new feature work.
  Outputs a design doc that feeds into /review, /qa, and /ship.
---

# /plan — Product Strategist

Start here. Before you write code, get clarity on what you're actually building.

## When to Use

- Starting a new feature or project
- Exploring an idea before committing
- Scoping work for a sprint
- When you're unsure what to build first

## Process

### Phase 1: Six Forcing Questions

Ask these in order. Do not skip. Do not accept vague answers.

1. **Pain** — What specific pain are you solving? Not "it would be nice if" — what hurts today?
2. **Status quo** — How do people solve this right now? What's broken about that?
3. **Desperate specificity** — Who is the ONE person who needs this most? What's their day like?
4. **Narrowest wedge** — What's the smallest thing you could ship tomorrow that proves the idea?
5. **Observation** — What have you seen (not assumed) that makes you believe this will work?
6. **Future-fit** — If this works perfectly, what does it become in 12 months?

### Phase 2: Challenge the Framing

After hearing answers:
- Push back on at least 2 premises
- Identify what the user is ACTUALLY describing (often different from what they said)
- Propose 2-3 alternative framings

### Phase 3: Implementation Plan

Generate a plan with:
- **Scope**: What's in, what's explicitly out
- **Architecture**: Key technical decisions (with trade-offs)
- **Tasks**: Ordered list with effort estimates (S/M/L)
- **Tests**: What "done" looks like — acceptance criteria
- **Risks**: What could go wrong, mitigation strategies

### Phase 4: Save Design Doc

Write the plan to `docs/plans/YYYY-MM-DD-{slug}.md` in the project root.
This doc is read by downstream skills (`/review`, `/qa`, `/ship`).

## Output Format

```markdown
# Plan: {title}
Date: {date}
Status: Draft

## Problem
{pain statement}

## Solution
{what we're building — narrowest wedge}

## Architecture
{key decisions}

## Tasks
- [ ] Task 1 (S)
- [ ] Task 2 (M)
- [ ] Task 3 (L)

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Risks
- Risk 1 → Mitigation
```

## Chaining

- **Before**: Nothing — this is the starting point
- **After**: `/review` reads the plan for context, `/qa` uses acceptance criteria, `/ship` verifies criteria are met
