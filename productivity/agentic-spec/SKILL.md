---
name: agentic-spec
description: >
  Create a structured specification before agentic coding work. Assemble the six
  context types, scale rigor for prototype/internal/production tasks, produce
  SPEC.md, and configure focused AGENTS.md boundaries. Use when asked to write a
  spec, plan a feature, design an agent/system, define architecture, or create
  AGENTS.md. Do NOT use for small bug fixes, simple edits, one-off scripts,
  direct implementation requests, or explanation-only questions.
---

# Agentic Spec

Use this skill to convert intent into a compact engineering contract before
implementation. Keep the result proportional; do not create ceremony for work
that only needs a direct fix.

## Workflow

1. Classify rigor:
   - `prototype`: throwaway exploration, personal tool, or demo.
   - `internal`: team feature, workflow automation, or shared tool.
   - `production`: user-facing, security-sensitive, data-sensitive, or agentic
     system with tools/actions.
2. Gather the six context types:
   - Instructions: roles, constraints, repo rules, user priorities.
   - Knowledge: APIs, schemas, business rules, source docs.
   - Memory: relevant project state and previous decisions.
   - Examples: existing patterns, input/output examples, nearby code.
   - Tools: required APIs, MCP servers, CLIs, sandboxes, permissions.
   - Guardrails: explicit boundaries, non-goals, unsafe actions.
3. Generate `SPEC.md` from `assets/templates/SPEC.md`.
4. For AGENTS.md work, apply the filter test: omit anything discoverable from
   the codebase, keep project-level rules under 200 lines, and push scoped rules
   into subdirectories.
5. If requirements are materially ambiguous, ask only the blocking question.
   Otherwise record assumptions in the spec and continue.

## Rigor Scaling

- Prototype: one-page spec, 1-2 edge cases, manual verification acceptable.
- Internal: focused spec, at least 3 edge cases, automated test plan expected.
- Production: full six-context spec, threat/data boundaries, measurable success
  criteria, eval/security/deploy follow-up links.

## References

Read `../agentic-engineering-sdlc/references/day1_sdlc_and_context.md` only
when deeper context-engineering or AGENTS.md guidance is needed.

## Done Criteria

- `SPEC.md` has goal, context, constraints, edge cases, out of scope, and
  success criteria.
- Rigor level is explicit and justified.
- Assumptions and user decisions are separated.
- Next recommended skill is named only when useful: `agentic-evals`,
  `agentic-security-review`, or `agentic-production-readiness`.
