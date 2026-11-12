---
name: ak-team
description: "Orchestrate Agent Teams of independent teammates for parallel multi-session work."
when_to_use: "Invoke for research, build, review or debug work split across teammates."
category: workflow
keywords: [agents, parallel, multi-session, collaboration]
argument-hint: "<template> <context> [--devs|--researchers|--reviewers N] [--delegate]"
metadata:
  author: agentkit
  version: "3.0.2"
---

# Agent Teams

Coordinate independent teammate sessions through a lead, shared work state,
and direct communication.

## Runtime Capability Contract

Before starting, discover the live collaboration surface for:

- team creation and cleanup;
- shared work creation, dependencies, ownership, and status;
- teammate delegation and isolation;
- direct and team-wide messages;
- waiting for updates and inspecting current state;
- plan approval when requested; and
- graceful shutdown.

Use only capabilities and parameters exposed by the live runtime. Do not cache
operation names, schemas, enablement flags, client restrictions, model lists,
limits, shortcuts, environment settings, or storage paths in this skill.

If a required capability is absent or fails, stop and report the observed
error. Do not silently substitute ordinary subagents: `/ak-team` either uses a
live team surface or aborts.

## Usage

```text
/ak-team <template> <context> [flags]
```

Templates: `research`, `cook`, `review`, `debug`.

Flags:

- `--devs N`, `--researchers N`, `--reviewers N`, `--debuggers N`: team size
- `--plan-approval` / `--no-plan-approval`: implementation plan gate
- `--delegate`: lead coordinates but performs no implementation
- `--worktree`: request isolated worktrees for implementation teammates

Choose the smallest team that creates genuinely independent workstreams.

## Stable Team Lifecycle

Use this lifecycle for every template:

1. **Decompose** the request into independent work with explicit outputs.
2. **Create the team** through the discovered live team lifecycle surface.
3. **Register work** with acceptance criteria, dependencies, ownership, and a
   durable report or plan destination.
4. **Spawn teammates** through the live delegation surface. Run independent
   scopes concurrently and isolate concurrent writers.
5. **Coordinate** through the discovered message, wait, and shared-state
   surfaces. Treat idle as waiting, not completion.
6. **Integrate** reports or changes only after prerequisite work is complete.
7. **Verify** the combined result; teammate completion messages are not proof.
8. **Shut down** teammates gracefully, wait for acknowledgements or concise
   handoffs, then invoke the live cleanup capability.
9. **Close out** with the durable report and `/ak-journal` (unless the shared
   "Journal step — opt-out" applies — see kits/core/skills/ak-journal/SKILL.md).

Do not poll a copied command name or fixed client interval. Wait through the
live surface and re-inspect state after relevant messages, state changes, or a
bounded interval appropriate to the work.

## Lead Responsibilities

The lead owns decomposition, non-overlapping ownership, dependency ordering,
integration, verification, user communication, shutdown, and cleanup.

With `--delegate`, the lead does not edit files, run implementation commands,
tests, or merges. Assign those actions to teammates and retain only
coordination, approval, synthesis, and reporting.

## Teammate Context Contract

Every teammate receives only the context needed for its scope:

- work context root;
- reports and plans locations;
- branch or worktree identity;
- active plan and accepted requirements;
- assigned files or read-only scope;
- dependencies and acceptance criteria;
- repository instructions and commit convention; and
- instruction to read `references/team-coordination-rules.md`.

Resolve these values from the current workspace and live AgentKit context. Do
not copy environment-variable snapshots into teammate prompts.

## Workflow template

Read the selected research, cook, review or debug section in `references/workflow-templates.md`. Relay concise findings, evidence paths and decisions rather than full histories.

## Plan Approval

When approval is requested:

1. Keep the teammate read-only while it plans.
2. Require scope, ownership, validation, risks, and rollback notes.
3. Approve or reject through the live approval surface.
4. On rejection, return concrete feedback and wait for a revision.
5. Allow writes only after approval is confirmed.

## Worktree Isolation

Use separate worktrees or the live runtime's equivalent for concurrent code
changes. Isolation does not replace ownership: each teammate still owns a
distinct file set. Discover branch and worktree details from live delegation
results, integrate sequentially, verify the combined tree, then clean up through
the repository's normal workflow.

## Error Recovery

1. Inspect live shared work and teammate state.
2. Message the owner with specific corrective guidance.
3. If work remains stalled, preserve a handoff, shut down that teammate, and
   assign the same bounded scope to a replacement.
4. Advance dependent work only after prerequisites are actually complete.
5. If shutdown or cleanup fails, report the live error and follow current
   runtime guidance. Never delete guessed state directories.

## Agent Teams vs Ordinary Subagents

| Scenario | Prefer |
|----------|--------|
| Focused test, lint, or single review | Ordinary subagent |
| Sequential plan → code → test chain | Ordinary subagents |
| Three or more independent workstreams | Agent Team |
| Competing hypotheses that need debate | Agent Team |
| Cross-layer work with clean ownership | Agent Team |
| Tight runtime budget | Ordinary subagents |

## Resource and Memory Policy

Every teammate owns a separate context and increases runtime cost. Inspect live
limits and use the smallest useful team. Use persistent teammate memory only
when the live runtime exposes it and project policy permits it. Treat memory
storage and lifecycle as runtime-owned. When evaluating team overhead, compare
startup, communication, retries and successful-task cost with an inline baseline
on the same workload; do not claim savings from team size alone. Track processes
started by each teammate and stop only those owned by this team during cleanup.

## References

- `references/team-coordination-rules.md`: teammate behavior and ownership
- `references/agent-teams-controls-and-modes.md`: stable control semantics
- `references/agent-teams-examples-and-best-practices.md`: portable examples
- `references/agent-teams-official-docs.md`: stable operating model and live-source boundary
