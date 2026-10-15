---
name: Browser
description: Drive a managed Chrome session via CDP. Navigate, click, fill forms, read the DOM, take screenshots, run JS.
requires:
  bins: [chrome]
  env: []
---

# Browser

Controls a real Chrome/Chromium instance managed by the agent process.
Use for tasks that require reading or interacting with a live web page:
research, scraping structured data, filling forms, downloading files,
grabbing a visual reference. Every tool call maps 1:1 to a Chrome
DevTools Protocol command, so actions are immediate — no sandbox.

## Use when

- "Open example.com and tell me what the homepage says"
- "Log in to this page and grab my account balance"
- "Screenshot the dashboard for me"
- "Find the cheapest flight on this comparison site"
- "Click the Accept cookies button before you read the page"
- "Fill this form with my saved details and submit"

## Do not use when

- You can answer with a simple HTTP GET — use `fetch-url` skill instead.
  The browser is heavy; spinning it up for plain JSON is wasteful.
- Sites that ship a proper API (GitHub, Gmail, Slack). Use the matching
  skill (`github`, `google`, etc.) which talks the API directly.
- Anti-bot protected sites (Cloudflare JS challenge, hCaptcha). The
  browser can technically get past some, but you're one bot-detection
  update from breaking. Ask the user first.

## Tools exposed

| Tool | When to call |
|---|---|
| `browser_navigate {url}` | Go to an absolute URL. Wait for load. Call first on any new page. |
| `browser_snapshot` | Text representation of the DOM with element refs (`@e1`, `@e2`…). Primary way to "see" a page. Refresh refs by calling again after any navigate/click. |
| `browser_screenshot` | Base64 PNG of the viewport. For vision-capable models, or when layout matters. Don't call blindly — snapshot is cheaper. |
| `browser_click {target}` | Click an element. `target` is an `@eN` from the latest snapshot or a CSS selector. Prefer `@eN`. |
| `browser_fill {target, value}` | Replace the contents of an input / textarea. `value` is literal — special keys don't work here. |
| `browser_press_key {key}` | Dispatch a keyboard event on the focused element. Names: `Enter`, `Tab`, `Escape`, `Arrow{Up,Down,Left,Right}`. Anything else is treated as a literal char. |
| `browser_scroll_to {target}` | Scroll an element into view. Do this before clicking items the snapshot flagged as below the fold. |
| `browser_wait_for {selector, timeout_ms?}` | Poll until a CSS selector appears. Use between `browser_click` and the next `browser_snapshot` when the page triggers an XHR/SPA transition. |
| `browser_evaluate {script}` | Run arbitrary JS. Escape hatch for anything the other tools can't express. Returned value is in `result`. |
| `browser_current_url` | Shortcut for `browser_evaluate{ 'location.href' }`. |
| `browser_go_back` / `browser_go_forward` | Step through the history stack. |

## Canonical workflow

```
1. browser_navigate({url: "https://example.com"})
2. browser_snapshot()                    ← read the page, collect refs
3. browser_fill({target: "@e12", value: "user@example.com"})
4. browser_fill({target: "@e13", value: "s3cret"})
5. browser_click({target: "@e14"})       ← submit
6. browser_wait_for({selector: ".dashboard"})
7. browser_snapshot()                    ← confirm logged in, collect new refs
```

Element refs (`@eN`) are only valid inside the snapshot that produced
them — as soon as the DOM changes, re-call `browser_snapshot` before
referencing more refs. CSS selectors stay valid across snapshots, but
the LLM usually gets better accuracy with refs.

## Failure modes

- `{ok: false, error: "navigate timed out"}` — page didn't fire `load`
  within the timeout. Retry once with a longer implicit timeout via
  evaluate, or check if the URL is wrong.
- `{ok: false, error: "element not found"}` — the `@eN` is stale or the
  selector doesn't match. Call `browser_snapshot` again.
- `{ok: false, error: "circuit breaker ... open"}` — the plugin is
  cooling off after repeated failures. Wait a few seconds or ask the
  user to retry.

## Gotchas

- The browser is shared across agents that have `plugins: [browser]` —
  actions interleave. For side-effect-free reads it's fine; for stateful
  sessions (logins), give each agent its own `user_data_dir` in
  `config/plugins/browser.yaml`.
- Screenshots are PNG base64, usually 100–500 KB. Don't pipe them
  through `browser_evaluate` — hit the tool directly.
- `browser_evaluate` returns the value of the last expression. Wrap
  complex objects in `JSON.stringify(...)` if you need the full shape.
- Headless mode is opt-in via `browser.headless: true`. With a visible
  window the user sees exactly what you're doing — useful for trust,
  expensive in CPU.
