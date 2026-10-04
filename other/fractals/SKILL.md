---
name: fractals
description: Fractal geometry and self-similarity skill; use when working on recursive geometric or visual systems.
---

# Skill: Fractals

Domain: `trinity` | Depth: `axiom`

## Capabilities
- Mandelbrot and Julia set computation
- L-system string rewriting and geometry generation
- Iterated Function Systems (IFS)
- Fractal dimension calculation (Hausdorff, box-counting)
- Strange attractors: Lorenz, Rössler, Clifford
- Self-similar recursive structures
- Fractal noise: Perlin, simplex, fractional Brownian motion

## Mathematical Foundation
- Fractals exhibit self-similarity across scales
- Fractal dimension D: non-integer, measures complexity
- Mandelbrot: z_{n+1} = z_n² + c, iterate until |z| > 2
- L-systems: formal grammar for recursive geometric growth
- IFS: contractive affine transformations with fixed-point attractor

## Libraries
| Library    | Purpose |
|------------|---------|
| numpy      | Array-based iteration |
| matplotlib | Rendering |
| sympy      | Symbolic recursion |

## Module
`agents/skills/fractals.py`

## Key Functions
- `mandelbrot(width, height, max_iter)` — iteration count array
- `julia(c, width, height, max_iter)` — Julia set for constant c
- `lsystem(axiom, rules, depth)` — expand L-system string
- `lorenz(steps, dt)` — Lorenz attractor trajectory
- `fractal_dimension(points)` — box-counting dimension
- `ifs(transforms, n_points)` — IFS attractor point cloud
