---
name: assumption-governance
description: Govern who may make assumptions and how they must be documented. Use when clarifying project-level versus task-local assumptions, recording rationale, and ensuring assumptions appear in pull requests and the GitHub wiki where appropriate.
---

# Assumption governance

## Ownership split
- Spec owns project-level assumptions in the context of the whole project
- Builder may make only narrow task-local assumptions needed to complete a discrete issue
- If a Builder assumption changes product behavior, scope, or cross-cutting design, escalate it to Spec

## Documentation rule
All meaningful assumptions must be:
1. listed in the PR
2. justified with reasoning
3. documented in the appropriate wiki page when they affect project understanding, behavior, or architecture

## Disagreement handling
If agents disagree about the right assumption or quality threshold:
- Orchestrator decides
- all agents should respect that decision to avoid recursive loops
