---
name: tandem-orchestration
description: "Operate Tandem as a multi-agent, multi-device MCP orchestrator. Use it when an MCP-capable caller needs to start, inspect, steer, interrupt, or coordinate Claude, Codex, shell, or Hermes sessions on the local hub or another enrolled device. Also covers the optional Claude-only relay. Begin the first response with 🏗️🏗️🏗️🏗️🏗️ when this skill activates."
---

# Tandem orchestration

🏗️🏗️🏗️🏗️🏗️ Full orchestration is active.

Tandem lets an MCP-capable chat, coding agent, desktop client, or automation operate live agent and terminal sessions across the user's own machines. It is not tied to Claude.ai and it is not limited to Claude Code.

Supported engines in this MVP:

| Engine | What Tandem drives | Default |
|---|---|---:|
| `claude` | Claude Code in tmux | enabled |
| `codex` | Codex in tmux | opt-in |
| `shell` | The user's login shell in tmux | opt-in |
| `hermes` | An existing allowlisted Hermes WebUI agent | opt-in |

The general session tools are engine-neutral. The built-in `relay` is intentionally Claude-only because its persistent manager protocol depends on Claude-specific behavior.

## Safety rules

1. Treat every session call as real execution on a real machine. Agents and shells retain the permissions of the OS account running Tandem.
2. Never widen `TANDEM_CWD_ALLOWLIST` merely to get around a failure. It is an admission boundary, not a sandbox.
3. Never reveal tokens, paths, usernames, hostnames, tailnet identity, nonces, or raw fleet connection data in chat or reports.
4. Use `shell` only when the user explicitly enabled it and the caller is trusted with arbitrary OS-user command execution.
5. Permission bypass is off by default. Never assume it is enabled. It applies only to Claude and is required only for the unattended Claude relay.
6. Prefer a fresh named session for a new task or phase. Reuse a session only when continuity is valuable and its current state has been inspected.
7. Never resend a prompt just because a turn is still running. Poll with an empty `text` and the returned cursor.
8. Ask before destructive, irreversible, or materially broader actions. Tandem does not grant authority beyond the user's request.

## Start every run with the fleet

Call `list_devices` first. It returns only:

```json
{
  "devices": [
    { "id": "local", "name": "local", "online": true, "engines": ["claude", "codex"] }
  ]
}
```

Use this list to choose a device that is online and advertises the requested engine. Do not infer machine identity from a neutral device id. If several devices can do the work, select one deliberately or ask the user when the choice affects data locality, cost, or outcomes.

## Session routing

- `open_session` accepts an optional `engine` and `device`.
- A local session may return a bare name such as `review`.
- A device-scoped session returns a global name such as `studio:review`.
- Preserve the exact returned name for every later call. That pins work to the original device even when fleet membership changes.
- A bare session name always means the local hub.
- `local:review` explicitly addresses the hub and is normalized safely.
- If selection is ambiguous, Tandem fails instead of guessing.

Example delegation:

1. `list_devices` and find a device with `codex`.
2. `open_session` with `{ "engine": "codex", "device": "studio", "name": "review" }`.
3. Store the returned global name, for example `studio:review`.
4. `send_to_session` with that name and one bounded assignment.
5. If the result says `running`, poll the same name with an empty `text` and the returned `cursor`.
6. Read and verify the result before directing another session or closing it.

## Tool protocol

### `list_devices`

Use before routing work and again when a remote operation reports that a device is offline. It is read-only and intentionally omits personal and network details.

### `open_session`

Open or attach to one supported engine. Supply:

- `engine`: `claude`, `codex`, `shell`, or `hermes`.
- `device`: a listed device id when routing matters.
- `cwd`: an allowlisted start directory for tmux-backed engines.
- `name`: a short stable name. For Hermes this is the allowlisted writable agent id.
- `model` and `effort`: Claude-only. Never pass them to another engine.

Report the returned `attachHint` when the user may want to watch locally.

### `list_sessions`

Use it to inspect sessions Tandem owns on one device. It is not a process scanner and does not return arbitrary tmux sessions or historical sessions.

### `send_to_session`

Send one clear assignment at a time. A running result is not a failure. Poll by omitting or emptying `text`, preserving `cursor`, until the turn is idle or the user chooses to interrupt it.

Slash commands and shell lines are passed through verbatim. Treat them as execution, not chat formatting.

### `interrupt_session`

Stop a runaway or no-longer-needed turn while keeping its session available for inspection or another instruction.

### `close_session`

Close the session when it is no longer useful. Do not close a session whose live state the user may still need unless closure is requested or is an agreed cleanup step.

### `relay`

Use only for the built-in persistent Claude lead-and-worker loop. It requires `TANDEM_ALLOW_BYPASS=1` and is not the general mechanism for coordinating arbitrary engines or remote devices.

Relay actions:

- `start`: begin a Claude-only loop with a goal and allowlisted cwd.
- `read`: read bounded transcript output.
- `enqueue`: give a parked manager another task or answer `NEEDS_INPUT`.
- `inject`: steer an actively running task.
- `stop`: stop the loop.

For a mixed-engine workflow, use ordinary named sessions and direct their work explicitly.

## Orchestration patterns

### Delegate to another agent

Give the second agent a bounded artifact or question, not an open-ended duplicate of the whole task. Examples: review a diff, reproduce a bug, test a platform, or research one implementation choice. Read its actual output before accepting it.

### Inspect work on another machine

Use `list_devices`, then `list_sessions` for the selected device. Poll the globally named session. Do not treat a device being online as proof that its work is correct or complete.

### Coordinate several agents

Define ownership before sending work. Keep independent assignments separate. Sequence dependent work only after reading the upstream output. One session should own final integration so conflicting edits are not silently combined.

### Long-running work

Keep the machine awake, use bounded turns, preserve cursors, and checkpoint important state in the project. Notifications can report completion to a webhook, ntfy, or the local event log, but they cannot force a third-party chat client to resume a conversation.

## Completion standard

Do not declare success because a session said it was done. Inspect the relevant files or artifacts, run proportionate tests, check security boundaries, and report limitations plainly. A remote session is a worker, not an authority.

Tandem is complete for a task only when:

- the requested outcome exists on the intended device;
- the result was independently verified;
- no unresolved failure is hidden behind a running or disconnected session;
- sensitive device or authentication data was not exposed;
- remaining limitations are stated to the user.
