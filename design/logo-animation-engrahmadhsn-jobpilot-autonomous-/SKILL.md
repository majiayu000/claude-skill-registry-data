---
name: logo-animation
description: This skill should be used when the user asks to "animate our logo", "make a logo intro/stinger", "build a brand reveal", "create an app splash animation", "loop a loader logo", "draw on our SVG mark", "morph an icon into the wordmark", or "sync the logo to a sound-logo". Covers web (SVG/Lottie), video, and app-splash delivery.
version: 0.1.0
---

# Logo Animation

Bring a brand mark to life with one clear idea, on-brand geometry, and a crisp settle. Animate for web (SVG/Lottie), video intros/outros, or app splash screens, and always ship a static end-frame fallback.

## When to use

- Build an intro stinger, sign-off, app splash, or loader idle loop.
- Reveal a brand mark on a landing hero or sizzle reel.
- Draw on an SVG mark, wipe/build it in piece by piece, or morph an icon into a wordmark.
- Sync the final settle of the mark to a sound-logo beat.

## Core principle

Pick ONE technique per logo — draw OR build OR morph — not all at once. Reveals run 0.8–2.5s. Never distort brand geometry; scale and fade are safe, skew and squash usually are not. Respect clearspace (keep the mark's minimum margin clear of motion debris). Always provide a `prefers-reduced-motion` path that shows the final mark with no motion.

## Technique map

| Technique | Best for | Mechanism |
|---|---|---|
| Stroke draw-on | Line marks, monograms, signatures | `stroke-dashoffset` 1→0 |
| Mask wipe / reveal | Filled shapes, gradients | animate a `<clipPath>` / `<mask>` rect |
| Build-on (stagger) | Multi-piece marks, grids | per-group opacity+transform, staggered |
| Morph | Icon ↔ wordmark, shape→logo | GSAP MorphSVG or matched path interpolation |
| Idle loop | Loaders, ambient splash | seamless cyclic transform (rotate/pulse) |
| Wordmark | Logotypes | per-letter mask/translate stagger |

## Quick start: SVG stroke draw-on

The fastest on-brand web reveal. Each path draws itself, then fills settle in.

```html
<svg viewBox="0 0 200 80" id="logo">
  <path class="ink" d="M10 60 L40 20 L70 60" fill="none"
        stroke="#111" stroke-width="6" stroke-linecap="round"
        pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
</svg>
<style>
  @keyframes draw { to { stroke-dashoffset: 0; } }
  #logo .ink { animation: draw 1.1s cubic-bezier(.65,0,.35,1) forwards; }
  @media (prefers-reduced-motion: reduce) {
    #logo .ink { animation: none; stroke-dashoffset: 0; }
  }
</style>
```

`pathLength="1"` normalizes every path to length 1, so one `stroke-dasharray`/`offset` value works regardless of geometry. Stagger multiple strokes with `animation-delay`.

## Quick start: build-on with stagger (GSAP)

```js
import gsap from "gsap";
// each <g class="piece"> is one mark component
gsap.from(".piece", {
  opacity: 0, scale: 0.85, transformOrigin: "50% 50%",
  duration: 0.5, ease: "back.out(1.6)", stagger: 0.08,
  onComplete: () => gsap.to("#mark", { scale: 1, duration: 0.2, ease: "power2.out" })
});
```

Group order matters: reveal the base/container first, then accents, then the wordmark last so the eye lands on the name.

## Sound-logo sync

When audio exists, the brand's final settle frame must land exactly on the sonic accent (the "ding"/whoosh peak). Decide the audio first, find the peak timecode, then time the reveal so the mark snaps to full opacity/scale on that frame. A 1.0s reveal landing a 1.2s mnemonic feels premium; a settle that floats free of the sound feels cheap. Add a tiny overshoot-and-settle (scale 1.04→1.00 over ~0.15s) on the beat for impact.

## Delivery targets

- **Web, interactive / hero**: inline SVG + CSS or GSAP. Smallest payload, crisp at any size, scriptable.
- **Product / app, designer-made**: Lottie (`.json` exported from After Effects via Bodymovin). Use `lottie-web` or `@lottiefiles/dotlottie-web`; set `loop`, `autoplay`, and a poster fallback frame.
- **Video intro/outro**: Remotion (React) or After Effects render to ProRes/H.264. Pre-render at 2x for crispness.

```js
// Lottie delivery with reduced-motion guard
import { DotLottie } from "@lottiefiles/dotlottie-web";
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const dl = new DotLottie({
  canvas: document.querySelector("#logo-canvas"),
  src: "/logo.lottie", autoplay: !reduce, loop: false,
});
if (reduce) dl.addEventListener("load", () => dl.setFrame(dl.totalFrames - 1));
```

## Output checklist

- Animated mark in the target format (SVG/Lottie/video).
- Static final-frame fallback (SVG or PNG) for reduced-motion and posters.
- One clear technique, reveal ≤2.5s, brand geometry intact, clearspace respected.
- Sound-logo settle aligned to the audio peak (if audio present).

## Deliver & verify (standalone HTML)

> **Packaged helper** (`scripts/`): `scripts/seek-shot.sh anim.html 0 1.5 3` freezes the `?t=N` harness and screenshots each moment; `scripts/contact-sheet.sh sheet.png frame-*.png` tiles them for one-glance review. See `scripts/README.md`.

Logo animation spans web/SVG/Lottie, video, and app splash. **For web/SVG/Lottie delivery use this standalone-HTML loop; for a video logo sting, render via the remotion-video verify loop instead.**

For web/SVG/Lottie, ship **one `.html` file that opens directly in a browser** — inline SVG markup plus the reveal (CSS or one CDN GSAP `<script>`), self-contained. One file is the right tier.

**Output contract:**
- One `.html` file: the inline SVG (or Lottie canvas) + the reveal in inline `<style>`/`<script>`.
- One animation driver — the CSS `@keyframes` draw/build, or a single GSAP timeline; not both.
- Include the freeze harness below, matched to the technique, so any moment can be screenshotted deterministically.

**Freeze harness — pin a frame for screenshots.** Match the mechanism to the technique:

```html
<script>
  const t = new URLSearchParams(location.search).get("t");
  if (t !== null) {
    const T = parseFloat(t);
    // CSS stroke-draw / build-on:
    document.querySelectorAll("#logo *").forEach(el => {
      el.style.animationDelay = (-T) + "s";
      el.style.animationPlayState = "paused";
    });
    // GSAP timeline instead? → tl.pause(); tl.seek(T);
    // SMIL <animate>?       → const s = document.querySelector("svg"); s.pauseAnimations(); s.setCurrentTime(T);
    // Lottie?               → dl.setFrame(Math.round(T * fps));
  }
  window.__ready = true;                                          // ready signal for headless wait
</script>
```

**Verify loop — render → freeze → screenshot → check:**
1. Open the file frozen at start / mid / end of the reveal (≤2.5s): `…/logo.html?t=0`, `?t=<dur/2>`, `?t=<dur>`.
2. Screenshot each frozen frame.
3. Check **fidelity** (matches the mark, one clear technique) and **artifacts** — brand geometry undistorted, clearspace clear of motion debris, no half-drawn strokes left at the end frame, the static final frame is the true logo.
4. **Iterate:** if any check fails (e.g. a half-drawn stroke at `?t=<dur>` or distorted geometry mid-reveal), fix the stroke-dashoffset/duration/easing, re-render the **same** `?t=N`, and re-screenshot to confirm the fix — loop until every frame is clean.

```bash
npx playwright screenshot --wait-for-timeout=500 "file://$PWD/logo.html?t=1.1" frame-mid.png
```

**Before you finish:**
1. Opens standalone in a browser — no console errors, no missing CDN.
2. One technique/driver; `?t=N` freezes the exact frame correctly.
3. Screenshotted at start / mid / end — geometry intact, clearspace respected, final frame is the clean mark.
4. `prefers-reduced-motion` honored (final static mark shown, no motion) + static end-frame fallback shipped.
5. Reveal ≤2.5s; if audio present, the settle lands on the sound-logo peak.

## Reference files

- `references/logo-patterns.md` — runnable code for every technique: stroke draw-on, mask wipe build-on, GSAP MorphSVG morph, seamless idle loop, Lottie delivery, plus timing tables (0.8–2.5s), brand clearspace rules, and reduced-motion fallbacks.
