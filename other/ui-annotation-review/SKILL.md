---
name: ui-annotation-review
description: Create annotated UI review artifacts from screenshots or browser captures using short notes, arrows, and consistent callouts. Use when Codex needs to mark visual defects, explain UI changes, produce screenshot evidence for PRs/issues/Linear, or publish browser-verified visual proof without relying on a full design tool.
---

# UI Annotation Review

Create clean annotated PNG artifacts for visual review work.

Prefer this skill when the output is a review artifact, not a product feature. Use the app's own annotation UI only when the user explicitly wants in-browser interactive editing.

## Workflow

Choose one of two modes:

1. **Live-page mode**: when Codex can inspect the page in a browser and anchor callouts to detected elements.
2. **Screenshot-only mode**: when the user already has an image and no live DOM context is available.

## Live-page mode

1. Capture the page screenshot.
2. Inject or use the page's structured detector output.
3. Export detections plus viewport metadata to JSON.
4. Write an anchor spec with one finding per callout.
5. Resolve anchors into pixel notes/arrows with `scripts/resolve_anchor_spec.py`.
6. Render the annotated PNG with `scripts/annotate_png.py`.
7. Attach or publish the artifact where the review is happening.

## Screenshot-only mode

1. Capture or locate the source image.
2. Decide whether the artifact needs one screenshot or a short set of screenshots.
3. Write a compact pixel-based annotation spec with one finding per callout.
4. Render the annotated PNG with `scripts/annotate_png.py`.
5. Attach or publish the artifact where the review is happening.

## Capture

For browser flows, capture the page first with Playwright or the available browser tool.

For existing screenshots, work directly from the provided PNG or JPEG. Prefer PNG when the user expects precise UI detail.

If the task includes multiple states, capture them separately instead of crowding one image with too many callouts.

## Structured detections

Prefer structured detections over raw pixels whenever the page is live.

If the page already exposes detector output, use that directly. If not, inject a detector first. For pages using `a11y-overlay`, read detections from:

```js
window.__a11yOverlayInstalled.collectDetections()
```

When the screenshot comes from a scrolled page position, export the current viewport origin alongside the detections. Use the live export pattern in [references/live-anchor-workflow.md](references/live-anchor-workflow.md).

## Annotation rules

Follow [references/annotation-style.md](references/annotation-style.md) before building the spec.

In live-page mode, author callouts against anchors, not DOM selectors. Resolve them into pixel coordinates before rendering.

In screenshot-only mode, use pixel coordinates relative to the image.

Use the schema and examples in [references/annotation-schema.md](references/annotation-schema.md).
For live-page anchors, use [references/anchor-schema.md](references/anchor-schema.md).

## Resolve anchors

Run:

```bash
python3 scripts/resolve_anchor_spec.py screenshot.png detections.json anchor-spec.json pixel-spec.json
```

This step matches each callout to the best detection and generates the note/arrow coordinates for the renderer.

## Render

Run:

```bash
python3 scripts/annotate_png.py input.png spec.json output.png
```

The script draws:
- sticky-note style callouts
- arrow lines with arrowheads
- optional short labels on arrows

If the callouts cover important UI, move the note boxes and rerender instead of adding opacity or shrinking text aggressively.

## Publish

After rendering, attach the PNG to the system of record:
- GitHub issue or PR comment
- Linear issue comment or attachment
- Slack thread
- design or QA handoff doc

When writing the accompanying text:
- keep it short
- match the callout numbering or labels
- do not repeat the full contents of each note if the image already says it

## Examples

Use these packaged examples as known-good fixtures when validating the workflow or showing the skill to someone else:

- [examples/reference-review/README.md](examples/reference-review/README.md): local document-style review on `reference.html`
- [examples/landing-review/README.md](examples/landing-review/README.md): local product-marketing review on `landing.html`

## Resources

- [references/annotation-style.md](references/annotation-style.md): placement and wording rules
- [references/annotation-schema.md](references/annotation-schema.md): screenshot-only pixel schema
- [references/anchor-schema.md](references/anchor-schema.md): live-page anchor schema
- [references/live-anchor-workflow.md](references/live-anchor-workflow.md): browser-side export flow for detections
- [scripts/resolve_anchor_spec.py](scripts/resolve_anchor_spec.py): resolve live anchors into pixel notes/arrows
- [scripts/annotate_png.py](scripts/annotate_png.py): deterministic image annotation renderer
- [examples/reference-review/](examples/reference-review/): packaged reference artifact set
- [examples/landing-review/](examples/landing-review/): packaged landing-page artifact set
