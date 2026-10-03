---
name: fragment-ion-matching
description: Use when you have two tandem mass spectra (query and reference) with
  precursor m/z and fragment ion peaks, and you need to identify which fragment ions
  correspond between them to assess spectral similarity, detect structural variants,
  or validate compound identifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SIMILE
  - Python
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-022-30118-9
  title: SIMILE
evidence_spans:
- SIMILE (Significant Interrelation of MS/MS Ions via Laplacian Embedding) is a Python
  library
- is a Python library for interrelating fragmentation spectra with significance estimation
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_simile_cq
    doi: 10.1038/s41467-022-30118-9
    title: SIMILE
  dedup_kept_from: coll_simile_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-022-30118-9
  all_source_dois:
  - 10.1038/s41467-022-30118-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragment-ion-matching

## Summary

Align fragment ions between paired tandem mass spectra using maximum weight matching, computing mass deltas and statistical significance scores to identify structurally related compounds. This skill generates a structured report of matched ion pairs with confidence metrics suitable for spectral library annotation and compound relationship discovery.

## When to use

You have two tandem mass spectra (query and reference) with precursor m/z and fragment ion peaks, and you need to identify which fragment ions correspond between them to assess spectral similarity, detect structural variants, or validate compound identifications. Use this when you want significance-tested alignment rather than simple peak matching, especially for spectra that differ in chemical structure.

## When NOT to use

- Spectra from fundamentally different compound classes where no meaningful fragment ion correspondence is expected (e.g., lipid vs. peptide); SIMILE will still produce matches but with low statistical significance.
- Single spectrum analysis without a reference spectrum to match against; maximum weight matching requires paired spectra.
- Precursor m/z values are unknown or unreliable; neutral loss-based counting requires accurate precursor mass.

## Inputs

- Query tandem mass spectrum (precursor m/z, fragment ion peaks with m/z and intensity values)
- Reference tandem mass spectrum (precursor m/z, fragment ion peaks with m/z and intensity values)
- Tolerance parameter (mass accuracy threshold in ppm or Da)

## Outputs

- Matching ions report table (matched ion pairs with m/z, intensity, mass delta, similarity score, p-value)
- Similarity matrix (S: fragmentation similarity between all fragment ion pairs)
- Maximum weight matching matrix (M: optimal bipartite matching between spectra)
- Comparison matrix (C: symmetric vs. asymmetric match classification)
- Statistical significance scores and p-values for matched pairs

## How to apply

Load the two spectra with their precursor m/z values and fragment ion peaks (m/z and intensity). Execute SIMILE's maximum weight matching algorithm to align fragment ions based on a similarity matrix that captures both mass difference frequency (property a: common mass deltas) and fragmentation ancestry/descendancy relationships (property b: laplacian embedding of ion relationships). The algorithm computes mass deltas (m/z differences) for each matched pair and assigns statistical significance scores (p-values) via z-testing against a null distribution derived from permuted intra- and inter-spectral similarities. Extract the matching ions report containing matched ion identifiers, m/z values, intensity values, mass delta values, similarity scores, and p-values along with precursor m/z and spectrum identifiers as metadata. Optionally use precursor-based neutral loss difference counts in addition to original m/z difference counts for improved specificity.

## Related tools

- **SIMILE** (Core library implementing maximum weight matching, laplacian embedding-based fragment similarity, and z-test significance calculation for spectrum alignment) — https://github.com/biorack/simile
- **Python** (Execution environment for SIMILE library and workflow orchestration)

## Examples

```
import simile as sml
S, spec_ids = sml.similarity_matrix(mzs, pmzs=pmzs, tolerance=0.1)
M = sml.multiple_match(S, spec_ids)
C = sml.sym_compare(M, spec_ids)
spec_scores, pval, null_dist = sml.z_test(S, M, C, spec_ids, return_dist=True)
df = sml.matching_ions_report(S, M, C, mzs, pmzs)
```

## Evaluation signals

- Matched ion pairs have mass deltas (m/z differences) that cluster around biologically meaningful neutral loss values (e.g., 18 for water loss, 44 for CO₂), indicating correspondence to real fragmentation pathways.
- P-values for matched ions fall below significance threshold (typically p < 0.05), confirming that matches are unlikely due to random chance under the permutation null distribution.
- Symmetric matches (reciprocal alignments between spectra) are marked as 'pro' in the comparison matrix and constitute the majority of high-scoring matches, indicating robust bidirectional correspondence.
- Reported metadata (precursor m/z, spectrum identifiers, instrument source) can be traced back to input spectra and match assignment logic is auditable through the matching matrix M.
- Mass delta distribution in the report exhibits expected ion fragmentation chemistry (neutral losses, isotope patterns) rather than random drift, validating the biological relevance of alignment.

## Limitations

- Performance depends on fragment ion density and spectral complexity; sparse spectra or heavily modified compounds may yield few matches even when structurally related.
- The laplacian embedding similarity measure assumes that ancestor and descendant fragment ions are informative about sibling relationships; this may not hold for highly unusual fragmentation pathways or small molecules with limited fragmentation chains.
- Multiple comparison statistics and null distribution generation via permutation can be computationally expensive for large spectral libraries; V2 documentation notes optimization but does not specify scalability limits.
- Maximum weight matching is constrained to one-to-one ion correspondences; multiply charged or doubly-fragmented ions that generate multiple m/z peaks may be under-represented compared to pairwise matching.

## Evidence

- [readme] Maximum weight matching algorithm used to align fragment ions between spectra: "Maximum weight matching is used instead of original monotonic alignment method with improved performance"
- [readme] Laplacian embedding captures both mass difference frequency and fragmentation ancestry properties: "Fragment ions are similar if the difference in mass between them is common. Fragment ions are similar if their ancestor and descendent fragment ions are similar."
- [readme] P-values are derived from null distribution based on permuted intra- and inter-spectral comparisons: "a null distribution generated by permuting intra and inter spectral fragment similarity scores to yield p-values"
- [intro] Matching ions report contains matched ion pairs with mass deltas, scores, and metadata: "Matching ions report summarizing all scores and mass deltas with metadata"
- [readme] Neutral loss counts can augment original m/z difference counts: "Precursor-based neutral loss difference counts can be used in addition to the original MZ difference counts"
