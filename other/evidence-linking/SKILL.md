---
name: evidence-linking
description: Use when you have tandem MS/MS spectra annotated by at least two of GNPS (FBMN), ISDB-LOTUS (CFM-ID 4.0 spectral matching), and Sirius 6, and you need to rank features by annotation agreement rather than trust a single tool's output.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3473
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3361
  - http://edamontology.org/topic_3373
  tools:
  - GitHub
  - GNPS (Global Natural Products Social Molecular Networking)
  - ISDB-LOTUS (Isomeric Spectral DataBase of Natural Products)
  - Sirius 6
  - MatchMS
  - MS2DECIDE
  - MZmine 2
  - mzmine2
  - MZmine
  - mzmine (successor)
  - GitHub (repositories and issue tracker)
  - npanalyst
  - forward_train.py
  - forward_evaluate_pipeline.py
  - analysis_pipeline.py
  - const.py
  - SIRIUS
  - CSI:FingerID
  - CANOPUS
  - MSNovelist
  - ZODIAC
derived_from:
- doi: 10.1002/cmtd.202400088
  title: ms2decide
- doi: 10.1186/1471-2105-11-395
  title: ''
- doi: 10.1021/acscentsci.1c01108
  title: ''
- doi: 10.1021/acs.analchem.2c02093
  title: ''
- doi: 10.1021/acs.analchem.5c03730
  title: ''
- doi: 10.1038/s41592-019-0344-8
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_13c_spacem
    doi: 10.1038/s42255-024-01118-4
    title: 13C-SpaceM
  - build: coll_bindiscover
    doi: 10.1186/s13321-023-00734-8
    title: bindiscover
  - build: coll_featurefindermetab
    doi: 10.1074/mcp.M113.031278
    title: featurefindermetab
  - build: coll_hexpmetdb
    doi: 10.1289/EHP7722
    title: HExpMetDB
  - build: coll_ms2decide
    doi: 10.1002/cmtd.202400088
    title: ms2decide
  - build: coll_mzmine2
    doi: 10.1186/1471-2105-11-395
    title: mzmine2
  - build: coll_np_analyst
    doi: 10.1021/acscentsci.1c01108
    title: NP Analyst
  - build: coll_rassp
    doi: 10.1021/acs.analchem.2c02093
    title: rassp
  - build: coll_rtmsecho
    doi: 10.1021/acs.analchem.5c03730
    title: rtmsecho
  - build: coll_sirius
    doi: 10.1038/s41592-019-0344-8
    title: sirius
  dedup_kept_from: coll_ms2decide
schema_version: 0.2.0
---

# evidence_linking

## Summary

Link mass spectrometry annotations from multiple sources (GNPS, ISDB-LOTUS, Sirius) to a unified ranked output by aggregating consensus confidence scores using decision theory. This skill identifies which annotations are supported by independent tools and surfaces the most reliable compound identifications for natural products discovery.

## When to use

You have tandem MS/MS spectra annotated by at least two of GNPS (FBMN), ISDB-LOTUS (CFM-ID 4.0 spectral matching), and Sirius 6, and you need to rank features by annotation agreement rather than trust a single tool's output. Use this skill when manual expert prioritization is infeasible and you want data-driven consensus across heterogeneous annotation engines.

## When NOT to use

- Annotations are from only a single tool (GNPS, Sirius, or ISDB-LOTUS alone) — consensus requires ≥2 independent sources.
- Your input spectra have not been processed through FBMN or CFM-ID workflows — missing prerequisite annotations.
- You have already manually curated the feature table and do not need automated consensus ranking.

## Inputs

- GNPS FBMN job output (library search results)
- ISDB-LOTUS CFM-ID spectral matching results (from get_cfm_annotation function)
- Sirius 6 structure_identifications.tsv file
- Quantitative table (.csv with feature IDs and abundance data)
- MGF file (tandem mass spectrometry spectra)

## Outputs

- Ranked TSV file with features sorted by K-value (knownness score)
- Optional: empty.tsv report (if iterative GNPS analog search was used and empty annotations are requested)

## How to apply

Compile annotations from GNPS, ISDB-LOTUS, and Sirius into a unified dataframe, then calculate pairwise Tanimoto similarity scores (or apply default fallbacks: 0.7 when GNPS–Sirius match is missing, 0.5 when Sirius fails to propose an annotation, and treat ISDB-LOTUS zero matches as significant novelty signals). Aggregate these similarities into a unified K-value that models expert preference for each feature, then filter and rank the dataframe by K in descending order. Export results as a TSV file mapping each feature to its K-ranked confidence tier, suitable for downstream visualization (e.g., coloring FBMN graph nodes by K rank).

## Related tools

- **GNPS (Global Natural Products Social Molecular Networking)** (Generates spectral library matches and FBMN clustering; outputs library search results and feature network topology) — https://gnps.ucsd.edu
- **ISDB-LOTUS (Isomeric Spectral DataBase of Natural Products)** (Provides CFM-ID 4.0 spectral similarity annotations via get_cfm_annotation; matched against 0.02 Da mass tolerance) — https://zenodo.org/records/8287341
- **Sirius 6** (Supplies structure identification with Confidence Approximate score; outputs structure_identifications.tsv ranked by CSI:FingerId and COSMIC)
- **MatchMS** (Underlying spectral comparison library used by ISDB-LOTUS annotation; computes cosine similarity) — https://github.com/matchms/matchms
- **MS2DECIDE** (Python library implementing the K_estimation function; orchestrates annotation aggregation and K-value ranking) — https://github.com/MejriY/MS2DECIDE

## Examples

```
from ms2decide.K_estimation import K_estimation
K_estimation()
```

## Evaluation signals

- Output TSV file has non-null K-values for all features with ≥1 annotation match; K-range is typically 0.0–1.0 with clear separation between high-consensus and low-consensus features.
- Tanimoto fallback defaults (0.7, 0.5) appear in the calculation only for features where GNPS–Sirius or Sirius matching failed; validate fallback usage by spot-checking source annotations.
- Total feature count in output TSV ≤ total features in input MGF (filtered by confidence thresholds); zero-annotation features are either excluded or flagged with K=0.
- When results are mapped onto FBMN graphs using K as a continuous color code, high-K clusters should correspond to well-annotated regions (multiple spectral library hits and structural predictions in agreement).
- Redundant feature IDs in Sirius input file are resolved before import (check for unique values in 'mappingFeatureId' column); absence of 'DataFrame index must be unique' error confirms clean Sirius input.

## Limitations

- Default Tanimoto similarity values (0.7, 0.5) are heuristic approximations; actual pairwise chemical similarity is unavailable when tools fail to match. Users should inspect these fallback cases manually for high-stakes identifications.
- ISDB-LOTUS strict library search (0.02 Da tolerance) is conservative; novel or unusual compounds are more likely to yield zero matches, which are treated as novelty signals rather than annotation failures.
- Sirius batch mode with Confidence Approximate score may fail to propose structures in some cases; a value of 0.5 is assigned to handle missing Sirius annotations, but structural confidence is degraded.
- GNPS FBMN with library score threshold 0.001 can produce spurious matches; users are advised to increase threshold (e.g., 0.1) to reduce false positives, but this reduces annotation coverage.
- Iterative weighted GNPS analog search launches 27 jobs and can take up to three hours; computational cost is high for large feature sets.

## Evidence

- [readme] Integrates annotation data from multiple sources: GNPS, ISDB-LOTUS, and Sirius.: "Integrates annotation data from multiple sources: GNPS, ISDB-LOTUS, and Sirius."
- [readme] In scenarios where there is no match with GNPS or no match with Sirius, the tanimoto between GNPS and Sirius cannot be calculated. Hence, a default value of 0.7 was assigned to T_gs and T_gi in these instances.: "In scenarios where there is no match with GNPS or no match with Sirius, the tanimoto between GNPS and Sirius cannot be calculated. Hence, a default value of 0.7 was assigned"
- [readme] Sirius annotations were performed in batch mode by using Sirius 6. we utilized the Confidence Approximate score. Unfortunately, in some cases, Sirius was not able to propose an annotation. To remedy, we associated a value of 0.5 to Sirius matching score.: "To remedy, we associated a value of 0.5 to Sirius matching score."
- [readme] For ISDB-LOTUS, since a strict library search was applied (0.02 Da), we considered a zero answer as an important information regarding our definition of novelty.: "For ISDB-LOTUS, since a strict library search was applied (0.02 Da), we considered a zero answer as an important information"
- [readme] Annotations from GNPS, Sirius, and ISDB-LOTUS are compiled into a unified dataframe. The dataframe is filtered and sorted by K-values.: "Annotations from GNPS, Sirius, and ISDB-LOTUS are compiled into a unified dataframe. The dataframe is filtered and sorted by K-values."
- [readme] By following these steps, you can effectively use the K_estimation function to process and aggregate your multiannotated MS/MS spectra. In combination with FBMN data you can upload the K.tsv on your graph program and map with a continuous color code the ranks proposed by the knownness score K.: "In combination with FBMN data you can upload the K.tsv on your graph program and map with a continuous color code the ranks proposed by the knownness score K."
