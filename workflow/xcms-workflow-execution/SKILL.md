---
name: xcms-workflow-execution
description: Use when you have raw LC-MS data files (mzML, netCDF, or raw vendor formats) from multiple samples and need to extract, align, and quantify chromatographic features across the cohort.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3172
  tools:
  - xcms
  - MsFeatures
  - MsExperiment
  - Spectra
derived_from:
- doi: 10.1021/acs.analchem.5c04338
  title: xcms
evidence_spans:
- The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data.
- The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms
    doi: 10.1021/acs.analchem.5c04338
    title: xcms
  dedup_kept_from: coll_xcms
schema_version: 0.2.0
---

# xcms-workflow-execution

## Summary

Execute a complete LC-MS data preprocessing pipeline using xcms, encompassing chromatographic peak detection, feature correspondence, and optional gap-filling to produce a quantitative feature abundance table from raw mass spectrometry data. This skill chains multiple xcms methods into a reproducible workflow suitable for metabolomics studies.

## When to use

You have raw LC-MS data files (mzML, netCDF, or raw vendor formats) from multiple samples and need to extract, align, and quantify chromatographic features across the cohort. Use this skill when your analysis goal requires going from raw instrument output to a feature-by-sample abundance matrix for downstream statistical or annotation analysis.

## When NOT to use

- Input is already a pre-processed feature table or abundance matrix — skip directly to statistical analysis.
- Data are from ion mobility MS or other non-traditional LC-MS acquisition modes not explicitly supported by the article's workflow.
- Raw data files are corrupted or in unsupported formats; verify file integrity and format compatibility first.

## Inputs

- Raw LC-MS data files (mzML, netCDF, or vendor formats)
- XcmsExperiment or xcmsSet object
- CentWaveParam peak detection parameters
- SimilarRtimeParam, AbundanceSimilarityParam, and/or EicSimilarityParam grouping parameters

## Outputs

- XcmsExperiment object with detected chromatographic peaks
- Feature groups (correspondence result)
- Feature abundance matrix (samples × features)
- Feature metadata table (m/z, retention time, peak statistics)

## How to apply

Load the raw data into an XcmsExperiment or xcmsSet object using appropriate file readers. Apply chromatographic peak detection with findChromPeaks() using CentWaveParam settings tuned to your instrument resolution and expected peak widths. Next, perform correspondence (feature grouping) by retention time using groupFeatures() with SimilarRtimeParam (typically 20-second window for LC-MS) to group peaks with similar m/z and retention time across samples. Optionally refine groups using AbundanceSimilarityParam (abundance correlation across samples) and EicSimilarityParam (peak shape similarity). Finally, apply fillChromPeaks() to recover missing feature abundances in samples where peaks were not detected by integrating signal from m/z–retention time windows defined by detected peaks. Extract the resulting feature abundance table and feature metadata (m/z, retention time, peak statistics) for downstream analysis.

## Related tools

- **xcms** (Core package providing findChromPeaks(), groupFeatures(), fillChromPeaks(), and feature correspondence methods) — https://github.com/sneumann/xcms
- **MsFeatures** (Provides general MS feature grouping functionality and parameter classes (SimilarRtimeParam, AbundanceSimilarityParam, EicSimilarityParam))
- **MsExperiment** (Container class for organizing raw spectra and results in version 4 xcms workflows)
- **Spectra** (Backend for efficient access to raw LC-MS spectra in xcms version 4)

## Examples

```
xcms_result <- findChromPeaks(xcms_data, param=CentWaveParam(ppm=15, peakwidth=c(5,20))); xcms_result <- groupFeatures(xcms_result, param=SimilarRtimeParam(window=20)); xcms_result <- fillChromPeaks(xcms_result); feat_table <- featureValues(xcms_result, value='into')
```

## Evaluation signals

- Number of chromatographic peaks detected matches expected range for the instrument and method (e.g., hundreds to thousands for typical metabolomics experiments).
- Feature groups produced by SimilarRtimeParam(20) show expected distribution of group sizes; verify group count and average features per group against reference values from the faahKO dataset or similar benchmark.
- Gap-filled feature abundance table has no missing values (or expected number of NA values if gap-filling was partial) and non-negative intensities.
- Feature metadata (m/z, retention time) show expected ranges and correlation patterns; isotopic doublets and adducts should be detected and grouped.
- Reproducibility: re-running the workflow with identical parameter settings produces identical feature groups and abundance values.

## Limitations

- Features of the same compound may not be grouped correctly if they fall outside the retention time window (SimilarRtimeParam window=20 seconds is a common default but may miss compounds with variable retention drift or in-source fragmentation patterns).
- For some samples, chromatographic peaks are not detected at feature locations even though signal is present in raw data, requiring gap-filling; gap-filling assumes the m/z–retention time window is correctly defined and may introduce noise if windows overlap with background.
- Peak detection and grouping parameters are method- and instrument-dependent; the workflow requires optimization for new instruments, chromatographic conditions, or compound classes not covered in the article's examples.
- No built-in handling of batch effects, systematic retention time shifts, or complex multi-modal peak shapes; post-processing refinement may be needed.

## Evidence

- [readme] The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data.: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
- [intro] SimilarRtimeParam: perform an initial grouping based on similar retention time.: "SimilarRtimeParam: perform an initial grouping based on similar retention time."
- [intro] AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples.: "AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples."
- [intro] for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated.: "for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated."
- [intro] Perform chromatographic peak detection on MS level 1 data using CentWaveParam: "Perform chromatographic peak detection on MS level 1 data using CentWaveParam"
