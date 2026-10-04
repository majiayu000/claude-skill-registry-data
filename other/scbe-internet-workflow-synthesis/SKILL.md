---
name: scbe-internet-workflow-synthesis
description: Synthesize and operate SCBE end-to-end internet workflows by discovering local and GitHub architecture templates, generating a baseline web pipeline profile, running ingestion and governance scans, and tuning system variables after the first run. Use when users ask to build, repair, or optimize internet workflow pipelines, workflow architecture maps, n8n or agent orchestration flows, or post-baseline threshold and concurrency tuning.
---

# Scbe Internet Workflow Synthesis

Build deterministic internet workflow pipelines from existing SCBE assets and the AI-Workflow-Architect repo, then run post-baseline variable tuning.

## Quick Start

1. Synthesize a repo-local profile:

```bash
python C:/Users/issda/.codex/skills/scbe-internet-workflow-synthesis/scripts/synthesize_pipeline_profile.py \
  --repo-root C:/Users/issda/SCBE-AETHERMOORE \
  --output training/internet_workflow_profile.json \
  --force
```

2. Run baseline plus variable tuning:

```bash
python C:/Users/issda/.codex/skills/scbe-internet-workflow-synthesis/scripts/run_e2e_pipeline.py \
  --repo-root C:/Users/issda/SCBE-AETHERMOORE \
  --profile training/internet_workflow_profile.json
```

## Workflow

1. Read `references/workflow-template-map.md` and prioritize local templates first.
2. Generate or update `training/internet_workflow_profile.json`.
3. Execute baseline with `scripts/web_research_training_pipeline.py`.
4. Read the latest `summary.json` emitted by the baseline run.
5. Tune thresholds and runtime knobs using `scripts/tune_system_variables.py`.
6. Emit a tuned cloud-kernel config plus a tuning report.

## Output Contract

Return or persist these artifacts:

- Baseline profile JSON (`training/internet_workflow_profile.json`)
- Baseline run summary (`training/runs/web_research/<run_id>/summary.json`)
- Tuned thresholds config (`training/cloud_kernel_pipeline.tuned.json` by default)
- Tuning report (`artifacts/internet_workflow_tuning_report.json` by default)
- Tuned runtime profile (`training/internet_workflow_profile.tuned.json` by default)

## Invariants

- Keep governance checks enabled for production flows (`skip_core_check=false`).
- Keep deterministic audit artifacts (`summary.json`, `audit.json`, `decision_record.json`).
- Keep secrets in environment variables; do not write tokens into profile files.
- Keep template discovery explicit (local first, GitHub fallback).

## Resource Guide

- `scripts/synthesize_pipeline_profile.py`: Build a default profile from template sources.
- `scripts/run_e2e_pipeline.py`: Run baseline ingest then invoke tuning automatically.
- `scripts/tune_system_variables.py`: Tune thresholds and runtime knobs from baseline metrics.
- `references/workflow-template-map.md`: Canonical local and GitHub template file map.
- `references/system-variable-tuning.md`: Tuning policy and variable bounds.
- `assets/internet_workflow_profile.template.json`: Copyable starter profile.
