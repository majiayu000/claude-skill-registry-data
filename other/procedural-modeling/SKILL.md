---

name: leeway-3d-procedural-modeling

description: Procedural and parametric 3D generation skill for repeatable geometry, modular environments, instancing, geometry nodes/graphs, seeded variation and deterministic regeneration.

license: MIT

---

# LeeWay 3D Procedural Modeling

## Use cases

Buildings, shelves, books, paths, vegetation distribution, repeated props, modular kits, LOD generation and parameterized variants.

## Contract

Declare parameters, units, seed/randomness policy, constraints, output ownership and regeneration test. Prefer instances over duplicated heavy geometry when visually equivalent.

## Verification

Regeneration with the same deterministic inputs should preserve required geometry/identity; stochastic variation must record seed/config.