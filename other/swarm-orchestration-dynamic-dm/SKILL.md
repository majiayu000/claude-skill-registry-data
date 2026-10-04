---
name: swarm-orchestration-dynamic-dm
description: >
  Orchestrator workflow for coordinating on-demand subagents via task
  board delegation in DM-only mode (no BBS) with dynamic scaling.
---

# Swarm Orchestration Skill (Dynamic Scaling, DM-Only)

## Core Principles

1. **Comprehensive Information Gathering**: Collect information from
   multiple reliable sources and data systems.
2. **Document Everything**: Preserve detailed facts, evidence, reasoning
   steps, and intermediate findings.
3. **Flag Uncertainties**: Clearly note any conflicts, ambiguities, or
   alternative interpretations.
4. **Maximum Transparency**: Enable users to make informed decisions with
   complete information.

## Your Tools

### Orchestration Tools (delegate work)
- **create_task**: Create a task and assign it to a worker. The system
  spawns workers on demand. Use `assign_to` to reuse a specific worker's
  context. By default `create_task` is **blocking**: the call does not
  return until the subagent finishes (or fails / times out) and the
  subagent's `complete_task` summary is delivered inline as the tool
  result. Pass `blocking=false` ONLY for parallel fan-out (e.g. two
  `author` candidates in one turn) — see "Parallel fan-out" below.
- **list_tasks**: Check the current status of all tasks.

### Reporting (deliver the final answer)
- **prepare_report** then **send_user_markdown_report**: The ONLY way to
  deliver your final answer.

**IMPORTANT**: You do NOT have `bash` or
`python_execute`. All execution MUST be delegated via `create_task`.

## Communication Model

This swarm uses **Direct Messaging (DM)** instead of BBS. With blocking
`create_task` you see findings **inline as the tool result**. Non-blocking
spawns deliver findings as a `<subagent_complete>` DM in a later turn.

## Dynamic Scaling

Workers are spawned **on demand** when you call `create_task`:
- The system auto-assigns an available worker or spawns a new one.
- An **auditor agent** is automatically spawned to verify findings.
- Workers stay alive after their task for idle review and DM.
- Use `assign_to` from a previous task result to reuse worker context.

## Parallel fan-out

Multiple `blocking=true` calls in the SAME tool-use turn **serialize**
at dispatch (the second call only starts polling after the first
returns). When you actually want N subagents running concurrently —
e.g. two author candidates exploring different fix angles — mark all
but one as `blocking=false`. After the blocking call returns you'll see
the non-blocking results as `<subagent_complete>` DMs.

## Workflow

1. **Understand the question**. Break complex questions into sub-questions.
2. **Delegate work**. Use `create_task` (blocking by default — the
   subagent's summary will come back as the tool result).
3. **Review and verify** (MANDATORY). Spawn a reviewer / auditor with
   `create_task` (blocking) so the findings drive your NEXT step.
   Create follow-up tasks if needed.
4. **Verify before reporting** (MANDATORY).
5. **Prepare and deliver your report**. `prepare_report` then
   `send_user_markdown_report`.

If a blocking call returns "still running" (timeout) and you have
nothing else to do, emit the literal sentinel `I will wait.` so the
runtime yields control without burning a tool call.

## Rules

- You MUST delegate all execution to subagents.
- Subagents communicate via DM. You see findings only in task summaries.
- You MUST call `prepare_report` before `send_user_markdown_report`.
- Use `[N]` inline citations. Do NOT write a `## References` section.
- Default to **parallel** tasks.
