---
name: gsap-explainer
description: 'Build a Kurzgesagt-quality GSAP-powered animated explainer video — a self-contained HTML file that plays like a produced YouTube video: layered worlds, character populations, physics-feeling choreography, a flying host mascot, seekable player chrome. Use when the user wants a high-production explainer/YouTube video, a "GSAP video", or a step up from a CSS-only animated explainer.'
user-invocable: true
---

# GSAP explainer — the produced-video tier

Builds a **self-contained HTML/SVG/GSAP explainer** that reads like a produced YouTube animation, not a slideshow: one GSAP timeline per scene driving physics-feeling choreography, a persistent flying host mascot, layered gradient worlds with depth, character populations, a vignette-and-grain "camera", and a seekable player. Use a CSS-only harness for tiny funnel embeds; use THIS for YouTube-grade content videos.

**The reference build is `scaffold.html`** in this skill folder — a runnable 5-scene worked example (topic: "How Compound Interest Snowballs") with every pattern below in context, retention + zero-overlap passed. It ships with GSAP stripped: run `python3 inline-gsap.py scaffold.html` once (fetches GSAP 3.13 into a gitignored `vendor/`, then inlines it) and open the file — it must play. Read it whenever a pattern below is unclear.

## Start here — the path that cannot fail

1. **Write the shot script FIRST** as a markdown doc: per scene — timestamp, duration, VISUAL, ON-SCREEN text, VO line. End with an accuracy checklist and verify every claim in it. Scene durations become the `SCENES` array; VO lines become the `sr-only` transcript.
2. **Copy `scaffold.html`** to `<topic>.html`. It has every gotcha pre-fixed: harness clock, seek chrome, host flights, world backgrounds, camera overlays, population characters, reduced-motion, transcript. Run `inline-gsap.py` on it and open it before touching anything — it must play.
3. **Replace scenes one at a time**, keeping the five worked examples as your idiom source until each is replaced: S0 = dark hook with a flip-reveal; S1 = drop-with-bounce physics; S2 = pour/motionPath flight + DrawSVG; S3 = the forced-overlap collision proof (the peak pattern); S4 = CTA hold. Update `SCENES`, `FL`, `ACTS`, `CH_STARTS` together — they are parallel structures keyed by scene index.
4. **QA every scene with freeze-frames** (see *QA*), fix, then publish (self-contained file).

Never write a scene's choreography from scratch when a pattern below matches — adapt the pattern. That is how you hit the bar regardless of model.

## Architecture contract (already wired in the scaffold)

- Fixed **800×500 stage** scaled to container (`fitScale`). Scene clock is **setTimeout** (`SCENES` array, seconds per scene; last entry `999` = CTA hold; `advance()` calls `done()` on it).
- **Text/chips/captions enter via CSS primitives** (`.fu` fade-up, `.pp` pop, `.fi` fade-in) with inline `animation-delay` — cheap and replayable. **Hero choreography is GSAP**: `runScene(i)` (called from `showScene`) kills the previous timeline and builds `gsap.timeline()` from `FL[i]` (host flight) + `ACTS[i]` (scene act).
- **Every `ACTS[i]` MUST start with `gsap.set(...)` resets** for all elements it touches — scenes re-activate on replay/seek and killed tweens leave stale inline styles.
- GSAP-owned elements get class `g-hero` (or live inside one) and **never** carry `.fu/.pp/.fi` — one owner per element.
- `pause()/resume()` call `curTl.pause()/play()`; CSS side is frozen by the `.paused` class. **Navigation always resumes playback** (a paused freshly-cut scene sits at opacity-0 entrances — never "seek and stay paused").
- Player: click-to-seek progress bar (`sceneAt(frac)`), prev/next buttons, ←/→ keys, chapter ticks (`CH_STARTS`), autoplay on scroll, auto-pause on tab-hide.
- Deliverable is the **silent visual track** (master stays silent); VO ships as a separate `<name>-vo.html` preview variant built by the ElevenLabs pipeline (see *VO production*). The `sr-only` transcript IS the VO script. Retiming to a read = EXTEND `SCENES[i]` to clip+1.5–2s (extending never strands beats; only trims do).

## The pattern library (adapt, don't invent)

All of these exist verbatim in `scaffold.html` — copy the nearest one.

- **Host flight** — `FL[i] = [[fraction, x, y, pointing], ...]`. First waypoint = previous scene's last (seamless cuts). Long legs auto-swoop via MotionPath (in `fly()`). The pencil tip sits at actor-offset ≈ (−10, +95): to point at a target, park the host **above-right** of it. Send the host offstage (x=850) when a scene needs the frame.
- **Drop with weight** — `gsap.set(els,{y:-300,opacity:0})` then `.to(els,{y:0,opacity:1,ease:'bounce.out',stagger:.09})`. The stagger + bounce IS the physics feel. (`layMarbles` packs rows inside the vessel; row width is 168, not 180 — wider and drops poke through the wall.)
- **Forced-overlap collision (the proof peak)** — two bars drop into one track that can't hold both; the second **tries to dodge** (`x` yoyo), fails, settles; the overlap segment pops in with `back.out` and glows (`boxShadow` yoyo repeat:-1); then two both-badge character minions pop inside it. Intent → failure → consequence is what makes it feel alive.
- **Pour/transform** — container rotates (`transformOrigin` at the spout), contents fly out one-by-one on `motionPath` arcs (`{path:[{x,y},{x,y}],curviness:1.6}, ease:'power1.in'`), land in a row, cross-fade into the new shape drawn with DrawSVG.
- **Flip-reveal** — a tempting ✓ pops (`back.out(2.4)`), wiggles, then swaps for the ✗ slamming in (`scale:3→1, power4.out`) + a background flash (`backgroundColor` yoyo).
- **Tempt-then-shatter** — answer glows/pulses (`scale` yoyo ×3), then dies (`opacity:.25, scale:.92, rotation:-3, power2.in`); the right answer stamps in after.
- **Stamp slam** — `gsap.set(stamp,{opacity:0,scale:2.6,rotation:-14})` → `.to({opacity:1,scale:1,rotation:0,duration:.35,ease:'power4.out'})`.
- **DrawSVG** — `gsap.set(path,{drawSVG:'0%'})` → `.to({drawSVG:'100%'})`; snap-back = draw to 72% then reverse fast. **DrawSVG overwrites `stroke-dasharray`** — dashed lines render solid while drawing; design accordingly.
- **Population as characters** (the single most Kurzgesagt move) — `minion(size, badges)` mini-character factory: quantities are little characters, not dots. Ambient 3-character swarm on 35–55s CSS loops; groups contain their character cast; the proof moment is characters wearing both badges.
- **Scene-cut wipe** (built into `runScene`) — two skewed panels (accent leads, ink trails .09s) sweep the stage at every cut. Leave it on; it's the cheapest "real transitions" win. Prop-rich scene ideas worth stealing: a living page character, a highlighter ruin, a file cabinet, a gauge needle, a progress-bar race.

## The free plugin suite (GSAP 3.13 — ALL free since Webflow's acquisition)

`inline-gsap.py` fetches + inlines core + DrawSVG + MotionPath + **MorphSVG, SplitText, Physics2D, PhysicsProps, CustomEase, CustomWiggle, CustomBounce, Flip, ScrambleText**. Everything is free-licensed. `inline-gsap.py <file>` injects everything + a registerPlugin block at the `<!--GSAP_INLINE-->` marker; `--refresh` swaps the suite in an already-inlined file. Proven patterns (all live in the scaffold):

- **SplitText char cascade** — split ONCE at init via a registry (`splitOnce(key,sel)` caching in `SPL{}` — re-splitting on every scene re-run nests spans). Kicker: chars from `{opacity:0,y:14}`, stagger .016, start ≤.15s. Hero word: chars from `{y:-64,rotation:-9}` with `back.out(1.9)` stagger .07; or `{scale:2.7}` power4 stagger .11 = stamp-slam. Scenes hide via opacity (not display:none) so init-time splitting is safe.
- **ScrambleText definition lock** — a payoff line scrambles into place: `scrambleText:{text:'≥ 1',chars:'<>=~≠≤≥',speed:.6}`. Prefer JS `\u` escapes for symbols in JS strings. Themed char sets (math symbols for definitions) read better than 'upperCase' — a long random-caps scramble reads as a loading glitch.
- **CustomWiggle settle** — `CustomWiggle.create('wigSettle',{wiggles:4,type:'easeOut'})`, then `rotation:'+=10', ease:'wigSettle'` — oscillates and RETURNS TO START, so relative values never accumulate across replays. Use for: stamp landings, character reactions, the host's pencil tap-tap on arrival (`if(wp[i][3]&&!wp[i-1][3])` in `fly()`).
- **CustomBounce drop with squash** — `CustomBounce.create('thud',{strength:.58,squash:2.4})` creates paired eases `'thud'`+`'thud-squash'`. The `drop(tl,targets,time,dur,stagger)` helper runs 3 synced tweens: opacity pop, `y` with 'thud', `scaleX:1.45,scaleY:.55` with 'thud-squash' (`transformOrigin:'50% 100%'` in the reset). Strictly better than `bounce.out` — the squash IS the weight.
- **Physics2D burst** — `burst(tl,scene,x,y,n,time,colors)`: celebration/debris particles where landing doesn't matter (collision peaks, victory stamps). Index-seeded angles/velocities (`(i*53)%140`) = replay-identical, no Math.random. Removes stale `.pfx` on re-entry; fade-out before scene end so nothing lingers.
- **MorphSVG fuse** — the top Kurzgesagt move: N objects "become" the concept. Items land in a row → a capsule path fades in over them → `morphSVG` to the arrow silhouette while `fill` tweens ("same objects, new shape", literally). Reset needs `gsap.set(path,{morphSVG:ORIGINAL_D})` — a morphed path keeps its mutated `d`.
- **Flip: DON'T, here** — in a fixed 800×500 absolute-coordinate stage you always know the delta; a plain `y:` tween is deterministic under `tl.pause(t)` QA, while Flip's measure-at-runtime breaks freeze-frame scrubbing (and callbacks don't fire on suppressed seeks). Flip earns its keep only in real reflow layouts (DOM-driven lists, responsive containers). A "claim the vacated spot" beat is a known-delta tween.

## Asset craft (10x-pass patterns — how props stop looking like styled divs)


> Deep-dive: the full asset-generation discipline (build order, factories, SVG contracts, quality gates) lives in the **explainer-assets** skill — use it whenever CREATING or rebuilding an asset; this section is the quick reference.

- **The one-recipe sticker** — depth entirely from layered `box-shadow`: hard down-right ink drop (`3px 3px 0 var(--ink)`) + `inset 0 2px 0 rgba(255,255,255,.3-.5)` top gloss + `inset 0 -3px 0 rgba(0,0,0,.1)` bottom shade + `inset 0 0 0 1-2px rgba(255,255,255,.14)` die-cut rim. Translucent insets ride ANY background color, so one CSS pass on `.xchip/.qbar/.stamp/.l3 span` elevates every variant, light and dark. Keep one radius scale (sm 10 / base 13 / lg 16) and ONE light direction (top-left) film-wide.
- **Two-tone any flat fill** — swap `background:rgba(...)` for `linear-gradient(180deg, lighter, base)` + the gloss/shade insets. Semantic color survives; the surface reads lit.
- **Crafted-vessel recipe** (buckets/jars/cups) — base-shadow ellipse → gradient body → 2 tapered hoop bands with 1px white highlight → rim ring + a DARKER INNER-OPENING ELLIPSE (that one dark ellipse is what makes a mouth read 3D) → soft specular curve. Interpolate band endpoints along the trapezoid sides.
- **Crafted line-art in one selector** — static `filter:drop-shadow(0 1.5px .5px rgba(0,0,0,.17))` on all drawn strokes gives every arrow/box a 2-tone underside and reveals WITH the DrawSVG animation (filter is independent of dashoffset).
- **Decorate GSAP-driven props with pseudo-elements** — `::before/::after` (ruled lines, tape strips, cracks, meniscus lines) ride the timeline's transform automatically: zero new choreography, zero footprint change. Track which pseudos are "taken" per class — collisions are silent.
- **Factory characters: ids only on singletons** — the host (one instance) may carry `uid`-suffixed gradients/speculars; a many-inlined factory (mini-characters) must stay id-FREE (plain fills only) or ids duplicate across the document.
- **Preserve the choreography contract while re-crafting** — build a selector inventory from the script FIRST; positional selectors are landmines (`.bkt3 path` = FIRST path must stay the tweened body — lead with ellipses, not paths). New decorative transforms go on wrapper `<g>`s.
- **Text-safe gloss caveat** — on chips carrying SplitText/hero text, gloss must be inset box-shadows (paint UNDER text), never a positioned `::before` overlay (paints OVER the chars and dims them).
- **Paper-stack + dog-ear recipe** (any sheet prop) — 2 offset back-rects (±0.6–1.5° rotate, darker cream, `overflow:visible` on the svg), corner-cut shadow triangle + folded flap, a margin rule, top-left sheen path. Footprint unchanged, only visual bleed.
- **Drawer/furniture front kit** — front rect + top gloss strip + label plate + recessed handle bar + inter-unit depth-shadow line; parameterize palette for the highlighted unit, keep its animation class.
- **2-tone vector cloud** — tinted base ellipse + 3 overlapping white circles + one brighter top ellipse; recolor the base tint per mood variant.
- **Blueprint-card overlay** — absolutely-positioned child svg (faint ruled grid + 4 corner ticks) as a card's first child: technical-drawing texture with zero effect on the card's tween class or text child.

## The cinema layer (Kurzgesagt-pass patterns)

- **Camera rig `#xplCam`** — a content-only wrapper INSIDE `#xplStage` holding the scenes (env layers, actor, vig/grain stay outside). Per-beat push-ins on payoffs (~1.02–1.05, transformOrigin at the hero), pull-outs on reveals, reset scale to 1 in `runScene` every cut. Never scale `#xplStage` itself — that's `fitScale`'s. The peak scene earns ONE unbroken slow creep across its whole act. Check clip risk against the VISIBLE pill/prop bounds, not full-width containers.
- **Host acting handle `actorBody`** — `.xpl-actor > [data-host]` div, independent of `fly()` (outer x/y) and `armEl`. Helpers: hop (y-8 yoyo), lean (±4° toward pointed target), startle (recoil+tilt), 360 spin at the biggest win. Reset each cut. Mini-character entrance personality: peek from behind an edge (x offset → 0) BEFORE the pop.
- **Payoff light** — one shared `#xplGlow` blurred radial (`mix-blend-mode:screen`, tint via CSS var), positioned + bloomed behind the hero object at each scene's biggest beat, reset per cut. Instant "lit" feel for ~15 lines.
- **Time-of-day drift** — seed a base `filter` on `#envFar` at init (so tweens interpolate, never jump from `none`), then ease brightness/hue per chapter in `runScene`. Composes with the CSS translate loop and the GSAP x dolly because it's a different property.
- **Hybrid injection into a CSS-only harness** — CSS beats stay the base layer; a guarded `GACTS{}` + `runG(i)` bridge (called from showScene, wired into pause/resume, expose `tl()` on `__xpl`) adds GSAP hero accents to money scenes only. Everything additive, `typeof gsap` guarded, FX classes swept per cut. The file must still play if GSAP never loads.

## Movement craft (10x Wave B patterns)

- **Anticipation windup on any slam** — one pre-frame of reverse motion sells weight: `scale .975` (cards) or `.86` (stamps) with `power2.in` BEFORE the overshoot + elastic/back settle. One keyframe, deterministic under `tl.pause()`.
- **CSS-owned-motion rule (hybrid files)** — if a CSS keyframe animates the `transform` SHORTHAND on a node, GSAP cannot layer rotation/x/y there (the running animation overrides inline styles). Let CSS own the motion; GSAP sells it with impact FX synced to the CSS times (dust puffs, impact rings, a racing bloom along the cascade). Bonus: no reset burden on nodes GSAP never touches.
- **Frame-shake in a CSS-base file → actor startle instead** — the scene container's transform is reserved by the Ken-Burns animation, so container shakes are invisible; use a host recoil+tilt (`wigSettle`, returns to rest).
- **`dust()` vs confetti** — impact dust = low velocity (54–94), low gravity (~140), near-horizontal angles, round, `box-shadow:none`, quick fade; keep `.pfx` class for the per-cut sweep.
- **Tight-band placement audit** — measure in logical stage coords (`(rect − stageRect)/scale`); when a caption is squeezed between a prop and a FROZEN lower-third with <1.3× line-height clearance, move the PROP, not the caption.
- **Follow-through = trailing micro-tween, not a bigger yoyo** — knees-give dip after a hop landing, overshoot-past-neutral on a lean return; 1–2 frames, always ending at 0 (reset-safe).
- **Anticipation on rotators: relative windup, absolute swing** — `rotation:'-=6'` cock-back then rotation to an ABSOLUTE target; the absolute overwrites the relative so nothing accumulates across cuts.
- **Host no-fly zones** — the kicker band (y<70) and any full-width sub/caption line are the two chronic overlap traps at final-beat freeze. Park in the gap between text bands, at a diagram's arrowhead, or in the right margin (`x ≈ stageW−90`) so only the pencil tip crosses onto the target ("ticking it off"). Body-edge-to-text gap ≥24px; verify at the exact HOLD fraction, then re-chain the NEXT scene's fraction-0 waypoint (seam continuity).
- **Programmatic lower-third sweep before publish** — goto each scene, compare every content box vs the `.l3 span` box; only full-stage glow/flash overlays may overlap.
- **Sync a swell-FX's PEAK, not its start** — if `bloom()` peaks at start+0.5s, call it at beat−0.5.
- **`#xplCam` x is a free impact-shake channel** — scale carries the creep, x/y are zeroed every cut by runScene, so a decaying x-shake (amp 3→0, 5 steps) composes with an ongoing push at zero reset cost.
- **MotionPath + back.out = arc-and-settle in one tween** — for ≥150px non-collision slides; the ease returns exactly to the final path point (deterministic under pause). Keep head-on collisions and card-stack reveals STRAIGHT — arcing weakens the metaphor.
- **Even 1px yoyos need their axis in the reset** — a cut mid-oscillation strands the offset; the replay-reset audit (interrupt mid-beat → re-enter → getProperty) is the tool that catches it.

## VO-sync choreography (the "say it = show it" contract)

- **The named object moves ON its name.** Walk the transcript sentence-by-sentence; estimate speech time word-proportionally within the scene; the corresponding visual must have a beat within ±1.5s. Classify every content phrase SYNCED / MISTIMED / WRONG-OBJECT / DEAD before calling a scene done.
- **Enumerations reveal WITH the roll-call, not before.** The chronic defect: multi-item reveals (4 bricks, 6 icons, 3 rows) all land in the first 2-8s while the VO names them across 15-20s. Space each item's entrance to its name; let the item's dust/label/stamp travel with it.
- **Payoffs resolve WITH their reasoning, never before.** A ✓ that stamps 5s before the VO finishes the argument spoils the peak. Gate winner-stamps, shatters, and confetti to the phrase that earns them.
- **Every hard concept gets a dedicated animated diagram** — if a phrase asserts a mechanism, a static caption is not teaching it; build the 3-6s mini-diagram (object transforms as the mechanism happens). Longer and clearer beats shorter.
- Timing note: word-proportional estimates get beats matching the WRITTEN script; re-nudge ±0.5s against the recorded read at retime.

## Pre-publish gates (run ALL of these, every time)

1. `node --check` the last script block.
2. Selector inventory: every script-targeted class resolves.
3. Replay-reset audit: interrupt mid-beat → re-enter → getProperty on every animated property.
4. Beat-audit no-regression (`tools/beat-audit.mjs`, from the retention-pass skill).
5. **Pairwise overlap audit — `tools/overlap-audit.js`** (inject into the page). THE RULE: nothing overlaps anything unless the overlap IS the lesson — no words on words, host on nothing ever, arrows never cross text, ambient characters stay out of text bands. Deliberate teaching overlaps get `data-ovl-ok="sharedToken"` on BOTH elements; everything else is a defect. **Sample at 0.5s steps** — 1s sampling passed a flight that struck a headline 96px deep mid-transit; fast legs live between coarse samples. Zero non-whitelisted violations before publish. Why this tool exists: the frozen preview reports CSS-entrance elements at opacity 0, so box-sweeps that read live opacity SILENTLY EXCLUDE half the content — the tool forces each CSS element visible per its own animation-delay before measuring. Auditability disciplines: hide via autoAlpha (visibility:hidden) not bare opacity/scale so hidden elements don't leave phantom boxes; keep entrance delay+opacity on the SAME element that carries the text (parent-wrapper delays blind the audit); entrance drop-columns may mutually whitelist (transient fall-throughs read as physics); when a caption is squeezed, move the PROP row, not the caption into the other band — and re-run, because a fix can create the inverse collision.
6. VO-sync pass (section above) on any scene whose choreography changed.

## Layout laws (overlap prevention by construction)

- **Sequential occupancy** — a zone is VACATED before it's reused: prior occupants exit (fade+shrink or slide off) as a real narrative beat, they don't just dim underneath. Dense scenes = the #1 overlap source; if a scene needs 3 acts, it needs 3 exits.
- **Host paths, not just holds** — flight lines must route around text bands; a transit through a caption reads exactly as bad as a parked overlap.
- **Ambient characters live in margins** — drifting mini-characters/motes never cross text bands; park their base positions in empty corners.
- **Symmetry pass on any touched layout** — equal gaps in stacks/rows, true centering, one consistent margin rhythm. Unsymmetrical spacing reads as a mistake even when nothing overlaps.
- **The crafted pencil** (host prop standard, lives in `host()`): a hex body gradient + 2 facet lines + 30% white specular, silver ferrule with crimp grooves, blush eraser, cream wood taper with grain line, graphite cone. Same wrapper/anchor as the arm rotation expects; gradient ids uid-suffixed.

## The look levers (what makes it "produced")

All present in the scaffold — keep them when replacing scenes; reuse the data-URIs:

1. **Real 3-layer parallax environments** — scene backgrounds are TRANSPARENT; the world lives in shared stage layers: `#envFar` (sky gradient, sun/moon glow, stars, far hills — below scenes), `#envMid` (close hills, a landmark prop, foreground detail — below scenes), `#envNear` (blurred foreground at the frame corners — **above content**, `filter:blur(2.2px)`, corners only so it never covers captions). Each has 4 mood variants (`.vwarm/.vpaper/.vcold/.vdark`) cross-faded by `stage[data-mood]`, which `showScene` sets from the scene's `s-*` class. Layers drift on independent 32–64s loops (`translate` property), and `runScene` adds a **per-cut camera dolly** — far 6px / mid 14px / near 26px, direction alternating by scene index (GSAP `x` composes with the CSS drift). New scenes get the whole world for free: just pick an `s-*` class.
2. **The camera** — `.xpl-vig` vignette + `.xpl-grain` (feTurbulence at 5%) overlays above everything. Do not remove; instant produced feel.
3. **Two-tone shading on every object** — rim highlight + inner bottom shade on containers; radial-gradient + specular on drops (`.marble`); `::before` gloss on bars (`.qbar`). A new prop with flat fill is below the bar — give it light.
4. **Glow on dark scenes** — colored multi-layer `box-shadow` on chips over `s-black` (see the `[data-scene="0"]` rule).
5. **Ambient life everywhere** — chip float (desynced per kind), dust motes, sparks on payoff beats, Ken-Burns push-in per scene, drifting light wash, host wing-flutter. All CSS, all already global.
6. **Theme (swappable)** — palette tokens live in `:root`; the default is a warm honey/ink look with a friendly bee host mascot (like Kurzgesagt's birds). To rebrand: change the `:root` color tokens and replace the `host()` SVG string. Semantic color slots in the demo: accent = the highlighted term, ink = the contrast term, green = valid, red = trap, violet = the collision/overlap. Serif (`--font-serif`) headings, a handwriting font for accents ONLY, mono for lower-third captions (`.l3`).

## Retention pass (run before publishing — this is what holds the YouTube curve)

The full method lives in the **`retention-pass` skill** (3 rounds: STRUCTURE → BEAT COVERAGE → POLISH, plus `tools/beat-audit.mjs` which walks ACTS vs SCENES and prints coverage/dead zones). Run it BEFORE VO is recorded — that's when durations are still free.

While BUILDING (so the pass has less to fix), hold the big five: first beat ≤0.5s; the hook opens a loop the PEAK closes (build the hook from the peak scene's own prop classes, held as a question); every scene gets a content B-beat past its 60% mark; kickers re-hook rather than label (best: close a loop by name); never announce duration. Field calibration: in production use every scene overran its choreography by 30–100% by default, and hooks drifted toward teasing the trap instead of the peak — expect both.

## QA — how to verify in a preview browser (its animation clock may be FROZEN)

Some embedded preview browsers never tick rAF, so neither CSS animations nor GSAP visually advance. This is a preview artifact — real browsers are fine. Verify like this:

- **GSAP moments (deterministic):** `window.__xpl.goto(i)` then `window.__xpl.tl().pause(t)` — sets every tween's state at time `t` synchronously. Screenshot. This is your main tool; freeze each scene at 2–3 beat times.
- **CSS entrances:** inject a freeze style so text shows its end state:
  `.xpl-scene.is-active{animation:none!important;opacity:1!important}.xpl-scene.is-active .fu,.xpl-scene.is-active .pp,.xpl-scene.is-active .fi{opacity:1!important;translate:0 0!important;scale:1!important;animation:none!important}`
- **Syntax-check after any scripted surgery:** extract the last `<script>` block and run `node --check` on it. A silent syntax error = no `__xpl`, no host, blank harness.
- Check console logs after every reload; serve the folder with `python3 -m http.server`.
- Finish with a multi-lens critic pass (motion craft, persuasion, brand, a11y/robustness, fresh creative-director) — integrate the top fixes, re-verify.

## Gotchas (every one of these cost real debugging time)

- **Self-contained/published HTML can't load CDNs** — GSAP must be INLINE. The scaffold ships stripped with a `<!--GSAP_INLINE-->` marker; run `python3 inline-gsap.py <file>` (fetches GSAP 3.13 from jsDelivr into a gitignored `vendor/`, full free plugin suite; `--refresh` upgrades an old file in place).
- **SplitText re-split** — never `new SplitText` inside `ACTS[i]` (re-runs nest spans); use the `splitOnce` registry.
- **Wiggle accumulation** — relative `'+=n'` tweens are safe ONLY with wiggle eases (they return to start). If a scene can be cut mid-wiggle, the killed tween leaves a partial offset — every ACTS reset must include `rotation:0` on wiggled elements.
- **Entrances use `translate`/`scale`/`rotate` properties; idle/ambient life uses `transform`** — they compose. Never animate the `transform` shorthand in an entrance keyframe or you'll clobber inline centering transforms.
- `.pp`/`.fu` on an element that also needs `transform:translateX(-50%)` centering: wrap — outer div centers, inner carries the class.
- **SVG motion rule:** keyframes/tweens go on a dedicated wrapper `<g>`, never on a node with a `transform` attribute (the animation overwrites the attribute).
- **px `transformOrigin` on an SVG group is BBOX-relative, not user-space** — `transformOrigin:'120px 150px'` means "120px right of the group's bounding-box top-left", so rebuilding the group's geometry silently moves the pivot (a gauge needle swung off-stage for a whole scene this way). For a fixed pivot in SVG coordinates always use `svgOrigin:'120 150'`. Audit every px-origin whenever an SVG asset is rebuilt.
- **`layMarbles` row width 168** (vessel walls slant); drops at 180 poke through.
- **Charset:** without `<meta charset="utf-8">`, `python http.server` serves files as latin-1 and symbols mojibake. The scaffold ships the charset tag — keep it in every new file. HTML entities (`&mdash; &check;` …) are fine for DOM text; `\u` escapes for JS strings.
- Scene indexes are DOM order — `SCENES`, `FL`, `ACTS`, `data-scene`, and the CTA-nudge CSS selector must all agree after any add/remove. Re-run the node syntax check + a `__xpl.scenes()` count after surgery.
- The final scene entry is `999` and `advance()` must hit `done()` on it, or the toggle sticks on "Pause".
- Keydown guard: `e.target.closest && e.target.closest('input,...')` — document-targeted synthetic events have no `.closest`.
- Host/actor overlap: after building a scene, freeze-frame every waypoint hold and check the host isn't parked on top of text; fix `FL` coordinates, not the content.

## VO production (ElevenLabs pipeline)

- **Voice:** pick any ElevenLabs voice id — it's a required argument to the helper. Key = `ELEVENLABS_API_KEY` (environment or `./.env`). REST call: `POST api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_64`, header `xi-api-key`, model `eleven_multilingual_v2`, settings stability .5 / similarity .75. Helper: `tools/vo-generate.py <script.md> <outdir> <voiceId>`.
- **Write scripts at ≈2.5 words/sec × scene duration** — a cloned/TTS voice reads ~2.6 w/s; estimating 3+ w/s runs clips over their scenes. Target 85–94% fill per scene (continuous narration, natural breath at cuts); CTA hold stays short.
- **Continuous + valuable**: every added phrase narrates an on-screen beat (count the re-reads aloud with the counter, speak the enumeration as items land, autopsy the trap as it dies). No filler.
- **Per-scene clips, not one track**: one mp3 per scene → duration-check each vs `SCENES[i]` (ffprobe) → extend scenes for overruns → base64 `VO[]` array injected before the main script + `voPlay(i)` from `showScene` (kills prior clip on cut), `voCur.pause()/play()` wired into pause/resume. Browser autoplay policy: first click enables sound — `play().catch(()=>{})` and let the poster click be the gesture.
- The `-vo.html` variant is a rebuilt COPY of the master (master stays silent); regenerate it after any master edit.

## Publishing & production

- Publish as a self-contained HTML file — everything is inline, so it's portable and CSP-safe.
- YouTube pipeline: screen-record fullscreen playback → lay VO → export. Shorts = seek to a chapter, record that scene range at 9:16 crop.
- When VO is recorded: retime each scene's `SCENES[i]` to the read; `FL` fractions usually survive unchanged; GSAP beat times inside `ACTS[i]` are absolute seconds — nudge them to the read's emphasis points.
