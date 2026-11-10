---
name: find-unknowns
description: Use when clarifying ambiguous or under-specified requests, GitHub issues, work items, specifications, investigations, or unfamiliar problem domains before design or implementation.
---

# Find Unknowns

Surface what is known, assumed, missing, or tacit before design or implementation. Stay in exploration and verbalization.

This invocation is discovery-only. Use read-only inspection. Do not change repository state or external systems.

## Workflow

### 1. Inspect the Territory

Inspect the request and relevant issue, repository, documentation, contracts, history, and prior art.

- Separate evidence from inference.
- Resolve questions answerable by inspection before questioning the user.
- If a source is unavailable, identify the missing context precisely.
- If sources conflict, surface the conflict instead of choosing silently.

### 2. Map the Unknowns

Use these lenses internally:

- **Known knowns:** Explicit facts, requirements, and constraints.
- **Known unknowns:** Recognized but unanswered questions.
- **Unknown knowns:** Tacit preferences, criteria, and constraints surfaced through examples.
- **Unknown unknowns:** Blind spots revealed by evidence, edge cases, or alternative framings.

Reclassify items as evidence or answers make them explicit.

### 3. Interview Selectively

If material unknowns remain, ask exactly one question and wait for the user's answer. Do not bundle decisions or return the final Discovery Brief during the interview. After each answer, update and reclassify the unknowns, then ask one next material question or proceed to the brief.

Prioritize questions whose answers could materially change the objective, problem framing, scope, success criteria, non-goals, or real constraints.

- Use examples and contrasts to surface tacit criteria.
- Explain unfamiliar concepts before asking for judgment.
- Resolve inspectable facts before questioning the user.
- Do not manufacture questions when the work is clear.
- Split independent problems and ask which one to clarify first.

For a requested single pass, declined answer, or unavailable interaction, produce the brief with remaining material unknowns unresolved or deferred.

Route architecture, public contracts, data models, compatibility, migration, security boundaries, and other one-way-door decisions to Design Preflight unless needed to clarify intent.

### 4. Stop at the Right Point

Stop when no unanswered question could materially change the problem definition, or remaining unknowns are explicitly deferred.

After returning the Discovery Brief, stop. Do not design or implement as part of this invocation.

## Discovery Brief

Return a self-contained brief with this exact shape:

```markdown
# Discovery Brief: <topic>

## Framed Problem
## Evidence and Existing Context
## Clarified Requirements
## Success Criteria
## Non-goals
## Explicit Assumptions and Constraints
## Unknowns
### Resolved
### Unresolved
### Deferred
## Design Preflight Candidates
```

For each unknown, include its impact and evidence, decision, next question, or deferral. Write `None identified` for empty sections.

## Common Mistakes

- Restating the input without finding hidden assumptions.
- Treating every caveat as a user question.
- Selecting a solution before success is clear.
- Mixing unresolved facts with design choices.
- Interviewing after only low-impact unknowns remain.
