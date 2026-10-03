---
name: drift-time-filtering
description: Use when you have loaded a raw GCIMS dataset and need to isolate the
  region of interest in drift time (typically 5–16 ms for small organic molecules)
  to exclude low-drift-time chemical noise, high-drift-time tail artifacts, or off-scale
  ion signals that would degrade subsequent alignment and peak.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GCIMS
  - ggplot2
  techniques:
  - GC-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1016/j.chemolab.2023.104938
  title: GCIMS
evidence_spans:
- library(ggplot2) library(cowplot) library(GCIMS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gcims_cq
    doi: 10.1016/j.chemolab.2023.104938
    title: GCIMS
  dedup_kept_from: coll_gcims_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.chemolab.2023.104938
  all_source_dois:
  - 10.1016/j.chemolab.2023.104938
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# drift-time-filtering

## Summary

Restrict Gas Chromatography–Ion Mobility Spectrometry (GCIMS) samples to a target drift time range to remove instrumental noise and out-of-range ion signals before downstream alignment and peak detection. This is a critical preprocessing step that reduces data dimensionality and improves signal quality.

## When to use

Apply this skill when you have loaded a raw GCIMS dataset and need to isolate the region of interest in drift time (typically 5–16 ms for small organic molecules) to exclude low-drift-time chemical noise, high-drift-time tail artifacts, or off-scale ion signals that would degrade subsequent alignment and peak detection.

## When NOT to use

- The drift time range is already known to contain no signal or has been validated in a prior run (refiltering with identical bounds is redundant).
- You are working with high-resolution or exploratory data and want to preserve the full drift time axis to discover unexpected ion populations.
- The dataset is already post-alignment or has been decimated; re-filtering after decimation may introduce edge artifacts.

## Inputs

- GCIMSDataset object (loaded from raw GCIMS NetCDF or mzML file)

## Outputs

- Filtered GCIMSDataset object (drift time range restricted)
- Updated 2D matrix (retention time × drift time, with drift time dimension reduced)

## How to apply

Load a GCIMSDataset object in R and call the filterDt() function with a drift time range specified in milliseconds (e.g., c(5, 16) for a typical small-molecule assay). The filtering is applied to the entire 2D retention time × drift time matrix before any smoothing or decimation steps. Choose the lower and upper bounds based on the expected ion mobility characteristics of your analytes and instrument calibration; narrower ranges reduce memory and computation cost but risk losing signal if bounds are too tight. Verify the filtered output by inspecting the resulting Reverse Ion Chromatogram or Total Ion Spectra plots for retained signal intensity and absence of artifacts at the boundaries.

## Related tools

- **GCIMS** (R package that implements the filterDt() function for drift time range restriction) — https://github.com/sipss/GCIMS
- **R** (Runtime environment for executing GCIMS filtering workflows)
- **ggplot2** (Visualization of filtered Total Ion Spectra and Reverse Ion Chromatogram plots to evaluate filtering outcome)

## Examples

```
filterDt(dataset, dt = c(5, 16))
```

## Evaluation signals

- Verify that the filtered dataset retains all samples and that no samples were dropped during range restriction.
- Plot the Total Ion Spectra and Reverse Ion Chromatogram of the filtered dataset and confirm visual absence of signal outside the specified drift time range.
- Compare the memory footprint (RAM) and matrix dimensions before and after filtering; drift time dimension should be reduced proportionally to the range restriction.
- Check that the lower and upper drift time boundaries in the filtered object match the specified thresholds (e.g., 5 ms and 16 ms).
- Confirm that subsequent alignment (drift time, then retention time) produces well-aligned peaks without edge distortions at the filtered boundaries.

## Limitations

- Drift time filtering is a lossy, irreversible operation; if the range is too narrow, analyte signal may be discarded and cannot be recovered.
- The optimal drift time range is instrument- and compound-class-specific; thresholds derived from one dataset (e.g., small ketones at 5–16 ms) may not transfer to other analyte classes or instruments.
- Filtering before smoothing and decimation may leave instrumental noise at the boundaries; boundary artifacts can propagate into downstream alignment if not inspected.
- The GCIMS package uses delayed evaluation, so filtering operations may not materialize into memory until explicitly computed or plotted; unexpected behavior may occur if downstream operations do not trigger full evaluation.

## Evidence

- [intro] filterDt() function call and range specification: "filterDt(dataset, dt = c(5, 16)) # in ms"
- [intro] Drift time filtering as a preprocessing step in the workflow: "Filter the retention and drift time of your samples"
- [intro] Rationale for drift time filtering in the context of GCIMS misalignment: "Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time."
- [intro] GCIMS package overview and delayed evaluation efficiency: "GCIMS uses delayed evaluations were possible, so dataset modifications can be executed in a more efficient way and without using too much RAM."
- [intro] Workflow sequence showing filtering before smoothing and alignment: "1. Load the threeketones dataset and create a GCIMSDataset object using GCIMS. 2. Filter retention time to 0–1100 s using filterRt(). 3. Filter drift time to 5–16 ms using filterDt()."
