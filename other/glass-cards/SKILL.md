---
name: glass-cards
description: >-
  Build frosted "liquid glass" UI cards/panels on a dark animated background, where a card
  ZOOMS FORWARD to demo itself and then falls back as the next one rises, plus a gentle camera
  zoom-in/settle. Use for glassmorphism UI mockups, a product explainer's feature panels, an
  animated card grid where each card steps forward in turn, or any "frosted glass panels that
  zoom out and come back" / "liquid glass" look. Triggers: "liquid glass cards", "glassmorphism
  panels", "frosted glass UI", "cards that zoom forward then fall back", "glass panel zooming
  out and back", "animated card grid that highlights one at a time", "camera zoom into the scene".
---

# Glass Cards

The signature **liquid-glass card** system: frosted translucent panels with a neon gradient border and a glass shine, sitting on a dark gradient background with a drifting glow and dot grid — where one card **zooms/rises forward** to play its content, then **falls back** to the grid as the next rises, all under a gentle **camera zoom-in → settle**. Drop-in via `assets/glass.css` + `assets/glass.js`.

## Pieces (pick what you need)
- **Animated background** — `.stage` (dark multi-gradient, 16:9, container-query units) + `.bgfx` (soft dot grid) + `.wash` (slow drifting glow orb).
- **Liquid-glass card** — `.lcard`: frosted `backdrop-filter` glass, a masked **gradient border** (`::before`, fed by `--edge`), and a diagonal **shine** (`::after`). Set `--accent`/`--accent2`/`--edge` per scene for the color.
- **Zoom-forward / fall-back** — toggle `.up` on the active card (it grows to a forward "hero" size and turns **dark + opaque** so nothing shows through it) and `.dim` on the rest; switching `.up` to the next card makes the current one fall back. The `left/top/width/height` transition does the zoom.
- **Staggered entrance** — add `.cardsin` to the stage/scene to play `cardIn` (cards rise + fade in one after another).
- **Camera zoom** — wrap scenes in `.world`; `enterScene(world)` nudges scale to ~1.06 then settles to 1.0 (the 1.6s CSS transition is the move).

## Minimal usage
```html
<div class="stage"><div class="bgfx"></div><div class="wash"></div>
  <div class="world"><section class="scene">
    <div class="cardstage">
      <div class="lcard" data-k="a"><div class="pad">…card A…</div></div>
      <div class="lcard" data-k="b"><div class="pad">…card B…</div></div>
      <div class="lcard" data-k="c"><div class="pad">…card C…</div></div>
    </div>
  </section></div>
</div>
<script src="glass.js"></script>
<script>
  const stage = document.querySelector('.cardstage');
  placeGrid(stage, 3, 1);                 // lay the cards out in a grid
  enterScene(document.querySelector('.world'));   // camera zoom-in → settle
  revealCards(document.querySelector('.scene'));  // staggered entrance
  // step through them on cue (e.g. from vo-sync timing): raise(stage,'a') → raise(stage,'b') → …
  raise(stage, 'a');
</script>
```
`raise(stage, key)` zooms that card forward and dims the rest; call it again with the next key to make the current fall back and the next rise. `raise(stage, null)` drops everything back to the grid.

## Liquid glass variants (v3–v6 tokens)
The default `.lcard` is one glass material. A real film usually needs three, and they are not
restyles of each other — they are different answers to "what is behind this card?". All three ship
as custom properties in `assets/glass.css`; two of them also ship as card variants.

| token group | material | use it when |
|---|---|---|
| `--lg-*` → **`.lcard.violet`** | **dark violet liquid glass** — a violet→pink tint over a faint white base, a bright highlight **streak** across the top 42 %, a soft violet inner glow, a pale violet edge, `blur(40px) saturate(180%)` | the ground is dark and you want the card to read as *glass* — the ground's colour should come through it |
| `--lgl-*` | **light glass** — a much weaker tint over `rgba(255,255,255,.55)`, a single white top highlight, a soft violet-tinted shadow, `blur(30px) saturate(160%)` | the ground is pale; a dark-glass recipe on a pale ground just looks grey |
| `--lgw-*` → **`.lcard.white`** | **WHITE glass floating on a dark ground** — near-opaque white (`.96 → .84`), a white edge with a violet hairline, a deep `0 30px 70px rgba(20,8,60,.35)` shadow | the ground is dark *and* the card holds real content (UI, tables, body copy). The card is a lit surface **above** the ground, not a window into it |

```html
<div class="lcard violet" data-k="a"><div class="pad">…</div></div>
<div class="lcard white"  data-k="b"><div class="pad">…</div></div>
```
Light glass has no class of its own on purpose — point the main tokens at it in one line:
```css
.scene.pale .lcard{--lg-bg:var(--lgl-bg);--lg-border:var(--lgl-border);
                   --lg-hi:var(--lgl-hi);--lg-shadow:var(--lgl-shadow);--lg-blur:var(--lgl-blur);}
```

### Card-scoped ink (the one that bites)
On a dark ground the frame's ink is light — headings, kickers, captions are all pale. A **white**
card in that frame needs the opposite. So `.lcard.white` **re-declares `--ink` on the card itself**:

```css
.lcard.white{ --ink:#1c1633; --ink-dim:#4c4668; --ink-faint:#7c7794;
              --line:rgba(28,22,51,.12); --line2:rgba(28,22,51,.2); }
```
Three rules, learned the hard way:
- The declaration must sit **on the surface element**, not on a wrapper around it. If a ground
  writes ink tokens on `:root` per frame (see `mark-driven-ground`), anything declared higher up is
  shadowed for the card's whole subtree and the text goes white-on-white for a few frames.
- Re-declare **every** ink token the card's contents might read — text, dim text, faint text, hairlines,
  chart fills — not just the main one. One missed token is one invisible label.
- Anything that lifts out of a white surface (a toast, a tooltip, a zoomed copy of the card) is
  *also* a white surface: give it the same block, or it inherits the frame's light ink.

### Token table
| | violet (`--lg-*`) | light (`--lgl-*`) | white-on-dark (`--lgw-*`) |
|---|---|---|---|
| background | streak + violet/pink tint + `rgba(255,255,255,.07)` | weak tint + `rgba(255,255,255,.55)` | `linear-gradient(180deg,#fff .96,#fff .84)` |
| border | `rgba(196,181,253,.30)` | `rgba(124,58,237,.18)` | `rgba(255,255,255,.9)` |
| highlight | `inset 0 1px 0 rgba(255,255,255,.28)` + `inset 0 0 44px rgba(167,139,250,.14)` | `inset 0 1px 0 rgba(255,255,255,.8)` | `inset 0 1px 0 #fff` + `0 0 0 1px rgba(124,58,237,.18)` |
| shadow | `0 22px 54px rgba(0,0,0,.42)` | `0 18px 44px rgba(76,29,149,.12)` | `0 30px 70px rgba(20,8,60,.35)` |
| blur | `blur(40px) saturate(180%)` | `blur(30px) saturate(160%)` | `blur(30px) saturate(160%)` |
| ink | `#f6f4ff / #b3adcf / #7c7794` | `#1c1633 / #4c4668 / #7c7794` | `#1c1633 / #4c4668 / #7c7794` |

The `--*-blur` tokens are the only blur in the file. Set them to `none` at capture time — headless
Chromium/Edge software-rasterizes `backdrop-filter` and the tint + streak + edge carry the look
without it (see `smooth-render`).

## Composes with the other skills
- **kinetic-typography** — put a `.lead` (headline) beside the `.cardstage` and mark the scene `.choreo dk-left|dk-right` so the headline gets pushed aside as the cards arrive.
- **vo-sync** — drive `raise()` and `enterScene()` from `timing.json` so each card zooms forward exactly when the voiceover names it.
- **smooth-render** — renders cleanly: the glass/zoom are CSS transitions (scale their durations by 1/RATE) and the camera/raise are state toggles. Drop `backdrop-filter` at capture time (per-frame expensive, visually negligible over the gradient).

## Notes
- Units are `cqw`/`cqh` (relative to `.stage`); keep content inside the stage container.
- The forward card is intentionally **opaque** so lower cards don't bleed through it; the others sit at ~28% (`.dim`). Tune `.lcard.up` size/position (or add `[data-type]` variants) for taller demo content.
