---
name: feature-pair-ranking
description: Use when you have two feature matrices from different modalities (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - haCCA
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.08.20.608773v2
  title: haCCA
evidence_spans:
- haCCA, a workflow utilizing high Correlated feature pairs combined with a modified
  spatial morphological alignment
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hacca_cq
    doi: 10.1101/2024.08.20.608773v2
    title: haCCA
  dedup_kept_from: coll_hacca_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.08.20.608773v2
  all_source_dois:
  - 10.1101/2024.08.20.608773v2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-pair-ranking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify and rank high-correlation feature pairs between two omics datasets (e.g., spatial transcriptome and metabolome) by computing pairwise correlation coefficients and filtering by correlation threshold. This ranking prioritizes the strongest cross-modal associations for downstream integration and alignment.

## When to use

You have two feature matrices from different modalities (e.g., gene expression and metabolite abundance) measured on the same samples or spots, and you need to discover which features are most strongly co-varying across modalities to guide spot-to-spot data integration or multimodal alignment.

## When NOT to use

- Input datasets have no expected cross-modal correlation structure (e.g., unrelated tissue types or experimental conditions).
- Feature matrices are already aligned or pre-filtered to contain only known co-varying pairs; ranking would be redundant.
- Sample/spot size is very small (n < 10) or correlation estimates would be unreliable due to statistical noise.

## Inputs

- Spatial transcriptome feature matrix (n_spots × n_genes, numpy.ndarray or scipy.sparse matrix)
- Metabolome feature matrix (n_spots × n_metabolites, numpy.ndarray or scipy.sparse matrix)
- Correlation threshold (float, absolute value, default ~0.7)
- Correlation metric choice (string: 'pearson' or 'spearman')

## Outputs

- Ranked feature pair list (DataFrame or structured array with columns: transcriptome_feature, metabolome_feature, correlation_coefficient, abs_correlation)
- Filtered high-correlation pairs subset (subset of input feature matrices corresponding to selected pairs)

## How to apply

Load the spatial transcriptome feature matrix (X_transcriptome) and metabolome feature matrix (X_metabolome) as numpy arrays or from .h5ad files. Compute pairwise Pearson or Spearman correlation coefficients between all transcriptome features and all metabolome features. Apply a correlation threshold (e.g., |r| ≥ 0.7) to retain only high-correlation pairs and discard weak associations. Rank the filtered pairs by absolute correlation coefficient in descending order. Output a ranked list of feature pairs with their correlation scores and metadata (feature names, modalities). This ranking serves as input to the spatial morphological alignment module to ensure only the most reliable cross-modal signals guide registration.

## Related tools

- **haCCA** (Workflow framework that uses high-correlated feature pair ranking as a core module before spatial morphological alignment) — github.com/LittleLittleCloud/haCCA

## Examples

```
import numpy as np
from scipy.stats import pearsonr
a_h5ad = sc.read_h5ad('/path/to/transcriptome.h5ad')
b_h5ad = sc.read_h5ad('/path/to/metabolome.h5ad')
X_t = a_h5ad.X.toarray()
X_m = b_h5ad.X.toarray()
corr_matrix = np.corrcoef(X_t.T, X_m.T)[:X_t.shape[1], X_t.shape[1]:]
pairs = [(i, j, corr_matrix[i, j]) for i, j in zip(*np.where(np.abs(corr_matrix) >= 0.7))]
pairs_sorted = sorted(pairs, key=lambda x: abs(x[2]), reverse=True)
```

## Evaluation signals

- Correlation coefficients are within expected range (typically |r| ∈ [−1, 1]) and satisfy the applied threshold.
- Ranked list is sorted in descending order by absolute correlation coefficient with no ties broken inconsistently.
- Feature names in output pairs are present in both input feature matrices and span biological relevance (e.g., metabolites known to be produced by genes in the ranked pairs).
- Number of retained pairs after filtering is reasonable relative to input dimensionality (not all pairs retained, nor zero pairs).
- Downstream spatial alignment using top-ranked pairs produces lower registration error or higher spot-to-spot matching accuracy than unranked or random pairs.

## Limitations

- Pearson correlation assumes linear relationships; non-linear cross-modal associations may be missed.
- Correlation threshold is data-dependent and must be tuned; no universal cutoff is provided in the article.
- High correlation does not imply causality or direct functional interaction; pairs may be confounded by spatial gradients or shared environmental factors.
- Sparsity in metabolome data (many zero values) may inflate or deflate correlation estimates; sparse-aware metrics are not discussed.

## Evidence

- [other] Compute pairwise Pearson or Spearman correlation coefficients between all transcriptome features and all metabolome features.: "Compute pairwise Pearson or Spearman correlation coefficients between all transcriptome features and all metabolome features."
- [other] Filter feature pairs by correlation threshold to retain only high-correlation pairs.: "Filter feature pairs by correlation threshold to retain only high-correlation pairs."
- [other] Rank filtered pairs by absolute correlation coefficient in descending order.: "Rank filtered pairs by absolute correlation coefficient in descending order."
- [intro] haCCA utilizes high correlated feature pairs as a core component of its workflow, which are combined with modified spatial morphological alignment: "haCCA utilizes high correlated feature pairs as a core component of its workflow, which are combined with modified spatial morphological alignment"
- [intro] ensure high resolution and accuracy of spot-to-spot data integration of spatial transcriptomes and metabolomes: "ensure high resolution and accuracy of spot-to-spot data integration of spatial transcriptomes and metabolomes"
