---
name: design
description: Use this skill after Phase 2 Analyze to produce the design artifacts a build depends on — application architecture, data/platform/infrastructure/security architecture, test architecture, test cases, technical specifications, and DevOps pipeline design. Validates existing architecture artifacts against current requirements before writing new ones. Trigger after requirements have been approved, or when the user asks to "design", "architect", "create specs", or "plan the tests". This is the densest phase — consider delegating architecture validation and test-case generation to subagents when available.
next_suggestions:
  - when: design_gate_signed
    suggest: "run /build to write code and unit tests scoped to the plan"
  - when: pending_signoff_for_current_user
    suggest: "write your sign-off at sign-offs/<REQ-ID>-<role>.md, then /build when all roles are covered"
---

# Design (Phase 3)

Produce the artifacts Build will reference and Test will execute against.

## Prerequisite

`.claude/sdlc/gates/analyze-<task-slug>.md` must exist and be signed.

## Artifacts produced (or updated)

All live under `.claude/sdlc/architecture/` with a `manifest.json` index:

1. **Application architecture** — components, integrations, data flow, NFRs (performance, availability, scalability)
2. **Data architecture** — entities, schema changes, flows, retention, classification
3. **Platform architecture** — runtimes, orchestration, environments
4. **Infrastructure architecture** — compute, network, storage, identity
5. **Security architecture** — threat model, controls, secrets handling, authn/authz
6. **Test architecture** — pyramid shape, test types, tooling, environments, test-data strategy
7. **Technical specifications** — API contracts, data contracts, module responsibilities (under `.claude/sdlc/tech-specs/`)
8. **Test cases** — one or more per requirement, each tied to REQ IDs (under `.claude/sdlc/test-cases/`)
9. **DevOps pipeline design** — stages, gates, environments, promotion rules

## Rule: validate before rewriting

If architecture artifacts already exist:

- Read them.
- Produce a **validation report** comparing existing architecture against the current requirements set.
- Surface deltas (new NFRs, new entities, new integrations, new controls) for human decision.
- Only *after* the human agrees, update the affected files. Never wholesale-regenerate a working architecture.

## Test-case rule

Each requirement gets at least one test case. Each test case references:

- The REQ IDs it covers
- The test type (unit / integration / e2e / NFR)
- Preconditions, steps, expected outcome
- Data needs

Use `templates/test-case.md`.

## Tech spec rule

For each in-scope module or service, produce or update a spec under `.claude/sdlc/tech-specs/`. Specs are the contract Build validates its code against — API shape, inputs/outputs, error modes, side effects, NFR commitments.

## Subagent delegation (optional)

When the `architect` or `test-designer` subagents are enabled, run them in parallel:

- `architect` validates existing architecture and proposes changes (read-only over code; write-only into `architecture/`)
- `test-designer` produces test cases from requirements (write-only into `test-cases/`)

The skill coordinates; the human still approves.

## Human gate

Summarize: architecture deltas, test-case count, spec count, pipeline changes. Sign-off goes to `.claude/sdlc/gates/design-<task-slug>.md`.

## What this skill must NOT do

- Do not write application code. That is Build.
- Do not generate a new architecture when a valid one exists — validate first.
- Do not produce test cases that aren't traceable to a REQ ID.

## References

- `templates/tech-spec.md`
- `templates/test-case.md`
- `templates/gate.md`
- `agents/architect.md`
- `agents/test-designer.md`

## Next step hint

After writing the gate file, pipe the `next_suggestions` conditions to `skills/_shared/next-hint.sh` and print any output:

```bash
printf '%s\n' \
  'design_gate_signed|run /build to write code and unit tests scoped to the plan' \
  'pending_signoff_for_current_user|write your sign-off at sign-offs/<REQ-ID>-<role>.md, then /build when all roles are covered' \
  | bash skills/_shared/next-hint.sh
```

Print any output verbatim. If the script outputs nothing, add nothing.
