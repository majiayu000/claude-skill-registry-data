---
name: scanpy-qc-starter
description: Use this skill to run a lightweight Scanpy QC pass on a toy count matrix with the repository-managed Scanpy environment.
---

## Purpose
Provide a reproducible starting point for Scanpy-based QC work with toy matrix inputs, AnnData export, and a small verification report.

## When to use
- You want to verify Scanpy and AnnData on this repository.
- You need a minimal example layout for single-cell QC work.

## When not to use
- You need GPU-backed modeling or integrated single-cell workflows.

## Inputs
- Tab-separated matrix with gene names in the first column and sample or cell columns after that

## Outputs
- Summary statistics about matrix dimensions and zero fraction
- QC summary JSON with per-cell metrics
- Optional `.h5ad` artifact

## Requirements
- `slurm/envs/scanpy`
- Run with `slurm/envs/scanpy/bin/python`

## Procedure
1. Inspect `examples/toy_counts.tsv`.
2. Run `python3 skills/transcriptomics/scanpy-qc-starter/scripts/preflight_counts.py --input skills/transcriptomics/scanpy-qc-starter/examples/toy_counts.tsv`.
3. Run `slurm/envs/scanpy/bin/python skills/transcriptomics/scanpy-qc-starter/scripts/run_scanpy_qc.py --input skills/transcriptomics/scanpy-qc-starter/examples/toy_counts.tsv --summary-out skills/transcriptomics/scanpy-qc-starter/assets/scanpy_qc_summary.json --h5ad-out scratch/scanpy/toy_counts_qc.h5ad`.
4. Inspect `total_counts`, `n_genes_by_counts`, and `pct_counts_mt` in the summary output.

## Validation
- Preflight script exits successfully.
- Reported dimensions match the example matrix.
- Scanpy writes a valid `.h5ad` file.
- QC summary includes per-cell metrics.

## Failure modes and fixes
- Ragged rows: normalize the input to a rectangular TSV.
- Non-numeric counts: clean or coerce the count columns before QC.
- Missing Scanpy environment: recreate `slurm/envs/scanpy` and rerun with that interpreter.

## Safety and limits
- This is a lightweight QC starter, not a full single-cell analysis workflow.
- Toy matrices are for environment verification and examples only.

## Examples
- `python3 .../preflight_counts.py --input skills/transcriptomics/scanpy-qc-starter/examples/toy_counts.tsv`
- `slurm/envs/scanpy/bin/python .../run_scanpy_qc.py --input skills/transcriptomics/scanpy-qc-starter/examples/toy_counts.tsv --summary-out scratch/scanpy/summary.json --h5ad-out scratch/scanpy/toy_counts.h5ad`

## Provenance
- Scanpy docs: https://scanpy.readthedocs.io/en/stable/
- Scanpy installation docs: https://scanpy.readthedocs.io/en/stable/installation.html
- Scanpy QC metrics API: https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.calculate_qc_metrics.html
- AnnData docs: https://anndata.readthedocs.io/en/latest/index.html
- scvi-tools docs: https://docs.scvi-tools.org/en/latest/index.html

## Related skills
- `snakemake-toy-workflow-starter`
