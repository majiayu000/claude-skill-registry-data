---
name: frontend-design
description: Create high-quality, distinctive web interfaces that avoid generic AI aesthetics. Use when building web components, pages, dashboards, landing pages, or applications. Triggers on "build UI", "create page", "design frontend", "make it look good", "dashboard design", or any web interface creation task.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Frontend Design

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Create production-grade web interfaces with intentional, distinctive aesthetics.

## Core Philosophy

**Avoid generic AI design.** Every interface should have a clear aesthetic point-of-view. Generic means forgettable—be bold.

## Before Coding: Design Thinking

### 1. Clarify Purpose
- What is this interface for?
- Who uses it?
- What emotion should it evoke?

### 2. Choose Aesthetic Direction
Pick a BOLD direction (not "clean and modern"):

| Direction | Characteristics |
|-----------|-----------------|
| **Brutalist** | Raw, unpolished, intentionally rough |
| **Minimalist** | Extreme restraint, negative space, few elements |
| **Maximalist** | Rich, layered, abundant detail |
| **Retro-Futuristic** | Blend of vintage and sci-fi |
| **Organic** | Flowing shapes, natural colors, soft edges |
| **Corporate Refined** | Precise, professional, subtle luxury |
| **Playful** | Bright colors, rounded shapes, micro-interactions |
| **Dark Mode Premium** | Deep blacks, accent glows, high contrast |

### 3. Identify Constraints
- Framework (Vue, React, Blade, plain HTML)
- CSS approach (Tailwind, custom, component library)
- Performance requirements
- Accessibility needs

## Aesthetic Execution

### Typography
**Never use:** Arial, Helvetica, Times New Roman, default system fonts, Inter (overused)

**Do:**
- Choose distinctive, characterful fonts
- Pair fonts deliberately (display + body)
- Use dramatic size contrast
- Consider variable fonts for expressiveness

```css
/* Example: Bold pairing */
--font-display: 'Playfair Display', serif;
--font-body: 'Source Sans Pro', sans-serif;

h1 { font-size: 4rem; letter-spacing: -0.02em; }
```

### Color & Theme
**Avoid:** Purple-to-blue gradients (AI cliche), rainbow gradients, gray-on-gray

**Do:**
- Commit to a cohesive palette
- Use CSS variables for theming
- Pick ONE dominant color, sharp accents
- Consider dark mode from the start

```css
:root {
  --color-primary: #1a1a2e;
  --color-accent: #e94560;
  --color-surface: #16213e;
  --color-text: #eaeaea;
}
```

### Motion & Animation
**Avoid:** Animations everywhere, slow fades, gratuitous bounces

**Do:**
- Prioritize high-impact moments
- Use staggered reveals (`animation-delay`)
- Scroll-triggered animations for storytelling
- Micro-interactions on key actions

```css
/* Staggered entrance */
.card {
  animation: fadeUp 0.4s ease-out forwards;
  opacity: 0;
}
.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }
```

### Spatial Composition
**Avoid:** Predictable grids, everything centered, symmetrical layouts

**Do:**
- Embrace asymmetry
- Use overlap and layering
- Break the grid intentionally
- Strategic negative space

### Visual Details
**Add depth with:**
- Subtle gradients
- Noise textures
- Custom shadows (not default box-shadow)
- Border treatments
- Background patterns

```css
/* Atmospheric shadow */
.card {
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 20px 25px -5px rgba(0, 0, 0, 0.15),
    0 0 50px -12px var(--color-accent);
}

/* Subtle noise texture */
.surface::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,...") repeat;
  opacity: 0.03;
  pointer-events: none;
}
```

## Framework-Specific Guidance

### Tailwind CSS
See [references/tailwind.md](references/tailwind.md) for patterns

### Vue/Nuxt
See [references/vue.md](references/vue.md) for component patterns

### React
See [references/react.md](references/react.md) for component patterns

### Laravel Blade
See [references/blade.md](references/blade.md) for template patterns

## Anti-Patterns Checklist

Before finalizing, verify you avoided:

- [ ] Generic font choices (Inter, Arial, system-ui only)
- [ ] Purple-blue gradients
- [ ] Everything centered
- [ ] Default shadows
- [ ] Animations on everything
- [ ] Gray-on-gray color scheme
- [ ] Cookie-cutter card layouts
- [ ] Stock photo aesthetics

## Output Requirements

Deliver:
1. **Complete, functional code** (not pseudo-code)
2. **Responsive design** (mobile-first or desktop-first, state which)
3. **Cohesive aesthetic** matching chosen direction
4. **Performance-conscious** (optimize images, lazy load)
5. **Accessible** (semantic HTML, ARIA where needed)

## Process

1. **Ask** about purpose, audience, constraints if unclear
2. **Propose** aesthetic direction with rationale
3. **Build** with production-grade code
4. **Refine** based on feedback
5. **Deliver** complete, tested implementation

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
