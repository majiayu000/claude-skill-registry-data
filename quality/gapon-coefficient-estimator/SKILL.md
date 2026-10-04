---
name: gapon-coefficient-estimator
description: Estimate calcium-normalized Gapon selectivity coefficients from paired exchange and solution chemistry, or initialize depth-explicit EcoSIM Gapon inputs from the closest bundled ecosystem template when paired chemistry is unavailable. Use when deriving or checking EcoSIM GKC4, GKCH, GKCA, GKCM, GKCN, or GKCK values; matching a target ecosystem, climate, vegetation, and management regime to a starting profile; remapping template values to target soil layers; or documenting that template-based values require calibration or tuning.
---

# Gapon Coefficient Estimator

## Core Rule

Do not compute Gapon coefficients from SSURGO/gSSURGO alone. Prefer a
site-specific calculation when both of these data groups are available:

- Exchange phase: exchangeable cations in charge-equivalent units, ideally
  `cmolc/kg` (`CaX`, `MgX`, `NaX`, `KX`, `NH4X`, `AlX`, `FeX`, `HX`).
- Solution phase: ion activities, or at least consistently unit-normalized
  dissolved concentrations for `Ca`, `Mg`, `Na`, `K`, `NH4`, `Al`, `Fe`, and
  `H`.

SSURGO/gSSURGO can provide priors such as `cec7_r`, `ecec_r`, `sumbases_r`,
`ph1to1h2o_r`, `ec_r`, `sar_r`, `extracid_r`, and `extral_r`, but standard
`chorizon` does not provide all species-resolved exchangeable bases or
solution cation activities.

When paired chemistry is unavailable and an EcoSIM input still needs starting
values, use the bundled depth-explicit ecosystem templates as an explicit
fallback. Select the ecosystem family closest to the target first, then refine
the match with climate, vegetation, water regime, and management. Never
describe template values as measured, site-derived, or independently
validated.

Every template-based output and user-facing summary must include this reminder:

> Gapon coefficients are initialized from the closest ecosystem template, not
> derived from site-specific paired exchange and solution chemistry. They are
> starting values and are subject to calibration or tuning when needed.

## Lyotropic Adsorption Prior

Use the cation adsorption lyotropic series as a calibration and QC prior:

`Al = Fe > Ca > Mg > K = NH4`

This means trivalent `Al` and `Fe` should generally be treated as the
strongest exchange competitors, followed by `Ca`, then `Mg`, with `K` and
`NH4` approximately tied at lower adsorption strength. Use this order to
interpret uncertain coefficients, set plausible priors, and flag suspicious
data inversions. Do not overwrite paired exchange-solution evidence solely to
force the series. `Na` is retained for EcoSIM sodicity calculations but is not
part of this specific adsorption series, and `H` is pH-controlled rather than a
simple base-cation competitor.

## Data-Derived Workflow

1. Gather exchangeable cations from local lab data, WoSIS profiles, national
   soil lab datasets, or project measurements. Use SSURGO/gSSURGO only for
   CEC/ECEC/pH/acidity priors and gap flags.
2. Gather solution chemistry from saturated paste, soil solution, lysimeter,
   groundwater, stream chemistry, or a geochemical speciation model.
3. Convert exchangeable cations to consistent charge-equivalent units.
4. Convert solution concentrations to activities if possible. If using raw
   concentrations, label the output as an activity approximation.
5. Compute Ca-normalized Gapon coefficients with:

   `K_G(Ca-i) = (E_i / E_Ca) * a_Ca^(1/2) / a_i^(1/z_i)`

   where `E_i` and `E_Ca` are exchange-phase equivalent amounts and `z_i` is
   the cation charge. This gives exponents of 1 for monovalent ions, 1/2 for
   divalent ions, and 1/3 for Al3+ or Fe3+.
6. Report quality flags: missing solution data, CaX closure assumptions,
   concentration-as-activity assumptions, negative closures, lyotropic-series
   inconsistencies, and conditional Al/Fe/H interpretations.

## Ecosystem-Template Fallback

Use this route only when paired exchange-solution chemistry is missing or
insufficient for a defensible calculation:

1. Identify the target ecosystem family. Use the actual land use or ecosystem,
   such as cropland, forest, pasture, grassland, tundra, wetland, peatland, or
   rainforest; do not match from climate alone.
2. Record climate, dominant vegetation or crop, water regime, and management.
   These attributes distinguish otherwise similar cases, including dryland and
   irrigated maize-soybean systems.
3. Run `scripts/select_gapon_template.py`. Automatic selection requires a
   same-family template. Use `--template-id` only for a deliberate, documented
   override.
4. Preserve the source profile layers or map the selected profile to the target
   EcoSIM layer-bottom depths. Mapping uses the source layer that contains each
   target bottom depth and extends the deepest source value only when needed.
5. Transfer all six supported coefficients together: `GKC4` (Ca-NH4), `GKCH`
   (Ca-H), `GKCA` (Ca-Al), `GKCM` (Ca-Mg), `GKCN` (Ca-Na), and `GKCK` (Ca-K).
6. Keep the generated provenance JSON with the EcoSIM input. Where the target
   format supports metadata, also record `gapon_source_method`,
   `gapon_template_id`, and the mandatory template/tuning reminder.
7. Replace or calibrate the starting values when paired chemistry, exchange
   observations, soil-solution data, or site response data become available.

## Important Scientific Cautions

- Ca-Mg under the general Gapon form uses `sqrt(a_Ca) / sqrt(a_Mg)`, not
  `a_Ca / a_Mg`. If a project uses Vanselow or Gaines-Thomas selectivity
  conventions, state that explicitly and do not mix coefficients.
- `extracid_r` is exchangeable acidity, not pure exchangeable H. If Al is
  separately available, estimate `HX = max(extracid - AlX, 0)` only as a
  flagged approximation.
- `extral_r` or lab-extractable Al is not automatically aqueous `Al3+`.
  Solution Al should be speciated because hydrolysis and DOC complexation
  strongly affect activity.
- Exchangeable Fe and solution `Fe3+` are usually difficult to interpret from
  total or extractable Fe alone. Fe hydrolysis, oxide precipitation, redox
  state, and organic complexation can dominate apparent Fe activity; use
  speciated Fe activities when possible and flag total-Fe substitutions.
- `[H+] = 10^-pH` is a fallback activity estimate only; pH method and solution
  matrix matter.
- `NH4X` is transient and usually absent from regional soil maps; prefer local
  agronomic or incubation data.
- The lyotropic series `Al = Fe > Ca > Mg > K = NH4` is a prior for cation
  adsorption strength, not a mass-balance equation. If fitted coefficients
  violate it, keep the measured result but report the inversion and check
  extraction chemistry, activity corrections, and units.
- For EcoSIM, treat data-derived coefficients as uncertain calibrated
  parameters and ecosystem-template coefficients as initialization priors.
  Neither route makes them deterministic outputs from global soil products.

## Script

Use `scripts/estimate_gapon_coefficients.py` for repeatable CSV calculations.
It accepts flexible column aliases, estimates missing `CaX` by a flagged CEC
or ECEC closure when requested, and writes coefficient plus QC columns,
including `kg_ca_fe`, `lyotropic_series`, and possible lyotropic inversion
flags.

Example:

```bash
python .agents/skills/gapon-coefficient-estimator/scripts/estimate_gapon_coefficients.py \
  --input data/site_exchange_solution.csv \
  --output result/site_gapon_coefficients.csv \
  --estimate-ca
```

Use `--self-test` to run a built-in smoke test.

Use `scripts/select_gapon_template.py` when paired chemistry is unavailable.
It selects the closest ecosystem profile, remaps it to requested layer-bottom
depths, writes all six EcoSIM coefficients, and creates a provenance sidecar.

Example:

```bash
python .agents/skills/gapon-coefficient-estimator/scripts/select_gapon_template.py \
  --ecosystem-type "maize soybean cropland" \
  --climate "warm temperate" \
  --water-regime dry \
  --management "dryland rotation" \
  --target-depths "0.01,0.03,0.06,0.10,0.16,0.23,0.33,0.45,0.60,0.80,1.20,2.00" \
  --output result/site_gapon_template.csv
```

Use `--list-templates` to inspect the catalog. Use `--template-id` for an
explicit override when local knowledge supports a different source case.

## References

For column aliases, closure rules, and source-database suitability, read
`references/data-requirements.md` when the task involves unfamiliar data
schemas or global/national soil products.

Read `references/template-fallback.md` before using a bundled ecosystem
template or transferring the selected coefficients into an EcoSIM input.
