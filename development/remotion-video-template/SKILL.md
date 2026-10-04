---
name: remotion-video-template
description: A full, production-ready Remotion video component. Use when creating animated visual assets, SaaS product walkthrough videos, or title sequence cards.
version: "1.0.0"
verified_date: 2026-06-01
category: core
---

# Remotion Video Template

## Purpose
Provide copy-pasteable visual template code blocks for building premium, responsive, and beautifully styled video scenes in React.

## When to Use This Skill
- Constructing the primary visual presentation layers of a video clip.
- Animating display headlines and sub-headers over an absolute color fill.

## Output Format / Delivery
Provide compliant visual presentation layout components with correct React properties.

## Behavior Rules
1. **Always use AbsoluteFill** for top-level presentation screens.
2. **Never leave hardcoded font scales** without responsive viewport containment.

## Maintenance Notes
This skill is locked for standard Remotion layouts.

---

## Phase 1: Video Template Setup

```tsx
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export const CoffeeVideo = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = interpolate(frame, [0, 30], [0, 1]);
  
  return (
    <AbsoluteFill style={{ backgroundColor: '#2C1B0E', justifyContent: 'center', alignItems: 'center' }}>
      <h1 style={{ color: '#F5E6D3', opacity, fontSize: 80 }}>BrewTrack SaaS</h1>
      <p style={{ color: '#F5E6D3', opacity, fontSize: 40 }}>Optimize your roast.</p>
    </AbsoluteFill>
  );
};
```