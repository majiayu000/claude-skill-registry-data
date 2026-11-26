---
name: ui-pass
description: The UI/UX improvement loop for Conch's clients. Capture real screenshots of a flow's states at desktop, desktop-app and phone sizes against a real LiveKit, critique them against the UX rules, file ranked issues with the images, fix with before/after screenshots, and pin each fix with a layout test. Use when asked to review or improve the UI or UX of a flow (talk, stream, chat, sign-in, settings), or before a release that changes how a client looks.
---

# ui-pass

UI bugs in Conch have mostly been found by accident (the blank band under the
composer, #2133; scroll drift, #2173). This skill replaces that with a loop
that looks at the real client, judges it against a written standard, and
proves each fix. It changes how the clients look and behave, never the wire:
no `pkg/schema`, API or reducer changes come out of a UI pass without their
own issue and the usual gates.

## The standard

Judge against, in order:
1. [docs/design/client-experience.md](../../../docs/design/client-experience.md), UX-01 to UX-23. These rules win.
2. The tokens and decisions in [docs/design/browser-ui-polish.md](../../../docs/design/browser-ui-polish.md).
3. Basic heuristics:
   - **State and status:** is it always clear whether I'm in voice, transmitting, muted, sharing or watching?
   - **Cost of a mistake:** is leaving voice or stopping a share unmistakable, and does browsing never look like joining (UX-02)?
   - **Consistency:** do the browser, desktop-app layout and phone show the same state the same way?
   - **Text:** truncation, wrapping, long names, many people.
   - **Accessibility:** WCAG AA contrast, visible focus, a sensible tab order, 44 px touch targets on phone, and nothing conveyed by colour alone.
   - **Layout:** no stray scroll, nothing covered or clipped, and stability: nothing jumps when a state changes.

## 1. Capture

The capture lives in `web/e2e/ui-pass/capture.ui.ts`, run with its own config, so it never runs in CI:

```sh
cd web
# Once per checkout: the Node in web/.nvmrc, the locked dependencies and
# Playwright's Chromium (as for `make web-e2e`; no --with-deps locally).
nvm use && npm ci --no-audit && npx playwright install chromium
# The capture, through the repository's own Playwright (npm run e2e).
GOFLAGS=-buildvcs=false conch-headless npm run e2e -- -c playwright.ui-pass.config.ts
# CONCH_UI_FLOWS=talk,stream (default)   CONCH_UI_OUT=<dir> (default web/test-results-ui/shots)
```

The config refuses to run when `CI` is set: the capture is local only.

- **Requirements:** Docker for the pinned LiveKit image, and `conch-headless`, so no window opens on Nick's screens.
- **People:** alice in a 1440×900 desktop browser, bob on a 390×844 phone, and carol at 1215×900 with the desktop app's strip drawn.
- **Desktop app:** the packaged app's voice needs the Rust helper (`make rust-build`), so carol is its layout in the browser. Say so wherever the report calls it the desktop app.
- **States:** each one is screenshotted for every person it concerns. `manifest.json` lists the shots and any step that failed.
- **A failed step is a finding.** Something the flow should reach and doesn't is usually a bug, or a test-ID gap worth fixing.
- **New flows:** add a block in `capture.ui.ts` guarded by `flows.has('<flow>')`. Keep every step best-effort, through `step()`.

## 2. Critique

Open every screenshot with the Read tool and look at it. Read the component code only to explain what you see. For each state, write findings as:

| Field | Content |
|---|---|
| ID | `UI-<flow>-<n>` |
| Where | state, person/size, screenshot file |
| What | what's wrong, in one sentence, from the user's point of view |
| Rule | the UX rule or heuristic it breaks |
| Severity | **S1** wrong or misleading state, broken or unreachable control, data hidden · **S2** confusing, inconsistent across clients, accessibility failure · **S3** polish |
| Fix idea | the smallest change, with the file if known |

Then rank them: S1 first, and within a severity, the ones on the most-used path (talk before settings). Don't pad the list: three real S1s beat thirty S3s.

## 3. Report and decide

Write the findings and the screenshots up as a report for Nick:
- publish it as an Artifact page, with the images inline, grouped by flow and state;
- give the ranked table first, then the state-by-state gallery.

Nick picks what to fix and in what order; he owns UX direction. Don't file or fix before he has ranked, unless he says to.

## 4. Issue and fix

- **File each chosen finding** with the `issue-writer` skill. The Context names the finding ID and embeds the before screenshot (attach it to the issue or link it from the report). The acceptance criteria are what the screenshot should show after.
- **Dispatch** with the `dispatch` skill: `web-engineer`, or codex for crisp CSS and layout fixes. Claim first.
- **Every UI PR carries before and after screenshots** of the states it changes, from the capture: run it on main and on the branch, at the same sizes, each into its own fresh directory so neither overwrites the other or leaves stale shots:
  ```sh
  CONCH_UI_OUT=$PWD/test-results-ui/before-<issue> ...   # on main
  CONCH_UI_OUT=$PWD/test-results-ui/after-<issue>  ...   # on the branch
  ```
  Use the PR body or a docs/design note for a larger change, as `browser-ui-polish.md` did.

## 5. Gate

- **Pin each layout fix with a test** that fails without it, in `web/e2e/16-layout.spec.ts` or the flow's spec. Follow the `P2133`, `P2168` and `P2171` tests: measure geometry (no stray scroll, nothing covered, still in view) and don't compare pixels.
- **Dispatch gate first:** a worker's output goes through the `dispatch` skill's five-gate review before it's committed. What follows adds to that gate; it doesn't replace it.
- **Review:** the PR's one review (codex or the Claude `reviewer`), told to check what the change could clip, cover or move elsewhere. An earlier layout PR captured an unrelated hidden element; give the reviewer the capture so it can compare.
- **Merge** under the usual rules: reviewed, CI green including all web-e2e shards.

## Never

- Change a wire shape, an API or voice behaviour as part of a UI pass.
- Mark a phone or desktop finding fixed from a browser-only check. The capture's sizes are the minimum, and real-device checks stay open until done.
- Add an npm dependency for styling (`web/deps-allowlist.txt` needs Nick's sign-off), or inline styles (CSP `style-src 'self'`).
