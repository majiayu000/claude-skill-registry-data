---
name: requirement-preflight
description: Review a product requirement, PRD, brief, or meeting note before design or development; expose missing decisions, contradictions, edge cases, dependencies, and validation gaps without inventing business rules.
---

# Requirement Preflight

Turn an incoming requirement into an evidence-grounded readiness review that helps product, design, engineering, and QA decide what must be clarified before work proceeds.

## Working rules

- Treat supplied artifacts as the source of truth. Separate explicit facts, reasonable inferences, and unknowns.
- Do not silently complete missing product decisions. Phrase them as assumptions or questions.
- Distinguish a documentation gap from a flawed requirement; missing text alone does not prove the product decision is wrong.
- Cite the relevant section, quote, screen, or source label when available. If provenance is unavailable, say so.
- Prioritize issues by likely impact on scope, user harm, compliance, implementation, or rework—not by writing quality.
- Match the language and depth to the user's audience. Preserve domain terminology from the source.
- Do not modify source documents or external systems unless the user explicitly asks.

## Review workflow

1. Establish the review boundary: the supplied artifacts, intended stage, target users, and known constraints. If context is sparse, still review what exists and label the gaps.
2. Restate the requirement briefly: user problem, business outcome, target users, core scenario, scope, and proposed success signal.
3. Inspect the requirement across the dimensions that materially apply:
   - problem evidence and expected outcome;
   - users, roles, permissions, entry conditions, and exclusions;
   - happy path, alternate paths, recovery, cancellation, and reversibility;
   - loading, empty, error, partial-success, duplicate, timeout, and extreme-data states;
   - business rules, lifecycle states, calculations, limits, and conflicts;
   - data sources, integrations, dependencies, migration, and operational ownership;
   - privacy, security, accessibility, localization, and regulatory constraints;
   - analytics, release strategy, acceptance criteria, and validation plan.
4. Classify findings:
   - **Blocker**: a decision is required before responsible design or implementation can continue.
   - **High rework risk**: work can start, but the uncertainty is likely to change scope or core flow.
   - **Improvement**: clarification would improve quality but need not block progress.
5. Convert findings into answerable questions. Name the likely owner—product, design, engineering, data, legal, operations, or business—when it is evident.
6. End with a readiness recommendation: ready, conditionally ready, or not ready, followed by the smallest next actions.

## Default deliverable

Use a compact structure unless the user requests another format:

1. Requirement snapshot
2. Readiness recommendation and rationale
3. Findings by severity, each with evidence, impact, and owner
4. Missing flows and states
5. Assumptions requiring confirmation
6. Questions for the review meeting
7. Suggested next actions

When comparing versions, add a change-impact section covering resolved questions, new risks, and affected designs, analytics, or acceptance criteria.
