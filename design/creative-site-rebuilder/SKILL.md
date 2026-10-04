---
name: creative-site-rebuilder
description: Analyze a reference URL, screenshot, recording, or existing frontend and rebuild its design logic into an original site. Use for reference-led reconstruction; use creative-web-studio for a new whole-site concept without a reference. Preserve third-party IP boundaries.
---

# Creative Site Rebuilder

Reverse-engineer systems, not stolen pixels.

## Inputs
Accept one or more:
- URL
- screenshot set
- screen recording/GIF
- existing codebase
- design file/export
- user notes about what specifically they like

If browsing tools are available and a URL is provided, inspect the live reference. If only screenshots exist, infer behavior conservatively and label uncertainty.

## Analysis pass

Capture observations in six layers:
1. **Content hierarchy:** what appears first and why.
2. **Composition:** grids, scale, negative space, cropping, section rhythm.
3. **Typography:** role, size ratios, line lengths, alignment, kinetic behavior.
4. **Motion:** triggers, direction, timing, easing, continuity, scroll semantics.
5. **Spatial/GPU behavior:** canvas, 3D, shader, video, particles, camera-like movement.
6. **Implementation clues:** likely DOM/CSS vs canvas/WebGL, sticky/pin strategies, responsive behavior.

Use `references/analysis-rubric.md`.

## Similarity target

Ask what must be similar:
- interaction idea
- pacing
- typography attitude
- section rhythm
- 3D technique
- color/material language
- overall energy

Then intentionally change at least two major dimensions: composition, content structure, palette, type system, central metaphor, imagery, or interaction mechanic. The goal is a new work that captures useful principles.

Before implementation, write an originality ledger with three columns: `retain as generic principle`, `transform materially`, and `exclude`. Pass the resulting thesis, scene purposes, rendering boundary, variants, budgets, and acceptance criteria in the same handoff shape used by `creative-web-studio`.

## IP safety boundary

Allowed:
- observe public behavior and infer techniques
- reproduce generic interaction mechanics
- build a similar technical pattern from scratch
- use user-owned or properly licensed assets
- create an original design inspired by broad traits

Avoid:
- scraping/copying proprietary source code
- reproducing paid prompt libraries verbatim
- downloading or reusing protected assets without rights
- duplicating distinctive text, illustrations, model assets, or exact overall composition when the user has not supplied rights

See `references/ip-boundaries.md`.

## Rebuild workflow

1. Build a static semantic version first.
2. Match hierarchy and rhythm, not pixel trivia.
3. Add the primary motion grammar.
4. Add one signature interaction.
5. Add 3D/shaders only where the reference uses spatial/GPU logic that materially defines the experience.
6. Re-choreograph mobile independently.
7. Add reduced-motion version.
8. Compare visually and behaviorally.
9. Optimize and remove effects that do not contribute.

## When code already exists

Preserve architecture until there is evidence it blocks quality. Identify the smallest components responsible for layout, animation, scroll, and canvas. Refactor boundaries before rewriting everything.

## Visual diff method

Compare:
- first-frame hierarchy
- vertical rhythm and section heights
- anchor/focal positions
- text wrap/measure
- image crop
- entry/exit timing
- scroll thresholds
- camera/object states
- responsive breakpoint behavior

Do not chase exact pixels if doing so reproduces a protected design rather than the user's intended principles.

Compare the rebuilt work against its own acceptance criteria as well as the reference. Evidence should cover desktop, narrow mobile, reduced motion, keyboard/touch alternatives, and any canvas/WebGL fallback; visual similarity alone is not completion.

## Showcase comparison mode

When several references are supplied, build a small pattern matrix: memorable principle, generic technique, distinctive expression to avoid copying, implementation hypothesis, and originality change. Synthesize across references instead of cloning the closest one.

## Output modes

- reference analysis report
- original redesign direction
- implementation plan
- React/Next/Tailwind/GSAP/R3F code
- “inspired by” coding prompt
- gap list between current implementation and reference

## Examples and showcase calibration

Read `references/examples.md` for concrete “inspired by” transformations and confidence labeling. Read `references/showcase.md` to practice extracting transferable principles while preserving clear IP boundaries.

## References
- `references/examples.md`
- `references/showcase.md`
- `references/analysis-rubric.md`
- `references/ip-boundaries.md`
- `references/rebuild-checklist.md`
