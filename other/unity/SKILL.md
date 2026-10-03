---
name: unity
description: Ohio State ASC Unity HPC cluster basics and routing skill. Use when the user mentions Unity, ASC Unity, Slurm on Unity, OnDemand, Jupyter on Unity, Unity Python environments, or Unity remote editor workflows.
---

# Unity Skill

This is the top-level Unity skill.

It is intentionally not a pure router. It contains the always-relevant Unity basics that should be read first, then points to narrower subskills only when the task needs deeper Unity-specific detail.

## Unity Basics

- Unity uses **Slurm** for scheduling and **Lmod** for software modules.
- Heavy computation should not run on login nodes.
- GPU-dependent package installs are often safer on compute nodes than on login nodes.
- Unity's shared module-managed conda/mamba roots can be read-only; user-owned prefix environments are often the least painful option.
- If an environment was created with `mamba create --prefix /path/to/env`, activate it by full path.
- If `sbatch` accepts a script and returns a job ID, the resource syntax is valid. A long wait is a scheduling problem, not necessarily a script problem.
- If a GPU job fails with CUDA OOM, the requested GPU is probably too small for the model or load path. More GPUs do not help if the process loads the full model on one card.
- When current hardware matters, prefer live inspection with `sinfo`/`scontrol` over stale notes or memory.

## Unity-Specific Commands Worth Remembering

- `ml avail`
- `ml spider <term>`
- `ml load <module>`
- `squeue -u $USER`
- `scontrol show job <jobid>`
- `scontrol show partition <partition>`
- `scontrol show node <node>`
- `sinfo -N -o "%.8N %.5c %.10m %.20R %.20G %.f "`

## When To Use Which Subskill

Use the subskills only when the task is specifically about one of these areas:

- `unity-python-envs`
  - Python, conda/mamba, wheels, pip installs, package build/install strategy, compute-node installs, read-only env issues

- `unity-ondemand`
  - Unity OnDemand itself, web UI entrypoints, choosing between desktop/app/server style launches, browser-based workflows

- `unity-jupyter`
  - Jupyter Notebook or Jupyter server launch settings, resource choices for notebook sessions, common Unity Jupyter launch mistakes

- `unity-vscode-cursor`
  - VS Code, Cursor, remote SSH/editor workflows, login-node editor-server issues, safer alternatives

- `unity-slurm`
  - Only for Unity-specific Slurm quirks beyond standard HPC knowledge: partition naming, typed GPU requests, queue/resource triage

## Intent

Assume standard HPC knowledge by default.
Only pull a subskill when the user needs Unity-specific detail that is not already covered above.
