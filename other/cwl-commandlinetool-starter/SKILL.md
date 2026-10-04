---
name: cwl-commandlinetool-starter
description: Use this skill to author and run a minimal Common Workflow Language CommandLineTool and one-step workflow with cwltool. Do not use it for containerized production execution or complex scatter/gather workflows.
---

## Purpose
Run a small local CWL example end to end and use it as a starter for command-line tool wrapping.

## When to use
- You need a verified local CWL example.
- You want a starter for wrapping a simple command-line tool in CWL.

## When not to use
- You need cluster scheduling or production orchestration.
- You need Docker-only workflows.

## Inputs
- A CWL workflow or command-line tool file
- A YAML or JSON job input file
- Optional output directory and summary path

## Outputs
- The workflow output file
- A JSON run summary with the parsed CWL outputs and the rendered greeting text

## Requirements
- `slurm/envs/workflow-languages`
- `cwltool`

## Procedure
1. Run `python3 skills/reproducible-workflows/cwl-commandlinetool-starter/scripts/run_cwl_hello.py --message "hello from cwl" --workspace scratch/cwl/workspace --summary-out scratch/cwl/summary.json`.
2. Inspect the `raw_summary` block and the materialized `greeting.txt`.
3. Use `examples/hello.cwl` and `examples/hello-job.yml` as the base for a new local `CommandLineTool`.

## Validation
- `cwltool` validates and runs successfully.
- The summary records a greeting text and an output file named `greeting.txt`.

## Failure modes and fixes
- Missing runtime: verify `slurm/envs/workflow-languages` exists and contains `cwltool`.
- Validation failure: run `python -m cwltool --validate` on the CWL file before debugging execution.

## Safety and limits
- This skill disables containers and runs a local toy example only.
- Extend carefully before wrapping destructive commands or large data paths.

## Provenance
- https://www.commonwl.org/user_guide/
- https://github.com/common-workflow-language/cwl-v1.2
