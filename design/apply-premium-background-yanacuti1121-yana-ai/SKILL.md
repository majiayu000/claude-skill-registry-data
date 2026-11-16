---
name: apply-premium-background
description: CSS and Tailwind background effects — animated dots, grids, radial gradients, aurora blurs, mesh gradients, noise textures. Ibelick-style premium backgrounds for hero sections, cards, and full-page layouts.
origin: ibelick/background-snippets (MIT)
license: MIT
version: 1.0.0
compatibility: CSS3, Tailwind v3+, React, Next.js
---

# apply-premium-background

## When to Use

- Building hero sections, landing pages, or splash screens that need depth
- Card backgrounds that feel more polished than a flat color
- Dark-mode UIs that benefit from subtle animated grain or aurora effects
- When the design calls for layered CSS backgrounds without JS overhead

## Do NOT use for

- Content-heavy reading areas (backgrounds distract from text)
- Tables, data grids, code blocks — use `--color-background-subtle` token instead
- Any surface where reduced-motion users will see animation — always respect `prefers-reduced-motion`

---

## Dot Grid Background

```css
/* Dot grid — light and dark variants */
.bg-dot-grid {
  background-color: var(--color-background);
  background-image: radial-gradient(
    circle,
    hsl(var(--dot-color, 215 20% 65%) / 0.4) 1px,
    transparent 1px
  );
  background-size: 24px 24px;
}

/* Dark mode */
.dark .bg-dot-grid {
  --dot-color: 215 20% 35%;
}
```

```jsx
// Tailwind + inline CSS
export function DotGrid({ children }) {
  return (
    <div
      className="relative min-h-screen bg-white dark:bg-gray-950"
      style={{
        backgroundImage:
          "radial-gradient(circle, rgba(99,102,241,0.15) 1px, transparent 1px)",
        backgroundSize: "24px 24px",
      }}
    >
      {children}
    </div>
  );
}
```

---

## Line Grid Background

```css
.bg-line-grid {
  background-color: var(--color-background);
  background-image:
    linear-gradient(var(--grid-color, rgba(100,100,100,0.08)) 1px, transparent 1px),
    linear-gradient(90deg, var(--grid-color, rgba(100,100,100,0.08)) 1px, transparent 1px);
  background-size: 40px 40px;
}
```

---

## Aurora / Mesh Gradient

```css
/* Animated aurora — GPU-composited, uses transform only */
.bg-aurora {
  position: relative;
  overflow: hidden;
}

.bg-aurora::before {
  content: "";
  position: absolute;
  inset: -50%;
  background:
    radial-gradient(ellipse 80% 50% at 20% 40%, hsl(270 60% 60% / 0.35), transparent),
    radial-gradient(ellipse 60% 80% at 80% 20%, hsl(200 80% 60% / 0.3), transparent),
    radial-gradient(ellipse 70% 60% at 50% 80%, hsl(320 70% 65% / 0.25), transparent);
  animation: aurora-drift 12s ease-in-out infinite alternate;
  will-change: transform;
}

@keyframes aurora-drift {
  from { transform: translate(0, 0) rotate(0deg) scale(1); }
  to   { transform: translate(5%, 3%) rotate(3deg) scale(1.05); }
}

@media (prefers-reduced-motion: reduce) {
  .bg-aurora::before { animation: none; }
}
```

---

## Noise Texture Overlay

```css
/* Subtle grain — adds organic texture over flat or gradient backgrounds */
.bg-noise {
  position: relative;
}

.bg-noise::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.04;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 128px 128px;
}
```

---

## Radial Spotlight (Cursor-Tracked)

```tsx
"use client";
import { useRef } from "react";

export function SpotlightCard({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);

  const handleMouseMove = (e: React.MouseEvent) => {
    const el = ref.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    el.style.setProperty("--mouse-x", `${x}%`);
    el.style.setProperty("--mouse-y", `${y}%`);
  };

  return (
    <div
      ref={ref}
      onMouseMove={handleMouseMove}
      className="relative overflow-hidden rounded-2xl border border-white/10 bg-gray-900 p-8"
      style={{
        background:
          "radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(99,102,241,0.15) 0%, transparent 60%), hsl(222 84% 5%)",
      }}
    >
      {children}
    </div>
  );
}
```

---

## Anti-Fake-Pass Checklist

- [ ] `prefers-reduced-motion` respected — animation disabled when user prefers no motion
- [ ] `will-change: transform` used on animated elements (compositor-only — no layout reflows)
- [ ] No arbitrary hex colors — all color values from design token system or HSL with CSS variables
- [ ] Background does not reduce text contrast below 4.5:1 (verify with contrast checker)
- [ ] `pointer-events: none` on decorative pseudo-elements (::before/::after)
- [ ] `overflow: hidden` on parent to prevent background bleed outside border-radius
- [ ] Noise SVG uses `stitchTiles='stitch'` to tile seamlessly without seams
- [ ] Aurora animation uses `transform` only — never `top/left/width/height` (no layout thrash)
