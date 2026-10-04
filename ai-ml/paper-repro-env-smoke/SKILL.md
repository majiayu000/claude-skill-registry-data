---
name: paper-repro-env-smoke
description: Plan and run minimal environment smoke tests for AI/ML paper reproduction repositories. Use after sources are locked, or when Codex must inspect dependency files, choose an isolated environment strategy, run cheap import/help/demo/pytest checks, capture logs, classify blockers, and decide whether a repo is viable for deeper reproduction.
---

# Paper Repro Env Smoke

## Overview

Use this skill to answer one narrow question: can the locked repo and artifacts support a cheap, auditable first run? It must not jump straight to full training unless the user explicitly selected that as the smoke target.

Read `references/patterns.md` before designing a smoke plan for CUDA-heavy, Docker-only, conda/pip-mixed, or missing-entry repositories.

## Inputs

- A locked repository path or URL, preferably from `$paper-repro-source-lock`.
- Optional `claim_map` and `source_lock` artifacts.
- Optional local dataset/model paths.
- User constraints for hardware, network, auth, time budget, and whether Docker/conda/venv is allowed.

## Workflow

1. Inspect the repository without modifying it:
   - dependency manifests: `environment.yml`, `requirements*.txt`, `pyproject.toml`, `setup.py`, `Dockerfile`, lock files;
   - entrypoints: `train.py`, `main.py`, `eval.py`, `test.py`, notebooks, scripts, CLI docs;
   - tests and demo assets;
   - GPU/CUDA/framework assumptions;
   - dataset path conventions.
2. Prefer an isolated environment:
   - existing project venv/conda env if documented and safe;
   - conda env from `environment.yml`;
   - venv plus `requirements.txt`;
   - Docker/Apptainer only when the repo clearly provides it or the user approves.
3. Choose the cheapest viable smoke command:
   - dependency/import probe;
   - `--help` for main entrypoints;
   - pytest/unit tests;
   - evaluation on a tiny sample or pretrained checkpoint;
   - one dry-run/minimal batch/one epoch only if explicitly cheap.
4. Run commands incrementally and log every command, cwd, exit code, duration, stdout/stderr path, and environment facts.
5. Classify blockers before repair:
   - `dependency`, `python-version`, `cuda-driver`, `missing-data`, `missing-model`, `path-config`, `api-auth`, `license`, `code-paper-mismatch`, `resource-cost`, `unknown`.
6. Produce an environment smoke report and stop before expensive runs unless the user asks to continue.

## Helper Script

Generate a first-pass plan:

```powershell
python skills\paper-repro-env-smoke\scripts\repro_env_smoke.py inspect `
  --repo path\to\official_repo `
  --output-dir output\repro\env_smoke
```

Capture the current interpreter and framework probe:

```powershell
python skills\paper-repro-env-smoke\scripts\repro_env_smoke.py env `
  --output-dir output\repro\env_smoke
```

Run only an explicitly selected small command:

```powershell
python skills\paper-repro-env-smoke\scripts\repro_env_smoke.py run `
  --repo path\to\official_repo `
  --output-dir output\repro\env_smoke `
  --command "python train.py --help" `
  --timeout 60
```

## Output Contract

Create `env_smoke_report.md`, `env_smoke_plan.json`, and command logs under `logs/`.

Required report sections:

- `Repository`
- `Environment Inputs`
- `Detected Manifests`
- `Candidate Setup Commands`
- `Candidate Smoke Commands`
- `Executed Commands`
- `Blockers`
- `Verdict`
- `Next Run Recommendation`

Smoke verdicts:

- `ready_for_minimal_reproduction`
- `ready_with_minor_fixes`
- `blocked_by_missing_artifact`
- `blocked_by_environment`
- `blocked_by_auth_or_license`
- `not_enough_information`

## Guardrails

- Do not install into the global/base Python environment.
- Do not overwrite `.env`, credentials, datasets, checkpoints, or repo source files.
- Do not launch full training, broad downloads, or GPU-heavy runs as a smoke test.
- Do not treat a successful import as reproduction success. It only proves environment viability.
- Preserve logs even for failed commands.

## Resources

- `scripts/repro_env_smoke.py`: standard-library helper for repo inspection, environment probe, and explicit small-command logging.
- `references/patterns.md`: smoke-test practices distilled from ReproAgent, Papers with Code, smoke testing guidance, Docker/conda reproducibility, and ML environment reproducibility discussions.
