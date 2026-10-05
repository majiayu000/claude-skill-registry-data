---
name: freemaster-lite-stop-server
description: >
  Stops a running FreeMASTER Lite instance. Use whenever the user wants to
  stop fmlite.exe, restart it with a different configuration, release the
  server port, or recover from a stuck or unresponsive FreeMASTER Lite service.
  Triggers on "stop FreeMASTER Lite", "kill fmlite", "restart with new config",
  "fmlite stuck", "shut down FreeMASTER Lite".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: freemaster
  tags: '[freemaster, lifecycle, shutdown, process]'
---

# Stopping FreeMASTER Lite

Cleanly shuts down a running `fmlite.exe` instance. Prefer the graceful
JSON-RPC path; fall back to OS-level process termination only when the service
is unresponsive.

## When to use

- Stopping the FreeMASTER Lite process itself.
- Restarting FreeMASTER Lite with a different configuration.
- Recovering from a stuck or unresponsive FreeMASTER Lite service.

Do **not** use this skill to stop target communication while keeping the
service alive — call the `StopComm` method via `freemaster-lite-jsonrpc-api`
instead.

## Quick start

```text
1. Open a WebSocket session (host="localhost", port=8090) -- reconnect if needed
2. call Exit {}                                      -- graceful shutdown
3. Verify: opening a new session now fails           -- service is gone
4. If step 2 fails or times out: terminate fmlite.exe via the OS
```

## Shutdown Procedure

### 1. Graceful shutdown via JSON-RPC

Open a WebSocket session to the service if not already connected:

```text
Input: host (default: "localhost"), port (default: 8090)
Output: { "session_id": "ws-session-id" }
```

Invoke the shutdown method:

```text
Call method: "Exit"
params: {}
result example: true
```

### 2. Fallback: OS process termination

Use when `Exit` fails, times out, or the service is too unresponsive for
JSON-RPC. Terminate the `fmlite.exe` (Windows) or `fmlite.bin` (Linux) process
through the host operating system.

### 3. Verify shutdown

Confirm the service is gone by attempting a new connection:

```text
Expected: opening a new WebSocket session fails — the service is no longer running.
```

Do not rely on target communication state to confirm process death; a
disconnected target does not mean the service has stopped.

## Guardrails

**Scope**
- This skill only terminates the FreeMASTER Lite process. It does not modify
  configuration files, delete data, or affect the embedded target.

**Destructive actions**
- Terminating the process drops all active WebSocket sessions without notice.
  Prefer the graceful `Exit` path. Use OS termination only as a last resort
  and report to the user that sessions were dropped.

**Secrets**
- No credentials involved.

**Refuse-and-escalate**
- If the user intended to stop target communication only (not the process),
  stop and redirect to the `StopComm` method in
  `freemaster-lite-jsonrpc-api`.

## Validation loop

1. After `Exit` call, attempt to open a new WebSocket session — it must fail or
   time out to confirm the process stopped.
2. After OS termination, verify the port is free (e.g. no process listening on
   the configured port).
3. If a restart is needed, use `freemaster-lite-start-server` after confirming
   shutdown.

## Out of scope

- Stopping target communication only (`StopComm`) — use `freemaster-lite-jsonrpc-api`.
- Starting FreeMASTER Lite — use `freemaster-lite-start-server`.
- Configuration file changes — use `freemaster-lite-configuration-file`.

## See Also

- `freemaster-lite-start-server` — launch FreeMASTER Lite after stopping it
- `freemaster-lite-jsonrpc-api` — `StopComm` stops target communication without
  killing the process
