---
name: visual-debugging
description: Use for screenshot-driven frontend visual debugging and implementation tasks where a target page must match a reference screenshot, mockup, design capture, or expected UI state. Trigger when the user asks to compare a running page against a reference image, recreate a screenshot, fix visual differences, use Playwright for UI inspection, iterate until a page matches a reference, or visually validate responsive desktop/mobile states.
---

# Visual Debugging

## Goal

Use Playwright to inspect a targeted page, compare it against a reference screenshot, make the smallest appropriate UI changes, and repeat until the rendered page materially matches the reference.

## Required Inputs

Before starting, confirm these inputs exist:

- Target page: a local route, URL, component preview, Storybook story, or reproducible command that opens the page to debug.
- Reference screenshot: an attached image or local file path.
- Viewport: use the reference screenshot dimensions when obvious; otherwise infer from the task or ask.

If the target page or reference screenshot is missing, ask the user for the missing item before editing code. Do not guess the intended reference.

## Workflow

1. Establish the runnable page.
   - Inspect the project commands and start the app if needed.
   - Use an existing server when one is already running.
   - Record the exact URL and viewport used for captures.

2. Capture the current state with Playwright.
   - Navigate to the target page and wait for network and UI idle states where practical.
   - Take a full-page screenshot and, when useful, an element screenshot of the relevant region.
   - If fonts, images, canvas, or animations affect the UI, wait or freeze state enough to produce deterministic captures.

3. Compare against the reference.
   - Inspect the reference image directly.
   - Compare layout, spacing, alignment, typography, color, sizing, imagery, borders, shadows, overflow, clipping, and responsive behavior.
   - Prioritize large structural differences before small polish.
   - When visual evidence is ambiguous, use Playwright DOM inspection, computed styles, bounding boxes, and screenshots rather than relying on source-code assumptions.

4. Implement targeted fixes.
   - Prefer existing design tokens, component APIs, CSS conventions, and layout patterns from the repo.
   - Keep edits scoped to the target surface unless shared styling is clearly responsible.
   - Avoid unrelated refactors while matching the reference.

5. Iterate.
   - Re-run Playwright after each meaningful change.
   - Capture a new screenshot at the same URL and viewport.
   - Compare again and continue until the remaining differences are minor or explicitly blocked.
   - Do not stop after a code change without a fresh visual verification unless the app cannot run.

6. Verify responsive states when relevant.
   - If the reference includes multiple breakpoints or the page is responsive, repeat the loop for each requested viewport.
   - Check that text fits, controls do not overlap, primary content is visible, and interactive states still render.

## Playwright Usage

Use available Playwright tools when present. If they are not loaded, discover them with tool search. If MCP Playwright tools are unavailable but the repo has Playwright installed, use the project’s Playwright test runner or a short local script to navigate and screenshot.

Helpful inspection actions:

- Take screenshots at exact viewport dimensions.
- Query bounding boxes for mismatched elements.
- Read computed styles for typography, color, spacing, and box model mismatches.
- Inspect console errors and failed network requests when assets do not render.
- Use screenshot diffs if the project already has visual comparison tooling.

## Reporting

Keep progress updates tied to visual evidence:

- State what changed and why it should move the page closer to the reference.
- Mention the screenshot path or viewport used for verification.
- If a perfect match is blocked, name the specific blocker and the closest achieved state.

Final response should include:

- Files changed.
- Verification performed with URL and viewport.
- Remaining visual differences, if any.
