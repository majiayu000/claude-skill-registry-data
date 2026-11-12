---
name: remotion-architect
version: 1.2.0
description: Remotion 4.0.542 programmatic video — compositions, frame-deterministic animation (interpolate, spring), Sequence/Series/TransitionSeries timing, assets and fonts, Zod props and calculateMetadata, Studio, CLI/SSR/Lambda rendering, licensing. Includes a guide for explainer videos (scene kinds, A/B variants, embedding a Manim clip). Use when building, structuring, rendering, or reviewing a Remotion video project.
---

# Remotion Architect

Targets **Remotion 4.0.542** (React, TypeScript). Produces real Remotion source — `Root.tsx`, composition components, render scripts — not a storyboard or script document (for that, see [demo-script-designer](../../frontend/demo-script-designer/SKILL.md)). Project skeletons and render recipes in [RECIPES.md](RECIPES.md); explainer videos, scene kinds, variants and embedding Manim clips in [EXPLAINERS.md](EXPLAINERS.md); pinned versions in [STACK.md](STACK.md). General React conventions (hooks, component structure) defer to [react-architect](../react-architect/SKILL.md).

## 1. Mental model

- **A video is a pure function of the frame number.** `useCurrentFrame()` returns the frame; the component renders what that frame looks like. Remotion renders each frame independently (often in parallel, on many tabs or Lambdas), so anything not derived from the frame is a bug waiting to happen.
- **A composition** = component + `width` + `height` + `fps` + `durationInFrames` + unique `id`. Duration is a positive integer count of frames, not seconds: `durationInFrames = Math.round(seconds * fps)`.
- **A `<Still>`** is a one-frame composition (thumbnails, OG images).
- **Studio** (`remotion studio`) previews and edits props; **render** produces the file.

## 2. Interview-first protocol

Never scaffold before these are answered, in order:

1. **Output** — video, audio, still, or all three? Dimensions, fps, length, codec/container.
2. **Content source** — fixed scenes, or data-driven (same template, many variants)? See §7.
3. **Assets** — video/audio/images/fonts/Lottie/3D; who supplies them; licenses.
4. **Rendering target** — local CLI, a Node server, AWS Lambda / Cloud Run, or in-browser `@remotion/player` only. See §9.
5. **Licensing** — who is the user (individual, small team, company)? See §10.
6. **Styling** — plain CSS-in-JS/inline, or Tailwind (`@remotion/tailwind-v4`).

## 3. Determinism rules (the ones that break renders)

- **Animate from the frame only** — `interpolate()`, `spring()`, or arithmetic on `useCurrentFrame()`.
- **No CSS `transition`, CSS `animation`/`@keyframes`, or Tailwind `animate-*` / `transition-*` classes.** They run on wall-clock time, so frames render inconsistently or not at all.
- **No `Math.random()`, `Date.now()`, `new Date()`** in render code. Use `random('seed')` from `remotion`, or derive from props. Same frame must yield same pixels on every render.
- **No `setTimeout`/`setInterval`/`requestAnimationFrame` driving visuals.**
- **Use Remotion's media components**, not native tags: `<Img>` (not `<img>`), `<Video>` from `@remotion/media` (not `<video>`), `<Audio>` from `@remotion/media`, `<Gif>`/`@remotion/lottie` for animation formats. Native tags are not frame-synced and don't wait for loading.
- **Async work blocks the render until released.** Fetching data or loading fonts uses `useDelayRender()` (`delayRender` / `continueRender` / `cancelRender`); prefer the hook over the global functions. Always release in `finally` or on error — a leaked handle times out the render (default 30 s).
- **`useCurrentFrame()` is relative to the nearest `<Sequence>`.** Don't pass absolute frames into children of a Sequence.

## 4. Animation

- **`interpolate(frame, inputRange, outputRange, { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })`** — clamp by default; unclamped output keeps running past the range and shows up as drift, overshoot or negative opacity.
- **`spring({ frame, fps, config })`** — physical easing returning 0 to 1. Tune `damping`/`stiffness`/`mass`; pass `durationInFrames` to stretch to a fixed length. Pair with `interpolate(spring, [0, 1], [a, b])` to map to real units.
- **Delay by subtracting frames** (`frame - 20`), or wrap in a `<Sequence from={20}>`; don't branch on `frame > n` to start animations.
- **Easing:** `Easing.bezier(...)` / `Easing.out(Easing.cubic)` via the `easing` option of `interpolate`; springs for UI motion, interpolate for linear timing.
- **Color and path interpolation:** `interpolateColors`, and `@remotion/paths` for SVG path morphing/drawing.
- Prefer a **small set of named animation helpers** (e.g. `useFadeIn(start, duration)`) over repeating `interpolate` ranges; keep durations in named constants in frames.

## 5. Timing and structure

- **`<Sequence from durationInFrames>`** places content on the timeline and shifts its local frame to 0. Use `layout="none"` when you don't want the wrapping `AbsoluteFill`.
- **`<Series>`** chains scenes back to back (each `<Series.Sequence durationInFrames>`); negative `offset` overlaps them. Prefer it to hand-computed `from` values.
- **`<TransitionSeries>`** from `@remotion/transitions` for cross-scene transitions (`fade`, `slide`, `wipe`, `flip`, `clockWipe`). A transition overlaps scenes, so the **total duration = sum of scenes − sum of transitions**; compute it, don't guess.
- **`premountFor`** on Sequence mounts content ahead of time so media and heavy components are ready on the first frame.
- **`<Loop>`**, **`<Freeze>`**, and `<AbsoluteFill>` as the default full-canvas layer; stack layers with DOM order.
- **Structure by scene:** one component per scene, scene durations as named constants (or derived from props/data), a thin root that sequences them. Keep scenes independent so each is previewable as its own composition in a `<Folder>`.
- Derive layout from `useVideoConfig()` (`width`, `height`, `fps`); never hardcode 1920×1080 into scene math.

## 6. Assets, fonts and media

- **Static assets** live in `public/` and are referenced with `staticFile('name.ext')` — never relative `import` paths for media at runtime and never absolute filesystem paths (the bundle runs elsewhere).
- **Remote assets** must be CORS-accessible and reachable from the renderer (Lambda has no local files). Prefer copying to `public/` or object storage.
- **Fonts:** `@remotion/google-fonts/<Family>` (`loadFont()` handles delay), or `@remotion/fonts` `loadFont({ family, url: staticFile(...) })` for local files. Load at module scope or in the root, not per frame.
- **Video:** `<Video>` from `@remotion/media` (recommended; frame-exact extraction with Mediabunny, native buffering). `<OffthreadVideo>` and `<Html5Video>` remain for legacy or specific needs; `Html5Video` is not supported by the web renderer. Trim with `trimBefore`/`trimAfter`, not by cutting the file.
- **Audio:** `<Audio>` from `@remotion/media`; drive `volume` as a function of the frame (`(f) => interpolate(...)`) for fades. Visualise with `@remotion/media-utils` / `@remotion/audio-viz` instead of `AudioContext`.
- **Captions/subtitles:** `@remotion/captions` types; render word-level highlights from timestamps, converted to frames with `Math.round(ms / 1000 * fps)`.
- **Tailwind:** `npx create-video@latest --tailwind` or `npx remotion add @remotion/tailwind-v4`; utility classes for layout and type only — no animation utilities (§3).
- **3D / Lottie / Skia / Rive:** use the matching `@remotion/*` package; each syncs its own clock to the frame.

## 7. Props, schemas and data-driven videos

- **Props are the API of a composition.** Type them; give `defaultProps` that render a complete, representative video in Studio.
- **Zod schema** (`schema` on `<Composition>`) when props need validation, constraints, enums, descriptions or specialized controls (`zColor()`, `zTextarea()` from `@remotion/zod-types`). Since 4.0.516 Studio infers basic controls from `defaultProps`, so a schema is no longer required for simple editing. Install with `npx remotion add zod`.
- **`calculateMetadata`** makes `durationInFrames`, `width`, `height`, `fps` and even the props depend on data or media (fetch JSON, measure a video's duration with `getVideoMetadata`/Mediabunny, transform props). It runs before rendering and is the right place for fetches — not `useEffect`.
- **`inputProps`** (CLI `--props`, `renderMedia({ inputProps })`) override `defaultProps` per render. Treat them as untrusted input: validate with the schema before rendering on a server.
- **Batch rendering:** one bundle, many `renderMedia` calls with different `inputProps`; never re-bundle per video. Recipe in [RECIPES.md](RECIPES.md#batch-rendering-from-data).

## 8. Project layout and tooling

- Entry `src/index.ts` calls `registerRoot(RemotionRoot)`; `src/Root.tsx` lists `<Composition>`s; one folder per video/scene under `src/`. Skeleton in [RECIPES.md](RECIPES.md#project-skeleton).
- Scaffold with `npx create-video@latest`; add packages with `npx remotion add <pkg>`.
- **All `remotion` and `@remotion/*` packages must be the exact same version, with no `^`/`~`.** Mixed versions throw at startup. Upgrade with `npx remotion upgrade`.
- Commands: `remotion studio`, `remotion render <id> <out>`, `remotion still <id> <out>`, `remotion compositions`, `remotion upgrade`. Wire them as package scripts / Task targets.
- `remotion.config.ts` for project-wide render defaults (codec, concurrency, image format, overwrite).
- Keep composition ids stable and kebab-case; they are the public interface of render scripts and Lambda calls.

## 9. Rendering

- **Local CLI** — default for development and one-off videos. Control `--codec` (h264 default; vp8/vp9 for WebM; prores; `gif`), `--crf` (lower = better quality), `--concurrency`, `--props`, `--frames`. Use `--scale` for resolution tweaks instead of editing dimensions.
- **Node SSR** — `bundle()` once, `selectComposition()`, then `renderMedia()` from `@remotion/renderer`. Run inside a queue; renders are CPU/memory heavy. Recipe in [RECIPES.md](RECIPES.md#server-side-rendering).
- **AWS Lambda** (`@remotion/lambda`) — fastest and most scalable; best for videos under ~80 min at Full HD and for bursts of renders. Deploy function and site once, then `renderMediaOnLambda` + progress polling or webhook. Mind AWS concurrency limits and the 15-minute function limit (Remotion splits work across functions). **Cloud Run** (`@remotion/cloudrun`) is the GCP equivalent.
- **In-browser preview/playback** — `@remotion/player` embeds a composition in any React app (`<Player component durationInFrames ... inputProps />`). It plays; it does not export. Client-side export exists via `@remotion/web-renderer` with limits (no `Html5Video`).
- **Docker:** Chrome needs system libraries; use Remotion's documented Dockerfile (see [docker-architect](../../infra/docker-architect/SKILL.md)). Don't use distroless for the renderer.
- **Quality vs. speed:** raise `concurrency` until memory, not CPU, is the limit; use `OffthreadVideo`/`<Video>` over native video; avoid huge `box-shadow`, `filter: blur`, and large `backdrop-filter` regions on every frame — they dominate render time.

## 10. Licensing

Remotion is source-available, **not** plain MIT: individuals and eligible small teams use it free; **companies above the free-tier eligibility need a paid Company License**, and the license terms also cover Lambda render usage telemetry. Before delivering a project for a company, confirm eligibility at <https://www.remotion.dev/docs/license> and tell the user — don't assume.

## 11. Explainer and teaching videos

When the video teaches, plan it with [explainer-designer](../../frontend/explainer-designer/SKILL.md) (scene rule, provenance chips, content file, cues, versions, look check), write its words with [narration-writer](../../frontend/narration-writer/SKILL.md), and read [EXPLAINERS.md](EXPLAINERS.md) for the Remotion side: scenes as a union of kinds with optional `a`/`b` variants, a `style` prop whose default is the old look, charts wired through the schema, embedding a Manim clip ([manim-architect](../manim-architect/SKILL.md)), and render pitfalls.

## 12. Anti-patterns and review checklist

Rules already stated above, checked on review:

- Wall-clock animation (CSS transitions/animations, `Date.now`, timers) and `Math.random()` (§3).
- Native `<img>`/`<video>`/`<audio>`; absolute file paths; un-awaited fonts (§3, §6).
- Unclamped `interpolate`; `frame > n` branching for starts (§4).
- Hand-computed `from` offsets instead of `Series`; transition overlap not subtracted from duration (§5).
- Data fetched in `useEffect` instead of `calculateMetadata`/`useDelayRender` (§3, §7).
- Mixed or `^`-ranged `@remotion/*` versions (§8).
- Re-bundling per render in batch jobs; unvalidated `inputProps` on a server (§7).
- Hardcoded dimensions in scene math (§5).
- A teaching scene that opens with the formula, scene times from a guessed speech rate, a render that overwrote an earlier version, a new look that changes the default render (§11).

Before handing off: `remotion compositions` lists every id; a still of a first, middle and last frame of each composition renders with no console errors; duration constants add up to `durationInFrames`; the license question (§10) was raised.
