---
name: nextflow-hello-workflow
description: Use this skill to run a minimal Nextflow workflow through the repo-managed Java and Nextflow prefix, either locally or on the Slurm cluster. Do not use it for containerized production pipelines.
---

## Purpose
Verify that the repository-local Nextflow runtime works and execute a tiny deterministic workflow end to end, including a Slurm executor path.

## When to use
- You need a small, local Nextflow smoke test.
- You want a known-good example before adapting a larger workflow.
- You want to confirm that Nextflow can submit tiny jobs to the local Slurm cluster.

## When not to use
- You need container orchestration or production pipeline packaging.

## Inputs
- `examples/main.nf`
- Optional `--out-dir`, `--work-dir`, and executor settings
- For cluster runs: `--executor slurm` plus an optional partition

## Outputs
- Published greeting files in the chosen output directory
- JSON summary with the runtime version, produced files, and optional Slurm trace/accounting details

## Requirements
- The repo-local toolchain at `slurm/envs/nextflow-tools`
- Local filesystem write access for the work and output directories
- For cluster verification: `sbatch` and `sacct` access on the local Slurm cluster

## Procedure
1. Run `python3 skills/reproducible-workflows/nextflow-hello-workflow/scripts/run_nextflow_hello.py --out-dir scratch/nextflow-hello/results` for a local smoke path.
2. Run `python3 skills/reproducible-workflows/nextflow-hello-workflow/scripts/run_nextflow_hello.py --executor slurm --partition cpu --out-dir scratch/nextflow-hello-slurm/results --work-dir scratch/nextflow-hello-slurm/work --summary-out scratch/nextflow-hello-slurm/summary.json` for a cluster-backed smoke path.
2. Inspect the returned `files` list and the output directory contents.
3. For Slurm runs, inspect `trace_rows` and `slurm_jobs` in the summary.
4. Reuse the pattern in `examples/main.nf` when bootstrapping larger pipelines.

## Validation
- `nextflow info` succeeds through the repo-local wrapper environment.
- `nextflow run` completes without errors.
- Four greeting files are published to the output directory.
- For Slurm runs, the trace file contains native job IDs and `sacct` reports `COMPLETED` with `ExitCode 0:0`.

## Failure modes and fixes
- `java: command not found`: run through the provided wrapper script instead of calling `nextflow` directly.
- Write-path issues: switch `--out-dir` and `--work-dir` to writable locations.
- Raw `nextflow run` treats a relative script name like a remote pipeline: use the wrapper or pass an explicit local path.
- Slurm queue delays: rerun on `cpu` or adjust the partition if the cluster is busy.

## Safety and limits
- This skill verifies local and tiny Slurm-backed executor paths only.
- It does not prove container, cloud, or production-scale execution readiness.

## Examples
- `python3 .../run_nextflow_hello.py --out-dir scratch/nextflow-hello/results --work-dir scratch/nextflow-hello/work`
- `python3 .../run_nextflow_hello.py --executor slurm --partition cpu --summary-out scratch/nextflow-hello-slurm/summary.json`

## Provenance
- Nextflow installation docs: https://www.nextflow.io/docs/latest/install.html
- Nextflow first-script tutorial: https://www.nextflow.io/docs/latest/your-first-script.html
- Nextflow executor docs: https://www.nextflow.io/docs/latest/executor.html
- Slurm quick start: https://slurm.schedmd.com/quickstart.html

## Related skills
- `snakemake-toy-workflow-starter`
- `nf-core-pipeline-list`
- `slurm-job-debug-template`
