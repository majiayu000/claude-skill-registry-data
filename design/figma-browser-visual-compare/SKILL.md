---
name: figma-browser-visual-compare
description: >-
  Visual-fidelity verification for implementing web UI from Figma. Compares native 4x Figma exports
  with real Chromium rendering, measures both Figma layers and DOM geometry, and inspects expected,
  actual, and pixel-diff images from single atoms up to full compositions. Use it for Figma-to-code
  work, pixel-perfect or high-fidelity UI implementation, Storybook/design alignment, screenshot-diff
  iteration, static visual regression diagnosis, 视觉还原、设计稿对齐、截图 diff、像素对齐, or whenever
  spacing, geometry, typography, strokes, shadows, backgrounds, clipping, or layout do not
  convincingly match the design. Code inspection or a single screenshot is not equivalent evidence.
---

# Figma Browser Visual Compare

Make a browser implementation visually faithful to Figma without turning the production component
into a screenshot-specific mock.

Requires Node.js 22+, pnpm, Git, Git LFS, Chromium or Google Chrome, a reachable local browser target,
and a Figma token with file-content and image-export access.

## Diff-Inspired, Not Diff-Driven

The diff is diagnostic evidence. It says which layer to look at; it does not dictate the
implementation. A lower diff percentage bought with any of the following is a regression, not a pass:

- **Exporting a layer instead of building it.** Never place a Figma export, flattened group,
  whole-section raster, or screenshot-shaped SVG into the implementation so the pixels agree. Text
  stays text and layout stays layout. Export an asset only when the design intends an image or
  illustration and the project has no primitive for it.
- **Transcribing the Figma layer tree.** Understand what the design _is_ before writing markup.
  Groups, wrapper frames, and auto-layout scaffolding are authoring artifacts, not a component
  structure. Reproduce the visual result with the target project's own primitives and a semantic
  hierarchy.
- **Hard-coding sizes.** Keep fixed widths and heights, crop heights, fixed canvases, and forced
  viewports out of production components. Express the intent instead: intrinsic sizing, the project's
  spacing scale, design tokens. Static comparison constraints belong to the story or the run script.
- **Magic numbers and irregular decimals.** Round incidental measurements such as `15.9px` to `16px`
  and resolve them to the project's scale. Keep precise values only where precision is real —
  hairline strokes, nested radii, optical alignment — and record why.
- **Chasing rasterization noise.** Figma and Chromium are different engines for font layout, line
  breaking, antialiasing, and glyph rasterization. Match declared font properties and the intended
  text box. Do not add transforms, per-browser offsets, or altered font metrics to erase glyph-ink
  differences when the line box and composition are already correct. Make an optical adjustment only
  when it visibly improves the real design at normal scale, and record the reason.

## Resolve The Persistent Workspace First

The skill package is immutable. Never edit it, install dependencies inside it, or write run artifacts
into it.

At the start of every invocation, run:

```bash
npx tsx <skill-dir>/scripts/workspace.mts resolve --json
```

- A valid `workspacePath` is the repository to use for the entire run.
- On `WORKSPACE_NOT_CONFIGURED` or `WORKSPACE_INVALID`, ask the user for an absolute destination
  directory. Do not guess a location. Then run `workspace.mts init --path '<absolute-path>'`, or
  `bind --path '<absolute-path>'` when the user deliberately points at an already initialized
  compatible workspace.

The initializer copies the bundled template, creates a local Git repository with no remote, installs
dependencies, creates the ignored `runs-local/` directory, and records the selected path through the
skill's external state pointer.

## Understand The Target Before Coding

1. Read the target repository's agent instructions and existing component patterns.
2. Identify the exact Figma file key and node ID. Never guess a node.
3. Run `pnpm figma:me` in the resolved workspace before other Figma API work. Log only the returned
   account identity; never print or persist the token.
4. Inspect the Figma screenshot and hierarchy. Record the target node's dimensions, layers, layout
   mode, padding, gaps, fills, strokes, effects, opacity, typography, and clipping.
5. Inspect the browser DOM hierarchy and computed layout. Record bounding boxes and the computed
   styles that explain geometry. For a greenfield component, build the smallest structural first pass,
   then inspect that DOM before visual tuning.
6. Decide which constraints belong to the reusable component and which exist only to reproduce one
   static Figma projection.

When Figma MCP tools are available, prefer `get_design_context` for the target node and use metadata
or screenshots to drill down. REST exports remain the source for exact 4x reference PNGs. If a task
requires `use_figma`, load the `figma-use` skill before calling it.

## Work From Atoms To Composition

Start with the smallest independently meaningful piece that explains the larger result: a text run,
icon, logo, button, tab, image mask, or small group. Compare those first, then the containing
component, then the section or page.

Do not start by diffing a full page while several unverified atoms are nested inside it. Large diffs
hide the owning layer and make fixes speculative.

## Create An Iteration

Create one top-level subject under `<workspace>/runs-local/<subject>/iteration-NNN/`. One `run.mts`
may compare many related atoms or states. Treat the script as code-as-config: copy and adapt the
nearest example instead of reducing the workflow to a rigid JSON config.

```text
run.mts
measurements.json
report.json
<comparison-name>/
  01-expected-figma@4x.png
  02-actual-chromium@4x.png
  03-diff-pixelmatch.png
```

Keep implementation code in the target project and only scripts, measurements, screenshots, and
reports in `runs-local/`.

Read `<workspace>/README.md` and the reusable scripts under `<workspace>/scripts/` before writing a
new run. Repository-owned repro fixtures live under the repository's top-level `evals/` directory;
they are evidence for developing this skill, not mutable contents of an initialized workspace.

## Measure Before Capturing

1. Measure the Figma node and relevant descendants.
2. Measure the browser target and relevant ancestors and descendants with `getBoundingClientRect()`
   and computed styles.
3. Choose a viewport that reproduces the static Figma projection while leaving the component
   adaptive.
4. Set a concrete capture background, mandatory for translucent fills, gradients, shadows,
   antialiased edges, and backdrop effects. Composite the Figma alpha over the same color.
5. Wait for fonts, images, animations, and the requested state. Pause videos and disable
   nondeterministic motion.
6. Capture Figma at 4x through the REST images endpoint with `scale=4`, and Chromium with
   `deviceScaleFactor: 4`.

MCP screenshots are good for inspection, but some MCP paths return only the node's natural raster size
even when a larger maximum is requested. Never upscale a 1x Figma PNG and label it `@4x`.

Choose the background from the component's intended Figma ancestor or the real page/story background.
If a detached translucent component has no recoverable background, use `#f5f5f5` as an explicit
fallback and record the assumption. Never choose a background because it reduces the diff.

Do not create a persistent Chrome profile inside the target project, implementation fixture, or run
directory. Use an isolated Playwright context or a task-owned temporary profile and remove it after
the run.

When `tsx` transforms functions passed into `page.evaluate`, Playwright can hit a missing `__name`
helper. Install the compatibility bootstrap before evaluated callbacks:

```ts
await page.evaluate("globalThis.__name = (value) => value");
```

### Effects Outside The Layout Box

Compare `absoluteBoundingBox` with `absoluteRenderBounds` and the exported PNG dimensions. The PNG
dimensions are authoritative for the comparison canvas, `absoluteBoundingBox` for the component's
layout box and semantic anchor; `absoluteRenderBounds` is diagnostic only. When a shadow or blur
expands the reference, create an explicit browser effect canvas around the component and record its
insets. Do not mistake render padding for component padding.

Derive insets from the native export size divided by the requested scale: start from the extra width
and height around the layout box, then distribute it asymmetrically using effect offsets and the
reference image. A vertically centered shadow canvas with `y: 2px` has 2px less inset above and 2px
more below. Record the derivation.

### Equal Canvases On The Pixel Grid

Before capture, verify that `x`, `y`, `width`, and `height` multiplied by `deviceScaleFactor` are
integers. Prefer a measured page clip over a locator screenshot when locator rounding changes output
dimensions, and verify PNG dimensions after capture instead of assuming Playwright emitted native DPR
pixels.

Expected and actual images must have identical pixel dimensions before pixelmatch. If they differ,
stop and classify the cause:

- the component or layout box differs: fix the implementation or the test projection;
- the wrong Figma node or browser selector was captured: fix the capture target;
- a benign text or raster bound differs by a fraction: compare a shared explicit CSS/Figma box, not
  each image's opaque-content bounds;
- padding is genuinely unavoidable: use equal canvases with the same background and an explicit
  semantic anchor, recorded in `measurements.json`. Never silently center-pad.

### Preserve Stroke Ownership

Decide whether a Figma stroke participates in layout. Inside strokes on glass surfaces are usually
visual overlays and must not shrink the content box.

- `border` only when the stroke is structurally part of the box model;
- `box-shadow: inset 0 0 0 <width> <color>` for simple inside strokes that must not affect layout;
- an absolutely positioned, `pointer-events: none`, `aria-hidden` overlay with inherited radius for
  gradient, masked, or multi-layer strokes;
- `outline` with a negative `outline-offset` when its rendering matches the required inside stroke.

This matters most at `0.5px`: Chromium may report a CSS half-pixel border as a computed `1px`,
changing content geometry or thickening the perimeter. Do not compensate with padding until the
stroke sits on the correct visual layer.

Figma effect radius and CSS shadow blur are not universally interchangeable. Start from the project's
existing implementation or Figma-generated CSS, then verify visually with the layout box held fixed.

## Measurement Evidence Contract

`measurements.json` is evidence, not a dump of convenient values. Record at least:

- `capture`: background, device scale factor, viewport, browser clip, expected and actual pixel sizes,
  semantic anchor, effect insets, and any normalization or padding;
- `figma`: target ID/name/type, `absoluteBoundingBox`, `absoluteRenderBounds`, clipping, layout mode,
  padding, item spacing, fills, strokes, effects, opacity, text styles, and a simplified child
  hierarchy;
- `browser`: viewport, device pixel ratio, target and capture rects, relevant ancestor and child
  hierarchy, and computed display/position, box geometry, padding, margin, gap, overflow, fill,
  border, radius, shadow, filter/backdrop-filter, opacity, and typography.

Keep this to the layers that explain the comparison. The REST nodes endpoint returns the subtree but
not its ancestors: use Figma MCP page metadata when available, otherwise fetch the file document at
the shallowest useful `depth` and retain only the target's ancestor path. Never persist a full-file
dump. If the ancestor is unrecoverable, use the real background or the documented fallback rather
than inventing parent styling.

Read [references/artifact-contract.md](references/artifact-contract.md) when writing a new run
script. It defines the result schema, preflight-failure behavior, and stopping rule.

## Compare And Inspect

Use these defaults unless the task documents a reason to differ:

```ts
const threshold = 0.02;
const maxAllowedDiffPercent = 1;
```

After every run, inspect `03-diff-pixelmatch.png`, then `01-expected-figma@4x.png`, then
`02-actual-chromium@4x.png`. Do not rely on `report.json` alone: the report says how much differs,
the images and hierarchies say why.

Classify a visible difference before editing it as geometry or relative position, wrong layout
ownership or hierarchy, a paint difference (fill, gradient, opacity, border, mask, shadow, backdrop),
typography metrics or line wrapping, or rasterization-only noise.

Fix the smallest owning layer, rerun into the next numbered iteration, and keep prior iterations as a
local visual log. Stop when the diff is at or below 1% and inspection shows no unexplained
owning-layer error. Above 1%, run at least one targeted experiment against the largest coherent diff
region; stop only when geometry and hierarchy match and the remainder is convincingly isolated to
engine rasterization or an unavailable asset, with that evidence recorded.

Before finishing, render the component at one meaningfully narrower width — about 25% narrower than
the Figma projection, or a 320px viewport with 16px gutters for fluid components, or a 96px viewport
for an intrinsically fixed small control. This is a sanity check, not another projection: verify no
document overflow, clipping, overlap, or broken wrapping. Record the width and pass criteria.

## Concurrent Runs

The workspace is shared and persistent. Give each task a distinct top-level subject and reserve a new
iteration with an atomic `mkdir`; if it exists, take the next number instead of editing another
agent's run. Never use a shared persistent browser profile. Ordinary runs do not modify package
metadata or the skill.

Compare only states represented by an exact Figma node. Production hover, focus, pressed, loading,
and disabled behavior follows the target project's interaction conventions; do not claim visual
verification for states the design file does not define.

## Completion Checklist

- The production component remains adaptive, uses project conventions, and contains no export-shaped
  raster, transcribed Figma wrapper chain, hard-coded size, or unexplained magic number.
- Static comparison constraints live only in the story or run script.
- Figma and DOM hierarchies were inspected, not inferred from screenshots alone.
- Figma and browser geometry were measured before diffing.
- Every comparison has equal-sized 4x expected, actual, and diff images over a concrete shared
  background.
- The diff, expected, and actual images were visually inspected.
- Remaining differences are explained rather than hidden by a permissive threshold.
- Run artifacts live under `runs-local/`; the skill directory is unchanged.
