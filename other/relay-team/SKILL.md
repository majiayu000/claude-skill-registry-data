---
name: relay-team
description: Spawn and coordinate a relay team for a multi-part task. Use when work should be split across several Claude workers with explicit ACK and DONE signaling.
argument-hint: "[task]"
disable-model-invocation: true
---

Build and run a coordinated relay team for this task:

$ARGUMENTS

## How spawning works

Workers are spawned with Claude Code's built-in **Agent tool**. The relay is only used for communication between agents.

- Use `subagent_type: "relay-worker"`. Only `relay-worker` subagents get the Agent Relay MCP server, the inbox-polling hooks, and the worker protocol. Other subagent types (`researcher`, `general-purpose`, …) cannot talk over the relay.
- Run workers in **background mode** (`run_in_background: true`) so they work concurrently.
- Workers inherit the workspace automatically — the relay MCP server resolves the workspace pinned to this project. **Do not put the workspace key in a worker prompt.** It is an administrative credential, and copying it into N prompts puts it in N transcripts. If a worker reports no workspace, fix the pin (step 2) rather than pasting the key.
- **One relay team per checkout.** The pin is per-project and last-writer-wins, so two leads running teams from the same directory will fight over it and a worker can register into the other lead's workspace. Run concurrent teams from separate checkouts or git worktrees. The ACK gate below is what catches this: a worker that landed in the wrong workspace finds no assignment and cannot ACK.
- The `SubagentStart` hook injects the relay bootstrap (register, check inbox, ACK, DONE) into every worker.
- Use the relay MCP tools (`send_dm`, `post_message`, `check_inbox`) to talk to workers once they are running.
- Do not add setup scripts or dependencies. Use the plugin's existing hooks, MCP tools, and `relay-worker` agent definition.

## Protocol

1. Pick a stable coordinator name — `relay-lead`. Pass `as: "relay-lead"` on **every** relay tool call you make, so your messages, inbox reads, and reactions stay attributed to the lead.
2. **Set up the workspace.** Call `register_agent` with `relay-lead`. If it fails with "Workspace key not configured", call `create_workspace`, then `register_agent` again. Both `create_workspace` and `set_workspace_key` pin the workspace to this project, which is how workers pick it up.
3. **Give the user a link to follow along.** Call `get_observer_url` and print the URL it returns — or run `agent-relay observer` if your session does not expose that tool. Either way the link is backed by a read-only token that expires, so it is safe to share. Never build an observer URL from the workspace key, and never print the key.
4. Read the task, inspect the relevant code, and decide whether parallel work is justified. Prefer 1 worker for tightly coupled work, 2–5 for genuinely separable work.
5. Break the task into non-overlapping scopes. Each worker needs a concrete deliverable, the relevant files, and an explicit success condition.
6. Spawn each worker with the Agent tool:
   ```text
   Agent(
     subagent_type: "relay-worker",
     run_in_background: true,
     prompt: "You are relay-worker-1. Your lead is relay-lead.
              CRITICAL: pass as: \"relay-worker-1\" on every relay tool call, or your messages
              can be attributed to another agent.
              Your task: [specific scope and deliverables].
              Files: [list of files/directories].
              Success condition: [what done looks like].
              When done, DM your lead a DONE message with the evidence for your scope.
              Do not call remove_agent on yourself — the lead releases you once the work
              is accepted, so it can send you review findings to fix."
   )
   ```
7. After spawning, DM each worker any extra context it needs.
8. Watch for ACKs with `check_inbox(as: "relay-lead")`. A worker is not working until it ACKs — expect a cold-start delay, and re-DM if an ACK never arrives.
9. Keep a live worker table in your notes: name, scope, ACK, blocked, DONE.
10. Coordinate dependencies explicitly. Send each worker the minimum context it needs and keep workers independent where you can.
11. Collect every DONE, verify the results yourself, and synthesize the final answer — what each worker finished, plus remaining gaps and risks.

## Rules

- Prefer fewer well-scoped workers over many vague ones.
- Do not let workers infer coordination details. Send explicit follow-ups when assumptions change.
- If the work turns out to be independent across targets, switch to fan-out instead of keeping a coordinator busy.
- If it turns out to be sequential, switch to pipeline instead of forcing parallelism.
- Workers cannot spawn their own subagents — only the lead spawns.
