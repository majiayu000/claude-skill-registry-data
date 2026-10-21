---
name: engine
description: Technical reference for the drawn-by-code engine. Use it when writing or debugging a scene's code (scene.js), when rendering to MP4 or stills, when touching engine/ or a style kit, or when something jitters, runs slow or doesn't load. Covers the Motion.scene contract, determinism, units, caching and commands.
---

# Engine

2D canvas in headless Chromium, frame by frame. No animation libraries: time is a
variable `t` and every frame is a **pure function of t**.

## Scene contract

```js
Motion.scene({
    fps: 24, duration: 6.5,
    logical: [1600, 900],          // logical units; the output is scaled (k = px/unit)
    uses: ['styles/paper-cutout/paper.js', 'styles/paper-cutout/kit.js', 'sandbox/x/cast.js'],
    fonts: [{ family: 'Hand', src: 'fonts/PatrickHand-Regular.ttf' },
            { family: 'Shrikhand', src: 'fonts/Shrikhand-latin.woff2' }],
    bpm: 120, beatOffset: 0,       // musical grid (review.mjs checks the cuts)
    shots: [[0, 4, 'Workshop'], [4, 8, 'Box']],
    audio: { mix: 'mix.wav' },  // render.mjs adds it automatically
    setup(env) { return { kit: PaperKit.make(env) }; },  // → env.state
    draw(g, t, env) { ... },       // logical coordinates; the canvas comes already scaled
    post(ctx, t, env) { ... },     // optional, in PIXELS: grain, vignette
});
```

`env`: `W, H` (logical), `k`, `fps`, `duration`, `total`, `px: [width, height]`, `state`.
Paths in `uses` and `fonts` are relative to the repo root. An entry can be optional
(`{ src: 'sandbox/x/private/brand.js', optional: true }`, fonts `{ family, src, optional:
true }`): it is skipped when missing. That is how a client's brand material stays in the
uncommitted `sandbox/*/private/` while the committed code still runs on a placeholder
brand.

**Scenes outside this repo.** A client's pieces can live in the client's own (private)
repo and still use this engine. Mark the root of that folder with a `drawn-by-code.json`
(its presence is the contract; `{}` is enough). Every tool then takes a scene path under it:
the server mounts that root at `/@ext/`, so inside it paths from the root are written
`'@ext/…'` (`const DIR = '@ext/pieces/x/'`, `uses: ['@ext/brand/brand.js']`, fonts
`'@ext/brand/fonts/…'`), while this repo's kits, fonts and effects keep their paths
(`'styles/…'`, `'fonts/…'`). Nothing outside the two roots is served. `new.mjs --in <dir>`
creates the experiment there (and logs it in that folder's `INDEX.md`); the preview lists
those scenes with `node engine/serve.mjs --ext <root>`. Lessons that generalize still come
back here, to the skills; only the client's material stays there.

Utilities in `engine/core.js`: `Motion.rng(seed)`, `noise1`, `sprite(key, box,
scale, draw)`, `shotAt`, `pulse(t, bpm)`, `beatIndex`, `onBeat`, `cam(g, env, cx, cy,
zoom, rot)`, `shake`, `keys([[t, v], …], t)`; and `Ease.seg/inOut/out/in/back/elastic/bump/
pop/lerp/lerpPt`. `Motion.layer(env, name, fn)` paints a shot on a separate canvas
(at output size) and `Motion.drawLayer` pastes it: for transitions and mirrors. The local-time pattern is `const u = Ease.out(Ease.seg(t, 2.0, 2.6))`.
`Motion.quad(g, src, [tl, tr, br, bl], n, box, { bend })` maps an image onto any
quadrilateral (triangle-subdivided affine), with an optional bend: paper in perspective,
a page turning, a note flipping over.

**Animating on twos:** hand animation changes drawing every 1/12 s. Index per-drawing
tables with `const d = Math.floor((t - t0) * 12 + 1e-6)` and hold the drawing between;
smooth curves look wrong next to a reference animated on twos.

## Determinism (golden rule)

- Forbidden: `Math.random()`, `Date`, `performance.now()` and state that accumulates
  between frames (positions that keep adding up, live particles). Everything is computed
  from `t`.
- Randomness = `Motion.rng('stable-seed')` or `Paper.rng`. The seed identifies the
  piece, **never the frame**, or the texture boils.
- Simulations (falls, paper rain): a closed-form formula per particle with its own seed,
  or a simulation fully precomputed in `setup` and indexed by frame.
- `review.mjs` paints the frames in a different order and compares hashes: if it warns,
  there is state.

## Long or multi-style scenes

One file per segment in `segments/` (each adds its function to a global object, e.g.
`Segment.frog = (g, t, env) => …`), loaded from `uses` together with the kits of every
style. `scene.js` only assembles: it decides which segment or which transition plays at
each `t`. See `sandbox/2026-09-24-exquisite-corpse/`.

## Performance

- Static things (backgrounds, cutouts, textures) are painted once with `Motion.sprite` /
  the kit's `sprite`, with a key that includes everything that changes their look.
- Marker texture is expensive: low `density` on large pieces, and always cached.
- Target: < 150 ms/frame warm at 1920. `review.mjs` measures it.

## Commands

```bash
npm run preview                                           # http://127.0.0.1:5173
node engine/review.mjs sandbox/x/scene.js                 # automatic review + sheet
node engine/render.mjs sandbox/x/scene.js --at 1.5,3.2    # stills at 1920 → out/stills
node engine/render.mjs sandbox/x/scene.js --size 1920     # MP4 → out/x.mp4
node engine/render.mjs sandbox/x/scene.js --size 1080 --from 4 --to 8   # a segment
node engine/render.mjs sandbox/x/scene.js --size 1920 --gpu   # on a machine with a graphics card (prints the GL it got; a laptop's discrete NVIDIA card is tried first, through PRIME offload; MOTION_IGPU=1 skips it)
node engine/mix.mjs sandbox/x/audio.json                  # mix.wav
node engine/strip.mjs sandbox/x/render/x.mp4 sandbox/x/render/strip.jpg --at 1,3,5   # a film strip for READMEs
node engine/gif.mjs sandbox/x/render/x.mp4 sandbox/x/render/x.gif --clips 2-6,10-14   # a looping GIF (< ~5 MB)
# working against a reference video (replicas, style studies)
node engine/reference.mjs sheets ref.mp4 --every 0.25      # labelled contact sheets
node engine/reference.mjs compare sandbox/x/scene.js ref.mp4 --times 2,3.5 --crop 0.3,0.2,0.4,0.4
node engine/reference.mjs colors ref.mp4 3.5 skin=0.42,0.31 # sampled palette
node engine/reference.mjs track ref.mp4 --color '#d2745e' --from 10 --to 12   # per-frame box
node engine/reference.mjs cuts ref.mp4                                         # exact cut frames
node engine/reference.mjs box ref.mp4 1.75 --color '#302222' --region 150,100,850,800
node engine/reference.mjs runs out/stills/t_3.79s.png 0 --row 0.6               # edges along a row
node engine/reference.mjs face ref.mp4 --body '#d2745e' --from 12 --to 12.5    # face per drawing
# a scene outside this repo (a folder marked with drawn-by-code.json)
node engine/new.mjs x --in ../client/marketing/pieces --aspect 9:16
node engine/serve.mjs --ext ../client/marketing
node engine/render.mjs ../client/marketing/pieces/2026-10-01-x/scene.js --at 1
```
The whole method for replicas is in the **replicate** skill.

Preview: space = pause, ←/→ one frame, shift+←/→ one second, `&t=3.5` in the URL.
Chrome: looked up in `CHROME_PATH`, `/opt/pw-browsers`, and the usual Linux/macOS paths.

## Debugging

- Black screen or no READY: `review.mjs` prints the page error. Typically: a wrong `uses`
  path, a font that doesn't load or an exception in `setup`.
- Text in a system font on the first frame: the font is not in `fonts`.
- Everything blurry: the sprite was cached at low resolution (raise `res`) or is scaled
  up a lot.

## Lessons

<!-- Added from the review loop: date · experiment · one-line lesson. -->
- 2026-09-24 · coffee-first · Everything that bleeds off the frame (backgrounds, floors, tables) must cover the camera's full travel: `paperBg(…, { bleed })` and pieces wider than the pan. `review.mjs` warns about «Transparent holes».
- 2026-09-24 · coffee-first · To cache a moving piece, draw the sprite at its origin and move it with `translate/rotate/scale`; the sprite key must not depend on t.
- 2026-09-24 · what-do-you-love · A text drawn with `strokeText` on top of `fillText` only gets bolder; a felt-tip look needs the glyph thinned: fill, then `destination-out` stroke on an offscreen canvas (cache it per scale from `getTransform()`).
- 2026-09-24 · saas-promo · Key tables compared with `tq = Math.floor(t*12)/12` must be exact twelfths: 1.67 is not ≥ 20/12, so a drawing silently shifts. Write times as beats/halves/quarters or snap with `Math.round(a*12)/12`.
- 2026-09-25 · physics-history v2 · Never wait for a render with `until ! pgrep -f "render.mjs …"`: the waiting shell's own command line contains the pattern, so it waits forever. Run the render itself in the background and let its completion notify you.
- 2026-09-27 · pyramid-engraving · This container has no GPU: WebGL runs in SwiftShader, which executes every branch of a shader for every pixel (masked). An `if` never saves time there; what does: fewer call sites of heavy functions, relief gradients from `dFdx/dFdy` instead of extra evaluations, and shader variants compiled per draw (`#ifdef`, `variantFor` in the engraving kit). Profile before guessing: time one still at half size (fragment-bound work drops 4×), then knock features out one at a time. For long films, render with `--gpu` on a machine that has one.
- 2026-09-27 · pyramid-engraving · On a laptop with Intel + NVIDIA (Optimus), headless Chrome takes the integrated GPU unless the process is launched with PRIME offload (`__NV_PRIME_RENDER_OFFLOAD=1`, `__VK_LAYER_NV_optimus=NVIDIA_only`, `__GLX_VENDOR_LIBRARY_NAME=nvidia`); ANGLE on Vulkan there was 6× faster than OpenGL on the Intel (0.27 s vs 1.75 s a heavy frame), and only without `--enable-features=Vulkan`, which left no WebGL2. `--gpu` now tries it first.
- 2026-09-27 · pyramid-engraving · The same shader can differ by GPU: in GLSL ES 3.0 a fragment shader's `int`/`uint` default to `mediump` (16 bits on NVIDIA: an integer hash collapsed to a constant), and a float hash like `fract(p · 123.34 …)` amplifies a compiler's reassociation of `(i + 1) · k` into a visible jump at every noise lattice line. Declare `precision highp int`, hash lattices in integers, and check a still on each GPU you render on.
- 2026-09-30 · external product promo · Motion blur by averaging copies: paint each pass whole into its own layer (`Motion.layer`) and composite it with alpha 1/(k+1); painted straight onto the canvas, each pass's background washes out the previous ones and objects turn half transparent. Pick the number of samples from the real displacement in pixels, at least 3 as soon as anything moves (switching from 1 to 2 samples changes the edges in one frame, a visible jump), and never let it be 1 in a formula like `i / (n − 1)`: 0/0 gives NaN and the layer silently paints nothing (an empty frame).
- 2026-10-02 · product videos · A scaled `drawImage` with a source crop samples one pixel outside the crop (Chrome): a reused temporary canvas is cleared whole, not only the area about to be copied, or leftovers of the previous group show as a line. And `ctx.filter = 'blur()'` every frame doubled a scene's cost (105 → 47 ms for a frame): blur once into a sprite and stretch it.
