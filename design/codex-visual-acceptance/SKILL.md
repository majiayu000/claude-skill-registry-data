---
name: codex-visual-acceptance
description: Use when a UI, HTML note, figure, PDF page, generated image, or visual artifact needs browser/screenshot-based validation; run a native Codex visual acceptance loop with references, viewports, evidence, and iteration.
---

# Codex Visual Acceptance

Validate what a human will actually see. Use this skill for HTML pages, frontend UI, generated figures, rendered PDFs, slide images, generated images, and other visual outputs.

This is the native Codex adaptation of OMX `$visual-ralph` / visual verdict loops as of upstream `oh-my-codex` main `f947e3a`: keep reference-driven checks, screenshot evidence, viewport matrices, visual verdicts, pixel-diff as debug evidence, iteration, and design-system follow-through; replace OMX image continuation helpers, Stop hooks, and `.omx/artifacts` with native Playwright/PDF/screenshot tools and repo-local artifact folders.

## Visual Done Contract

Define done before inspecting:

- visual surface: browser route, HTML file, PDF pages, figure/image, slide, or app canvas
- reference: user screenshot, live URL baseline, generated mockup, existing design, source PDF/page, or explicit acceptance criteria
- states: default, empty, loading, error, interaction, responsive, print/PDF as relevant
- viewports/pages: at least desktop for UI; include narrow/mobile for responsive UI; inspect key PDF/slide pages
- evidence path: where screenshots/renders/diffs will be saved

If no reference exists, state the intended acceptance criteria before judging.

## Workflow

1. Prepare the artifact.
   - Start or reuse the correct dev server when needed.
   - Use static file open only when it is enough.
   - For PDFs, render pages or inspect through PDF tooling.
2. Capture evidence.
   - Save screenshots/renders under the repo's artifact convention.
   - Record viewport, URL/path, page number, and timestamp when useful.
   - Check browser console warnings/errors for browser surfaces.
3. Review visually.
   - Look for blank canvases, broken images, font failures, clipped or overlapping text, unreadable labels, wrong aspect ratios, layout shifts, accidental horizontal scroll, weak contrast, missing states, and occluded controls.
   - For 3D/canvas/video, verify nonblank pixels, framing, movement/interaction when expected, and asset loading.
4. Compare to the reference.
   - Use human visual judgment first.
   - Use pixel diff or overlay as secondary debug evidence for hard-to-localize mismatches.
   - Preserve reference and final screenshot paths together.
5. Iterate.
   - Fix source artifact, regenerate or rebuild, recapture, and re-review.
   - Do not declare success from a stale screenshot.
6. Preserve reusable decisions.
   - Update CSS tokens, component variants, theme files, design notes, or generated-figure scripts when the fix should persist.

## Pass/Fail

Pass only when:

- required viewports/pages were checked
- screenshots or rendered artifacts exist and are inspectable
- console/render errors are absent or explained
- no blank, clipped, overlapping, unreadable, broken, or obviously off-reference elements remain
- remaining differences are documented and acceptable
- source changes that produce the visual result are committed or clearly identified

## Output

Report:

- reference or acceptance target
- surfaces/viewports/pages checked
- screenshot, render, and diff paths
- console/render status
- visual issues found and fixed
- reusable design/source updates
- remaining manual checks or residual risk

## References

Read `references/visual-checklist.html` for a compact acceptance checklist.
