---
name: using-playwright
description: Use when verifying UI changes, scraping web data, or automating browser flows.
---

# Using Playwright

## What this is

Playwright MCP drives a real browser. You can navigate, click, type, observe console/network, and snapshot the DOM. It's how you **verify a UI change actually works** — not just compiles — and how you scrape dynamic content that static HTTP can't see.

## When to use

- Verifying a UI change: load the page, check a button renders/clicks, confirm console is clean
- Reproducing a frontend bug locally before/after a fix
- Scraping data from sites where content is JS-rendered (SPA, dynamic React/Vue/Svelte)
- End-to-end testing of a web flow (login → action → result)
- Capturing screenshots when the user asks to see the app

## When NOT to use

- Static HTML scraping where a `WebFetch` would work — Playwright is heavier
- The user didn't ask for UI verification and isn't expecting browser automation
- You need to test backend APIs only (use HTTP clients/curl/Invoke-RestMethod)
- Quick info lookups (`WebSearch`/`WebFetch` are cheaper)
- Tests that should be permanent — write actual Playwright test files instead of using MCP ad-hoc

## Core tools

| Tool | Purpose |
|---|---|
| `mcp__playwright__browser_navigate` | Load a URL |
| `mcp__playwright__browser_snapshot` | Accessibility tree — **prefer this over screenshot for navigation** |
| `mcp__playwright__browser_click` | Click by element `ref` from snapshot |
| `mcp__playwright__browser_type` | Type into an element by `ref` |
| `mcp__playwright__browser_fill_form` | Fill multiple form fields at once |
| `mcp__playwright__browser_evaluate` | Run arbitrary JS in the page |
| `mcp__playwright__browser_console_messages` | Read console output |
| `mcp__playwright__browser_network_requests` | List network requests (numbered) |
| `mcp__playwright__browser_network_request` | Full details of one request by index |
| `mcp__playwright__browser_take_screenshot` | PNG/JPEG screenshot — **only when the user wants to see** |
| `mcp__playwright__browser_wait_for` | Wait on text appearing/disappearing or N seconds |
| `mcp__playwright__browser_close` | Close the page when done |

## Standard workflow

```
1. browser_navigate           → load page
2. browser_snapshot           → get accessibility tree with refs
3. browser_click / browser_type using refs from step 2
4. browser_snapshot           → confirm state changed
5. browser_console_messages   → verify no errors
6. browser_network_requests   → if API calls matter, check them
7. browser_close              → clean up
```

The `ref` from `browser_snapshot` is the **canonical handle** for elements — pass it as `target` to click/type/hover. Don't guess CSS selectors when you have a ref.

## Snapshot vs screenshot — important

- `browser_snapshot` returns the accessibility tree as text. It's how you understand structure, find elements, and verify state. **Token-cheap.**
- `browser_take_screenshot` returns a PNG/JPEG. It's how the **user** sees the UI. **Token-expensive.**

Rule:
- **You** look at snapshots to act.
- **User** sees screenshots when they asked for one.

Taking a screenshot then describing the DOM from it = wrong tool. Take a snapshot.

## Waiting — use conditions, not sleep

Don't blindly wait. `browser_wait_for` takes:
- `text: "Welcome back"` — wait until text appears
- `textGone: "Loading..."` — wait until text disappears
- `time: 3` — last resort, fixed seconds

Condition-based waits beat fixed-time waits every time. Same principle as `condition-based-waiting` skill.

## Common verification patterns

### Verify a button click works

```
browser_navigate(url="http://localhost:3000")
browser_snapshot()                                  # get ref for "Submit" button
browser_click(target=<ref>, element="Submit button")
browser_wait_for(text="Saved successfully")
browser_console_messages(level="error")             # should be empty
```

### Confirm no console errors on a page

```
browser_navigate(url=<url>)
browser_wait_for(time=2)                            # let the app settle
browser_console_messages(level="error", all=true)
```

### Check an API call fires correctly

```
browser_navigate(url=<url>)
browser_click(...)                                  # trigger the action
browser_network_requests(static=false, filter="/api/")
browser_network_request(index=<N>, part="response-body")
```

## Constraints and notes

- The browser session is shared across calls — `browser_close` only when done, not between every step
- `browser_evaluate` runs arbitrary JS in the page — use sparingly, prefer dedicated tools when available
- `browser_run_code_unsafe` runs arbitrary code in the Playwright server process — **RCE-equivalent, avoid unless absolutely necessary**
- File uploads via `browser_file_upload` need absolute paths
- Dialogs (alert/confirm/prompt) need `browser_handle_dialog` or they hang

## Combining with other tools

- **For a permanent test**, write a `.spec.ts` file and run it with `npx playwright test` — MCP is for one-off verification, not a test suite replacement
- **With `context7`**: query Playwright docs if you hit an unfamiliar API
- **With dev server**: `npm run dev` in background (`run_in_background: true`), then drive it via MCP

## Red flags — wrong tool

- You took a screenshot and are now writing prose describing what's in it for yourself → should be `browser_snapshot`
- You used `Start-Sleep` between two MCP calls → should be `browser_wait_for` with a condition
- You're trying to scrape a server-side-rendered HTML page → `WebFetch` is cheaper
- The user didn't ask you to verify the UI and you're spinning up a browser anyway → ask first

## One-liner reminder

Snapshot to act, screenshot to show. Wait on conditions, not clocks.
