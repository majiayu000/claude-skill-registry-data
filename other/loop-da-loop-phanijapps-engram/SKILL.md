---
name: loop-da-loop
description: Execute a well-defined roadmap end to end by deriving phase JSON, writing specs/plans, implementing each phase through new-spec and work-loop, updating phase status, validating gates, and pausing only after hardening or a true blocker. Use when the user asks to loop through a roadmap, implementation plan, phase list, or docs/implementation-roadmap.md without waiting for per-phase approval.
---

# Loop-Da-Loop

Use this skill when the scope is already defined by a roadmap, ADRs, and
research, and the user wants steady execution without stopping after each slice.

## Preconditions

- A roadmap exists, usually `docs/implementation-roadmap.md`.
- Architecture decisions exist under `docs/adr/`.
- Research or rationale exists under `docs/research/` when the roadmap depends
  on it.
- The repository has a validation story for the stack being changed.

If any source is missing, create the smallest clarifying doc/spec needed to make
the next phase executable, then continue.

## Source Order

Read current state in this order before implementing a phase:

1. `docs/implementation-roadmap.md`
2. `docs/implementation/phases.json` if present
3. relevant `docs/adr/*.md`
4. relevant `docs/research/*.md`
5. existing code, tests, contracts, and docs in the touched boundary

Treat the worktree as authoritative. Do not rely on previous chat memory when a
file or command can prove the current state.

## Workflow

1. Build or refresh `docs/implementation/phases.json`.
   - Use continuous IDs: `PHASE00`, `PHASE01`, ...
   - Each phase must have `phase_id`, `status`, `description`, `spec_file`, and
     `plan_file`.
   - Valid statuses are `DRAFT`, `IN_PROGRESS`, `BLOCKED`, and `DONE`.

2. Select the next phase.
   - Prefer the first non-`DONE` phase.
   - If all phases are `DONE`, inspect the roadmap queue for remaining work.
   - If the roadmap has remaining work, create the next phase entry.
   - If no work remains, run a completion audit before declaring the loop done.

3. Create or update the phase spec and plan.
   - Use `new-spec` for new phase specs.
   - Keep the spec concrete: objective, boundaries, testing strategy,
     acceptance criteria, and assumptions.
   - Keep the plan task-oriented with verification commands.
   - Do not wait for human approval unless the phase changes public contracts,
     adds new infrastructure, or hits a real ambiguity.

4. Mark the phase `IN_PROGRESS` before implementation.

5. Implement through `work-loop`.
   - Keep changes inside the phase boundary.
   - Prefer existing crate/package patterns.
   - Avoid god modules, broad refactors, and speculative abstractions.
   - Log unrelated concerns as technical debt instead of derailing the loop.

6. Validate with the phase-specific gates and relevant repository gates.
   - Always run formatting or lint checks for touched languages.
   - Run contract/docs hooks when contracts, specs, skills, README, or public
     docs change.
   - Run feature gates called out by the user or roadmap, such as sqlite-vec or
     FastEmbed checks.

7. Mark the phase `DONE` only after validation passes.
   - Update spec status and acceptance checkboxes.
   - Update plan checkboxes.
   - Update roadmap shipped-slice notes or queue items.
   - Commit and push if the user requested publishing.

8. Continue to the next phase until the roadmap queue is empty or a strict
   blocker is reached.

## Completion Audit

Before claiming the roadmap loop is complete:

- Verify every phase in `docs/implementation/phases.json` is `DONE`.
- Verify every phase has an existing spec and plan file.
- Verify phase IDs are continuous.
- Verify specs are marked shipped/done.
- Verify `docs/implementation-roadmap.md` has no remaining queue item.
- Run the full validation suite required by the roadmap or repo docs.
- Confirm no tracked generated-file drift remains.

Do not redefine completion around the phases already implemented. The roadmap
and phase ledger decide completion.

## Blocker Policy

Use `BLOCKED` only when progress is impossible without user input or external
state. Do not mark a phase blocked because the work is large, messy, or would
benefit from clarification. If a non-blocking ambiguity exists, choose the
conservative repository-local interpretation, document the assumption, and keep
moving.

## Phase JSON Template

```json
{
  "phase_id": "PHASE##",
  "status": "DRAFT | IN_PROGRESS | BLOCKED | DONE",
  "description": "Simple description",
  "spec_file": "docs/specs/<phase-slug>/spec.md",
  "plan_file": "docs/specs/<phase-slug>/plan.md"
}
```

## Status Update Pattern

Use short progress updates:

- what source you are reading
- what phase you selected
- what you are editing
- what validation passed or failed
- what commit was pushed

Keep updates factual and compact. The loop should feel continuous, not like a
new negotiation for every phase.
