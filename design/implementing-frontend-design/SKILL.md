---
name: implementing-frontend-design
description: Used by the Developer agent during Phase 8 (Implement) when building web components, pages, or UI features. Provides strict aesthetic guidelines to create distinctive, production-grade frontend interfaces that avoid generic 'AI slop' aesthetics.
---

# Implementing Frontend Design (Phase 8: Implement)

## Overview

As the **Developer** agent in Phase 8, your role is to execute the architecture plan and implement real working code with exceptional attention to aesthetic details and creative choices.

This skill guides the creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. You have **full Edit/Write/Bash access**.

## Context Gathering Protocol

Before doing any design work, you MUST have confirmed design context:
- **Target audience**: Who uses this product and in what context?
- **Use cases**: What jobs are they trying to get done?
- **Brand personality/tone**: How should the interface feel?

Check the Architecture Plan from Phase 7 (locate it within .jonggrang/.output/features/ using your search tools) or AGENTS.md for this context. If not present, infer it from existing codebase files (like DESIGN.md or a global theme file).

## Design Direction

Commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work—the key is intentionality, not intensity.

## Frontend Aesthetics Guidelines (Flattened References)

### 1. Typography
Choose fonts that are beautiful, unique, and interesting. Pair a distinctive display font with a refined body font.
- **DO**: Use a modular type scale with fluid sizing (clamp).
- **DO**: Vary font weights and sizes to create clear visual hierarchy.
- **DON'T**: Use overused fonts (Inter, Roboto, Arial, Open Sans, system defaults).
- **DON'T**: Put large icons with rounded corners above every heading.

### 2. Color & Theme
Commit to a cohesive palette. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **DO**: Use modern CSS color functions (oklch, color-mix, light-dark) for perceptually uniform, maintainable palettes.
- **DO**: Tint your neutrals toward your brand hue.
- **DON'T**: Use gray text on colored backgrounds—it looks washed out; use a shade of the background color instead.
- **DON'T**: Use pure black (#000) or pure white (#fff)—always tint.
- **DON'T**: Use the AI color palette: cyan-on-dark, purple-to-blue gradients, neon accents on dark backgrounds.
- **DON'T**: Use gradient text for "impact".

### 3. Layout & Space
Create visual rhythm through varied spacing—not the same padding everywhere. Embrace asymmetry.
- **DO**: Create visual rhythm through varied spacing—tight groupings, generous separations.
- **DO**: Use fluid spacing with clamp() that breathes on larger screens.
- **DO**: Use asymmetry and unexpected compositions; break the grid intentionally for emphasis.
- **DON'T**: Wrap everything in cards—not everything needs a container.
- **DON'T**: Use identical card grids—same-sized cards with icon + heading + text, repeated endlessly.
- **DON'T**: Use the hero metric layout template—big number, small label, supporting stats, gradient accent.
- **DON'T**: Center everything—left-aligned text with asymmetric layouts feels more designed.

### 4. Visual Details & Polish
- **DO**: Use intentional, purposeful decorative elements that reinforce brand.
- **DON'T**: Use glassmorphism everywhere.
- **DON'T**: Use rounded elements with thick colored border on one side.
- **DON'T**: Use sparklines as decoration.
- **DON'T**: Use rounded rectangles with generic drop shadows.
- **DON'T**: Use modals unless there's truly no better alternative.

### 5. Motion & Interaction
Focus on high-impact moments. Make interactions feel fast. Use optimistic UI.
- **DO**: Use motion to convey state changes (entrances, exits, feedback).
- **DO**: Use exponential easing (ease-out-quart/quint/expo) for natural deceleration.
- **DO**: Use progressive disclosure (start simple, reveal sophistication through interaction).
- **DO**: Design empty states that teach the interface.
- **DON'T**: Animate layout properties (width, height, padding, margin)—use transform and opacity only.
- **DON'T**: Use bounce or elastic easing.
- **DON'T**: Make every button primary.

### 6. Responsive & UX Writing
- **DO**: Use container queries (@container) for component-level responsiveness.
- **DO**: Make every word earn its place.
- **DON'T**: Hide critical functionality on mobile—adapt the interface.
- **DON'T**: Repeat information users can already see.

## The AI Slop Test

**Critical quality check**: If you showed this interface to someone and said "AI made this," would they believe you immediately? If yes, that's the problem. Review the DON'T guidelines above—they are the fingerprints of AI-generated work.

## Implementation Principles

Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details.

Interpret creatively and make unexpected choices that feel genuinely designed for the context.

## Completion

Once the implementation is complete and matches the aesthetic standards, use the Bash tool to run typechecks, linting, and tests to verify.

Output the following completion signal exactly on its own line:
`IMPLEMENTATION_COMPLETE`
