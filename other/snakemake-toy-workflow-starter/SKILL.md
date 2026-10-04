---
name: snakemake-toy-workflow-starter
description: Use this skill to run a tiny Snakemake workflow through the repo-managed Snakemake prefix and inspect deterministic toy outputs.
---

## Purpose
Provide a small, readable Snakemake workflow that can be executed locally, inspected, and adapted into larger scientific pipelines.

## When to use
- You need a seed workflow layout for scientific pipeline work.
- You want a tiny example before adapting a larger pipeline.

## When not to use
- You need production-grade workflow packaging or containerization.

## Inputs
- `examples/data/input.txt`
- `examples/config.yaml`

## Outputs
- `results/copied.txt`
- `results/summary.json`
- Optional run summary JSON from the wrapper script

## Requirements
- The repo-local Snakemake runtime at `slurm/envs/snakemake`
- Local filesystem write access for a scratch workspace

## Procedure
1. Review `examples/Snakefile` and `examples/config.yaml`.
2. Run `python3 skills/reproducible-workflows/snakemake-toy-workflow-starter/scripts/check_workflow_layout.py`.
3. Run `python3 skills/reproducible-workflows/snakemake-toy-workflow-starter/scripts/run_snakemake_workflow.py --workspace scratch/snakemake-toy-workflow --summary-out scratch/snakemake-toy-workflow/run_summary.json`.
4. Inspect `results/copied.txt`, `results/summary.json`, and the wrapper summary JSON.

## Validation
- Layout script succeeds.
- `snakemake --version` works from the repo-managed prefix.
- The workflow completes with `--cores 1`.
- The summary JSON reports the copied toy content and a stable checksum.

## Failure modes and fixes
- Missing Snakemake: recreate `slurm/envs/snakemake`.
- Wrong working directory: pass absolute or repo-relative paths when invoking Snakemake.
- Stale workspace contents: rerun through the wrapper, which reseeds a clean workspace.

## Safety and limits
- This is a small local workflow only.
- It verifies local execution, not cluster submission or containerized workflow deployment.

## Examples
- `python3 .../check_workflow_layout.py`
- `python3 .../run_snakemake_workflow.py --workspace scratch/snakemake-toy-workflow --summary-out scratch/snakemake-toy-workflow/run_summary.json`

## Provenance
- Snakemake documentation: https://snakemake.readthedocs.io/en/stable/
- Snakemake installation guide: https://snakemake.readthedocs.io/en/stable/getting_started/installation.html
- Snakemake tutorial: https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html

## Related skills
- `slurm-job-debug-template`
- `scanpy-qc-starter`
- `nextflow-hello-workflow`
- `nf-core-pipeline-list`
