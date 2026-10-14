---
name: e1012-dd-unc
description: "Use when determine displacement damage (DD) assessment uncertainty factors for a spacecraft radiation analysis under ECSS-E-ST-10-12C §8.7: identify each uncertainty source (environment model, NIEL scaling, shielding transport, and device response data), assign a numeric factor to each source, combine the factors into an overall uncertainty multiplier using either the multiplicative or root-sum-square method, apply the combined factor to the nominal proton-equivalent fluence to obtain the design fluence, and verify the result accommodates the required design margin. Trigger: ecss, e-st-10-12c, displacement-damage, dd-uncertainty, niel-scaling, radiation-hardness-assurance, proton-fluence, uncertainty-budget, design-margin."
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
  tags: [ecss, e-st-10-12c, displacement-damage, dd-uncertainty, niel-scaling, radiation-hardness-assurance, proton-fluence, uncertainty-budget, design-margin]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Radiation Hardness Assurance — Displacement Damage Uncertainty Budget (space-systems/ecss/e1012-dd-unc)

Use when the task is to determine and document the uncertainty budget for a
displacement damage (DD) radiation assessment, per ECSS-E-ST-10-12C §8.7.
The procedure identifies each source of uncertainty, assigns a bounding factor,
combines the factors into a single overall multiplier, applies it to the nominal
proton-equivalent fluence, and checks whether the resulting design fluence is
covered by the device's DD withstand capability with the required margin.

## Domain quick reference

- Displacement damage (DD) results from non-ionizing energy deposited by
  incident particles (protons, neutrons, electrons, heavy ions) that displace
  atoms from their crystal lattice sites. The damage level is characterised by
  the proton-equivalent fluence (p_eq/cm²), derived by applying Non-Ionizing
  Energy Loss (NIEL) scaling factors to each particle species in the environment.
- §8.7 of ECSS-E-ST-10-12C requires that the DD assessment explicitly accounts
  for every significant uncertainty source. Four sources must be addressed:
  (a) **environment model** — uncertainty in the particle flux/fluence predicted
      by the space environment model (e.g. AP8/AP9 proton belts, solar proton
      event statistics);
  (b) **NIEL scaling** — uncertainty in the NIEL tables or functions used to
      convert each particle species to the proton-equivalent basis; published
      NIEL values carry their own experimental scatter;
  (c) **shielding transport** — uncertainty introduced by simplifying the
      spacecraft geometry or using an approximate particle-transport code;
  (d) **device response data** — uncertainty arising from limited lot-to-lot
      test data, inter-device scatter, or extrapolating published DD thresholds
      to the actual mission conditions.
- Each source is assigned a numeric uncertainty factor ≥ 1.0 representing the
  upper-bound multiplier on the nominal estimate. Two combination methods are
  used in practice: multiplicative (product of all factors, conservative, used
  when source independence cannot be demonstrated) and root-sum-square (RSS,
  applied when sources are statistically independent, yielding a smaller but
  still bounding combined factor).
- The combined uncertainty factor is applied to the nominal proton-equivalent
  fluence to yield the design fluence. The device's DD withstand fluence must
  exceed the design fluence by at least the required design margin factor
  (typically 2.0 for qualified parts per the ECSS radiation hardness assurance
  programme).

## Workflow

1. List every uncertainty source relevant to the assessment. At minimum address
   the four mandatory sources: environment model, NIEL scaling, shielding
   transport, and device response data. Reject any source label not in this set
   before assigning a factor.
2. Assign a numeric factor ≥ 1.0 to each source, justified by supporting
   evidence (model validation data, published NIEL scatter bounds, transport
   code benchmarks, device test scatter). A factor of 1.0 must be explicitly
   justified; it implies negligible uncertainty from that source.
3. Select the combination method. Use multiplicative unless the independence of
   every source pair can be demonstrated; use RSS only when that demonstration
   is documented. Compute the combined factor by the chosen method.
4. Multiply the nominal proton-equivalent fluence by the combined factor to
   obtain the design fluence. This is the fluence the part must survive with
   margin.
5. Retrieve the device DD withstand fluence from the radiation test data or
   the published tolerance level. Compute the margin factor as withstand fluence
   divided by design fluence.
6. Compare the margin factor against the required value (default 2.0 for
   standard qualification paths). If the margin factor is below the required
   value, the part fails the DD margin check; increase shielding, select a more
   tolerant device, or reduce mission fluence.
7. Document the full uncertainty budget: source list, assigned factors,
   combination method, combined factor, nominal fluence, design fluence, margin
   factor, and pass/fail conclusion. The budget is a required deliverable under
   §8.7.

## Pitfalls

- Assigning factors less than 1.0 on the basis that an uncertainty source
  is "well-characterised". A factor less than 1.0 implies the nominal estimate
  overestimates the true value, which is not a conservative assumption for a
  margin check. All factors must be ≥ 1.0.
- Combining factors using RSS without documenting the independence argument.
  RSS gives a smaller combined factor than multiplicative; using it without
  justification unconservatively reduces the design fluence and may hide a
  margin shortfall.
- Omitting the NIEL scaling source because it appears small. NIEL tables for
  protons at energies below ~10 MeV carry non-trivial scatter; omitting this
  source is not permissible under §8.7 without an explicit justification that
  its factor equals 1.0.
- Reading a margin factor ≥ 1 as a pass when the required margin is 2.0.
  A margin factor of 1.5 means the device survives the design fluence but
  without the required safety margin; this is a margin non-compliance, not a
  pass.
- Using the same uncertainty budget across different device types or mission
  orbits without re-evaluating the environment model factor. Each orbit profile
  samples a different particle energy spectrum, and the model uncertainty is
  spectrum-dependent.

## Behavior contract (gate 3)

The factor validation, combination logic (multiplicative and RSS), design
fluence computation, margin check, and end-to-end budget assembly are exercised
by the gate 3 contract test: scripts/test_e1012_dd_unc.py against
scripts/e1012_dd_unc_logic.py (stdlib unittest, offline). Run:

    python3 scripts/test_e1012_dd_unc.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite source and paraphrase per
  standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
