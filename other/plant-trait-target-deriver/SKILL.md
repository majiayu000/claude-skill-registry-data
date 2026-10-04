---
name: plant-trait-target-deriver
description: Use this skill when you need to derive, from web-sourced evidence, typical values for a named plant's annual GPP, LAI, specific LAI or specific leaf area, Rubisco Vcmax at 25oC, Jmax at 25oC, root-to-shoot ratio, rooting depth, leaf protein nitrogen, and leaf chlorophyll nitrogen.
---

# Plant Trait Target Deriver

## Use When

Use this skill when the user gives a plant name such as `Limber Pine`, `maize`, or `switchgrass` and wants a compact trait summary with defensible typical values.

## Target outputs

Derive typical values for:

- annual `GPP`
- `LAI`
- specific `LAI` or specific leaf area
- Rubisco `Vcmax` at 25oC
- `Jmax` at 25oC
- root-to-shoot ratio
- rooting depth
- leaf protein nitrogen concentration
- leaf chlorophyll nitrogen concentration

## Output expectations

Return a compact table or JSON object with:

- `plant_name`
- `accepted_scientific_name`
- `growth_form`
- one row per target trait
- `typical_value`
- `units`
- `provenance`
  - `species-sourced`
  - `genus-inferred`
  - `functional-type-inferred`
  - `no-defensible-estimate`
- `rationale`
- `source_links`

## Required behavior

1. Resolve the accepted scientific name first.
2. Determine the growth form:
   - tree
   - shrub
   - grass
   - crop grass
   - forb/herb
3. Search the web using primary and peer-reviewed sources.
4. Prefer species-level values.
5. If species-level values are unavailable, fall back in order:
   - same species in a closely related study system
   - same genus
   - same functional type
6. Label the provenance explicitly.
7. Never present a guessed value as directly measured.

## Unit conventions

Use these default units unless the user requests otherwise:

- annual `GPP`: `gC m-2 yr-1`
- `LAI`: `m2 leaf m-2 ground`
- specific `LAI` / specific leaf area: `m2 gC-1`
  - this is the preferred EcoSIM-facing unit
  - if source values use dry-mass units such as `m2 kg-1 DW` or `cm2 g-1 DW`, convert to `m2 gC-1` only when a defensible carbon fraction is available
  - if conversion is not defensible, report the source value separately and state that the EcoSIM-unit conversion is unresolved
- `Vcmax25`: `umol m-2 s-1`
- `Jmax25`: `umol m-2 s-1`
- root-to-shoot ratio: `kg root kg-1 shoot` or unitless mass ratio
- rooting depth: `m`
- leaf protein nitrogen concentration: `g N g-1 leaf` or `mg N g-1 leaf`
- leaf chlorophyll nitrogen concentration: `g N g-1 leaf` or equivalent chlorophyll-N fraction

If a source reports nitrogen on an area basis rather than mass basis, preserve the source unit unless a clean conversion is possible from the same source.

## Search strategy

Before doing substantial work, read [references/trait_derivation_guide.md](references/trait_derivation_guide.md).

Suggested sequence:

1. Taxonomy and growth form:
   - Kew POWO
   - USDA or species-profile sources
2. Productivity and canopy structure:
   - flux, forestry, crop, or ecological studies
3. Photosynthetic traits:
   - peer-reviewed gas-exchange or trait papers
4. Rooting traits:
   - species reviews, crop references, root trait papers
5. Nitrogen allocation traits:
   - leaf economics or crop physiology papers

## Trait-specific guidance

- `GPP`
  - Prefer site- or ecosystem-specific annual ranges for the target species or strongly species-dominated stands.
  - If only NPP or biomass increment is available, do not silently convert to GPP without a defensible method.

- `LAI`
  - Prefer field studies, flux-site metadata, crop handbooks, or forest canopy studies.

- specific `LAI` / SLA
  - Treat this as specific leaf area unless the user clearly means something else.
  - State the interpretation explicitly.
  - Prefer the final reported value in `m2 gC-1`.

- `Vcmax25` and `Jmax25`
  - Prefer values already standardized to 25oC.
  - If a paper reports temperature-response parameters rather than `Vcmax25`/`Jmax25`, do not back-calculate unless the paper provides the needed model clearly.

- root-to-shoot ratio
  - Prefer whole-plant or stand-level biomass allocation studies.

- rooting depth
  - Prefer effective or typical maximum rooting depth from species or crop references.
  - Distinguish between observed depth and model-assumed depth when possible.

- leaf protein nitrogen
  - Accept direct protein-N measurements.
  - If only total leaf N is available, do not relabel it as protein N unless the source distinguishes the fraction.

- leaf chlorophyll nitrogen
  - Prefer explicit chlorophyll-N or nitrogen-allocation measurements.
  - If only chlorophyll concentration is reported without nitrogen partitioning, do not convert unless a cited relationship supports it.

## Deliverable format

Prefer a flat table with these columns:

- `trait`
- `value`
- `units`
- `provenance`
- `source`
- `notes`

If the user asks for machine-readable output, emit JSON using the schema in [references/trait_output_schema.md](references/trait_output_schema.md).

## Notes

- This skill is intentionally narrow and should not attempt to derive the entire EcoSIM parameter set.
- Be conservative with `Vcmax25`, `Jmax25`, protein N, and chlorophyll N because these are often study-specific.
- Use exact source links in the final answer whenever web evidence is used.
