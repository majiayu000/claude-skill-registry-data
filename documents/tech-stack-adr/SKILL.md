---
name: tech-stack-adr
description: Guide technology selection workflow and ADR creation. Use when user asks about choosing a technology, comparing options, or needs to make a tech decision. Orchestrates discovery, evaluation, and documentation.
---

# Tech Stack ADR Workflow

Guide technology selection from discovery to ADR documentation.

## Workflow

```
1. Requirements    → Clarify what user needs
2. Discovery       → tech-stack-discoverer agent finds candidates
3. Evaluation      → tech-stack-evaluator agents (parallel) assess each
4. Comparison      → Present results, discuss trade-offs
5. Decision        → User decides
6. ADR             → Write to docs/adr/YYYYMMDD-<topic>.md
7. Review          → tech-stack-adr-reviewer validates ADR content
```

## Phase 1: Requirements

Ask user:
- What problem are you solving?
- Any constraints? (must integrate with X, no large dependencies, etc.)
- Any candidates already in mind?

## Phase 2: Discovery

Launch `tech-stack-discoverer` agent with requirements.

```
Task: Find candidates for {requirement}
Requirements:
- {requirement 1}
- {requirement 2}
```

## Phase 3: Evaluation

Launch `tech-stack-evaluator` agents **in parallel** for **ALL** candidates found in Phase 2.

**Do NOT filter or narrow down candidates. Evaluate every single one.**

```
Task: Evaluate {technology} for {use case}
Context: {brief project context}
```

## Phase 4: Comparison

Aggregate results into comparison table using criteria from `docs/adr/evaluation-criteria.md`.

Discuss trade-offs with user.

## Phase 5: Decision

User decides. Confirm:
- Chosen option
- Key reasons
- Accepted trade-offs

## Phase 6: ADR

Write ADR to `docs/adr/YYYYMMDD-<topic>.md` using `docs/adr/TEMPLATE.md`.

Reference the ADR in related spec if applicable.

## Phase 7: Review

Launch `tech-stack-adr-reviewer` agent to validate ADR content.

If violations found, fix and re-run review until PASS.
