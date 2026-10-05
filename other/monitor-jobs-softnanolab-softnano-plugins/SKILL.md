---
name: monitor-jobs
description: Monitor SLURM/PBS jobs and their logs. Use when the user asks to monitor, check, or watch a submitted job. Automatically detects running/pending jobs, tails logs, and reports errors.
argument-hint: "[job-id (optional)]"
allowed-tools: Bash, Read, Grep, Glob, Task
---

# Monitor HPC Jobs
You are monitoring HPC jobs on a cluster. Follow this workflow:

## Step 0: Resolve project root and environment

1. Look for `.env` by walking up from `$PWD` (check `$PWD/.env`, `$PWD/../.env`, etc.)
2. The directory containing `.env` is `$PROJECT_ROOT`
3. If no `.env` is found, fall back to `$PWD`
4. Read `.env` to get `JOBS_DIR` (used for locating job scripts and logs).

## Step 1: Detect the scheduler and cluster

```bash
command -v sbatch && echo "SLURM" || (command -v qsub && echo "PBS" || echo "UNKNOWN")
```

Then identify which cluster you are on:

```bash
# CX3 (Imperial) — PBS Pro
[[ "$PWD" == /rds/general/user/* ]] && echo "CX3"

# Isambard — SLURM
[[ "$PWD" == /home/*/* ]] && ls /projects/ &>/dev/null && echo "ISAMBARD"
```

If on **CX3**, also check if you are on a login node (hostname contains `login`). If you are NOT on a login node, you can run short Python commands directly without submitting a job.

Follow the **SLURM** or **PBS Pro** paths below depending on the scheduler.

## Step 2: Identify the job

- If `$ARGUMENTS` contains a job ID, use that.

### SLURM
- Run `squeue -u $USER --format="%.18i %.20j %.8T %.10M %.6D %.4C %.20R %o" --sort=-V` to find the user's active jobs.
- If no jobs are running/pending, check recently completed jobs with `sacct -u $USER --starttime=$(date -d '24 hours ago' +%Y-%m-%d) --format=JobID,JobName%30,State,ExitCode,Start,End,Elapsed --noheader`.

### PBS Pro (CX3)
- Run `qstat -u $USER` to find the user's active jobs.
- If no jobs are running/queued, try `qstat -f <job_id>` if a job ID was provided (may still work for recently-finished jobs). Otherwise, report that no active jobs were found — PBS Pro has no `sacct`-equivalent history command.

## Step 3: Get job details

### SLURM
- Run `scontrol show job <job_id>` to get full job info (WorkDir, StdOut path, submission script, state, node allocation).
- Extract the **log file path** from the `StdOut` field. Note: `%j` in the path is replaced by the job ID.

### PBS Pro (CX3)
- Run `qstat -f <job_id>` to get full job info (Output_Path, Error_Path, job state, resources).
- Extract **both** log paths: `Output_Path` (stdout) and `Error_Path` (stderr). PBS Pro uses separate files unlike SLURM.
- PBS log filenames are fixed strings — there is no `%j` job ID expansion.
- Log paths from `#PBS -o` / `#PBS -e` are relative to `PBS_O_WORKDIR` (the submission directory). Resolve them accordingly.

## Step 4: Wait for job to start (if PENDING/QUEUED)

If the job is PENDING (SLURM) or Q (PBS), do NOT just report and stop. Instead, **automatically poll until it starts**:

1. Report the current state: "Job 12345 is PENDING. Waiting for it to start..."
2. Run `sleep 30` in the background using `run_in_background: true`.
3. After each sleep, re-check:
   - **SLURM**: `squeue -j <job_id> --noheader --format="%.18i %.8T"`
   - **PBS**: `qstat <job_id>` (check the state column)
4. If still pending, report briefly ("Still pending, waited Xm so far...") and sleep again.
5. Repeat until the job transitions to RUNNING (R) or FAILED/CANCELLED.
6. Once RUNNING, wait 10 more seconds for the log file to appear, then proceed to Step 5.

This polling loop is the **default behavior** — do not ask the user whether to wait. Just do it.

## Step 5: Monitor the logs

- Check if the log file exists yet. If not, sleep 10 seconds and retry (up to 5 times).
- Once the log file exists, read the **last 100 lines** using `tail -n 100 <log_path>`.
- **PBS Pro**: Check both the `.out` (stdout) and `.err` (stderr) log files. Errors often appear only in the `.err` file.
- Look for:
  - **Errors**: Python tracebacks, `Error`, `Exception`, `FAILED`, `CANCELLED`, `OOM`, `CUDA error`, `RuntimeError`
  - **Warnings**: `UserWarning`, `FutureWarning`, deprecation notices
  - **Progress indicators**: epoch numbers, step counts, loss values, W&B run URLs
  - **Training metrics**: `train/loss`, `val/loss`, learning rate, gradient norms

## Step 6: Report status

Provide a concise summary:
1. **Job state** (PENDING / RUNNING / COMPLETED / FAILED / TIMEOUT)
2. **Runtime** so far
3. **Training progress** (current epoch/step, latest loss values)
4. **W&B run URL** if visible in logs
5. **Errors or warnings** if any — include the full traceback

## Step 7: If errors are found

- Analyze the error and identify the root cause.
- Check the relevant source files in the codebase to understand the issue.
- Propose a fix. If the fix is clear and safe:
  1. Apply the fix to the source code.
  2. Cancel the failed job (ask user first):
     - **SLURM**: `scancel <job_id>`
     - **PBS**: `qdel <job_id>`
  3. Resubmit the job with the original script.
- If the fix is ambiguous or risky, present options to the user before acting.

## Step 8: Continuous monitoring (if job is still running)

If the job is running and healthy, offer to keep monitoring. If the user wants continued monitoring:
- Sleep for 60 seconds between checks.
- Re-read the last 100 lines of the log.
- Report any new errors, warnings, or progress updates.
- Stop monitoring when the job completes, fails, or the user asks to stop.

## Key paths

| What | Path |
|------|------|
| Job scripts | `$JOBS_DIR/<project>/[<group>/]` (the optional `<group>/` sub-dir is used by `/softnano:submit-wandb-job`) |
| SLURM logs | `$JOBS_DIR/<project>/[<group>/]logs/` (or as specified by `#SBATCH --output`) |
| PBS logs | `$JOBS_DIR/<project>/[<group>/]logs/` (or as specified by `#PBS -o` / `#PBS -e`) |
| Env vars | `$PROJECT_ROOT/.env` → `JOBS_DIR` |

## CX3 (PBS Pro) Reference

### Queue Reference

| Queue | Walltime | CPUs | Memory | GPUs | Use case |
|-------|----------|------|--------|------|----------|
| `v1_gpu72` | 72h | 1–64 | up to 920 GB | L40S / A100 | GPU inference/training |
| `v1_medium24` | 24h | 1–64 | up to 450 GB | — | CPU-only, moderate memory |
| `v1_largemem72` | 72h | 1–128 | 921–4000 GB | — | mmseqs2 / large-index jobs |

> 12 GPU limit per user on `v1_gpu72`.

### CX3 Storage

| Path | Size | Notes |
|------|------|-------|
| `/rds/general/user/<user>/home` | 1 TB | Code, logs, outputs |
| `/rds/general/user/<user>/ephemeral` | 10 TB | Large datasets (auto-deleted every 30 days) |

### Key Differences from SLURM

- No `srun` — run Python directly after activating the venv.
- No `%j` job ID expansion in `#PBS -o` — use fixed log filenames.
- Resource syntax: `select=<N>:ncpus=<C>:mem=<M>gb:ngpus=<G>` instead of `--nodes`/`--gpus`.
- Variables via `qsub -v "KEY=val"` instead of `--export`.
- Queue via `#PBS -q` instead of `#SBATCH --partition`.

## Important notes

- **SLURM**: Always resolve `%j` in log paths to the actual job ID.
- **PBS Pro**: Monitor both `.out` and `.err` files. Log filenames are fixed (no job ID expansion).
- If the log path is relative, resolve it relative to the job's WorkDir (SLURM: from `scontrol`, PBS: from `PBS_O_WORKDIR`).
- When sleeping/waiting, use `sleep` in Bash with `run_in_background` to avoid blocking.
- Present errors with enough context (surrounding lines) for the user to understand.
- See the `cluster-instructions` skill (`isambard.md` for SLURM, `cx3.md` for PBS Pro) for full HPC reference.
