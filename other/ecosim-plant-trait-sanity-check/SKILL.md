---
name: ecosim-plant-trait-sanity-check
description: Read-only sanity-check of EcoSIM plant_trait.*.desc parameter values for the first grid. Use when validating plant trait description files, enforcing clean C3/C4 physiological parameterization, reviewing photosynthetic kinetics, active leaf/root protein allocation, and root hydraulics such as RSRR, RVSR, and ARSRA, or checking ranges, units, and woody/herbaceous block consistency before running EcoSIM. Never edit or replace the `.desc` file.
---

# EcoSIM Plant Trait Sanity Check

## Overview

Use this skill to sanity-check EcoSIM `plant_trait.*.desc` files. These files are
strictly read-only: never edit, overwrite, patch, or generate a replacement
`.desc` file. Each `PLANT traits for FUNCTIONAL TYPE` block represents one plant,
and the default check is intentionally confined to the first grid only:
`NY=1, NX=1`. All active plant blocks at that grid are checked.

The check has two layers:

- deterministic file checks for malformed values, units, ranges, and block consistency
- web-informed ecological checks using species, genus, or plant-functional-type evidence gathered during the task

Always back parameter-value judgments for `plant_trait.*.desc` files with web search unless the user explicitly asks for an offline/local-only check. Treat deterministic checker results as a first pass, not as sufficient evidence that ecological or physiological parameter values are correct.

## Workflow

1. Locate the target `plant_trait.*.desc` file. If the user gives no path, prefer a local path they recently mentioned, then search under `data/`, then under the repository.
2. For calibration or run readiness, run the deterministic checker in strict physiology mode:

```bash
python3 .agents/skills/ecosim-plant-trait-sanity-check/scripts/check_plant_trait_desc.py /absolute/path/to/plant_trait.1930.desc --strict-physiology
```

Omit `--strict-physiology` only for an exploratory review where physiological findings should remain warnings. Strict mode promotes physiological-consistency warnings to errors and returns a nonzero status.

3. Keep the default grid scope unless the user explicitly asks for another grid. The default is equivalent to:

```bash
python3 .agents/skills/ecosim-plant-trait-sanity-check/scripts/check_plant_trait_desc.py /absolute/path/to/plant_trait.1930.desc --ny 1 --nx 1
```

4. Use web search to gather trait evidence for each first-grid plant block. Read [references/web_evidence.md](references/web_evidence.md), then search for the plant name, likely taxon, or functional type plus trait terms. For `ndlf35`, `woak35`, US-Me2, or US-xSP/SOAP work, also read [references/pft_case_notes.md](references/pft_case_notes.md).
5. Convert the evidence into EcoSIM units and save a temporary evidence JSON file. Use species-level evidence when available; otherwise use genus, family, or functional-type evidence and mark that evidence level.
6. Re-run the checker with the evidence file:

```bash
python3 .agents/skills/ecosim-plant-trait-sanity-check/scripts/check_plant_trait_desc.py /absolute/path/to/plant_trait.1930.desc --web-evidence /absolute/path/to/web_evidence.json
```

7. Report findings by severity. Lead with `ERROR` findings, then `WARN` findings, and include the plant code, grid tuple, parameter name, source line, and web source when applicable.
8. If there are no findings, state that the first-grid plant blocks passed both deterministic and web-informed checks and mention how many plants and parameters were inspected.

## What Is Checked

The checker validates the plant blocks at the selected grid for:

- required EcoSIM trait sections
- parseable finite numeric values in numeric sections
- fraction variables within `[0, 1]`
- positive rates, capacities, dimensions, uptake parameters, resistance terms, and nutrient ratios
- `CLASS` as four inclination fractions that sum to one
- optical albedo plus transmission not exceeding one
- pathway-specific Rubisco `Kc`, `Ko`, carboxylation:oxygenation turnover ratio, and implied CO2/O2 specificity
- Rubisco and PEPC fractions of total leaf N implied by their allocations within the N/P-limited total leaf-protein pool
- leaf and root protein C supported jointly by N and P in active structural biomass, with only active root biomass used for woody PFTs
- C4 protein-normalized `Vpmax:Vcmax` and a lower-priority, model-formulation-sensitive C3/C4 `Jmax:Vcmax` diagnostic
- pathway-specific `FCO2`, C4 mesophyll chlorophyll partitioning, and PAR/shortwave absorptance
- total photosynthetic protein allocation without double-counting the shared leaf-protein pool
- `SLA1` against explicit species- or site-specific web evidence, without using SLA to infer photosynthetic kinetics
- `ANGSH = 0` for plant forms without petiole or sheath tissue, including conifer, lichen, and moss PFTs
- osmotic potential sign and standing dead biomass sign
- growth yield bounds
- N and P concentration magnitudes
- class-information conventions, including that annual plants are treated as evergreen in EcoSIM
- woody versus herbaceous root trait consistency
- cross-parameter checks such as `PhiMIN <= PhiMAX` and fine-root radius not exceeding primary-root radius
- `RSRR` radial root resistivity, its implied fully wetted conductivity, and its interaction with soil drying and total root resistance
- literal `RVSR` conduit radius, conifer tracheid anatomy, conduit geometry relative to `RRAD2M`, and `ARSRA` resistance correction

Read [references/sanity_rules.md](references/sanity_rules.md) before expanding the checker or interpreting a borderline warning. Read [references/web_evidence.md](references/web_evidence.md) before making web-informed trait comparisons. Use [references/pft_case_notes.md](references/pft_case_notes.md) for retained project evidence and interpretation caveats for previously studied PFT/site combinations.

## Web-Informed Evidence

The script does not browse by itself. Codex must do the web search, evaluate sources, convert values into EcoSIM units, and provide the evidence as JSON. This keeps the check reproducible and prevents untraceable web-derived warnings.

Use this JSON shape:

```json
{
  "plants": [
    {
      "pft_code": "woat35",
      "nz": 3,
      "ny": 1,
      "nx": 1,
      "taxon": "Avena fatua",
      "numeric_ranges": [
        {
          "variable": "RUBP",
          "min": 0.05,
          "max": 0.35,
          "unit": "gC rubisco gC protein-1",
          "source": "literature-derived protein-allocation range",
          "url": "https://example.org/source",
          "evidence_level": "species",
          "conversion_note": "Range must match EcoSIM's total-leaf-protein basis."
        }
      ],
      "categorical_expectations": [
        {
          "variable": "ICTYP",
          "contains": "C3",
          "source": "USDA/NRCS or species profile",
          "url": "https://example.org/source",
          "evidence_level": "species"
        }
      ]
    }
  ]
}
```

Web evidence findings default to `WARN` because literature and trait database ranges vary with species, site, phenology, and measurement protocol. Use `severity: "ERROR"` in the evidence JSON only when a value is unequivocally impossible or contradicts a required categorical identity. Do not use external deciduous foliage descriptions to override the EcoSIM convention that annual plants are represented as evergreen in `IWTYP`.

For photosynthetic-property checks, interpret `RUBP`, `PEPC`, and `CHL` as fractions of the same total leaf-protein pool. Derive that pool from the smaller of the N- and P-supported amounts in active leaf structural biomass. All leaf structure is active; all non-tree root structure is active; for trees, apply root protein relationships only to active structural root biomass and exclude lignified heartwood. Separate `CNRTLIG` and `CPRTLIG` trait inputs are not required. Check `SLA1` only as an independently evidenced morphological trait. Do not use `SLA1` to back-calculate leaf-area `Vcmax`, `Jmax`, or other photosynthetic capacities unless the model mapping and all required conversions are explicitly supported.

Interpret `RVSR` as the literal arithmetic mean lumen radius of root water conduits: tracheids for conifers and vessel elements for angiosperms. Do not use an effective hydraulic radius or tune `RVSR` to absorb pit and end-wall resistance; use `ARSRA` for that correction. Convert published conduit diameters to radius in meters before adding web evidence.

Interpret `RSRR` as radial root resistivity per unit root surface area in `MPa h m-1`, not as conductivity. Convert it to the fully wetted intrinsic radial conductivity with `k_radial = 1/(3600*RSRR)` in `m s-1 MPa-1`. High `RSRR` means low radial conductivity. Review it separately from `RVSR` and `ARSRA`, which control axial transport, and remember that EcoSIM further increases radial resistance as the soil micropore water fraction declines.

Treat every root-resistance equation and parameter interpretation as EcoSIM-code-version dependent. Before diagnosing or transferring `RSRR`, `RVSR`, or `ARSRA`, verify the active model revision and record its commit or version when available. Recheck radial-resistance assembly, soil-moisture modifiers, conduit-count geometry, and axial-resistance scaling in that revision; the formulas documented here describe the inspected implementation and are not guaranteed across versions.

## Parser Notes

The parser treats each block header as a plant identity record:

```text
PLANT traits for FUNCTIONAL TYPE (NZ,NY,NX)= <NZ> <NY> <NX> <pft_code>
```

Parameter names are not globally unique, so preserve file order and section context when discussing findings.

Trait descriptions sometimes contain colons, such as `Leaf length:width ratio`; split parameter values at the final colon in a row.

## Output Options

Use Markdown output for human review:

```bash
python3 .agents/skills/ecosim-plant-trait-sanity-check/scripts/check_plant_trait_desc.py /absolute/path/to/plant_trait.1930.desc
```

Enforce physiological consistency for calibration and run readiness. The model-formulation-sensitive `Jmax:Vcmax` diagnostic remains a warning:

```bash
python3 .agents/skills/ecosim-plant-trait-sanity-check/scripts/check_plant_trait_desc.py /absolute/path/to/plant_trait.1930.desc --strict-physiology
```

Use JSON output for automated pipelines:

```bash
python3 .agents/skills/ecosim-plant-trait-sanity-check/scripts/check_plant_trait_desc.py /absolute/path/to/plant_trait.1930.desc --json
```

Use web evidence in either Markdown or JSON mode:

```bash
python3 .agents/skills/ecosim-plant-trait-sanity-check/scripts/check_plant_trait_desc.py /absolute/path/to/plant_trait.1930.desc --web-evidence /absolute/path/to/web_evidence.json --json
```

The script returns a nonzero status when `ERROR` findings are present or when no blocks match the requested grid. With `--strict-physiology`, physiological-consistency warnings are promoted to `ERROR` except the model-formulation-sensitive `Jmax:Vcmax` diagnostic, which remains a lower-priority `WARN`. Unrelated ecological warnings also remain warnings.

## Reporting Guidance

Never edit the trait file. This skill is a diagnostic pass. Report recommended
corrections and, when the user asks to apply them, update the corresponding
`ecosim_pftpar_*.nc` file through the `ecosim-pftpar-editor` skill and
`ParamEditor.py`.

When summarizing results, make clear that the check is scoped to the first grid by default, not the full file. If repeated grid columns exist, say how many total blocks were present and how many first-grid plant blocks were inspected.

Always report each checked plant's `RSRR` and implied fully wetted `k_radial`, even when the value passes the deterministic screen. For a high `RSRR` warning, recommend a sensitivity test and diagnose whether radial resistance dominates total root resistance during moist periods before proposing an edit.

For root-hydraulic findings, report the EcoSIM source version or commit used to verify the equations. If the source revision is unavailable, label equation-level conclusions as version-unverified.

When trait plausibility is being inferred from EcoSIM output, condition GPP, LAI, height, biomass, and mortality judgments on cohort age and initialization. A cohort emerging from seed in the simulation must be compared with seedlings or young stands, not the mature AmeriFlux stand observed at the same location. Treat `WTSTDI` as an initial-condition pool tied to the simulation start date and disturbance history, not as an intrinsic PFT trait.
