---
name: thalarch-browser-qa
description: >
  Verifies web UI behavior in a real browser using the strongest browser/DevTools/Playwright
  capability actually available on the current host. Use after frontend changes or for
  browser-only bugs. Checks interaction, console, network, responsive behavior, screenshots,
  recordings, accessibility signals, and performance evidence rather than treating a successful
  build as proof.
---

# Thalarch Browser QA

Use a **real browser/runtime capability that actually exists in the current host/session**.
Antigravity may expose a Browser Subagent/Chrome integration; Codex or Claude Code may expose
browser/MCP/Playwright/Chrome tooling differently; some environments may expose none.

Never invent browser evidence, screenshots, console state, network traces, or a browser agent/tool
name because another host supports it.

Do not install a competing automation stack merely for ritual QA when an existing trusted browser
path can prove the requirement. Do not silently install browser dependencies without authorization.

If no usable browser capability is available, perform source/build checks that are still meaningful
and keep browser/visual/interaction claims `UNVERIFIED`.

## QA path

When browser tooling is available:

1. Start or locate the application using repository-native instructions.
2. Use the browser on the real running page, not a generated mockup.
3. Navigate the primary user flow.
4. Verify visible acceptance criteria.
5. Inspect console errors/warnings relevant to the change.
6. Inspect relevant network requests and failures.
7. Capture at least:
   - a compact/mobile viewport;
   - a normal desktop viewport;
   - any specific breakpoint named by the requirement.
8. Capture screenshots for load-bearing visual claims.
9. Exercise changed interactions, not only the initial screen.
10. When useful and supported, preserve a recording/trace artifact showing the flow.
11. For performance work, collect concrete metrics/traces rather than subjective speed.

Use the host tool's actual current schema/capabilities. Do not assume Chrome DevTools, Playwright,
screenshot, recording, network inspection, or device emulation features exist until confirmed.

## Visual stress cases

Select only relevant stress cases:

- long text;
- narrow viewport;
- wide viewport;
- empty/loading/error state;
- open menu/dialog/sheet;
- keyboard focus;
- reduced motion;
- slow image/network load;
- zoom/high text scale where practical.

## Image integration checks

For generated or edited imagery used by a site, inspect the real integration when possible:

- crop and focal point at responsive widths;
- loading behavior;
- contrast behind text;
- resolution/sharpness;
- aspect-ratio stability;
- layout shift;
- fallback/alt behavior;
- asset weight where relevant.

An image can pass standalone QA and still fail inside the page.

## Evidence handoff

Use `thalarch-visual-qa` and an independent design/visual review role when such review capability
exists. Otherwise perform a staged cold visual check in the strongest available context.

A successful frontend build is not equivalent to the user flow passing.
A generated mockup is not equivalent to the implemented page passing.
A browser capability that was not actually invoked is not evidence.
