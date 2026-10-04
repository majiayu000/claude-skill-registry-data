---
name: writing-plans
description: Use when work needs an implementation plan because it is architectural, cross-component, risky, migration-heavy, multi-stage, long-running, or explicitly requested as a plan.
---

# Writing Plans

## Complexity Gate

Write an implementation plan when any of these apply:

- The user explicitly asks for a plan.
- An approved design or specification is ready for implementation planning.
- The work changes architecture, cross-component contracts, public APIs, permissions, security, billing, or durable data.
- The work includes migrations, compatibility transitions, rollout sequencing, recovery requirements, or difficult rollback.
- Delivery has multiple meaningful stages, owners, repositories, deployments, or long-running checkpoints.
- Correctness depends on resolving sequencing, interface, or verification choices before implementation.

Use a short internal plan when the outcome is clear and the work has no meaningful sequencing or unresolved contract decisions. A change to behavior or several files does not by itself require a separate plan document. Inspect discoverable details before deciding; preserve the user's requested planning depth.

If high-impact product or architecture decisions remain unresolved, use `brainstorming` before writing the plan.

## Planning Workflow

1. Read the approved requirements, relevant repository instructions, implementation surfaces, contracts, tests, and deployment conventions.
2. Confirm the goal, scope, non-goals, constraints, and unresolved assumptions. Do not silently turn an implementation plan into a new design.
3. Map the files and contracts that create meaningful implementation boundaries.
4. Organize work into independently understandable, verifiable outcomes. Fold mechanical setup and documentation into the outcome they support.
5. Add cross-cutting verification, rollout, observability, rollback, and completion criteria where relevant.
6. Self-review the plan against the source requirements, repository state, and operational risks.

Save the plan to `docs/superpowers/plans/YYYY-MM-DD-<topic>.md` unless the user or repository specifies another location.

## Plan Contract

Start with:

```markdown
# <Topic> Implementation Plan

**Goal:** <one concrete outcome>
**Source:** <approved spec, issue, or requirements>
**Approach:** <short implementation strategy>
**Scope:** <included work and explicit non-goals>
**Key risks:** <material risks and mitigations>
**Completion:** <observable conditions that mean the work is done>
```

Then include only the sections relevant to the work:

### File and Contract Map

Name the files or directories expected to change and their responsibilities. Identify contracts that must remain aligned, such as API shapes, events, schemas, generated clients, feature flags, permissions, or cross-repository interfaces.

### Implementation Boundaries

Use one section per meaningful outcome:

```markdown
## N. <Outcome>

**Files:** <exact paths or the narrowest discoverable locations>
**Contracts:** <inputs, outputs, invariants, compatibility requirements>

- <implementation action and important decision>
- <error, fallback, migration, or cleanup behavior when relevant>

**Verification:**
- <targeted automated tests and exact commands when known>
- <integration, manual, or operational evidence when needed>

**Complete when:** <observable boundary-specific result>
```

Choose boundaries where an implementer or reviewer can evaluate a coherent result. Avoid decomposing work into tiny edits that have no independent behavior or verification value.

### Cross-Cutting Verification

Cover the applicable layers:

- focused unit or component tests
- integration and contract tests
- typecheck, lint, build, or generated-artifact checks
- migration rehearsal, backfill validation, or compatibility checks
- staging, preview, browser, or production verification in the environment relevant to the requested rollout
- observability signals, rollback conditions, and recovery steps

Do not invent commands or environments. Derive them from repository scripts, CI, runbooks, and deployment configuration.

### Rollout and Completion

For risky or staged work, state ordering, ownership, feature-flag or migration sequencing, monitoring, rollback, and the evidence required before advancing. Finish with repository-wide completion criteria that connect implementation, verification, documentation, and rollout.

## Detail Calibration

- Record exact names, paths, signatures, schemas, and commands when they resolve real ambiguity.
- Prefer behavioral descriptions, contracts, and pseudocode over full implementation code.
- Include code only when a precise snippet is necessary to lock down a subtle interface, migration, algorithm, or test expectation.
- Keep low-risk sections brief and expand the areas with irreversible decisions, cross-component coordination, or operational risk.
- Use explicit discovery steps only when information cannot be determined while planning; name the artifact or command that will resolve it.

## Handoff

For an authorized implementation request, continue into implementation after the plan is ready. Do not stop to ask whether to execute it or require the user to choose a workflow. Ask only about unresolved decisions that materially change the outcome or require additional authorization. A planning-only request ends with the plan.

Keep planning separate from implementation and review orchestration:

- Use `subagent-driven-development` when executing a written plan with suitable independent implementation tasks in the current session.
- Use another implementation workflow when tasks are tightly coupled or the user selects a different execution approach.
- Use `running-subagent-reviews` for focused fresh-context review passes over a plan, diff, PR, or handoff. It reviews work; it does not replace the implementation workflow.

## Self-Review

Before handoff, verify:

- Every requirement and explicit non-goal maps to a plan boundary or completion criterion.
- Files, contracts, sequencing, and ownership agree across sections.
- Risks cover data, security, compatibility, deployment, and rollback where applicable.
- Verification names the right test layers and relevant environments.
- Tasks are meaningful outcomes rather than arbitrary file edits or ceremonial micro-steps.
- The plan contains no placeholders, invented commands, or unnecessary full implementation code.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for upstream attribution and licensing.
