---
name: relay-pipeline
description: Run a sequential relay pipeline where each stage feeds the next. Use when worker N plus 1 depends on worker N's output or decisions.
argument-hint: "[task]"
disable-model-invocation: true
---

Run a relay pipeline for this task:

$ARGUMENTS

## How spawning works

Workers are spawned with Claude Code's built-in **Agent tool**. The relay is only used for communication between agents.

- Use `subagent_type: "relay-worker"`. Only `relay-worker` subagents get the Agent Relay MCP server, the inbox-polling hooks, and the worker protocol. Other subagent types (`researcher`, `general-purpose`, …) cannot talk over the relay.
- Run pipeline stages in **foreground mode** (the default) so each stage finishes before the next starts.
- Workers inherit the workspace automatically — the relay MCP server resolves the workspace pinned to this project. **Do not put the workspace key in a worker prompt.** It is an administrative credential, and copying it into N prompts puts it in N transcripts. If a worker reports no workspace, fix the pin (step 2) rather than pasting the key.
- **One relay team per checkout.** The pin is per-project and last-writer-wins, so two leads running teams from the same directory will fight over it and a worker can register into the other lead's workspace. Run concurrent teams from separate checkouts or git worktrees. The ACK gate below is what catches this: a worker that landed in the wrong workspace finds no assignment and cannot ACK.
- The `SubagentStart` hook injects the relay bootstrap (register, check inbox, ACK, DONE) into every worker.
- Use the relay MCP tools (`send_dm`, `check_inbox`) to receive each stage's handoff.
- Do not add setup scripts or dependencies. Use the plugin's existing hooks, MCP tools, and `relay-worker` agent definition.

## Protocol

1. Pick a stable coordinator name — `relay-lead`. Pass `as: "relay-lead"` on **every** relay tool call you make, so your messages, inbox reads, and reactions stay attributed to the lead.
2. **Set up the workspace.** Call `register_agent` with `relay-lead`. If it fails with "Workspace key not configured", call `create_workspace`, then `register_agent` again. Both `create_workspace` and `set_workspace_key` pin the workspace to this project, which is how workers pick it up.
3. **Give the user a link to follow along.** Call `get_observer_url` and print the URL it returns — or run `agent-relay observer` if your session does not expose that tool. Either way the link is backed by a read-only token that expires, so it is safe to share. Never build an observer URL from the workspace key, and never print the key.
4. Break the task into ordered stages. Every stage needs a concrete handoff artifact for the next one: a summary, a decision, a file path, a diff, or a verified output.
5. Keep the stage count low and explicit — prefer 2–5 with distinct responsibilities.
6. Start stage 1. Spawn its worker with the Agent tool in foreground mode:
   ```text
   Agent(
     subagent_type: "relay-worker",
     prompt: "You are relay-stage-1. Your lead is relay-lead.
              CRITICAL: pass as: \"relay-stage-1\" on every relay tool call, or your messages
              can be attributed to another agent.
              Your task: [stage 1 scope].
              Files: [relevant files].
              When done, DM your lead a DONE message containing: [handoff artifact description],
              then end your turn so the lead can continue.
              Do not call remove_agent on yourself — the lead releases you."
   )
   ```
7. Wait for stage 1's DONE with `check_inbox(as: "relay-lead")`. Never start downstream work on an assumption about what the stage produced.
8. For each later stage, spawn a worker carrying the original task context, the upstream DONE summary and handoff artifact, and any files, decisions, or constraints the earlier stages produced:
   ```text
   Agent(
     subagent_type: "relay-worker",
     prompt: "You are relay-stage-2. Your lead is relay-lead.
              CRITICAL: pass as: \"relay-stage-2\" on every relay tool call.
              Previous stage completed: [DONE summary from stage 1].
              Your task: [stage 2 scope, using stage 1's output].
              Files: [relevant files].
              When done, DM your lead a DONE message containing: [this stage's handoff artifact —
              or, if this is the final stage, the deliverable plus the evidence that proves it works],
              then end your turn so the lead can continue.
              Do not call remove_agent on yourself — the lead releases you."
   )
   ```
9. Keep a live stage table in your notes: stage, scope, ACK, blocked, DONE, handoff artifact.
10. After each stage, check the handoff is sufficient. If it is ambiguous, ask the user before starting the next stage.
11. When the last stage finishes, synthesize the end-to-end result and show where each handoff happened.

## Rules

- Use a pipeline only for genuine dependencies. If the stages can run independently, switch to fan-out.
- Stages run in the foreground, so a stage worker **must end its turn** after sending DONE. Telling it to stay idle deadlocks the run: the blocking Agent call never returns, so the lead can never read the DONE or spawn the next stage. (Team and fan-out workers are backgrounded and do stay idle — that instruction belongs there, not here.)
- Releasing a relay identity (`remove_agent`) is separate from ending a turn. Workers never do the former; the lead does it once the whole pipeline is accepted.
- Handoffs must be explicit. A downstream worker should never have to guess what mattered upstream.
- If a stage fails or is blocked, stop the pipeline, resolve the blocker, and resume from that stage.
- Workers cannot spawn their own subagents — only the lead spawns.
