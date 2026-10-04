---
name: ascent-frontend-design
description: Create distinctive, on-brand frontend interfaces for Ascent Training. Use this skill when building landing pages, marketing sites, app UI, React components, or any visual artifact for Ascent. Combines the mountain/guide brand identity with topographic map aesthetics and emerald/charcoal color system. Generates production-grade code that is immediately recognizable as Ascent.
---

# Ascent Frontend Design Skill

This skill guides creation of distinctive, on-brand frontend interfaces for Ascent Training that are immediately recognizable and avoid generic "AI slop" aesthetics.

## Brand Context

**Ascent Training** is an intelligently guided training platform for endurance athletes. The core metaphor is **"You Climb. We Guide."** — athletes do the work and earn their achievements, while Ascent provides expert direction and support.

**Visual Identity**: Premium, focused, outdoor-inspired. Think: the feeling of early morning on a mountain trail, topographic maps in a high-end outdoor shop, the precision of Apple combined with the soul of Patagonia.

**NOT**: Generic fitness app, startup purple gradients, clinical dashboards, or motivational poster aesthetics.

---

## Signature Visual Elements

### 1. Topographic Map Backgrounds

**THE defining visual element of Ascent.** Use custom Mapbox topographic styling as hero backgrounds, section dividers, and atmospheric elements.

**Mapbox Style URL**: `mapbox://styles/jeremy-kalmus/cmj0mlugz007h01r87296hs3n`

**Implementation patterns**:

```css
/* Full-bleed hero background */
.hero-map-background {
  background-image: url('mapbox-static-api-url');
  background-size: cover;
  background-position: center;
  position: relative;
}

/* Gradient overlay for text legibility */
.hero-map-background::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(10, 10, 10, 0.7) 0%,
    rgba(10, 10, 10, 0.4) 50%,
    rgba(10, 10, 10, 0.9) 100%
  );
}

/* Subtle contour line pattern for sections */
.section-with-terrain {
  background: 
    url('/patterns/contour-lines.svg') repeat,
    linear-gradient(180deg, #171717 0%, #0a0a0a 100%);
  background-blend-mode: soft-light;
}
```

**When to use**:
- Landing page hero (full viewport)
- Section backgrounds (subtle, with overlay)
- Card accents (cropped detail views)
- Email headers and social media graphics

**Key principle**: The map should feel like looking at actual terrain, not a decorative pattern. Show real topography with elevation, ridgelines, and valleys visible.

### 2. Emerald + Charcoal Color System

**Primary Palette**:
```css
:root {
  /* Backgrounds - Charcoal scale */
  --bg-primary: #0a0a0a;      /* neutral-950 - deepest */
  --bg-secondary: #171717;    /* neutral-900 - cards */
  --bg-tertiary: #262626;     /* neutral-800 - elevated */
  --bg-interactive: #404040;  /* neutral-700 - inputs */

  /* Accent - Emerald scale */
  --accent-primary: #10b981;  /* emerald-500 - main */
  --accent-light: #34d399;    /* emerald-400 - hover */
  --accent-dark: #059669;     /* emerald-600 - pressed */
  --accent-subtle: #064e3b;   /* emerald-900 - backgrounds */
  --accent-glow: rgba(16, 185, 129, 0.2); /* glows, focus rings */

  /* Text */
  --text-primary: #fafafa;    /* neutral-50 */
  --text-secondary: #e5e5e5;  /* neutral-200 */
  --text-tertiary: #a3a3a3;   /* neutral-400 */
  --text-muted: #737373;      /* neutral-500 */

  /* Secondary accent */
  --accent-warm: #f59e0b;     /* amber-500 - warmth, energy */
}
```

**Color meaning**:
- **Emerald**: Growth, vitality, forward progress, nature, health
- **Charcoal**: Focus, sophistication, premium, nighttime training sessions
- **Amber**: Warmth, sunrise/sunset on peaks, energy, secondary emphasis

**NEVER use**: Purple gradients, bright blue CTAs, pure white backgrounds, or any "startup gradient" combinations.

### 3. Typography

**Font Stack** (Athletic Premium):
```css
:root {
  --font-display: 'Outfit', system-ui, sans-serif;        /* Geometric, confident, athletic */
  --font-body: 'Inter', system-ui, sans-serif;            /* Clean, highly legible, modern */
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;  /* Metrics and data */
}
```

**Typography rules**:
- Headlines: Bold (700-800), confident, generous letter-spacing (-0.02em) using Outfit
- Body: Clean, highly legible (400-600), comfortable reading using Inter
- Data/metrics: Monospace, lighter weight, emerald accent using JetBrains Mono
- Size contrast: Use dramatic scale jumps (3x+), not timid 1.5x

**Rationale**: Outfit brings athletic confidence and geometric precision. Inter is the industry standard for body text—highly legible and professional without feeling generic.

**Avoid**: Roboto, Open Sans, Lato, or overly playful fonts.

### 4. Motion & Animation

**Philosophy**: Purposeful motion that reinforces the "ascent" metaphor. Elements rise, reveal, and settle — never bounce or wiggle.

```css
/* Core timing */
:root {
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
}

/* Hero load-in: staggered rise */
.hero-content > * {
  opacity: 0;
  transform: translateY(20px);
  animation: rise-in 0.6s var(--ease-out) forwards;
}
.hero-content > *:nth-child(1) { animation-delay: 0.1s; }
.hero-content > *:nth-child(2) { animation-delay: 0.2s; }
.hero-content > *:nth-child(3) { animation-delay: 0.3s; }

@keyframes rise-in {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Emerald glow pulse for key elements */
@keyframes glow-pulse {
  0%, 100% { box-shadow: 0 0 20px var(--accent-glow); }
  50% { box-shadow: 0 0 40px var(--accent-glow); }
}

/* Subtle parallax on scroll */
.parallax-slow { transform: translateY(calc(var(--scroll) * 0.1)); }
.parallax-medium { transform: translateY(calc(var(--scroll) * 0.2)); }
```

**Motion vocabulary**:
- **Rise**: Elements enter from below (climbing metaphor)
- **Reveal**: Content fades in with subtle movement
- **Glow**: Emerald accent pulses to draw attention
- **Settle**: Elements ease into final position (reaching summit)

**Avoid**: Bounce, wiggle, spin, or any playful/childish motion.

### 5. Spatial Composition

**Layout principles**:
- **Generous whitespace**: Premium feel, breathing room
- **Asymmetric balance**: Not rigid grids, but intentional imbalance
- **Vertical rhythm**: Strong vertical flow (the ascent)
- **Full-bleed moments**: Map backgrounds, hero sections that fill viewport
- **Contained content**: Max-width 1200px for text, let visuals break out

```css
/* Content container */
.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 clamp(1rem, 5vw, 4rem);
}

/* Full-bleed break */
.full-bleed {
  width: 100vw;
  margin-left: calc(-50vw + 50%);
}

/* Vertical spacing scale */
.section { padding: clamp(4rem, 10vh, 8rem) 0; }
.section-tight { padding: clamp(2rem, 5vh, 4rem) 0; }
```

---

## Component Patterns

### Primary Button (CTA)

```css
.btn-primary {
  background: var(--accent-primary);
  color: var(--bg-primary);
  font-weight: 600;
  padding: 1rem 2rem;
  border-radius: 12px;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  transition: all var(--duration-normal) var(--ease-out);
  box-shadow: 0 0 20px var(--accent-glow);
}

.btn-primary:hover {
  background: var(--accent-light);
  transform: translateY(-2px);
  box-shadow: 0 0 30px var(--accent-glow);
}

.btn-primary:active {
  background: var(--accent-dark);
  transform: translateY(0);
}
```

### Card Component

```css
.card {
  background: var(--bg-secondary);
  border: 1px solid #262626;
  border-radius: 16px;
  padding: 1.5rem;
  transition: all var(--duration-normal) var(--ease-out);
}

.card:hover {
  border-color: var(--accent-primary);
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Card with emerald accent bar */
.card-accent {
  border-left: 4px solid var(--accent-primary);
}
```

### Metric Display

```css
.metric {
  font-family: var(--font-mono);
}

.metric-value {
  font-size: 3rem;
  font-weight: 300;
  color: var(--accent-primary);
  line-height: 1;
}

.metric-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-tertiary);
  margin-top: 0.5rem;
}
```

---

## Landing Page Structure

For the Ascent landing page specifically:

### Hero Section
- Full-viewport topographic map background
- Gradient overlay for text legibility
- Bold headline: "You Climb. We Guide."
- Subhead: One sentence value prop
- Single CTA: "Start Your Ascent" or "Join the Beta"
- Staggered rise animation on load

### Problem/Solution Section
- Dark background (#0a0a0a)
- Split layout: problem (left) vs solution (right)
- Use amber accent for problem, emerald for solution
- Subtle contour line pattern in background

### How It Works
- Three steps with mountain metaphor
- Basecamp → Ascent → Summit visual
- Icons or illustrations that feel outdoor/trail-inspired
- NOT generic icons or illustrations

### Features
- Card grid with emerald accent bars
- Each card: Icon + Title + Brief description
- Hover reveals more detail
- Consider subtle map detail as card background

### Social Proof
- Testimonials from real athletes (when available)
- Simple quotes, not elaborate carousel
- Athlete photo + name + discipline

### CTA Section
- Return to topographic map background
- Simple, bold call to action
- Email capture for waitlist

### Footer
- Minimal, dark
- Essential links only
- Small Ascent wordmark

---

## What Makes Ascent Frontend Distinctive

1. **Topographic maps** — No other training app uses this. It's immediately recognizable.

2. **Emerald + Charcoal** — Not the purple/blue of most SaaS, not the orange/black of fitness apps.

3. **Mountain/outdoor aesthetic** — Premium outdoor brand feel, not generic tech startup.

4. **Vertical motion** — Everything rises, reinforcing the "ascent" metaphor.

5. **Premium restraint** — Apple-like polish with outdoor soul. Not cluttered, not clinical.

---

## Anti-Patterns (NEVER Do These)

❌ Purple gradients on white backgrounds
❌ Inter, Roboto, or system fonts
❌ Generic hero images of runners
❌ Bright blue CTAs
❌ Bouncy/playful animations
❌ Stock photography of athletes
❌ Gradient buttons with multiple colors
❌ Busy patterns or textures
❌ Cookie-cutter SaaS layouts
❌ "Get Started Free" in blue button

---

## Implementation Notes

### For React/Next.js
- Use Tailwind CSS with custom config matching color system
- Import Bricolage Grotesque and Source Sans 3 from Google Fonts
- Use Framer Motion for animations
- Mapbox GL JS for interactive map elements

### For Static HTML
- CSS custom properties for theming
- CSS animations (no JS required for core effects)
- Static Mapbox images for performance

### For Artifacts/Prototypes
- Can use inline styles matching color system
- Include Google Fonts link in head
- Use placeholder for map images, describe the topographic effect

---

## Quick Reference

**Brand tagline**: "You Climb. We Guide."
**Primary color**: #10b981 (emerald-500)
**Background**: #0a0a0a (charcoal/neutral-950)
**Font display**: Bricolage Grotesque
**Font body**: Source Sans 3
**Signature element**: Topographic map backgrounds
**Motion**: Rise, reveal, glow — never bounce
**Vibe**: Patagonia meets Apple meets midnight training sessions
