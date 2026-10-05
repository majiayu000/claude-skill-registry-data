---
name: experiment-setup
description: Use this skill when setting up, validating, or repairing the local environment for the cross-modal appraisal transfer project, including Python dependencies, model boot, GPU checks, dataset access, version pinning, and smoke tests for Gemma 3, TransformerBridge, and optional Qwen verification.
---

# Experiment Setup

This skill prepares the project to run reliably before any substantive experiment begins. Use it for first-time setup, environment repair, dependency drift, version checks, smoke tests, and reproducibility checks.

## Use this skill when

- The repo is being initialized on a new machine or fresh environment.
- Dependencies may be missing, incompatible, or incorrectly pinned.
- TransformerBridge, Hugging Face, PyTorch, CUDA, or model loading is failing.
- A model boots but outputs appear numerically wrong or hooks do not fire as expected.
- A dataset path, credential, or access-controlled source must be checked before experiments.
- A task asks for “setup,” “sanity check,” “boot test,” “environment validation,” or “smoke test.”

## Do not use this skill for

- Full experimental runs with training or evaluation loops.
- Writing the final paper/report.
- Detailed result analysis beyond setup verification.

## Primary goal

Bring the project into a known-good, reproducible state and leave behind a short, actionable record of:
1. what was checked,
2. what passed,
3. what failed,
4. what exact commands reproduce the successful setup.

## Required mindset

- Prefer minimal, reproducible checks before expensive runs.
- Verify before assuming.
- Pin versions when a component is known to be fragile.
- Never treat “imports succeeded” as enough; always run at least one real forward-pass smoke test.
- Surface blockers early, especially dataset-access and model-version issues.

## Inputs to inspect first

Before changing anything, inspect:

- `CLAUDE.md`
- `README.md`
- `requirements.txt`, `pyproject.toml`, `environment.yml`, or equivalent dependency files
- `docs/models-gemma3.md`
- `docs/datasets.md`
- `docs/experiment-1.md`
- any setup scripts under `scripts/` or `src/`

If these files do not exist, infer the minimum viable setup from the repo structure and propose creating the missing docs later.

## Setup workflow

### Step 1: Identify the environment contract

Determine:

- Python version expected by the repo
- package manager in use (`uv`, `pip`, `poetry`, `conda`, etc.)
- CUDA and PyTorch expectations
- whether the project expects local GPU, remote GPU, or CPU fallback
- required model families and dataset sources
- any pinned versions already documented

If setup instructions conflict across files, treat the stricter or more recent version spec as the provisional source of truth and explicitly note the conflict.

### Step 2: Validate core dependencies

Check for the installability and version compatibility of:

- Python
- PyTorch
- CUDA availability
- Transformers
- TransformerBridge
- datasets / pandas / numpy / scikit-learn
- any project-specific packages used for probes, metrics, or plotting

Prioritize known-fragile components first, especially multimodal model support and hook frameworks.

### Step 3: Validate model boot path

Run the smallest possible model boot test for the primary model path.

For Gemma + TransformerBridge, verify:
- the model boots successfully,
- multimodal mode is active if expected,
- tokenization works,
- a single text-only and/or image-conditioned forward pass completes,
- intended hook paths can be reached.

If the project includes a fallback verification model such as Qwen, check that path only after the primary path is stable.

### Step 4: Validate datasets

Check:
- dataset directories exist,
- expected file names or manifests are present,
- licenses / gated access requirements are satisfied,
- train/val/test split assumptions are documented,
- sample loading works for at least 1–3 examples.

For gated datasets, do not fabricate access. Report the exact blocker and the next manual step needed.

### Step 5: Run smoke tests

At minimum, run:
- one import smoke test,
- one forward-pass smoke test,
- one hook-registration smoke test,
- one tiny data-loading smoke test,
- one write-path smoke test for logs or outputs.

Keep smoke tests cheap and deterministic.

### Step 6: Produce a setup verdict

Classify the environment as one of:
- Ready
- Ready with warnings
- Blocked

Then provide:
- exact commands to reproduce the setup,
- known risks,
- unresolved blockers,
- recommended next task.

## Expected outputs

When this skill completes, produce:

- a concise environment status summary,
- a checklist of pass/fail items,
- exact reproduction commands,
- specific remediation steps for failures,
- recommended next action.

If useful, propose adding or updating:
- `docs/setup.md`
- `scripts/smoke_test.py`
- `scripts/check_environment.py`

## Guardrails

- Do not start long training jobs during setup.
- Do not silently upgrade fragile packages without stating what changed.
- Do not assume tokenizer behavior, hook names, or multimodal compatibility; verify them.
- Do not mark the setup successful unless an actual forward pass succeeds.
- When version-sensitive bugs are known, call them out explicitly and recommend pinning.

## Good completion criteria

This skill is complete only when:
- the environment contract is clear,
- core dependencies are validated,
- the primary model path has passed a smoke test,
- dataset availability has been checked,
- the next experiment step is unambiguous.

## Example invocations

- “Set up this repo on a new GPU machine.”
- “Check why Gemma 3 won’t boot through TransformerBridge.”
- “Validate the environment before running Stage A.”
- “Create a reproducible smoke test for the multimodal path.”