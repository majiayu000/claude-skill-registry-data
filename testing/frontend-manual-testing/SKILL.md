---
name: frontend-manual-testing
category: qa
description: Use when the task changes anything a user sees in a web app - booting it, driving flows with the browser tools, the four-width check, console/network/keyboard checks and the visual checklist
source: microsoft/playwright-cli (Apache-2.0), anthropics/skills webapp-testing (Apache-2.0), wshobson/agents (MIT), adapted
---
# Frontend Manual Testing

## Overview

A frontend task is verified by rendering it: boot the app, drive the changed flows in a real browser, and look at what the user would see. Screenshots are mandatory evidence — a UI verdict without having looked at the screen is an untested claim.

**Preconditions:** case matrix recorded with `record_test_cases` (scenario-plan-first), covering both functional cases (per AC) and visual cases (layout, states, responsiveness); environment chosen per test-environment-selection.

## Booting

- First choice `start_task_preview` (test-environment-selection); only when it cannot run the project, install and start per the project's declared commands (`npm ci` + dev/preview script, or the repo's `build_command`) with the log at `$QA/dev.log`, never `/tmp/dev.log`. Point the app at the local backend you booted (backend-manual-testing) or at the stage API base URL — the API base is usually an env var (`VITE_API_URL` or similar); read the project's config, don't guess.
- Confirm the page actually loads before scenario work: a blank page with console errors is finding #1.
- Confirm the app is talking to the real backend, not mock data (MSW/`VITE_USE_MOCKS`/fixtures): `requests` from playwright-cli (below) or the backend's own access log shows the actual calls.

## Shared browser

The browser tools' session is shared with every agent running right now — there is one headless browser for the whole server. Each screenshot result prints `url:` and `viewport WxH`: confirm both are what you set before judging the image; a mismatch means another run moved it — re-navigate, re-set the viewport, retake. If the page suddenly shows a login screen, log in again.

## Driving flows and taking screenshots

The browser tools are the primary way to drive the app — no local Chromium setup, no script files:

1. `browser_navigate` to the page under test.
2. `browser_wait_for` the element or text that proves the page rendered (an eternal spinner or a timeout here is finding #1 — never screenshot a page you have not waited on).
3. `browser_screenshot` the screen at all four widths of the four-width check — phone (`browser_set_viewport {device:"mobile", width:360}`), tablet (`{device:"tablet"}`), laptop (`{device:"desktop", width:1024}`), desktop (`{device:"desktop"}`) — for every changed screen's resting state and its empty/error state. Each viewport switch emulates size, touch and the matching user agent together, and answers the responsive question in words: whether the page scrolls sideways and which elements overflow. Report what it says at each width; horizontal overflow is a finding.

   **Never pass `width` to `browser_screenshot` after `browser_set_viewport`** — it re-emulates a bare viewport (no touch, no mobile UA) and silently discards the size you set. Check the `viewport WxH` line in every screenshot result matches the width you set.

Interactive flows (login, forms, dialogs): `browser_fill` each field, `browser_click` the submit or action element, `browser_wait_for` the post-action state (URL, toast, new element), then `browser_screenshot` the result. Use `browser_read_dom` for what a screenshot cannot prove — an input's actual value, a disabled/aria state, the exact error text.

The four widths apply to every changed screen's resting state and its empty/error state. Interactive flow steps are captured at 360 and 1440; a flow step needs all four only when a criterion is specifically about layout at that step. This keeps a round to roughly 20 screenshots instead of 80, with no loss on the standard: interactive states still get at least phone width.

Fallback — only for what the browser tools cannot do (console, network, keyboard; see below) or when they report Chrome is missing — drive the system's headless Chromium (`$CHROME_BIN`, `/usr/bin/chromium`, `--no-sandbox` in containers) via `run_terminal`, writing nothing into the workspace:

```bash
QA=${TMPDIR:-/tmp}/tt-<task-key>/qa; mkdir -p "$QA"
chromium --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --window-size=360,800 --screenshot="$QA/01-board-phone.png" http://localhost:5173/board
```

## What the browser tools cannot see: console, network, keyboard

The browser tools show pixels and DOM, not the console, the network or the keyboard. For those, drive a second browser with playwright-cli from `$QA` — it uses the installed Chrome and does not share the browser tools' session, so log in again:

```bash
PW="npx -y @playwright/cli@0.1"; cd "$QA"; $PW open --browser=chrome <url>
# walk the flow: $PW fill / click / press Enter
$PW console error    # must be empty for the flow
$PW requests          # no 4xx/5xx the UI swallowed, and calls go to the real backend, not mocks
$PW route "**/api/<dep>/**" --status=500   # repeat the action to see the dependency-down error state, no backend change needed
$PW close
```

Images from playwright-cli land as files you cannot view in API mode — pixels stay with `browser_screenshot`.

## Visual inspection checklist

Look at each screenshot deliberately — per image, answer:

- Overflowing/clipped/truncated text, overlapping elements, broken alignment or spacing?
- Broken images or icons, missing fonts, unreadable contrast?
- Empty state, loading state, and error state each render intentionally (not a blank area or eternal spinner)?
- Mobile width: nothing unusable, no horizontal scroll?
- Console and network: zero uncaught errors and no swallowed failed requests during the flow (see above).
- Copy: right language for the app's locale, no placeholder text left in, and the longest realistic translation (roughly +30-40% for German/Finnish) still fits at 360.
- Consistency: the same control looks identical across screens, using design tokens — no off-palette colours?
- Touch targets ≥44px on phone?
- Long-content resilience: tried with the longest realistic names/words, not just sample data?
- Navigation collapse on phone: the menu button opens and closes the menu correctly?
- Tables usable on phone: stacked cards or a scrollable container, not squeezed unreadable?
- Form states: inline errors next to the field, visible focus, a pending/submitting state, success feedback?
- No generic placeholder/lorem copy left in?

Accessibility beyond this checklist (axe/Lighthouse scan, keyboard walk) is a separate pass: accessibility-check.

## Evidence

In each criterion's note and each case's `evidence`, one line per screen: width/device, URL, the viewport report, and what the screenshot showed — "360x800 /settings (no horizontal scroll, 0 overflow) — Save button visible under the form, inline error under Email". A screenshot has no file path; never write one. The run log archives every screenshot, so the human can open it there. Findings become need_revision items with that same line as reproduction evidence (bug-report-writing).

## Red Flags

- A UI verdict formed from the diff or from "the build passed" → you have not seen the pixels.
- Screenshots only at desktop width for a layout-affecting change.
- A stuck spinner or blank section dismissed as "probably my environment" → reproduce or report it, never ignore it.
- A `browser_screenshot` call with `width` right after `browser_set_viewport` → the size you set was silently discarded.
