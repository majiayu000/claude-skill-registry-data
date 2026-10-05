---
name: "playwright"
description: "Use when the task requires automating a real browser from the terminal (navigation, form filling, snapshots, screenshots, data extraction, UI-flow debugging) via `playwright-cli` or the bundled wrapper script."
metadata:
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/playwright/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/playwright/SKILL.md`
> Source of truth: `registry/skills/playwright/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Playwright CLI Skill

Drive a real browser from the terminal using `playwright-cli`. Prefer the bundled wrapper script so the CLI works even when it is not globally installed.
Treat this skill as CLI-first automation. Do not pivot to `@playwright/test` unless the user explicitly asks for test files.

## Prerequisite check (required)

Before proposing commands, check whether `npx` is available (the wrapper depends on it):

```bash
command -v npx >/dev/null 2>&1
```

If it is not available, pause and ask the user to install Node.js/npm (which provides `npx`). Provide these steps verbatim:

```bash
# Verify Node/npm are installed
node --version
npm --version

# If missing, install Node.js/npm, then:
npm install -g @playwright/cli@latest
playwright-cli --help
```

Once `npx` is present, proceed with the wrapper script. A global install of `playwright-cli` is optional.

## Skill path (set once)

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"
```

User-scoped skills install under `$CODEX_HOME/skills` (default: `~/.codex/skills`).

## Quick start

Use the wrapper script:

```bash
"$PWCLI" open https://playwright.dev --headed
"$PWCLI" snapshot
"$PWCLI" click e15
"$PWCLI" type "Playwright"
"$PWCLI" press Enter
"$PWCLI" screenshot
```

If the user prefers a global install, this is also valid:

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
```

## Dedicated Chrome Profile + CDP Runtime

When the user wants Playwright to control an authenticated browser session, do not try to attach to the Codex in-app browser or a normal already-open Chrome window. Start a dedicated browser profile with a remote debugging port, then connect with Playwright over CDP.

For headed Chrome work that needs a persisted profile, follow the Browser skill profile governance:

- Use `$env:USERPROFILE\.codex\plugins\cache\openai-bundled\browser-use\0.1.0-alpha1\skills\browser\profile-01` as the primary writable Chrome `--user-data-dir`.
- Use `$env:USERPROFILE\.codex\plugins\cache\openai-bundled\browser-use\0.1.0-alpha1\skills\browser\profile-02` only as a readable backup or recovery source.
- Do not launch Chrome directly against `profile-02` for ordinary Playwright work, do not modify it, and do not copy state back into it unless the user explicitly asks.
- If `profile-01` is missing or unusable, first restore or copy a fresh writable profile from `profile-02` or the original source paths, then operate on that writable copy.
- If neither bundled profile can be used or restored, choose or create a context-appropriate writable profile and state that fallback briefly to the user.

Windows helper:

```powershell
$PW_CHROME_CDP="$env:USERPROFILE\.codex\skills\playwright\scripts\start_chrome_cdp.ps1"
& $PW_CHROME_CDP -Url "https://chatgpt.com" -Port 9222
```

Optional parameters:

```powershell
& $PW_CHROME_CDP `
  -Browser Chrome `
  -Url "https://chatgpt.com" `
  -Port 9222 `
  -UserDataDir "$env:USERPROFILE\.codex\plugins\cache\openai-bundled\browser-use\0.1.0-alpha1\skills\browser\profile-01" `
  -ProfileDirectory "Default"
```

Verify the runtime:

```powershell
curl http://127.0.0.1:9222/json/version
# If 127.0.0.1 is occupied by another browser process, use the helper's printed endpoint, often:
curl http://[::1]:9222/json/version
```

Connect from Playwright code when CLI commands need the authenticated runtime:

```js
const { chromium } = require("playwright");
const browser = await chromium.connectOverCDP("http://127.0.0.1:9222"); // or the helper's printed endpoint
const context = browser.contexts()[0];
const page = context.pages()[0] ?? await context.newPage();
await page.goto("https://chatgpt.com");
```

Smoke-test the CDP connection when Playwright is available:

```powershell
npx --yes --package playwright node "$env:USERPROFILE\.codex\skills\playwright\scripts\cdp_smoke.mjs" "http://[::1]:9222"
```

Use this pattern for ChatGPT, OAuth, and other login-gated UI flows. Pause for the user at login, OAuth consent, write-action warnings, and admin publish confirmations.

## Core workflow

1. Open the page.
2. Snapshot to get stable element refs.
3. Interact using refs from the latest snapshot.
4. Re-snapshot after navigation or significant DOM changes.
5. Capture artifacts (screenshot, pdf, traces) when useful.

Minimal loop:

```bash
"$PWCLI" open https://example.com
"$PWCLI" snapshot
"$PWCLI" click e3
"$PWCLI" snapshot
```

## When to snapshot again

Snapshot again after:

- navigation
- clicking elements that change the UI substantially
- opening/closing modals or menus
- tab switches

Refs can go stale. When a command fails due to a missing ref, snapshot again.

## Recommended patterns

### Form fill and submit

```bash
"$PWCLI" open https://example.com/form
"$PWCLI" snapshot
"$PWCLI" fill e1 "user@example.com"
"$PWCLI" fill e2 "password123"
"$PWCLI" click e3
"$PWCLI" snapshot
```

### Debug a UI flow with traces

```bash
"$PWCLI" open https://example.com --headed
"$PWCLI" tracing-start
# ...interactions...
"$PWCLI" tracing-stop
```

### Multi-tab work

```bash
"$PWCLI" tab-new https://example.com
"$PWCLI" tab-list
"$PWCLI" tab-select 0
"$PWCLI" snapshot
```

## Wrapper script

The wrapper script uses `npx --package @playwright/cli playwright-cli` so the CLI can run without a global install:

```bash
"$PWCLI" --help
```

Prefer the wrapper unless the repository already standardizes on a global install.

## References

Open only what you need:

- CLI command reference: `references/cli.md`
- Practical workflows and troubleshooting: `references/workflows.md`

## Guardrails

- Always snapshot before referencing element ids like `e12`.
- Re-snapshot when refs seem stale.
- Prefer explicit commands over `eval` and `run-code` unless needed.
- When you do not have a fresh snapshot, use placeholder refs like `eX` and say why; do not bypass refs with `run-code`.
- Use `--headed` when a visual check will help.
- When capturing artifacts in this repo, use `output/playwright/` and avoid introducing new top-level artifact folders.
- Default to CLI commands and workflows, not Playwright test specs.
