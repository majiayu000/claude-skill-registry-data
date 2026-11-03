---
name: brainstorming
description: This skill should be used when the user wants to brainstorm ideas before implementing a software feature, component, or technical solution. Use when the user says "brainstorm" or wants to explore options before building or architecting something.
license: MIT
---

# Brainstorming

A structured approach to exploring implementation options before committing to a technical direction.

## When to Use

Use for pre-implementation ideation: features, components, UI patterns, APIs, or architectural approaches. Do NOT use for implementation or coding tasks.

## Workflow

### Phase 1: Define Requirements

Ask the user what they're building. Clarify:
- What is the technical goal?
- What is the stack / environment?
- What constraints apply (performance, team size, timeline)?

### Phase 2: Generate Options

Produce 2–3 technical approaches. For each:
- Describe the core implementation idea
- List pros and cons
- Estimate complexity (low / medium / high)

### Phase 3: Evaluate Trade-offs

Walk through the options with the user. Use a comparison table if the decision is non-trivial.

### Phase 4: Select Direction

Help the user pick one approach based on their constraints and priorities.

### Phase 5: Produce Design Doc

Write a brief technical design doc summarizing:
- The chosen approach
- Key decisions and rationale
- Next implementation steps

## Critical Rules

- Always produce exactly 2–3 options — never just one, never more than three
- Always end with a design doc — this is the final deliverable
- Keep the focus on technical feasibility and implementation paths
- If the user asks about naming, marketing, or non-technical topics, note that this skill is scoped to technical brainstorming
