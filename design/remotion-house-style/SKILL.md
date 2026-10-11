---
name: remotion-house-style
description: Create new Remotion compositions that match this project's established visual style — brand colors/fonts, transparent overlay exports, animation conventions, and file/registration structure. Use whenever asked to build a new visual or graphic composition for this channel, regardless of what the composition depicts.
metadata:
  tags: remotion, style-guide, brand, animation, design-system
---

## When to use

Whenever asked to build a new Remotion composition/graphic for this project (list reveals, gauges, timelines, counters, block builds, etc.) that should look and animate consistently with the existing ones. For every composition, also use the `overlay-coordinate-grid` skill: positions are measured off a labelled coordinate grid — on the footage frame when graphics must line up with something in shot, and on your own renders always — rather than estimated. Pair with the `remotion-best-practices` skill for general Remotion API knowledge (fonts, captions, ffmpeg, sequencing) — this skill covers this project's specific design system and conventions, not generic Remotion usage.

## Before you build: propose first

**Always offer a few options before writing any composition code**, even when the
brief looks unambiguous. A one-line brief admits many readings, and the gap
between them is a whole build, not a tweak — so the cheapest moment to be wrong
is before any code exists.

- Offer **three** concepts that are genuinely different *structures*, not three
  treatments of one idea. For each, say what it argues and what its single
  strongest moment is.
- **Recommend one**, in a sentence, and say what the runners-up do better. A flat
  menu hands the decision back without helping make it.
- **Flag anything that would block the build**: a payoff word you'd otherwise be
  guessing (the answer in a question-and-answer piece, the line a lesson resolves
  to), an unusually long duration, or a structure that repeats one already in the
  set.
- **Wait for a pick.** "Create a composition for X" is still a request to propose.

Skip the proposal only when the user has already chosen ("build #2", "do the
gate"), or is asking to change a composition that already exists.

## Brand system

**Fonts are loaded from vendored files via plain CSS, not Typekit and not
`@remotion/fonts`.** The Typekit stylesheet in `src/app/layout.tsx` belongs to the
Next app and is never pulled into the Remotion bundle, so a family that isn't
loaded explicitly silently falls back to `sans-serif` — and one that *appears* to
work may only be resolving because it happens to be installed on that machine,
which breaks on CI or any other computer.

Brand fonts live in `public/fonts/` and are declared as `@font-face` rules in
`src/remotion/fonts.css`, imported by `src/remotion/index.ts`.

**Do not reintroduce `delayRender()` for font loading.** An earlier version of
this used `@remotion/fonts` `loadFont()` with a module-scope
`delayRender()`/`continueRender()` pair. It repeatedly failed in Studio with
`A delayRender() "Loading brand fonts" was called but not cleared after 28000ms`,
taking every render down with it — including compositions that don't draw text at
all, because the handle is global and created before any composition mounts.
Adding a timeout race and pinning the package version did not fix it. An
`@font-face` has no handle to leak: the browser owns the load, and
`font-display: block` holds text back until it resolves.

To add a font: drop the file in `public/fonts/`, add an `@font-face` block to
`src/remotion/fonts.css` with the family name used in `BRAND_FONTS`, and verify it
by declaring the same file a second time under a deliberately fake family name and
rendering that alias against a nonexistent font. If the alias renders correctly the
file is genuinely being used rather than a system install. Remove the probe
afterwards. Currently only `baga` is vendored; `le-havre-rounded`
(`BRAND_FONTS.secondary`) and `Pollen` (`BRAND_FONTS.tertiary`) have no file yet
and render as `sans-serif`.

**Keep every `@remotion/*` package pinned to the same version as `remotion`.** On
a mismatch a package resolves its own copy of `remotion`, so anything relying on
shared module state breaks in ways the error message won't explain. Check with
`npx remotion versions`.

Always import from `src/remotion/theme.ts` rather than hardcoding hex values or font names:

- `BRAND_COLORS`: black `#000000`, pink `#FF37A1`, yellow `#E1FF62`, textPrimary black, textSecondary `rgba(0,0,0,0.7)`, textLight white, trackLine `rgba(255,55,161,0.15)`
- `BRAND_FONTS`: `primary` = "baga" (titles/headlines, semibold weight), `secondary` = "le-havre-rounded" (body/labels, lighter weight), `tertiary` = "Pollen" (accents/special emphasis)

Pink-to-yellow gradients (`linear-gradient(90deg, ${BRAND_COLORS.pink}, ${BRAND_COLORS.yellow})`) are a recurring accent for underlines, progress fills, and gauge arcs.

## File & folder conventions

- One composition per folder: `src/remotion/<ComponentName>/Main.tsx`
- Export the component **and** an async `calculateMetadata` function from the same file
- Component names are plain nouns describing the visual — PascalCase, no "Composition" suffix (`PushUpTypes`, `MaxThreshold80`, `TwoYearTimeline`, `PriorityList`)

## Export / canvas conventions

Existing compositions render as **transparent overlays** meant to sit on top of real footage, not standalone videos. Transparency is the default preference for every new composition unless told otherwise:

- No solid `backgroundColor` on the outer `AbsoluteFill` — either omit `backgroundColor` entirely or set it explicitly to `"transparent"` for self-documentation
- `calculateMetadata` should return `fps: 30`, `width: 1920`, `height: 1080` (unless told otherwise), plus:
  ```ts
  defaultCodec: "prores" as const,
  defaultVideoImageFormat: "png" as const,
  defaultPixelFormat: "yuva444p10le" as const,
  defaultProResProfile: "4444" as const,
  ```
  This is what preserves the alpha channel for overlay use — don't drop it. Both
  halves are load-bearing: `png` because JPEG has no alpha channel and would
  flatten transparency before encoding, and the `yuva…`/ProRes `4444` pair
  because that's what carries alpha through the video codec. Drop either and you
  get an opaque render regardless of the other.
- **Render scale is 2x, and it is NOT a `calculateMetadata` field.** `CalcMetadataReturnType`
  has no `scale` property — scale only exists as a render-level setting. It is set
  once, project-wide, in `remotion.config.ts` via `Config.setScale(2)`, so a
  1920x1080 composition renders at 3840x2160. Don't try to add `scale` to a
  composition's metadata (it won't type-check and wouldn't do anything); to
  override it for a one-off render, pass `--scale=<n>` on the CLI. `remotion.config.ts`
  also pins `Config.setVideoImageFormat("png")` and `Config.setStillImageFormat("png")`
  for the alpha reason above — do not set either back to `jpeg`.
- Choose text/shape colors assuming they'll sit over arbitrary video, not a fixed background: black (as in `PushUpTypes`, `MaxThreshold80`) reads on light footage, light/yellow (as in `TwoYearTimeline`) reads on dark footage. Ask which is likely if it's not obvious from the brief.
- **Known gotcha:** `styles/global.css` (shared with the Next.js app via `src/app/layout.tsx`) applies a solid `body { @apply bg-background }` with `--background: #000000`, and it is imported by `src/remotion/index.ts` — so the Remotion bundle does pull in an opaque body background. In practice rendered frames still come out with real alpha (verified by rendering overlay stills and inspecting them), because the composition's own `AbsoluteFill` is what gets captured, not the page body. If you ever *do* see an opaque background bleed through, fix it in a Remotion-scoped stylesheet imported after `global.css` in `src/remotion/index.ts` (forcing `html, body { background: transparent !important; }`) — don't edit `global.css` itself, since it's shared and its body background is intentional for the Next app.

## Animation conventions

- CSS transitions/animations and Tailwind animation classes are forbidden — everything is driven by `useCurrentFrame()` with `interpolate()` / `spring()`
- Typical easing: `Easing.bezier(0.16, 1, 0.3, 1)` for a snappy-decelerate entrance; `Easing.inOut(Easing.cubic)` for continuous scroll/roll motion
- Typical spring config for staggered card/row entrances: `{ damping: 200, stiffness: 120, mass: 0.8 }`, staggered by offsetting `frame - baseDelay - index * stepDelay`
- Common opener: a title/intro fade + rise (opacity 0→1, `translateY` ~18-20px→0) over the first ~15-28 frames before the main animation begins

## Reusable motifs — pick based on the ask

1. **Staggered card/list reveal** — items spring in one after another, side by side or stacked. See `src/remotion/PushUpTypes/Main.tsx`.
2. **Progress bar / timeline** — SVG line with a moving marker and tick labels. See `src/remotion/TwoYearTimeline/Main.tsx`.
3. **Radial gauge / threshold ring** — SVG arc with gradient stroke filling toward a value. See `src/remotion/MaxThreshold80/Main.tsx`, `src/remotion/Gauge/Main.tsx`.
4. **Block build-up** — counting/building blocks. See `src/remotion/PushUp100BlocksBuild`, `src/remotion/BlocksTimesThree`, `src/remotion/ThreeBlocksReveal`.
5. **Rolling/rolodex list scan** — a long list scrolls through a masked viewport, the centered item is highlighted (e.g. color shift + scale), and it lands on a final item. Good for "sequence through N items until you reach X" briefs, works well for lists too long to reveal all at once (10-100+ items). See `src/remotion/PriorityList/Main.tsx` for a full worked example (100-item scroll with a `mask-image` fade at the viewport edges, `Easing.inOut(Easing.cubic)` for the roll, and a settle-pulse on the final item).
6. **Traveling highlight bar** — a static stacked list where a highlight pill/bar moves down to the active row instead of the whole list scrolling. Better fit than the rolodex for short lists (roughly ≤8 items) where every item should stay visible on screen at once.

When the brief is a list that sequences to a final/bottom item, ask (or infer from list length) whether a traveling highlight bar (short list, everything visible) or a rolodex scroll (long list, masked viewport) fits better.

## Registering a new composition

In `src/remotion/Root.tsx`:

1. Import the component and its `calculateMetadata`, aliasing the latter (e.g. `calculateMetadata as calculate<Name>Metadata`) since every composition file exports a function with that same name
2. Add a `<Composition>` inside the right `<Folder>` — `TYUniverse` for graphics belonging to that video's argument, `Visuals` for general-purpose or reusable ones — with `id`, `component`, `width`, `height`, `fps`, a `durationInFrames` that matches what `calculateMetadata` will compute (this is only the Studio's initial guess before `calculateMetadata` resolves — keep it in sync so the two don't disagree), and `calculateMetadata`

## Sanity check

Render one or two still frames to confirm layout and timing before calling it done:

```bash
npx remotion still <composition-id> --scale=0.5 --frame=<n> out.png
```

(The project default is `scale: 2`, so pass an explicit small `--scale` like this
for quick checks — otherwise every sanity-check still renders at 3840x2160.)

Check a frame partway through the animation and a frame at the final held state (e.g. the last item, the completed gauge). Grid those stills with the `overlay-coordinate-grid` scripts rather than judging positions by eye.
