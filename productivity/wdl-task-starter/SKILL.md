---
name: wdl-task-starter
description: Use this skill to author and run a minimal WDL task and workflow with miniwdl. Do not use it for Cromwell-specific backends or large imported workflow graphs.
---

## Purpose
Run a local WDL task end to end and use it as a starter for task and workflow authoring.

## When to use
- You need a verified OpenWDL-style local example.
- You want a small WDL task or workflow starter with JSON inputs.

## When not to use
- You need cloud backends or Cromwell execution.
- You need advanced imports or large workflow graphs.

## Inputs
- A WDL document
- A Cromwell-style JSON input object
- Optional run directory and summary path

## Outputs
- A JSON run summary with the output JSON emitted by `miniwdl`
- The rendered `greeting.txt` file inside the run directory

## Requirements
- `slurm/envs/workflow-languages`
- `miniwdl`
- `udocker` inside the same prefix for daemonless local execution

## Procedure
1. Run `python3 skills/reproducible-workflows/wdl-task-starter/scripts/run_wdl_hello.py --name Ada --workspace scratch/wdl/workspace --summary-out scratch/wdl/summary.json`.
2. Inspect the WDL outputs JSON and the materialized `greeting.txt`; the wrapper configures a daemonless local `miniwdl` execution path for this toy task.
3. Use `examples/hello.wdl` and `examples/hello-inputs.json` as the base for new tasks or workflows.

## Validation
- `miniwdl run` exits successfully.
- The output JSON includes greeting text and a file output.

## Failure modes and fixes
- Missing runtime: verify `slurm/envs/workflow-languages` exists and `python -m WDL --version` works.
- Missing daemonless backend: verify `slurm/envs/workflow-languages/bin/udocker --version` works.
- Input mismatch: run `miniwdl run --json` to inspect the required input object shape.

## Safety and limits
- This skill runs a local toy workflow only.
- Extend runtime blocks carefully before using external containers or large file inputs.

## Provenance
- https://docs.openwdl.org/
- https://github.com/openwdl/wdl
- https://miniwdl.readthedocs.io/
