---
name: omniroute-gateway
description: OmniRoute install, MCP, Hermes on WSL. Load on issues.
version: 1.0.0
author: Hermes Agent + Publieople
license: MIT
metadata:
  hermes:
    tags: [omniroute, gateway, mcp, providers, llm-router, wsl, systemd]
    related_skills: [hermes-agent, hermes-bootstrap]
---

# OmniRoute Gateway — Install, Configure, Integrate

OmniRoute is a **local AI gateway**: a Node.js HTTP server (`http://localhost:20128`) exposing an OpenAI-compatible API at `/v1` that proxies to 290+ upstream AI providers with auto-failover, 12-factor scoring, and 15-95% token compression. Goal: replace direct provider API calls with one local endpoint so any AI coding tool (Claude Code, Codex, Cursor, OpenCode, Hermes, etc.) gains provider-agnostic resilience.

This skill captures the **operational** knowledge needed to install OmniRoute, expose its MCP server to external agents (Hermes), and integrate it as a model provider — knowledge that repeats every time someone sets this up fresh.

## When to load this skill

- "install OmniRoute" / "set up OmniRoute"
- "route Claude Code / Codex / Cursor through OmniRoute"
- "expose OmniRoute's MCP tools to Hermes"
- "OmniRoute is detected but Hermes isn't" / "OmniRoute 500 errors"
- "switch Hermes default to OmniRoute"
- "set up an AI gateway / LLM router"
- Troubleshooting MCP connection failures to localhost:20128
- **"opencode-go 400 MissingSessionID / x-opencode-session"** — opencode.ai 自 2026-09-06 强制该头；3.8.49 默认只透传不合成，**3.8.50 起默认合成**（`OPENCODE_SYNTHESIZE_CLI_HEADERS` 反转为 opt-out）。升级到 ≥3.8.50 即修复，勿设 false。
- **npm 自更新跳过 install scripts** — `npm install -g omniroute@latest` 报 "install scripts not yet covered by allowScripts"（better-sqlite3 等 native 包静默跳过 → 500）。重跑带完整 allow-scripts CSV，再 `omniroute doctor` 验证 native binary OK。
- **"omniroute.service restarting loop" / "exit-code 203 EXEC"** — unit pointing at wrong binary path
- **"AppImage / AUR omniroute-bin failed" / "sqlite driver unavailable on AppImage"**
- **"Missing X server or $DISPLAY" / "platform failed to initialize"** in omniroute service log
- **"PATCH /api/settings returns 200 but does nothing on languageConfig"** → real endpoint is `PUT /api/settings/compression`
- **"compression_status MCP tool does not show languageConfig"** → schema intentionally partial; use `GET /api/settings/compression` to see `languageConfig`
- **"key value masked in API response" / "reveal disabled"** — API key not recoverable; ask user to Dashboard-copy
- **"Too many failed attempts on /api/auth/login"** → restart service to clear

## The 7-step install procedure on Linux/WSL

```bash
# 1. Install (background — ~5 min, 1176 packages)
npm install -g omniroute

# 2. CRITICAL: re-install with native-binding scripts allowed.
#    Without this, better-sqlite3/sharp/onnxruntime-node are silently skipped
#    and the CLI launches but every endpoint returns HTTP 500 ("better-sqlite3
#    native binary was not found"). The full allow-scripts CSV:
npm install -g --allow-scripts=omniroute,better-sqlite3,keytar,tls-client-node,onnxruntime-node,sharp,core-js,esbuild,@parcel/watcher,@swc/core,protobufjs,koffi omniroute

# 3. Verify native binary
omniroute doctor
#   → "OK  Native binary: better-sqlite3 native binary is compatible"

# 4. systemd unit at ~/.config/systemd/user/omniroute.service
#    ⚠️ MUST have ProtectHome=false AND ProtectSystem=false.
#    The default templates ship with ProtectHome=read-only, which makes SQLite
#    writes silently fail (storage.sqlite created at install but never
#    updated post-startup) → /v1/models and /api/health return HTTP 500 with
#    no log error. The "OmniRoute is running!" banner lies — it only proves
#    the HTTP server bound the port, not that requests work. Verify with curl:
curl http://localhost:20128/v1/models
#   → 200 + JSON catalog. If 500, fix ProtectHome/ProtectSystem and restart.

# 5. Enable + start
systemctl --user daemon-reload
systemctl --user enable --now omniroute.service

# 6. Wait ~8s for "OmniRoute is running!" then verify with curl.
# 7. Add providers via Dashboard (http://localhost:20128) — or use the
#    OmniRoute Agent Skills catalog at /api/agent-skills for automation.
```

**Reference systemd unit (tested, works):**

```ini
[Unit]
Description=OmniRoute AI Gateway
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/po
ExecStart=/home/po/.npm-global/bin/omniroute
Restart=on-failure
RestartSec=5
TimeoutStartSec=30
# CRITICAL: these two must be false for OmniRoute to write ~/.omniroute/
ProtectSystem=false
ProtectHome=false
PrivateTmp=true

[Install]
WantedBy=default.target
```

### AUR / AppImage variant (`omniroute-bin`)

`omniroute-bin` (AUR) packages the OmniRoute Electron AppImage at `/opt/omniroute-bin/OmniRoute.AppImage` and a 68-byte `/usr/bin/omniroute` wrapper (`exec /opt/omniroute-bin/OmniRoute.AppImage "$@"`). The package ships **no systemd unit** and **no AppArmor/systemd integration**, so you must author your own — and on WSL you must also work around three defects the npm build path does not expose (see Pitfall 8 and `references/or-appimage-wsl-quirks.md`):

```ini
[Unit]
Description=OmniRoute AI Gateway (AppImage)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/po
# Electron app needs a display server; xvfb-run resolves the ozone/x11 crash.
# AppRun locates APPDIR by readlink-ing itself, so we run it from the
# extracted dir, NOT directly (FUSE unavailable on WSL2).
ExecStart=/usr/bin/xvfb-run -a /home/po/squashfs-root/AppRun
Restart=on-failure
RestartSec=5
TimeoutStartSec=30
ProtectSystem=false
ProtectHome=false
PrivateTmp=true

[Install]
WantedBy=default.target
```

To seed the `squashfs-root/` directory:
```bash
cd /home/po                       # AppImage must write somewhere user-writable
/opt/omniroute-bin/OmniRoute.AppImage --appimage-extract
```

## Enabling the MCP server (4 prerequisites)

Default `mcpEnabled: false` and `mcpTransport` unset. External agents (Hermes, Claude Desktop) hitting `/api/mcp/stream` will get `{"error":"MCP server is disabled. Enable it from the Endpoints page."}` until all four are set:

1. **Enable MCP via settings API** (management auth required — login cookie from `/api/auth/login` with the initial admin password from logs):
   ```bash
   curl -X PATCH http://localhost:20128/api/settings \
     -H "Content-Type: application/json" \
     -H "Cookie: auth_token=$COOKIE" \
     -d '{"mcpEnabled":true,"mcpTransport":"streamable-http","a2aEnabled":true}'
   ```
2. **Create a dedicated API key** for the agent (not the admin cookie):
   ```bash
   curl -X POST http://localhost:20128/api/keys \
     -H "Content-Type: application/json" -H "Cookie: auth_token=$COOKIE" \
     -d '{"name":"hermes-mcp","scopes":["admin"]}'
   ```
   → returns `{"key":"sk-XX...YY","id":"..."}`. **`sk-…` value is masked on the wire** (response shape `{"key":"sk-41a4c****37f1",…}`); the `reveal` endpoint is **disabled in v3.8.49** by default (`{"error":"API key reveal is disabled"}`). The full key is shown exactly once, only when the operator clicks "copy" in the Dashboard. CLI/API users cannot recover it. Plan: ask the user to create the key in Dashboard and paste it; do **not** rely on the API as the source of full keys. See `or-compression-config.md` § "API key creation returns masked value". `manage` scope is sufficient for `PUT /api/settings/compression`; only `/api/keys` admin and `/api/auth/login` revocation need `admin`.
3. **The `Authorization: Bearer <key>` header works for both chat completions and MCP** if the key has admin scope. No cookie needed from external clients.
4. **MCP session handshake requires session ID**: first call `initialize` returns `Mcp-Session-Id` response header → pass it as `Mcp-Session-Id` on every subsequent `tools/list` / `tools/call` within the same session. Server returns SSE format (`event: message\ndata: {json}\n\n`).

Verify with `hermes mcp test omniroute` → should show `✓ Connected (~500ms)` and `✓ Tools discovered: 99`.

## Adding OmniRoute as Hermes' model provider

Hermes supports any OpenAI-compatible endpoint via `provider: custom` (NOT `provider: openai` — that errors at startup with `Unknown provider 'openai'`):

```bash
hermes config set model.default "minimax-cn/MiniMax-M3"     # or auto/coding
hermes config set model.provider "custom"
hermes config set model.base_url "http://localhost:20128/v1"
hermes config set model.api_key "sk-..."                       # the OR gateway key from step 2
hermes config set model.context_length 1048576                # match the model's context window
hermes chat -q "test"                                          # verify end-to-end
```

The `auto/*` virtual models (no combo creation needed) make Hermes pick the best model across all providers OR has connected — `auto/coding`, `auto/fast`, `auto/cheap`, `auto/coding:fast`, `auto/reasoning:pro` etc. Validated against `GET /v1/models`; the `combo` owned_by group in that list IS the auto catalog.

## Provider model-id prefix format

Each provider has an `alias` field in `src/shared/constants/providers.ts` (or registry files). The model ID format is `<alias>/<model-id>`:

| Provider | Prefix | Example |
|---|---|---|
| `minimax-cn` (China, Token Plan) | `minimax-cn/` | `minimax-cn/MiniMax-M3` |
| `minimax` (Global) | `minimax/` | — |
| `github` (Copilot OAuth) | `gh/` or `github/` | `github/claude-sonnet-5` |
| `auggie` | `aug/` | `aug/claude-sonnet-4.6` |
| `opencode` (free tier) | `oc/` | `oc/minimax-m3-free` |
| `duckduckgo-web` | `ddgw/` | `ddgw/gpt-5-mini` |
| `theoldllm` | `tllm/` | `tllm/CLAUDE_4_6_OPUS` |
| `veoaifree-web` | `veo-free/` | `veo-free/veo` |
| `mimocode` (Xiaomi) | `mcode/` | `mcode/mimo-auto` |
| `chipotle` | `pepper/` | `pepper/pepper-1` |

To verify what each provider exposes: `curl http://localhost:20128/v1/models -H "Authorization: Bearer $KEY" | python3 -c "import sys,json; d=json.load(sys.stdin); [print(m['owned_by'], m['id']) for m in d['data']]"`.

## Common pitfalls (all observed, all reproducible)

### Pitfall 1: "Installed but every endpoint returns 500"

Banner shows "running" but `/v1/models` and `/api/health` return HTTP 500 with no log error. **Root cause: `ProtectHome=read-only` in systemd unit blocking SQLite writes.** Fix: edit the unit to set `ProtectHome=false ProtectSystem=false`, then `systemctl --user daemon-reload && systemctl --user restart omniroute`. Verify with `stat -c '%y' ~/.omniroute/storage.sqlite` — mtime should advance past the service restart time after the first request.

### Pitfall 2: `npm install` succeeds but `native binary was not found`

PEP 668-like mechanism silently blocked 12 native-binding install scripts (better-sqlite3, sharp, onnxruntime-node, koffi, esbuild, @parcel/watcher, @swc/core, keytar, tls-client-node, core-js, protobufjs, omniroute itself). Re-install with the explicit `--allow-scripts` CSV above. **Applies to ANY npm package using node-gyp** (electron tools, SQLite drivers, ONNX, image-processing CLIs).

### Pitfall 3: MCP endpoint returns "MCP server is disabled"

`mcpEnabled` is false by default. Fix requires PATCH `/api/settings` (not just toggling in UI if API-only). Confirms MCP is exposed: `curl -X POST http://localhost:20128/api/mcp/stream` should return `event: message\ndata: {"result":{"serverInfo":{"name":"omniroute"}}}`, not the disabled error.

### Pitfall 4: Hermes `Unknown provider 'openai'`

`model.provider` is the **dispatcher name**, not the upstream API name. For ANY OpenAI-compatible endpoint (OmniRoute, LiteLLM, vLLM, Ollama, LM Studio), use `provider: custom`. The skill-level fix is in SKILL.md at `## Providers` → add an explicit note. (Bundled skill; cannot edit. Carry the rule in this skill.)

### Pitfall 5: OmniRoute CLI agent detector misses Hermes on Linux/WSL

OmniRoute's `src/lib/cli-helper/tool-detector.ts` uses `getCachedLoginShellPath()` which **returns null on any non-darwin platform** (line 60: `if (platform !== "darwin") return null`). On Linux/WSL, detector only sees systemd's truncated PATH (typically `/usr/local/bin:/usr/bin`), missing `~/.npm-global/bin/` and `~/.local/bin/`. Hermes installs to `~/.local/bin/hermes` (Python venv wrapper). Workaround: symlink to a path in the truncated PATH:
```bash
ln -sf /home/po/.local/bin/hermes /home/po/.npm-global/bin/hermes
```

### Pitfall 6: "OmniRoute detects openclaw but I uninstalled it"

OR detector checks for binary in PATH (not config dir). If you only deleted `~/.openclaw/` config but didn't run `npm uninstall -g openclaw`, the binary is still in `/home/po/.npm-global/bin/` and detector reports "installed". Fix: `npm uninstall -g openclaw`. Detector then returns installed=false.

### Pitfall 7: Token Plan with OmniRoute — cost/billing path

OmniRoute's `minimax-cn` provider hardcodes `https://api.minimaxi.com/anthropic/v1/messages` as the base URL (Anthropic-compatible surface), NOT the `/v1/coding_plan/...` path used by the `mmx` CLI. **The same API key works for both** — Token Plan quota IS consumed when calling through OmniRoute's `minimax-cn/MiniMax-M3` (verified by `x-mm-request-id` response header in the request back to minimaxi.com). If the user wants the dedicated Token Plan endpoint instead, that requires an OmniRoute provider plugin (custom baseUrl).

### Pitfall 8: AUR `omniroute-bin` (AppImage) on WSL — three stacked defects

The AUR package works on native Linux but fails on WSL across three layers; each layer masks the next, so users typically only see `HTTP 500` on `/v1/models` and assume it's a config bug. **All three fixes are needed.**

1. **No systemd unit.** `omniroute-bin` ships only `/usr/bin/omniroute` (AppImage launcher) and `/opt/omniroute-bin/OmniRoute.AppImage`. There is no unit file. An orphan user unit pointing at the old npm path (`/home/po/.npm-global/bin/omniroute`) will silently keep restarting with `status=203/EXEC` ("no such file"). Symptom: `Restart counter is at N`, port 20128 never opens.

2. **FUSE unavailable in WSL2 kernel.** Running `/opt/omniroute-bin/OmniRoute.AppImage` directly fails: `Cannot mount AppImage, please check your FUSE setup`. WSL2's kernel is sealed/signed-readonly; userspace `apt install fuse` only gives userspace helpers, not `fuse.ko`. AppImage itself has a fallback: `AppImage --appimage-extract` writes `squashfs-root/` to cwd and exits. Then point systemd at `<extracted>/AppRun`.

3. **Electron ozone/x11 crash under systemd.** Even after extraction, `./AppRun` runs Electron directly. Without `$DISPLAY`, Chromium-ozone dies: `Missing X server or $DISPLAY` → `The platform failed to initialize. Exiting` → SIGSEGV. systemd user manager does not export `$DISPLAY`. Wrap with `xvfb-run -a`: it spawns a background `Xvfb :99` and provides `$DISPLAY=:99` to AppRun. xvfb-run is normally already installed (`/usr/bin/xvfb-run`).

After wrapping with xvfb-run, OmniRoute starts and binds 20128 — but **a fourth issue then surfaces**:

4. **SQLite driver availability on AppImage.** The npm install chain populates `better-sqlite3` native binary via `--allow-scripts`. The AUR/AppImage build skips that, the embedded Electron Node is **22.2.10** (≤22.4), so `node:sqlite` (≥22.5 stdlib) is also unavailable. Only sql.js WASM remains, and its lazy `warmUpRuntimes()` may not finish before the first HTTP request lands, yielding `[DB] Nenhum driver SQLite disponível ... sql.js WASM ainda não foi pré-inicializado` on every `/v1/*` call. This is a packaging defect in `omniroute-bin`, not a misconfiguration. The recommended fix is to revert to the npm install path on WSL; the AUR/AppImage install should be considered unsupportable on WSL2 until upstream bundles a portable SQLite layer.

**Decision matrix:**

| Choice | SQL guaranteed? | WSL2 cost | Recommended for |
|---|---|---|---|
| `npm i -g omniroute --allow-scripts=...` | ✅ bundled better-sqlite3 | low | **Yes — default** |
| `yay -S omniroute-bin` + AppImage + xvfb | ⚠️ only sql.js, may 500 | medium | Native Arch on bare metal |
| Docker | ✅ | low | Hermetic / cross-machine |
| Source build (`git clone && npm i`) | ✅ | high | Customization / patch dev |

Bottom line: **on WSL stay on the npm install path.** The AUR/AppImage install is not viable there without upstream changes.

→ Full reproduction transcript + exact logs at `references/or-appimage-wsl-quirks.md`.

## The MCP tool catalog (99 tools)

`hermes mcp test omniroute` should report 99 tools. The notable ones for agent automation:

- `omniroute_get_health` — uptime, memory, circuit breakers, cache stats
- `omniroute_list_combos` — all configured combos
- `omniroute_route_request` — send a chat completion through OR routing
- `omniroute_simulate_route` — predict routing without firing request
- `omniroute_check_quota` — remaining quota per provider
- `omniroute_cost_report` — cost by period (session/day/week/month)
- `omniroute_list_models_catalog` — all available models
- `omniroute_set_routing_strategy` — change routing strategy at runtime
- `omniroute_set_resilience_profile` — aggressive/balanced/conservative
- `omniroute_set_budget_guard` — USD cap per session
- `omniroute_test_combo` — live-fire all providers in a combo
- `omniroute_compression_status` — RTK/Caveman engine state
- `omniroute_cache_stats` — semantic + prompt cache hit rate
- `omniroute_sync_pricing` — refresh pricing from LiteLLM
- `omniroute_db_health_check` — repair broken combo references
- `omniroute_pick_fastest_model` — best latency combo across providers
- `omniroute_set_compression_engine` — switch RTK/Caveman/Lite/stacked/etc.
- `omniroute_agent_skills_list` / `_get` / `_coverage` — 42 SKILL.md catalog
- `omniroute_web_search` / `omniroute_web_fetch` — web gateway tools
- `omniroute_oneproxy_*` — proxy pool management
- `omniroute_omniroute_skills_*` — agent skills discovery

Plus per-feature clusters: memory, eval, a2a, gamification, webhooks.

## Auto-routing via `auto/*` model IDs

OmniRoute's 12-factor scoring (`health` 0.20, `quota` 0.15, `costInv` 0.15, `latencyInv` 0.12, `taskFit` 0.08, etc.) means Tier 1 subscription (cost = 0) wins over Tier 2 API key over Tier 3 free. With Token Plan minimax-cn connected, `auto/coding` defaults to M3. Pre-defined weight profiles override: `X-OmniRoute-Mode: fast|cheap|quality|reliable|offline`.

Per-request controls:
```bash
curl -X POST http://localhost:20128/v1/chat/completions \
  -H "X-OmniRoute-Mode: fast" \
  -H "X-OmniRoute-Budget: 0.05" \
  -H "X-OmniRoute-Budget-Fallback: strict" \
  -d '{"model":"auto",...}'
```

## Compression — what configures what

Compression has **two orthogonal persist surfaces**; setting either alone gives a half-configured pipeline. See `references/or-compression-config.md` for the full three-surface table.

| Surface | Persists via | What it writes |
|---|---|---|
| Engine pipeline (which engines + intensities) | MCP `omniroute_set_compression_engine`, or in the `PUT /api/settings/compression` body | `stackedPipeline`, `engines.*.enabled`, `rtkConfig`, `cavemanConfig` |
| Trigger layer (when, how much, hard guards) | MCP `omniroute_compression_configure`, or in the `PUT /api/settings/compression` body | `defaultMode`, `autoTriggerMode`, `autoTriggerTokens`, `strategy`, `targetRatio`, `preserveSystemPrompt`, `languageConfig` |

**Rule of thumb**: call engine first (decides WHAT pipeline runs), then trigger (decides WHEN + HOW MUCH). Doing only one yields half-configured compression that may or may not fire.

`PATCH /api/settings` (i.e. the root settings endpoint) accepts the body, returns 200, and **silently drops** every compression-namespace key — including `languageConfig`. That's why dashboard toggles survive a refresh but PATCH scripts have no effect. Real entrypoint is `PUT /api/settings/compression` (Zod-validated schema `compressionSettingsUpdateSchema`).

`MCP omniroute_compression_status` returns the **trigger** state but **not** `languageConfig`. To see / change `languageConfig` you must use `GET/PUT /api/settings/compression`.

**Language packs** in v3.8.49: `["en","zh","pt-BR","es","de","fr","ja","id"]` (8 installed). The wiki `Compression-Language-Packs` page lists only 6 — outdated; `zh` (16 rules) and `id` exist but are missing from the docs. To enable:
```bash
curl -X PUT http://localhost:20128/api/settings/compression \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"languageConfig":{"enabled":true,"enabledPacks":["en","zh"],"defaultLanguage":"zh","autoDetect":true}}'
```

## How much context do OmniRoute skills cost?

When a system prompt enumerates external SKILL.md directories (e.g. `~/.hermes/skills/devops/omniroute-agents/` containing all 44 OR agent-skill files), Hermes's loader (`agent/prompt_builder.py:1514 build_skills_system_prompt`) parses the YAML **frontmatter** of each one and emits exactly one index line per skill:

```text
- omni-inference: The core OpenAI-compatible inference endpoints: chat completions, embeddings, …
```

It does **not** emit the SKILL.md body. The body is only loaded when the model explicitly calls `skill_view(name='omni-inference')`. So the 44 SKILL.md files (avg ~10 KB body each) cost roughly **2 K tokens / 8.5 KB** in the system prompt — average description length is ~172 chars. This is small enough to install them all at once (option `B` is acceptable) rather than cherry-picking. Confirmed by frontmatter scan, not estimated.

→ If the model **needs full skill prose**, ask it to call `skill_view(name='omni-inference')` first rather than guessing from the description line.

## Verifying end-to-end

```bash
# Service alive
curl -sS -o /dev/null -w "%{http_code}\n" http://localhost:20128/v1/models    # → 200

# Provider active
curl -sS -X POST http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer $KEY" \
  -d '{"model":"minimax-cn/MiniMax-M3","messages":[{"role":"user","content":"1+1"}],"max_tokens":10}'
# → 200 with x-mm-request-id header (proves minimaxi.com was called)

# MCP for external agents
hermes mcp test omniroute
# → ✓ Connected + ✓ Tools discovered: 99

# Auto routing
curl -sS -X POST http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer $KEY" \
  -d '{"model":"auto/coding","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
# → 200, model field shows which provider won
```

## See also

- Bundled `hermes-agent` skill — Hermes configuration, MCP server commands, providers
- `references/or-provider-prefix-table.md` — verified alias/model-id mapping for OR 3.8.x
- `references/or-mcp-curl-smoke.sh` — reproducible smoke test for MCP enable + 99-tool discovery
- `references/or-appimage-wsl-quirks.md` — full transcript of the 4-layer failure chain when running `omniroute-bin` on WSL2 (FUSE → xvfb → SQLite) and why the npm path is the only stable one
- `references/or-compression-config.md` — the three persistence surfaces (`PATCH /api/settings` vs `PUT /api/settings/compression` vs MCP `compression_configure`), the 8 actually-installed language packs (incl. `zh`/`id`, not 6 like the wiki claims), the verified "standard" recipe, and the API key reveal gotcha"