---
name: xcms-profile-parsing
description: Use when you have xcms-processed LC-MS data with detected feature groups
  (from xcms grouping), suspect retention time misalignment across samples due to
  long acquisition periods or large sample cohorts, and need to feed raw profiles
  into ncGTW's realignment algorithm.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3932
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - ncGTW
  - R
  - xcms
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btaa037
  title: ncGTW
evidence_spans:
- Neighbor-wise Compound-specific Graphical Time Warping (ncGTW) [@ncgtw19] is an
  alignment algorithm
- '`ncGTW` is an R package developed as a plug-in of `xcms`'
- ncGTW is an R package developed as a plug-in of xcms
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ncgtw_cq
    doi: 10.1093/bioinformatics/btaa037
    title: ncGTW
  dedup_kept_from: coll_ncgtw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaa037
  all_source_dois:
  - 10.1093/bioinformatics/btaa037
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# xcms-profile-parsing

## Summary

Parse and structure raw LC-MS profile data from xcms-processed files into organized feature-by-sample objects for downstream realignment analysis. This skill extracts retention time and intensity profiles needed by ncGTW to detect and correct misaligned feature groups.

## When to use

You have xcms-processed LC-MS data with detected feature groups (from xcms grouping), suspect retention time misalignment across samples due to long acquisition periods or large sample cohorts, and need to feed raw profiles into ncGTW's realignment algorithm. Trigger: xcms output files + list of potentially misaligned feature group identifiers.

## When NOT to use

- Input profiles are already aligned or no misalignment has been detected by ncGTW.
- Data are not from xcms preprocessing; loadProfile() expects xcms-compatible file formats and metadata.
- Feature groups are already in peak-table or feature matrix form; loadProfile() requires raw profile objects.

## Inputs

- xcms-processed profile file paths (character vector)
- excluGroups table: detected misaligned feature group identifiers (data.frame or matrix)

## Outputs

- ncGTWinputs object: nested list structure containing raw LC-MS profiles indexed by feature and sample identifiers

## How to apply

Call the ncGTW::loadProfile() function, passing file paths to xcms-processed profiles and a table of detected misaligned feature groups (excluGroups). loadProfile() reads the raw xcms profiles and constructs an ncGTWinputs object—a nested list structure keyed by feature and sample identifiers—that organizes retention time and intensity values for each compound-sample pair. Validate that the returned ncGTWinputs object contains the expected hierarchical list structure with profiles accessible by both feature and sample keys, confirming all misaligned groups have been loaded.

## Related tools

- **ncGTW** (R package providing loadProfile() function to parse and structure raw profiles for misalignment detection and realignment) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (Upstream LC-MS preprocessing package; ncGTW is a plug-in that processes xcms output profiles)
- **R** (Programming language runtime for executing loadProfile() and ncGTW functions)

## Examples

```
ncGTWinputs <- loadProfile(file_paths = c('sample1.RData', 'sample2.RData'), excluGroups = misaligned_features_table)
```

## Evaluation signals

- ncGTWinputs object is successfully returned without NULL values or parsing errors
- List structure contains nested keys matching all feature identifiers in excluGroups and all sample identifiers in input files
- Each profile entry contains numeric vectors for retention time and intensity; no missing or NaN values in expected data
- Object class is 'ncGTWinputs' or equivalent; str() confirms expected hierarchical organization
- Profile count and sample coverage match input feature group and file path dimensions

## Limitations

- loadProfile() requires strict xcms file format compatibility; incompatible or corrupted xcms output will cause parsing failure.
- excluGroups table must contain valid feature group identifiers that exist in the xcms profiles; mismatched identifiers will result in empty or partial output.
- Function assumes retention time drift structures are present in data; sparse or single-timepoint profiles may not be informative for downstream realignment.

## Evidence

- [other] loadProfile() function definition and inputs: "loadProfile() accepts file paths and detected feature groups (excluGroups) as inputs and outputs ncGTWinputs, a structured object containing the raw profiles needed for downstream realignment"
- [other] Workflow steps for xcms profile parsing: "Call loadProfile() function from the ncGTW R package to read xcms-processed profiles and construct the ncGTWinputs object, which organizes raw profiles by feature and sample identifiers."
- [other] Validation step and expected output structure: "Validate that the output object contains the expected list structure with profiles accessible by feature and sample keys."
- [intro] ncGTW role as xcms plug-in: "`ncGTW` is an R package developed as a plug-in of `xcms`, a popular LC-MS data analysis R package"
- [readme] Misalignment detection motivation: "ncGTW can detect the misaligned features with two criterions. First, ncGTW algorithm estimates the p-value of each feature using higher resolution alignment result"
