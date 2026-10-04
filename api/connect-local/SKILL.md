---
name: connect-local
description: "Outbound bridge from matrx-extend to the matrx-local engine. Use when a browser tool needs a desktop-only capability (shell commands, local files), calls `desktopRpc` or `/extension/rpc`, needs engine port or tunnel discovery or its WebSocket push events, or hits 'desktop bridge offline'."
---

# connect-local — outbound calls into the Matrx Local desktop engine

The matrx-local desktop app exposes a small HTTP control surface for the
extension at `/extension/rpc`, plus a WebSocket for reverse-push events.
This skill is the entry point when you're working in this repo and need
to drive the desktop engine from extension code.

**Status reality check:** Channel B is active and live-E2E verified.
Local discovery probes 22140–22159 through public `GET /health`; remote
discovery reads the signed-in owner's freshest active
`app_instances.tunnel_url` under RLS. HTTP RPC and the offscreen WS use the
same engine-issued pair token. Two simultaneous packaged Chrome profiles and
independent reverse `read_page` calls were verified on 2026-08-08.

## When to use

- Wiring a new privileged tool that needs to shell out, read a local
  file, or run a desktop-only operation.
- Plumbing port discovery (probe-and-cache against `~/.matrx/local.json`).
- Subscribing the extension to an engine-pushed event (e.g. progress for
  a long-running command) over the WebSocket.
- Extending the `desktop_run_command` envelope shape.

## When NOT to use

- Changes to the matrx-local Python or Rust source. Switch to that repo
  and use its `connect-matrx-extend` skill.
- Anything that should run inside the browser sandbox (page DOM, tabs,
  cookies, screenshots). Those are extension-only — see the existing
  `src/lib/tools/handlers/` files.

## 30-second mental model

```
extension src/lib/desktop/http.ts
   │  POST <local-or-tunnel-base>/extension/rpc
   │  body: { command, args }
   ▼
matrx-local app/api/extension_routes.py
   │  extension_handlers.HANDLERS
   ▼
app/tools/dispatcher.py::dispatch
   │
   ├─→ result returned over HTTP response
   │
   └─→ progress pushed over WebSocket
        app/websocket_manager.py::broadcast / broadcast_notification

base = live port probe, then owner-RLS app_instances tunnel discovery
```

## Quick start

When you need to call a desktop command from extension code:

```ts
import { desktopRpc } from "@/lib/desktop/bridge";

const result = await desktopRpc({
  command: "tool",
  args: { tool_name: "SystemInfo", tool_input: {} },
});
```

Discovery in place today (see `src/lib/desktop/discovery.ts`):

1. SW cannot read `~/.matrx/local.json` directly, so the chosen port is
   discovered by parallel `GET /health` probes across 22140–22159
   (`DesktopHealthSchema` validates that the listener actually
   identifies itself as `service: "matrx-local"`).
2. Winner is cached in `chrome.storage.local` for 30 min; cache is
   invalidated on any subsequent `/health` or RPC failure so the next
   call re-discovers.
3. **Never use `POST /extension/rpc` for unauthenticated probing.**
   That endpoint is auth-walled by `AuthMiddleware` and rejects with
   401 — both a useless probe response *and* a warning per tick in the
   engine log. Health checks stay on `GET /health` (public).
4. If local discovery fails, query the owner's active `app_instances` rows
   for the freshest HTTPS `tunnel_url`; refresh this short cache on failures.
5. Surface "desktop bridge offline" loudly — privileged tools that
   need it should fail with a clear message, not hang.

## File index (extension side)

| File | Role |
|---|---|
| `src/lib/desktop/discovery.ts` | Local port probing + owner-RLS remote tunnel discovery |
| `src/lib/desktop/http.ts` | HTTP client; calls `getEngineBaseUrl()` for every `probeHttp` / `rpcHttp` |
| `src/lib/desktop/ws-client.ts` | WS reverse-channel client; resolves base URL the same way |
| `src/lib/desktop/types.ts` | RPC envelope and `DesktopHealthSchema` (the probe fingerprint) |
| `src/lib/tools/handlers/privileged.ts` | `desktop_run_command` lives here (lines 212–226) |
| `src/lib/desktop/discovery.ts` | Port discovery, its rate limits, and the last-good-port fast path. There is NO build-time fallback address: discovery returns `null` when the engine is offline, and callers degrade on that. |

## Engine-side reference (read-only from this repo)

- `app/api/extension_routes.py` + `extension_handlers.py` — HTTP command
  dispatch and the persistent WS route.
- `app/api/extension_invoke.py` + `extension_ws_manager.py` — engine-driven
  reverse invocation and per-profile session correlation.

## Failure modes

- **Loud: HTTP 502 / connection refused.** Discovery couldn't find any
  listener on 22140–22159 and the build-time fallback URL doesn't
  match either. Engine is offline, or it bound a port outside the
  scan range — check `~/.matrx/local.json`. The probe is cheap (one
  parallel fan-out per 30-min TTL), so the next alarm tick auto-recovers
  once the engine is back.
- **Spurious warning: `[auth] rejected POST /extension/rpc — missing
  bearer token`** in the engine log on every alarm tick. Means
  something is probing `/extension/rpc` without a token — the probe in
  `discovery.ts` should be on `GET /health`, not `POST /extension/rpc`.
  Anything that wants to call `/extension/rpc` must go through
  `rpcHttp` which attaches the bearer.
- **Remote 401 with a valid pair code.** Confirm the installed matrx-local
  includes the scoped outer-auth fix and that the active `app_instances`
  tunnel belongs to the machine that issued the pasted code.
- **Remote discovery empty.** The extension must be signed in, its Supabase
  session restored, and matrx-local must report `tunnel_active=true` with a
  fresh HTTPS `tunnel_url`.

## Pointer

For the full topology, the FORBIDDEN domain list (de-spaced forms of
`m a t r x . a p p` and `m a t r i x . c o m` — never reference either),
and the parallel channels (A and C), see
[`/Users/armanisadeghi/code/common-docs/systems/apps/extension/CHANNELS.md`](/Users/armanisadeghi/code/common-docs/systems/apps/extension/CHANNELS.md).
