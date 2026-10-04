---
name: manim
description: Python library for creating precise mathematical animations programmatically — the engine behind 3Blue1Brown's YouTube videos. Renders LaTeX equations, geometric proofs, graphs, and data visualisations as smooth MP4/GIF animations. Use when you need publication-quality math or technical animations generated from code rather than a design tool.
---

# Manim — Mathematical Animation Engine (3Blue1Brown)

The animation library Grant Sanderson (3Blue1Brown) built and uses for his YouTube channel, now MIT-licensed and community-maintained.

## What it replaces

Manually keyframing math visualisations in After Effects, Keynote, or PowerPoint — Manim generates them programmatically from Python code, so they are version-controlled, reproducible, and scriptable.

## Key capabilities

- **LaTeX rendering**: Typeset equations and have them animate — morph, highlight, move
- **Geometric primitives**: Circles, lines, arrows, polygons with precise coordinate control
- **Graphs & charts**: Function plots, bar charts, number lines with animation transitions
- **Camera control**: Zoom, pan, 3D rotation (with `ThreeDScene`)
- **Text animation**: Write-on effects, color transforms, morphing between expressions
- **Scene composition**: Multi-scene videos with consistent styling

## When to reach for it

- Educational content explaining algorithms, proofs, or data structures with animated visuals
- Marketing / explainer videos for technical products
- Research presentations that need publication-quality figure animations
- Generating animated diagrams for documentation

## Stack

Python 3.8+ · Cairo (2D rendering) · OpenGL (3D) · LaTeX (equation rendering) · FFmpeg (video encoding)

## Clone

```bash
git clone https://github.com/3b1b/manim
# or community fork (more active maintenance):
git clone https://github.com/ManimCommunity/manim
```

## Quickstart

```bash
pip install manim
manim -pql your_scene.py YourSceneName
```

Flags: `-p` = preview, `-q` = quality (`l`ow/`m`edium/`h`igh/`k` 4K), `-l` = low resolution for fast iteration.

## Example

```python
from manim import *

class Pythagorean(Scene):
    def construct(self):
        eq = MathTex(r"a^2 + b^2 = c^2")
        self.play(Write(eq))
        self.wait(2)
```
