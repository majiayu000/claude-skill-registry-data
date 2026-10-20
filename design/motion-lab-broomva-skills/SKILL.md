---
name: motion-lab
tier: D
category: video
description: >-
  Make code-first motion (an animation that is a program, rendered frame by frame
  in a headless browser) look directed instead of generic, and check that
  sampled frames re-render identically. Ships the render contract (every frame a pure function of t,
  window.renderAt(t), no clocks, timers or unseeded random, pinned libraries,
  frames 0..N-1), a numbers-not-adjectives prompt template with a living ban list,
  and a render -> look -> fix loop whose notes name frames. Deterministic core:
  scripts/motion_lint.py (static contract linter), scripts/render.mjs (Playwright
  freeze-frame renderer that also seeks SVG SMIL, with a labelled contact sheet
  and a --verify purity re-render of sampled frames), scripts/motion_math.py (drift-free beat grid, spring damping ratio,
  loop frames, text holds, GIF delay schedule and a GIF timing reader). USE WHEN:
  writing or fixing an animated loop, title card, product shot, explainer clip,
  logo reveal or launch video in plain HTML/CSS, Canvas, SVG, three.js, GSAP,
  HyperFrames or Remotion; a render flickers, jitters, hiccups at the loop seam,
  drifts off the beat or "looks like AI"; exporting a loop for X. Triggers on
  "motion lab", "motion design", "animate this", "make an animation", "animated
  loop", "render this animation", "render contract", "renderAt", "contact sheet",
  "frame 84", "looks like AI", "it looks generic", "loop hiccup", "GIF for X".
  NOT FOR: UI micro-interactions inside a live app (use the animate skill or the
  Motion library), editing recorded footage (video-cut), AI-generated video
  footage or people (higgsfield, ltx-video), or a fixed-aesthetic Remotion recipe
  (launch-video).
---

# motion-lab — directed, reproducible code-first motion

An LLM does not output pixels for an animation. It writes a program that draws
each frame, and a headless browser records the frames. Three properties follow,
and this skill is built to keep them:

1. **A frame is reproducible.** Frame 84 rendered twice is the same image twice.
2. **An edit is cheap.** Change one number and re-render. Nothing is re-rolled.
3. **The agent can check its own work.** It reads stills and a contact sheet, and
   writes notes against frame numbers.

## The one rule

> **Adjectives get defaults. Numbers get direction.**
>
> The generic look is what the model produces where the prompt left a value open.
> "Premium", "cool" and "modern" decide nothing, so the model decides for you:
> dark navy space, glow, bloom, particles, a spinning turntable. Every adjective
> you replace with a number is a decision you take back.

## Pipeline

1. **Pick the engine and the canvas first.** Changing the canvas later means
   re-directing every shot.

   | Piece | Engine |
   |---|---|
   | one idea, under 10 s, 2D | plain HTML + CSS / Canvas / SVG |
   | a series, a template, data-driven | Remotion (load the `remotion` skill) |
   | thinks in web pages and GSAP timelines | HyperFrames |
   | anything 3D | three.js (pin the version: `three@0.160.0`) |

   Sizes: 1920x1080 (16:9), 1080x1080 (1:1, safest in the feed), 1080x1350 (4:5),
   1080x1920 (9:16).

2. **Write the directed prompt.** Fill every line of
   [`assets/prompt-template.md`](assets/prompt-template.md): GOAL, OUTPUT, TIME, LOOK,
   MOTION, SHOTS, BANNED, QA. Paste the render contract (below) under it. Get every
   number from [`references/motion-numbers.md`](references/motion-numbers.md) or
   compute it:

   ```bash
   python3 scripts/motion_math.py frames --seconds 6 --fps 60 --bpm 120   # 360 frames, loop closes on the music
   python3 scripts/motion_math.py beats --fps 30 --bpm 128 --count 32      # beat frames, rounded per beat
   python3 scripts/motion_math.py damping --stiffness 100 --damping 10     # zeta 0.5: playful
   python3 scripts/motion_math.py hold --words 2 --fps 24                  # 27 frames minimum
   ```

   Hand the model [`assets/motion.js`](assets/motion.js) with the line
   *"use only these tokens, no inline numbers"*. It holds the easing curves, the
   durations, the stagger and a closed-form spring that needs no simulation, so
   frame 84 renders without computing frames 0 to 83.

3. **Lint before rendering.** The static half of the contract:

   ```bash
   python3 scripts/motion_lint.py anim.html            # exit 1 on any ERROR
   ```

   | Rule | Catches | Level |
   |---|---|---|
   | MC01 | `Date.now`, `Date()`, `new Date`, `performance.now`, `requestAnimationFrame`, three.js `setAnimationLoop` / `Clock` / `getElapsedTime` / `getDelta`, `gsap.ticker.add`, `document.timeline` | ERROR; a WARN when `renderAt` exists and a `?t=` guard appears to wrap the loop, and always ERROR inside `renderAt` itself. The static guard check is a heuristic: `render.mjs` decides at runtime (exit 7) |
   | MC02 | `setTimeout` / `setInterval` | ERROR |
   | MC03 | `Math.random` (also aliased: `const r = Math.random`, `Math["random"]`, `const {random} = Math`), `getRandomValues`, `randomUUID`, three.js `MathUtils.randFloat/randInt/randFloatSpread` | ERROR |
   | MC04 | JS-driven motion (rAF, timers, three.js, GSAP; a canvas painted once does not count) with no `window.renderAt(t)`, or a `renderAt` the renderer cannot reach (a `const`/`let`, or declared inside a `type="module"` script) | ERROR |
   | MC05 | a CSS transition with a non-zero duration, in CSS, a `style=""` attribute or set from JS | ERROR |
   | MC06 | `fetch` / XHR / WebSocket, or a *loaded* remote URL (src/href/poster/data/srcset quoted or not, SVG `<image>`, `<object>`, `<embed>`, importmap, `url()` in CSS or a `style=""` attribute, `@import`, a JS import, `.src =`, `.load()`, `new URL()`, a JS string naming a loadable file) that is not a font host and not pinned to `MAJOR.MINOR.PATCH`. Any other remote URL in a JS string is a WARN; the SVG namespace is never checked | ERROR |
   | MC07 | a local `src`/`href` (not one self-contained file) | WARN |
   | MC08 | web fonts with no `document.fonts.ready` wait | WARN |
   | MC09 | `@keyframes` animating width / height / top / left | WARN |
   | MC10 | something on its own clock: GSAP with no paused timeline or seek, an autoplaying `<video>`/`<audio>` | WARN |

   It also lints code outside `<script>`: inline `on*` event handlers and `srcdoc`
   documents. It lints a bare `.js` / `.tsx` module (a Remotion component) too,
   where MC04 does not apply but MC01–MC03 and MC06 do. Font hosts are matched by
   exact hostname.

4. **Render stills, a contact sheet, and verify purity.** From a project with
   Playwright installed (`npm i -D playwright && npx playwright install chromium`):

   ```bash
   node scripts/render.mjs anim.html --seconds 6 --fps 24 --width 1080 --height 1080 --verify
   ```

   It writes `out/frames/0000.png…` for frames 0..N-1, `out/contact.png` (up to 12
   frames labelled with their numbers), and `out/manifest.json`. For each frame the
   renderer first seeks its animations (`document.getAnimations()`) and the SVG
   SMIL timelines (`<animate>` is not in `getAnimations()`), then calls `renderAt(t)`
   last, so `renderAt` wins for anything it sets itself. Which animations are the
   page's is tested, not guessed: during the warm-up the renderer calls `renderAt`
   at every frame time (no screenshots), and a paused animation whose timing
   `renderAt` changed between consecutive calls is driven by it (a scrub through a
   negative `animation-delay`, a WAAPI animation it positions, even one that starts
   late in the timeline) and is left alone (`driven_by.page_owned`). Every other
   animation is seeked to t, including CSS the page froze under `?t=` and
   animations inside open shadow roots. `--verify` reloads the page
   and re-renders the first, middle and last frames; if any byte differs, a frame
   is not a pure function of t. This catches what the linter cannot, such as a
   `renderAt` that reads a counter. `--verify-all` re-renders every frame, in
   reverse order: a `renderAt` that depends on its call history replays identically
   when frames come in the same order, so an in-order check passes it. The manifest
   records the scope (`sampled 3 of N frames` or `all N frames`); if the check
   could not finish (a timeout), `verify.pure` is `null` and the run exits 5. `--every N` puts
   every Nth frame on the contact sheet and always ends it on frame N-1, the seam. Add `--mp4` for an
   H.264 file (needs ffmpeg).

   | Exit | Meaning |
   |---|---|
   | 0 | rendered |
   | 2 | usage or runtime error (including a duration that rounds to zero frames) |
   | 3 | `--verify` found an impure frame (listed in the manifest), or the frames change although nothing the renderer seeks drives them (motion on its own clock) |
   | 4 | `--mp4` failed |
   | 5 | the page threw, or a `renderAt` call did not finish within 30 s (`page_errors` in the manifest; `MOTION_LAB_FRAME_TIMEOUT_MS` overrides) |
   | 6 | nothing drives motion, so every frame is the same image (`--allow-static` for a still) |
   | 7 | a frozen frame keeps changing on its own: something still draws while the page is frozen at `t` (a preview loop its `?t=` guard does not stop, a timer chain, a worker, a transition `renderAt` starts) |

   When several apply, one code is reported by precedence 3 > 5 > 7 > 6 > 4
   (`manifest.exit_code`); the manifest lists every finding.

   Exit 7 is a drift check, not a code reading: the renderer seeks a frame,
   screenshots it, waits 250 ms, and screenshots again (`manifest.drift`). It does
   this once right after load (catching an intro that plays for a while and then
   stops) and at frames 0, N/2 and N-1 after the render. A pixel that changes while frozen is what corrupts a render,
   and the check sees it however the loop is written: `requestAnimationFrame`,
   three.js `setAnimationLoop`, a `setTimeout` chain, a worker. A paused GSAP
   timeline keeps its ticker running but draws nothing, so it passes. A loop that
   only redraws slower than 250 ms can slip past; `--verify-all` is the backstop,
   and the manifest says so when the page scheduled frames but nothing drifted.
   `manifest.loop_probe` still counts the page's `requestAnimationFrame` and
   `setInterval` calls, as a diagnostic. A `renderAt` that throws for some `t` is
   recorded in `page_errors` (exit 5) and the render continues; one that times out,
   in the warm-up or in any frame, stops the render there (`aborted_at_frame`),
   since a hung page hangs every later frame too, and the manifest is still
   written. Earlier `contact.png`, `anim.mp4` and `manifest.json` in `--out` are
   removed first, so an aborted run never leaves a previous run's outputs looking
   current.

   The input is treated as untrusted: a `file://` request is served only when it is
   a regular file whose real path (symlinks resolved) lies inside the real input
   file's directory, with no path segment below it starting with a dot (`.env`,
   `.git`). Directory URLs and everything else are blocked and listed in
   `manifest.blocked_requests`. A symlinked input renders from its target's
   directory. A `frames/` directory in `--out` that is a symlink is refused before
   anything is deleted. Other files in that directory remain
   readable by the page, so render untrusted HTML from a directory that holds only
   its assets. Only `NNNN.png` files are removed from
   `out/frames/` before a render, and only after Playwright has loaded.

5. **Look, then fix with frame numbers.** Read `contact.png` first, then only the
   frames a note needs. Write notes as numbers, never feelings:

   | The note you have | The note you send |
   |---|---|
   | "make it pop" | scale 1.0 → 1.08 → 1.0 over 6 frames, peak on the beat |
   | "make it feel premium" | ease-out-quint entrances, springs at zeta 0.8, no overshoot on text |
   | "it drags" | shorten each hold by one beat (12 frames at 120 BPM, 24 fps) |
   | "it feels busy" | one hero move at a time; the rest start 150 ms later at 60% of its travel |
   | "it looks like AI" | name every default it used, add each to BANNED, render again |

   Send one or two notes per round; seven at once turns a fix into a rewrite. Two to
   four rounds is normal. If a fix does not hold, render the frames on either side
   of the problem and list every difference. More prompts that work are in
   [`references/fixes.md`](references/fixes.md).

6. **Sound (optional), measured not heard.** The model cannot listen. Score from
   frame numbers, synthesize in code (Web Audio), land each hit 1 frame *after* its
   picture, mix to −14 LUFS with peaks at −1 dBTP, then check each hit by decoding
   the finished MP4. The picture must work muted first: the feed autoplays silent.

7. **Export and check.** Commands are in
   [`references/motion-numbers.md`](references/motion-numbers.md#export-for-x). Then
   measure the GIF rather than trusting the encoder:

   ```bash
   python3 scripts/motion_math.py gif-check out/anim.gif --fps 24
   ```

   A GIF stores delays in hundredths of a second, so 24 fps (41.67 ms) cannot be
   stored exactly. An encoder that rounds every frame to 4 cs runs 4% fast and falls
   off the beat grid. ffmpeg 8.1 (macOS) and 6.1.1 (Ubuntu CI) were both measured
   alternating 4 and 5 cs and holding a 144-frame loop at exactly 6.00 s; the integration test
   `test_ffmpeg_gif_export_keeps_exact_loop_timing` re-measures whatever ffmpeg is
   installed, so the claim is checked rather than remembered. Other encoders may
   differ. `gif-delays` prints the exact schedule.

## The render contract

Paste it under every motion prompt. Each line closes one way a render goes wrong.

```text
Output one self-contained HTML file. Only the libraries the prompt names, pinned to a version.
No network requests except fonts and those pinned libraries.
Every frame must be a pure function of time t, in seconds.
If JavaScript drives any motion, expose window.renderAt(t) that draws exactly that frame.
With ?t= in the URL, draw that frame and never start requestAnimationFrame.
Animate with CSS keyframes, the Web Animations API, SVG, Canvas 2D or WebGL. No CSS transitions.
No Date.now, no setTimeout or setInterval starts, no unseeded Math.random.
Loops: render frames 0 to N-1 only, and frame N-1 must flow into frame 0.
If the page needs time to load (fonts, textures), set window.__ready = true when done.
```

When a fix works, add its line to the contract. The contract is the memory: every
line is a failure you never have to see again.

## The ban list

Start from this, then grow it after every first render by naming what the model
used anyway:

- purple or blue gradients, glow, lens flares, bloom, neon
- floating particles as decoration
- dark void backgrounds (unless the brief asks for one)
- everything fading in at once; fade-and-slide-up on every element
- centered-everything layouts
- text that moves while it is being read
- spinning turntables

One hero move per shot. Secondary moves travel 50–70% as far and start 100–200 ms
later. Ambient motion stays under 5% of the hero's travel.

## What the gates cannot see

- The linter is static. It cannot tell whether `renderAt` reads only `t`, whether
  a seeded generator is reseeded per frame, or a clock reached through an alias it
  does not know. `render.mjs --verify` is the runtime check, and it samples three
  frames in one session, not all of them. A clock that changes slower than the
  verify window (the minute of the hour, say) passes both gates.
- The linter scans JavaScript with a small tokenizer, not a parser. A regex literal
  that contains a quote or a backtick (``s.replace(/`/g, "'")``) can hide the code
  after it; the runtime checks still see what that code does.
- The warm-up that keeps frame 0 pure guards a compositor race seen on macOS
  Chromium (24 of 25 cold runs failed without it). Ubuntu CI's headless Chromium
  never shows the race, so its mutation runs only on macOS.
- `--verify` compares bytes. WebGL on a different GPU or driver can differ by a few
  pixels between machines. Verify on the machine that renders.
- Neither tool judges taste. The contact sheet and the frame-numbered notes are
  where judgment happens.

## Composition

| With | How |
|---|---|
| `remotion` / `remotion-best-practices` | the engine for series and data-driven video; lint its components in module mode |
| `launch-video` | a Remotion recipe with a fixed Liquid Glass look (dark void, glow, particles). Those are on this ban list: use launch-video when that look is the brief, and this skill when the brief is your own direction |
| `adaptive-video-ingest` (via `checkit`) | the same contact-sheet instrument, used to read video rather than grade your own |
| Claude Motion (claude.ai artifact) | the hosted version of this paradigm; this skill is the in-harness path |

## Tests

```bash
python3 -m pytest tests/ -q                                  # lint + math (render tests skip without playwright)
MOTION_LAB_NODE_DIR=/path/with/playwright python3 -m pytest tests/ -q   # + end-to-end render tests
python3 tests/mutation_proof.py                              # each listed mechanism has a test that fails without it
```

## Provenance

Method, numbers and the render contract distilled from Florence (@flxrnc),
"Opus 5.5 Motion Lab: Make Claude Animate Like a Studio" (X Article, 2026-09-30,
<https://x.com/flxrnc/status/2105311836190978392>), assessed in the broomva
workspace note `research/notes/2026-10-15-opus-motion-lab-render-contract-raw.md`.
The linter, renderer changes (`?t=0` load, animation warm-up, SMIL seeking,
`--verify`, exit codes, labelled sheet) and the GIF timing measurement are this
skill's own. BRO-3117.
