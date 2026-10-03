---
name: hmdb-formula-sampling
description: Use when when you need to create in silico LC-MS/MS experiments with
  diverse chemical backgrounds for testing fragmentation strategies or acquisition
  controllers, and you want the chemical diversity to reflect real metabolomic samples.
  Use this when you have a target m/z range (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - ViMMS
  - ViMMS (Virtual Metabolomics Mass Spectrometer)
  - HMDB (Human Metabolome Database)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a flexible
  and modular framework designed to simulate fragmentation strategies'
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a comprehensive
  and modular framework for the simulation of fragmentation strategies'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_vimms_cq
    doi: 10.21105/joss.03990
    title: vimms
  dedup_kept_from: coll_vimms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.03990
  all_source_dois:
  - 10.21105/joss.03990
  - 10.1021/acs.analchem.0c03895
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# HMDB Formula Sampling

## Summary

Sample diverse molecular formulas from the Human Metabolome Database (HMDB) within a specified m/z range to generate chemically realistic mixtures for LC-MS simulation. This skill enables rapid prototyping of MS acquisition strategies on representative chemical backgrounds without requiring real samples.

## When to use

When you need to create in silico LC-MS/MS experiments with diverse chemical backgrounds for testing fragmentation strategies or acquisition controllers, and you want the chemical diversity to reflect real metabolomic samples. Use this when you have a target m/z range (e.g., 100–1000) and want to ensure your simulated experiment includes realistic chemical complexity before validating on real instruments.

## When NOT to use

- When you need targeted analysis of specific metabolites (e.g., known disease biomarkers); HMDB sampling produces unbiased chemical diversity, not a curated set.
- When you require only a small, highly curated chemical background; HMDB sampling returns tens of thousands of formulas, which may add unnecessary computational overhead for simple validation studies.
- When you need to match a specific real sample's chemical composition; sampling from HMDB does not preserve the actual relative abundances or co-occurrence patterns of a measured sample.

## Inputs

- m/z range boundaries (min_mz, max_mz as floats)
- HMDB database access (local or remote)
- DatabaseFormulaSampler instance (ViMMS)

## Outputs

- List of sampled molecular formulas (unique, stratified across m/z range)
- Chemical mixture object (ChemicalMixtureCreator output)
- Chemical objects compatible with IndependentMassSpectrometer

## How to apply

Initialize a DatabaseFormulaSampler configured to retrieve molecular formulas from the HMDB database, specifying your m/z range boundaries (e.g., min_mz=100, max_mz=1000). The sampler will return a large set of unique molecular formulas stratified across that range. Pass these formulas to a ChemicalMixtureCreator with ms_levels=1 to generate MS1-only chemical mixtures, then feed the resulting Chemical objects into an IndependentMassSpectrometer instance (configured for your desired ionization polarity). The sampler successfully retrieved 73,822 unique HMDB formulas in the 100–1000 m/z range in the source study, providing sufficient chemical diversity for realistic full-scan simulations. Success is confirmed when the returned formula set spans the requested m/z range without gaps and the resulting chemical mixture can be instantiated without schema errors.

## Related tools

- **ViMMS (Virtual Metabolomics Mass Spectrometer)** (Framework providing DatabaseFormulaSampler, ChemicalMixtureCreator, IndependentMassSpectrometer, and Environment classes for chemical generation and LC-MS simulation) — https://github.com/glasgowcompbio/vimms
- **HMDB (Human Metabolome Database)** (Source database of molecular formulas and compound metadata used by DatabaseFormulaSampler)

## Examples

```
from vimms.ChemicalSampler import DatabaseFormulaSampler; sampler = DatabaseFormulaSampler(min_mz=100, max_mz=1000); formulas = sampler.sample()
```

## Evaluation signals

- Number of unique formulas returned matches expected cardinality (~73,822 for m/z 100–1000)
- All sampled formulas fall within the specified m/z bounds (min_mz ≤ each formula m/z ≤ max_mz)
- No duplicate formulas in the returned set
- ChemicalMixtureCreator successfully instantiates with sampled formulas without schema or type errors
- Resulting Chemical objects are compatible with IndependentMassSpectrometer (match expected attribute schema)

## Limitations

- HMDB sampling is unbiased and does not reflect the actual relative abundances or co-occurrence patterns observed in real biological samples, potentially resulting in artificial peak patterns.
- The diversity and size of the sampled set depends on HMDB database version and maintenance status; outdated or incomplete HMDB snapshots may yield fewer formulas or miss recently discovered metabolites.
- Sampling is performed at the formula level only; no structural stereoisomers or ionization adducts are distinguished during sampling, which may under-represent the true chromatographic and MS complexity of real samples.

## Evidence

- [other] A DatabaseFormulaSampler successfully sampled 73,822 unique formulas from the HMDB database within the m/z range 100–1000, enabling generation of realistic chemical mixtures for MS1-only simulation.: "A DatabaseFormulaSampler successfully sampled 73,822 unique formulas from the HMDB database within the m/z range 100–1000"
- [other] Chemicals can be sampled from databases such as HMDB or from specific distributions: "Chemicals can be sampled from databases such as HMDB or from specific distributions"
- [other] Initialize a DatabaseFormulaSampler to retrieve chemical formulas from the HMDB database.: "Initialize a DatabaseFormulaSampler to retrieve chemical formulas from the HMDB database"
- [other] Use ChemicalMixtureCreator to generate a chemical mixture with ms_levels=1 (MS1 only).: "Use ChemicalMixtureCreator to generate a chemical mixture with ms_levels=1 (MS1 only)"
- [results] hmdb_compounds.p - Human Metabolome Database metabolite database extracted for simulation: "Human Metabolome Database metabolite database extracted for simulation"
