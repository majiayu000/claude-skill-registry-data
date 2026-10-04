---
name: rseng-hpc-computing
description: >-
  Covers working effectively on high-performance computing clusters: writing
  and debugging SLURM job scripts, choosing and requesting resources honestly,
  running containers with Apptainer, using module systems and EESSI software
  stacks, MPI basics, checkpointing, and scaling from laptop to cluster
  reproducibly. Use when the user mentions a cluster, supercomputer, SLURM,
  sbatch, MPI, Apptainer or Singularity, module load, job arrays or walltime,
  or when a compute workload has outgrown a single machine.
  (Larger-than-memory data processing with Dask or Spark is
  rseng-big-data-processing; measuring scaling before requesting allocations is
  rseng-performance-profiling.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Research computing on HPC clusters

HPC clusters are where much research code actually runs, and they
invert desktop habits: you do not run programs, you request resources
and submit batch jobs; you do not install software, you load modules
or bring containers; the login node is a shared hallway, not a
workstation. An agent's job is to translate the user's computation
into this model correctly and reproducibly - and to respect that
every cluster has local documentation that overrides generic advice.

## Batch jobs done right (SLURM)

A job script is a shell script with resource directives:

```bash
#!/bin/bash
#SBATCH --job-name=fit-model
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --output=logs/%x-%j.out

module load Python/3.12
srun python fit_model.py --config configs/run.yaml
```

Practices that matter:

- Request honestly: measure a pilot run, then set time/memory with
  modest headroom. Over-requesting wastes allocation and queue
  priority (and energy - rseng-green-computing); under-requesting
  kills jobs at 99%.
- Never compute on the login node; test with a short interactive
  allocation (srun --pty or salloc) instead.
- Parameter sweeps are job arrays (--array=0-99), not 100 submitted
  scripts; index into a config list with $SLURM_ARRAY_TASK_ID
  (externalized run configs pair naturally with rseng-workflows).
- Long jobs checkpoint: clusters preempt and nodes fail; save
  restartable state at intervals and make the script resume from the
  last checkpoint.
- Log usefully: %x-%j names, and `seff JOBID` after completion to
  compare requested vs used resources - feed that back into the next
  request.

## Software environments on clusters

Three layers, in order of preference for reproducibility:

1. Containers with Apptainer (formerly Singularity): the HPC-native
   container runtime - unprivileged, image-file based, GPU-aware.
   Build once (possibly from a Docker image), run identically on any
   cluster; pairs with rseng-reproducible-environments for the build
   recipe.
2. EESSI: a shared, optimized, ready-to-use scientific software
   stack streamed to any cluster or laptop - when available it gives
   identical software everywhere without building anything.
3. Module system (module avail / module load): the site's curated
   builds; record exact module versions in the job script - an
   unversioned `module load Python` is a reproducibility hole.

Never pip-install into the home directory as the primary strategy;
quota, node-architecture and reproducibility problems follow.

## Parallelism: pick the right kind

- Independent runs (sweeps, bootstraps, per-file processing): job
  arrays or a workflow engine - no MPI needed. This covers most
  research workloads.
- Single-node parallelism: threads/multiprocessing;
  --cpus-per-task, and pin BLAS/OpenMP thread counts to match.
- Multi-node tightly-coupled computation: MPI (mpi4py or native),
  launched with srun; requires the code to be written for it.
  Distributed data processing frameworks are their own path
  (rseng-big-data-processing).

Scaling discipline: measure strong/weak scaling on small counts
before requesting large allocations; doubling cores that yield 1.2x
wastes everyone's allocation
(rseng-performance-profiling for the measurement).

## Cluster citizenship and data

- Filesystems differ: home (small, backed up), project (shared),
  scratch (fast, purged) - stage data to scratch for jobs, move
  results back, and script the staging (rseng-data-management).
- Transfer with rsync (resumable) or the site's data-transfer nodes;
  never leave the only copy of results on scratch.
- Read the site's own docs first; when the user's cluster is known,
  prefer its conventions over anything generic, including this
  skill.

## Working with this skill

This skill is source-independent: its authority is the scheduler,
container and software-stack documentation linked below, plus each
cluster's local documentation.

Learn more (verified):
  - https://slurm.schedmd.com - SLURM documentation
  - https://apptainer.org - Apptainer container runtime
  - https://www.eessi.io/docs/ - EESSI shared software stack
  - https://carpentries-incubator.github.io/hpc-intro/ - HPC
    Carpentry introduction
  - https://coderefinery.github.io/TTT4HPC_parallel_workflows/ -
    CodeRefinery tuesday-tools lessons on HPC workflows

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-big-data-processing - distributed data framework path
- rseng-data-management - staging data across cluster filesystems
- rseng-green-computing - honest requests save energy
- rseng-performance-profiling - measure scaling before allocating
- rseng-reproducible-environments - containers and pinned modules
- rseng-workflows - sweeps via workflow engines

<!-- related-skills:end -->
