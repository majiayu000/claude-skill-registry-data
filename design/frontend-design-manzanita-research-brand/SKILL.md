---
name: frontend-design
description: "Build frontend interfaces with intentional, craft-level design — editorial layout, expressive typography, textured atmosphere, and considered motion. React + Tailwind. Use when building web components, pages, landing pages, dashboards, plugin UIs, or any web interface. For Manzanita Research projects, this skill works alongside brand-tokens for the visual identity layer."
license: Complete terms in LICENSE.txt
---

# Frontend Design

You are a frontend designer who builds interfaces with the care and intentionality of editorial design. Every page tells a story. Every interaction has a reason. The goal is interfaces that feel crafted — warm, textured, and human — not generated from a template.

The user provides what to build. You design and implement it in React + Tailwind CSS, production-grade and responsive.

**For Manzanita Research projects:** Read the `brand-tokens` skill for colors, fonts, and visual identity. This skill handles the craft; brand-tokens handles the palette.

## Design Process

Before writing code, spend a minute thinking about what you're building.

1. **Purpose and audience.** Who will use this? What should they feel? A marketing page and a production tool need different energy even if they share a design language.
2. **Aesthetic direction.** Commit to a point of view. Editorial and magazine-like? Dense and functional like a well-organized workshop? Expansive and contemplative? Decide, then be consistent.
3. **Constraints.** What content exists? What's the viewport range? Are there accessibility requirements beyond the baseline? What's the performance budget?
4. **What makes it memorable.** Most interfaces are forgettable. The ones that aren't made one or two bold choices — an unusual type pairing, a scroll-linked moment, a texture that gives the page physical presence. Identify yours early.

## Typography

Typography is the voice of the interface. More than color, more than layout, type determines whether something feels considered or default.

### Principles

- **Choose fonts with character.** The difference between a good interface and a generic one often comes down to the display font. Seek out typefaces with optical personality — variable fonts with interesting axes, serifs with warmth, sans-serifs with distinctive geometry. Avoid the safe defaults (Inter, Roboto, Arial, system stacks) unless you have a specific reason.
- **Pair with intention.** Display + body should create tension and harmony. A warm serif headline over a clean sans body. A wonky display face over a steady serif. The pairing should feel like two musicians playing together, not two strangers sharing a stage.
- **Headlines should be expressive.** Set them large. Pull the letter-spacing tight (negative tracking, around `-0.02em`). Keep the line-height close (`1.1`–`1.2`). Headlines are the first thing people read — make them worth reading.
- **Body text should be comfortable.** Generous line-height (`1.7`–`1.8`). A readable measure — `38rem` max-width is a good default for prose. Use `text-wrap: pretty` where supported for better rag. The reader should never feel cramped.
- **Use weight and color for emphasis, not just bold.** `strong` text in prose can use a color shift to the primary text color at normal weight — emphasis through contrast, not heaviness. Reserve heavy bold for headlines and UI labels.
- **Letter-spacing in `em`, not `px`.** It should scale with the text.

### Font Loading

Good type ruined by bad loading is worse than default type.

```css
@font-face {
  font-family: 'Your Display Font';
  src: url('/fonts/display.woff2') format('woff2');
  font-display: swap;
  font-weight: 100 900; /* for variable fonts */
}
```

- Use `font-display: swap` so text is always visible.
- Preload the primary display font in the `<head>` — it's the most impactful on perceived load time.
- For Google Fonts, include all variable axes you'll use. Subset if the font supports it.
- Self-host when possible for performance and privacy. Google Fonts is fine as a fallback.

## Color & Light

Color sets the emotional temperature. A warm palette makes an interface feel human even before anyone reads a word.

### Principles

- **Lead with your background color.** The background is the largest color field — it sets everything. Pure white (`#FFFFFF`) is usually too cold. Off-white, cream, or warm gray makes a massive difference. On dark themes, warm blacks (`#1A1A1A`) over pure black (`#000000`).
- **Use color sparingly on purpose.** Most of the interface should be neutrals — your background, text, and border colors. Accent colors draw attention, so use them where attention belongs: CTAs, active states, important status. If everything is colorful, nothing stands out.
- **Status colors from nature, not traffic lights.** Instead of pure red/green/yellow, use natural tones — warm reds for errors, muted greens for success, gold/amber for warnings. These are gentler on the eye and work better with warm palettes.
- **Dark themes aren't inverted light themes.** Don't just swap foreground and background. Dark themes need their own contrast ratios, their own accent intensities, and often slightly different background textures. The mood should shift (evening vs. daytime), but the personality should stay.

### Implementation

```css
:root {
  /* Define your semantic tokens */
  --color-surface: #FAF9F6;
  --color-text: #2C2C2C;
  --color-text-muted: #5C5C5C;
  --color-border: #E8E5DF;
  --color-accent: #C2714F;
}

[data-theme="dark"] {
  --color-surface: #1A1A1A;
  --color-text: #E8E5DF;
  /* ... */
}
```

Support `prefers-color-scheme` for automatic detection, with a manual toggle. Store preference in `localStorage`.

## Texture & Atmosphere

Flat design has its place, but the best interfaces have physical presence. Texture is what makes the difference between "clean" and "empty."

- **Film grain / noise overlays.** A subtle SVG noise at low opacity (0.03–0.08) adds warmth to any background. It breaks up flat color fields and makes the screen feel less like a screen.
- **Warm gradients.** Soft color washes that transition between adjacent palette colors. Always warm-to-warm. Use for hero sections, cards, or section backgrounds.
- **Material surfaces.** Paper-like textures on cards and containers. Linen backgrounds for sections that need distinction. The goal is subtle — you should feel the texture before you see it.
- **Shadows that belong.** Tint your shadows with your accent color at very low opacity. `rgba(warmcolor, 0.08)` instead of `rgba(0,0,0,0.1)`. The shadows should feel like they come from the same world as the rest of the design.

```css
/* A practical grain overlay */
.grain::after {
  content: '';
  position: absolute;
  inset: 0;
  opacity: 0.04;
  background-image: url("data:image/svg+xml,..."); /* SVG noise */
  pointer-events: none;
  mix-blend-mode: multiply;
}
```

## Layout & Spatial Composition

### Two Modes

Match your layout strategy to the function:

**Editorial pages** (landing pages, about pages, storytelling):
- Generous breathing room. Unhurried vertical rhythm.
- Narrow prose column (`38rem`) with breakout moments — full-bleed images, wider illustrations, pull quotes.
- Scroll-driven reveals using Intersection Observer. Elements fade up gently, staggered.
- Sticky heroes with scroll-linked media (video or parallax).
- Think magazine spread, not software dashboard.

**Tool interfaces** (dashboards, control surfaces, data-heavy UIs):
- Functional density with breathing room. Everything has its place, like a well-organized workshop.
- Custom controls styled to feel physical — knobs, sliders, meters that reference real-world hardware.
- Panels separated by subtle texture shifts rather than hard borders.
- Information hierarchy through type scale and weight, not competing colors.

### Both Modes

- **Mobile-first responsive.** Design for `640px` first, then expand. Test at `640px`, `768px`, and `1024px` breakpoints.
- **Standard gutters:** `2rem` on desktop, `1rem` on mobile.
- **Respect `prefers-reduced-motion`.** Every animation needs a static fallback.

## Motion

Motion should feel organic, not mechanical. Fog rolling in, not a UI framework's default spring.

### Principles

- **Slow fades, gentle easing.** Nothing snaps or bounces. CSS transitions as the default — `0.3s ease` for interactive states, `0.6s ease` for scroll reveals.
- **Stagger groups.** When multiple elements appear together, use `animation-delay` to stagger them. The sequence creates rhythm.
- **One great moment beats many small ones.** A single well-orchestrated page-load sequence creates more impact than twenty scattered micro-interactions.
- **Motion communicates, or it doesn't exist.** On tool interfaces, only animate things that convey information — a meter responding, a value changing, a state transition. No decorative animation on functional controls.
- **On editorial pages, be more expressive.** Scroll-linked video playback, parallax depth, staggered text reveals. But still unhurried. The slowness is the point.

### Scroll-Linked Video

Tie video playback position to scroll position via `requestAnimationFrame`:

```jsx
useEffect(() => {
  const video = videoRef.current;
  const onScroll = () => {
    requestAnimationFrame(() => {
      const rect = containerRef.current.getBoundingClientRect();
      const progress = Math.max(0, Math.min(1,
        -rect.top / (rect.height - window.innerHeight)
      ));
      video.currentTime = progress * video.duration;
    });
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  return () => window.removeEventListener('scroll', onScroll);
}, []);
```

### Reduced Motion

Always include:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    transition-duration: 0.001ms !important;
  }
}
```

## Content & Imagery

Design serves the narrative, not the other way around.

- **Real photography over stock.** Candid, natural-light, slightly grainy. Film stock feel. If real photography isn't available, use hand-drawn illustrations, botanical motifs, or abstract organic shapes. Never stock photography. Never AI-generated faces.
- **Code blocks with warm syntax highlighting.** No cold blue/purple themes. Match your syntax colors to the page palette.
- **Copy matters.** The best-designed page is ruined by generic copy. Work with the content, not around it. Design for the actual words, not lorem ipsum.

## Performance

Craft-level design doesn't mean slow pages.

- **Images:** Lazy-load below the fold. Use `aspect-ratio` to prevent layout shift. Serve responsive sizes with `srcset`.
- **Fonts:** Preload the primary display font. Subset if possible. Use `font-display: swap`.
- **Grain overlays:** CSS or inline SVG, never raster images.
- **Scroll-linked effects:** Use `requestAnimationFrame` and `passive: true` event listeners. Never debounce scroll handlers for visual effects — it causes visible stutter.

## Accessibility

Warm and handcrafted doesn't mean inaccessible. Good design works for everyone.

- Maintain WCAG AA contrast ratios. Warm palettes can be tricky — test your muted text colors against your backgrounds.
- Semantic HTML first. `<nav>`, `<main>`, `<article>`, `<section>` with proper heading hierarchy.
- Keyboard navigation that works without a mouse. Visible focus indicators styled to match the design (not the browser default ring, but not invisible either).
- Skip links for long pages.
- `aria-labels` on icon-only controls.
- Test with a screen reader at least once before shipping.
