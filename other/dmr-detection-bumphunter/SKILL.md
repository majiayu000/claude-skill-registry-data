---
name: dmr-detection-bumphunter
description: Use when you have preprocessed, normalized beta-value matrices from EPIC or 450k methylation arrays with at least two sample groups (case/control, treatment/untreated, or similar contrasts) and seek to identify regions of coordinated differential methylation rather than individual CpG sites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0654
  tools:
  - Bumphunter
  - ChAMP
  - ChAMPdata
  - minfi
derived_from:
- doi: 10.1093/bioinformatics/btx513
  title: champ
evidence_spans:
- previous DMR detection functions Bumphunter and DMRcate
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

# dmr-detection-bumphunter

## Summary

Detect differentially methylated regions (DMRs) in EPIC or 450k methylation array data using the bumphunter-based method implemented in ChAMP. This skill identifies contiguous genomic regions with coordinated methylation differences between sample groups, filtering out single-CpG or low-complexity signals.

## When to use

Apply this skill when you have preprocessed, normalized beta-value matrices from EPIC or 450k methylation arrays with at least two sample groups (case/control, treatment/untreated, or similar contrasts) and seek to identify regions of coordinated differential methylation rather than individual CpG sites. Use when you expect DMRs to contain multiple CpGs (≥3) and want bumphunter's spatial clustering approach rather than probe-level detection.

## When NOT to use

- Input is already a list of called CpG-level differential methylation results; use DMR detection on raw or minimally processed beta values instead.
- Sample groups are not well-defined or biological replicates are absent; bumphunter requires sufficient statistical power within groups.
- Data contains strong batch effects or confounding variables not corrected during preprocessing; apply ComBat or RefbaseEWAS adjustment before DMR calling.

## Inputs

- EPIC or 450k methylation array beta-value matrix (samples × CpG sites)
- Sample phenotype/group labels (case/control or multi-group contrast)
- Preprocessed, normalized methylation data (quality control and batch correction applied)

## Outputs

- DMR object containing genomic coordinates, CpG membership, and statistics for each detected region
- DMR count and summary table with region-level p-values or test statistics
- Annotated DMR list with gene associations

## How to apply

Load your EPIC or 450k methylation dataset (from .idat files or preprocessed beta-value matrix) into R and ensure it is normalized using one of ChAMP's supported methods (SWAN, PBC, BMIQ, or Functional Normalization from minfi). Call champ.DMR() function specifying the bumphunter-based detection method. The function will perform spatial clustering of CpGs and apply a minimum CpG threshold (typically ≥3 CpGs per region) to filter out isolated signals. Extract and count DMRs from the output; expect fewer regions than simulated DMRs due to filtering of single-to-dual-CpG signals. Verify DMR count is reasonable for your data scale and biological context (e.g., ~4700 DMRs for EPIC simulation data with 5000+ simulated regions indicates proper filtering).

## Related tools

- **ChAMP** (Primary R package providing champ.DMR() function and bumphunter-based DMR detection pipeline) — https://github.com/YuanTian1991/ChAMP
- **Bumphunter** (Underlying spatial clustering algorithm for identifying contiguous DMRs)
- **ChAMPdata** (Companion data package providing CpG annotations, array manifests, and example datasets (EPICSimData)) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (Provides Functional Normalization method used in preprocessing before DMR detection)

## Examples

```
library(ChAMP); data(EPICSimData); result <- champ.DMR(beta, pheno, method='bumphunter'); print(length(result$DMR))
```

## Evaluation signals

- DMR count should be lower than the number of simulated or expected regions, reflecting filtering of low-complexity (1–2 CpG) signals; for EPIC simulation data, expect ~4700–4800 called DMRs from ~5000 simulated regions.
- Each detected DMR should contain ≥3 CpGs; verify no single-CpG or dual-CpG regions are included in output.
- DMR genomic coordinates should be non-overlapping and fall within expected chromosomal regions; check for contiguity and absence of intergenic gaps.
- DMR statistics (p-value, effect size) should show statistical and biological consistency with the underlying CpG-level beta-value differences.
- Reproducibility check: re-running champ.DMR() on the same input should yield identical DMR calls and counts.

## Limitations

- DMRs with only 1–2 CpGs are excluded by default; if you require detection of very small clustered regions, this tool is inappropriate.
- Bumphunter method is sensitive to spatial proximity assumptions; sparse CpG arrays or non-contiguous probe designs may yield fragmented or spurious regions.
- Performance depends on upstream preprocessing and normalization quality; inadequate batch correction or poor quality control can inflate or deflate DMR counts.
- No built-in multiple testing correction at the region level is described; users must apply downstream FDR or Bonferroni adjustment based on the number of tested regions.

## Evidence

- [other] The EPIC simulation dataset contains fewer than 5000 DMRs (approximately 4700+) because some simulated DMRs contain only 1-2 CpGs, which are not regarded as DMRs in champ.DMR() function.: "approximately 4700+) because some simulated DMRs contain only 1-2 CpGs, which are not regarded as DMRs in champ.DMR() function"
- [intro] For the identification of Differentially Methylated Regions (DMRs), ChAMP offers the new Probe Lasso method, in addition to previous DMR detection functions Bumphunter and DMRcate: "For the identification of Differentially Methylated Regions (DMRs), ChAMP offers the new Probe Lasso method, in addition to previous DMR detection functions Bumphunter and DMRcate"
- [intro] ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
- [intro] The ChAMP package is designed for the analysis of Illumina Methylation beadarray data (EPIC and 450k) and provides a pipeline that integrates currently available 450k and EPIC analysis methods: "The ChAMP package is designed for the analysis of Illumina Methylation beadarray data (EPIC and 450k) and provides a pipeline that integrates currently available 450k and EPIC analysis methods"
- [intro] For the EPIC Simulation Data Set, user may use following code to load it: data(EPICSimData): "For the EPIC Simulation Data Set, user may use following code to load it: data(EPICSimData)"
