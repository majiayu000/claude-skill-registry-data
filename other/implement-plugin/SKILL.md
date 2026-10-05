---
description: "Scaffold, implement, and test Starlark plugins. From protocol/event/phase selection to running sample tests"
user-invokable: true
---

# /implement-plugin

A workflow skill for creating Starlark plugins on the RFC-001 §9.3 plugin engine (`internal/pluginv2/`). Interactively select protocol/event/phase to generate a working scaffold.

## Arguments

- `/implement-plugin` — Create a plugin in interactive mode
- `/implement-plugin <description>` — Auto-generate a plugin from a description (e.g., `/implement-plugin Add X-Request-ID header to HTTP requests`)

## Steps

### Phase 1: Requirements Clarification

If no description argument is given, interactively confirm:

1. **Purpose**: What should the plugin do?
2. **Protocol**: Target plugin protocol — one of `http`, `ws`, `grpc`, `grpc-web`, `sse`, `raw`, `tls`, `connection`, `socks5` (the plugin protocol vocabulary; see `internal/pluginv2/surface.go`).
3. **Event**: Hook event under that protocol (e.g. `on_request`, `on_message`, `on_chunk`).
4. **Phase**: `pre_pipeline` (default — before Intercept/Transform) or `post_pipeline` (after; right place for signing/last-mile mutation). Lifecycle / observation events (`on_close`, `on_handshake`, `on_disconnect`, `socks5.on_connect`, etc.) take **no `phase=` argument** — passing one is a load-time error.
5. **Action**: CONTINUE (mutate in place) / DROP (transaction-start only) / RESPOND (transaction-start request, plus `http.on_response` for replacement).

If a description argument is given, auto-determine from its content.

### Phase 2: Context Collection

Read the following to understand the plugin API:

1. `docs/rfc/plugin-migration.md` — Direct migration table from legacy hook names to `(protocol, event, phase)` and the rationale.
2. `internal/pluginv2/surface.go` — The 17-entry hook surface table. Authoritative for which (protocol, event) pairs exist and which actions each accepts.
3. `internal/pluginv2/convert.go` — The Starlark `msg` dict shape per protocol (snake_case field names, `*HeadersValue` ordered list, `msg["raw"]` first-class byte injection).
4. `internal/pluginv2/lifecycle.go` — Dict shapes for lifecycle events (`connection.on_connect`, `socks5.on_connect`, `tls.on_handshake`, `ws.on_close`).
5. `internal/pluginv2/respond_action.go` — Typed `action.RESPOND(...)` / `action.RESPOND_GRPC(...)` builtin signatures.
6. `examples/plugins/` — Existing sample plugins for each major protocol.

### Phase 3: Plugin Generation

Create a plugin file in `examples/plugins/`:

- Filename: `<snake_case_name>.star`
- Include a comment block at the top describing purpose, the `register_hook` call(s), and a config snippet
- Hook registration is **script-driven** via `register_hook(protocol, event, fn[, phase=...])` — there is no `protocol`/`hooks` config key
- Hook signature is `def fn(msg, ctx):` — two positional arguments
- Returning `None` means CONTINUE; `action.DROP` drops; `action.RESPOND(...)` short-circuits with a synthetic response
- Mutate `msg` in place — `msg["headers"].append(name, value)`, `msg["body"] = b"..."`, `msg["raw"] = b"..."`. Mutations to the dict and to `*HeadersValue` are committed regardless of the return value.

#### Template Structure

```python
# <Plugin Name>
#
# Purpose: <description of purpose>
#
# Hook identity (RFC-001 §9.3):
#   register_hook("<protocol>", "<event>", fn[, phase="post_pipeline"])
#
# Config:
#   { "path": "examples/plugins/<name>.star", "on_error": "skip" }

def <hook_name>(msg, ctx):
    # Read fields: msg["method"], msg["headers"].get_first("X"), ...
    # Mutate fields: msg["headers"].append("X-Foo", "bar"), msg["body"] = b"..."
    return None  # CONTINUE

register_hook("<protocol>", "<event>", <hook_name>)
```

#### Protocol → `msg` dict shape (RFC-001 §9.3 + USK-669 snake_case)

| Plugin protocol | Events | Key fields on `msg` |
|-----------------|--------|---------------------|
| `http` | `on_request`, `on_response` | `method`, `scheme`, `authority`, `path`, `raw_query`, `status`, `status_reason`, `headers`, `trailers`, `body`, `anomalies` (RO), `raw` |
| `ws` | `on_upgrade`, `on_message`, `on_close` | `opcode`, `fin`, `masked`, `mask`, `payload`, `close_code`, `close_reason`, `compressed`, `raw` |
| `grpc` / `grpc-web` | `on_start`, `on_data`, `on_end` | start: `service`, `method`, `metadata`, `timeout`, `content_type`, `encoding`, `accept_encoding`; data: `service` (RO), `method` (RO), `compressed`, `wire_length`, `payload`, `end_stream`; end: `status`, `message`, `status_details`, `trailers` |
| `sse` | `on_event` | `event`, `data`, `id`, `retry`, `anomalies` (RO), `raw` |
| `raw` | `on_chunk` | `bytes`, `raw` |
| `tls` | `on_handshake` (lifecycle, no phase) | `side`, `sni`, `alpn`, `version_name`, `cipher_name`, `peer_cert_subject`, `client_fingerprint` (frozen) |
| `connection` | `on_connect`, `on_disconnect` (lifecycle, no phase) | connect: `conn_id`, `client_addr`, `listener_name`; disconnect: `conn_id`, `client_addr`, `duration_ms` (frozen) |
| `socks5` | `on_connect` (lifecycle, no phase) | `conn_id`, `client_addr`, `target_addr` (frozen) |

`headers` / `trailers` / `metadata` are `*HeadersValue` instances, not dicts. Methods: `append(name, value)`, `delete_first(name) -> bool`, `replace_at(index, name, value)`, `get_first(name) -> str|None`. Iteration yields `(name, value)` 2-tuples; `name in headers` is case-insensitive. Wire order, casing, and duplicates are preserved.

#### `ctx` (second positional argument)

- `ctx.client_addr` — client IP string (port stripped) or `None`
- `ctx.tls` — frozen dict of `{sni, alpn, version_name, cipher_name, peer_cert_subject, client_fingerprint}` or `None`
- `ctx.transaction_state` / `ctx.stream_state` — mutable scoped dicts: `.get(k)`, `.set(k, v)`, `.delete(k)`, `.keys()`, `.clear()`. Lifetime is owned by the Layer (transaction = (ConnID, FlowID) for HTTP / (ConnID, StreamID) for streaming protocols; stream = (ConnID, StreamID) always).

#### Action constraints (RFC-001 §9.3, surface.go)

| Action | Allowed events |
|--------|----------------|
| CONTINUE | All events (always implicit) |
| DROP | Transaction-start only: `http.on_request`, `ws.on_upgrade`, `grpc.on_start`, `grpc-web.on_start`, `connection.on_connect`, `socks5.on_connect` |
| RESPOND | Transaction-start request events (as above, minus `connection`/`socks5`), plus `http.on_response` (replace upstream response). gRPC uses `action.RESPOND_GRPC(status, message, trailers)` instead of `action.RESPOND(...)`. |

Mid-stream events (`on_data`, `on_message`, `on_event`, `on_chunk`) and lifecycle/observation events (`on_close`, `on_end`, `on_handshake`, `on_disconnect`) accept CONTINUE only — terminating a stateful stream uses native termination (gRPC `RST_STREAM`, WS close frame), not an action enum.

### Phase 4: Verification

1. Visually verify Starlark syntax (compliance with `go.starlark.net` syntax rules)
2. Build and run the engine load tests:

```bash
make build
make test
```

The engine's `LoadPlugins` validates `register_hook` calls at load time — unknown protocol/event, invalid phase, or non-callable `fn` are reported as `LoadError` with `Kind` = `LoadErrUnknownProtocol` / `LoadErrUnknownEvent` / `LoadErrInvalidPhase` / `LoadErrPhaseNotSupported` / `LoadErrNotCallable`.

### Phase 5: Present Configuration Example

Present the `PluginConfig` for the generated plugin (RFC-001 shape — no `protocol`/`hooks` keys at the config level):

```json
{
  "path": "examples/plugins/<name>.star",
  "vars": { "<key>": "<value>" },
  "on_error": "skip",
  "max_steps": 1000000,
  "redact_keys": []
}
```

`vars` is exposed as a frozen Starlark `config` dict; `redact_keys` hides values from `plugin_introspect`. Plugins are loaded once at proxy boot; to change the loaded set, edit the config and restart the proxy (RFC §9.3 D2).

For runtime introspection, use the `plugin_introspect` MCP tool — read-only listing of loaded plugins and their `(protocol, event, phase)` registrations:

```json
// MCP tool: plugin_introspect
{}
```

The legacy `plugin` MCP tool (`list`/`reload`/`enable`/`disable`) was removed in USK-695; there is no replacement for `reload`/`enable`/`disable` by design.

## Notes

- **gRPC mid-stream events accept CONTINUE only.** DROP/RESPOND on `grpc.on_data` / `grpc.on_end` is a load-time/dispatch-time error. `grpc.on_start` accepts DROP and `action.RESPOND_GRPC(...)`.
- **WebSocket mid-stream events accept CONTINUE only.** To redact a `ws.on_message` payload, mutate `msg["payload"]` in place rather than dropping. To refuse a connection, hook `ws.on_upgrade` and return DROP.
- **`(socks5, on_connect)` accepts DROP** for connection-level allowlists, but **no `phase=` argument** — it is a lifecycle event.
- **WebSocket Ping/Pong frames are still delivered** as `(ws, on_message)` events; filter by `msg["opcode"]` (0x9 = ping, 0xA = pong, 0x1 = text, 0x2 = binary) when only certain frame types matter.
- **`msg["raw"] = b"..."` writes verbatim wire bytes** (RFC §9.3 D4 "raw wins") — when both raw and message-side fields are mutated, raw is shipped and message-side mutations are recorded only in the variant snapshot.
- **Body cap**: `msg["body"]` is capped at 1 MiB; oversize bodies are surfaced as `ErrBodyTooLarge` and the plugin is skipped (the body is never truncated for the plugin).
- **Starlark is a subset of Python**: `import`, `class`, file I/O, and network access are not available. `print()` writes to the proxy log.
- **Module-level variables are frozen after load** — mutable objects (lists, dicts) at module level cannot be modified inside hooks. Use immutables (strings, ints, tuples) at module level; mutate via `msg` / `ctx.transaction_state` / `ctx.stream_state` / `state.*` instead.
- **`config` is a frozen dict** of `vars` from the plugin config. Use `config["key"]` (or membership-test first with `"key" in config`) — there is no schema enforcement beyond the engine's primitive type whitelist.
