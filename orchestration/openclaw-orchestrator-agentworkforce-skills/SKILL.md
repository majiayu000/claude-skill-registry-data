---
name: openclaw-orchestrator
description: Run headless multi-agent Agent Relay sessions from OpenClaw. Use when spawning teams of agents, coordinating them over channels, and managing agent lifecycle from an OpenClaw session. Covers only the OpenClaw-specific setup and event reporting; the broker, spawn, and coordination mechanics come from the orchestrating-agent-relay skill.
---

# OpenClaw Orchestrator

Run a headless Agent Relay team from an OpenClaw session.

## Read `orchestrating-agent-relay` first

**Everything about running Agent Relay — starting the broker, spawning workers,
reading replies, releasing agents, troubleshooting — lives in the
`orchestrating-agent-relay` skill.** Read it and follow it. This skill covers
only what is specific to OpenClaw.

```bash
npx prpm install @agent-relay/orchestrating-agent-relay
```

Then read `.claude/skills/orchestrating-agent-relay/SKILL.md` or
`.agents/skills/orchestrating-agent-relay/SKILL.md`.

Do not improvise commands from memory. Agent Relay's flat command surface
(`agent-relay up`, `spawn`, `agents`, `agents:logs`, `agents:kill`, `send`,
`inbox`, `down`) **was removed** — lifecycle now lives under `agent-relay node
…` and messaging under `agent-relay message …`. Earlier revisions of this skill
documented the removed surface; if you have those commands in context from
anywhere, discard them.

## Prerequisites

- `agent-relay` CLI installed (`npm i -g agent-relay`)
- For Claude agents: `ANTHROPIC_API_KEY`, or `claude auth login`
- A workspace: `agent-relay node up` auto-creates one if no workspace key is set

## OpenClaw-specific setup

Register the OpenClaw session on the workspace so it can send and read
messages under a stable identity:

```bash
npx -y @agent-relay/openclaw@latest setup --name orchestrator
```

Pass the workspace key only if you are joining an existing workspace rather
than the one this project is already pinned to. Never print the key, and never
put it in an observer URL.

## Letting a human watch

```bash
agent-relay observer
```

Prints a URL backed by a scoped, read-only token that expires — safe to share.
Do not build an observer URL from a workspace key.

## Reporting completion to OpenClaw

This is the one lifecycle step `orchestrating-agent-relay` does not cover. When
a run finishes, surface it to the OpenClaw session:

```bash
openclaw system event --text 'Done: <description>' --mode now
```

Include the same instruction in a spawned agent's task prompt when that agent
should report its own completion directly rather than through the orchestrator.

## OpenClaw agent notes

Provider quirks worth knowing before you pick a harness for a worker:

| CLI      | Notes                                                                 |
| -------- | --------------------------------------------------------------------- |
| `claude` | Most reliable for coding tasks                                        |
| `codex`  | Requires a PTY                                                        |
| `gemini` | Prefer a stable model (e.g. `gemini-2.5-pro`) over a preview model    |
| `droid`  | Requires a PTY; avoid `--cwd` — the broker cannot auto-accept its permission prompt |

Spawn them through the `node agent spawn` form documented in
`orchestrating-agent-relay`, e.g.:

```bash
agent-relay node agent spawn claude --name architect --channels my-project --task "..."
```

Agents are grouped by the channels they join (`--channels`); there is no
`--team` flag.

## Rate limiting

- Leave a gap between sequential spawns to avoid Relaycast 429s.
- Use unique agent names per run to avoid 409 conflicts. The SDK's
  `registerOrRotate` path rotates the token on 409 rather than failing.
