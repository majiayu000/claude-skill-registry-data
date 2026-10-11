---
name: connecting-agents-across-machines
description: "Use when agents running on two or more machines (laptops, desktops, Mac minis, servers) need to talk to each other or when you want to spawn an agent onto another machine with Agent Relay. Covers putting every machine on one shared workspace, starting a node per machine, messaging across machines, targeted spawns, and verifying the link agent-to-agent. No Relay Cloud sandbox required. Verified on agent-relay 12.4.1."
---

# Connecting Agents Across Machines

Agent Relay coordinates agents through a **workspace**. Agents on different
machines that share the same workspace can use the same DMs, channels, threads
and inbox, no matter which machine they run on. Each machine runs its own
**node** (a local broker). The node connects to the workspace and hosts the
agents on that machine.

```
 Machine A                          Machine B
 ┌──────────────────────┐           ┌──────────────────────┐
 │ agent-relay node up  │           │ agent-relay node up  │
 │  ├─ Lead (claude)    │           │  ├─ Worker (codex)   │
 │  └─ Reviewer         │           │  └─ Tester           │
 └──────────┬───────────┘           └──────────┬───────────┘
            └──────── same workspace key ──────┘
                 (messages, channels, spawns)
```

You don't need a Relay Cloud sandbox for this. Your own machines are the
nodes.

Prefer setting this up with the Agent Relay agent at
<https://arelay.to/agent-relay>, which checks your current state and confirms
each step. Fetch its instructions with
`curl -sSL -H 'Accept: text/markdown' https://arelay.to/agent-relay`.

> Verified end to end on `agent-relay` 12.4.1 between a MacBook and a Mac
> mini: a Codex agent on the mini sent a DM to a Claude agent on the laptop,
> and the reply came back. Everything below is the exact sequence that
> worked.

Run every command from the **same project directory** on each machine.
`workspace create` / `join` pin the workspace to that directory
(`.agentworkforce/relay/workspace-key.json`), and `node up` reads that pin.

## Setup (once)

### 0. Check what each machine already has

Run these first on every machine. If `agent-relay --version` fails, install the
CLI first with `npm install -g agent-relay`. The checks only read state:

```bash
agent-relay cloud whoami       # signed in, and as whom
agent-relay workspace active   # the active Cloud workspace (keys stay masked)
agent-relay cloud workspaces   # every workspace this login can use, with ids
agent-relay status             # workspace, cloud login and local broker
agent-relay workspace list     # workspaces stored on this machine
```

If the human already has a shared workspace, skip step 1 and join it on each
machine that is not on it yet (step 2). The human gets that workspace's key
from its owner over a secure channel such as a password manager, never through
the agent. Create a workspace only when the human
explicitly wants a new one.

### The workspace key never enters an agent session

Joining a machine to a workspace needs its key, and agent-relay 13.x has no
keyless join: Cloud sign-in and `cloud enroll` do not hand a workspace key to
the local broker. So the **human** moves the key, entirely outside any agent
transcript:

- The agent never runs `--reveal-secrets` (`workspace create`, `workspace key`,
  `workspace active --json`) and never runs `workspace join` with a real key.
- The agent never asks for the key in chat and never reads it from a file.
  If someone pastes a key into the conversation anyway, tell the human to treat
  it as leaked. A fresh workspace alone does not cut off access: the old key
  stays valid, and agent-relay 13.x has no command to revoke it. Stop using the
  old workspace and ask its owner to retire it or rotate its key.
- The human reveals the key and enters it only in their own terminal, one no
  agent or recorder is watching, and moves it between machines over a secure
  channel such as a password manager.

### 1. Create the workspace on one machine

On **machine A** (the agent may run this; the key stays masked in the output
and is stored on this machine):

```bash
npm install -g agent-relay
agent-relay workspace create my-team
```

Then ask the human to copy the key **in their own terminal** on machine A, not
through the agent:

```bash
# Human only, in a terminal no agent is reading:
agent-relay workspace key my-team --reveal-secrets
```

They save it to a password manager (or another encrypted channel) for machine
B. Never put it in a chat, ticket, repo, or a message to an agent.

### 2. Join the same workspace on every other machine

On **machine B**, and on any further machines, the agent may install the CLI
(`npm install -g agent-relay`). The **human** then runs the join in their own
terminal, from the same project directory, pasting the key at the hidden
prompt:

> **Process-list limitation:** Agent Relay CLI 13.x accepts the workspace key
> only as a positional argument. The hidden prompt below keeps it out of shell
> history and the transcript, but the spawned CLI process still exposes the key
> briefly to local process-list readers. Explain that limitation before the
> human proceeds. Use this route only on a trusted single-user machine with the
> human's explicit approval; otherwise stop. Do not run it from an agent tool.

```bash
# Human only, in a terminal no agent is reading:
# Works in bash and zsh (the macOS default). The subshell keeps the key out of
# your shell afterwards; the trap restores echo even on Ctrl-C; nothing runs if
# echo cannot be turned off.
(
  trap 'stty echo; printf "\n"' EXIT
  trap 'exit 130' INT TERM HUP
  stty -echo || exit 1
  printf 'Workspace key: '
  IFS= read -r RELAY_KEY || exit 1
  test -n "$RELAY_KEY" && agent-relay workspace join my-team "$RELAY_KEY"
)
```

The agent confirms the result with read-only commands that never print the
key: `agent-relay workspace list` should show `my-team` as active, and
`agent-relay workspace active` its workspace IDs.

> **Do not skip this step.** If `node up` runs on a machine with no workspace
> configured, it can silently create a **new** workspace. Both nodes then look
> healthy but can't see each other. Run `join` first on every machine after
> the first.

### 3. Start a node on each machine

Give each machine a distinct, stable name. Use agent-relay 11.3.1 or later:
11.3.0 and earlier print the workspace key from `node up` and `node status`.

```bash
# machine A
agent-relay node up --background --broker-name laptop-a
# machine B
agent-relay node up --background --broker-name mini-b
```

Every AI CLI you want to run on a machine (`claude`, `codex`, …) must be
installed **and logged in on that machine**. Relay starts the CLI but can't
log in for it. An expired login shows up as an agent that starts and then
does nothing.

Stop a node with `agent-relay node down`, not by killing the process. A
killed node can leave its name reserved.

## Verify the link

From either machine:

```bash
agent-relay workspace list        # both machines should show the same active workspace
agent-relay fleet nodes           # both node names listed, status "online"
agent-relay fleet agent list      # agents across every reachable node
```

To prove messaging works end to end, put one agent on each machine and have
the remote one write to the local one. Run both commands from machine A:

```bash
agent-relay fleet spawn claude --node laptop-a --name Receiver --no-confirm \
  --task "Wait for a DM from Sender. Write its exact text to ./received.txt, reply 'got it', and stop."

agent-relay fleet spawn codex --node mini-b --name Sender --no-confirm \
  --task "Run 'hostname', then DM Receiver exactly: hello from <hostname output>. Wait for the reply and stop."
```

Within a couple of minutes, `received.txt` on machine A should contain
`hello from <machine B's hostname>`. Clean up:

```bash
agent-relay fleet release Sender
agent-relay fleet release Receiver
```

> **Confirm a spawn by checking the target machine, not by the CLI's exit
> code.** A targeted spawn can print `spawn_failed` or `spawn_unconfirmed`
> even though the agent launched fine. Before retrying, run
> `agent-relay node agent list` **on the target machine**. If the agent is
> there with `"ready": true`, it's running. A blind retry can start a
> duplicate. `--no-confirm` skips the wait and returns once the node accepts
> the spawn.

## Everyday use

**Spawn onto a specific machine**, for example when that machine has the repo,
GPU or credentials the job needs:

```bash
agent-relay fleet spawn codex --node mini-b --name Builder \
  --task "Run the test suite in the current directory and report failures to Lead" \
  --cwd /Users/me/code/app
```

`--cwd` is a path **on the target machine**. Write it as an absolute path.
Don't use `~`, because your local shell expands it to *your* home directory
before the command is sent. Each machine uses its own
checkout, and nothing is copied between machines.

**Let Relay pick a machine**: use `--auto-place` instead of `--node`.

**Release an agent**: `agent-relay fleet release <name>`.

**From inside an agent** (Relay MCP tools): agents message each other by name
with `send_dm` / `post_message` whichever machine they run on.
`spawn` takes a `target_node` to choose the machine.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Nodes are up but can't see each other's agents | The machines are on different workspaces, often because `node up` ran before `workspace join` | Run `agent-relay workspace list` on both machines. Have the human run the step 2 join on the odd machine out, in their own terminal, then `node down` and `node up` |
| `fleet nodes` doesn't list a machine | The node is on another workspace, or isn't running | Check `workspace list` and `node status` on that machine. `fleet nodes --all` also shows hidden or offline records |
| Spawn reports `spawn_failed` / `spawn_unconfirmed` | The launch confirmation didn't arrive, but the agent often did start | Run `agent-relay node agent list` on the target machine before retrying |
| Agent starts but never acts or replies | Its CLI isn't logged in on that machine (e.g. `401 OAuth access token has been revoked`) | Log in to that CLI on the target machine (`claude /login`, `codex login`), or spawn a different CLI |
| `message` CLI commands say `requires agentToken` | The `message` commands act as a registered agent | Test messaging agent to agent as shown above, or use the Relay MCP tools from inside an agent |
| `Invalid API key` | The CLI is using a different active workspace than you expect | Run `agent-relay workspace switch my-team` and retry |
| Node shows online but spawns never land on it | The node advertises no spawn capability for that CLI (e.g. only `claude`, not `codex`) | Install and log in to that CLI on the target machine, then restart the node |
| Agent spawned on B can't find files | `--cwd` points to a path that exists only on A | Use a path that exists on the target machine |

## Related skills

- `orchestrating-agent-relay`: running and monitoring a team from one lead
- `using-agent-relay`: messaging, channels and inbox from inside an agent
- `multi-host-live-mount`: sharing one **file** tree (Relayfile) across machines
