---
name: beam-vibration
description: "Use when you must compute the natural frequencies of a continuous beam member: exact Euler-Bernoulli bending frequencies in hertz for pinned-pinned, cantilever, clamped-clamped and free-free end conditions from the characteristic-equation roots cos x cosh x = -1 and cos x cosh x = 1, the closed-form pinned-pinned law n^2 pi^2 sqrt(EI/(m L^4))/2pi, the shared rule f_n = (beta_n L)^2 sqrt(EI/(m L^4))/2pi, and a Rayleigh-quotient fundamental estimate omega^2 = 20 EI/(m L^4) for non-uniform cantilever shapes. Produces member natural frequencies for vibration clearance and excitation checks; complements the discrete 2-DOF modal-analysis leaf. Trigger: euler bernoulli beam, characteristic equation roots, cantilever beam, pinned-pinned beam, clamped beam frequency, free-free beam, rayleigh quotient, vibration clearance."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: far-25
    reference-only: true
gated: false
domain: structures
pack: fem
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: structures
  subdomain: fem
  tags: [beam-vibration, euler-bernoulli-beam, characteristic-equation-roots, cantilever-beam, pinned-pinned-beam, clamped-beam-frequency, rayleigh-quotient]
  version: 0.1.0
  author: AeroSkills
---

# Beam Vibration (structures/fem/beam-vibration)

Use when the task is computing the natural frequencies of a continuous
Euler-Bernoulli beam member: exact bending frequencies in hertz for
pinned-pinned, cantilever, clamped-clamped and free-free end
conditions, obtained from the transcendental characteristic-equation
roots rather than a discrete mass model. The beam is treated as a
distributed-parameter member with bending stiffness EI (N m^2) and
mass per unit length m (kg/m); every end condition reduces to a root
of cos x cosh x = -1 or cos x cosh x = 1, and each root feeds the
shared frequency law f_n = (beta_n L)^2 sqrt(EI / (m L^4)) / 2pi.
This leaf is the continuous-member complement to the discrete 2-DOF
modal-analysis leaf, and it supplies the member natural frequencies
that a random-vibration or vibration-clearance check consumes.

## Domain quick reference

- Transverse free vibration of a uniform Euler-Bernoulli beam obeys
  EI y'''' + m y_ddot = 0; separation of variables gives spatial
  solutions built from cos, sin, cosh and sinh of beta x, and the end
  conditions select the allowed beta_n L.
- Pinned-pinned (simply supported): beta_n L = n pi exactly, so
  f_n = n^2 pi^2 sqrt(EI / (m L^4)) / 2pi, with the exact spacing
  f_n = n^2 f_1. No root search is needed.
- Cantilever (fixed-free): cos x cosh x = -1. Bisection roots:
  1.87510407 (n=1), 4.69409113 (n=2), 7.85475744 (n=3).
- Clamped-clamped and free-free: cos x cosh x = 1, roots
  4.73004074 (n=1), 7.85320462 (n=2). A free-free beam also carries
  two zero-frequency rigid-body modes (translation, rotation); only
  the elastic modes are reported, so the first elastic free-free root
  is 4.73004074, identical to clamped-clamped.
- Shared frequency law for every end condition:
  f_n = (beta_n L)^2 sqrt(EI / (m L^4)) / 2pi in hertz, where the
  characteristic roots are non-dimensional.
- Rayleigh quotient for non-uniform members:
  omega^2 = int_0^L EI phi''^2 dx / int_0^L m phi^2 dx. With the
  uniform-cantilever parabola phi = (x/L)^2 this gives omega^2 =
  20 EI / (m L^4), an upper bound about 1.272x the exact fundamental
  (ratio sqrt(20) / 3.51602).
- FAR-25 (25.301-25.307) sets the certification context for structure
  loads and proof; the natural frequencies computed here feed
  vibration-clearance and excitation checks, not the loads
  themselves.

## Workflow

1. Gather the member data: bending stiffness EI (N m^2), mass per
   unit length m (kg/m) and length L (m), all SI.
2. Name the end condition: pinned-pinned, cantilever,
   clamped-clamped or free-free.
3. For a pinned-pinned member call pinned_pinned_frequency(mode_n,
   ei, mass_per_len, length_m); the closed form is exact and the mode
   ratios come out as exact squares.
4. For the other end conditions the module first re-derives the
   characteristic root with characteristic_root(mode_n, bc,
   tol=1e-12) by bisection: the cantilever root n=1 is bracketed in
   (1.8, 2.0), cantilever n>=2 in ((n-1) pi, n pi), and the
   clamped-clamped/free-free roots in (n + 0.5) pi +/- 0.8, brackets
   verified to straddle the published values. Pass any root into
   beam_frequency(beta_n_L, ei, mass_per_len, length_m), or call the
   convenience functions cantilever_frequency,
   clamped_clamped_frequency and free_free_frequency (elastic modes
   only) directly.
5. Sweep modes with beam_mode_frequencies(bc, n_modes, ei,
   mass_per_len, length_m) to get the first n_modes frequencies as an
   ascending list for one boundary condition.
6. For a non-uniform member or a quick shape-based estimate, call
   rayleigh_fundamental(ei, mass_per_len, length_m) with the stored
   cantilever-parabola shape and report the result as an upper bound
   to the exact fundamental.
7. Confirm the deterministic checks with the contract test
   scripts/test_beam_vibration.py.

## Worked example

Aluminum beam: E = 73.1 GPa, rho = 2780 kg/m3, cross-section 50 x
100 mm, L = 2 m. Then I = b h^3 / 12 = 4.1667e-6 m^4, EI = 3.0458e5
N m^2 and m = rho b h = 13.9 kg/m. Module outputs:

- Characteristic roots by bisection: cantilever 1.87510407,
  4.69409113, 7.85475744; clamped-clamped and free-free 4.73004074,
  7.85320462 (all match published Blevins values).
- Cantilever: f1 = 20.7089 Hz, f2 = 129.7803 Hz, f3 = 363.3887 Hz
  (about 20.709, 129.780, 363.389 Hz).
- Pinned-pinned: f1 = 58.1307 Hz, and f2 = 232.5228 Hz = 4 f1
  exactly.
- Clamped-clamped: f1 = 131.7758 Hz; free-free first elastic mode is
  the same 131.7758 Hz (shared root 4.73004074).
- Rayleigh cantilever-parabola estimate: 26.3403 Hz = 1.272x the
  exact 20.7089 Hz, confirming the upper-bound property.


## Pitfalls

- Reading the wrong characteristic equation: cantilever roots come
  from cos x cosh x = -1 while clamped-clamped and free-free share
  cos x cosh x = 1; swapping them swaps the frequency sets.
- Counting free-free rigid-body modes as elastic: a free-free beam
  carries two zero-frequency rigid-body modes, and the module
  reports elastic modes only - its first elastic root 4.73004074
  matches clamped-clamped, so expecting a lower first free-free
  frequency is wrong.
- Using the Rayleigh estimate as exact: the cantilever-parabola
  quotient gives 26.3403 Hz against the exact 20.7089 Hz fundamental
  in the worked example (an upper bound at 1.272x), so it is a
  screening bound, not the frequency.
- Forgetting pinned-pinned is closed form: pinned-pinned needs no
  root search, f_n = n^2 f_1 exactly; forcing it through the
  transcendental machinery invites rounding where none is needed.
- Feeding the shape guess into the wrong law: the shared law
  f = (beta_n L)^2 sqrt(EI / (m L^4)) / 2pi needs the
  NON-dimensional characteristic root, not a radian frequency or a
  beta in 1/m.
- Asking for invalid modes or members: a mode number below 1 (or
  fractional), non-positive EI, mass per length or length, and
  unknown boundary-condition names all raise ValueError.
## Verification

- Cantilever roots land within 1e-6 of 1.87510407 / 4.69409113 /
  7.85475744 and clamped roots within 1e-6 of 4.73004074 /
  7.85320462 (contract requires 1e-5).
- Pinned-pinned closed form: f_n / f_1 = n^2 exactly, asserted for
  several modes.
- Rayleigh bound: rayleigh_fundamental returns 26.3403 Hz, above the
  exact cantilever fundamental 20.7089 Hz by the expected 1.272x.
- Free-free reports elastic modes only: its mode list equals the
  clamped-clamped list, and no zero-frequency rigid-body rows
  appear.
- Determinism: no random numbers anywhere; identical floats run to
  run.
- beam_mode_frequencies returns n_modes entries in ascending order
  for every boundary condition.
- Every non-positive ei, mass per unit length or length, every mode
  number below 1 (and every fractional mode), and every unknown
  boundary-condition name raises ValueError.
- Run the contract test offline: python3
  scripts/test_beam_vibration.py (32 tests, deterministic, under one
  second).

## Related leaves

- structures/fem/modal-analysis: the discrete 2-DOF sibling; this
  leaf is its continuous-member complement for distributed-parameter
  beam members.
- structures/loads/random-vibration-analysis: consumes member natural
  frequencies for random excitation response assessment.
- cross-cutting/numerics/eigenvalue-decomposition: generic eigensolvers
  for discretized models; a continuous beam member instead uses the
  closed-form characteristic roots above.

## Behavior contract (gate 3)

Run the deterministic contract test (stdlib unittest, offline):

    python3 scripts/test_beam_vibration.py

The test covers the worked aluminum beam frequencies inside the spec
bounds, the published characteristic roots to 1e-5 or better, the
bisection brackets and tolerance behavior, the exact pinned-pinned
n^2 spacing, the shared beam_frequency law and its round trip, the
Rayleigh upper bound at 1.272x, the free-free elastic mode identity
with clamped-clamped, ascending mode lists for every boundary
condition, determinism run to run, and ValueError rejection of
non-positive stiffness/mass/length, invalid mode numbers and unknown
boundary-condition names.

## Compliance

- Standards referenced, not reproduced: FAR-25 is public-domain US
  government work (17 U.S.C. 105) but standards-map.yaml marks it
  gated: false and reference-only: true, so only the summary
  paraphrase above is used, never standard text. The characteristic
  roots and frequency laws are standard engineering methodology
  (Blevins-style formulas), summary-only.
- compliance: STANDARDS-REF, gated: false.
