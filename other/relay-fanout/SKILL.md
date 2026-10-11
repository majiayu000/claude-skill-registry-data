---
name: relay-fanout
description: Run a fan-out relay pattern for independent subtasks. Use when the same kind of work can be split across files, components, services, or targets with minimal coordination.
argument-hint: "[task]"
disable-model-invocation: true
---

Run a relay fan-out for this task:

$ARGUMENTS

## How spawning works

Workers are spawned with Claude Code's built-in **Agent tool**. The relay is only used for communication between agents.

- Use `subagent_type: "relay-worker"`. Only `relay-worker` subagents get the Agent Relay MCP server, the inbox-polling hooks, and the worker protocol. Other subagent types (`researcher`, `general-purpose`, …) cannot talk over the relay.
- Run all workers in **background mode** (`run_in_background: true`) so they work concurrently.
- Workers inherit the workspace automatically — the relay MCP server resolves the workspace pinned to this project. **Do not put the workspace key in a worker prompt.** It is an administrative credential, and copying it into N prompts puts it in N transcripts. If a worker reports no workspace, fix the pin (step 2) rather than pasting the key.
- **One relay team per checkout.** The pin is per-project and last-writer-wins, so two leads running teams from the same directory will fight over it and a worker can register into the other lead's workspace. Run concurrent teams from separate checkouts or git worktrees. The ACK gate below is what catches this: a worker that landed in the wrong workspace finds no assignment and cannot ACK.
- The `SubagentStart` hook injects the relay bootstrap (register, check inbox, ACK, DONE) into every worker.
- Use the relay MCP tools (`send_dm`, `check_inbox`) to monitor progress.
- Do not add setup scripts or dependencies. Use the plugin's existing hooks, MCP tools, and `relay-worker` agent definition.

## Protocol

1. Pick a stable coordinator name — `relay-lead`. Pass `as: "relay-lead"` on **every** relay tool call you make, so your messages, inbox reads, and reactions stay attributed to the lead.
2. **Set up the workspace.** Call `register_agent` with `relay-lead`. If it fails with "Workspace key not configured", call `create_workspace`, then `register_agent` again. Both `create_workspace` and `set_workspace_key` pin the workspace to this project, which is how workers pick it up.
3. **Give the user a link to follow along.** Call `get_observer_url` and print the URL it returns — or run `agent-relay observer` if your session does not expose that tool. Either way the link is backed by a read-only token that expires, so it is safe to share. Never build an observer URL from the workspace key, and never print the key.
4. Confirm the work is genuinely parallelizable. Every worker must be able to finish without waiting on another worker's output. If that is not true, use the pipeline pattern instead.
5. Pick the worker count from the task shape. Prefer 2–8, and stay low enough that you can still track every ACK and DONE.
6. Partition the work into independent units — each with its own files, target, or scope boundary, and no shared intermediate state.
7. Spawn one worker per unit with the Agent tool:
   ```text
   Agent(
     subagent_type: "relay-worker",
     run_in_background: true,
     prompt: "You are relay-worker-N. Your lead is relay-lead.
              CRITICAL: pass as: \"relay-worker-N\" on every relay tool call, or your messages
              can be attributed to another agent.
              Your unit: [specific target/scope].
              Files: [list of files/directories].
              Deliver: [concrete output].
              When done, DM your lead a DONE message with the evidence for your scope.
              Do not call remove_agent on yourself — the lead releases you once the work
              is accepted, so it can send you review findings to fix."
   )
   ```
8. Wait for an ACK from every worker with `check_inbox(as: "relay-lead")`. A missing ACK means that worker is not working — re-DM it.
9. Keep a live worker table in your notes: name, unit, ACK, blocked, DONE.
10. Let workers run independently. Only DM them for blockers, missing ACKs, or a global decision that changes every unit.
11. Collect every DONE, verify the outputs yourself, and merge the summary. Call out units that finished partially or hit blockers.

## Rules

- Do not use this pattern when stage N depends on stage N-1. That is a pipeline.
- Do not give two workers the same files unless duplicate review is the point.
- Keep the task wording uniform across units so the outputs are easy to compare and merge.
- Workers cannot spawn their own subagents — only the lead spawns.
