---
name: chrome-browser
description: Use when setting up a dedicated Chrome browser for Playwright MCP with session persistence, or when encountering Cloudflare challenges during browser automation. Covers CDP setup, launchd auto-start, and persistent login sessions.
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: "1.6.0"
---

# Dedicated Chrome Browser

A dedicated headed Chrome for Testing (CfT) instance with CDP for Playwright MCP. Persistent profile (cookies/logins survive restarts), launchd-managed, multi-session safe. Distinct "TEST" badge icon in the Dock.

## Why

- Chrome's single-instance lock prevents CDP when the default profile is in use — **dedicated user-data-dir required**
- Chrome for Testing has its own `CFBundleIdentifier` — shows as a **separate app** in Dock/Cmd+Tab with a distinctive icon
- Headed so the user can log into sites manually; Playwright shares the session
- launchd auto-starts on login, restarts on crash

## Tool Selection

This skill drives Chrome **only** through Playwright MCP attached to `127.0.0.1:9222`.

**Do NOT use these lookalike MCPs even if they are loaded in the session:**

- `mcp__chrome-devtools__*` — different MCP. Using it mixes tool surfaces and breaks the single-source-of-truth model this skill relies on. Typical failure: agent silently switches MCPs after a transient Playwright error and continues against an unrelated browser context.
- `mcp__claude-in-chrome__*` — **deprecated predecessor; this skill replaces it.** If it shows up loaded somewhere, the config is stale — ignore it and use Playwright against `127.0.0.1:9222`.

If Playwright MCP isn't loaded, **stop and tell the user** — do not silently switch to a sibling MCP, and do not drive the browser via raw `curl`/CDP-WebSocket (see "Working with pages").

The Playwright MCP tools may be exposed under either namespace depending on how it was installed:

- `mcp__playwright__browser_*` — when added via `claude mcp add playwright …` (the INSTALL.md flow).
- `mcp__plugin_<plugin>_playwright__browser_*` — when loaded as part of a Claude Code plugin.

Either is fine; both attach to the same `127.0.0.1:9222` CDP. The preflight below checks whichever variant is present.

## On activation

Before the first browser action in a session, run a 2-check preflight:

1. **Browser ready:** `chrome-cdp-health` (exit 0). On exit 1 → CDP unreachable, run `launch-chrome-cdp`. On exit 2 → endpoint reachable but `webSocketDebuggerUrl` is not local; the Playwright MCP `--cdp-endpoint` is misconfigured.
2. **Playwright MCP loaded:** at least one `mcp__*playwright*__browser_*` tool is available (either `mcp__playwright__*` or the plugin-namespaced `mcp__plugin_<plugin>_playwright__*`). If neither is present, stop and tell the user — see Tool Selection.

If either check fails, stop and surface the issue. Do not improvise an alternative.

## Architecture

```
Chrome for Testing (CfT, ~/.local/Applications/)
  └── CDP on port 9222 + ergonomic flags
      └── ~/.cache/chrome-cdp-profile (persistent, isolated from daily Chrome)
          ├── Claude session 1 → Playwright MCP → CDP
          ├── Claude session 2 → Playwright MCP → CDP
          └── User can log into sites manually (headed)
```

## Quick Reference

```bash
# Health / inspect / restart helpers (~/.local/bin/, installed by install-cft.sh)
chrome-cdp-health         # exit 0 alive, 1 unreachable, 2 endpoint wrong host
chrome-cdp-tabs           # list open tabs — read-only
chrome-cdp-restart        # kickstart launchd-managed Chrome (use when CDP hangs)

# Configure Playwright MCP (user-scope, one-time)
claude mcp add -s user playwright -- npx @playwright/mcp --cdp-endpoint http://127.0.0.1:9222

# Start / ensure Chrome CDP is running (one-shot, idempotent)
launch-chrome-cdp                                    # ~/.local/bin/launch-chrome-cdp

# Install / update Chrome for Testing (also (re)creates the helper symlinks)
${CLAUDE_SKILL_DIR}/scripts/install-cft.sh          # latest stable
${CLAUDE_SKILL_DIR}/scripts/install-cft.sh 147      # specific milestone
```

### Finding the scripts when `${CLAUDE_SKILL_DIR}` isn't set

Cold sessions or one-shot bash calls may not have `${CLAUDE_SKILL_DIR}`. After `install-cft.sh` has run once, the canonical entry point is on `$PATH`:

```bash
launch-chrome-cdp     # symlink in ~/.local/bin → skills/chrome-browser/scripts/launch-chrome-cdp.sh
```

If that's missing, locate the skill directory directly. **Do NOT guess** paths like `~/.cache/launch-chrome-cdp.sh`, and **do NOT fall back** to launching `/Applications/Google Chrome.app` manually — you'd bypass Chrome for Testing and the curated flag set:

```bash
SKILL_DIR="$(dirname "$(find ~/.claude/skills ~/.claude/plugins ~/CODE \
  -path '*/chrome-browser/scripts/launch-chrome-cdp.sh' 2>/dev/null | head -1)")"
"${SKILL_DIR}/launch-chrome-cdp.sh"
```

## Using the browser via Playwright MCP

- **Inspect and close tabs:** use the `browser_tabs` tool (no action = list; `close` action = close). Playwright `page.close()` does NOT work over CDP — it fails silently.
- **One tab at a time:** close each tab when done. If 10+ tabs accumulate, close all and start fresh.
- **Sequential, not parallel:** browser tool calls in parallel race the same Chrome instance. Wait for the previous call to settle before issuing the next.
- **Verify you're talking to the local CDP:** run `chrome-cdp-health`. Exit 0 = alive on `127.0.0.1:9222`; exit 2 = endpoint reachable but `webSocketDebuggerUrl` points elsewhere (the MCP `--cdp-endpoint` is pointed at a remote host — fix it before doing anything else).
- **Never drive the browser via raw HTTP/WebSocket against `:9222/json/*`.** Those endpoints are for diagnostics only. For read-only inspection use `chrome-cdp-tabs` or `chrome-cdp-health`. Tab manipulation, navigation, snapshots, and any action go through Playwright MCP — direct CDP calls bypass Playwright's state tracking and break subsequent MCP calls.

### When Playwright MCP errors but CDP is alive

If `mcp__playwright__browser_*` errors but `chrome-cdp-health` returns 0, CDP is healthy and Playwright is the problem. Restart launchd-managed Chrome and retry the same Playwright call:

```bash
chrome-cdp-restart
```

**Never** switch to `mcp__chrome-devtools__*` or `mcp__claude-in-chrome__*` as a workaround. The fix is always to restore CDP, not to change MCPs. If CDP itself is dead, see Troubleshooting → "CDP unreachable" below.

## Working with pages

- **React / SPA text extraction:** use `innerText`, not `textContent`. React's virtual DOM may leave text nodes empty while `innerText` reflects rendered visual output.
- **Batch crawling:** `page.goto()` works inside `browser_run_code` for multi-page work without an MCP round-trip per page. Add 1–2 s between navigations to avoid rate limiting.
- **No filesystem inside `browser_run_code`:** `require('fs')` is unavailable in the Playwright MCP sandbox. Return data as the function's return value, or POST it to a local HTTP server.
- **Cloudflare:** if a site shows a challenge / waiting page, just wait — the browser MCP usually handles it. Real blocks are rare. Don't retry in a tight loop, and don't open a second tab to the same site.
- **Rate limits:** sites like Galaxus / Digitec block after ~100+ rapid requests. Crawl slowly (1–2 s/page); expect a ~5 min cool-off after a block.

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Chrome for Testing | Distinct Dock icon ("TEST" badge), own `CFBundleIdentifier`, no auto-update surprises — but see "CfT behind stable" below: not auto-updating is also how it drifts into a fingerprint bot detection rejects. The launcher now picks stable automatically when CfT is a major version behind. |
| `~/.local/Applications/` install path | User-writable, stable path independent of puppeteer cache |
| Isolated profile (`~/.cache/chrome-cdp-profile`) | Avoids single-instance lock, doesn't interfere with daily browsing |
| Headed (not headless) | User can log into sites manually, cookies persist for automation |
| launchd KeepAlive on crash only | Restart on crash, but intentional quit stays quit |
| `--no-first-run --no-default-browser-check` | Zero-friction automated sessions |
| `--disable-infobars` + UI suppression flags | Suppress infobars, search engine choice, hang monitor, popup blocking, form repost dialogs |
| `--disable-features=Translate,...` | Disable translation, password check, autofill, media routing, AI mode, tab organization, optimization hints |
| `--password-store=basic --use-mock-keychain` | Bypass macOS keychain — no unlock prompts during automation |
| Background reduction flags | Disable background networking, phishing detection, component updates, sync, metrics upload |
| User-scope MCP (`-s user`) | Available across all projects |

## Troubleshooting

**CDP unreachable** (`chrome-cdp-health` exit 1):

1. `launchctl list | grep chrome-cdp` — is the launchd agent loaded?
2. `pgrep -f chrome-cdp-profile` — is a Chrome process actually running?
3. **Process exists but CDP is dead** (the "running but hung" case): `chrome-cdp-restart` (when launchd-loaded), or `pkill -f chrome-cdp-profile` + `launch-chrome-cdp` if the launchd agent isn't loaded.
4. **Launchd shows non-zero exit** in `launchctl list`: check the stdout/stderr paths defined in your plist.

**CDP reaches the wrong machine** (`chrome-cdp-health` exit 2): `webSocketDebuggerUrl` does not start with `ws://127.0.0.1:9222/`. The Playwright MCP `--cdp-endpoint` has been pointed at a remote host — re-run the `claude mcp add` line in Quick Reference.

**Profile lock errors:** zombie Chrome holding `~/.cache/chrome-cdp-profile`. `pkill -f chrome-cdp-profile`, wait 2 s, relaunch.

**Clicks time out on "visible, enabled and stable" — and the element is fine.** The machine's display has gone to sleep, or the Chrome window is covered by another window. macOS then reports the window as occluded, Chrome stops firing `requestAnimationFrame`, and Playwright's actionability check — which waits for two stable animation frames — can never pass. It looks like a selector or a page problem; it is neither, and it hits elements that worked moments earlier.

Confirm it in one call: `document.visibilityState` reads `hidden` while the page is plainly loaded. The launch flags above (`--disable-backgrounding-occluded-windows` and friends) prevent it; if you are debugging a Chrome that was started without them, check the running process's argv before blaming the page. As a one-off unblock you can click via `element.click()` in `browser_evaluate`, which does not depend on animation frames — but verify the result in the application, not in the UI, and fix the launch flags rather than keeping the workaround.

No third-party keep-awake app is needed, and neither is `caffeinate`: the flags make Chrome ignore the display state, which was measured directly — display asleep went from **0 animation frames in 2 s to 80**, with `visibilityState` back to `visible`. CDP screenshots keep working with the display asleep too.

**Cloudflare challenges:** wait, don't retry. Real blocks are very rare; they need a fresh IP, not another browser restart.

**CfT update:** run `${CLAUDE_SKILL_DIR}/scripts/install-cft.sh` to download/install the latest stable version (it also refreshes the `launch-chrome-cdp` symlink).

**CfT behind stable — a login page refuses to proceed.** Symptom: a site's sign-in
shows a generic "your browser is behaving strangely" notice and will not accept
credentials, while the *same* login succeeds in Safari, or in Chrome stable, on the
same machine and the same network. That last part is the discriminator: it rules
out the IP, the network and the account, leaving the browser build.

The cause is the property CfT is chosen *for* — it does not auto-update. Left
alone, it falls behind stable and presents a version/capability combination no
real user has. The console tell is a probe of a newer web API aborting rather
than a request failing: for example a built-in-AI API that is present but whose
model reports `"unavailable"`.

**Do not read a `429` from a bot-defence sensor endpoint as a rate limit.** Some
vendors answer their sensor endpoint with `429` *plus* a valid token as their
normal handshake, and it appears in the console as a failed request. Diagnose by
comparing browsers on one machine, not by reading status codes.

Fix: update CfT (`install-chrome-for-testing.sh`). The launcher also detects this
now — if CfT's major version is below installed stable it uses stable and says so.
Force either with `CHROME_CDP_PREFER=testing` or `CHROME_CDP_PREFER=stable`.

**Lost session after CfT update:** the persistent profile at `~/.cache/chrome-cdp-profile` may lose stored cookies/logins after a Chrome for Testing version bump. This is one-time per upgrade — re-login manually in the headed browser, no profile reset needed. Warn the user before any destructive `pkill`/profile-clear, since they may need the existing tab state for re-auth.

## Setup

See [INSTALL.md](INSTALL.md) for the full setup checklist, including the launch script and launchd plist.

## Self-Improvement

If you encounter a setup step that fails, a Chrome/Playwright behavior change, or missing guidance in this skill, don't just work around it — fix the skill:

1. **Create a PR** from a fresh worktree of `https://github.com/eins78/agent-skills` on a new branch, fixing the issue directly
2. **Or file an issue** on `https://github.com/eins78/agent-skills` with: what failed, the actual behavior, and the suggested fix

Never silently work around a skill gap. The fix benefits all future sessions.
