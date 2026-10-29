---
name: frontend-slides
description: "Use when building standalone HTML/CSS/JS presentation slide decks — self-contained single-file decks with viewport-fit layout, keyboard navigation, and browser Print-to-PDF export."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Self-contained: one HTML file with inline CSS and JS. No build step, no framework, no external tooling.
- Vanilla HTML/CSS/JS only — no React, no bundler, no Node scripts, no Python.
- Viewport fit is a hard gate: every slide fits one viewport with no internal scrolling.
- Accessibility is required: semantic headings, readable contrast, `prefers-reduced-motion` support.

## Use when
- Building a talk deck, pitch deck, workshop deck, or internal presentation.
- Improving an existing HTML deck's layout, motion, or typography.
- You need a deck that runs from a local file and exports to PDF without installing anything.

## Deck structure
One HTML file. One `<section class="slide">` per slide inside a `<main>`. Theme values live in CSS custom properties so they are trivial to change.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Deck</title>
<style>
:root {
  --bg: #0f172a; --fg: #f8fafc; --accent: #38bdf8;
  --font: system-ui, sans-serif;
}
* { box-sizing: border-box; margin: 0; }
html, body { height: 100%; background: var(--bg); color: var(--fg); font-family: var(--font); }

/* One slide = one viewport. Active slide shown, others hidden. */
.slide {
  position: fixed; inset: 0;
  height: 100vh; height: 100dvh;
  overflow: hidden;
  display: none; flex-direction: column;
  justify-content: center; align-items: flex-start;
  padding: clamp(2rem, 6vw, 6rem);
  gap: clamp(0.75rem, 2vh, 2rem);
}
.slide[aria-current="true"] { display: flex; }

/* Type and spacing scale with the viewport so nothing overflows. */
.slide h1 { font-size: clamp(2rem, 6vw, 5rem); line-height: 1.05; }
.slide h2 { font-size: clamp(1.5rem, 4vw, 3rem); }
.slide p, .slide li { font-size: clamp(1rem, 2.2vw, 1.6rem); line-height: 1.4; max-width: 60ch; }
.slide ul { padding-left: 1.2em; display: grid; gap: clamp(0.4rem, 1.2vh, 1rem); }

.accent { color: var(--accent); }

.progress {
  position: fixed; bottom: 0; left: 0; height: 4px;
  background: var(--accent); transition: width .3s ease;
}

/* Enter animation, disabled for reduced motion. */
.slide[aria-current="true"] > * { animation: rise .5s ease both; }
@keyframes rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
@media (prefers-reduced-motion: reduce) {
  .slide[aria-current="true"] > *, .progress { animation: none; transition: none; }
}
</style>
</head>
<body>
<main>
  <section class="slide" aria-current="true">
    <h1>Deck <span class="accent">Title</span></h1>
    <p>Subtitle or tagline.</p>
  </section>
  <section class="slide">
    <h2>Key points</h2>
    <ul><li>First point</li><li>Second point</li><li>Third point</li></ul>
  </section>
</main>
<div class="progress" id="progress"></div>
<script>
const slides = [...document.querySelectorAll('.slide')];
let current = slides.findIndex(s => s.getAttribute('aria-current') === 'true');
if (current < 0) current = 0;

function show(i) {
  current = Math.max(0, Math.min(slides.length - 1, i));
  slides.forEach((s, n) => s.setAttribute('aria-current', String(n === current)));
  document.getElementById('progress').style.width =
    ((current + 1) / slides.length * 100) + '%';
  location.hash = '#' + (current + 1);
}

document.addEventListener('keydown', e => {
  if (['ArrowRight', 'ArrowDown', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); show(current + 1); }
  if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(e.key)) { e.preventDefault(); show(current - 1); }
  if (e.key === 'Home') show(0);
  if (e.key === 'End') show(slides.length - 1);
});

const fromHash = parseInt(location.hash.slice(1), 10);
show(Number.isFinite(fromHash) ? fromHash - 1 : current);
</script>
</body>
</html>
```

## Viewport fit (hard gate)
- Every `.slide` uses `height: 100vh; height: 100dvh; overflow: hidden;`.
- All type and spacing scale with `clamp()` — never a fixed pixel font that overflows small screens.
- When content does not fit, split it into multiple slides. Never shrink text below readable size and never allow a scrollbar inside a slide.
- Avoid invalid CSS such as a negated `-clamp(...)`.

Validate at: 1920x1080, 1280x720, 768x1024, 375x667, 667x375.

## Typography and spacing
- Strong hierarchy: one dominant heading per slide, supporting text clearly smaller.
- Generous whitespace via `clamp()`-based padding and gaps.
- Choose a palette and type pairing for the talk. Avoid the default deck look: a purple-to-blue gradient, a centered title over a blurred atmospheric image, emoji bullets, and the template's slate-and-sky colors left unchanged.

## Accessibility
- Semantic structure: `main`, `section`, real `h1`/`h2`, `ul`/`li`.
- Readable contrast between `--fg` and `--bg`.
- Keyboard-only navigation works (arrows, Page keys, Home/End).
- Honor `prefers-reduced-motion` by disabling animation and transitions.

## Content density limits

| Slide type | Limit |
|------------|-------|
| Title | 1 heading + 1 subtitle + optional tagline |
| Content | 1 heading + 4–6 bullets or 2 short paragraphs |
| Feature grid | 6 cards max |
| Code | 8–10 lines max |
| Quote | 1 quote + attribution |
| Image | 1 image constrained by the viewport |

## Export to PDF (no dependency)
The default path uses the browser's built-in Print-to-PDF. Add a print stylesheet so every slide becomes one page.

```css
@media print {
  @page { size: 1280px 720px; margin: 0; }
  .progress { display: none; }
  .slide {
    position: static; display: flex !important;
    height: 720px; width: 1280px;
    break-after: page;
  }
}
```

Then: open the deck in a browser, Print (Cmd/Ctrl+P), choose "Save as PDF", set margins to None and background graphics on.

Open the deck with the platform opener: macOS `open deck.html`, Linux `xdg-open deck.html`, Windows `start "" deck.html`.

Optional, if available: a headless browser (e.g. a Chromium `--print-to-pdf` invocation) can render the same print stylesheet to PDF unattended. Do not require or install it — the browser Print-to-PDF path always works.

## Anti-patterns
- Generic gradient decks with no visual identity.
- Long bullet walls; code blocks that need scrolling.
- Fixed-height content boxes that break on short screens.
- Disabling reduced-motion support.
- Reaching for a framework or build tool when one HTML file suffices.

## Done when
- The deck runs from a local file in any modern browser.
- Every slide fits the viewport at all five test sizes with no scrolling.
- Arrow/Page/Home/End keyboard navigation works and the progress bar tracks position.
- Reduced-motion is respected.
- Print-to-PDF produces one page per slide.
- File path, slide count, and theme custom properties are explained at handoff.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
