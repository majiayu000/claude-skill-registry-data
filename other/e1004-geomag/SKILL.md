---
name: e1004-geomag
description: "Use when defining the geomagnetic field environment model for a mission under ECSS-E-ST-10-04C: select the applicable geomagnetic field model (an IGRF-class internal field model alone at low/mid geocentric distance, or that model combined with an external/magnetospheric field model at high geocentric distance) from the mission orbit's geocentric distance, determine the correct IGRF epoch and apply secular variation to update the reference internal field for the mission's target date, verify the target date remains within the secular-variation extrapolation validity window, compute the dipole-approximation B,L equatorial field magnitude for radiation-belt characterization, and validate that the analysis case's declared model and epoch handling meet these requirements. Trigger: geomagnetic field, IGRF, secular variation, B L coordinates, magnetospheric field, external field model, Tsyganenko, dipole approximation, e-st-10-04, ecss, space environment."
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
  tags: [ecss, e-st-10-04c, geomag, igrf, secular-variation, b-l-coordinates, external-field, space-environment]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Geomagnetic Field Environment (space-systems/ecss/e1004-geomag)

Use when the task is selecting and applying a geomagnetic field model
under ECSS-E-ST-10-04C clause 5.2, to characterize the Earth's
internal magnetic field (and, where applicable, the external
magnetospheric contribution) for a mission orbit, including epoch
selection, secular-variation handling, and B,L coordinate usage.

## Domain quick reference

- The geomagnetic field has an internal (core-origin) component and
  an external (magnetospheric) component. The internal component
  dominates at low and mid geocentric distance and is well
  represented by an IGRF-class spherical-harmonic model alone. At
  high geocentric distance -- approaching and beyond the magnetopause
  region -- the external/magnetospheric contribution (solar-wind
  interaction, ring current, tail currents) becomes significant and
  an internal-only model understates the actual field; an external
  field model (e.g. a Tsyganenko-class model) must be added.
  Geomagnetic shielding of incident particle flux (Stormer cutoffs) is
  the sibling e1004-stormer leaf; trapped-belt long-term flux models
  are the sibling e1004-trapped-leo leaf -- both consume the field
  geometry this leaf characterizes rather than redefining it.
- IGRF-class models are published as spherical-harmonic (Gauss)
  coefficient sets at fixed 5-year epochs, each accompanied by a
  secular-variation (SV) coefficient set describing the field's
  linear rate of change. Coefficients between two published epochs
  are interpolated; coefficients for dates after the latest published
  epoch are extrapolated by applying the SV rate, and that
  extrapolation is only certified accurate for a bounded number of
  years (nominally the 5 years following the latest epoch) until the
  next IGRF generation is released.
- B,L coordinates express a field point by the local field magnitude
  B and the McIlwain L-shell parameter; L labels the dipole field
  line the point lies on and is the standard coordinate for
  characterizing trapped-radiation-belt structure. A dipole
  approximation gives the equatorial field magnitude on a given
  L-shell as the epoch equatorial surface field strength divided by L
  cubed.
- This leaf scopes internal/external model selection by geocentric
  distance regime, IGRF epoch and secular-variation handling, and the
  B,L dipole-approximation field computation only. It does not
  implement the full spherical-harmonic synthesis of the real IGRF
  coefficient set -- that is an external reference implementation
  (see the informative e1004-ref-geomag reference-data leaf) -- nor
  does it compute Stormer cutoffs or belt fluxes.

## Workflow

1. For each geomagnetic analysis case, record its case id, the
   mission orbit's geocentric distance (Earth radii), the target
   date (decimal year) the field is needed for, the model the
   analysis declares it used, the epoch equatorial surface field
   strength (B0) for the nearest IGRF epoch, and the secular-variation
   rate for that epoch.
2. Classify the case's geocentric distance into a field regime:
   "internal_only" at or below the internal/external threshold
   distance, "internal_plus_external" above it.
3. Select the model required for that regime (IGRF-class internal
   field model alone, or that model combined with an
   external/magnetospheric field model) and compare it against the
   case's declared model; flag a mismatch rather than accepting an
   internal-only analysis at high geocentric distance.
4. Determine the nearest IGRF epoch at or before the target date and
   the elapsed time since that epoch; verify the target date falls
   within the secular-variation extrapolation validity window
   (target date not before the earliest published epoch, and not more
   than the extrapolation limit beyond the latest published epoch).
5. Apply secular variation: scale the epoch equatorial field strength
   by the secular-variation rate over the elapsed time to obtain the
   field strength applicable to the target date.
6. Where a case supplies an L-shell value, compute the dipole
   equatorial field magnitude at that L-shell from the
   secular-variation-adjusted equatorial field strength.
7. Mark the case compliant only when its declared model matches the
   regime's required model and its target date is within the epoch
   validity window; roll every case's compliance into the assessment
   record and do not close the geomagnetic field model definition
   while any case remains non-compliant.

## Pitfalls

- Using an internal-only IGRF model for a high-altitude or
  magnetopause-adjacent orbit instead of adding the
  external/magnetospheric contribution, understating the actual field
  (and, downstream, misjudging particle trajectories that depend on
  it).
- Applying secular variation beyond its certified extrapolation
  window instead of flagging that a newer IGRF generation is needed,
  silently carrying growing error into the field estimate the further
  the target date drifts past the latest published epoch.
- Treating the B,L dipole approximation as exact near the real,
  non-dipolar field (e.g. in the South Atlantic Anomaly) rather than
  as a simplified coordinate for belt characterization only.
- Selecting an epoch by nearest calendar rounding instead of the
  correct interpolation/extrapolation rule, which silently drops the
  secular-variation correction that dominates the difference between
  adjacent epochs.

## Behavior contract (gate 3)

The regime classification, model-selection, IGRF epoch validity,
secular-variation, and B,L field-computation logic is exercised by
the gate 3 contract test: scripts/test_e1004_geomag.py against
scripts/e1004_geomag_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e1004_geomag.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
