---
name: orchestrate
description: Run the AgentBoard workspace pipeline from Codex using parallel spawned agents for planning, review, implementation, and audit. Use when the user wants cards progressed end-to-end across a board.
---

# Orchestrate

Use this skill to run the workspace board pipeline inside Codex.

Worker templates live in:

- `references/planning-worker.md`
- `references/review-worker.md`
- `references/implementation-worker.md`
- `references/audit-worker.md`

## Pipeline

1. Planning
2. Review
3. Implementation
4. Audit

Cards flow:

`backlog -> review -> implementation -> audit -> finished`

Rejected work returns to planning/review as appropriate.

## Workflow

1. Load `agentboard` and `workspace-orchestration`.
2. Select the target app and board.
3. Read the board's `auto_transitions` settings.
4. Locate the governing spec document, if applicable.
5. Prime companion analysis tools once for the run.
6. For each wave:
   - collect cards in the wave's input column
   - load the matching worker template from `references/`
   - use `spawn_agent` to launch one worker per card
   - keep worker scopes isolated per card
   - wait only when the next pipeline step depends on the results
   - update the board based on each worker result
7. Pause at review and audit checkpoints when board settings require it.
8. Present a final board summary.

## Rules

- Use parallel spawned agents only for independent cards.
- Treat review and audit as quality gates, not formality passes.
- Stop on build or verification failure and surface the concrete failure.
- Do not let one worker overwrite another worker's code or card state.
- Reuse the worker templates rather than improvising wave prompts from scratch.

## Spawn Pattern

Use `spawn_agent` with:

- `agent_type: "worker"` for implementation
- `agent_type: "default"` or `worker` for planning, review, and audit depending on whether edits are expected
- a prompt built from the matching worker template plus live card variables
- explicit ownership of the card and any expected write scope

Pass only the context the worker needs:

- card identifiers
- spec path when relevant
- approved plan reference when relevant
- target repo path when relevant

## Wave Mapping

- Planning wave -> `references/planning-worker.md`
- Review wave -> `references/review-worker.md`
- Implementation wave -> `references/implementation-worker.md`
- Audit wave -> `references/audit-worker.md`
