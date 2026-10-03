---

name: leeway-mathematical-sun

description: Governed Central Radial Equilibrium evaluation layer for LeeWay skills and shiproom evidence. Represents discipline measurements as zero-centered deviation vectors, weighted radial potentials, deterministic threshold bits, and an 11-bit release register without claiming these are the canonical LeeWay Formula internals.

license: MIT

metadata:

  authority: Creator/Human Authority > LeeWay Standards

  mode: central-radial-equilibrium

  stage: measurement-to-shiproom

  metrics: skills/leeway-centered-skill-metrics/SKILL.md

  shiproom: skills/leeway-shiproom/SKILL.md

---

# LeeWay Mathematical Sun

## Authority boundary

The Mathematical Sun is a governed evaluation model proposed by the Creator. It may consume Formula-ready context and feed Shiproom, but it MUST NOT be called the canonical LeeWay Formula encoding unless the canonical implementation/version/hash explicitly binds to it.

## Continuous geometry

For each discipline i, define a measured deviation vector x_i with target/equilibrium x_i*=0 and an evidence-supported symmetric positive-definite W_i. Radial displacement is r_i = sqrt(x_i^T W_i x_i).

Zero means zero deviation from a defined target/envelope, not physically impossible zero work, zero render time, or zero resource consumption.

## Eleven-ray register

The governed v1 register contains: 1 SWE determinism; 2 distributed architecture; 3 SRE/observability/budget; 4 product delivery/value; 5 application security/STRIDE; 6 UX/accessibility; 7 organizational capacity; 8 motion dynamics; 9 PBR/BRDF physical validity; 10 Oklab/perceptual color; 11 frame budget/VRAM.

## Binary gate

For threshold theta_i >= 0, b_i = 1 iff r_i <= theta_i, otherwise 0. Encode Omega = sum(b_i * 2^(11-i)). For exactly 11 rays, Omega_max=2047. Phi_Gate = product(b_i), therefore Phi_Gate=1 iff Omega=2047.

## Hard-gate law

Binary compliance is deterministic only after x_i, W_i and theta_i are defined from evidence. Never invent missing measurements/weights/thresholds to force an all-1 state.

## Cross-skill law

Rays are measurement axes, not skill silos. A single skill may contribute to multiple rays and multiple skills may measure/repair one ray. Skill Orchestrator builds the capability weave; Mathematical Sun evaluates measured state.

## Extension law

The 11-bit v1 register is a release profile, not a universal upper bound on company intelligence. New measured disciplines may use versioned extension registers or hierarchical Suns. Never silently change bit order or reinterpret an existing bit.

## Creative geometry note

Vector Bézier continuity is currently a measured subdimension feeding creative/UX/rendering evidence rather than a v1 bit. Promote it to a new versioned ray only through an explicit schema/version change.

## Shiproom

Phi_Gate=1 may satisfy the Sun profile but does not override independent hard legal, authority, privacy, safety, integrity or other Shiproom blockers outside the profile.