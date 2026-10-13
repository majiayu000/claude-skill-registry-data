---
name: automation-browser
description: >
  Drive a real browser against an in-scope web app with Playwright / agent-browser: automated
  login, form and payload submission through the UI, scraping JS-rendered pages, request/response
  interception, and evidence screenshots. Load on "browser automation", "fill this form", "submit
  payload", "screenshot this page", automated login, headless crawling, or UI-driven XSS testing.
  Signals: Playwright, agent-browser, headless, @e1 element refs, networkidle, DOM interaction.
domain: automation
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: info
mitre: [T1059.007]
tools: [playwright, agent-browser, nodejs, burp]
schema_version: 1
---

# Browser automation (Playwright / agent-browser)

## When it applies
The in-scope target (`scope.txt`, `tradecraft-scope-roe`) needs a *real browser*, not raw HTTP:
multi-step or JS-heavy login flows, pages that render client-side, payloads that must go through
the UI (XSS into a live DOM, CSRF flows), evidence screenshots, or scraping behind a session. For
pure request replay use Burp/curl instead; honor bug-bounty rate limits in `roe.md` — automation
multiplies request volume.

## Why it works
A scripted browser executes the app's JavaScript, holds cookies/session like a real user, and sees
the post-render DOM — so guards that defeat raw HTTP (JS challenges, dynamic forms) just work. The
`agent-browser` CLI exposes the accessibility tree as stable `@eN` element refs, which survive
layout changes better than CSS selectors; the Playwright Node API adds network interception,
storage extraction, and screenshots for everything the CLI can't do.

## Method
1. **Install once:** `npm install -g playwright agent-browser && npx playwright install`.
2. **Core CLI loop** — open, snapshot, act, verify, close:
   ```bash
   agent-browser open "https://target.com/login"
   agent-browser snapshot -i          # interactive elements only → @e1, @e2...
   agent-browser fill @e2 "admin"
   agent-browser type @e3 "password"  # type, not fill, when JS listens for input events
   agent-browser click @e4
   agent-browser wait --load networkidle
   agent-browser get url              # did we land in the authenticated area?
   agent-browser close                # mandatory — leaked processes hang later runs
   ```
   Always `snapshot` before acting — refs are per-page-state, never guess them.
3. **Drop to the Playwright Node API** when you need cookies/localStorage extraction, request
   interception or response tampering (e.g. flip `role: user → admin` to test client-side
   authorization), or `fullPage` screenshots for evidence. Full command and API reference, plus
   pentest patterns (auto-login, XSS injection, batch payload loops): [`cheatsheet.md`](cheatsheet.md).
4. **Route through Burp** (`proxy: { server: 'http://127.0.0.1:8080' }` + `ignoreHTTPSErrors:
   true`) so every automated request lands in your proxy history for manual follow-up.
5. **Adjacent: desktop GUI automation.** If the target is a Windows desktop app (thick client, IDA,
   x64dbg) rather than a web page, the same agent-driven model exists in
   [OpenReverse](https://github.com/zhexulong/openreverse): UIA mode for standard Windows controls,
   CUA (vision-driven) mode for custom-rendered GUIs, plus a built-in mitmproxy lane for observing
   the app's traffic. Install and command shapes are in the cheatsheet; pair it with
   `reverse-eng-thick-client`.

## Gotchas
- **Leaked processes** — a missing `agent-browser close` leaves a browser that breaks the next
  `open`; close first when a session wedges.
- **Stale element refs** — any navigation or re-render invalidates `@eN`; re-`snapshot -i` after
  every page change instead of reusing old refs.
- **`fill` silently no-ops** on inputs with JS listeners — use `type` (per-character events).
- **Timing** — after submits wait on `networkidle` (or a specific selector/response), not fixed
  sleeps; use `domcontentloaded` for slow heavy pages.
- **Headless detection** — some apps behave differently headless (anti-bot); run headed or tune
  the user agent when behavior diverges from manual testing.

## Verify success
The flow completed end-to-end (final URL/DOM confirms the authenticated or post-submit state) and
evidence is on disk: screenshot, captured response, or extracted storage — reproducible from the
commands you ran.

## References
Playwright docs (playwright.dev); agent-browser CLI; OpenReverse (github.com/zhexulong/openreverse).

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
