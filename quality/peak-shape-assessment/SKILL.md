---
name: peak-shape-assessment
description: Use when after peak detection in a nontargeted LC-MS workflow when you
  have a feature table with detected peaks and need to filter low-quality features
  or understand why certain features have inconsistent intensity or poor annotation
  confidence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - masscube
  - Python
  techniques:
  - LC-MS
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: huaxuyu/masscube
  license_tier: noncommercial
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-025-60640-5
  title: MassCube
evidence_spans:
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing
- masscube is an integrated Python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_masscube_cq
    doi: 10.1038/s41467-025-60640-5
    title: MassCube
  dedup_kept_from: coll_masscube_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-60640-5
  all_source_dois:
  - 10.1038/s41467-025-60640-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-shape-assessment

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Evaluate the morphological quality of detected LC-MS peaks by extracting and analyzing peak shape attributes (e.g., symmetry, width, definition) as part of comprehensive feature quality scoring. This skill surfaces problematic peaks that may indicate instrumental artifacts, co-elution, or poor signal quality before downstream annotation.

## When to use

Apply this skill after peak detection in a nontargeted LC-MS workflow when you have a feature table with detected peaks and need to filter low-quality features or understand why certain features have inconsistent intensity or poor annotation confidence. Peak shape assessment is essential before committing features to MS/MS annotation or statistical analysis.

## When NOT to use

- Input is already a validated, publication-ready feature table with pre-computed quality scores.
- Analysis is targeted and peaks are known a priori (e.g., selected reaction monitoring); peak shape assessment is most valuable in nontargeted discovery workflows.
- Peak detection algorithm has not yet been run; this skill requires detected features, not raw LC-MS data alone.

## Inputs

- feature table from peak detection (pandas DataFrame or equivalent with retention time, m/z, intensity, chromatographic metrics)
- raw LC-MS data or extracted ion chromatogram data for peak profile analysis

## Outputs

- quality-annotated feature table with per-feature quality scores
- peak shape quality flags (pass/fail/warning)
- per-feature diagnostic metrics (peak definition, chromatographic resolution scores)

## How to apply

Extract peak morphology attributes (retention time, m/z, peak width, symmetry metrics, signal-to-noise ratio) from the detected feature table using MassCube's quality evaluation module. Compute individual peak shape quality dimensions, such as peak definition and chromatographic resolution, which quantify how well-defined and baseline-separated the peak is. Aggregate shape metrics with other quality dimensions (intensity consistency, isotope/adduct coherence) into a per-feature quality score and assign quality flags (pass/fail/warning). Features with poor peak shape scores should be flagged for review or exclusion, as they indicate potential instrumental noise, co-elution, or chemical artifacts rather than true molecular signals.

## Related tools

- **masscube** (Provides the integrated quality evaluation module that extracts peak shape attributes and computes per-feature quality scores including peak definition and chromatographic resolution) — https://github.com/huaxuyu/masscube/
- **Python** (Programming environment for loading feature tables with pandas, extracting peak attributes, and scripting the quality evaluation workflow)

## Evaluation signals

- Output feature table schema matches input but includes new columns for per-feature quality scores and peak shape flags; all rows retain original feature identifiers.
- Quality scores are numeric, bounded (e.g., 0–1 or 0–100), and correlate inversely with peak width, asymmetry, and baseline noise.
- Features flagged as 'fail' or 'warning' exhibit visually poor peak morphology (broad, asymmetric, low signal-to-noise ratio) when inspected in the extracted ion chromatogram.
- Aggregate quality distribution shows expected bimodality or right-skew toward high-quality features in a typical nontargeted dataset; absence of such distribution suggests algorithm failure or misconfiguration.
- Per-feature diagnostics (peak definition and resolution scores) are internally consistent and inversely correlated with intensity variance across replicates.

## Limitations

- Peak shape assessment depends on accurate peak detection upstream; misdetected or partially detected peaks will receive misleading quality scores.
- Quality thresholds and aggregation weights are not explicitly tuned in the README; practitioners may need to validate cutoffs against their own instrumental and sample contexts.
- No changelog is available; feature definitions and quality metrics may change across MassCube versions without warning.

## Evidence

- [other] Extract feature attributes including retention time, m/z, peak shape, signal-to-noise ratio, and chromatographic metrics.: "Extract feature attributes including retention time, m/z, peak shape, signal-to-noise ratio, and chromatographic metrics."
- [other] Compute individual quality dimensions (peak definition, chromatographic resolution, intensity consistency, isotope/adduct coherence) using masscube's quality evaluation module.: "Compute individual quality dimensions (peak definition, chromatographic resolution, intensity consistency, isotope/adduct coherence) using masscube's quality evaluation module."
- [intro] Comprehensive feature quality evaluation.: "Comprehensive feature quality evaluation."
- [other] Aggregate per-feature quality scores into a single comprehensive metric and assign quality flags (pass/fail/warning).: "Aggregate per-feature quality scores into a single comprehensive metric and assign quality flags (pass/fail/warning)."
- [readme] masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing.: "masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing."
