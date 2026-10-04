---
name: nf-core-pipeline-list
description: Use this skill to verify the repo-managed nf-core tools install and retrieve a cleaned summary of available pipelines. Do not use it for interactive launch flows or full pipeline downloads.
---

## Purpose
Check that nf-core tools run correctly in the repo-local environment and return a deterministic pipeline summary.

## When to use
- You need a quick nf-core installation check.
- You want a compact machine-readable view of available nf-core pipelines.

## When not to use
- You need interactive parameter entry with `nf-core launch`.
- You need to download or execute a full nf-core pipeline.

## Inputs
- Optional `--sort` and `--limit`

## Outputs
- Cleaned JSON summary with local and remote nf-core pipeline metadata

## Requirements
- The repo-local toolchain at `slurm/envs/nextflow-tools`
- Network access for the remote pipeline catalog

## Procedure
1. Run `python3 skills/reproducible-workflows/nf-core-pipeline-list/scripts/list_nfcore_pipelines.py --limit 5`.
2. Inspect `counts.remote_workflows` and the returned `remote_workflows` entries.
3. Use the names and release metadata as a starting point for later nf-core workflows.

## Validation
- The wrapper runs `nf-core pipelines list` successfully through the repo-local environment.
- The malformed multiline JSON emitted by the CLI is cleaned and parsed.
- At least one remote pipeline is returned.

## Failure modes and fixes
- JSON parse issues: use the provided wrapper instead of calling `nf-core --json` directly.
- Empty remote list: check outbound network access and retry.

## Safety and limits
- This skill verifies catalog access only.
- It does not prove that any specific nf-core pipeline can be executed locally.

## Examples
- `python3 .../list_nfcore_pipelines.py --sort pulled --limit 3`

## Provenance
- nf-core tools installation docs: https://nf-co.re/docs/nf-core-tools/installation
- nf-core pipelines list docs: https://nf-co.re/docs/nf-core-tools/pipelines/list

## Related skills
- `nextflow-hello-workflow`
- `snakemake-toy-workflow-starter`
