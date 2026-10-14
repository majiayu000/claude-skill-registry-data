---
name: e1012-bg-gwd
description: "Use when estimate radiation-induced noise contributions for a space-based gravity-wave detector test mass under ECSS-E-ST-10-12C §10.4.7: determine the particle-flux-driven charge deposition rate on the test mass, compute the stochastic force noise power spectral density from charge shot-noise coupling and from cosmic-ray momentum-transfer recoil, convert total force noise to displacement noise using the free test-mass transfer function, verify that accumulated charge stays within the charge-management design limit, and compare resulting displacement noise against the instrument radiation noise budget allocation. Trigger: ecss, e-st-10-system-scope, gravity-wave-detector, radiation-noise, charge-deposition, force-noise-psd, displacement-noise, cosmic-ray, test-mass, noise-budget."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, e-st-10-system-scope, gravity-wave-detector, radiation-noise, charge-deposition, force-noise-psd, displacement-noise, cosmic-ray, test-mass, noise-budget]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Space Environment — Gravity-Wave Detector Radiation Noise (space-systems/ecss/e1012-bg-gwd)

Use when the task is to estimate radiation-induced noise for a space-based
gravity-wave detector (GWD) test mass per ECSS-E-ST-10-12C §10.4.7 —
characterising the particle-environment-driven charge deposition rate,
computing the resulting stochastic force noise and cosmic-ray recoil force
noise, converting to displacement noise, and verifying compliance with the
charge-management design limit and the instrument radiation noise budget.

## Domain quick reference

- Two radiation noise mechanisms act on a free-falling GWD test mass.
  First, ionising particles deposit net charge on the test mass at a
  Poisson rate Ṅ_q (charges/s); because the test mass is capacitively
  coupled to its electrode housing (coupling α N/C), the accumulated charge
  creates a force. The Poisson statistics of the deposition process produce
  a random-walk charge fluctuation whose force noise power spectral density
  (PSD) rises steeply toward lower frequencies: S_F_charge(f) = α² × 2e²
  × Ṅ_q / (2πf)², where e is the elementary charge. Second, galactic and
  trapped heavy ions traverse the test mass and transfer momentum; the
  Poisson arrival of these impulses gives a white (frequency-independent)
  force noise floor: S_F_CR = 2 × Ṅ_CR × p̄², where Ṅ_CR is the impact rate
  and p̄ is the mean momentum transfer per impact.
- The particle environment is characterised via the proton, electron, and
  cosmic-ray fluxes at the mission orbit (from ECSS-E-ST-10-04C models).
  Net charge per particle must account for secondary electron emission,
  which partially offsets the deposited charge; ignoring secondaries
  overestimates the charge rate and therefore the force noise.
- The charge-management system (typically an ultraviolet discharge
  mechanism) keeps the accumulated charge Q near zero between discharge
  pulses. The assessment must bound Q_acc = Ṅ_q × e × Δt over the
  interval between discharges and check it does not exceed the design
  maximum Q_max. Exceeding Q_max is a charge-management finding independent
  of the noise budget comparison.
- Displacement noise is obtained from total force noise via the free
  test-mass mechanical transfer function:
  S_x(f) = S_F_total(f) / (m × (2πf)²)², where m is the test mass.
  The test mass is radiation-noise-compliant only when both the charge
  budget and the displacement noise budget are satisfied.

## Workflow

1. Obtain the ionising-particle flux at the mission orbit: proton and
   electron differential spectra and the galactic (plus trapped) cosmic-ray
   flux, sourced from ECSS-E-ST-10-04C space environment models. Identify
   the orbit phase (solar min/max, trapped-belt passage) that gives the
   worst-case charge deposition rate.
2. Determine the effective cross-section of the test mass presented to the
   flux (the face area projected along the dominant flux direction) and the
   mean net charges deposited per particle, accounting for secondary
   electron yield from the test-mass material.
3. Compute the charge deposition rate:
   Ṅ_q = flux × effective_area × mean_net_charges_per_hit  (charges/s).
4. Compute the charge-driven force noise PSD at the measurement frequency f:
   S_F_charge(f) = α² × 2e² × Ṅ_q / (2πf)²  (N²/Hz),
   where α is the electrostatic coupling coefficient (N/C) derived from the
   electrode-housing geometry and the test-mass bias voltage.
5. Compute the cosmic-ray recoil force noise PSD:
   impact rate Ṅ_CR = cr_flux × test_mass_total_area  (impacts/s);
   S_F_CR = 2 × Ṅ_CR × p̄²  (N²/Hz, white),
   where p̄ is the mean momentum transfer per impact from the energy
   spectrum and the test-mass stopping-power model.
6. Sum all force noise contributors:
   S_F_total(f) = S_F_charge(f) + S_F_CR.
7. Convert to displacement noise:
   S_x(f) = S_F_total(f) / (m × (2πf)²)²  (m²/Hz).
8. Compute accumulated charge over the exposure window (or discharge cycle):
   Q_acc = Ṅ_q × e × Δt  (C).
   Check Q_acc ≤ Q_max; flag an exceedance as a charge-management finding.
   Compare S_x against the instrument radiation noise budget allocation;
   flag any exceedance as a noise-budget finding. Report overall compliance
   only when both finding lists are empty.

## Pitfalls

- Evaluating the charge-driven force noise at a convenient mid-band
  frequency rather than the actual measurement-band lower edge: S_F_charge
  rises as 1/f², so noise near the low-frequency limit of the band is much
  larger than at a higher reference point. Always evaluate at the lowest
  frequency of the sensitivity band.
- Omitting secondary electron emission when estimating net charge per
  particle: energetic protons and electrons can each liberate one or more
  secondary electrons from the gold test-mass surface, offsetting some
  primary charge. Ignoring secondaries overestimates Ṅ_q, which in turn
  overestimates S_F_charge and may trigger false exceedances.
- Assuming that the charge-management system keeps Q = 0 at all times:
  the discharge system operates with a finite duty cycle. The assessment
  must bound Q_acc over the full interval between consecutive discharge
  events and verify it stays below Q_max; compliance with the noise budget
  does not imply compliance with the charge budget.
- Applying cosmic-ray momentum-transfer values from high-energy galactic
  primaries to trapped-belt protons or solar energetic protons without
  adjusting p̄ for the actual energy spectrum: the momentum transfer per
  particle varies substantially with energy and test-mass thickness, so a
  single generic p̄ drawn from the wrong population can underestimate the
  recoil noise from the dominant local environment.
- Adding force noise PSDs from contributors evaluated at different
  frequencies: each contributor must be evaluated at the same f =
  f_measurement before summation; mixing values from different frequencies
  produces a meaningless total.

## Behavior contract (gate 3)

The charge-deposition, charge-force-noise, cosmic-ray-recoil, displacement-
noise, accumulated-charge, and budget-compliance logic is exercised by the
gate-3 contract test: scripts/test_e1012_bg_gwd.py against
scripts/e1012_bg_gwd_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e1012_bg_gwd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
