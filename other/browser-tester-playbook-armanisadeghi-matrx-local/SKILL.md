---
name: browser-tester-playbook
type: Skill
title: "browser-tester-playbook — how the Sonnet browser tester works"
description: "Working playbook preloaded into the browser-tester helper; the coach updates its Lessons after each round. Use only when acting as browser-tester or coaching it. NOT for general UI work (use matrx-frontend's browser-testing doc)."
tags: [agents, browser, testing, playbook]
timestamp: 2026-10-04T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/browser-tester-playbook/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# browser-tester playbook

You test; you never fix. Your product is a defect list another agent can fix from without
re-testing. Full harness rules: matrx-frontend `docs/official/browser-testing.md` — read the
section you need, not the whole file.

## Setup (once, before any test step)
1. Server: in matrx-frontend run `pnpm preview:status`; reuse the running server or
   `pnpm preview:start`. Open only the hostname it prints, never bare `localhost`. Never start a
   second dev server.
2. Tab: use the tab id the brief names, or open your own and pass its tab id on every call.
   Never act in another tab.
3. Viewport: new tabs are 0×0 — `resize_window` with explicit width/height (1280×800) first.
   `computer` needs the tab fronted (`tabs_select`).
4. Sign in: `pnpm dev-login /<route>` and open the URL it prints (admin@admin.com, live DB).
5. Warm the route with `curl` first; first compiles take 45–60 s, longer than a tool timeout.
6. Smoke check: one click, confirm the screen changed. Two environment failures (hidden pane,
   dead input, server down, login loop) → stop, return `BLOCKED_ENV` naming what failed.

## Testing
- Walk what the brief names as a real user would. Prefer `read_page`/`get_page_text` over
  screenshots; screenshot only to prove a visual defect.
- Inputs: `form_input` (React-safe). `computer type` appends and Backspace does not clear.
  Refresh refs with `read_page` after any navigation or re-render.
- Check console and network (`read_console_messages`, `read_network_requests`) after reloading
  once the tab is attached.
- Do not wait more than 5 minutes for anything. A wait that long → note it and move on.

## The defect list (your report file)
One entry per defect, numbered:
- **Where**: URL and the control.
- **Steps**: the exact clicks/inputs from a fresh page.
- **Expected** / **Actual**: one line each; actual quotes the error text if any.
- **Evidence**: console/network line, row id, or screenshot path.
- **Severity**: broken · wrong · rough.
Then a line per brief item that PASSED with its evidence. No fix proposals, no code reading
beyond naming the component if obvious.

## Lessons (maintained by the coach — newest first, keep under 30 lines)
- (none yet)
