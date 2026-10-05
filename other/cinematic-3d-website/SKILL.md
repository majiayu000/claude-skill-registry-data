---
name: cinematic-3d-website
description: >-
  Use when building a scroll-driven cinematic 3D landing experience for any brand:
  AI-generated photoreal frames displaced into real 3D by depth maps, a scroll-scrubbed
  camera fly-through with weighted-leg pacing and per-leg camera moves, mouse parallax,
  explode-on-scroll shatter transitions, an ember particle field, warp streaks, a live
  in-scene terminal that runs a REAL product demo, a branded preloader, an exit handoff
  into the page below, a self-hosted display typeface, phone gyro parallax, and opt-in
  synthesized ambient sound. Covers 2K image generation via OpenRouter, depth maps, the
  WebGL engine, chrome (nav/consent) integration, the observe-first verify loop, and the
  flag-off ship posture.
---

# Cinematic 3D Website

If `OPENROUTER_API_KEY` is unset, do not abort the whole skill: proceed with
user-supplied frames (or skip Phase 1 generation) and continue depth/engine work
from assets the user already has.

The end-to-end process for building a "fly through the story" landing
experience with realtime WebGL, from a blank repo to a verified flag-off
ship. Every rule below was learned on a shipped production build; every
Gotcha cost real debugging time once. Follow the phases in order.

## Phase 0: Ground rules (non-negotiable)

- **Ship behind a feature flag.** The cinematic replaces a live hero; every
  iteration lands flag-off (prod byte-identical) with a dev preview route.
  Flipping the flag is a deliberate launch decision, never a side effect.
- **Raw three.js, never @react-three/fiber** in Next.js App Router: fiber
  crashes SSR on React internals. Load the canvas via
  `next/dynamic({ ssr: false })`; keep the scaffold component SSR-able so the
  static fallback renders for crawlers and no-JS.
- **Hard mobile / a11y fallback.** Motion gate: prefers-reduced-motion,
  Save-Data, or (coarse pointer AND viewport under ~900px) renders a static
  hero (one frame, stacked copy, CTAs). Zero WebGL on that path. Phase 7
  upgrades this fallback with gyro parallax; it stays zero-WebGL.
- **Honest content only.** If a screen in the scene shows product numbers,
  they must match the public claims. Better: run a REAL API call (Phase 3b).
  A cinematic that lies is a liability.
- Brand colors enter the engine as two props (a cool accent and a hot ember);
  everything else derives from them.
- **Slice-per-commit with full gates.** Each slice (pacing, assets, demo,
  preloader, chrome, typeface, gyro, sound) ships as its own commit: type
  check, lint, FULL test suite, render-verify on the preview, push, then
  watch the CI run to its conclusion in the background. Never stack unshipped
  slices.

## Phase 1: Generate the frames (best models, one key, 2K)

Use OpenRouter (`OPENROUTER_API_KEY` env var; never print it, never commit it).

- Models (verified 2026-07): `openai/gpt-5.4-image-2` (GPT Image 2) is the
  quality leader but slow (~109s per image); use it for the hero frame.
  `google/gemini-3-pro-image` (Nano Banana Pro) is fast with the best
  cross-frame consistency; use it for sequences and all image-to-image work.
- API shape: POST `https://openrouter.ai/api/v1/chat/completions` with
  `"modalities": ["image", "text"]`; the image returns at
  `choices[0].message.images[0].image_url.url` as a base64 data URI.
- **Resolution is a structured field, not a prompt.** Asking for "2048px"
  inside the prompt is IGNORED; the only working lever is
  `"image_config": {"aspect_ratio": "1:1", "image_size": "2K"}`. Provider
  routing is inconsistent: retry a frame that comes back 1024 (2 tries), and
  Lanczos-upscale a stubborn one from its best 1024. Ship 2K: at ~300-430KB
  WebP the sharpness upgrade is dramatic, and a "bandwidth budget" 1024 reads
  as intentional blur to any reviewer. Pair 2K color frames with
  `texture.anisotropy = renderer.capabilities.getMaxAnisotropy()` in the
  engine or oblique displaced surfaces still smear.
- Prompting: one long cinematic art-direction paragraph per frame (camera
  position, subject, palette locked to the brand, "photoreal, volumetric
  light, no text, no watermark"). For sequences, reference the prior frame's
  composition so N frames read as one journey. Templates in
  `references/prompts.md`.
- Review EVERY image by actually looking at it. Regenerate misses; a weak
  frame drags the whole journey.
- Script: `references/gen_stills.py` (set `SIZE_2K=1`). Optimize with
  `references/optimize.py` to WebP quality 82-86.

## Phase 2: Depth maps (what turns stills into 3D)

- Image-to-depth via `google/gemini-3-pro-image`: send the frame plus the
  prompt "Output ONLY a precise grayscale DEPTH MAP of this exact image, same
  framing. Nearest surfaces pure white, farthest pure black, smooth gradient,
  no colour, no text." Script: `references/gen_depth.py`.
- VERIFY each map by eye: near geometry white, background black. A bad map
  produces warped displacement.
- **Regenerate depth after ANY frame change** (2K upgrade, re-roll, crop):
  old maps no longer match the new pixels and the displacement warps.
- **Gaussian-blur every depth map before shipping** (radius ~7 at 1024).
  Sharp depth edges are the number one cause of mouse-parallax "screen tear":
  the plane stretches its texture across each hard near/far transition and
  reads as smearing, not 3D. Blurring spreads the edge across several mesh
  cells so the same displacement becomes a smooth lean. Blur AFTER the eye
  check (blurred maps are harder to review).
- Optimize to grayscale WebP (16-60KB each, 1024 is fine for depth). The
  engine falls back to luminance-as-depth until the real map loads, so frames
  can ship first.

## Phase 3: The engine (references/depth-fly-engine.tsx)

One pinned canvas for the whole scroll range. A single eased progress value
(0..1) drives everything: `eased += (target - eased) * 0.09`.

Nine systems, in dependency order:

1. **Depth-displaced frames**: per-frame subdivided plane (200x120) with a
   vertex shader that samples the depth map, pushes `pos.z` by
   `(d - 0.32) * uDisplace` and adds depth-scaled pointer parallax
   `pos.xy += uMouse * (d - 0.32) * uParallax`. Keep uParallax around 0.4:
   this in-shader XY shift is FAKE parallax that stretches the texture at
   depth edges, and at 0.85 it visibly tears. Carry the strong-3D feel with
   the CAMERA instead: raise the camera-position mouse gain (~0.11/0.08),
   which moves the view against the z-displaced relief for true
   view-dependent parallax that cannot stretch pixels. Cover-fit UVs;
   crossfade opacity `1 - dist/step`; per-frame fly-in zoom; max anisotropy
   on every color texture.
2. **Explode-on-scroll shatter**: a vertex-shader cell grid
   (`hash2(floor(uv * vec2(7,5)))`); shards fly radially and toward the
   camera as `uShatter` ramps over the frame's exit band; the fragment tints
   shards toward the hot color.
3. **Ember particle field**: ~1300 additive points between camera and frames,
   upward drift with mod-wrap, seeded flicker, pointer parallax at its own
   depth rate. This is what makes transitions feel continuous.
4. **Warp light-streaks**: a camera-attached quad with a radial streak shader,
   driven by `uWarp = s * (1 - s) * 4` where s is the max active shatter, so
   it peaks mid-seam and is invisible at rest (skip the draw when idle).
5. **Live terminal monitor**: an offscreen 2D canvas rendered to a
   CanvasTexture on a subdivided, angled plane. It types a real session
   (config-driven lines), animates a progress bar, blinks a caret, gets
   scanlines and a glowing bezel in the fragment shader, floats idly, and
   SHATTERS on exit with the same cell-grid shader. Throttle texture redraws
   (every 4th frame, only while visible). Place it opposite the copy column.
   Phase 3b makes it run a REAL demo.
6. **Cinematic camera**: settle-in intro dolly
   (`camera.z += (1 - intro) * 0.4`, intro eased over ~1.6s), mouse banking
   (`rotation.z = -mx * 0.045`), idle lissajous micro-drift, a
   pointer-velocity "energy" accumulator (decay 0.93/frame) that excites the
   embers and deepens the displacement, PLUS per-leg camera grammar: each
   journey leg gets one move (lateral drift, push-in, rise, yaw sweep) shaped
   by `sin(pi * legProgress)` so the move is ZERO at both beat centers and no
   seam ever pops. While the terminal is up, damp embers ~65% and warp ~50%
   so the product moment reads calm.
7. **DOM intro**: the first beat's copy rises out of blur via a one-shot CSS
   animation, reduced-motion guarded.
8. **Branded preloader veil** (`.gc-cine-loader` in engine.css): a solid
   brand-dark overlay with a letter-spaced wordmark and a thin progress bar
   that counts frame textures as they land, then fades out. Count texture
   ERRORS toward the total too, or one failed asset hangs the veil forever.
   Depth maps are excluded (the luminance fallback covers them). See the
   stacking-context Gotcha before styling it.
9. **Scroll-driven exit handoff** (`.gc-cine-handoff`): a bottom gradient that
   dissolves the journey's floor into the page background token so the
   cinematic never ends on a hard edge. Its opacity MUST be scroll-driven
   (0 through the journey, smoothstep in over the final 20 percent): it sits
   above the beat copy in z-order, so an always-on gradient washes out every
   mid-journey headline. Gradient target is `var(--bg-base)` so it lands
   correctly in dark AND light page themes.

Performance: DPR cap 2, IntersectionObserver + visibilitychange pause, dispose
everything in cleanup.

## Phase 3b: The live demo (the conversion hook)

The terminal should not just replay a script: wire a `runDemo` prop that
calls YOUR real public demo API and types the genuine result.

- **Typing model**: give each terminal line an optional `t0` start time and
  advance a sequential clock (`start = max(clock, line.t0)`,
  `clock = start + chars / CPS`). Appended lines type in order no matter when
  they arrive; the whole transcript stays scrub-safe.
- **Trigger**: a keypress (e.g. "D") gated on the terminal actually being
  visible (`cliOpacity > 0.5`), ignored while focus is in an input/textarea/
  contentEditable, debounced while a demo is running, and re-armed ~6s after
  completion. Append the command line, a progress bar with `t0 = now`, then
  the real result line (hot color) or a graceful busy line on failure.
- Advertise it with a dim hint line ("press D: compress a real document,
  live") only when `runDemo` is provided.
- The demo result is the one number on the whole page a skeptic can verify
  themselves. Never fake it.

## Phase 4: Copy beats (legibility laws)

- Beat text opacity half-width MUST be under 0.5 * step (0.42 works) so
  adjacent beats can never overlap. The failure mode is two double-exposed
  headlines, and it will happen at exactly the transition your screenshots
  skip.
- Never animate `opacity` in a CSS keyframe on an element whose opacity is
  driven inline by the scroll handler: the running animation wins and pins it
  visible. Keyframe the transform only.
- Keep copy in one consistent zone (lower-left) with a scrim; put in-scene
  elements (the terminal) in the opposite zone.
- No em-dashes or fabricated numbers in visible copy.

## Phase 4b: Display typeface

A distinct display face on the beat titles is a large share of the "designed,
not generated" feel, and it costs $0.

- Self-host via `next/font/local` with a CSS `variable` (e.g. `--font-cine`);
  put the variable class on the stage wrapper AND the static fallback root,
  then style `.gc-film-title { font-family: var(--font-cine, inherit); }`.
- **Cascade trap**: if a shared base class (your generic `.title`) sets
  font-family later in the sheet, a single-class override silently loses.
  Use a descendant selector (`.stage .title`) so specificity wins regardless
  of sheet order, and verify with computed `font-family` in the browser, not
  by reading the CSS.
- Tighten display tracking slightly (about -0.015em) at clamp sizes.
- Free faces that work: Clash Display (Fontshare, ITF Free Font License,
  self-hosting allowed; commit the woff2 plus a license README) reads
  premium-2026; Instrument Serif is the editorial risk; avoid defaulting to
  Space Grotesk (a recognized AI-default tell).
- Font choice on a flag-off surface is a reversible design fork: pick by
  evidence, ship it, let the owner veto on the rendered result. Do not stall
  the build on a taste question.

## Phase 5: Pacing (weighted legs + linger remap)

Implemented in `references/stage-template.tsx` as `LEG_WEIGHTS` +
`journeyProgress()`:

- **Weighted legs**: hero and payoff legs get more scroll distance than
  transit legs (e.g. `[1.3, 0.9, 0.95, 1.25]`).
- **Linger remap**: within each leg, a smoothstep
  (`s = x * x * (3 - 2x)`) lingers at both beat centers (zero slope) and
  accelerates through the seam.
- **Invariants**: f(0)=0, f(1)=1, monotonic. Scroll is a scrubber; the remap
  must reverse exactly, and seam frames must be untouched.
- **Seam velocity law** (credit: scroll-world): camera velocity must never
  reverse across a transition. Keep all transition effects parameter-driven
  (pure functions of progress), never time-based one-way, and they reverse
  cleanly for free.
- **Camera grammar by concept**: product or luxury = slow half-orbit;
  industrial = low lateral track with foreground parallax; travel =
  rise-and-reveal then descending swoop. Encode each as a per-leg
  `sin(pi * x)` arc so it zeros at beat centers.

## Phase 6: Chrome integration (nav, consent, page seam)

The cinematic lives under your site's global chrome. Audit what actually sits
on top of it:

- **Nav**: the right pattern is scroll-aware transparency: a background layer
  at `opacity: scrolled ? 1 : 0` (threshold ~50px) with blur when on. If your
  nav already does this, the cinematic needs NO nav change: verify computed
  opacity at scroll 0 instead of rebuilding.
- **Consent banner**: a full-width bottom bar sits directly on the payoff CTA
  and reads as damage. Reshape it into a compact corner card (max-width
  ~340px, radius 12, same copy, same choices and handlers: geometry only).
  This improves every page, not just the cinematic.
- **Exit seam**: the Phase 3 handoff gradient must target the PAGE background
  token so the dissolve lands in both themes.

## Phase 7: Phone gyro parallax (the mobile cinematic)

The static fallback upgrades to a gyro-driven hero with zero WebGL:

- Listen to `deviceorientation`; clamp gamma to about +/-30 and use
  `beta - 45` (a phone held naturally sits near beta 45); map to a max
  ~14px/10px translate; lerp at 0.08/frame; apply
  `scale(1.12) translate3d(...)` to the background layer with the parent
  `overflow: hidden`.
- Respect `prefers-reduced-motion` (skip entirely).
- **iOS 13+**: `DeviceOrientationEvent.requestPermission()` exists and MUST
  be called from a user gesture. Bind on the first tap; stay static if
  declined; never prompt on load. Desktop and Android bind immediately
  (no requestPermission function).
- Verify without a phone: browser-devtools emulation with viewport
  `390x844x3,mobile,touch` flips `pointer: coarse` so the fallback mounts;
  then dispatch a synthetic
  `new DeviceOrientationEvent('deviceorientation', {beta, gamma})` and assert
  the transform moves in the expected DIRECTION with the expected x/y RATIO.
  Assert the vector, not the absolute settle: rAF runs slow under emulation
  and repeated synthetic dispatches through devtools bridges are unreliable.

## Phase 8: Opt-in ambient sound (references/cinematic-sound.ts)

Fully synthesized, so there is no audio asset to license:

- Graph: a 4s brown-noise loop (leaky integrator over white noise) into a
  lowpass (base ~180Hz) into a gain (0 at rest, ~0.055 on).
- **Opt-in only**: construct NOTHING until the user hits a small "sound"
  toggle chip; create the AudioContext inside that gesture (autoplay-policy
  safe); `setTargetAtTime` ramps for click-free on/off; dispose on unmount.
- Feed journey progress: brighten the filter and lift the gain through the
  transit legs with a `sin(pi * p)` arc, settling darker at the payoff.
- Verify: click the toggle and assert the pressed state flips (a failed
  AudioContext build returns false and the label stays "enable"), scroll with
  sound on (no errors), toggle off.

## Phase 9: Verify like a director (observe-first)

1. Type-check and lint, then run a dev server with the flag on.
2. Screenshot the MOMENTS, not even intervals: the intro after it settles,
   each seam mid-shatter, every element's entry and exit band, the terminal
   AFTER it finishes typing, pointer far-left vs far-right (parallax proof),
   and the exit hand-off into the page below.
3. Check seams in BOTH scroll directions.
4. Read the console. Any WebGL or three.js error is stop-the-line. The classic
   silent killer: a uniform used in both shader stages with different
   precision fails VALIDATE_STATUS and the mesh just does not draw. Declare
   `precision highp float;` in fragments that share uniforms with the vertex
   stage.
5. The full expanded checklist (preloader lifecycle, handoff opacity at
   mid vs end, live-demo network receipt, gyro vector, sound toggle) is in
   `references/verify.md`.

## Phase 10: Ship loop (per slice)

1. Full gates: type-check, lint, the WHOLE test suite (a scoped run hides
   stacked failures). If the full suite fails with timeouts near the per-test
   limit under parallel load, rerun the failing files in ISOLATION before
   believing the red: pass-in-isolation means load flake, not a break.
2. Render-verify the slice on the preview route with tool-measured receipts
   (computed styles, network calls, screenshots), not eyeballs.
3. Commit flag-off (mention receipts in the body), push, and watch the CI run
   to its conclusion in the background. CI-green is the receipt; a local pass
   is not.
4. The flag flip to prod is the owner's explicit call, never automatic.

## Phase 11: Archetype B — the editorial-fusion landing

Phases 1-10 build **Archetype A**: the full-bleed scroll-scrubbed journey
(pinned canvas, copy beats crossfading over a camera flight). There is a
second shape worth mastering: **Archetype B, the editorial fusion** — the
layout language of the best 2026 dev-tool sites, powered by your WebGL stack
where it counts. Ship A as the immersive experience, B as the conversion
landing; they share every asset and the engine.

**Step 1 — study a reference live** (`references/study-a-reference-site.md`):
screenshot ladder + tech probe + section outline. The recurring finding: the
"$50k feel" on these sites is CSS keyframes + IntersectionObserver + stills —
zero WebGL. Their moat is layout discipline; yours is the engine. Fuse them.

**Step 2 — adopt the layout system** (all observed live, all cheap):
- **Tokens**: near-black base, ALL body copy in a mono face, display face for
  headlines only, ONE accent spent only where data lives.
- **Eyebrow spine**: `SECTION-NAME` with a glowing accent dot, mono-uppercase,
  opens every section.
- **Product-as-hero-art**: a window-chromed panel bleeding past the hero
  column beats abstract art — and yours runs the LIVE depth relief inside it.
- **Zig-zag rows**: left copy / right real product panel, alternating.
- **Contrast inversion**: one light section (grid-paper bg, border-matrix
  cells) as rhythm, not theme.
- **Settle discipline**: ONE entrance reveal per section (single
  IntersectionObserver, `data-*` markers, fire-once, unobserve), then
  stillness. Perpetual motion only for cursor-blink-class elements. This
  makes reduced-motion support nearly free: add `.is-in` to everything.
- **Honesty guard**: pre-traction, a measured-facts marquee (every number
  test-locked) replaces the logo wall. Never invent logos or metrics.

**Step 3 — mount the engine in hero mode** (the fusion move):
- Reuse the SAME depth-fly canvas with `progressRef` pinned at `0`: idle
  drift + mouse parallax with no scroll scrubbing.
- **Minimum 2 frames/depths** even in hero mode — the camera math needs a
  valid leg; 1 frame renders black.
- Gate the canvas on `pointer: fine` AND motion-OK; a static
  `background-image` still fills the same box otherwise.
- Mount inside a window-chrome card whose canvas box has a fixed
  `aspect-ratio` — the engine sizes to its mount (`clientWidth/Height`), so
  the wrapper defines the stage.
- Cinema break: one full-bleed still with rAF-throttled scroll parallax
  (`scale(1.18)` headroom so translation never reveals edges).

**Step 4 — the live terminal section**: click-to-run against a real
no-auth demo endpoint, sequential-clock line typing, a graceful error line,
and a RUN AGAIN state. This is the section a static competitor cannot copy.

Template: `references/editorial-fusion-template.tsx` +
`references/editorial-fusion.css` (verbatim from a shipped build; adapt
points in the header).

## Design lessons (what actually makes it feel world-class)

1. **Continuity beats fidelity.** Gorgeous stills that crossfade read as a
   slideshow. The wow lives in the systems that BRIDGE frames: persistent
   particles, seam energy, a camera that never stops moving.
2. **Show the product doing something real.** The most-praised element is a
   terminal typing an honest session; a keypress that runs a REAL API call is
   stronger still. Generic beauty is ignorable; a live product moment is the
   conversion hook.
3. **Interactivity is the moat of realtime over video.** Depth-scaled
   parallax, banking, cursor energy, gyro on phones: none are possible in a
   pre-rendered scrub.
4. **Transitions ARE content.** An explode-on-scroll beats any crossfade.
   Peak intensity mid-seam with `x * (1 - x) * 4`.
5. **Sharpness is a feature.** 2K frames plus max anisotropy changed the
   perceived quality more than any shader tweak. Do not pre-optimize to 1024
   on a bandwidth hunch; the reviewer reads it as blur.
6. **Legibility is a hard law.** Text bugs, not 3D bugs, are what make an
   ambitious build read as broken.
7. **The frame around the art matters.** Preloader, exit handoff, quiet nav,
   compact consent, a real display face: the chrome pass is what moves the
   build from "impressive demo" to "designed site".
8. **Ship behind a flag** so ambition can move fast while prod stays inert.

## Gotchas (each cost real time once)

| Trap | Fix |
|---|---|
| @react-three/fiber SSR crash | raw three.js + dynamic ssr:false |
| `position: sticky` dead under an ancestor overflow clip | manual fixed/absolute pin driven by the scroll handler |
| Beat text double-exposure | opacity half-width under 0.5 * step |
| CSS keyframe opacity vs inline fade | keyframe transform only |
| Shader VALIDATE_STATUS false, mesh silently invisible | match uniform precision across stages |
| Prompt-level "2048px" resolution request | ignored; use the structured `image_config` field, retry small returns, Lanczos-upscale stubborn frames |
| 2K frames still smear at oblique angles | `texture.anisotropy = getMaxAnisotropy()` |
| Depth maps stale after a frame upgrade | regenerate depth whenever the pixels change |
| Mouse parallax reads as "screen tear" smearing, not 3D | texture stretching at hard depth-map edges; Gaussian-blur the depth maps (radius ~7) AND drop the in-shader XY parallax to ~0.4, moving the 3D feel to camera-position mouse gain against the z relief |
| Preloader veil renders UNDER the copy overlays | an explicit `z-index` on the canvas host creates a stacking context that traps its children; remove it (DOM order already layers the canvas below) |
| Preloader hangs forever on one bad asset | count texture onError toward the loaded total |
| Exit-handoff gradient washes out mid-journey copy | scroll-drive its opacity (0 until the final leg) since it sits above the beats |
| Display font silently not applied | a later single-class base rule wins; use a descendant selector and verify COMPUTED font-family in the browser |
| Terminal lines type out of order when appended late | sequential clock with per-line `t0`, never per-line absolute timers |
| Demo hotkey fires while user types in a form | ignore when target is input/textarea/contentEditable; gate on terminal visibility; re-arm on a timer |
| iOS gyro dead | requestPermission needs a user gesture; bind on first tap, static on decline |
| Sound blocked by autoplay policy | create the AudioContext inside the toggle gesture, nothing at load |
| Dev server serves a STALE compile through restarts and a build-dir wipe | two causes seen: (a) a stray lockfile in a PARENT dir makes the bundler misinfer the workspace root (set the bundler root explicitly in local dev); (b) a PWA service worker caches chunks at the fetch layer (never register the SW in dev, and actively unregister leftovers) |
| Full-suite test timeouts at ~the per-test limit | parallel-load flake: rerun the failing files in isolation before believing the red; never run two full suites concurrently |
| Screenshot shows the wrong scroll position | the page can move between an evaluate and a screenshot call; re-scroll and capture in immediately adjacent calls |
| Pillow on Windows | use `C:/` style paths |
| Slow hero model for sequences | gpt-image-2 for the hero only; nano-banana-pro for sequences and depth |
| First-hit dev compile exceeds nav timeout | raise the timeout or retry once |
| `:first-child` misses the first beat | preceding siblings exist; use an explicit class |
| Screenshot too early | eased scroll and typing content need settle time before capture |
| Hero-mode canvas renders black | the engine needs >=2 frames for a valid camera leg even with progress pinned at 0 |
| Live demo works in curl but fails in the browser during dev | CORS preflight: the API allowlist lacks the dev-preview port; test `OPTIONS` (it 400s while direct POST 200s), add the origin |
| "Mobile looks fine" tested by shrinking the window | desktop windows floor at ~640-650px min-width; use DevTools device emulation (`375x812x3,mobile,touch`) and assert `document.documentElement.scrollWidth === innerWidth` as the no-overflow receipt |
| IO reveals re-fire or stagger-jank on scroll-up | fire once and `unobserve` each target; reduced-motion path adds `.is-in` to all targets immediately |
| Cinema-break parallax reveals image edges | give the still `scale` headroom (~1.18) larger than the max translation |
| A gating test run piped through `tail`/`grep` | the pipe exit code (always 0) gates the chain and the filter destroys the failure list; run the gate in its OWN call writing the FULL log, read it, then ship in a separate call |

## References

- `references/depth-fly-engine.tsx`: the full engine, verbatim from the
  shipped production build (nine systems incl. the live-demo terminal and
  preloader veil; raw three.js, config-driven, self-cleaning).
- `references/stage-template.tsx`: the scaffold, verbatim (manual pin,
  weighted-leg pacing, beats, motion gate, exit handoff, typeface wiring,
  gyro fallback, sound toggle). Header lists the adapt points.
- `references/cinematic-sound.ts`: the synthesized ambient engine (drop-in).
- `references/engine.css`: the complete stage styling (pin, beats, copy,
  scrollcue, preloader, handoff, sound chip, static fallback) on CSS tokens.
- `references/gen_stills.py` (2K via `SIZE_2K=1`), `references/gen_depth.py`,
  `references/optimize.py`: the OpenRouter + Pillow asset pipeline.
- `references/prompts.md`: prompt templates and the camera grammar table.
- `references/editorial-fusion-template.tsx` + `references/editorial-fusion.css`:
  Archetype B — the editorial-fusion landing (11 sections, hero-mode engine
  mount, IO reveal system, measured-facts marquee, cinema break, live
  terminal section, light contrast section), verbatim from a shipped build.
- `references/study-a-reference-site.md`: the repeatable reference-site study
  procedure (screenshot ladder + tech/section probes) with the 2026
  editorial-site findings as the worked example.
- `references/verify.md`: the full QA checklist.
