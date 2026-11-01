---
name: lipid-candidate-matching
description: Use when you have peak-picked MS/MS data (e.g., from MZmine, XCMS, MS-DIAL, or Compound Discoverer) and need to identify lipid species present in your sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  - LipidMatch
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch
schema_version: 0.2.0
---

# lipid-candidate-matching

## Summary

Match experimental fragment m/z values from high-resolution tandem MS/MS data against in-silico fragmentation libraries to identify and rank lipid candidates. This skill enables annotation of lipidomics datasets by comparing observed ion patterns to simulated spectra from comprehensive lipid databases.

## When to use

Apply this skill when you have peak-picked MS/MS data (e.g., from MZmine, XCMS, MS-DIAL, or Compound Discoverer) and need to identify lipid species present in your sample. Use when working with Q-Exactive orbitrap, Agilent, Bruker, or SCIEX Q-TOF UHPLC-HRMS/MS instruments, or when performing direct infusion or imaging experiments. Do NOT use if your data originates from Waters instruments, which are not currently supported.

## When NOT to use

- Input data originates from Waters instruments (currently unsupported by LipidMatch)
- Raw, unprocessed MS data without prior peak picking step
- Analysis of non-lipid small molecules or metabolites (tool is lipid-specific)

## Inputs

- Peak-picked MS/MS dataset or experimental fragment m/z list (from MZmine, XCMS, MS-DIAL, or Compound Discoverer)
- In-silico fragmentation lipid library (.csv format or built-in LipidMatch library)
- Sample ionization mode and acquisition method parameters (targeted, ddMS2-topN, or AIF)

## Outputs

- Ranked lipid candidate list with matched m/z fragments and scoring metrics
- Annotated MS/MS dataset with assigned lipid identities
- Lipidomics feature table with lipid species annotations

## How to apply

First, obtain the experimental fragment m/z list from your peak-picked MS/MS dataset and prepare it in the format expected by LipidMatch (typically a tabular format with experimental m/z and intensity values). Load the LipidMatch software with the active in-silico fragmentation library (comprising over 500,000 lipid species across 60+ lipid types), or integrate a custom user-authored .csv lipid library if analyzing specialized lipid classes. Run the matching algorithm to compare each experimental m/z fragmentation pattern against the library's simulated m/z values. Inspect the ranked output candidate list, which prioritizes matches based on agreement between observed and predicted fragment patterns. Filter candidates using domain knowledge (e.g., retention time, ionization mode, expected lipid class) to narrow the final annotation set.

## Related tools

- **MZmine** (Peak picking and feature detection prior to lipid matching)
- **XCMS** (Peak picking and feature detection prior to lipid matching)
- **MS-DIAL** (Peak picking and feature detection prior to lipid matching)
- **Compound Discoverer** (Peak picking and feature detection prior to lipid matching)
- **LipidMatch** (Executes fragment m/z matching against in-silico lipid fragmentation libraries) — https://github.com/GarrettLab-UF/LipidMatch

## Evaluation signals

- At least one candidate from the built-in or custom library appears in the ranked output list with a matching score above background noise threshold
- Experimental fragment m/z values show ≤5 ppm mass accuracy when matched to predicted library fragments
- Top-ranked candidate lipid species is consistent with expected lipid class, retention time, and ionization polarity for the sample
- Custom library entries (if used) successfully appear as matching candidates after integration and library loading workflow
- Output candidate list is non-empty and ranked by match quality metric (e.g., fragment pattern similarity, mass error)

## Limitations

- LipidMatch does not currently support Waters instrument files or data formats
- Matching accuracy depends on the completeness and quality of the in-silico fragmentation library; novel or uncommon lipid species may not be represented
- Requires properly formatted, pre-processed peak-picked input; raw MS data cannot be used directly
- No changelog or version history documented, making reproducibility tracking difficult

## Evidence

- [readme] Fragment m/z matching methodology: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values using in-silico fragmentation libraries of over 500,000 lipid species across"
- [readme] Supported instrument platforms: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] Workflow modularity and peak picking integration: "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
- [readme] Custom library integration capability: "LipidMatch allows for facile integration of user generated libraries for unique applications"
- [readme] Waters instrument limitation: "The software does not currently support Waters files"
