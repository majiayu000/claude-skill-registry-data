---
name: scbe-colab-training-ops
description: Operate SCBE Colab notebooks as a daily training and remote-compute lane using the Issac command center, local bridge profiles, notebook catalog, and Hugging Face training scripts. Use when the user wants to run or prepare Colab notebooks, wire local Colab URLs into SCBE, choose the right notebook for SFT or pivot work, or turn browser/compute sessions into repeatable training flows.
---

# SCBE Colab Training Ops

Use this skill when Colab should become part of the normal SCBE operating surface instead of an ad hoc notebook tab.

## Entry Surface

- Start with `issac-help` and look at the `COLAB` section.
- Use `colab-catalog` first to see what notebooks already exist.
- Use `colab-show <name>` or `colab-url <name>` before guessing which notebook to run.
- Use `colab-bridge-set` only when the user already has a Colab local-connection URL.

## Core Lanes

1. Notebook Selection
- `colab-catalog`
- `colab-show pivot`
- `colab-show finetune`
- `colab-show webtoon`

2. Local Bridge / Session Reuse
- `colab-bridge-set -BackendUrl <url> -Name pivot`
- `colab-bridge-status -Name pivot`
- `colab-bridge-env -Name pivot`

3. Training Prep
- `hf-generate-sft`
- `hf-train-wave`
- `hf-agent-loop`

4. Guided Multi-Step Lane
- `buildflow-colab <topic>`

## What Exists Already

- notebook catalog script: `scripts/system/colab_workflow_catalog.py`
- bridge script: `C:\Users\issda\.codex\skills\scbe-n8n-colab-bridge\scripts\colab_n8n_bridge.py`
- command-center surface: `scripts/hydra_command_center.ps1`
- free T4 fine-tune notebook: `notebooks/scbe_finetune_colab.ipynb`
- pivot notebook: `notebooks/scbe_pivot_training_v2.ipynb`

Read `references/notebook-map.md` when you need the notebook-by-notebook breakdown.

## Safety Gates

1. Do not invent a new notebook if an existing one already matches the job.
2. Do not store raw Colab tokens in repo files.
3. Prefer bridge profiles and env exports over pasting secrets into notebooks.
4. Keep notebook selection explicit: pivot, finetune, qlora, webtoon, or cloud workspace.
5. Treat Colab as compute, not as the source of truth. The source of truth stays in repo files and datasets.

## Output Contract

Every Colab operation should leave:

- the chosen notebook name and path
- the Colab URL or local bridge profile name
- any generated SFT/training artifacts
- a note about whether compute stayed local, Colab-only, or crossed into HF push
