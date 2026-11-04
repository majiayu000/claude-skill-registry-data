---
name: cursorctl
description: >-
  Use the `cursorctl` CLI (Cursor SDK Bridge) to spawn, send, detach, follow up,
  inspect, and collect Cursor cloud or local agents. Trigger when delegating work
  to Cursor cloud agents (`bc-…` IDs), running a local Cursor agent, fire-and-forget
  with `--detach`, polling `run get`/`wait`/`watch`, collecting artifacts or
  conversations, managing `cursorctl auth` profiles, or troubleshooting the SDK
  Bridge. Run cursorctl via Bash. Do not call the SDK Bridge HTTP API directly.
user-invocable: true
---

# cursorctl

`cursorctl` is a Go CLI over the Cursor SDK Bridge. Use it for agent-to-agent delegation from Claude Code: start Cursor cloud agents against GitHub repos, detach, inspect runs later, send follow-ups, and collect results. It also supports local Cursor agents against this machine's filesystem.

Do not invent SDK Bridge HTTP/RPC calls. Drive everything through `cursorctl` in Bash. Keep this hub short; open a reference file only when needed.

Canonical source: [nickmisasi/cursor-utils](https://github.com/nickmisasi/cursor-utils) (`skills/cursorctl/`). This plugin is the Claude Code translation of that skill.

## Claude Code runtime

- Run every `cursorctl` invocation with Bash. Do not use Claude Code's Agent/Task tool to spawn Cursor cloud agents — those subagents are Claude processes, not SDK Bridge agents. Cursor cloud IDs start with `bc-` and exist only through `cursorctl`.
- Only create or send to agents when the user asked to delegate to Cursor or the task clearly requires a Cursor cloud/local agent. Confirm the `--repo` URL (and ref) before the first create/prompt.
- Interactive TTY prompts do not work here. If auth is missing, tell the user to run `cursorctl auth add <name> --stdin --default` themselves. Never print, log, or pass a raw API key on the argv.
- Blocking `agent prompt`, `agent send` (without `--detach`), and `run wait` can run for many minutes. Prefer `--detach` plus `run get`/`run wait`/`run watch`, or set a Bash timeout well above the expected run. `--detach` is not cancellation.
- If `command -v cursorctl` fails, stop and tell the user how to install it. Do not emulate the CLI.

## Binary and auth

```bash
command -v cursorctl
cursorctl version
```

If it is missing, install from [GitHub Releases](https://github.com/nickmisasi/cursor-utils/releases) (linux/darwin amd64/arm64; not Windows) or `go install github.com/nickmisasi/cursor-utils/cursorctl@latest`. A common local path is `~/.local/bin/cursorctl`.

Store a user API key from https://cursor.com/dashboard/api. Do not `export CURSOR_API_KEY` in shell rc files; Cursor's `agent` CLI treats that variable as higher-priority than stored login.

```bash
cursorctl auth add work --stdin --default
```

Key resolution: `--api-key` → env named by `--api-key-env` → `--profile`/`CURSORCTL_PROFILE` → stored default.

The first bridge-backed command downloads the pinned SDK Bridge (`v1.0.27`), verifies SHA-256, and caches it under `~/.cache/cursorctl/sdk-bridge/`. Pre-fetch with `cursorctl bridge install`.

Use explicit cloud flags when delegating. `--repo URL[@ref]` selects cloud; without cloud-only flags the CLI builds local options and uses `--cwd` (default: `--workspace`).

## Start here

```bash
cursorctl agent prompt \
  --repo https://github.com/acme/widgets@main \
  --auto-create-pr \
  --skip-reviewer-request \
  --quiet \
  "Fix the failing tests, verify the fix, and open a PR."
```

## The three delegation patterns

### 1. One-shot: `agent prompt`

Create an agent, send one message, consume its run, then close the agent:

```bash
cursorctl agent prompt --repo "$REPO_URL@main" --auto-create-pr --quiet \
  "Implement the issue, run tests, and open a PR."
```

Use for one task with no follow-up. Omit `--quiet` for NDJSON events. In Claude Code, prefer `--detach` (pattern 2) unless you can wait the full run in one Bash call.

### 2. Fire-and-forget: `agent send --detach`

Create a durable cloud agent, then detach as soon as its run ID is known:

```bash
agent_id="$(cursorctl agent create --repo "$REPO_URL@main" --auto-create-pr |
  jq -r '.agentId')"
cursorctl agent send "$agent_id" --detach "Implement the issue and open a PR."
# {"agentId":"bc-...","runId":"..."} (pretty-printed in default JSON)
```

Save both IDs. Later use `cursorctl run get RUN_ID`, `run wait RUN_ID`, or `run watch RUN_ID`. Detaching closes only the client stream; it does not cancel the server-side run.

This is the default pattern from Claude Code when the run may outlive a single Bash timeout.

### 3. Durable conversation: create, send, follow up

```bash
agent_id="$(cursorctl agent create --repo "$REPO_URL@main" --auto-create-pr |
  jq -r '.agentId')"
cursorctl agent send "$agent_id" --quiet "Implement the issue."
cursorctl agent send "$agent_id" --quiet "Now add regression tests and update the PR."
```

Use when later messages need the same agent's conversation context.

## When to open a reference file

| If the task is... | Read |
| --- | --- |
| Looking up any command, positional argument, flag, RPC, payload, or response | [`references/command-reference.md`](references/command-reference.md) |
| Delegating cloud work, detaching, following up, triaging agents, or collecting results | [`references/delegation-patterns.md`](references/delegation-patterns.md) |
| Parsing streams, choosing JSON/YAML/TOON, using `--json`, or handling exit codes | [`references/output-and-json-mode.md`](references/output-and-json-mode.md) |
| Debugging auth, bridge installation, truncated streams, runtime routing, or failures | [`references/troubleshooting.md`](references/troubleshooting.md) |

Wire-level SDK Bridge details: [sdk-bridge-protocol.md](https://github.com/nickmisasi/cursor-utils/blob/main/docs/sdk-bridge-protocol.md).

## Local agents and custom tools

Local agents run on this machine against `--cwd`; a model is required. Cloud agents clone `--repo`; their IDs start with `bc-`.

For local agents, `agent create --custom-tool NAME=COMMAND` declares a tool. Pass the same executor flag to `agent send` so cursorctl runs a loopback callback server. The command receives tool-argument JSON on stdin and should return a JSON object on stdout. See the command reference before using `--custom-tool-config`.

Local custom tools require the `agent send`/`agent prompt` process to stay attached; `--detach` shuts down the loopback executor.

## Top traps

1. Exit `2` is a completed run with terminal status `ERROR`, `CANCELLED`, or `EXPIRED`; exit `1` is a CLI, bridge, RPC, or stream failure. Exit `0` means `FINISHED` for run-returning commands.
2. `--json` is a complete raw RPC request, not an extra options object. It conflicts with positional and per-field flags by default. `--quiet`, `--detach`, artifact `--file`, and custom-tool executor flags are the documented exceptions where applicable.
3. `me`, `models`, and `repos` require the Cursor API key inside `options`; cursorctl injects it from `--api-key`, the env named by `--api-key-env`, `--profile`/`CURSORCTL_PROFILE`, or the stored default profile (`cursorctl auth add`).
4. `--detach` is not cancellation. `agent prompt --detach` skips `CloseAgent`. Follow up later with `agent send bc-...` (it resumes in the same process, then sends). Use `cursorctl run cancel RUN_ID` to request cancellation.
5. `agent send`, `agent prompt`, and `run watch` write one compact JSON event per line regardless of `-o`. Use `--quiet` to suppress events and format only the final result with `-o`.
6. `run watch --after-offset` accepts only an offset previously emitted by `run watch`/`ObserveRun`, not an offset from the initial `agent send` stream.
7. Cloud dashboard hides SDK agents by default; filter Source → SDK, or open `https://cursor.com/agents/bc-…`.
