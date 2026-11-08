---
name: browser-use
description: "Chrome DevTools MCP automation: existing Chrome tabs, no AppleScript."
---

# Browser Use

Browser tasks against existing Chrome session. Config repair: `mcporter-config.md`.

Hard rule: reattach existing Chrome profile only.

```bash
mcporter call chrome-devtools.<tool>
```

Login-heavy sites fail in isolated profiles (captcha, device checks, missing SSO/extension). Prefer existing Chrome for any site needing login.

Never use `chrome-isolated`, Playwright, Puppeteer, Codex in-app browser, AppleScript, `osascript`, GUI scripting, or macOS `open` for browser control unless user explicitly asks for isolated/new browser.

Screenshot/live UI bugs require existing-Chrome path. `curl`, source inspection, Worker tests, local Playwright = supporting proof only; not equivalent when user showed rendered browser problem or page depends on login/profile state.

## Check MCP

```bash
mcporter list chrome-devtools --schema
mcporter call chrome-devtools.list_pages --args '{}' --output text
```

`list_pages` must show user's real open tabs. Blank/default isolated Chrome → reattach failed, stop and say so.

Attach prompt recovery: if Chrome shows "Allow remote debugging?", click Allow via Peekaboo, rerun `list_pages`.

```bash
PB="${PEEKABOO_BIN:-$HOME/bin/peekaboo}"
[ -x "$PB" ] || PB="$(command -v peekaboo)"
"$PB" permissions status --json
"$PB" see --app frontmost --path /tmp/chrome-attach.png --json --annotate
# Click visible Allow button using current snapshot coords
"$PB" click --coords <allow_x>,<allow_y> --json
mcporter call chrome-devtools.list_pages --args '{}' --output text
```

Attach-alert rule: snapshot shows Chrome DevTools/MCP attach prompt → click visible Allow once, rerun `list_pages`. Button not visible or prompt ambiguous → stop, ask. Never silently switch to Playwright/Puppeteer.

`DevToolsActivePort` error → ask user to restart Chrome or DevTools bridge, retry once:

```bash
mcporter daemon restart
mcporter call chrome-devtools.list_pages --args '{}' --output text
```

Still fails → stop, say Chrome DevTools MCP unavailable. No AppleScript.

Avoid noisy recovery loops. Repeated restarts trigger reconnect/login prompts. Try once, then pause.

## Typical Flow

```bash
mcporter call chrome-devtools.select_page --args '{"pageId":9}' --output text
mcporter call chrome-devtools.take_snapshot --args '{}' --output text
mcporter call chrome-devtools.navigate_page --args '{"url":"https://example.com"}' --output text
mcporter call chrome-devtools.click --args '{"uid":"1_38","includeSnapshot":true}' --output text
mcporter call chrome-devtools.fill --args '{"uid":"1_13","value":"text","includeSnapshot":true}' --output text
mcporter call chrome-devtools.evaluate_script --args '{"function":"() => document.title"}' --output json
```

Use `take_snapshot` before actions, current `uid` values only. `take_screenshot` only when visual layout matters.

## Live UI Proof

```bash
mcporter call chrome-devtools.list_pages --args '{}' --output text
mcporter call chrome-devtools.select_page --args '{"pageId":9}' --output text
mcporter call chrome-devtools.navigate_page --args '{"url":"https://example.com"}' --output text
mcporter call chrome-devtools.take_snapshot --args '{}' --output text
mcporter call chrome-devtools.evaluate_script --args '{"function":"() => document.body.innerText"}' --output json
```

Browser automation unavailable → report as verification gap, don't substitute isolated tooling.

## Secret Handling

Never print tokens/passwords from DOM, network logs, inputs. Token checks: shape only (present/absent, length, status code, account/org).
