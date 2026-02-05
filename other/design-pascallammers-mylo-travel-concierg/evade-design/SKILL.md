---
name: evade-design
description: Use when working on EVADE game UI, creating screens, styling components, or making visual decisions. Apply for any React Native code touching colors, typography, layouts, animations, or visual elements.
---

# EVADE Design System

## Overview

80s Synthwave/Neon aesthetic with Dynamic Hybrid approach: crystal-clear UI layered over rich atmospheric backgrounds. Apple Award-worthy polish.

## Color Palette

```typescript
const COLORS = {
  // Backgrounds
  backgroundDeep: '#0a0a12',      // Deep space black (primary)
  backgroundPanel: '#1a1a2e',     // Dark purple-black (panels/modals)

  // Neon Accents
  neonCyan: '#00f5ff',            // Player, highlights, primary actions
  neonMagenta: '#ff2a6d',         // Enemies, danger, warnings
  neonPurple: '#9d4edd',          // UI accents, secondary actions
  chromeGold: '#ffd700',          // Titles, achievements, rewards
  hotPink: '#ff00aa',             // Secondary accents

  // Supporting
  gridLines: '#4a1a6b',           // Subtle purple grid
  textPrimary: '#ffffff',
  textMuted: '#888888',

  // Gradients
  sunBands: ['#ff2a6d', '#ffd700', '#ff6b35'], // Horizon sun
}
```

## Visual Motifs (Layered)

| Layer | Element | Animation |
|-------|---------|-----------|
| 1 | Deep black + star particles | Slow parallax drift |
| 2 | Perspective grid floor | Subtle forward movement |
| 3 | Horizon sun (banded) | Position varies by screen context |
| 4 | Geometric halos (hexagons/circles) | Slow counter-rotation |
| 5 | UI elements | Glow pulses, micro-interactions |

**Per-Screen Sun Position:**
- Main Menu: 60% up (welcoming)
- High Scores: Higher (triumphant)
- Shop: Lower (sunset/relaxed)
- Play: Hidden (no distraction)
- Game Over: Below horizon (defeat)

## Typography

| Use | Style | Properties |
|-----|-------|------------|
| Game title "EVADE" | Chrome gradient | Gold-white-gold, cyan outer glow, 72px bold |
| Screen titles | Chrome | Smaller chrome, consistent glow |
| Buttons | Geometric sans | All caps, wide letter-spacing, 20px bold |
| Body text | Geometric sans | Clean, high contrast white |
| Labels/muted | Geometric sans | Muted gray, smaller |

## Button Styles

**Primary (Play, main actions):**
```typescript
{
  background: 'transparent',
  borderWidth: 1,
  borderColor: COLORS.neonCyan,
  shadowColor: COLORS.neonCyan,
  shadowRadius: 8,
}
```

**Secondary (Settings, back):**
```typescript
{
  background: 'transparent',
  borderWidth: 1,
  borderColor: COLORS.neonPurple,
}
```

**Glass-morphic panels:**
```typescript
{
  backgroundColor: 'rgba(26, 26, 46, 0.8)',
  backdropFilter: 'blur(10px)', // Web only, use opacity on native
  borderRadius: 12,
  borderWidth: 1,
  borderColor: 'rgba(157, 78, 221, 0.3)',
}
```

## Micro-interactions

| Element | Interaction | Effect |
|---------|-------------|--------|
| Button touch | Press | Scale 0.98, border flash white |
| Button release | Release | Ripple glow outward |
| Toggle switch | State change | Overshoot spring, glow pulse |
| Score change | Increment | Roll animation, gold flash |
| Item collect | Pickup | Bounce + sparkle particles |

## Screen Transitions

| Transition | Effect |
|------------|--------|
| Menu → Play | Grid rushes forward, sun dips, UI fades |
| Play → Game Over | White flash, chromatic aberration, blur in |
| Any → Modal | Dim background 40%, modal scales up |
| Horizontal nav | Parallax slide (background slower than UI) |

## Game Entities

**Player:**
- 3-layer glow: inner white, mid color, outer soft
- Shape/color from cosmetics
- Shield: pulsing cyan hexagonal barrier

**Enemies:**
- Neon edge glow (not solid fill)
- Shape = speed tier (circle/square/triangle)
- Color fades red → yellow near despawn

**Boosters:**
- Green octagon with inner glow pulse
- Clear icon inside (plus/shield/x3)
- Sparkle particles around edges

## Modal Structure

```
┌─────────────────────────────────────┐
│ [Hexagonal frame border with glow] │
│                                     │
│         TITLE (chrome)              │
│                                     │
│         Content area                │
│                                     │
│   ┌─────────────────────────────┐   │
│   │     PRIMARY ACTION          │   │  ← Cyan border
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │     SECONDARY ACTION        │   │  ← Purple border
│   └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

- Game Over modal: Magenta border (danger)
- Continue modal: Cyan border (opportunity)
- Shop/Settings: Purple border (neutral)

## Quick Reference

| Need | Use |
|------|-----|
| Primary action | Cyan border button |
| Secondary action | Purple border button |
| Danger/warning | Magenta color |
| Success/reward | Chrome gold |
| Player highlight | Neon cyan |
| Panel background | Glass-morphic dark purple |
| Section headers | Uppercase, letter-spaced, purple + line |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Solid color buttons | Use transparent + border + glow |
| White backgrounds | Always dark (#0a0a12 or #1a1a2e) |
| System fonts | Use geometric sans with letter-spacing |
| Static elements | Add subtle glow pulse or drift |
| Competing visual layers | Dim background during gameplay |
| Harsh edges | Add glow/blur for neon effect |
