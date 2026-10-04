---
name: ui-screenshot-feedback
description: "Use when: adding UI screenshot capture, Puppeteer screenshot rigs, Electron UI review, control-centre screenshot galleries, user journey planning, or reading screenshot comments before UI improvements."
---

# UI Screenshot Feedback

Use this skill when a UI app needs automatic screenshots, control-centre review artifacts, or comment-driven iteration.

Canonical references:

- `docs/guides/UI_SCREENSHOT_FEEDBACK_METHODOLOGY.md`
- `docs/workflows/ui-screenshot-feedback-loop.md`

## Procedure

1. Create or continue a session and write the relevant user journeys.
2. Add stable UI markers: `data-screenshot-subject`, `data-screenshot-route`, readiness marker, and metric selectors.
3. Choose the capture rig:
   - Puppeteer for deterministic automated screenshots and `analysis.json`.
   - Prefer `scripts/ui/lib/screenshotCapture.js` for route-set captures; expose `--save-screenshots`, `--no-screenshots`, and `--save-dom-snapshots`.
   - Electron for persistent control-centre/operator review or desktop-shell-specific behavior.
   - Playwright/MCP for exploratory visual inspection that should later be promoted into a script if it becomes repeatable.
4. Save active screenshots to `docs/sessions/<session>/screenshots/`.
5. Use the Control Center `/?app=screenshot-review` panel to browse saved `analysis.json` runs and write comments.
6. Write `SCREENSHOT_REVIEW.md` with image embeds and evidence notes.
7. Write `SCREENSHOT_COMMENTS.md` so the user can comment and future agents know where to look.
8. Before later UI edits, read `SCREENSHOT_COMMENTS.md`, `.agent/pending_comments.md`, and SVG `agent-comment` groups.
9. Recapture after changes and record the visual judgement plus validation commands.

## Validation

- screenshot script exits cleanly.
- PNGs are non-empty and linked from `SCREENSHOT_REVIEW.md`.
- `analysis.json` reports readiness, browser events, overflow, loading states, and key feature metrics.
- responsive work includes desktop and mobile route entries.
- unresolved comments are either addressed or explicitly left pending.