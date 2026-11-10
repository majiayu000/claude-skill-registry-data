---
name: ecosim-plant-history-evaluation
description: Evaluate plant physiology and realized traits in existing EcoSIM history output against selected plant parameters, model equations, site observations and literature. Use for seasonal plant diagnostics, implausible growth or uptake, and parameter-sensitivity comparisons. Output-coverage checks alone and static plant_trait.desc validation belong to their dedicated skills.
---

# EcoSIM Plant History Evaluation

Evaluate how plants behaved during the requested simulation period and which
mechanisms or parameters plausibly explain that behavior. Distinguish numerical
validity, physiological plausibility and agreement with observations; none
establishes the others. Default to read-only analysis of existing output.

## Establish the comparison

1. Resolve the requested case, history files, date window, grid and active PFTs.
   For "last N years", use the last N complete years actually present, recording
   the assessment cutoff. For a follow-up to an earlier analysis, retain its
   frozen window unless the user requests a newer one. Do not infer completion
   from the namelist's intended end year or the presence of a restart alone.
2. Preserve a stable snapshot or a bounded extraction before analyzing live
   output. Record source paths, hashes, selected rows, time origin/calendar,
   interval coverage and extraction time. Preserve the namelist, selected input
   identities and executable provenance when available. A current namelist or
   source commit does not prove which inputs/binary produced old history.
3. Expand `forc_periods` from the original start date to map each model year to
   forcing year and cycle. For branches, account for the checkpoint and the
   staged schedule. Align weather, management and observations on their actual
   year basis. Check leap days, timezone and interval registration before daily
   scoring. Separate spin-up/cycled-year diagnostics from transient evaluation.
4. Read [history semantics and diagnostic rules](references/history_diagnostics.md)
   before calculating metrics. Verify dimensions, active masks, variable units,
   averaging and update/reset semantics against the selected model source.
   Treat unavailable fields and uncertain units as explicit gaps.

Use [ecosim-h0-target-extractor](../ecosim-h0-target-extractor/SKILL.md) for the
basic annual/seasonal targets when its time handling, season and PFT weighting
fit the task. Inspect its warnings and override inappropriate weighting. For a
single active PFT, report that PFT directly. Do not infer leaf area from whole
shoot carbon when actual leaf-area information is available.

For tower/field evaluation, read [observation matching and conversions](references/observation_comparison.md)
before declaring a target unavailable or computing observation scores. It covers
archived sensor metadata, harvest-comment yields, moisture conversion, hourly
restart checks and multiweek time series, and the distinction between seasonal
agreement and interannual skill.

## Evaluate plant behavior

Choose relevant diagnostics from the reference; do not fabricate absent fields
or force irrelevant checks onto nonvascular vegetation, perennial stands or
bare periods. At minimum, cover the user's requested quantities and enough
coupled variables to assess their interpretation.

- **Numerical and accounting checks:** contiguous interval coverage, valid
  active data, carbon identities, conservation counters, nonphysical negative
  pools and abrupt unexplained changes. An emitted all-fill target is a gap;
  masked inactive PFT/layer padding is not automatically an error.
- **Canopy and phenology:** seasonal LAI, height, leaf/shoot/root biomass,
  emergence or leafout, flowering, grain filling and senescence as applicable.
  Compare photosynthetic shutdown with green leaf area and phenological stage.
- **Photosynthetic traits:** realized SLA, Vcmax25, Vomax25, Jmax25, Rubisco
  activation, leaf N/P and protein allocation. Compare the relevant growing or
  mature-leaf period, not all-year means dominated by zeros or senescing tails.
- **Water supply:** canopy potential, water-stress counters, root uptake and
  biomass by layer, rooted-zone moisture, oxygen stress and comparable radial,
  axial and soil resistance diagnostics. Wet column-average soil alone does
  not establish adequate water delivery to leaves.
- **Nutrients and reproduction:** total and mineral uptake, uptake timing,
  tissue concentrations, grain number/mass and remobilization where available.
  Read fertilizer and irrigation inputs back from selected files; distinguish
  input amounts, gross uptake, plant accumulation and fertilizer recovery.

Save annual and relevant seasonal/PFT metrics with units and definitions.
Produce a small set of scientific plots that reveal timing and coupled
responses, rather than only annual means. Visually inspect generated figures.

## Condition diagnoses on parameters and evidence

Use [ecosim-plant-trait-sanity-check](../ecosim-plant-trait-sanity-check/SKILL.md)
on the relevant **read-only** `plant_trait.*.desc` files, and compare their
values with the selected PFT NetCDF. Record temporal changes rather than
assuming one year's traits apply throughout. Check cohort age, initialization,
planting density, disturbance and management before comparing modeled plants
with a mature field stand.

Trace each proposed explanation from history behavior through its update
equation to a real selected parameter. Account for reader conversions before
comparing printed input traits with output capacities. Separate enzyme amount,
maximum catalytic capacity, temperature response and activation; increasing
capacity does not resolve zero activation by itself. Preserve jointly
constrained kinetics and allocations when proposing tuning.

Use staged BIF/field records and tower observations first, then browse primary
literature for ecological judgments and parameter recommendations. Use
[plant-trait-target-deriver](../plant-trait-target-deriver/SKILL.md) when typical
literature targets are needed. Match species/root class, cohort, organ,
temperature, experimental conditions, units and temporal/depth support. Keep
measured site values, literature context, model defaults and diagnostic
perturbations distinct. Explain rather than average away conflicts.

Rank tuning candidates by coupled evidence. State the baseline value, mechanism,
supported range or explicitly labeled sensitivity factors, intended diagnostic
response and remaining uncertainty. Do not increase SLA, enzyme allocation,
fertilizer or uptake Vmax just to compensate for a small canopy without checking
biomass supply, hydraulics, phenology and nutrient feedback. Do not silently
change parameters while evaluating output.

The [US-Ne1 worked example](references/us-ne1_lessons.md) illustrates the unit,
root-geometry and causal-inference traps. Its numerical values and outcomes are
case-specific, not universal thresholds or defaults.

## Missing outputs and requested sensitivity runs

An evaluation request alone does not require a new simulation. Report what can
be established from existing output and which missing diagnostics limit it.
Use [ecosim-evaluation-output-check](../ecosim-evaluation-output-check/SKILL.md)
when the task includes establishing output coverage; that one-year workflow
tests output readiness, not scientific agreement. Enable registered inactive
fields through `hist_fincl*`, reconcile exclusions and averaging qualifiers,
and verify actual emission. Unregistered mechanisms need instrumentation.

When a sensitivity run is requested, follow the model repository's
`ecosim-restart-run` skill for existing checkpoints, or the appropriate site-run
workflow. Use private parameter copies through
[ecosim-pftpar-editor](../ecosim-pftpar-editor/SKILL.md), fresh output directories
and the mandatory current case preflight before each launch. Preserve the
requested duration and forcing mapping. A matched unchanged-parameter control
from the same checkpoint separates parameter response from restart/state
effects. Record runtime completion separately from unresolved trait findings.
Do not rebuild a usable executable merely to analyze history.

## Deliverables

Save under the selected case's `evaluation/<unique-assessment>/` (or the user's
chosen destination):

- Scope/provenance and a reproducible script or explicit calculation manifest.
- Annual/seasonal metrics and comparison tables with units and missing targets.
- Focused plots, field/literature evidence and a readable report.
- Separate verdicts for output validity, plant behavior and parameter plausibility;
  ranked diagnoses and any proposed sensitivities, with uncertainty stated.

Lead the response with the main supported finding. Quantify consequential
conflicts and show their calculations. In HTML reports, use a red title for the
warning/conflict section, following the repository's reporting convention.
Update the existing site tracker if this evaluates an active site-run task;
do not mark a full simulation or field validation complete from a short test.
