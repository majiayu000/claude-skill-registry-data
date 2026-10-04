---
name: kinetic
description: Motion-first, animated transitions, dynamic typography, scroll-driven.
---
# Kinetic
## Mission
Design interfaces where motion is not decoration but the primary storytelling device — every scroll, hover, and state change drives engagement through purposeful, choreographed animation.
## Brand
### 🎨 Colors
- `#0d0d0d` — Deep black (canvas)
- `#ffffff` — Pure white (text, accents)
- `#ff3366` — Electric pink (primary motion accent)
- `#00d4ff` — Cyan (secondary motion)
- `#ffcc00` — Amber (highlight)
- `#1a1a2e` — Dark navy (alt background)
### 🔤 Typography
- **Heading:** Syncopate (geometric, wide) or Orbitron — fonts that look good in motion
- **Body:** Inter or DM Sans (clean, neutral, readable in motion)
- **Scale:** xs: 0.75rem, sm: 0.875rem, base: 1rem, lg: 1.125rem, xl: 1.25rem, 2xl: 1.5rem, 3xl: 3rem (large for impact)
### 📐 Spacing
- Flexible spacing that shifts with animation: 1rem–4rem gaps
- Section padding: 6rem vertical (room to animate), 2rem horizontal
- Card gaps: 2rem with animated offset on scroll
- Border radius: 0–8px (sharp enough for crisp motion edges)
### 🧩 Components
- **Buttons:** Magnetic hover effect (button follows cursor slightly), animated gradient border, scale pulse on click
- **Cards:** Reveal on scroll with staggered fade-up and slight rotation, parallax depth effect on hover
- **Nav:** Appears/disappears on scroll direction with smooth slide, background blur transitions
- **Hero:** Split-text animation on load (letters animate in sequence), scroll-driven parallax backgrounds, cursor-reactive elements
- **Footer:** Reveal animation on scroll into view, subtle continuous marquee or particle effect
### ♿ Accessibillity
- All animations respect prefers-reduced-motion: replace with instant transitions
- No animation that triggers vestibular disorders: avoid large parallax, excessive scaling, spinning
- Focus states animate smoothly (not abruptly) to help users track focus movement
- Scroll-driven animations must not interfere with keyboard navigation or screen reader focus order
- Minimum animation duration: 200ms, maximum: 600ms for UI transitions
### ✍️ Writing Tone
Dynamic and punchy. Verb-driven headlines. Short, rhythmic sentences. Words should carry the same energy as the motion. Sentence case labels.
## Do / Don't
### ✅ Do
- Choreograph entrance animations in sequence — stagger, don't flood
- Use scroll-driven animations (CSS scroll-timeline or Intersection Observer) for narrative flow
- Keep animations between 200–500ms for UI; longer for narrative/hero moments
- Test all animations at 60fps on mid-range mobile devices
- Provide instant-fallback static states when motion is disabled
### ❌ Don't
- Animate everything — motion is a signal; overuse dilutes its impact
- Use infinite looping animations except for deliberate loading states
- Animate layout-triggering properties (width, height, top, left) — use transform and opacity
- Start animation before the element is in viewport
- Ship without prefers-reduced-motion testing
## Quality Gates
- [ ] All animations run at 60fps on a mid-range mobile device (Moto G4 equivalent)
- [ ] prefers-reduced-motion disables all non-essential animation
- [ ] No layout-triggering properties animated (only transform + opacity)
- [ ] Entrance animations are staggered, not simultaneous — test with DevTools timeline
- [ ] Scroll-driven animations work in both scroll directions (up and down)
- [ ] Focus transitions are smooth and never teleport