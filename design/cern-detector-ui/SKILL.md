---
name: CERN Detector UI
description: Design system for the CERN Particle Detector aesthetic. Use when building UI components, styling elements, or implementing the detector workstation interface.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# CERN Particle Detector UI Design System

This skill provides the complete design system for the Composition app's "CERN Particle Detector" aesthetic - inspired by CERN control rooms, ATLAS/CMS detector visualizations, and particle physics instrumentation.

## When to Use This Skill

- Building new UI components
- Styling existing components
- Implementing layout patterns
- Creating detector-style interfaces
- Building 3D workstation controls

## Design Philosophy

**NOT a generic terminal.** This is a research instrument interface:
- **Circular/radial elements** - detector cross-sections, not rectangular cards
- **Wire chamber aesthetic** - fine grids, track visualizations
- **Particle color language** - each color has scientific meaning
- **Data-dense but elegant** - like real physics control software

## Color Palette

### Void (Backgrounds)
| Variable | Hex | Usage |
|----------|-----|-------|
| `--void-deep` | `#030305` | Page background |
| `--void-primary` | `#060609` | Main background |
| `--void-secondary` | `#0a0a0f` | Panel backgrounds |
| `--void-tertiary` | `#0f0f16` | Elevated surfaces |
| `--void-elevated` | `#14141e` | Cards, modals |

### Wire Chamber
| Variable | Hex | Usage |
|----------|-----|-------|
| `--wire-dim` | `#1a1a2e` | Subtle borders, grids |
| `--wire-medium` | `#252540` | Scrollbars, dividers |
| `--wire-bright` | `#3d3d66` | Hover states, accents |

### Particle Colors
| Variable | Hex | Meaning |
|----------|-----|---------|
| `--particle-gold` | `#ffd700` | Verified, stable, heavy particles |
| `--particle-cyan` | `#00d4ff` | Active tracking, live data, leptons |
| `--particle-magenta` | `#ff2d7e` | Collisions, processing, bosons |
| `--particle-green` | `#39ff14` | Element traces, hadrons |
| `--particle-orange` | `#ff8c00` | Warnings, estimations, jets |

### Node Types (Composition Hierarchy)
| Variable | Hex | Type |
|----------|-----|------|
| `--node-product` | `#ffffff` | Product nodes |
| `--node-component` | `--particle-cyan` | Component nodes |
| `--node-material` | `--particle-orange` | Material nodes |
| `--node-chemical` | `--particle-green` | Chemical nodes |
| `--node-element` | `--particle-gold` | Element nodes |

### Text
| Variable | Hex | Usage |
|----------|-----|-------|
| `--text-bright` | `#f0f0f8` | Headings, emphasis |
| `--text-primary` | `#d0d0e0` | Body text |
| `--text-secondary` | `#8080a0` | Labels, muted |
| `--text-tertiary` | `#505070` | Disabled, hints |
| `--text-data` | `--particle-cyan` | Data values |
| `--text-highlight` | `--particle-gold` | Verified data |

## Typography

```css
--font-display: 'DM Sans', system-ui, sans-serif;
--font-mono: 'Space Mono', 'Overpass Mono', monospace;
--font-data: 'Overpass Mono', 'Space Mono', monospace;
```

### Usage Classes
```tsx
// Display text
className="font-display text-lg font-semibold text-[var(--text-bright)]"

// Mono labels
className="font-mono text-xs text-[var(--text-secondary)] uppercase tracking-wider"

// Data readouts
className="font-data text-sm text-[var(--text-data)] tabular-nums"

// Detector label style
className="label-detector" // 10px, uppercase, 0.15em tracking
```

## Component Patterns

### Detector Panel
```tsx
<div className="detector-panel">
  <div className="detector-panel-header">
    <span className="label-detector">Panel Title</span>
  </div>
  <div className="detector-panel-content">
    {children}
  </div>
</div>
```

### Detector Input
```tsx
<input
  className="detector-input"
  placeholder="Enter value..."
/>
```

### Detector Buttons
```tsx
// Standard
<button className="btn-detector">Action</button>

// Primary (cyan gradient)
<button className="btn-detector btn-detector-primary">Analyze</button>

// Gold accent
<button className="btn-detector btn-detector-gold">Verify</button>
```

### Status Indicator
```tsx
<div className="status-indicator status-active" />  // Cyan with pulse
<div className="status-indicator status-verified" /> // Gold
<div className="status-indicator status-warning" />  // Orange
<div className="status-indicator status-error" />    // Magenta
```

### Specimen Tag
```tsx
<button className="specimen-tag">iPhone 15 Pro</button>
```
Has automatic cyan dot before text, hover glow effect.

### Readout Display
```tsx
<div className="flex flex-col gap-1">
  <span className="label-detector">Label</span>
  <div className="font-data text-lg tabular-nums">
    <span className="particle-cyan">42.5</span>
    <span className="text-[var(--text-tertiary)] text-sm ml-1">units</span>
  </div>
</div>
```

### Wire Frame Container
```tsx
<div className="wire-frame p-4">
  {/* Has corner brackets automatically */}
  {children}
</div>
```

## Layout Patterns

### Detector Background
```tsx
<div className="detector-bg min-h-screen">
  {/* Radial rings + grid pattern + center glow */}
</div>
```

### App Shell
```
┌────────────────────────────────────────────────────────────┐
│ ◉ STATUS │ TITLE                              │ SESSION    │
├──────────┼────────────────────────────────────┼────────────┤
│ SIDEBAR  │         MAIN CONTENT               │ READOUTS   │
│          │                                    │            │
│          │                                    │            │
├──────────┴────────────────────────────────────┴────────────┤
│ BOTTOM PANEL (Tabs: Hierarchy | Chat)                      │
└────────────────────────────────────────────────────────────┘
```

### Corner Brackets (Decorative)
```tsx
<div className="fixed top-4 left-4 w-8 h-8 border-l-2 border-t-2 border-[var(--wire-dim)]" />
<div className="fixed top-4 right-4 w-8 h-8 border-r-2 border-t-2 border-[var(--wire-dim)]" />
<div className="fixed bottom-4 left-4 w-8 h-8 border-l-2 border-b-2 border-[var(--wire-dim)]" />
<div className="fixed bottom-4 right-4 w-8 h-8 border-r-2 border-b-2 border-[var(--wire-dim)]" />
```

## Animation Classes

```css
.animate-pulse-ring      /* Expanding ring for status indicators */
.animate-detector-scan   /* 360° rotation for scanning effects */
.animate-data-stream     /* Horizontal data flow */
.animate-glow-pulse      /* Opacity pulse for active elements */
.animate-fade-in         /* 300ms fade in */
.animate-slide-up        /* 300ms slide up with fade */
.animate-slide-in-right  /* 300ms slide from right */

/* Stagger delays */
.stagger-1 through .stagger-5  /* 50ms increments */
```

## Transitions

```css
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
--ease-in-out-expo: cubic-bezier(0.87, 0, 0.13, 1);
--duration-instant: 50ms;
--duration-fast: 150ms;
--duration-normal: 300ms;
--duration-slow: 500ms;
```

## Motion Principles

1. **Quick responses** (150ms) for hover/click feedback
2. **Expo easing** for smooth, physics-like movement
3. **Pulse animations** for live status indicators
4. **Staggered reveals** for list items
5. **Spring physics** for 3D camera movements

## Accessibility

- Maintain WCAG 2.1 AA contrast ratios (particle colors are designed for this)
- All interactive elements keyboard accessible
- Focus indicators: `outline: 1px solid var(--particle-cyan); outline-offset: 2px;`
- Status changes announced to screen readers
- Reduced motion: Respect `prefers-reduced-motion`

## SVG Patterns

### Detector Rings
```tsx
<svg viewBox="0 0 400 400">
  {[160, 140, 120, 100, 80].map((r, i) => (
    <circle
      key={i}
      cx="200" cy="200" r={r}
      stroke="var(--wire-dim)"
      strokeWidth="1"
      fill="none"
      opacity={0.5 - i * 0.08}
    />
  ))}
</svg>
```

### Sector Lines
```tsx
{Array.from({ length: 12 }).map((_, i) => {
  const angle = (i * 30 * Math.PI) / 180;
  return (
    <line
      x1={200 + 60 * Math.cos(angle)}
      y1={200 + 60 * Math.sin(angle)}
      x2={200 + 165 * Math.cos(angle)}
      y2={200 + 165 * Math.sin(angle)}
      stroke="var(--wire-dim)"
      strokeWidth="1"
      opacity="0.3"
    />
  );
})}
```
