---
name: qa-preflight
section: pipeline
description: "Verifies the minimum environment needed to run the audit. Skips checks that don't apply to the chosen browser bridge."
model: haiku
---

# qa-preflight

## Overview

Verifies the environment **only for things the run actually needs**. Detects which browser bridge is active (MCP vs Bash fallback) and skips irrelevant checks. Skips ADO/jq checks entirely when `dry_run = true`.

## Decision tree

Run Check 0 first (fast fail-fast). Then Check 1 with auto-install. The rest depend on the bridge mode resolved by Check 1.

### Check 0 — URL health (ALWAYS, fail-fast)

Per `customize.toml → resilience.preflight_url_health = true` (default), send a HEAD request to every `apps[].baseUrl` with a 5-second timeout BEFORE any LLM cost is incurred. This prevents 9-minute hangs on unreachable targets.

```bash
curl -sf -I --max-time 5 "<BASE_URL>" -o /dev/null
```

| Result | Action |
|---|---|
| 200 / 301 / 302 / 401 / 403 / 404 | ✓ pass (target is responsive, even if auth-gated) |
| 000 (connection refused / DNS failure) | ✗ HARD STOP: `"Target {baseUrl} not reachable. Check network or baseUrl in automation.config.json."` |
| 5xx | ✗ HARD STOP: `"Target {baseUrl} returned 5xx. The app may be down. Try again later."` |
| Timeout (> 5s) | ✗ HARD STOP: `"Target {baseUrl} timed out after 5s. Target unreachable."` |

This is the single cheapest way to avoid wasting tokens on a dead target.

### Check 1 — Browser bridge detection + AUTO-INSTALL (ALWAYS)

Look for Playwright MCP tools registered in this Claude Code session:
- If `browser_navigate` (or any `mcp__playwright__*` tool) is available → **MCP mode** → skip to Check 3
- Otherwise → **MCP missing — AUTO-INSTALL inline (do NOT fall through silently)**

#### Auto-install sequence (when MCP not detected)

The orchestrator MUST attempt to install MCP automatically. This is the highest-impact UX fix because most new users won't know they need to install MCP separately.

Log:
```
⚠ Playwright MCP not detected — auto-installing (one-time, ~90 seconds)...
```

Run these three commands in sequence via Bash tool. Each must succeed before the next runs:

```bash
# 1. Install Playwright MCP globally (~30s)
npm install -g @playwright/mcp@latest

# 2. Install browser binaries Playwright will drive (~60s)
npx playwright install chromium firefox webkit

# 3. Register MCP with Claude Code (instant)
claude mcp add playwright -- npx "@playwright/mcp@latest"
```

**After successful install:**

Claude Code does NOT hot-load new MCP servers — they are picked up only at session start. So the orchestrator HARD STOPs with a clear restart message:

```
═══════════════════════════════════════════════════════════════
 ✓ Playwright MCP installed successfully
═══════════════════════════════════════════════════════════════

 The MCP server is registered, but Claude Code only loads MCP
 servers at startup. To complete setup:

   1. Close Claude Code completely (Cmd+Q / Alt+F4)
   2. Reopen Claude Code
   3. Re-run your audit command (e.g. "audit my-app")

 This is a one-time step. After restart, future audits skip
 installation entirely.
═══════════════════════════════════════════════════════════════
```

This is a friendly hard-stop, not an error — the user understands they're 60 seconds away from a working audit.

**If any install command fails:**

| Failure | Action |
|---|---|
| `npm install` fails (no npm, no network, permission denied) | Log error, suggest `sudo npm install -g @playwright/mcp@latest` on Linux/Mac OR running as Administrator on Windows, then HARD STOP |
| `npx playwright install` fails (disk space, network) | Log error with exact stderr, HARD STOP with "Free disk space or check network, then run `npx playwright install chromium firefox webkit` manually" |
| `claude mcp add` fails (Claude Code CLI not in PATH) | Log error, suggest `claude` is not in PATH, HARD STOP with manual install instructions |
| Any error | Fall through to Bash fallback path (Check 2). MCP install failure is non-fatal IF local Playwright is available. |

#### Skipping auto-install

If the user explicitly does not want MCP (rare), pass `--bash-fallback` to skip Check 1's auto-install and force Bash mode. The orchestrator then requires Check 2 to pass.

Log the resolved bridge:
```
✓ Browser bridge: MCP active                  (recommended, cheap path)
```
or
```
⚠ Browser bridge: Bash fallback               (works, slightly more tokens)
   To upgrade later: npm install -g @playwright/mcp@latest && claude mcp add playwright -- npx "@playwright/mcp@latest"
```

### Check 1.5 — Generate `.mcp.json` to match (browsers × viewports), then verify readiness

Parallelism is one browser per (engine × viewport). The `.mcp.json` server pool must therefore equal `resolvedConfig.browsers × resolvedConfig.viewports[].class`. This check keeps them in sync — so when the user changes browsers or viewports, the pool follows.

**1. Compute the required server set** (`serverFor(engine, vp)` from qa-argus Step 5.0: chromium-desktop = `playwright`, else `pw-{engine}-{vp}`):
```
required = {}    // serverName -> engine
for engine in resolvedConfig.browsers:
  for vp in resolvedConfig.viewports.map(v => v.class):
    required[serverFor(engine, vp)] = engine
```

**2. Compare to the current `{project-root}/.mcp.json`.** If the set of server names differs:
- Write `.mcp.json` with exactly those servers (Write tool — it is a data file, NOT a script). Each entry:
  `"<name>": { "command": "npx", "args": ["@playwright/mcp@latest", "--isolated", "--browser", "<engine>"] }`
  (add `"--headless"` to args when `[parallelism].headed = false`).

  **Device emulation (named devices):** For each viewport that has a `name` but NO explicit `width`/`height` in `automation.config.json`, the viewport is a named Playwright device (e.g. "iPhone 12", "iPad Air"). Add `"--device", "<viewport.name>"` to that server's args so Playwright sets the correct UA, touch support, pixel ratio, and viewport size automatically:
  ```
  // viewport has name only (no width/height) → device emulation
  args: ["@playwright/mcp@latest", "--isolated", "--browser", "<engine>", "--device", "<viewport.name>"]

  // viewport has explicit width+height → plain browser, worker calls browser_resize
  args: ["@playwright/mcp@latest", "--isolated", "--browser", "<engine>"]
  ```
  This is what makes mobile audits use a real iPhone UA and touch model instead of a desktop browser resized to 390px.
- Then HARD STOP with a restart message (MCP servers load only at startup):
  ```
  🔁 Browser pool updated for your selection ({browsers} × {viewports} = {N} browsers).
     Fully restart Claude Code, then re-run the audit — the {N} browser windows will open.
  ```

**3. If `.mcp.json` already matches**, verify each required server actually connected (its `mcp__{server}__browser_navigate` tool exists):
```
for (server, engine) in required:
  if mcp__{server}__browser_navigate NOT registered:
    WARN (do NOT hard stop):
      "⚠ {server} ({engine}) not connected — run `npx playwright install {engine}` then restart.
       Its cells will be reported as degraded (Step 5.9), never silently dropped."
```
Log: `✓ Browser pool: {browsers} × {viewports} = {N} dedicated browsers, all connected`.

firefox/webkit browser binaries are installed by `install.bat` / `npx playwright install`; a bare `/plugin install` gives chromium only — preflight will tell the user exactly what to install.

### Check 2 — Local Node (ALWAYS runs, MCP or Bash mode)

The plugin's permanent scripts (`scripts/annotate-cell-prepare.cjs`, `scripts/annotate-cell-finalize.cjs`, `scripts/file-bugs.cjs`, etc.) are **pure Node, no external npm deps**. They run on the Node runtime alone.

```bash
node --version          # must be >= 18
```
If Node missing or < 18 → HARD STOP: "Install Node.js >= 18 from https://nodejs.org and re-run."

That's it. **No `npm install` required for the main audit flow.** Annotation is MCP-driven (HTML built by Node script, rendered by MCP's browser, JSONL updated by Node script). ADO bug filing uses only Node built-ins (https, fs, path).

#### Check 2.5 — node_modules (ONLY for Bash fallback mode + recovery tools)

Skip this section in MCP mode unless the user is invoking `scripts/repair-bugs.cjs` (recovery tool — re-files bugs from a prior audit).

When needed, verify:
```bash
test -d "{project-root}/node_modules" && test -d "{project-root}/node_modules/@playwright/test"
```
If missing → **AUTO-INSTALL inline**:
```
⚠ node_modules missing — auto-installing (one-time, ~60 seconds)...
```
```bash
cd "{project-root}" && npm install
```
If `npm install` fails:
- Log the exact stderr (first 500 chars)
- In MCP mode: log warning and continue (main audit flow doesn't need it).
- In Bash fallback mode: HARD STOP: "npm install failed. Check network and `package.json` integrity, then run `npm install` manually in {project-root}."

Final Bash-mode verification:
```bash
npx playwright --version
```
Should print the Playwright version. If missing browser binaries:
```bash
npx playwright install chromium firefox webkit
```

### Check 3 — Server reachability (ALWAYS)

```bash
curl -sf -o /dev/null -w "%{http_code}" <BASE_URL>
```
Accept: 200, 302, 401, 403, 404. Reject: 000 (unreachable), 5xx. Critical.

### Check 4 — Secrets gitignored (ALWAYS, security)

If `{project-root}/.claude/secrets.json` exists, verify it's listed in `.gitignore`:
```bash
git -C "{project-root}" check-ignore -q .claude/secrets.json
```
If file exists but is NOT gitignored, append `.claude/secrets.json` to `.gitignore` and warn the user. Critical only if write fails.

### Check 5 — jq (CONDITIONAL)

**Skip when `dry_run = true`** in customize.toml. jq is only used by `scripts/ado-api.sh` for filing real ADO bugs.

When `dry_run = false`:
```bash
jq --version
```
Critical: jq is required for ADO bug filing.

### Check 6 — ADO PAT (CONDITIONAL)

**Skip when `dry_run = true`.**

When `dry_run = false`:
1. Read PAT from `{project-root}/.claude/secrets.json → AZURE_DEVOPS_PAT`, or env `AZURE_DEVOPS_PAT`.
2. If found, verify with:
   ```
   GET https://dev.azure.com/{ADO_ORG}/_apis/projects/{ADO_PROJECT}?api-version=7.1
   Authorization: Basic base64(:<PAT>)
   ```
   200 → pass. 401/403 → warn (invalid PAT or missing `Work Items: Read & Write` scope). Not found → warn (user will be prompted at Step 1.5).
3. Non-critical: PAT issues prevent bug filing but do not block the audit.

### Check 7 — Auth credentials (SKIPPED in preflight)

Login validation now happens during route discovery (Step 3) where the browser bridge is already active. Preflight does not start a browser just to verify login.

## Output

```
═══════════════════════════════════════════════════════
 🔍 Preflight checks
═══════════════════════════════════════════════════════
 ✓ URL health: 200 https://ui-dev.undertakings.dobusiness.dev (resilience.preflight_url_health)
 ✓ Browser bridge: MCP active
 ⊝ Node + Playwright + node_modules: skipped (MCP mode)
 ✓ Server: 200 https://ui-dev.undertakings.dobusiness.dev
 ✓ Secrets: .claude/secrets.json is gitignored
 ⊝ jq: skipped (dry_run = true)
 ⊝ ADO PAT: skipped (dry_run = true)
═══════════════════════════════════════════════════════
```

On a fresh-machine first run where MCP is auto-installed:

```
═══════════════════════════════════════════════════════
 🔍 Preflight checks
═══════════════════════════════════════════════════════
 ✓ URL health: 200 https://ui-dev.undertakings.dobusiness.dev
 ⚠ Playwright MCP not detected — auto-installing (one-time, ~90s)...
   ✓ npm install -g @playwright/mcp@latest
   ✓ npx playwright install chromium firefox webkit
   ✓ claude mcp add playwright -- npx @playwright/mcp@latest
 ⏸ Restart Claude Code to load MCP, then re-run your audit
═══════════════════════════════════════════════════════
```

Symbols:
- `✓` pass
- `✗` critical failure
- `⚠` warning or auto-install starting
- `⊝` skipped (not needed for this run's config)
- `⏸` paused, awaiting user action (e.g. restart Claude Code)

## Return behaviour

| Outcome | Action |
|---|---|
| All critical checks pass | Return success; audit proceeds |
| Any critical check fails | Set `PREFLIGHT_FAILED=true`; halt audit; report which check failed |
| Only warnings | Return success with warnings; audit proceeds in degraded mode |

## What this skill explicitly does NOT check anymore

These were in the old preflight and have been removed:
- **Local Playwright in MCP mode** — MCP server runs its own Playwright; local install is unused
- **Local Playwright browser binaries in MCP mode** — MCP downloads its own browsers
- **jq when `dry_run = true`** — jq is only used for ADO bug filing
- **ADO PAT when `dry_run = true`** — never going to file bugs, no point
- **Auth credentials in preflight** — login validation moved to route discovery (Step 3) where the browser is already running

## What this skill explicitly DOES now (added 2026-06-02)

- **Pre-flight URL health (Check 0)** — HEAD baseUrl with 5s timeout BEFORE any LLM cost; per `resilience.preflight_url_health`
- **Auto-install Playwright MCP** — when MCP not detected, runs `npm install -g @playwright/mcp@latest` + `npx playwright install ...` + `claude mcp add playwright -- npx "@playwright/mcp@latest"` then asks user to restart Claude Code
- **Auto-install node_modules** — when in Bash fallback mode and `node_modules/` missing, runs `npm install` in the project root before failing
- **Auto-install browser binaries** — when `npx playwright --version` fails on the binaries side, runs `npx playwright install chromium firefox webkit`

These three auto-install paths are the single biggest UX fix for a new user — `/plugin install` does not run shell scripts, so without these automatic preflight installs, every new user would hit a "Browser bridge unavailable" hard stop on their first audit. The auto-install path makes the first-audit-out-of-the-box flow possible.
