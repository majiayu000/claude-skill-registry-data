---
name: 2d-tic-preprocessing
description: Use when when you have raw GCxGC-MS data imported from NetCDF into a
  2D-TIC chromatogram object and need to remove chemical and instrumental noise (column
  bleeding, baseline drift, detector contamination) to reveal metabolite differences
  between sample groups for downstream multiway PCA or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - RGCxGC
  - R
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1016/j.microc.2020.104830
  title: RGCxGC
- doi: 10.1371/journal.pntd.0006215
  title: ''
evidence_spans:
- The goal of RGCxGC is to provide an easy-to-use platform to analyze two-dimensional
  gas chromatography data.
- This is the vignette to explain the implementation of RGCxGC package.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rgcxgc_cq
    doi: 10.1016/j.microc.2020.104830
    title: RGCxGC
  dedup_kept_from: coll_rgcxgc_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.microc.2020.104830
  all_source_dois:
  - 10.1016/j.microc.2020.104830
  - 10.1371/journal.pntd.0006215
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# 2D-TIC preprocessing

## Summary

A multi-stage preprocessing pipeline for two-dimensional total intensity chromatogram (2D-TIC) objects that applies smoothing, baseline correction, and peak alignment to remove instrumental noise and artifacts from GCxGC-MS data before multivariate analysis.

## When to use

When you have raw GCxGC-MS data imported from NetCDF into a 2D-TIC chromatogram object and need to remove chemical and instrumental noise (column bleeding, baseline drift, detector contamination) to reveal metabolite differences between sample groups for downstream multiway PCA or supervised classification.

## When NOT to use

- Input data is already a processed feature matrix or peak table (preprocessing is only applicable to raw chromatogram objects)
- The chromatogram data is from a non-GCxGC platform (e.g., HPLC, UPLC) where 2D alignment may not be appropriate
- Baseline distortion is minimal or the analytical goal is to preserve absolute intensity values for quantification rather than pattern discovery

## Inputs

- 2D-TIC chromatogram object (from read_chrom applied to NetCDF raw data)
- Reference chromatogram (for 2DCOW alignment)

## Outputs

- Smoothed 2D-TIC chromatogram object
- Baseline-corrected 2D-TIC chromatogram object
- Peak-aligned 2D-TIC chromatogram object
- Joined multi-sample chromatogram R object ready for MPCA

## How to apply

Load the 2D-TIC chromatogram object (output from read_chrom on a NetCDF file) and sequentially apply: (1) Whittaker smoothing via wsmooth to reduce high-frequency noise, (2) asymmetric least squares baseline correction via baseline_corr to remove steady and increasing intensity artifacts, and (3) 2D correlation optimized warping (2DCOW) via twod_cow or batch_2DCOW to align peaks across samples. The asymmetric least squares algorithm prioritizes fitting the baseline at low intensity regions while allowing peaks to deviate, making it robust to column bleeding and instrumental drift. After alignment, join all preprocessed chromatograms into a single R object using join_chromatograms before multiway PCA analysis.

## Related tools

- **RGCxGC** (Provides wsmooth, baseline_corr, twod_cow, batch_2DCOW, join_chromatograms, and m_prcomp functions for 2D-TIC preprocessing and multiway PCA) — https://github.com/DanielQuiroz97/RGCxGC
- **R** (Runtime environment for executing RGCxGC preprocessing functions)

## Examples

```
# Load 2D-TIC, apply smoothing, baseline correction, and 2DCOW alignment
chrom_smooth <- wsmooth(chrom_obj, lambda = 1e4, d = 2)
chrom_bc <- baseline_corr(chrom_smooth, lambda = 1e6, p = 0.01)
chrom_aligned <- batch_2DCOW(chrom_bc, reference = ref_chrom)
chrom_joined <- join_chromatograms(chrom_aligned_list)
```

## Evaluation signals

- Baseline-corrected chromatogram shows reduced low-intensity baseline drift with preserved peak heights compared to raw 2D-TIC
- Smoothed chromatogram exhibits reduced high-frequency noise while maintaining peak shape and resolution
- Aligned chromatograms from batch_2DCOW show consistent peak positions across replicates when overlaid
- Joined multi-sample object contains no NA or missing values and all samples have identical retention time and modulation time dimensions
- Downstream MPCA score plot shows clear separation between biological groups (e.g., typhoid carriers vs. controls) after preprocessing, indicating noise reduction revealed biological signal

## Limitations

- Asymmetric least squares baseline correction performance depends on the choice of smoothness and asymmetry parameters; suboptimal tuning may over-correct or under-correct baseline distortion
- 2DCOW peak alignment requires careful selection of reference chromatogram; a poor reference may propagate misalignment across all samples
- Preprocessing pipeline assumes column bleeding and instrumental drift are the primary sources of baseline distortion; other artifacts (e.g., sample matrix effects) may not be fully resolved
- The sequential application of smoothing, baseline correction, and alignment may introduce cumulative distortions if parameters are not carefully validated

## Evidence

- [other] baseline_corr removes baseline distortion from 2D-TIC: "The baseline_corr function applies the asymmetric least squares algorithm to remove steady and increasing intensity from 2D-TIC chromatograms caused by instrumental contamination or column bleeding"
- [intro] smoothing and baseline correction reduce noise before multivariate analysis: "noise can be significantly reduced by using preprocessing algorithms, herein smoothing, baseline correction, and peak alignment. Then, in order to reveal differences between groups, multivariate"
- [readme] RGCxGC offers baseline correction based on asymmetric least squares: "RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares"
- [intro] 2D-TIC is created from NetCDF import and folded via read_chrom: "the raw chromatogram is importing from a NetCDF file and is folded into the two-dimensional Total Intensity Chromatogram (2D-TIC)"
- [intro] wsmooth and baseline_corr are applied sequentially for preprocessing: "you can perform preprocessing routines like smoothing and/or baseline correction by using the function wsmooth and baseline_corr"
- [intro] 2DCOW aligns peaks across samples before joining: "peak alignment of a single sample against a reference chromatogram can be performed based on the two-dimensional correlation optimized warping (2DCOW) algorithm. Alternatively, multiple sample"
- [intro] Preprocessed chromatograms are joined into single object before MPCA: "Once the chromatograms are already preprocessed, it has to be in a single R object. To meet this requirement, the join_chromatograms functions does it"
