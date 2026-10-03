---
name: define-visual-style
description: "Use when defining the visual style for a game — dimension, perspective, rendering, and color palette through a guided interview."
---

## 1. Output Artifact

- **Target**: `{TARGET_FOLDER}/docs/visual_style.md`
- **Maps four dimensions**: Dimension, Perspective, Rendering, Palette → technical specification.

## 2. Four-Dimension Interview

Conduct full interview with user BEFORE generating spec. Use `question` tool one dimension at a time.

| Step | Dimension | Options |
|------|-----------|---------|
| 1 | Dimension | 2D / 3D / 2.5D |
| 2 | Perspective | Top-down / Side-view / First-person / Third-person / Isometric |
| 3 | Rendering | Pixel Art / Low-poly / Realistic / Cel-shaded / Hand-drawn |
| 4 | Palette | Warm / Cool / Monochrome / Vibrant / Muted (or custom) |

**Ask ONE → STOP. After all four, present summary for confirmation → STOP → generate spec.**

## 3. When to Use

- **Triggers**: `define visual style`, `art direction`, `visual style`, `art style`, `color palette`.
- **When to use**: Starting a new project or when `visual_style.md` does not yet exist. For asset budgeting/bundle strategy, use core audit skills instead.

## 4. Quick Reference

**Output**: `{TARGET_FOLDER}/docs/visual_style.md`. **Tool**: `question` (one per turn).

Four dimensions:
1. Dimension — 2D / 3D / 2.5D
2. Perspective — Top-down / Side-view / First-person / Third-person / Isometric
3. Rendering — Pixel Art / Low-poly / Realistic / Cel-shaded / Hand-drawn
4. Palette — Warm / Cool / Monochrome / Vibrant / Muted (or custom)

Ask one dimension at a time, then present summary for confirmation before generating spec.

## 5. Intercepts

- **Style vs Gameplay Conflict**: If style contradicts core loop → suggest adjustment.
- **Vague Descriptor**: If user provides non-technical terms → ask for concrete options.

## 5. Red Flags

- Asking multiple questions in one turn · Proceeding with contradictions · Accepting vague terms · Skipping summary confirmation

## 6. Execution Command

`/define-visual-style`
