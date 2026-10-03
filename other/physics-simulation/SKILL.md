---

name: leeway-3d-physics-simulation

description: 3D physics and simulation skill for rigid bodies, cloth, soft bodies, particles, fluids and physically constrained scene behavior with deterministic baking/validation where required.

license: MIT

---

# LeeWay 3D Physics & Simulation

## Setup

Define units, scale, mass/density, gravity, collision shapes, constraints, solver/time step, substeps, initial conditions and cache/bake policy.

## Validation

Simulation plausibility is measured against the intended behavior and stable numerical settings. Visual appeal does not prove physical correctness.

## Game route

Use offline simulation for authored/baked motion where appropriate; use simplified runtime physics/collision for interactive assets according to target performance.