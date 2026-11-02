---
name: agent-bridge
description: |-
  Use when an agent in one harness must create, observe, or steer one or more agents in another harness through a tmux session the user can watch. Triggers: "use an agent in another harness", "bridge to <agent>", "run <agent> in tmux", "use a different harness", "check on the external agent". Not for subagents or delegation inside the current harness (use `subagent-patterns`).
---

# Agent Bridge

Create and work with agents in another harness through separate windows of a tmux session named `agents`.
Use `scripts/agent_bridge.py` to control the target agents while the user watches them.

Supported adapters are `codex`, `claude`, `copilot`, `gemini`, `cursor` (the `cursor-agent` binary), and `pi`.
Each spawn can select a different adapter with `--agent`.

## When to Use

- The current harness must create, observe, or steer an agent in another harness.
- The target agent must run under its own harness's sandbox and approval controls.
- The user wants to watch or steer the target agent in its native TUI.
- The target agent must keep its session across several of your turns.
- The user wants to compare agents from different harnesses on the same task.

## When Not to Use

- The work belongs in this harness.
  Use `subagent-patterns` for internal delegation.
- The target is a normal subprocess, not an agent harness.
  Use the harness's command tool instead.
- The user did not authorize another agent harness.
  Propose the bridge and wait because it starts another harness and increases token use.

## Invocation Notice

- Tell the user when this skill is running: `agent-bridge`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Overview

The user starts and watches the tmux session.
The tmux server forks each agent from the user's shell, so the agent runs under the user's own settings and its own CLI's approval controls.
That is the reason to use tmux here: starting an agent CLI from one of your tool calls instead nests it inside your sandbox, where it runs with your permissions rather than the user's.

Only use this capability for work that the user authorized.

## Workflow

### 1. Prepare the session

Ask the user to run this command in their terminal, and wait for them:

```bash
tmux new-session -s agents
```

Confirm that the session exists:

```bash
scripts/agent_bridge.py list
```

If the command reports `Operation not permitted` on the socket, read `references/tmux-and-sandbox.md` before you suggest a change.

The tmux server continues after the user detaches or closes their terminal.
They can return with `tmux attach -t agents`.
Run `scripts/agent_bridge.py attach` to print that command rather than typing it from memory; on a non-default socket the command differs.

### 2. Spawn each track

Give each track one name that describes its work, such as `api-flaky-tests`.
Window names share one namespace, so avoid generic names such as `tests`, `docs`, `agent1`, or `w2`.

Spawn an agent with its initial prompt:

```bash
scripts/agent_bridge.py spawn api --cd ~/src/api --prompt "Read the failing tests in tests/ and report what breaks. Do not fix anything yet."
scripts/agent_bridge.py spawn docs --agent claude --cd ~/src/api --prompt "Draft release notes from the last 20 commits."
```

Prefer `--prompt` because `send` can lose text before the TUI composer exists.
`--prompt` works for `codex` and `claude`.
For another adapter, spawn without a prompt, run `scripts/agent_bridge.py wait <name>`, and then use `scripts/agent_bridge.py send <name> "<message>"`.
Use `scripts/agent_bridge.py send <name> --file <path>` for a long brief.

When the target writes a report or findings file, name its path in the brief, inside the target's working directory.
The target has its own sandbox and `$TMPDIR`, loads its own harness's instructions file, and may run a different installed copy of a skill, so its default output location can be one you cannot find.

`--cd` sets the tmux window's working directory for every adapter.
Pass extra CLI flags after `--`, for example `spawn api -- --search`.

On the first spawn in a session, relay the `posture:` line to the user.
`OVERRIDDEN` means an argument such as `--profile` selected configuration other than the CLI's default.

Each spawn is detached and prints a `watch:` line with the new window's index.
Relay that line so the user can supervise the agent.

| To do this              | The user presses         |
| ----------------------- | ------------------------ |
| Go to a window by index | `Ctrl-b <n>`             |
| Next or previous window | `Ctrl-b n` or `Ctrl-b p` |
| Pick from a list        | `Ctrl-b w`               |
| Return to the last one  | `Ctrl-b l`               |

### 3. Monitor and steer

Run `scripts/agent_bridge.py wait <name>` to wait until the screen stops changing.
Poll a slow agent on a later turn instead of holding a tool call open.

Always run `scripts/agent_bridge.py peek <name>` after `wait`.
An `idle` result can mean that the agent finished its turn or stopped at an approval prompt.
Use `scripts/agent_bridge.py peek <name> -n 40` for the screen tail or `scripts/agent_bridge.py peek <name> --history 200` for scrollback.

Use `scripts/agent_bridge.py send <name> "<message>"` to steer an agent.
Use `scripts/agent_bridge.py keys <name> <key>` only for raw keys such as `Escape` or `C-c`.

The script refuses `send`, `keys`, and named `kill` for another project's agents.
`peek`, `wait`, and `list` read any window.

When several projects share a session, `list` marks another project's agents with `[name]` and prints your owner at the bottom.
Use `--session agents-<project>` when the user wants a separate session for each project.
Read `references/tmux-and-sandbox.md` for the ownership model and socket details.

Add `--json` to any command when you need machine-readable output.

### 4. Finish

Kill each agent when its work is done.
A running agent continues to use tokens and can hold repository locks.

Use `scripts/agent_bridge.py kill <name>` for one agent or `scripts/agent_bridge.py kill --all` for every agent that you own.
`kill --all` leaves the user's windows and other projects' agents intact.

Dead agents leave readable windows, so use `peek` to inspect a crashed agent.

## Safety rules

1. Never start the tmux server yourself, and never pass `--create-session`.
   Agents forked from a server you started inherit your sandbox, and some sandboxes cannot create a window at all.
2. Never attach from a tool call.
   `tmux attach` blocks until the client detaches.
3. Never pass a flag that disables the target CLI's approval gate.
   The script's refusal list comes from each CLI's documentation, not from testing, so an unknown gate-removing flag still reaches the CLI.
4. The user answers every approval prompt.
   Describe what the agent is asking for and let them answer in their own window.
   Use `keys <name> y` only when they tell you to answer for them.
5. Only send input to agents you spawned.
   `--any-owner` crosses that line and needs the user to ask for it.
6. Never run `kill-session` or `kill-server`.
   Both destroy the user's terminal state.
7. Never edit the user's sandbox settings.
   Suggest the change and let them apply it.
8. Report what `peek` shows, and check an agent's completion claim against the work before you repeat it.

## References

- `references/tmux-and-sandbox.md` — process inheritance, session ownership, sockets, platform-specific sandbox settings, TUI input, idleness detection, and troubleshooting.
- `references/adapters.md` — adapter implementation and verification.
  You do not need it to work with a target agent.
- `scripts/agent_bridge.py` — the bridge controller.
  Run `--help` for every command and flag.
