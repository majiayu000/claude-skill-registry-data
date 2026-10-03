---
name: r-package-champ-usage
description: Use when when you have raw methylation array data (450K or EPIC format) in .idat files or as a beta-valued matrix and need to conduct a complete analysis pipeline including data import, quality filtering, normalization, batch effect correction, DMR detection, or gene set enrichment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3204
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_3674
  tools:
  - ChAMP
  - ChAMPdata
  - minfi
  - Bumphunter
  - DMRcate
  - FEM
derived_from:
- doi: 10.1093/bioinformatics/btx513
  title: champ
evidence_spans:
- ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_champ
    doi: 10.1093/bioinformatics/btx513
    title: champ
  dedup_kept_from: coll_champ
schema_version: 0.2.0
---

# R package ChAMP usage

## Summary

ChAMP is an R package for comprehensive DNA methylation array analysis, supporting HumanMethylation450 (450K) and EPIC array types from data loading through gene set enrichment analysis. Use this skill when you have .idat files or beta-valued methylation matrices and need to perform quality control, normalization, batch correction, and downstream statistical analysis.

## When to use

When you have raw methylation array data (450K or EPIC format) in .idat files or as a beta-valued matrix and need to conduct a complete analysis pipeline including data import, quality filtering, normalization, batch effect correction, DMR detection, or gene set enrichment. Specifically use champ.load() when you need to verify pre-filter probe counts (485,512 for 450K arrays, 867,531 for EPIC arrays) before applying quality-based filtering.

## When NOT to use

- Input data is already a fully normalized and filtered feature table from another pipeline (e.g., already processed by minfi, RnBeads, or IMA); ChAMP assumes raw or minimally processed .idat or beta matrix input.
- You are analyzing non-array methylation data (e.g., WGBS, targeted bisulfite sequencing) — ChAMP is designed specifically for Illumina beadarray platforms (450K and EPIC).
- Your data contains fewer probes than expected or is from an unsupported array type (e.g., mouse arrays require ChAMPdata to be installed separately).

## Inputs

- .idat files (raw methylation array data for 450K or EPIC arrays)
- beta-valued matrix (methylation β-values)
- sample metadata and phenotype information

## Outputs

- Filtered and normalized methylation matrix (probe × sample)
- Quality control plots and reports
- Batch-corrected methylation data
- DMR detection results
- Gene set enrichment analysis results

## How to apply

Install ChAMP (version ≥2.29.1) along with ChAMPdata (≥2.23.1) from GitHub or Bioconductor. Load your methylation data using champ.load() or champ.import() functions, specifying the array type (450K or EPIC). Verify pre-filter probe counts match expected values for your array type. Apply quality control using ChAMP's QC functions, then proceed through the analysis pipeline: choose a Type-2 probe correction method (SWAN, PBC, or default BMIQ), apply Functional Normalization if needed, correct batch effects using SVD inspection and ComBat correction, adjust for cell-type heterogeneity via RefbaseEWAS if applicable, and finally perform DMR detection (Probe Lasso, Bumphunter, or DMRcate) or gene set enrichment analysis. The modular design allows selection of methods appropriate to your study design.

## Related tools

- **ChAMP** (Primary R package for complete DNA methylation array analysis pipeline, including data loading, QC, normalization, batch correction, and DMR detection) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Data package containing CpG-probe manifests and test datasets (450K, EPIC V1, EPIC V2, mouse arrays); required dependency for ChAMP) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (Alternative/complementary package offering Functional Normalization method; available within ChAMP workflow)
- **Bumphunter** (DMR detection method available in ChAMP alongside Probe Lasso and DMRcate)
- **DMRcate** (DMR detection method available in ChAMP for identifying Differentially Methylated Regions)
- **FEM** (Gene module inference package integrated in ChAMP version 2.29.1+)

## Examples

```
library(ChAMP); champ.load(method='ChAMP', arraytype='450K'); # or arraytype='EPIC' for EPIC arrays
```

## Evaluation signals

- Pre-filter probe counts match expected values: 485,512 probes for 450K arrays and 867,531 probes for EPIC arrays reported by champ.load() before any quality-based filtering
- Quality control plots show expected distribution patterns (e.g., density plots, box plots) with no systematic technical artifacts or sample outliers requiring removal
- Batch effect visualization via SVD method shows substantial variance explained by known batch covariates; ComBat correction reduces this variance in subsequent PCA/SVD plots
- DMR detection output includes valid genomic coordinates, effect sizes, and p-values with appropriate multiple-testing correction applied
- Gene set enrichment results (GSEA) show interpretable pathway associations with nominal p-values and false discovery rate (FDR) adjusted values

## Limitations

- ChAMP development version on GitHub is under intensive modification and may be unstable; formally released versions are available on Bioconductor and are recommended for production analyses
- Type-2 probe correction methods (SWAN, PBC, BMIQ) have different assumptions and performance characteristics; BMIQ is default but SWAN or PBC may be more appropriate depending on array design and sample composition
- Cell-type heterogeneity adjustment via RefbaseEWAS assumes availability of reference cell-type methylation profiles and may not be applicable to all tissue types or disease contexts
- DMR detection methods (Probe Lasso, Bumphunter, DMRcate) have different statistical assumptions and may produce discordant results; consensus approach recommended for high-confidence DMRs

## Evidence

- [other] The ChAMP loading functions should return 485,512 probes for 450K arrays and 867,531 probes for EPIC arrays before any quality-based filtering is applied.: "The ChAMP loading functions should return 485,512 probes for 450K arrays and 867,531 probes for EPIC arrays before any quality-based filtering"
- [intro] ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
- [intro] The ChAMP package is designed for the analysis of Illumina Methylation beadarray data (EPIC and 450k) and provides a pipeline that integrates currently available 450k and EPIC analysis methods: "The ChAMP package is designed for the analysis of Illumina Methylation beadarray data (EPIC and 450k) and provides a pipeline that integrates currently available 450k and EPIC analysis methods"
- [intro] Type-2 probe correction methods include SWAN, Peak Based Correction (PBC) and BMIQ (the default choice): "Type-2 probe correction methods include SWAN, Peak Based Correction (PBC) and BMIQ (the default choice)"
- [intro] for correction of multiple batch effects the ComBat method has been implemented: "for correction of multiple batch effects the ComBat method has been implemented"
- [readme] Current latest version: `2.29.1`, which support EPICv2, but it must be used along with ChAMPdata >= 2.23.1: "Current latest version: `2.29.1`, which support EPICv2, but it must be used along with ChAMPdata >= 2.23.1"
- [readme] This is the data pacakge supporting the Methylatin Analysis R package ChAMP, which must be installed in your R environment along with ChAMP.: "This is the data package supporting the Methylatin Analysis R package ChAMP, which must be installed in your R environment along with ChAMP"
- [readme] Note that this is NOT a proper release version ChAMP and under intensive modification and upgrade, the formally released one is on Bioconductor: "Note that this is NOT a proper release version ChAMP and under intensive modification and upgrade, the formally released one is on Bioconductor"
