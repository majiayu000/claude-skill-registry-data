---
name: solar-browser
description: >
  Provide a shared browser runtime for Solar: Chrome with remote debugging,
  optional ensure/check scripts, and safe cleanup of leaked DevTools MCP helper
  processes. MCP clients use npx chrome-devtools-mcp with --browserUrl; Chrome
  is started with ensure_browser.sh --start and released with --stop (or --stop --force), not when an IDE opens.
---

# Solar Browser

## Purpose

Provide one reusable browser runtime layer for Solar:

- **Chrome on demand:** `ensure_browser.sh` (default) only checks the debug port and trims MCP helpers — it **does not** open Chrome. Use `ensure_browser.sh --start` immediately before browser MCP work; use `ensure_browser.sh --stop` when that browser workflow is finished (or `--stop --force` only for controlled override; see root `AGENTS.md`).
- Expose a stable `--remote-debugging-port` / `browserUrl` for `chrome-devtools-mcp`.
- Trim leaked `chrome-devtools-mcp` helper processes defensively.

## Scope

- Shared local Chrome with `--remote-debugging-port` and a dedicated profile directory.
- Safe detection and cleanup of stale DevTools MCP helper processes.
- No browser automation logic for WhatsApp, Zoho, LinkedIn, etc. Those stay in their own skills.

## Required MCP

None (this skill does not register MCP servers; it prepares **local Chrome** that `chrome-devtools-mcp` attaches to.)

## Contract for other skills (low token cost)

Domain skills (WhatsApp, Zoho, LinkedIn, etc.) should **not** embed MCP client snippets (`mcp.json`, `config.toml`, etc.). They only need a short prerequisite line, for example:

- **Requires:** `chrome-devtools` MCP (or equivalent) and a debuggable Chrome at `http://${SOLAR_BROWSER_DEBUG_HOST:-127.0.0.1}:${SOLAR_BROWSER_DEBUG_PORT:-9222}`.

Operators run `onboard_browser_env.sh`, `check_browser.sh`, and `ensure_browser.sh` / `--start` / `--stop` here when they need the shared browser.

## Validation commands

```bash
# Validate skill structure
python3 core/skills/solar-skill-creator/scripts/package_skill.py core/skills/solar-browser /tmp

# Shell checks
bash -n core/skills/solar-browser/scripts/onboard_browser_env.sh
bash -n core/skills/solar-browser/scripts/ensure_browser.sh
bash -n core/skills/solar-browser/scripts/check_browser.sh
bash -n core/skills/solar-browser/scripts/validate_mcp.sh

# Sync core changes to local clients
solar client sync
```

## Runtime configuration

This skill manages a compact `.env` block:

```bash
bash core/skills/solar-browser/scripts/onboard_browser_env.sh
```

Block format:

```dotenv
# [solar-browser] required environment
SOLAR_BROWSER_DEBUG_HOST=127.0.0.1
SOLAR_BROWSER_DEBUG_PORT=9222
SOLAR_BROWSER_PROFILE_DIR=/tmp/com.solar.browser-profile
SOLAR_BROWSER_LOG_PATH=/tmp/com.solar.browser.log
SOLAR_BROWSER_MCP_LEAK_THRESHOLD=3
```

Optional:

```dotenv
SOLAR_BROWSER_BINARY=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
```

## Host MCP wiring (canonical)

Configure each AI host’s **`chrome-devtools`** MCP server as **`npx`** with args:

`-y`, `chrome-devtools-mcp@latest`, `--browserUrl`, `http://<SOLAR_BROWSER_DEBUG_HOST>:<SOLAR_BROWSER_DEBUG_PORT>` (defaults `http://127.0.0.1:9222`).

**Do not** use a wrapper that calls `ensure_browser.sh` from the MCP server command: that tends to open Chrome whenever the IDE starts the MCP process.

Drift check (read-only; compares `~/.codex`, `~/.claude.json`, `~/.cursor/mcp.json`, `~/.gemini` to repo `.env`):

```bash
bash core/skills/solar-browser/scripts/validate_mcp.sh
bash core/skills/solar-browser/scripts/validate_mcp.sh --all-clients
```

## Lifecycle (mental model)

```
Operator runs ensure_browser.sh --start  →  Chrome up with remote debugging (only when chosen)
ensure_browser.sh (no flag)  →  never opens Chrome; exits 0 if port healthy, else 1 with a hint
IDE / CLI starts MCP (npx … --browserUrl)  →  attaches only; does not own Chrome lifecycle
Operator or agent runs ensure_browser.sh --stop  →  exits only when no other active MCP clients are detected (safe default allows current session)
Operator or agent runs ensure_browser.sh --stop --force  →  forced teardown for this profile+port
Operator closes Chrome manually  →  same outcome; MCP reconnects fail until --start again
```

## Workflow (manual setup or diagnostics)

1. Bootstrap env block (when `.env` needs the `[solar-browser]` section):
   - `bash core/skills/solar-browser/scripts/onboard_browser_env.sh`
2. Check health:
   - `bash core/skills/solar-browser/scripts/check_browser.sh`
3. If not healthy (or right before browser MCP work), start Chrome:
   - `bash core/skills/solar-browser/scripts/ensure_browser.sh --start`
4. When finished with browser MCP for that workflow, stop Chrome:
   - `bash core/skills/solar-browser/scripts/ensure_browser.sh --stop`
   - If a controlled override is required (e.g. stale clients): `bash core/skills/solar-browser/scripts/ensure_browser.sh --stop --force`
5. Optional — trim / verify without launching (exits 1 if Chrome is down):
   - `bash core/skills/solar-browser/scripts/ensure_browser.sh`
6. Optional — drift check for host MCP configs:
   - `bash core/skills/solar-browser/scripts/validate_mcp.sh` (add `--all-clients` to audit every known path)

## Design notes

- `solar-system` does **not** orchestrate the browser. Nothing in the LaunchAgent “feature tick” starts Chrome.
- **Concurrent control:** multiple `chrome-devtools-mcp` processes may attach to the same `browserUrl`; this skill does **not** auto-shutdown Chrome when the last MCP exits (use `ensure_browser.sh --stop` or root `AGENTS.md` agent rules). Prefer **one active controlling session at a time** per profile — parallel CDP control is undefined and risky. Process count `2+` is a **soft signal** (overlap or stale helpers), not a hard leak proof.
- Health semantics with shared `browserUrl`:
  - `0-1` DevTools MCP helper processes is normal.
  - `2+` helper processes is degraded and usually means overlap or stale sessions.
  - `SOLAR_BROWSER_MCP_LEAK_THRESHOLD` is only a cleanup guardrail in `ensure_browser.sh`, not the normal expected count.
