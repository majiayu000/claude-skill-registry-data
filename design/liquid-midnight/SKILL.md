---
name: liquid-midnight
description: |
  Build or restyle anything in Liquid Midnight. The look: Apple Midnight blue-black grounds (hue 245-252, never
  purple), liquid glass rimmed in travelling liquid metal (a conic chrome edge with cyan, magenta and gold fringes),
  real WebGL glass plasma orbs, a quiet ASCII text-shader background, Raleway Light headlines with one blue payoff
  phrase, and spring motion where every frame is a pure function of t, so it renders to video.
  Ships tokens (OKLCH + hex), materials CSS, a framework-agnostic canvas/WebGL render kit, a starter scene, a style
  linter, a render-and-look tool, and Pencil shader fills.
  Use for keynotes and slides, 9:16 reels and 4:5 posts, landing sections, showcase cards in apps, living diagrams,
  and Pencil boards in this style.
  Triggers on "liquid midnight", "midnight blue style", "liquid glass and liquid metal", "chrome rim", "metal rim",
  "plasma orb", "orbloom", "ASCII shader background", "keynote style", "reel in our style", "the Agent Workspaces
  look", "showcase style".
  NOT for calm, matte product UI: that is broomva-design, an independent sibling, so do not mix their tokens.
  Never use the arcan-glass look for this.
license: Apache-2.0
metadata:
  version: "0.1.0"
  homepage: "https://github.com/broomva/liquid-midnight"
primitive: null
category: design
required: false
introduced_in: "0.51.1"
---

# Liquid Midnight

The expressive showcase style distilled from the Agent Workspaces keynote, its reels and a product landing page. The full contract is **[DESIGN.md](DESIGN.md)**: read it before you build. This file covers how to *apply* it.

`SKILL_DIR` is the directory that contains this file.

## 1. Decide that it fits

- **Fits:** keynotes and slides, reels and feed posts, landing sections, hero or empty-state moments, living diagrams, Pencil boards.
- **Does not fit:** everyday product chrome such as forms, tables and settings. Use `broomva-design` or the product's own system. A product may borrow one `.lm-glass` card for a showcase moment (DESIGN.md §12.4).
- If the target already has a design system, ask before restyling it. This style does not replace an incumbent system silently.

## 2. Install the assets into the target

```bash
node "$SKILL_DIR/scripts/materialize.mjs" install . --with templates          # + specimen, shaders if wanted
node "$SKILL_DIR/scripts/materialize.mjs" verify .                            # receipt check: missing / edited / stale
```

This writes `./liquid-midnight/` with:
- `tokens/` (CSS custom properties `--lm-*` with hex fallbacks, plus JSON);
- `css/materials.css`;
- `kit/` (ES modules);
- `fonts/`;
- `LIQUID_MIDNIGHT.json`, a receipt with the source commit and per-file hashes.

It refuses to overwrite core files you edited locally unless you pass `--force`; `verify` reports any it finds.

`templates/` are **starters**:
- copied once, and meant to be edited in place;
- not hash-tracked, and ignored by `verify`;
- never replaced on a later `install` unless you pass `--force`.

Updates keep the optional sets you installed before; remove one with `--without specimen`. Use `--dir` to install somewhere other than `liquid-midnight/`, and `--dry-run` to preview.

## 3. Build with the grammar, not around it

Load `tokens/tokens.css` and then `css/materials.css`. Use these classes and modules:

| Need | Use |
|---|---|
| Page ground + light | `.lm-ground` on body, `<div class="lm-ambient"><i></i><i></i><i></i></div>` |
| Living background | `asciiBackground(canvas)` from `kit/ascii.js` under every glass surface (alpha .15 night / .12 day) |
| Floating surface | `.lm-glass` (+ `.lm-card`): thin tint, 9 px blur, cyan caustic, **travelling chrome rim** |
| Nav pill / segmented control | `.lm-capsule`, `.lm-seg` with `.lm-thumb` (drive x/width with `Sp`, response .4), `.lm-chip` |
| Focal round button | `.lm-orb-button.lm-ring` with metal-stroked `.lm-icon`. Icons need the `#lm-metal` / `#lm-metal-day` SVG gradient defs: copy the `<svg><defs>` block at the top of `templates/scene.html` |
| Headline | `.lm-kicker`, then `.lm-title` / `.lm-hero` / `.lm-breaker`; payoff phrase in `<em>` (Raleway 400, blue, never italic) |
| Numbers | `.lm-glass.lm-counter` (`.is-gain` green, `.is-loss` coral), zero-padded mono |
| Reel captions | `.lm-caption` with `<mark>` on the spoken keyword (Roboto Flex 64, ≤ 22 chars/line) |
| Orbs | `ORB.attach(canvas); ORB.begin(ctx); orb(x, y, r, C.blue, t); ORB.end()`. The canvas needs a positioned offset parent |
| Metal on lines / rings | `ribbon(...)`, `metalRing(...)` from `kit/metal.js` |
| ASCII pieces | `glyphTrail`, `dotRing`, `ringText`, `asciiField` + `atlas` |
| Motion | `createLoop({init, step, paint})`. Integrate in `step` (fixed 1/60 s), keep `paint(t)` pure, expose `window.renderAt`. Under reduced motion the loop repaints only when invalidated: after any canvas change outside `step()` (resize/fit, theme, data, GPU context restore), call `loop.invalidate()` |

Start from the starter `liquid-midnight/templates/scene.html`. Edit it in place, or copy it to a sibling folder such as `scenes/` and change its `../` asset paths to `../liquid-midnight/`. Capture mode pins motion on. It handles `?format=keynote|reel|feed`, `?mode=day`, `?guides=1` (safe zones) and `?t=` (deterministic frame). Edit its CONTENT block and `paint()`. For the format recipes, follow the checklists in DESIGN.md §12: keynote scene, reel, landing section, app card.

**Never ship these** (each was rejected on sight, DESIGN.md §3):
- a purple cast;
- the arcan-glass look;
- a flat glass panel with no metal rim;
- a radial-gradient "glow orb" in place of the WebGL orb;
- ASCII that reads as noise or rain;
- italic emphasis;
- wall-clock-only animation on anything that must render to video.

## 4. Check, then render and look

```bash
node "$SKILL_DIR/scripts/check_style.mjs" src/ liquid-midnight/templates/      # LM001 purple (oklch/hex/hsl/rgb/named/Tailwind), LM002 the rejected glass skill (errors); LM003-5 warnings
node "$SKILL_DIR/scripts/render.mjs" . liquid-midnight/templates/scene.html --t 0,2,6 --format keynote,reel --mode night,day --out renders
```

`check_style` is a heuristic. It has one deliberate false positive: an ID or anchor name that reads as a purple-leaning hex (`#a3f`, `#dad`, `#cafe`, `#c0de`, `#e2e`, `#b2b`) used as a selector or in code. Silence it with `lm-ignore` on that line. Markdown files are exempt from the hex rule (issue and PR numbers like `#808`).

`render.mjs` needs Playwright with Chromium; it says how to install it if missing. **Open every PNG and look at it** against DESIGN.md §13's references: the keynote frames, the reel, orbloom for the orb. The style linter only catches patterns. Acceptance comes from the render, in both modes. Fix what you see, then re-render.

Accessibility checks to run on the render (DESIGN.md §11):
- text on glass stays at t1/t2;
- in day mode, `t3`, green, coral and gold are used only for large text or with a label;
- emulate `prefers-reduced-motion`, `prefers-reduced-transparency` and `prefers-contrast: more`, and confirm the fallbacks look right.

## 5. Pencil (.pen) work

Read [references/pencil.md](references/pencil.md) **before the first Pencil call**. The pen MCP silently edits the *active* tab when `filePath` names a file that isn't open; that has corrupted other sessions' files three times. That reference covers:
- creating the file safely;
- the per-call guard;
- the shader fills (`liquid-midnight/shaders/orb.glsl`, `ascii.glsl` + atlas, installed with `--with shaders`);
- the angular-gradient metal rim;
- exporting boards for review.

## 6. Provenance and updates

- **Source of truth:** [broomva/liquid-midnight](https://github.com/broomva/liquid-midnight). It holds DESIGN.md, the specimen, the renders and the Pencil boards.
- **Vendored copy:** this skill carries a pinned copy; `assets/manifest.json` records the commit and per-file hashes, and the tests fail if a vendored file drifts.
- **Changing the style:** change it in the source repo first, then run `node scripts/sync_from_repo.mjs /path/to/liquid-midnight` here.
- **Origin of the kit:** extracted from [broomva/agent-workspaces](https://github.com/broomva/agent-workspaces) `deck/index.html` (Apache-2.0), with line references in every file.
