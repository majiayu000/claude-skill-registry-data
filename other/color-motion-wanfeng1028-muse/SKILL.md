---
name: color-motion
description: This skill should be used when the user asks to "build a color palette for a motion piece", "make a gradient background", "animate a color transition", "interpolate colors smoothly", "fix muddy/gray gradients", "convert colors to OKLCH", "color-grade a video for mood", "fix washed-out After Effects renders", "gamma shift", "Rec.709 vs sRGB", "colors shifted after rendering", or "match preview to final video". Covers palette construction, gradients, perceptual interpolation (OKLCH/Lab), grading order, and video/render color management.
version: 0.1.0
---

# Color in Motion

Choose, pair, and animate color for motion design: building restrained palettes, constructing gradients that read as premium, interpolating colors in perceptually-uniform spaces, and grading a piece for mood and consistency. Produces palettes with exact OKLCH/hex values, gradient CSS/code, and transition parameters.

## When to use

- Picking or pairing a palette for a motion or video piece.
- Building gradient backgrounds (mesh, noise, animated drift).
- Animating color transitions (button states, theme switch, loaders).
- Grading a video for mood, or fixing dull/gray gradient interpolation.
- Fixing washed-out, gamma-shifted, or platform-inconsistent After Effects renders, and choosing correct per-platform export/color tags.

## Core techniques

### 1. Build a restrained palette

Limit hues. A strong motion palette is **1 primary + 1 accent + 2-3 neutrals**. Derive contrast and depth from lightness and chroma, not from adding more hues. Extra hues fight for attention and read as amateur.

In dark scenes, make the accent pop with **low-to-moderate chroma and high lightness** rather than maximum saturation — a blown-out saturated accent vibrates and looks cheap on dark backgrounds.

Use OKLCH to reason about color: `oklch(L C H)` where L is perceptual lightness (0-1), C is chroma (0 ≈ 0.37 max), H is hue angle (0-360). Holding L and C constant while rotating H gives hues of genuinely equal visual weight — impossible to do reliably in HSL.

```
Primary:   oklch(0.62 0.19 264)   /* confident blue */
Accent:    oklch(0.78 0.17 50)    /* warm amber, lighter so it pops */
Neutral-0: oklch(0.97 0.005 264)  /* near-white, faint hue tint */
Neutral-1: oklch(0.55 0.01 264)
Neutral-2: oklch(0.18 0.015 264)  /* near-black, same hue family */
```

Tinting neutrals slightly toward the primary hue (tiny chroma) unifies the frame; pure gray neutrals next to colored elements look disconnected.

### 2. Interpolate in OKLCH or Lab — never raw sRGB

Linearly interpolating two colors in sRGB passes through a desaturated, often gray or muddy midpoint (blue->yellow goes through gray; blue->red through muddy purple). Perceptual spaces (OKLCH, OKLab, CIE Lab) keep midpoints vivid and lightness even.

CSS gradients support this natively:

```css
/* Vivid, even midpoint */
background: linear-gradient(in oklch, #2b6cff, #ffb02e);

/* Control hue path around the wheel for two-stop gradients */
background: linear-gradient(in oklch longer hue, #2b6cff, #ffb02e);
background: conic-gradient(in oklch, red, blue, red);
```

For animated transitions interpolate with a library (see references) and emit per-frame colors, or for two-color CSS transitions register a typed custom property so the browser interpolates in the chosen space.

### 3. Gradients that read as premium

- **Mesh / multi-radial**: stack several `radial-gradient`s at different positions over a base color. Soft, organic, expensive-looking.
- **Add grain**: a faint noise overlay (SVG `feTurbulence` or a tiled PNG at ~3-5% opacity) kills banding and adds texture.
- **Animate slowly**: drift gradient positions over 8-20s with `ease-in-out alternate`. Slow is premium; fast gradient motion looks like a screensaver.

```css
.mesh {
  background-color: #0b0f1a;
  background-image:
    radial-gradient(at 20% 25%, oklch(0.62 0.19 264 / 0.7), transparent 50%),
    radial-gradient(at 80% 30%, oklch(0.70 0.16 320 / 0.6), transparent 55%),
    radial-gradient(at 50% 85%, oklch(0.78 0.17 50  / 0.5), transparent 50%);
  animation: drift 16s ease-in-out infinite alternate;
}
@keyframes drift {
  to { background-position: 8% -6%, -8% 6%, 4% 8%; }
}
```

### 4. Color transition animation

Inline timing essentials so this skill stands alone: enter/highlight with ease-out (`cubic-bezier(0.16, 1, 0.3, 1)`), state changes 150-300ms, theme/full-screen washes 400-800ms. Use `linear` only for continuous loops.

```css
@property --c { syntax: "<color>"; initial-value: #2b6cff; inherits: false; }
.btn { background: var(--c); transition: --c 200ms cubic-bezier(0.16,1,0.3,1); }
.btn:hover { --c: #ffb02e; }
```

`@property` registration is what makes the color actually interpolate (unregistered custom properties jump instantly).

### 5. Grade for mood — correct order

Apply grading operations in this order; reordering changes the result:

1. **Exposure / white balance** — fix overall brightness and neutralize/intentionally set the cast first.
2. **Contrast** — set black and white points; expand or compress the tonal range.
3. **Midtones / saturation** — adjust overall saturation and midtone color.
4. **Split-tone** — tint shadows and highlights separately. The classic cinematic look is **teal shadows + orange highlights** (complementary, flatters skin). Keep it subtle.
5. **Unify** — a final overall tint/LUT and a subtle vignette to bind the frame.

In code, grade by chaining CSS filters or a fragment shader; for video, an actual LUT or grading panel. Always grade the whole piece consistently so shots cut together.

### 6. Video / render color management

When a render looks correct in the After Effects comp viewer but washed-out, too bright, milky, or gamma-shifted in QuickTime, a browser, or across macOS/Windows, the cause is a gamma/transfer mismatch across four stages — AE working space, the render's embedded tag, the player's interpretation, and the display/OS gamma — not the artwork.

Core rules:

- **Set an explicit working space.** File > Project Settings > Color tab: Working Space = **Rec.709 Gamma 2.4** for SDR video (or **sRGB** for UI/stills); "None" disables color management and the viewer lies about the final look. Set Depth to **16 bpc** for grades/gradients to avoid banding.
- **Rec.709 vs sRGB.** They share primaries but differ in transfer (sRGB ~2.2 piecewise vs Rec.709 display 2.4 / BT.1886). Using the wrong one shifts midtone brightness — Rec.709 for video, sRGB for screenshots/PNG/UI.
- **Embed a color tag on export.** The shift across macOS/Windows/players comes from untagged files; each player guesses its own default. Tag Rec.709 (or sRGB) explicitly via Render Queue > **Output Module > Color Management** (do not leave "Preserve RGB" when a shift occurs).
- **The QuickTime gamma bug.** QuickTime/AVFoundation apply an extra ~1.96 gamma, so a file can look fine in QuickTime but dark/contrasty in Chrome. **Never grade or approve to QuickTime** — Chrome, Premiere, or Resolve is the correct reference for web delivery.
- **Match preview to final.** Toggle "Use Display Color Management" in the comp viewer while reviewing, and verify the export numerically: place a 50% grey (RGB 128) patch, render, re-sample — a value that rises (128 → 150+) confirms a washed-out gamma shift. Confirm the embedded tag with `ffprobe` (`color_primaries`/`color_transfer`/`color_space` = bt709).

Per-platform export at a glance: **ProRes 422 HQ/4444** tagged Rec.709 for editing masters; **H.264 (MP4)** tagged Rec.709 for web/`<video>`/social (verify in Chrome); ProRes 4444 + alpha → PNG (sRGB) for transparency; ProRes 4444 / HEVC 10-bit Rec.2020 PQ/HLG for HDR (needs 32 bpc float).

See `references/color-management.md` for the full diagnosis decision tree, exact menu paths, per-platform export table, the QuickTime workarounds, per-OS/player gamma values, the numeric test-patch method, `ffprobe`/`ffmpeg` tag commands, limited-vs-full-range pitfalls, and the pre-export checklist.

## Deliver & verify (standalone HTML)

> **Packaged helper** (`scripts/`): `scripts/seek-shot.sh anim.html 0 1.5 3` freezes the `?t=N` harness and screenshots each moment; `scripts/contact-sheet.sh sheet.png frame-*.png` tiles them for one-glance review. See `scripts/README.md`.

For a web palette/gradient/color-transition deliverable, ship **one `.html` file that opens directly in a browser** — no build step. CSS handles the color work; the file is self-contained.

**Output contract:**
- One `.html` file: your markup + the gradient/transition in inline `<style>` (CDN only if a JS interpolation lib is needed).
- One animation driver — a CSS `@keyframes` drift or a single `@property` transition; nothing competing.
- Include the freeze harness below so any moment can be screenshotted deterministically.

**Freeze harness — pin a CSS-animation frame for screenshots.** `?t=N` sets a negative `animation-delay` and pauses, so the gradient/transition lands on the exact frame at `N` seconds.

```html
<script>
  const t = new URLSearchParams(location.search).get("t");
  if (t !== null) {
    document.querySelectorAll(".bg, .btn").forEach(el => {       // animated elements
      el.style.animationDelay = (-parseFloat(t)) + "s";
      el.style.animationPlayState = "paused";
    });
  }
  window.__ready = true;                                          // ready signal for headless wait
</script>
```

**Verify loop — render → freeze → screenshot → check:**
1. Open the file frozen at start / mid / end: `…/color.html?t=0`, `?t=<period/2>`, `?t=<period>`.
2. Screenshot each frozen frame.
3. Check **fidelity** (matches the palette/brief) and **color artifacts** — at each frozen frame confirm the gradient/transition has **no banding and no muddy or gray midpoint** (the OKLCH/Lab path stays vivid). Add grain if banding appears.
4. **Iterate:** if banding or a muddy/gray midpoint shows up, adjust the OKLCH/Lab chroma & lightness (or add grain), re-render the **same** `?t=N`, and re-screenshot to confirm the fix — loop until every frozen frame is clean.

```bash
npx playwright screenshot --wait-for-timeout=500 "file://$PWD/color.html?t=8" frame-mid.png
```

**Before you finish:**
1. Opens standalone in a browser — no console errors, no missing CDN.
2. One color driver; `?t=N` freezes the exact frame correctly.
3. Screenshotted at start / mid / end — no banding, no muddy/gray midpoints, lightness even.
4. `prefers-reduced-motion` honored (drift paused on a static, readable frame).
5. Interpolation is in OKLCH/Lab (gradients/`@property`), never raw sRGB.

## Quick reference

| Need | Do |
|---|---|
| Palette size | 1 primary + 1 accent + 2-3 neutrals |
| Equal-weight hues | hold L,C in OKLCH, vary H |
| Vivid gradient | `linear-gradient(in oklch, ...)` |
| Smooth color anim | interpolate in OKLCH/Lab, register via `@property` |
| Premium bg | stacked radials + grain + 8-20s slow drift |
| Cinematic grade | teal shadows / orange highlights, subtle |
| Fix washed-out AE render | tag Rec.709 in Output Module > Color Management; verify in Chrome |
| Avoid | raw-sRGB interpolation (muddy midpoints); grading to QuickTime |

## Reference files

- `references/palettes-and-interpolation.md` — palette construction rules with OKLCH values and named recipes, gradient cookbook (mesh, conic, grain), culori and d3-interpolate code for perceptual interpolation and scales, and the full grading-order checklist with filter/shader examples.
- `references/color-management.md` — full video/render color management: diagnosis decision tree, AE project/output color settings with exact menu paths, per-platform export table, QuickTime gamma-bug workarounds, per-OS/player gamma values, the numeric test-patch method, `ffprobe`/`ffmpeg` tag verification, limited-vs-full-range pitfalls, and the pre-export checklist.
