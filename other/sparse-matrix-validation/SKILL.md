---
name: sparse-matrix-validation
description: Use when after generating a count matrix from fragment data using pp.add_tile_matrix, pp.make_peak_matrix, or pp.make_gene_matrix in SnapATAC2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0091
  tools:
  - SnapATAC2
  - Python
  - Scanpy
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- A Python/Rust package for single-cell epigenomics analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_snapatac2
    doi: 10.1038/s41592-023-02139-9
    title: snapatac2
  dedup_kept_from: coll_snapatac2
schema_version: 0.2.0
---

# sparse-matrix-validation

## Summary

Validation of sparse count matrices generated from single-cell ATAC-seq fragment data to ensure matrix shape, sparsity structure, and quantitative correctness before downstream analysis. This skill verifies that tile-based or peak-based count matrices possess expected dimensions, contain appropriately distributed non-zero entries across cells and genomic features, and reflect genuine chromatin accessibility signal.

## When to use

After generating a count matrix from fragment data using pp.add_tile_matrix, pp.make_peak_matrix, or pp.make_gene_matrix in SnapATAC2. Validation is essential whenever you transition from fragment-level preprocessing to matrix-based analysis (dimension reduction, clustering, peak calling) to detect generation errors, parameter misconfigurations, or data corruption that would propagate through the pipeline.

## When NOT to use

- Input is already a validated feature table (e.g., pre-computed matrix from a completed SnapATAC2 workflow); re-validation is redundant.
- Fragment file has not yet been imported into AnnData; validate fragment import separately before matrix generation.
- You are performing quality control on raw sequencing reads prior to alignment; use fragment-level QC (e.g., mapping rate, duplicate removal) instead.

## Inputs

- AnnData object with .obsm['fragment_paired'] or .obsm['fragment_single'] containing aligned fragment data
- Tile coordinate definitions or peak BED file used for matrix generation
- Matrix generation parameters (counting strategy, bin size or peak coordinates)

## Outputs

- Validated sparse count matrix (n_obs × n_vars) stored in .X or .obsm
- Summary statistics: matrix dimensions, sparsity fraction, entry value range, non-zero count distribution across cells and features

## How to apply

Inspect the resulting matrix object for three key invariants: (1) verify matrix shape (n_obs × n_vars) matches the number of cells (observations) and genomic tiles or peaks (variables) as defined by your binning or peak-calling parameters; (2) confirm the matrix contains non-zero entries distributed across both cells and genomic features, indicating signal is not concentrated in a pathological subset; (3) validate sparsity is appropriate for ATAC-seq (typically 85–99% sparse depending on sequencing depth and genome resolution), and that entry values are counts (non-negative integers). These checks catch mismatches between fragment input and matrix construction parameters (e.g., wrong genome build, misaligned tile coordinates, or empty fragment sets).

## Related tools

- **SnapATAC2** (Provides pp.add_tile_matrix, pp.make_peak_matrix, and pp.make_gene_matrix functions for count matrix generation from fragment data; matrix is stored in AnnData format for validation) — https://github.com/scverse/SnapATAC2
- **Python** (Language for writing validation scripts to inspect matrix shape, sparsity, and entry distributions)
- **Scanpy** (Seamless integration with SnapATAC2; provides utility functions for matrix inspection and summary statistics)

## Examples

```
import snapatac2 as snap; adata = snap.pp.add_tile_matrix(adata, counting_strategy='paired_insertion'); print(f'Matrix shape: {adata.X.shape}'); print(f'Sparsity: {1.0 - adata.X.nnz / (adata.n_obs * adata.n_vars):.2%}'); assert adata.X.nnz > 0, 'No non-zero entries in matrix'
```

## Evaluation signals

- Matrix shape (n_obs, n_vars) equals (num_cells, num_tiles_or_peaks) as expected from input parameters
- All matrix entries are non-negative integers; no NaN or infinite values present
- Sparsity (fraction of zero entries) is within expected range for ATAC-seq (typically 0.85–0.99)
- Non-zero entry counts are distributed across cells and features (not concentrated in a few cells or a few genomic regions), suggesting uniform signal rather than artifact
- Sum of counts per cell and per feature align with expected sequencing depth and open chromatin landscape (no cells with zero counts, no features with zero counts across all cells if feature was included in generation)

## Limitations

- Validation does not assess biological quality or signal-to-noise ratio; a well-formed matrix with low sequencing depth or high background will pass structural checks but may yield poor clustering or peak calls.
- Sparsity expectations may vary by organism, cell type, and sequencing platform; thresholds (e.g., 85–99%) are heuristic and should be calibrated against domain knowledge.
- Matrix validation cannot distinguish between true chromatin accessibility and technical artifacts (e.g., mitochondrial DNA contamination, barcode collisions) that are preserved in the count matrix; sample-level and cell-level QC filters should precede matrix generation.

## Evidence

- [other] Extract the resulting count matrix and verify matrix shape (n_obs × n_vars) matches tile coordinates.: "Extract the resulting count matrix and verify matrix shape (n_obs × n_vars) matches tile coordinates."
- [other] Validate that count matrix contains non-zero entries and that paired-insertion counts are distributed across cells and genomic tiles as expected.: "Validate that count matrix contains non-zero entries and that paired-insertion counts are distributed across cells and genomic tiles as expected."
- [methods] Matrix operation including pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix: "Matrix operation including pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix"
- [readme] SnapATAC2: A Python/Rust package for single-cell epigenomics analysis: "SnapATAC2: A Python/Rust package for single-cell epigenomics analysis"
- [readme] Seamless integration with other single-cell analysis packages such as Scanpy.: "Seamless integration with other single-cell analysis packages such as Scanpy."
