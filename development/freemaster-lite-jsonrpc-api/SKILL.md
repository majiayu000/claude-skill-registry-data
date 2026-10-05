---
name: freemaster-lite-jsonrpc-api
description: >
  Drives a running FreeMASTER Lite instance over its WebSocket JSON-RPC
  interface. Use whenever the user wants to connect to FreeMASTER Lite, start
  or stop target communication, load ELF or TSA symbols, define variables
  dynamically, validate variable definitions, read variables, write variables,
  or handle JSON-RPC errors. Triggers on "ReadVariable", "WriteVariable",
  "DefineVariable", "StartComm", "ReadELF", "GetAppVersion".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: freemaster
  tags: '[freemaster, jsonrpc, websocket, variables, communication]'
---

# FreeMASTER Lite JSON-RPC API

Interacts with a running FreeMASTER Lite instance over its WebSocket JSON-RPC
interface. Covers the full state sequence from WebSocket session setup through
target communication and variable access.

## When to use

- Connecting to a running FreeMASTER Lite service over WebSocket.
- Calling JSON-RPC methods: `GetAppVersion`, `StartComm`, `StopComm`,
  `IsCommPortOpen`, `ReadELF`, `ReadTSA`, `DefineVariable`, `GetVariableInfo`,
  `ReadVariable`, `WriteVariable`, `Exit`.
- Distinguishing service reachability from target communication state.
- Interpreting JSON-RPC errors and building a basic call sequence.

Do **not** use this skill to create `.fmcfg` files (`freemaster-lite-configuration-file`),
launch or stop the process (`freemaster-lite-start-server` /
`freemaster-lite-stop-server`), or build browser PCM clients
(`freemaster-lite-web-application`).

## State Model

Keep these three states distinct:

1. **Process running** — `fmlite.exe` has been launched.
2. **Service reachable** — WebSocket session opened to the service.
3. **Target communication active** — `StartComm` succeeded and `IsCommPortOpen` returns `true`.

A reachable service does not mean the embedded target is connected.

## Quick start

```text
1. open a WebSocket session                          -- connect to the service
2. call GetAppVersion {}                             -- confirm service alive
3. call StartComm {}                                 -- open target comm port
4. call IsCommPortOpen {}                            -- must return true
5. call ReadELF {}                                   -- load symbols (or ReadTSA)
6. call DefineVariable {"variable": {...}}           -- if not in .fmcfg
7. call GetVariableInfo {"name": "x"}                -- verify addr resolved
8. call ReadVariable {"name": "x"}                   -- read value
9. call WriteVariable {"name": "x", "value": 10.0}
10. call StopComm {}                                 -- release comm port
```

## Session Setup

```text
Open a WebSocket session to the service.
Input: host (default: "localhost"), port (default: 8090)
Output: { "session_id": "ws-session-id" }
```

Safe to reconnect or switch to a different instance.

## Method Reference

All operations call a JSON-RPC method:

```text
Input: method (string), params (dict or {})
Output: full JSON-RPC response; "result" on success, "error" on failure
```

| Method | params | result |
|--------|--------|--------|
| `GetAppVersion` | `{}` | version string |
| `StartComm` | `{}` | `true` |
| `StopComm` | `{}` | `true` |
| `IsCommPortOpen` | `{}` | `true` / `false` |
| `ReadELF` | `{}` | `true` |
| `ReadTSA` | `{}` | `true` |
| `DefineVariable` | `{"variable": {...}}` | `true` |
| `GetVariableInfo` | `{"name": "<name>"}` | variable descriptor |
| `ReadVariable` | `{"name": "<name>"}` | current value |
| `WriteVariable` | `{"name": "<name>", "value": <number>}` | `true` |
| `Exit` | `{}` | `true` (terminates process) |

### DefineVariable — variable object fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Variable name |
| `addr` | number \| string | yes | Address or ELF symbol name |
| `type` | string | yes | `int`, `uint`, `float`, `double`, `fract`, `ufract` |
| `size` | number | yes | `1`, `2`, `4`, or `8` |
| `shift` | number | no | Right-shift for integer types |
| `mask` | number | no | AND mask after shifting |
| `q_n` | number | fract/ufract | Fractional bits |
| `q_m` | number | fract/ufract | Integer bits |

After `DefineVariable`, call `GetVariableInfo` to confirm the definition
resolved to a numeric address (not just a symbol name) before reading or
writing.

## Error Handling

On failure, the response contains `error` instead of `result`:

```json
{ "jsonrpc": "2.0", "id": 3,
  "error": { "code": -32602, "message": "Variable not found: g_unknown" } }
```

Always check for `error` before using `result`.

## Guardrails

**Scope**
- This skill calls the FreeMASTER Lite JSON-RPC API only. It does not modify
  `.fmcfg` files or embedded firmware.

**Destructive actions**
- `WriteVariable` modifies live target memory. Confirm the variable name and
  value with the user before writing, especially for safety-critical variables.
- `Exit` terminates the FreeMASTER Lite process. Use
  `freemaster-lite-stop-server` for process lifecycle management.

**Secrets**
- No credentials involved in JSON-RPC calls.

**Refuse-and-escalate**
- If `IsCommPortOpen` returns `false` after `StartComm`, stop and diagnose
  the connection settings before attempting variable access.
- If `GetVariableInfo` shows no numeric address after `DefineVariable`, do not
  attempt `ReadVariable` or `WriteVariable` — the symbol was not resolved.

## Validation loop

1. `GetAppVersion` must return a non-empty version string after the session opens.
2. `IsCommPortOpen` must return `true` before any variable operation.
3. After `DefineVariable`, `GetVariableInfo` must show a numeric `addr` field.
4. `ReadVariable` result must be a number, not an error object.
5. After `WriteVariable`, read back the value with `ReadVariable` to confirm
   the write was accepted.

## Out of scope

- `.fmcfg` file creation — use `freemaster-lite-configuration-file`.
- Process launch or shutdown — use `freemaster-lite-start-server` /
  `freemaster-lite-stop-server`.
- Browser-side PCM client — use `freemaster-lite-web-application`.

## See Also

- `freemaster-lite-start-server` — launch the service before connecting
- `freemaster-lite-stop-server` — terminate the process via `Exit`
- `freemaster-lite-web-application` — browser-side PCM API for the same operations
