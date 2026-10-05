---
name: freemaster-lite-start-server
description: >
  Launches the FreeMASTER Lite service (fmlite.exe / fmlite.bin) and verifies
  it is reachable. Use whenever the user wants to start FreeMASTER Lite, find
  fmlite.exe, start the service from a .fmcfg file, or troubleshoot startup
  readiness before using the JSON-RPC API or a web client. Triggers on "launch
  FreeMASTER Lite", "start fmlite", "FreeMASTER Lite not running", "fmlite.exe
  path", "start service from .fmcfg".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: freemaster
  tags: '[freemaster, lifecycle, startup, process]'
---

# Starting FreeMASTER Lite

Launches `fmlite.exe` and verifies the service is reachable before handing
off to the JSON-RPC API or web client skills. Startup is a three-state
sequence: process launched -> WebSocket service reachable -> target
communication active.

## When to use

- Launching the FreeMASTER Lite process.
- Starting the service from an existing `.fmcfg` file.
- Finding `fmlite.exe` on the host system.
- Troubleshooting startup readiness before JSON-RPC or browser client use.

Do **not** use this skill to create or edit a `.fmcfg` file
(`freemaster-lite-configuration-file`), use CLI flags only
(`freemaster-lite-command-line-arguments`), call JSON-RPC methods
(`freemaster-lite-jsonrpc-api`), or stop the service
(`freemaster-lite-stop-server`).

## Quick start

```text
1. Confirm fmlite.exe is installed (see common locations below).
2. Confirm a .fmcfg file exists; create one with freemaster-lite-configuration-file if not.
3. Launch: "<path_to_fmlite.exe>" "<path_to_config.fmcfg>"
4. Open a WebSocket session (host="localhost", port=8090) -- verify service reachable
5. call StartComm {} -- open target comm port
6. call IsCommPortOpen {} -- confirm board connected
```

## Finding fmlite.exe

Common Windows installation locations:

```text
C:\NXP\FreeMASTER 3.2\FreeMASTER Lite\fmlite.exe
C:\NXP\FreeMASTER Lite 1.5.0\fmlite.exe
```

Check these paths first. If not found, ask the user for the installation path
— do not guess custom locations.

## Launch Command

Provide the absolute path to the `.fmcfg` file:

```text
"C:\NXP\FreeMASTER 3.2\FreeMASTER Lite\fmlite.exe" "C:\workspace\my_project\freemaster.fmcfg"
```

On Linux use `fmlite.bin` with the same argument convention.

## Verify Service Reachable

```text
Open a WebSocket session to the service.
Input: host (default: "localhost"), port (default: 8090)
Output: { "session_id": "ws-session-id" }
```

If connection fails, wait briefly and retry — the service may still be
initializing. A successful session confirms the service is reachable, not that
the embedded target is connected.

## Start Target Communication

```text
Call method: "StartComm"
params: {}

Call method: "IsCommPortOpen"
params: {}
result: true = comm port open; false = service up but target not connected
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `fmlite.exe` not found | Wrong install path | Check common locations; ask user |
| Session connect fails | Service still initializing or wrong port | Wait and retry; check port in `.fmcfg` |
| Session connect fails | Config file path wrong or invalid | Verify path; use `freemaster-lite-configuration-file` |
| Session connect fails | Port already in use | Check for running instances |
| `IsCommPortOpen` false | Target not powered or wrong transport | Check `.fmcfg` connection settings |

## Guardrails

**Scope**
- This skill launches one `fmlite.exe` instance with one `.fmcfg` file.
- Do not start duplicate instances on the same port unless the user explicitly
  requests it.

**Destructive actions**
- Launching the process has no destructive effect on files. Stopping a running
  instance before relaunch requires `freemaster-lite-stop-server`.

**Secrets**
- No credentials involved.

**Refuse-and-escalate**
- If no `.fmcfg` file exists, stop and direct the user to
  `freemaster-lite-configuration-file` before proceeding.
- If `fmlite.exe` cannot be found after checking common locations, ask for
  the path — do not guess.

## Validation loop

1. Confirm `fmlite.exe` path resolves to an existing executable.
2. After launch, opening a WebSocket session must return a `session_id`
   within a few seconds.
3. `IsCommPortOpen` must return `true` before any variable read/write is
   attempted.
4. If any step fails, apply the troubleshooting table above before retrying.

## Out of scope

- Creating or editing `.fmcfg` — use `freemaster-lite-configuration-file`.
- One-off launch flags — use `freemaster-lite-command-line-arguments`.
- JSON-RPC method calls — use `freemaster-lite-jsonrpc-api`.
- Stopping the service — use `freemaster-lite-stop-server`.

## See Also

- `freemaster-lite-configuration-file` — create the `.fmcfg` file needed here
- `freemaster-lite-stop-server` — shut down before relaunching with new config
- `freemaster-lite-jsonrpc-api` — full API reference once the service is running
