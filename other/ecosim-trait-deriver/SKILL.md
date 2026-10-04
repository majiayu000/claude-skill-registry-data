---
name: ecosim-trait-deriver
description: Use this skill when deriving EcoSIM plant trait parameter recommendations for a named plant from web and online literature evidence, using a read-only `plant_trait.*.desc` file and the `ndlf43` tree block or `gr3s43` grass block as the starting archetype. Never edit or replace the `.desc` file.
---

# EcoSIM Trait Deriver

## Use When

Use this skill for EcoSIM trait derivation tasks where:

- the user gives a plant name such as `Limber Pine` or `maize`
- a local `plant_trait.*.desc` file is available as the EcoSIM template
- you need to derive a species-specific parameter set from web evidence rather than just copying template values

## What this skill does

- Parses the template `.desc` file into functional-type blocks
- Extracts normalized parameter rows from each template block
- Uses `ndlf43` as the default tree archetype
- Uses `gr3s43` as the default grass archetype
- Guides web- and online-literature-based derivation of trait values for a named plant
- Separates values into:
  - directly supported by sources
  - inferred from close biological evidence
  - left at template defaults when no defensible evidence exists

## Required behavior

Treat every `plant_trait.*.desc` file as a read-only reference. Parse and inspect
it, but never edit, overwrite, patch, or generate a replacement `.desc` file.
Apply approved parameter changes to `ecosim_pftpar_*.nc` through the
`ecosim-pftpar-editor` skill and `ParamEditor.py`.

When the user asks for traits for a named plant, do not treat the template `.desc` values as species truth.

Instead:

1. Identify whether the target plant should start from the tree archetype `ndlf43` or the grass archetype `gr3s43`.
2. Parse the template file with `scripts/extract_trait_profiles.py`.
3. Search both the web and online literature for plant-specific evidence.
4. Map the evidence onto EcoSIM trait codes.
5. Keep a clear distinction between:
   - observed or explicitly reported values
   - values inferred from authoritative descriptions
   - values retained from the template because evidence is missing

## Source priority

Use sources in this order whenever possible:

1. Official taxonomic or species-profile sources for identity and life form.
2. Official crop or forestry databases for ecology, growth form, phenology, and environmental tolerances.
3. Peer-reviewed papers and online literature sources for quantitative physiological, morphological, nutrient, and hydraulic trait values.
4. Reputable extension or botanic-garden sources only as a fallback.

Preferred source types:

- Trees:
  - USDA Forest Service species pages
  - Fire Effects Information System
  - Kew POWO for taxonomy and growth form
- Grasses and crops:
  - FAO ECOCROP
  - USDA sources
  - peer-reviewed crop physiology literature
- Cross-cutting plant traits:
  - TRY database metadata and linked literature
  - peer-reviewed trait papers
  - online journal articles, books, theses, and technical reports when they provide primary trait measurements or defensible synthesis values

## Literature search requirement

For quantitative trait derivation, do not stop at species profile pages if the trait is likely to be reported in the literature.

You should actively search online literature for traits such as:

- `VCMX`, `VOMX`, `ETMX`
- `SLA1`
- leaf N and P concentrations
- seed mass and seedling carbon allocation
- root depth, rooting pattern, and fine-root traits
- hydraulic or drought-response traits

Use species-level sources first. If species-level values are not available, fall back in this order:

1. congeneric species
2. closely related taxa with similar life form and climate niche
3. functional-type syntheses for the same growth form

When using non-species fallbacks, mark the trait as `inferred` rather than `sourced`.

## Web workflow

Before doing substantial web- or literature-based derivation work, read [references/web_trait_derivation.md](references/web_trait_derivation.md).

For a plant like `Limber Pine` or `maize`:

1. Resolve the accepted scientific name and broad life form.
2. Choose the starting archetype:
   - tree, woody conifer, woody broadleaf, shrub-like tree form -> start from `ndlf43`
   - grass, cereal, herbaceous monocot grass form -> start from `gr3s43`
3. Gather evidence for:
   - taxonomy and life history
   - climate and habitat
   - phenology
   - morphology
   - root traits
   - photosynthetic and nutrient traits
4. Search online literature specifically for quantitative traits that are not usually present in species profile pages.
5. Update only the traits that have support.
6. If evidence is qualitative rather than numeric, convert only when the mapping is defensible and explain the inference.
7. If no support is found, keep the template value and mark it as template-retained.

## Mapping guidance

Use the template as a scaffold, not as a source of truth.

- `PLANT CLASS INFORMATION`
  - derive from taxonomy, life form, lifespan, growth pattern, phenology, photoperiod, mycorrhizal status
- `PHOTOSYNTHETIC PROPERTIES`
  - prefer peer-reviewed physiology measurements from online papers, theses, technical reports, or synthesis datasets
  - if unavailable, only adjust high-level expectations such as slower evergreen conifer vs faster crop grass
- `OPTICAL PROPERTIES`
  - usually retain template unless a credible species- or functional-type source provides values
- `PHENOLOGICAL PROPERTIES`
  - use flowering time, leafout, senescence, chilling, and photoperiod evidence
- `MORPHOLOGICAL PROPERTIES`
  - use SLA, leaf shape, seed size, canopy architecture, clumping, standing biomass evidence
  - look for seed mass and SLA values in online floras, trait databases, and literature appendices
- `ROOT CHARACTERISTICS`
  - use rooting depth, woody vs non-woody roots, fine-root structure, mycorrhiza, hydraulic traits if available
  - prioritize literature and technical reports for depth, fine-root morphology, and hydraulic behavior
- `ROOT UPTAKE PARAMETERS`
  - usually infer from functional type or retain template unless species-specific uptake kinetics are available
- `WATER RELATIONS`
  - use drought tolerance and water-stress physiology when supported
- `ORGAN GROWTH YIELDS` and `ORGAN N AND P CONCENTRATIONS`
  - prefer peer-reviewed measurements or defensible online literature values; otherwise retain template and label as such

## Command

```bash
python3 .agents/skills/ecosim-trait-deriver/scripts/extract_trait_profiles.py /absolute/path/to/plant_trait.1930.desc
```

## Output shape

The parser script returns JSON with:

- `source_file`
- `available_functional_types`
- `tree_profile`
- `grass_profile`

These are the template anchor profiles, not the final derived species profile.

Each anchor profile contains:

- `functional_type_code`
- `plant_name`
- `koppen_climate_info`
- `trait_count`
- `traits_by_code`
- `traits_by_section`

When a trait code appears more than once in a block, `traits_by_code[CODE]` becomes a list in file order instead of dropping later entries.

## Expected final deliverable

When the user asks for derivation for a plant name, produce:

- the chosen anchor block: `ndlf43` or `gr3s43`
- the accepted scientific name
- a derived trait table or JSON object
- per-trait provenance labels:
  - `sourced`
  - `inferred`
  - `template-retained`
- source links for the evidence used
- source links for the evidence used, including online literature when applicable

If the user asks for a file output, emit CSV or JSON under `result/`. Do not emit
or modify a `.desc` file; use the NetCDF editor workflow to apply changes.

## Notes

- `ndlf43` is the default tree reference block.
- `gr3s43` is the default grass reference block.
- The `.desc` file is a read-only template.
- If the plant does not clearly fit tree or grass, say so and choose the nearest valid EcoSIM archetype explicitly.
- If either template block is missing, fail clearly instead of guessing.
