---
name: unity-hpc
description: Help users interact with the OSU Unity HPC cluster (ASC). Use when the user mentions Unity, Slurm, sbatch, sinteractive, or needs help with HPC workflows like job submission, GPU requests, module management, and cluster debugging.
---

# Unity HPC Skill

This skill provides practical guidance for using the Ohio State University (OSU) Arts and Sciences (ASC) Unity computing cluster.

## Quick Start

- **Login**: `ssh name.#@unity.asc.ohio-state.edu`
- **Module Help**: Use `ml avail` or `module avail` to see software, and `ml load <name>` to use it.
- **Interactive Jobs**: Use `sinteractive` for a quick compute node session.
- **Batch Jobs**: Use `sbatch <script.sh>` to submit jobs.
- **Monitor Jobs**: Use `squeue -u $USER` to check queue status.

## Workflow: Submitting a Job

1. **Identify resources**: CPUs, memory, walltime, GPU count, and whether you need a specific GPU type.
2. **Check live cluster state**: Prefer `sinfo`/`scontrol` over memory or stale docs when choosing a partition or GPU type. See [REFERENCE.md](REFERENCE.md).
3. **Create a script**: Use a template from [TEMPLATES.md](TEMPLATES.md) or generate one using `#SBATCH` directives.
4. **Submit from a login node**: `sbatch my_script.sh`.
5. **Monitor and inspect**: `squeue -u $USER`, `scontrol show job <jobid>`, and log files.

## Environment Management (Lmod)

- `ml avail`: List available modules.
- `ml spider <term>`: Search for modules.
- `ml load <module>`: Load a module (for example `ml mamba`).
- `ml list`: See currently loaded modules.

## Unity-Specific Guidance

- Never run heavy computations or package installs on login nodes unless the docs explicitly say it is safe.
- Prefer compute-node installs for GPU-dependent Python packages.
- On Unity, shared module-managed conda/mamba roots can be read-only. User-owned prefix environments are safer than relying on named envs under the shared module prefix.
- If an environment was created with `mamba create --prefix /path/to/env`, activate it by full path: `mamba activate /path/to/env`.
- If `sbatch` accepts a script and returns a job ID, the request syntax is valid. Queue time is a scheduling issue, not necessarily a configuration failure.
- If a GPU job fails with CUDA OOM, that usually means the requested GPU is too small for the model or batch size. More GPUs do not help if the model is loaded onto a single card; you need a larger GPU or quantization.

## GPU Job Triage

When helping with GPU jobs on Unity:

1. Check whether the user needs **any GPU** or a **specific GPU type**.
2. Verify the current pool live with `sinfo` before assuming hardware availability.
3. Prefer typed GPU requests such as `--gres=gpu:h200:1` when the partition supports them.
4. Distinguish between:
   - **scheduler problems**: invalid partition, invalid GRES, pending queue, account access
   - **runtime problems**: CUDA unavailable, missing deps, OOM, incompatible drivers/libraries
5. For model-loading/OCR work, consider a two-lane plan:
   - large-GPU lane for the full model
   - quantized lane for smaller public GPUs

## Connection & Access

- **ASC Network**: Direct SSH access.
- **Off-campus**: Use ASCTech Jump Host or ASC VPN.
- **OnDemand**: <https://ondemand.asc.ohio-state.edu/>
- **Unity Cluster Guide**: <http://go.osu.edu/unitycompute>
- **Support Ticket**: <http://go.osu.edu/unitysupportticket>
- **Support Email**: <mailto:asctech@osu.edu>

## Guidelines

- Estimate walltime generously but reasonably.
- Prefer exclusive partitions if your group has access and queue time matters.
- For GPU-intensive workflows, verify the hardware live before finalizing the `#SBATCH` lines.
- If the docs and `sinfo` disagree, trust `sinfo` for current availability and use the docs as background context.

For detailed node specs and partition info, see [REFERENCE.md](REFERENCE.md).
For Slurm script templates, see [TEMPLATES.md](TEMPLATES.md).
