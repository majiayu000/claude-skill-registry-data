---
type: Skill
name: mcp-ai-artcraft-ops
description: "Operational guide for the ArtCraft MCP integration — the community Python rebuild (C:\\Users\\rasta\\artcraft-mcp-py\\artcraft_mcp_server.py) that replaces the broken upstream artcraft-mcp.exe, the live api.storyteller.ai/v1 API map (required headers, cookie auth, endpoint schemas), the upstream bug/PR trail (issues #1/#3, PR #2), the reverse-engineering playbook (browser capture, cookie injection, schema fishing via validation errors, handshake replay, Windows MITM kit), and the generic MCP-protocol debugging playbook (snake_case servers, the shim pattern, 'missing field protocolVersion' diagnosis). Use when working on ArtCraft MCP tools, debugging an artcraft server connection, extending the Python rebuild, or diagnosing any third-party MCP handshake failure."
license: Proprietary. See LICENSE.txt
metadata:
  plugin: mcp-ai-wpoos
  plugin-version: "1.1.94"
  plugin-version-tested: "1.1.94"
  last-updated: "2026-10-12"
---

# ArtCraft MCP Operations

Operational guide for the ArtCraft (generative media platform) MCP
integration. Everything below was reverse-engineered and verified live in the
2026-10-11/12 session: the upstream binary is broken two ways (protocol +
dead API), a Python rebuild now works end-to-end against the live API, and
the full endpoint map is captured in `reference/api-map.md`.

## When to use this skill

- "Why can't I connect to the artcraft MCP" / "artcraft MCP is broken"
- Extending the Python rebuild (`artcraft_mcp_server.py`) with new tools
- Any ArtCraft API question (models, cost, generation, jobs, library)
- Diagnosing **any** third-party MCP handshake failure — see the generic
  [MCP debugging playbook](#mcp-handshake-debugging-playbook-generic) section

## Context: why the shipped exe is dead

The upstream repo is `theCosmicCrafter/artcraft-mcp`. Its
`bin/artcraft-mcp.exe` (reports `serverInfo.version: 0.1.0` inside the v1.1.0
zip) fails twice:

1. **Wire-format bug** — its Rust structs serialize with snake_case field
   names (`protocol_version`, `server_info`, `list_changed`, `input_schema`,
   `is_error`); the MCP spec requires camelCase. Strict clients (Zed) abort
   the handshake: `missing field 'protocolVersion' at line 1 column 137`.
   Fixed upstream in PR #2 (serde `rename_all = "camelCase"` on
   `InitializeResult`, `ToolCapabilities`, `Tool`, `ToolCallResult` in
   `rust/artcraft_mcp_cli/src/types.rs`).
2. **Dead API surface** — the exe's private `artcraft_client` crate hardcodes
   `ApiHost::Storyteller` → `https://api.storyteller.ai` **and** calls stale
   `/v1/*` paths (`/v1/users/session_info`, `/v1/tts/models`, …) that no
   longer exist. The API moved routes and now requires web-origin headers.
   Tracked in upstream issue #3. The crate is not vendored in the public repo
   and is not on crates.io — only the maintainer can fix the binary.

## The working stack now

| Piece | Location |
|---|---|
| Python MCP server (live, 11 tools) | `C:\Users\rasta\artcraft-mcp-py\artcraft_mcp_server.py` (stdlib only, no deps) |
| CDP driver + capture hooks | `C:\Users\rasta\artcraft-mcp-py\cdp.js`, `hooks.js`, `set-file.js`, `char-upload.js` — drive/capture the desktop app's WebView2 |
| Legacy exe + shim (disabled) | `C:\Users\rasta\Downloads\artcraft-mcp.exe`, `artcraft-mcp-shim.js` |
| Zed config | user-level `settings.json`: `artcraft` → `enabled: false`; `artcraft-py` → `enabled: true` (`python` + the script path) |
| Zed backups | `settings.json.artcraft-backup`, `settings.json.pre-artcraft-py-backup` |
| MITM kit (unused now) | `C:\Users\rasta\artcraft-mitm\` (CA, proxy.js, add/remove-hosts.bat) |
| Upstream fork for the PR | `nvdigitalsolutions/artcraft-mcp`, branch `fix/mcp-wire-format-camelcase`, local clone at `C:\Users\rasta\AppData\Local\Temp\artcraft-mcp-fix` |

**The desktop app shares the same backend, session cookies, and library.**
Generations submitted via the Python server appear in the app's library
(verified). The app does not need to run; the server reads its cookie store.
Logging out of the app invalidates the MCP session too (same cookie).

## Auth (load order in the server)

1. `ARTCRAFT_SESSION` / `ARTCRAFT_AVT` env vars (raw cookie values)
2. `~/Artcraft/credentials/artcraft_session.txt` / `artcraft_avt.txt`
3. Tauri cookie store `%LOCALAPPDATA%\ai.artcraft.app\.cookies` — JSON array,
   `raw_cookie` strings `session=…; …` / `visitor=…; …` (host-only for
   `api.storyteller.ai`)

Env overrides: `ARTCRAFT_API_BASE` (default `https://api.storyteller.ai`),
`ARTCRAFT_WEB_ORIGIN` (default `https://app.getartcraft.com`).

## Live API essentials

- **Every request needs**: `Origin: https://app.getartcraft.com`,
  `Referer: https://app.getartcraft.com/`, `Cookie: session=…; visitor=…`,
  `Accept: application/json`, browser-ish User-Agent. Without the
  Origin/Referer pair Cloudflare serves 404/HTML for everything — this is the
  single biggest gotcha (cost the original debugging session a lot of time).
- `POST /v1/omni_gen/generate/*` requires an `idempotency_token` (UUID v4
  string) or it 400s with "idempotency token does not match the expected
  format".
- Full endpoint + shape map: see [`reference/api-map.md`](reference/api-map.md).

## Extending the Python server

1. Add a handler in `TOOL_ROUTER` + a definition in `build_tool_definitions()`
   (inputSchema keys are camelCase).
2. Reuse `api_request(method, path, body)` — it attaches headers + cookies.
3. Test with the printf replay pattern:

   ```bash
   printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"zed","version":"1"}}}' \
     '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
     '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
     '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"<tool>","arguments":{}}}' \
     | python "C:/Users/rasta/artcraft-mcp-py/artcraft_mcp_server.py"
   ```

4. Never submit paid generations while probing — prefer the cost endpoint and
   model enums; `flux_1_schnell` is free if a live run is unavoidable. The
   cost endpoints double as schema oracles: an invalid body returns the valid
   enum/field list in the error message (the "schema fishing" trick).

## MCP handshake debugging playbook (generic)

- **`missing field 'protocolVersion' at line 1 column N`** (or similar serde
  field errors) = the server emits non-spec JSON. Replay the handshake to see
  the raw response: `printf '<initialize json>' | <server>`. If the response
  shows snake_case (`protocol_version`, `server_info`, `input_schema`,
  `is_error`), the server is non-compliant.
- **Fix options**: upstream fix (serde `rename_all`, struct tags) or a local
  **shim** that spawns the broken server and rewrites the known fields —
  pattern lives at `C:\Users\rasta\Downloads\artcraft-mcp-shim.js`.
- Binary forensics: scan the exe for baked-in URLs/hosts with Node
  (`buf.toString('latin1')` + regex) — `strings` may not exist on Windows.
- If an API 404s from scripts but works from a web app, diff the request
  headers — Cloudflare origin rules (`x-rule-id` response header) commonly
  gate on `Origin`/`Referer`.
- Windows MITM recipe (does NOT work for Rust/rustls binaries that ignore the
  Windows cert store — that's how we ended up on browser capture): CA +
  per-host cert via openssl (use `//CN=` in Git Bash to defeat path
  mangling), `certutil -user -addstore Root`, Node TLS proxy on 443
  forwarding to real IPs with `servername`, hosts redirects via an elevated
  `.bat` (`Start-Process -Verb RunAs`), and full teardown after.
- **Browser capture beats MITM** when a web app exists: navigate with the
  Playwright tools, inject the desktop app's cookies via
  `browser_run_code_unsafe` + `page.context().addCookies(...)` (domain =
  the API host), then harvest `browser_network_requests` +
  `browser_network_request` bodies. Delete the injection script file
  immediately — it contains the cookie values.
- **Desktop-app capture (best, verified 2026-10-12):** relaunch the app with
  `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=9222` (env
  var for that launch only), connect CDP to `http://127.0.0.1:9222`, and
  inject `hooks.js` via `Runtime.evaluate`. The webview calls the Rust core
  via `fetch('http://ipc.localhost/<command>', …)` and makes API calls via
  the Tauri HTTP plugin (`ipc.localhost/plugin%3Ahttp%7Cfetch`) — its request
  `clientConfig` exposes the **full API URLs** (e.g.
  `https://api.storyteller.ai/v1/media_files/upload/image`), and the
  `fetch_send`/`__TAURI_CHANNEL__` entries carry response bodies. Drive the
  UI by clicking text nodes / coordinates, set files with
  `DOM.setFileInputFiles` (`set-file.js`, `char-upload.js`). Synthetic
  `KeyboardEvent('keydown',{key:'Escape'})` closes React dialogs; clicks can
  be blocked by overlays — close them first. Gotcha: the webview runs at
  `http://tauri.localhost/` and the app's API `Origin` is
  `https://studio.storyteller.ai` (the Python server's
  `ARTCRAFT_WEB_ORIGIN` default of `app.getartcraft.com` also works — both
  pass the Cloudflare rules).

## Known quirks

- Credits endpoint shows zeros for accounts with no credit balance — not an
  auth failure by itself (`/v1/session` `logged_in: true` is the auth test).
  Paid generations return `402 Payment Required` (`billing_issue`) — the
  request is still logged/valid, so a 402 can be used to verify request
  contracts without spending.
- Upload response shape is `{"success":true,"media_file_token":"m_…"}`
  (top-level), NOT `media_file.token` — the desktop app's channel showed a
  nested `media_file` wrapper; trust the direct API shape.
- TTS / voice tools are **retired** from the current API — every old
  `/v1/tts/*`, `/v1/voices/*`, `/v1/voice_designer/*` path 404s and the
  Create Audio page only offers Suno/Seed models. Do not re-add TTS tools.
- `media_files/list` results carry `public_bucket_url` +
  `media_links.cdn_url`; thumbnails are
  `cdn-cgi/image/width={WIDTH},quality=95/…` templates on `cdn-2.fakeyou.com`.
- Prompt text is not inline in media results — use
  `GET /v1/prompt/batch?tokens=a&tokens=b` (a few tokens per call).
- `jobs/session` is the poll loop; terminal states: `complete_success`,
  `complete_failure`, `cancelled`, `dead`.
- Model capabilities arrive per model: `aspect_ratio_options`,
  `resolution_options`, `quality_options`, `batch_size_min/max`,
  `image_refs_supported`, `text_prompt_supported` — mirror them in tool
  descriptions instead of hardcoding.

## Upstream tracker

| Item | Link | State (2026-10-12) |
|---|---|---|
| Issue #1 | snake_case handshake | open |
| Issue #3 | dead `api.storyteller.ai` host + stale endpoints | open |
| PR #2 | serde camelCase fix (fork `nvdigitalsolutions`) | open, unbuilt (no Rust toolchain locally) |

## Cleanup notes

- `C:\Users\rasta\artcraft-mitm\` is safe to delete when no future desktop-app
  capture is planned (contains a locally generated CA key).
- If the upstream maintainer ships a rebuilt exe: re-test the handshake
  before deleting the shim, and re-verify the endpoints before deleting the
  Python rebuild.
