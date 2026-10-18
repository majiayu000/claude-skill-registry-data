---
name: create-plan
description: Creates execution-ready `PLAN.md` artifacts by composing `grilling`, `parallel-research`, `swarm-planner`, `tdd`, and `codebase-design` into one planning run. Use when work must be decomposed before coding into a swarm graph of `Tn` tasks with explicit dependencies, backlog items, review gates, and per-task RED targets.
---

# Create Plan

## Contract

- **Role:** higher-order planning orchestrator
- **Entrypoint type:** public entrypoint
- **Upstream:** current retained agent-ready `ARCHITECTURE.md` and `SPEC.md`, including for an explicit planning request
- **Delegates to:** `planning-discovery` for bounded readonly orientation when subagents are available; `$grilling`, `$parallel-research`, `$swarm-planner`, `$tdd`, `$codebase-design`; `plan-reviewer` for the final readonly plan review
- **Downstream:** execution-ready `PLAN.md` for `implement-spec`
- **Entry conditions:** scope is clear enough to plan; stop if required planning inputs or tools are missing
- **Stop conditions:** `PLAN.md` is complete; eligible in-scope backlog sync is
  complete, or an explicit skip reason is recorded; no implementation started

## Required Inner Skills

- MUST use `$grilling`
- MUST consider `$parallel-research` for readonly planning discovery
- MUST use `$swarm-planner`
- MUST use `$tdd`
- MUST use `$codebase-design`
- MUST use `$show-me`
- MUST use `$wait-what`

Create a plan first. Never implement code in this skill.

Before naming or rewriting domain concepts, read the canonical glossary in the
routed `requirements-grill` status artifact. Preserve its canonical terms;
route proposed terminology changes through `requirements-grill` instead of
silently renaming them.

## Quick start

1. Read repo, git, existing plan, and backlog context before asking questions.
   Before planning on any entry or resume, verify the
   **Architecture/SPEC Pair Complete** gate in the installed `delivery-phase`
   skill's `references/artifact-state.md`.
   This includes direct requests and `local` plans. Return missing, stale or
   conflicting proof to Requirements Phase / `requirements-grill`; planning
   cannot choose replacement architecture decisions.
2. Keep a visible planning control panel in the conversation: locked decisions, open decisions, current graph step, and next step.
3. Read `references/grill-ambiguity.md` and run `$grilling` as explicit ambiguity reduction.
4. Update a running decision ledger after every response set, processing each answer individually so the user never has to reconstruct state from memory.
5. After a whole response set is processed, emit any synthesis checkpoint required by `references/grill-ambiguity.md`.
6. After `$grilling` completes, continue to plan synthesis; backlog eligibility
   remains step 14.
7. If readonly discovery has independent code paths, specs, backlog items, external docs, or hypotheses, read and use `$parallel-research` before final task synthesis.
8. Research with `opensrc path <package>` or `opensrc path <owner>/<repo>` plus primary-source web docs when current behavior matters.
9. Locate scoped `AGENTS.md` files for every planned task path. Scoped guidance
   uses one final `## Skills` table with `Skill | Exact trigger`. Select only
   non-phase rows whose exact triggers match the task, then open each selected
   installed skill's `SKILL.md`; that installed file is workflow authority.
   Root `AGENTS.md` stays table-free. Phase wrappers remain global orchestration
   entrypoints and are excluded from scoped tables.
10. For every implementation task, convert applicable scoped or named skill
    obligations into `implementation_skill_guidance`; preserve `assigned_skills`
    as planning provenance.
11. Read `references/architecture-convergence.md`. Persist architecture applicability.
    Derive applicable convergence detail from the current Architecture/SPEC pair;
    route missing or contradictory target design to Requirements Phase /
    `requirements-grill`. Applicability never waives the architecture artifact.
12. Read `references/planner-task-graph.md` and run `$swarm-planner` to produce the swarm graph and `Tn` task contract.
13. Read `references/tdd-shaping.md` and run `$tdd` to attach RED/GREEN targets to each `Tn` task.
14. Read `references/backlog-sync.md`. For eligible projected work, preserve the
    provider Task identities and native blocker graph returned by
    `write-backlog`; otherwise record an explicit skip reason and continue plan
    completion.
15. Invoke `$show-me` to present the task graph, dependencies, waves, and
    validation gates from the complete plan state before `$wait-what`. The
    presentation is a derived view; `PLAN.md` fields remain the execution authority.
16. Before writing `PLAN.md`, invoke `$wait-what` on the complete plan. Proceed
    only when its language contract passes without changing the resolved
    decision ledger.
17. Read `references/stop-conditions.md` and stop exactly there.

## Workflows

### Default workflow

1. Derive host, owner, tracker, and scope from repo state instead of assuming them.
2. Ask only for missing high-impact inputs such as scope, goal, or backlog target.
3. Every plan-shaping question in each `$grilling` round must use the exact block: `Decision`, `Recommendation`, `Question`, `Why it matters`.
4. Keep `$grilling`, `$parallel-research`, `$swarm-planner`, `$tdd`, and `$codebase-design` as visible inputs to one planning run; record when `$parallel-research`, `planning-discovery`, or `plan-reviewer` is used or intentionally skipped because the work is not split-friendly or subagents are unavailable.
5. Build the plan's Wiki Context before task synthesis. Resolve the wiki
   contract with the installed `docs-ingest-phase` skill's
   `references/wiki-contract.md`. Select articles through its discovery
   entrypoints, by each entry's "Applies when" cue, and through search. Read
   each selected article and its supporting sources; check every material claim
   that shapes the plan against primary evidence. Send each novel,
   evidence-backed finding to `docs-ingest-phase`, or record a knowledge no-op.
   Done when the plan's `## Wiki Context` section, in the
   `references/plan-schema.md` format, cites every routed page used or states
   no applicable context.
6. Resolve each task's scoped guidance from root `AGENTS.md` down to the nearest `AGENTS.md` for its `location`.
7. Use each task's required skill guidance while shaping its scope, dependencies, validation, RED target, and review mode; do not merely list skills after the plan is written.
8. Assign each task the deduplicated union of skills whose exact triggers match
   in every touched scope, merging all touched scopes for
   cross-directory tasks.
9. Build worker waves from the selected task-identity mode. Projected work uses
   provider Tasks and native blocker edges. Planning-only work uses the explicit
   unprojected `Tn` graph. Place every currently unblocked Task with a disjoint
   write scope in the same wave. Use a one-Task wave only when blockers or
   ownership leave one Task unblocked.
10. Normalize every task with stable ids, `depends_on`, `location`,
   `owned_paths`, `wave_boundary`, `description`, `validation`, `status`, `log`,
   `files edited/created`, task-identity mode and its required identity fields,
   `assigned_skills`,
   `implementation_skill_guidance`,
   `tdd_status`, `tdd_target`, RED/GREEN commands, evidence fields,
   `codebase_design_notes`, `review_mode`, `runtime_validation`,
   `runtime_target`, `runtime_evidence`, and `runtime_cleanup`. Each task's
   `validation` is focused: tests for the changed behavior, integration checks
   the change directly touches, and type/lint for affected workspaces. CI owns
   the full suite; see [validation scope](../implement-spec/references/validation-scope.md).
    Architecture-bearing tasks also carry the convergence fields required by
    `references/architecture-convergence.md`.
11. Keep the task execution kernel inline: identity, dependencies, owned paths,
    intended outcome and acceptance references, validation/RED/GREEN commands,
    applicable risk gates and Architecture Checkpoint identifiers, status and
    provider identity. Use the task schema for exact fields.
12. Supply detailed specification, code, architecture and skill context through
    resolvable Context Pointers. For a bounded Derived Context Excerpt, retain
    source identity, selector, freshness and subordinate status; source changes
    require refresh. Use the [worker context contract](../implement-spec/references/parallel-worker-brief.md#compact-task-kernel)
    for pointer selection and stale-context handling. Preserve authoritative
    decisions in their source instead of copying whole documents into the plan.
13. For complex work, express the plan as a swarm graph of `Tn` tasks with dependency-aware validation gates, expected outcomes, assertions, or checks that let the executor self-verify before moving on.
14. Stop after plan creation and either eligible in-scope backlog sync or its
    explicit skip record. Do not implement code or spawn implementation workers.

### Stack-aware preservation

If `SPEC.md` contains `Dependency Readiness` or `Branch/Base Intent`, copy those
sections into `PLAN.md` and validate that they are internally consistent.

- Preserve `No Stack Required` or `Ready` plus its dependency evidence.
- Do not decide stack topology in `create-plan`.
- `depends_on` preserves provider-native Task blocker edges. Those delivery
  blockers do not imply stacked PRs; accepted branch/base intent owns PR
  topology separately.
- `Blocked` is invalid agent-ready input. Stop planning and report the stale or
  contradictory spec instead of producing an execution-ready plan.
- If `Branch/Base Intent` is not `Not applicable`, make implementation tasks
  reference that intent as an execution constraint.

### Review modes

- `cli`: tests, commands, APIs, non-visual validation
- `browser`: interactive UI validation
- `mixed`: both are required

## Advanced features

See [REFERENCE.md](REFERENCE.md) for the overview and graph map.

- Grill / ambiguity reduction: see [references/grill-ambiguity.md](references/grill-ambiguity.md)
- Planner / swarm graph: see [references/planner-task-graph.md](references/planner-task-graph.md)
- TDD shaping: see [references/tdd-shaping.md](references/tdd-shaping.md)
- `PLAN.md` schema and task contract: see [references/plan-schema.md](references/plan-schema.md)
- Architecture applicability and convergence contract: see [references/architecture-convergence.md](references/architecture-convergence.md)
- Backlog sync rules: see [references/backlog-sync.md](references/backlog-sync.md)
- Stop conditions: see [references/stop-conditions.md](references/stop-conditions.md)
