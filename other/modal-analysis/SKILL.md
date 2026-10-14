---
name: modal-analysis
description: "Use when you must run a modal analysis of a two degree of freedom mass-spring structural model: compute the natural frequencies in rad/s and Hz, derive the mode shape ratios, and check an excitation frequency against the natural frequencies for resonance risk. Units are SI: masses in kg, stiffnesses in N/m, frequencies in rad/s and Hz. Trigger: modal analysis, natural frequency, mode shape, resonance, eigenvalue, vibration, two degree of freedom."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: far-25
    reference-only: true
gated: false
domain: structures
pack: structures
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: structures
  subdomain: fem
  tags: [modal-analysis, natural-frequency, mode-shape, resonance, eigenvalue, vibration, two-dof, structural-dynamics]
  version: 0.1.0
  author: Aero Agent Skills
---

# Modal Analysis (structures/fem/modal-analysis)

Use when the task is modal analysis of a two degree of freedom (2-DOF)
mass-spring structural model: computing natural frequencies in rad/s
and Hz, deriving mode shape ratios, and checking resonance risk
against an excitation frequency. Units are SI: masses in kg,
stiffnesses in N/m, frequencies in rad/s and Hz.

## Domain quick reference

- Modal analysis solves the generalized eigenvalue problem
  (K - w^2 M) phi = 0 for the natural frequencies w and the mode
  shape vectors phi of an undamped system.
- A 2-DOF model grounded at both ends has stiffness matrix
  K = [[k1+k2, -k2], [-k2, k2]] and mass matrix M = diag(m1, m2);
  the two natural frequencies are the roots of det(K - w^2 M) = 0.
- Each natural frequency has an associated mode shape: the relative
  motion of the two masses, expressed here as the ratio phi2/phi1.
- Forcing near a natural frequency drives large response amplitudes;
  a resonance check flags excitation frequencies inside a tolerance
  band around any natural frequency.
- FAR-25 (25.301-25.307) sets the certification context for structure
  loads and proof; this skill computes the modal quantities that
  feed vibration-sensitive assessments, not the loads themselves.

## Workflow

1. Gather the two masses (kg) and the two spring rates (N/m) of the
   grounded 2-DOF model.
2. Compute the natural frequencies in rad/s with natural_frequencies
   and in Hz with frequencies_hz.
3. Derive the mode shape ratio for each mode with mode_shapes
   (normalized to a first component of 1.0).
4. Check the excitation frequency with resonance_check (default
   tolerance band 10% of each natural frequency).
5. Interpret the verdict: resonance True means the excitation sits
   inside the band of a natural frequency; detune stiffness or mass
   to move the natural frequencies away.

## Pitfalls

- Mixing units: the module is all-SI (kg, N/m, rad/s, Hz); convert
  inputs before calling the functions.
- Forgetting that the coupling spring k2 appears in both diagonal
  entries of K (as k1+k2 and as k2).
- Reading mode shape ratios as absolute displacements; they describe
  relative motion only.
- Using an overly wide resonance tolerance band; 10% of the natural
  frequency is the default.
- Applying a 2-DOF result to a structure that needs more degrees of
  freedom to represent its modes.

## Behavior contract (gate 3)

The modal logic is exercised by the gate 3 contract test:
scripts/test_modal_analysis_logic.py against
scripts/modal_analysis_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_modal_analysis_logic.py

## Compliance

- FAR-25 is referenced, not reproduced: standards-map.yaml marks it
  gated: false and reference-only: true; only the summary paraphrase
  above is used, never standard text.
- compliance: STANDARDS-REF, gated: false.
