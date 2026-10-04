---
name: slurm-job-debug-template
description: Use this skill to render, submit, and inspect a minimal Slurm smoke job before submitting heavier workloads on a real cluster.
---

## Purpose
Generate a conservative `sbatch` template, submit it to Slurm, and capture the accounting record needed to verify the cluster path end to end.

## When to use
- You need a tiny Slurm smoke job.
- You want a reusable starting point for queue, environment, and log validation.

## When not to use
- You need multi-node or GPU tuning guidance beyond a first smoke job.

## Inputs
- Command string
- Optional job name, partition, runtime, memory, and output path

## Outputs
- Rendered `sbatch` script
- JSON submission and `sacct` summary

## Requirements
- Python 3.13+
- `sbatch`, `squeue`, and `sacct`
- A real Slurm cluster

## Procedure
1. Run `python3 skills/hpc/slurm-job-debug-template/scripts/render_sbatch.py --command "echo hello" --job-name smoke`.
2. Inspect the generated script or save it with `--out`.
3. Submit a verified smoke job with `python3 skills/hpc/slurm-job-debug-template/scripts/submit_smoke_job.py --partition cpu --job-name slurm-smoke --sleep 2 --out slurm/reports/slurm-smoke.json`.
4. Inspect the returned `job_id`, the log paths in `slurm/logs/`, and the `accounting` block from `sacct`.

## Validation
- Renderer exits successfully.
- Output contains `#SBATCH` directives and the command body.
- Submitted smoke job reaches `State=COMPLETED`.
- `ExitCode` is `0:0`.

## Failure modes and fixes
- Missing partition/account information: add them before submission.
- Output paths wrong: switch to cluster-appropriate scratch or log paths.
- `sacct` lags briefly after completion: retry once accounting catches up.

## Safety and limits
- Keep resource requests small for initial smoke jobs.
- Use a CPU partition and a short walltime for smoke checks.

## Examples
- `python3 .../render_sbatch.py --command "python analysis.py" --partition short --time 00:10:00 --mem 2G`
- `python3 .../submit_smoke_job.py --partition cpu --job-name slurm-smoke --sleep 1`

## Provenance
- Slurm quick start: https://slurm.schedmd.com/quickstart.html
- Slurm `sbatch` reference: https://slurm.schedmd.com/sbatch.html
- `sacct` reference: https://slurm.schedmd.com/sacct.html

## Related skills
- `snakemake-toy-workflow-starter`
