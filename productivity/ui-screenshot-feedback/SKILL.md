---
name: ui-screenshot-feedback
description: Automatic UI screenshots, Electron/Puppeteer capture rigging, control-centre screenshot review galleries, user journey planning, and comment-driven UI iteration.
---

# UI Screenshot Feedback

## Scope

Use this skill when developing, testing, or improving UI surfaces that should be visible to agents and reviewable by the user through saved screenshots.

It covers:

- planning user/operator journeys before UI testing.
- adding screenshot/readiness markers to UI controls and routes.
- choosing Puppeteer, Electron, or Playwright/MCP for capture.
- saving screenshots and analysis where the control centre/docs viewer can show them.
- reading and resolving screenshot comments in later UI passes.

It does not replace lower-level Puppeteer or jsgui3 activation debugging skills; use those when the capture rig itself fails.

## Inputs

- UI route or Electron surface.
- Active session folder.
- User journeys or operator tasks being developed.
- Existing screenshot artifacts/comments, if any.
- Stable selectors or files where selectors should be added.

## Procedure

1. **Discover comments first** for existing UI.
   - Read `SCREENSHOT_COMMENTS.md` in the active or linked session.
   - Check `.agent/pending_comments.md` if present.
   - Search linked SVG review diagrams for `<g class="agent-comment">`.

2. **Plan journeys**.
   - Write or update `USER_JOURNEYS.md` for substantial work.
   - Define journey key, goal, start state, steps, visible success criteria, and screenshot selectors.

3. **Instrument the UI**.
   - Add `data-screenshot-subject` and `data-screenshot-route`.
   - Add deterministic readiness markers after async data and client activation.
   - Add feature-specific metric selectors for the stats a screenshot must prove.

4. **Choose capture technology**.
   - Puppeteer: default for automated PNG + `analysis.json` runs.
   - Shared helper: use `scripts/ui/lib/screenshotCapture.js` for route-set capture, optional saving, desktop/mobile viewport passes, DOM snapshots, server startup, browser event collection, and `analysis.json` writing.
   - Electron: use when persistent operator/control-centre shell behavior matters.
   - Playwright/MCP: use for exploratory inspection, then promote repeated steps into scripts.

5. **Capture and save artifacts**.
   - Put active artifacts under `docs/sessions/<session>/screenshots/`.
   - Write `analysis.json` with readiness, browser events, layout checks, screenshot bytes, and app metrics.
   - Use `--save-dom-snapshots` when later debugging should not require reopening a browser.
   - Verify the run appears in the Control Center at `/?app=screenshot-review`.
   - Create `SCREENSHOT_REVIEW.md` with image embeds.
   - Create `SCREENSHOT_COMMENTS.md` for user review notes.

6. **Improve and recapture**.
   - Review image plus JSON evidence together.
   - Make focused UI changes.
   - Recapture identical journey keys and record before/after judgement.

7. **Close the loop**.
   - Mark addressed comments done.
   - Link final screenshots from session notes or hub.
   - Leave follow-ups for comments that still need work.

## Efficient Rig Checklist

- one server start per run unless using an existing `--base-url`.
- one browser launch reused across routes.
- route records with `key`, `path`, `waitSelector`, and optional `readySelector`.
- standard `--save-screenshots` and `--no-screenshots` flags.
- standard `--save-dom-snapshots` and desktop/mobile viewport output when responsive behavior matters.
- fixed desktop viewport and optional mobile viewport.
- subject clipping when full-page capture is noisy or huge.
- clean shutdown in `finally`.

## Validation

- UI render/server checks pass.
- screenshot capture command exits 0 or documents exact blockers.
- `analysis.json.ok === true` for happy-path captures.
- screenshots are visible from `SCREENSHOT_REVIEW.md`.
- comments are read before follow-up UI changes.

## References

- Methodology: `docs/guides/UI_SCREENSHOT_FEEDBACK_METHODOLOGY.md`
- Workflow: `docs/workflows/ui-screenshot-feedback-loop.md`
- Visual/numeric inspection skill: `docs/agi/skills/autonomous-ui-inspection/SKILL.md`
- Puppeteer efficiency skill: `docs/agi/skills/puppeteer-efficient-ui-verification/SKILL.md`
- Existing workflow: `docs/workflows/ui-inspection-workflow.md`