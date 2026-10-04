---
name: spec
description: Transform a product brief into a technical specification.
---

# Spec

## Invocation

This skill is performed in the `Architect` persona. If you are not already running as `Architect` (for example, the user invoked `/spec` directly), read `subagents/architect.md` and adopt its role guidance for the rest of this task. Stay in the current chat—do not delegate the skill itself to a subagent. You should, however, aggressively delegate **codebase research** to research subagents (see Codebase Discovery below) so that only their summarized findings—not raw file contents—land in this conversation.

## Objective

Transform a product brief into a technical specification and save it to `docs/specs/{project-name-slug}.md`.

## Instructions

1. Explain the brief-to-spec transformation.
2. Ask for the brief path and extract the goal, target users, constraints, and success metrics.
3. **Codebase discovery.** Before asking the user technical questions, dispatch research subagents in parallel for each independent area the spec needs to ground itself in. Typical areas:
   - existing modules likely to be touched (describe by feature or area, not by guessed file paths)
   - data model / database schema
   - relevant API routes, server actions, and their auth posture
   - existing tests and fixtures for the affected area
   - cross-cutting concerns already in play (feature flags, telemetry, rate limits)

   Each subagent prompt MUST request a **structured summary**, not file dumps. Require the subagent to return:
   - file paths and line ranges of the 3-10 most relevant symbols
   - current ownership boundaries and key types or interfaces
   - constraints, footguns, or TODOs already present
   - what is *not* in the area, to bound scope

   Treat the returned summaries as your working knowledge of the codebase. Only `Read` a file directly in this chat if a subagent summary is insufficient and you need a specific snippet to ground a decision in the spec. Inline `Read`/`Grep` is the exception, not the default.
4. Ask focused technical discovery questions one at a time as needed, informed by the discovery findings:
   - architecture and ownership boundaries
   - data model or schema changes
   - auth and authorization implications
   - external integrations
   - security and privacy concerns
   - performance budgets or expected scale
   - rollout and deployment considerations
5. Read `templates/tech-spec-template.md` and follow its structure. Capture the discovery findings as compact citations (path and line range with a one-line note), not pasted source.
6. Keep the testing plan at the requirements and assertions level, not the implementation level.
7. Save the spec to `docs/specs/{project-name-slug}.md`.
8. If the brief has a status field, update it from draft to completed.
9. End with the spec path, the most important technical decisions, and the recommended next step: `/tdd` or `/code`.
