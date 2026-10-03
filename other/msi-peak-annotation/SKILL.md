---
name: msi-peak-annotation
description: Use when you have processed MSI data (peak matrix and spatial coordinates)
  from matrix-assisted laser desorption/ionization (MALDI) or silver-assisted laser
  desorption/ionization (AgLDI) experiments, and you need to computationally distinguish
  matrix ions from analyte ions before downstream feature.
license: CC-BY-4.0
metadata:
  grounding_tier: link-only
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - rMSIcleanup
  - rMSI
  - rMSIproc
  - R
  - devtools
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-020-00449-0
  title: ''
evidence_spans:
- rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI
  data
- devtools::install_github("prafols/rMSI", ref = "0.8")
- devtools::install_github("prafols/rMSIproc", ref = "0.2")
- rMSIcleanup is an open-source R package
- install.packages("devtools")
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rmsicleanup_ms_imaging_matrix_peak_annot_cq
    doi: 10.1186/s13321-020-00449-0
    title: ''
  dedup_kept_from: coll_rmsicleanup_ms_imaging_matrix_peak_annot_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-020-00449-0
  all_source_dois:
  - 10.1186/s13321-020-00449-0
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Matrix-Related Peak Annotation in Mass Spectrometry Imaging

## Summary

Automated classification of ions as matrix-related or analyte-related in MSI datasets by integrating chemical formula matching and spatial distribution coherence, with isobaric peak detection to prevent misclassification. This skill disambiguates matrix signal from biological/chemical signals in imaging mass spectrometry workflows.

## When to use

Apply this skill when you have processed MSI data (peak matrix and spatial coordinates) from matrix-assisted laser desorption/ionization (MALDI) or silver-assisted laser desorption/ionization (AgLDI) experiments, and you need to computationally distinguish matrix ions from analyte ions before downstream feature extraction, statistical analysis, or biomarker discovery. Triggered by the presence of a peak matrix file (.zip format) and associated MSI dataset (.tar format) with known or inferred matrix composition.

## When NOT to use

- Input data are already in imzML or proprietary vendor formats without prior conversion to rMSIproc format; use rMSIproc::ProcessWizard() first.
- The matrix chemical formula is unknown or ambiguous; the algorithm requires a precise formula string to match against detected peaks.
- Data do not include full spatial imaging information or are already aggregated into a feature table without per-pixel ion intensities; spatial distribution is a required input signal.

## Inputs

- Peak matrix file in rMSIproc format (.zip)
- Processed MSI imaging data in rMSI format (.tar)
- Matrix chemical formula string (e.g., 'Ag1', 'DHB', 'CHCA')
- MSI spatial coordinates (implicit in the .tar and .zip files)

## Outputs

- Annotation results object with binary matrix/non-matrix labels per ion
- Visual PDF report justifying each annotation decision
- Cleaned peak matrix with matrix-related peaks flagged or removed

## How to apply

Load the MSI peak matrix and processed imaging data into the R environment using rMSIproc and rMSI. Extract spatial distribution patterns for each detected ion across the imaging dataset. Supply the peak matrix, a chemical formula string identifying the matrix (e.g., 'Ag1' for silver), and the full imaging data object to the rMSIcleanup::annotate_matrix() function. The algorithm evaluates each ion's chemical formula against known matrix characteristics and computes spatial coherence metrics; it flags overlapped or isobaric peaks to prevent false negatives. The output is a binary classification (matrix vs. non-matrix) for each ion, justified by formula matching and spatial distribution alignment. Generate a PDF annotation report to transparently audit each classification decision before removing matrix peaks from the peak matrix.

## Related tools

- **rMSIcleanup** (Primary annotation algorithm; integrates chemical formula matching and spatial distribution analysis to classify matrix-related peaks) — https://github.com/gbaquer/rMSIcleanup
- **rMSI** (Loads and manages processed MSI imaging datasets (.tar format) to extract spatial and spectral data for annotation) — https://github.com/prafols/rMSI
- **rMSIproc** (Processes raw imzML files and manages peak matrices (.zip format) that feed into the annotation workflow) — https://github.com/prafols/rMSIproc
- **R** (Execution environment for rMSIcleanup and dependent packages)
- **devtools** (Installation and dependency management for rMSIcleanup from GitHub)

## Examples

```
results<-rMSIcleanup::annotate_matrix(pks,"Ag1",full); rMSIcleanup::generate_pdf_report(results,pks,full,"test",folder="./"); pks_clean<-rMSIcleanup::remove_matrix(pks,results)
```

## Evaluation signals

- All detected ions are assigned a binary label (matrix or non-matrix); no unclassified peaks remain in the results object.
- The PDF annotation report includes justification (formula match score and spatial coherence metric) for each ion classified as matrix-related; transparent audit trail is present.
- Isobaric and overlapped peaks are flagged and their classification confidence is reduced or flagged for manual review, indicating the overlapping peak detection feature was engaged.
- Downstream statistical analysis (e.g., PCA, univariate tests) on the cleaned peak matrix shows improved separation between sample groups or reduced noise variance compared to unannotated data.
- Visual inspection of spatial ion maps confirms that flagged matrix ions are distributed uniformly across the imaging region (consistent with matrix deposition), while retained ions show biological/chemical localization patterns.

## Limitations

- The algorithm requires a precise chemical formula string for the matrix; unknown or ambiguous matrix compositions will degrade classification accuracy.
- Overlapping peaks and isobaric ions are detected but may still be misclassified if their spatial distributions are similar; manual curation is recommended for ambiguous cases.
- Performance on novel matrix types or atypical mass ranges not represented in the training/reference set is not documented.
- The method assumes spatial imaging data are present and informative; datasets with highly heterogeneous matrix deposition or poor spatial resolution may yield unreliable annotations.

## Evidence

- [intro] The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related: "The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related"
- [intro] The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions: "The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions"
- [intro] The package generates a visual report to transparently justify each annotation: "the package generates a visual report to transparently justify each annotation"
- [readme] Install rMSI and rMSIproc via devtools, then install rMSIcleanup; load data and call annotate_matrix function: "pks<-rMSIproc::LoadPeakMatrix("[Full Path to Peak Matrix (.zip)]"); full<-rMSI::LoadMsiData("[Full Path to Processed Data (.tar)]"); results<-rMSIcleanup::annotate_matrix(pks,"Ag1",full)"
- [readme] Generate PDF report to justify annotations before removing matrix peaks: "rMSIcleanup::generate_pdf_report(results,pks,full,"test",folder="/home/gbaquer/"); pks_clean<-rMSIcleanup::remove_matrix(pks,results)"
- [readme] Process imzML using rMSIproc format before annotation: "To annotate your own data you will have to process the imzML using the following command: rMSIproc::ProcessWizard()"
