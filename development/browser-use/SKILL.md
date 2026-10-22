---
name: browser-use
description: >-
  Automates the user's existing signed-in Chrome profile through Chrome DevTools MCP (via mcporter):
  inspecting pages, screenshots, forms, clicks, and running JavaScript, without AppleScript. Use when
  a task needs a real logged-in browser tab rather than a fresh headless one.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.0"
license: MIT
---

# Browser Use

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

Use this for browser tasks against the existing Chrome session.

## When to Use

- Automating browser interactions via Chrome DevTools MCP
- Inspecting or debugging live web pages in the user's existing Chrome profile
- Taking screenshots of rendered pages for visual regression
- Filling forms, clicking elements, or running JS in real browser tabs

Hard rule: reattach to the existing Chrome profile only. Use this target:

```bash
mcporter call chrome-devtools.<tool>
```

Most login-heavy sites fail in isolated profiles because fresh sessions trigger captcha, device checks, or missing SSO/extension state. Strongly prefer the existing Chrome profile for any website that needs login.

Never use `chrome-isolated`, Playwright, Puppeteer, the Codex in-app browser, AppleScript, `osascript`, GUI scripting, or macOS `open` for browser control unless the user explicitly asks for an isolated/new browser.

Screenshot/live UI bugs require this existing-Chrome path. `curl`, source
inspection, Worker smoke tests, or local Playwright are supporting proof only;
do not treat them as equivalent when the user showed a rendered browser problem
or the page may depend on login/profile state.

## Check MCP

```bash
mcporter list chrome-devtools --schema
mcporter call chrome-devtools.list_pages --args '{}' --output text
```

`list_pages` must show the user's real open tabs. If it shows a blank/default isolated Chrome, stop and say reattach failed.

If the call appears to hang while Chrome shows an auth/attach/update prompt, handle the attach alert before falling back. Prefer Peekaboo to press an explicit Chrome `Allow` button when visible; otherwise wait for the human. Do not restart daemons or kill MCP processes just because the first output is slow.

If `list_pages` fails with `DevToolsActivePort`, ask the user to restart Chrome or the DevTools bridge, then retry once:

```bash
mcporter daemon restart
mcporter call chrome-devtools.list_pages --args '{}' --output text
```

If it still fails, stop and say Chrome DevTools MCP is unavailable. Do not use AppleScript.

## Typical Flow

```bash
# pick the page id from list_pages
mcporter call chrome-devtools.select_page --args '{"pageId":9}' --output text

# inspect page
mcporter call chrome-devtools.take_snapshot --args '{}' --output text

# navigate selected page
mcporter call chrome-devtools.navigate_page --args '{"url":"https://example.com"}' --output text

# click an element uid from the latest snapshot
mcporter call chrome-devtools.click --args '{"uid":"1_38","includeSnapshot":true}' --output text

# type/fill
mcporter call chrome-devtools.fill --args '{"uid":"1_13","value":"text","includeSnapshot":true}' --output text

# run JS, keep secrets out of output
mcporter call chrome-devtools.evaluate_script --args '{"function":"() => document.title"}' --output json
```

Use `take_snapshot` before actions and use current `uid` values only. Avoid `take_screenshot` unless visual layout matters.

## Live UI Proof

For screenshot regressions, deployed dashboard checks, or anything where the
rendered browser is the bug:

```bash
mcporter call chrome-devtools.list_pages --args '{}' --output text
mcporter call chrome-devtools.select_page --args '{"pageId":9}' --output text
mcporter call chrome-devtools.navigate_page --args '{"url":"https://example.com"}' --output text
mcporter call chrome-devtools.take_snapshot --args '{}' --output text
mcporter call chrome-devtools.evaluate_script --args '{"function":"() => document.body.innerText"}' --output json
```

Use the existing logged-in/profile-bearing tab set. If browser automation is
unavailable, report that as a verification gap instead of substituting isolated
browser tooling.

## Secret Handling

Never print tokens/passwords from page DOM, network logs, or inputs. For token checks, return shape only: present/absent, length, status code, account/org name.
