---
name: orchestrate-luna-wb
description: "Coordinate substantial multi-agent work through a fixed two-tier topology: a GPT-5.6-sol coordinator at max reasoning plans the work, delegates bounded execution packets to the preconfigured luna_wb sub-agent (GPT-5.6-luna max), integrates outputs, and independently verifies completion. Use when the user explicitly requests Sol-to-Luna-WB orchestration or when a sizable coding or artifact task contains well-bounded implementation units suitable for Luna WB. Do not use for trivial single-step work, pure questions, or work whose scope is too unclear to delegate safely."
---

# Orchestrate Luna WB

Use GPT-5.6-sol at max reasoning as the sole coordinator and `luna_wb` as the execution worker. Keep planning, authority, integration, and the final completion decision with the coordinator.

## Enforce the topology

1. Confirm that the active coordinator is GPT-5.6-sol with `reasoning_effort: "max"`.
2. If the active model is not confirmed, and model-selectable sub-agents are available, start one dedicated controller with:
   - `agent_type: "default"`
   - `model: "gpt-5.6-sol"`
   - `reasoning_effort: "max"`
   - `fork_turns: "none"`
   - a self-contained copy of the user goal, constraints, skill path, and the marker `controller_confirmed=true`
3. Let that confirmed controller perform all further decomposition and spawn the workers. Do not create another controller after receiving `controller_confirmed=true`.
4. If the required controller cannot be established, report that limitation instead of silently substituting another model or effort level.
5. Confirm that the custom agent type `luna_wb` is available. If it is missing, stop and report that its TOML definition must be installed under `~/.codex/agents/`; do not substitute another worker role.
6. Spawn execution workers only with `agent_type: "luna_wb"`. Do not pass `model` or `reasoning_effort`; the role already fixes GPT-5.6-luna at max reasoning.

Use this worker shape:

```text
spawn_agent({
  task_name: "<short_unique_name>",
  agent_type: "luna_wb",
  fork_turns: "none",
  message: "<complete task packet>"
})
```

## Plan before delegating

Inspect the relevant source, constraints, and current workspace state before assigning work. Form the solution plan in the Sol coordinator.

Delegate only tasks that are:

- concrete enough to execute without changing the goal;
- bounded by explicit ownership and exclusions;
- independently verifiable;
- useful enough to justify coordination overhead.

Keep these responsibilities with Sol:

- resolving ambiguous requirements and choosing architecture;
- dividing ownership and sequencing dependent work;
- handling user communication and approvals;
- reconciling conflicts and integrating results;
- running final verification and deciding whether the task is complete.

Do not delegate trivial work. Do not ask Luna WB to invent the plan, broaden scope, approve destructive or external actions, or issue the final verdict.

## Write a complete task packet

Give every Luna WB worker all task-local context it needs because `fork_turns: "none"` supplies no conversation history. Include:

```text
Objective:
Owned paths or responsibility:
Required implementation:
Inputs and constraints:
Explicitly out of scope:
Acceptance checks:
Return exactly:
  - concise result summary
  - files changed or artifacts produced
  - verification commands and observed results
  - remaining risks or blockers
Coordination rules:
  - You are not alone in the workspace.
  - Do not revert or overwrite others' edits; accommodate concurrent changes.
  - Do not change the assigned goal, boundaries, or acceptance criteria.
  - Do not delegate to another agent.
```

Name owned files or modules whenever edits are involved. Prevent overlapping write ownership. For dependent units, run workers sequentially; parallelize only genuinely independent units and stay within the available agent slots.

## Integrate and verify

1. Continue useful coordinator work while workers run, without editing worker-owned paths.
2. Wait for results without frequent polling.
3. Inspect every returned artifact or diff; treat a worker summary as a claim, not proof.
4. Run the relevant checks from the coordinator environment. Add a targeted check when existing coverage cannot prove an acceptance criterion.
5. If a bounded correction is needed, send it back to the same worker with `followup_task`; state the observed failure and preserve the original scope.
6. Re-plan in Sol if the fix would change architecture, ownership, or user intent.
7. Finish only when the integrated workspace and coordinator-run checks satisfy the user's request.

In the final response, lead with the outcome and report the verification evidence. Mention delegation details only when they help the user understand ownership, risk, or remaining work.
