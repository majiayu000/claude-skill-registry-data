---
name: cluster-instructions
description: Detect which HPC cluster you are on and load the correct job submission instructions. Use when the user asks to submit, run, or schedule a job, or when you need to know which cluster environment you are in.
argument-hint: "[command-to-run (optional)]"
allowed-tools: Bash, Read, Grep, Glob, Write, Edit
---

# Cluster Instructions

You are on an HPC cluster. Before submitting any jobs or running heavy commands, detect which cluster you are on and follow the correct instructions.

**IMPORTANT**: Never run Python, heavy CPU, or GPU commands directly on a login node. Always submit via the scheduler unless you have confirmed you are on a compute node.

## Step 1: Detect the cluster

Run these checks in order:

```bash
# Check host and working directory path
hostname
hostname -f 2>/dev/null || true
pwd

# Check available scheduler
if command -v sbatch >/dev/null 2>&1; then
    echo "SLURM"
elif command -v qsub >/dev/null 2>&1 && command -v qconf >/dev/null 2>&1; then
    echo "SGE"
elif command -v qsub >/dev/null 2>&1; then
    echo "PBS"
else
    echo "UNKNOWN"
fi
```

| Path pattern | Cluster | Scheduler | Instructions |
|---|---|---|---|
| `/rds/general/user/<user>/home/` | Imperial CX3 | PBS Pro | `cx3.md` in this skill |
| `/gpfs/home/<user>` | Imperial HX1 | PBS Pro | Use CX3 instructions (`cx3.md`) |
| `/lustre/home/<user>` + `sbatch` available + Young hostname | UCL MMM Young NG (`ssh mmm`) | SLURM | `mmm-slurm.md` in this skill |
| `/lustre/home/<user>` + `qsub`/`qconf` available + Young hostname | UCL MMM old Young (`ssh mmm-old`) | SGE / Grid Engine | `mmm-sge.md` in this skill |
| `/home/<project>/<user>.<project>/` + `/projects/<project>/` exists | Isambard AI | SLURM | `isambard.md` in this skill |
| `softnanolab-HP-Z8-G4-Workstation` / `softnanolab-campus` | SoftNano campus workstation | SLURM may exist, but not the HPC cluster target | Do not submit MMM/HPC work here; SSH onward to `mmm`, `mmm-old`, `hx1`, or `leprotein` |

If none match, ask the user which cluster they are on.

Detection order matters. A plain "SLURM exists" check is not enough: MMM Young NG and Isambard both expose SLURM, while the SoftNano campus workstation may also expose SLURM commands without being the intended cluster target. Use host/path first, then the scheduler.

## Step 2: Check if you are on a login node

- **CX3**: Run `hostname`. If it contains `login`, you are on a login node — do not run compute commands directly. If it does NOT contain `login`, you are on a compute node and can run short Python commands directly.
- **MMM Young NG (`ssh mmm`)**: Hostnames like `login*.young.ucl.ac.uk` are login nodes. Use `sbatch` or `srun` via the MMM SLURM instructions.
- **MMM old Young (`ssh mmm-old`)**: Hostnames like `login*.ib.young.ucl.ac.uk` are login nodes. Use `qsub`; this is SGE, not PBS.
- **Isambard**: Assume login node unless inside an `srun` session or a batch job.
- **SoftNano campus**: This is a workstation/gateway. It may have SLURM commands, but it is not the MMM/HPC cluster target. Do not run or submit HPC workloads there unless the user explicitly asks for campus-local work; SSH to the actual cluster first.

## Step 3: Load cluster-specific instructions

Read the appropriate file from this skill's directory:

- **CX3 / HX1**: Read `cx3.md` — covers PBS Pro queues, job templates, key patterns, common commands, and storage paths.
- **MMM Young NG**: Read `mmm-slurm.md` — covers SLURM partitions/QoS, GPU A100 requests, modules, and common commands.
- **MMM old Young**: Read `mmm-sge.md` — covers SGE queues, project/account flags, GPU requests, modules, and common commands.
- **Isambard**: Read `isambard.md` — covers SLURM job templates, GPU allocation (Grace Hopper Superchips), DDP setup, and common commands.

Follow those instructions for all job submission, script creation, and resource allocation decisions.

## Step 4: Submit or run the command

If `$ARGUMENTS` contains a command or script to run:

1. Determine if it needs a batch job (long-running, GPU, heavy CPU) or can run directly (quick debugging, <5 min).
2. For batch jobs: create a job script using the templates from the cluster-specific instructions, then submit it.
3. For quick commands on a compute node: run directly.
4. For quick commands on a login node:
   - **CX3**: Use `qsub -I` for an interactive session.
   - **MMM Young NG**: Use `srun` with a partition/QoS from `mmm-slurm.md`.
   - **MMM old Young**: Use `qsub` with flags from `mmm-sge.md`; do not run tests directly on the login node.
   - **Isambard**: Use `srun` for an interactive session.

If no arguments are provided, just report which cluster and node type you detected.
