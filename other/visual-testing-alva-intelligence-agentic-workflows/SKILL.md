---
name: visual-testing
description: Validate UI work by driving the browser — what to click, what to check, screenshot evidence, and strict resource discipline (headless-first, one tab, no waste). Use whenever UI work claims to render, before declaring a UI phase complete, or when verifying a subagent's visual claims.
---

# Visual Testing — browser-use is the main browser

The agent's visual truth comes from **browser-use** driving a real browser. Anything claiming
"it renders" gets this treatment: the implementing subagent first, the orchestrator independently.

## Resource discipline (strict — this runs on the user's machine)

- **Headless as possible.** Attach to the user's running local Chrome over CDP (default flow) —
  no new Chrome processes, no visible tab needed. Screenshots and CDP input work on background
  tabs; never call `activate_tab()`/foreground anything unless a proven scroll timeout forces it.
- **One tab per task/site.** `new_tab(url)` once on first navigation; reuse it via
  `current_tab()` / `switch_tab()` after. Never leave duplicate tabs on a URL; never close tabs
  you didn't create.
- **No recordings** unless the user explicitly asks for a demo/video (`browser-use recordings` is
  opt-in by request, never by default).
- **AX tree before screenshots.** Screenshots only when layout or imagery is itself the question;
  they cost memory and tokens. Prefer `cdp("Accessibility.getFullAXTree")` filtered in Python.
- **Cloud/headless daemons only for** headless servers or truly parallel isolated sessions — and
  they bill per minute: ask the user before starting any `start_remote_daemon`, and
  `stop_remote_daemon(name)` the moment the check finishes.
- **Dev servers:** start a service once, reuse it for the whole testing round, stop it after
  (unless the user wants it left running). Never start duplicates — run-all/health commands live
  in the service registry. One visual-testing session at a time locally; parallel = cloud (ask
  first).
- **Local Chrome permission popups** (macOS remote-debugging): keep the waiting command running,
  call `browser-use mac-approve` in a second shell with the same `BU_NAME`.

## Procedure

```bash
browser-use <<'PY'
new_tab("http://localhost:3000/<route>")
wait_for_load()
print(page_info())
PY
```

1. **Navigate** with `new_tab` (first time) / `goto_url` (after), `wait_for_load()`.
2. **Structure first:** `cdp("Accessibility.getFullAXTree")["nodes"]` — filter for the roles/names
   the acceptance criteria demand (buttons, headings, tabs, empty states).
3. **Interact where behavior matters** — find the node, compute its box center, `click_at_xy`,
   then **verify the state changed** with a targeted `js(...)` or `page_info()` (URL, counter,
   toast text, data row count). A click without a post-check proves nothing.
4. **Data states:** exercise realistic data — valid entry, at least one realistic long/odd value,
   empty result, and the error path. Check loading UI actually resolves.
5. **Console errors:** capture `js` exceptions/errors near the interaction (page's own handlers or
   `window.onerror` hooks); any error that is *yours to own* (not the user's session quirks) is a
   finding, screenshot + note it.
6. **Evidence:** when layout matters, screenshot and keep the returned path. Reference it in the
   report ("verified `/brand-dashboard` renders 7 tabs — <path>").
7. **Viewport sanity:** check the main flow at a common desktop size; resize via the viewport skill
   when the task targets responsive behavior.
8. **Report claims like an evaluator, not a narrator:** what was expected, what was observed, file
   any mismatch as a must-fix with the reproduction click-path.

## Division of labor

- **Implementation subagent:** visual-tests its own service UI before reporting done (same
  discipline, tab of its own or, if harness allows sibling coordination, a shared session name).
- **Orchestrator:** independently re-tests the main paths of every UI claim — the same acceptance
  criteria, fresh eyes (fresh tab state where cheap). Acceptance = orchestrator's own observation,
  not the subagent's report.
- Subagents never start Chrome/daemons of their own accord; if parallel browser sessions are truly
  needed, ask the user.

## Traps (hit in real sessions)

- `scroll(...)` timing out on a *hidden* tab = the page needs visibility. Either `activate_tab()`
  once (visible! don't do it when user forbids foreground changes) or test that path differently —
  do NOT hand-roll `Runtime.evaluate` scrollbar hacks.
- Omnibox popups are not work tabs; CDP target order ≠ tab-strip order.
- Login walls: stop and ask; SSO with Chrome already signed in is the only auto-pass.
- Remote daemons bill until stopped — closing the tab is not stopping the daemon.
