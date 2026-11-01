---
name: similarity-matrix-export
description: Use when after computing pairwise similarity scores across a collection of preprocessed mass spectra using matchms similarity measures (Cosine-related, molecular fingerprint-based, or metadata-related assessments), use this skill to persist the resulting similarity matrix to a named output file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - matchms
  - Python
derived_from:
- doi: 10.21105/joss.02411
  title: matchms
evidence_spans:
- Matchms offers an array of tools for metadata cleaning and validation
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.21105/joss.02411
    title: matchms
  dedup_kept_from: coll_matchms
schema_version: 0.2.0
---

# similarity-matrix-export

## Summary

Export pairwise similarity scores computed across mass spectra into a structured matrix file format for downstream analysis and storage. This skill bridges spectrum comparison workflows and result persistence, enabling efficient handling of large-scale spectral datasets through sparse and dense matrix serialization.

## When to use

After computing pairwise similarity scores across a collection of preprocessed mass spectra using matchms similarity measures (Cosine-related, molecular fingerprint-based, or metadata-related assessments), use this skill to persist the resulting similarity matrix to a named output file. Particularly valuable when comparing several hundred thousands of spectra, where sparse data formats reduce storage footprint.

## When NOT to use

- Similarity scores have not yet been computed; export cannot generate similarities from raw spectra alone—apply a similarity measure first.
- Output is intended for immediate in-memory manipulation within the same Python session; direct array/dataframe retention is more efficient than write-read cycles.
- Input spectra are still in raw, unprocessed format (mzML, mzXML, etc.); run preprocessing and cleaning steps before similarity computation.

## Inputs

- Pairwise similarity scores matrix (numerical, typically float64)
- Spectrum identifiers or metadata labels (for row/column indexing)
- Output file path and desired format specification

## Outputs

- Serialized similarity matrix file (e.g., .npy, .npz, .csv, sparse COO/CSR format)
- Optionally: spectrum index/metadata mapping file

## How to apply

Following computation of pairwise similarity scores via matchms similarity measures (e.g., CosineGreedy, molecular fingerprint comparators), invoke matchms' export functionality to serialize the score matrix to a supported output format (commonly NumPy arrays, sparse matrices, or CSV). The choice of format depends on downstream use: sparse formats (e.g., COO or CSR) are preferred when only a subset of scores are computed or relevant, reducing both disk I/O and memory overhead. Dense formats are appropriate for smaller collections or when all pairwise comparisons must be retained. Validate the export by confirming file integrity, checking matrix dimensions match the input spectrum count, and spot-checking symmetry properties if the comparison was symmetric.

## Related tools

- **matchms** (Provides the similarity computation and export API; handles format serialization and sparse matrix support for efficient storage of pairwise similarity scores.) — https://github.com/matchms/matchms
- **Python** (Scripting language and runtime environment for orchestrating matchms export workflows and post-processing matrix outputs.)

## Evaluation signals

- Output file exists and is readable by standard array/matrix libraries (NumPy, SciPy, Pandas).
- Matrix dimensions are square (or rectangular for asymmetric comparisons) and equal to the number of input spectra.
- Non-zero entry count in sparse formats is consistent with the number of computed similarity scores; sparse matrix density is substantially lower than dense equivalents when appropriate.
- Spot-check: a few sampled similarity values from the exported matrix match the in-memory scores before export.
- File size is proportional to sparsity level; sparse formats yield smaller footprint than dense for datasets with many zero or uncomputed scores.

## Limitations

- Export performance scales with matrix size; very large all-to-all comparisons (millions of spectra) may require chunked or streaming export to avoid memory exhaustion.
- Sparse matrix formats (COO, CSR) sacrifice random-access efficiency for storage; dense formats are faster for subsequent dense operations but consume more disk space.
- Metadata and spectrum identifiers are not automatically embedded in all export formats; separate index files may be needed to map rows/columns back to original spectra.
- Format choice (dense vs. sparse) is user-determined; no automatic optimization is performed based on actual sparsity of the score matrix.

## Evidence

- [other] Apply the molecular fingerprint-based similarity measure available in matchms to compute pairwise similarity scores across all spectra. 3. Export the resulting similarity scores matrix to a named output file.: "compute pairwise similarity scores across all spectra. 3. Export the resulting similarity scores matrix to a named output file"
- [readme] Matchms enhances efficiency by using faster similarity measures for initial pre-selection and supports storing results in sparse data formats, enabling the comparison of several hundred thousands of spectra.: "supports storing results in sparse data formats, enabling the comparison of several hundred thousands of spectra"
- [readme] A key feature of matchms is its ability to apply various pairwise similarity measures for comparing extensive amounts of spectra. This encompasses not only common Cosine-related scores but also molecular fingerprint-based comparisons and other metadata-related assessments.: "various pairwise similarity measures for comparing extensive amounts of spectra. This encompasses not only common Cosine-related scores but also molecular fingerprint-based comparisons and other"
- [readme] Sparse scores array: We realized that many matchms-based workflows aim to compare many-to-many spectra whereby not all pairs and scores are equally important... For this reason, we now shifted to a sparse handling of scores in matchms (that means: only storing actually computed, non-null values).: "sparse handling of scores in matchms (that means: only storing actually computed, non-null values)"
