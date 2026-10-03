---
name: mass-defect-filtering
description: Use when after MS-Dial peak picking and feature table construction, when
  you observe a high proportion of features with anomalous m/z decimal values that
  are inconsistent with known metabolite ionization patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - R
  - margheRita
  - MS-Dial
  - notame
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow
- The R package margheRita
- The R package margheRita addresses the complete workflow for metabolomic profiling
  in untargeted studies based on liquid chromatography (LC) coupled with tandem mass
  spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  dedup_kept_from: coll_margherita_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.06.20.599545v1
  all_source_dois:
  - 10.1101/2024.06.20.599545v1
  - 10.1101/2024.06.20.599545
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-defect-filtering

## Summary

Remove spurious or artifact features from untargeted metabolomics data by filtering on the decimal portion of m/z values. This quality-control filter excludes features with m/z decimal values falling within specified ranges (commonly [4, 8]), retaining only features with biologically plausible mass-to-charge ratios for downstream metabolite identification.

## When to use

After MS-Dial peak picking and feature table construction, when you observe a high proportion of features with anomalous m/z decimal values that are inconsistent with known metabolite ionization patterns. Apply this filter early in the preprocessing pipeline, before statistical testing or metabolite annotation, to reduce the false-positive feature count and improve spectral library matching accuracy.

## When NOT to use

- Input is already a curated metabolite library or list of known standards; mass-defect filtering is a quality metric for discovery, not validation.
- Data were acquired using targeted or pseudo-targeted acquisition with pre-selected m/z ranges; filtering may exclude intentionally selected features.
- The m/z decimal distribution in your instrument or ionization protocol is known to differ from the [4, 8] anomalous range; re-validate or adjust the threshold before applying.

## Inputs

- Feature table with m/z values from MS-Dial output
- Feature abundance matrix (samples × features)
- m/z value vector (one per feature)

## Outputs

- Filtered feature table (retained features with appropriate m/z values)
- Removed feature table (excluded features with inappropriate m/z values)
- Filtering summary report (count of retained and excluded features)

## How to apply

Extract the decimal part of each feature's m/z value by computing m/z modulo 1 (i.e., m/z − floor(m/z)). Classify each feature as inappropriate if its decimal portion lies within the default interval [4, 8]; otherwise mark it as appropriate. Separate the feature table into two subsets: one containing features that pass the filter (appropriate m/z values) and one containing filtered-out features (inappropriate m/z values). Return both subsets along with a summary report documenting the count and proportion of retained vs. excluded features. The rationale is that authentic metabolites typically exhibit m/z decimal distributions outside this anomalous range, particularly in data-independent acquisition (DIA) and high-resolution MS/MS workflows where spectral accuracy is critical for downstream identification.

## Related tools

- **margheRita** (R package providing the m_z_filtering() function and integrated pre-processing workflow (quality control, filtering, normalization) for MS-Dial output analysis) — https://github.com/emosca-cnr/margheRita
- **MS-Dial** (Peak picking and feature table generation software producing the m/z values input to the mass-defect filter)
- **R** (Execution environment for modulo arithmetic on m/z vectors and feature classification)
- **notame** (Alternative R package for non-targeted LC-MS workflow that includes quality metrics and feature flagging; compatible via margheRita export functions) — https://github.com/hanhineva-lab/notame

## Evaluation signals

- Feature count conservation: sum of retained and excluded features equals the input feature count with no data loss.
- Decimal distribution check: plot the decimal portion of m/z values before and after filtering; verify that retained features show absence or near-absence of decimal values in the [4, 8] range.
- Consistency with spectral library matching: post-filtering metabolite annotation should show increased cosine similarity scores and reduced number of ambiguous or low-confidence matches (improvement in fragment matching accuracy).
- Sample-wise abundance stability: total feature abundance per sample should remain consistent across filtered features; large shifts may indicate loss of true biological signal.
- Reproducibility: filtering with identical m/z decimal interval [4, 8] applied to replicate MS runs should yield consistent proportions of retained features (e.g., ~90–92% retention in typical workflows).

## Limitations

- The [4, 8] m/z decimal threshold is empirically derived and may require adjustment for different instrument types, ionization methods, or chromatographic columns; no theoretical justification for the specific interval is provided.
- Mass-defect filtering does not distinguish between instrumental artifacts and genuine low-abundance or rare metabolites; features excluded may include valid compounds with atypical m/z decimals.
- The filter assumes that anomalous m/z decimals are uniformly distributed across features and samples; batch or polarity-specific artifacts may not be adequately corrected.
- Application to targeted or semi-targeted workflows where m/z selection is predetermined may inadvertently remove intentionally included features.

## Evidence

- [other] The m/z filtering function removes features whose m/z decimal values fall within the interval [4, 8] by default.: "The m/z filtering function removes features whose m/z decimal values fall within the interval [4, 8] by default. When applied to the dataset, this filter excluded 56 features with inappropriate m/z"
- [other] Extract the decimal part of each m/z value by computing m/z modulo 1; classify as inappropriate if within [4,8].: "Extract the decimal part of each m/z value by computing m/z modulo 1. 3. Classify features as inappropriate if the decimal part lies within [4,8]; otherwise mark as appropriate."
- [readme] Filtering by mass defects is a pre-processing method specifically recommended for metabolomic profiles.: "a series of pre-processing functions (quality control, filtering and normalization) with a particular focus on methods specifically recommended for metabolomic profiles, such as filtering by mass"
- [readme] This pipeline is especially advantageous in the case of data-independent acquisition (DIA), where all MS/MS spectra are acquired with high resolution.: "This pipeline is especially advantageous in the case of data-independent acquisition (DIA), where all MS/MS spectra are acquired with high resolution."
- [readme] margheRita enhances fragment matching accuracy by providing an original metabolite spectral library.: "margheRita enhances fragment matching accuracy by providing an original metabolite spectral library acquired in both polarities using different chromatographic columns."
