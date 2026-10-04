---
name: debugging
description: Diagnose and fix UI/runtime bugs. After a code change, verify in the browser with the available browser tools, read the console, and — for non-obvious bugs — add strategic temporary logging to locate the cause, then remove it. The agent decides how much of this flow a given bug needs.
---

# Debugging Skill: Diagnose, Fix, Verify

## Purpose
Find the root cause of a UI or runtime bug, fix it, and confirm the fix in the
browser with a clean console — without leaving temporary instrumentation behind.

## Browser tooling (works for both toolsets)
Use whichever browser automation is configured in your environment:
- **Claude** — Playwright MCP (`mcp_playwright_browser_*`).
- **VS Code Copilot** — the Copilot browser tools (`open_browser_page`,
  `read_page`, `screenshot_page`, `click_element`, `type_in_page`, …).

Both surface the page's console output — read it. Wherever this skill says
"browser tools", use whichever set is available.

## Match the effort to the bug
Not every bug needs the full flow. **The agent decides which steps a given bug
warrants:**
- **Obvious bugs** (clear stack trace, a typo, a wrong prop) — fix directly, then
  do a quick browser check to confirm.
- **Non-obvious bugs** (wrong value, state not updating, intermittent) — walk the
  flow and/or add strategic logging (below) to locate the cause before changing code.

## Workflow

1. **Reproduce**
   - Start a fresh browser session after any file change or hot-reload — don't
     reuse stale state.
   - Navigate to the affected surface and drive it as a real user would until the
     bug appears. (Skip login if a bypass flag is enabled.)

2. **Read the console**
   - Capture console logs, warnings, errors, and exceptions via the browser tools.
   - A clean console is part of "done" — don't proceed while errors/warnings remain.

3. **Add strategic logging (suggestion, for non-obvious bugs)**
   - When the console alone doesn't reveal the cause, add a few well-placed
     temporary `console.log`/`console.warn` statements to bisect the problem —
     e.g. log the value at each hop (loader hook → surface → child), before/after a
     state update, or on both branches of a suspect condition.
   - Prefer a small number of targeted logs over blanket instrumentation. Label
     them (e.g. `console.log('[dbg panel]', ...)`) so they're easy to find and remove.
   - Re-run the flow, read the logs, and narrow down to the root cause.

4. **Fix the root cause**
   - Change the code to address the underlying cause, not the symptom.

5. **Verify in the browser**
   - Fresh session, walk the flow again, confirm the bug is gone and the console
     is clean. Screenshot if a visual state changed.

6. **Remove temporary logging**
   - Delete every temporary log/instrumentation added in step 3 before finishing.
   - Double-check with a search for your debug label (e.g. grep for `[dbg`) so none
     leak into a commit. Keep only logging that is intentionally part of the code.

## Best Practices
- Always verify the UI is in a clean state before testing the fix.
- Use the available browser tools to drive the flow and read the console.
- Document any errors found and fix them before proceeding.
- Never commit temporary debug logging.
