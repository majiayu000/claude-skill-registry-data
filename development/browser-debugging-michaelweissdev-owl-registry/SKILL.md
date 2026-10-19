---
name: browser-debugging
description: >
  Debug front-end problems in the browser with Chrome DevTools: Console, Sources
  breakpoints, Network, Elements/computed styles, Application storage, Performance,
  and source maps; including debugging through an MCP/automation browser. Use when a
  page throws errors, a request fails or returns the wrong data, CSS does not apply,
  state or storage looks wrong, a bug only reproduces in the browser, or you need to
  turn a vague "it's broken" into a minimal repro with evidence. Do not use for writing
  automated tests (playwright-testing), general non-browser debugging method
  (debugging-workflow), Node.js server debugging (nodejs-development), or security
  testing (web-security-testing).
compatibility: >
  Chromium-based browsers with Chrome DevTools; Firefox and Safari have equivalent
  panels with different names. Optional automation via Playwright or a browser MCP
  server.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "devtools, chrome, debugging, console, network, breakpoints, source-maps, frontend"
  topics: "frontend, debugging, devtools"
---

# Browser Debugging

Turn a symptom into a located cause using the browser's own evidence: the console error with its stack, the failed request with its headers and body, the computed style with its winning rule, the breakpoint where state first goes wrong.

Related skills: `debugging-workflow` (the general hypothesis loop), `playwright-testing` (lock the fix in with a test), `web-html-css`, `javascript-development`, `react-performance` (profiling React), `web-accessibility-review`, `web-security-testing`.

## When to use / not use

Use for browser-side bugs and investigations. For server errors, use the server logs once the Network panel shows what the server returned. Do not use it to attack sites you do not own or have permission to test.

## Non-negotiable rules

1. **Reproduce first, minimally.** Exact steps, URL, build (dev vs production), browser version, logged-in state, and data. A bug you cannot reproduce cannot be verified fixed.
2. **Observe before changing.** Read the console, network, and DOM evidence before editing code. Change one thing at a time.
3. **Protect secrets.** HAR files, cookies, `Authorization` headers, and local/session storage can contain live tokens and personal data. Do not paste them into issues or chats; redact first. Do not read or export credentials you do not need.
4. **Use a clean profile for diagnosis.** Extensions can inject scripts and break pages; reproduce in a fresh profile or incognito with extensions disabled.
5. **Remote debugging ports are powerful.** If you launch Chrome with `--remote-debugging-port`, it grants full control of that browser instance to anything that can reach the port. Keep it bound to localhost, use a throwaway `--user-data-dir`, and never expose it on a network.
6. **Do not leave debugging changes behind**: `debugger` statements, Local Overrides, `console.log` noise, and disabled cache settings.

## Workflow

### 1. Frame the symptom
Write: expected vs actual, where it shows (UI, console, network), frequency (always, intermittent, only first load), and what changed recently.

### 2. Open the right panel first

| Symptom | Start in |
|---|---|
| Red error / blank page | Console (error text, stack trace, "Issues" panel) |
| Data missing or wrong | Network (status, response, payload, timing), then Sources |
| Looks wrong | Elements > Styles / Computed / Layout |
| Works once, fails after reload or login | Application (cookies, storage, service workers, cache) |
| Slow or janky | Performance (see `react-performance` for React) |
| Different in production | Source maps, Network (cache/CDN), build differences |

### 3. Console
- Read the first error, not the last; later errors are often consequences.
- Click the stack frame to jump to Sources. Enable source maps (default on) so you see original code; if frames show minified code, the map is missing or not served.
- Useful utilities in the console: `$0` (selected element), `$_` (last result), `copy(obj)`, `console.table(rows)`, `monitor(fn)`/`unmonitor(fn)`, `getEventListeners($0)`, and filtering by level or text.
- Use `console.log` with labeled objects or `console.table`; prefer breakpoints and logpoints over scattering logs.

### 4. Sources: breakpoints
Choose the breakpoint type to match the question:
- Line breakpoint: stop at code you suspect.
- Conditional breakpoint / logpoint: stop or log only when an expression is true, with no code edit (logpoints do not pause).
- "Pause on caught/uncaught exceptions": find where an error originates.
- XHR/fetch breakpoint (URL contains): stop when a request is made.
- Event listener breakpoints: stop on click, keydown, etc.
- DOM breakpoints (Elements panel): stop when a node's subtree, attributes, or the node itself is modified.
Then step (over, into, out), inspect Scope and Call Stack, and add Watch expressions. Use the Ignore List to skip framework/library frames. To find where state first went wrong, walk up the call stack and compare values at each frame.

### 5. Network
- Reload with "Disable cache" (while DevTools is open) when diagnosing stale assets; remember to re-enable it.
- Check status code, response body, request headers/payload, `Content-Type`, redirects, and timing (Waterfall).
- CORS failures appear as console errors plus a blocked or opaque response; the fix is server-side headers (`Access-Control-Allow-Origin`, preflight handling), not the client. Look at the preflight `OPTIONS` request.
- Throttle (Slow 4G / offline) to reproduce loading and error states.
- Filter by Fetch/XHR; use "Copy as cURL" only after redacting auth headers; compare a working and a failing request side by side.
- Local Overrides and request blocking help test hypotheses without a rebuild.

### 6. Elements and CSS
- Select an element, read the Styles pane top to bottom: struck-through rules lost the cascade; check specificity, order, and `!important`.
- Computed tab shows final values and which rule supplied them.
- Layout tools: Flexbox/Grid overlays, box model, and the `:hov` toggle for `:hover`/`:focus` states.
- Check for an element overlapping or `pointer-events: none` when clicks "do nothing".

### 7. Application
Inspect cookies (flags `HttpOnly`, `Secure`, `SameSite`, expiry), Local/Session Storage, IndexedDB, Cache Storage, and Service Workers (a stale service worker is a classic cause of "old code keeps loading": use Update on reload or Unregister during diagnosis). Clear site data to test first-visit behavior.

### 8. Narrow to a minimal repro
Remove code, data, and dependencies until the bug remains. Then bisect (`git bisect`, see `git-workflow`) if it is a regression.

### 9. Fix, verify, and lock in
Fix at the cause, re-run the exact repro, test other browsers if relevant, and add an automated test (`playwright-testing` or `unit-testing`).

## Debugging through automation or an MCP browser

When an agent drives a browser (Playwright, Chrome DevTools-style MCP): collect console messages, network requests, and a screenshot or DOM snapshot as evidence before and after a change; prefer role/text locators; run against localhost or authorized staging only; never feed secrets into page fields except designated test credentials for your own test app. For Playwright, `npx playwright test --debug` opens the inspector and `npx playwright show-trace trace.zip` opens a recorded trace (see `playwright-testing`).

## Worked example

Symptom: after login, the dashboard shows "No data" in production but works locally.

1. Console: no errors. Network: `GET /api/summary` returns 200 with `[]`, then the request goes to a different origin than local.
2. The request URL shows `https://staging.example.test/api/summary`. Sources (with source map) shows the base URL read from `import.meta.env.VITE_API_URL` at build time.
3. Conclusion: production build used the staging value. Evidence: the request URL, plus the env value baked into the bundle.
4. Fix the build configuration, rebuild, verify the request goes to the right origin, add a smoke test asserting the dashboard request host.

## Anti-patterns

- Fixing before reproducing; changing several things at once.
- Debugging in a polluted profile with extensions.
- Trusting the dev build when the bug is in production only (minification, env, caching, CDN).
- Pasting HAR files or cURL commands with live tokens.
- Leaving "Disable cache" on and forgetting why behavior differs later.
- Treating CORS errors as client bugs.
- Wrapping everything in `try/catch` to silence console errors.
- Commit-leaving `debugger` or debug logs.

## Verification checklist

- [ ] Repro steps and environment recorded
- [ ] First error or failing request identified with evidence
- [ ] Cause located (file/line, request, rule, or storage state)
- [ ] Fix verified by the original repro, in a clean profile
- [ ] Secrets redacted from anything shared
- [ ] Debug leftovers removed; regression test added where sensible

## References

- [DevTools panel and shortcut cheat sheet](references/devtools-cheatsheet.md)
- [Scenarios for evaluating this skill](references/scenarios.md)
- [Sources and provenance](references/sources.md)
