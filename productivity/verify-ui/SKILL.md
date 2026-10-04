---
name: verify-ui
description: >
  Verify local UI changes in a running app by starting the correct dev server if needed, opening
  the target page in the in-app browser, exercising the relevant flow, checking layout and visual
  behavior, and inspecting console and network errors. Use when the user asks to verify frontend
  changes, check a local page or browser flow, review a UI implementation, test whether a visual
  change works, or confirm that a local feature behaves correctly end to end.
---

# Verify UI

Announce at start: `Running UI verification...`

Validate a UI implementation in a real browser and return a findings report. This is implementation
verification, not a visual glance: "it renders" and "no obvious issues" are not verification.

## Delegation

A browser session is the most context-expensive thing this workflow does: page snapshots, console
dumps, network logs, and screenshots that bill as image tokens, nearly all of it noise once the
verdict exists. Delegate the whole run to a subagent when a delegation mechanism exists, briefing it
with the target route or flow, the run command, what the change was meant to do, and the Output
format below; take back the finished report and let the raw browser traffic die with the subagent.

Run inline when no delegation mechanism exists, or when the user is iterating on a fix and wants to
watch each attempt. The screenshot requirement still applies to whoever runs the flow.

Use `chrome-devtools-mcp:chrome-devtools` via the Skill tool when available - it covers navigation,
interaction, screenshots, console, and network in one surface. Any other browser automation surface
works too. With no browser surface at all, report that verification is **blocked** rather than
describing a UI you did not open.

## Workflow

**Establish the target.** Which app, which route or flow, and whether the user wants a broad smoke
check or a specific scenario. Infer it from the changed files and repo context before asking.

**Start or connect to the dev server.** Find the run command in the repo - documented project
commands, `package.json` scripts, app README or context docs - rather than guessing. Check whether
the app is already running (`lsof -i :<port> | grep LISTEN`, or curl the port) and reuse a healthy
server instead of spawning a duplicate. When starting one, run it in the background, capture the URL
and port, and wait until it is actually reachable. Report a startup failure with its blocking error.

**Open the app and read the current state.** Confirm the page loaded, then note rendering failures,
hydration errors, blank states, broken styling, or auth gates before touching anything. Form a
hypothesis about the intended flow, then act on it - clicking around at random finds nothing.

**Exercise the real flow.** Walk the user path relevant to the change: open the modal and check its
content, focus behavior, and close actions; submit the form and check validation, loading, success,
and failure states; navigate between pages and check preserved state, routing, and data refresh;
resize when the layout is part of the task. Where the implementation clearly has meaningful edge
states, go past the happy path into them.

**Inspect browser signals** during and after the flow: console errors and warnings that indicate
broken behavior, failed or suspicious network requests, loading states that never resolve, layout
breakage - overflow, clipping, overlap, misalignment, missing assets - and interaction regressions
like dead buttons, double submits, focus traps, or stale UI. Console and network issues are real
findings unless they are clearly unrelated noise; a rendered page does not excuse them.

**Capture a screenshot** of the final state before writing the report. It is the artifact that proves
verification happened, so always take it. If the server restarted mid-session, reload and re-exercise
the flow first.

## Output

### Verdict
`Pass` · `Pass with issues` · `Blocked` · `Fail`

### Verified
The route, flow, or behavior checked; the environment and local URL; the major actions performed.

### Findings
Severity, `file:line` when local code or logs already make the cause clear, the exact symptom,
reproduction steps, and the likely cause when reasonably supported.

### Not Covered
Flows, viewports, states, or dependencies left unverified - including partial runs blocked by missing
credentials, feature flags, seed data, or backend failures, a route that could not be reached, or
coverage limited to one viewport or one branch of the flow.

### Evidence
The final-state screenshot, relevant console errors, and failed requests.

Prefer a few high-signal findings over a diary of every click, and name what was actually exercised
rather than declaring success.
