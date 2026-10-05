---
name: dvc
description: Data Version Control (DVC) for tracking large datasets/models with Git-like semantics, defining reproducible data/ML pipelines (dvc.yaml stages that only re-run when their inputs change), and lightweight experiment tracking without a server. Use when large files (VCF/BAM/FASTQ, reference genomes, model weights) can't go in Git, when you need Make/Snakemake-style selective re-execution driven by data, or when comparing many training runs locally before promoting one. Pairs with Git (code), cloud object storage (data), and Snakemake/Nextflow (compute graph).
license: Apache-2.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
compatibility: Requires Python 3.9+ and dvc 3.x (current 3.67.1). Remote storage needs a matching extra (dvc[s3], dvc[gs], dvc[azure], dvc[ssh], ...) so the storage SDK is installed alongside the core CLI. The upstream GitHub org moved from iterative/dvc to treeverse/dvc in early 2026 after Treeverse (the lakeFS company) acquired Iterative; the PyPI package name (`dvc`), CLI, and file formats are unchanged.
metadata: {"version": "1.0", "skill-author": "community"}
---

# DVC (Data Version Control)

## Overview

DVC extends Git to the parts Git is bad at: large binary files and reproducible pipelines. Git tracks a small `.dvc` pointer file (a content hash); DVC stores the actual data in a local cache and, optionally, a remote (S3, GCS, Azure, SSH, or a plain directory). On top of that, DVC provides a lightweight pipeline definition (`dvc.yaml`) that re-runs only the stages whose inputs changed, and an experiment tracker (`dvc exp`) that snapshots code+data+params+metrics for each run without needing a tracking server.

Think of it as: **Git manages the recipe (code), DVC manages the ingredients (data, models) and can also manage the cooking steps (pipeline stages) and taste-tests (experiments).**

DVC is *not* a replacement for Snakemake/Nextflow when you need complex scheduling, retries, or cluster execution — it complements them. A common pattern is DVC tracking pipeline inputs/outputs while Snakemake or Nextflow drives the actual multi-node execution.

## Installation

```bash
# Core CLI, local/directory remotes only
uv pip install dvc

# Pick the extra(s) matching your remote storage backend
uv pip install "dvc[s3]"       # AWS S3 (boto3)
uv pip install "dvc[gs]"       # Google Cloud Storage
uv pip install "dvc[azure]"    # Azure Blob Storage
uv pip install "dvc[ssh]"      # SSH/SFTP remote
uv pip install "dvc[all]"      # every backend (heavier install)

# DVCLive for in-training metric logging (separate package)
uv pip install dvclive
```

Check version: `dvc --version` (targets 3.67.x; commands below are stable across the 3.x series).

## When to Use

- A dataset, model checkpoint, or reference genome is too large for Git (VCF, BAM, FASTQ, `.pt`/`.safetensors` weights, indexed references).
- You want `make`/`snakemake`-style "only re-run what changed" behavior driven by **data** hashes, not just file mtimes.
- You need to compare dozens of training runs (params, metrics, code diff) without standing up an MLflow/W&B server.
- You want data lineage that lives in the same Git history as the code that produced it (auditable, PR-reviewable).

Not a fit: real-time experiment dashboards for a team (use W&B/MLflow alongside DVC), or orchestrating thousands of parallel cluster jobs (use Nextflow/Snakemake/Ray, with DVC tracking their inputs/outputs).

## Core Concepts

- **Cache**: content-addressable local store at `.dvc/cache` (like Git's object store, but for large files).
- **`.dvc` files**: small YAML pointers (hash + size + path) that Git tracks in place of the real file.
- **Remote**: named storage location (S3 bucket, GCS bucket, SSH server, another local dir) DVC pushes/pulls cache objects to/from.
- **`dvc.yaml`**: pipeline definition — a DAG of named stages, each with `cmd`, `deps`, `outs`, and optionally `params`/`metrics`/`plots`.
- **`dvc.lock`**: auto-generated lockfile recording the exact hashes used in the last successful `dvc repro` — this is what makes re-runs skippable.
- **Experiments**: throwaway Git commits (not on your branch) created by `dvc exp run`, comparable side-by-side with `dvc exp show`.

## Quick Start: Versioning Data

```bash
git init
dvc init                      # creates .dvc/, commit this

dvc add data/raw/cohort.vcf.gz     # moves file into cache, writes cohort.vcf.gz.dvc
git add data/raw/cohort.vcf.gz.dvc data/raw/.gitignore
git commit -m "Track cohort VCF with DVC"

# Configure a remote once
dvc remote add -d myremote s3://my-bucket/dvc-store
git add .dvc/config
git commit -m "Add S3 remote"

dvc push        # upload cache objects referenced by tracked .dvc files
dvc pull        # (on another machine/clone) fetch data referenced by .dvc files
```

`dvc add` on a directory tracks the whole tree with one `.dir` hash — good for thousands of small files (e.g., a FASTQ batch) where you don't want thousands of Git-tracked pointers.

## Pipelines (dvc.yaml)

Define stages instead of ad hoc `dvc add`:

```yaml
# dvc.yaml
stages:
  align:
    cmd: bwa mem ref.fa reads_R1.fq.gz reads_R2.fq.gz | samtools sort -o aligned.bam
    deps:
      - ref.fa
      - reads_R1.fq.gz
      - reads_R2.fq.gz
    outs:
      - aligned.bam

  call_variants:
    cmd: python call_variants.py --bam aligned.bam --out variants.vcf --params params.yaml
    deps:
      - aligned.bam
      - call_variants.py
    params:
      - call.min_qual
    outs:
      - variants.vcf
    metrics:
      - metrics.json:
          cache: false
```

```bash
dvc repro          # runs only stages whose deps/params/code hash changed
dvc dag             # ASCII/graphviz view of the stage DAG
dvc metrics show    # print metrics.json across the tree
dvc metrics diff    # diff metrics vs. the previous commit
dvc params diff     # diff params.yaml vs. the previous commit
```

`params.yaml` is a plain YAML file of hyperparameters; `dvc.yaml` stages reference the specific keys they depend on, so bumping an unrelated param doesn't invalidate every stage.

## Experiments

For iterating on a single pipeline without polluting Git history with WIP commits:

```bash
dvc exp run -n exp-baseline               # runs the pipeline, snapshots as a hidden Git ref
vi train.py                               # tweak model code
dvc exp run -n exp-more-epochs -S train.epochs=50   # override a param inline

dvc exp show                              # tabular comparison: params, metrics, code
dvc exp diff exp-baseline exp-more-epochs # what changed, numerically
dvc exp apply exp-more-epochs             # promote the winning experiment into your workspace
dvc exp gc                                # clean up experiments you didn't apply
```

`dvc exp run --queue` + `dvc queue start` lets you batch many `-S param=value` sweeps and run them sequentially or across parallel workers without a scheduler.

## DVCLive: In-Training Logging

For frameworks where you want per-epoch metrics without polling files:

```python
from dvclive import Live

with Live() as live:
    for epoch in range(num_epochs):
        train_one_epoch(...)
        live.log_metric("train/loss", loss.item())
        live.log_metric("val/accuracy", val_acc)
        live.next_step()
    live.log_params({"lr": lr, "batch_size": batch_size})
```

DVCLive writes metrics/params in the format `dvc exp show` expects, and has drop-in callbacks for PyTorch Lightning, Keras, XGBoost, LightGBM, and Hugging Face `Trainer` (`from dvclive.lightning import DVCLiveLogger`, etc.) — no manual `log_metric` calls needed in those cases.

## Common Pitfalls

- **Forgetting to `dvc push` before sharing a repo.** A `git clone` gives collaborators the `.dvc` pointers, not the data — they must `dvc pull` (and have remote credentials configured) or `dvc pull` will error with missing cache objects.
- **Committing large files directly with `git add` instead of `dvc add`.** Once a large blob is in Git history, removing it requires history rewriting; always `dvc add` first for anything above a few MB.
- **Editing a tracked file without going through DVC.** If you `chmod`/edit a file DVC has cached (DVC often uses reflinks/hardlinks or read-only cache files), you can corrupt the cache link. Run `dvc unprotect <file>` before manual edits, or just `dvc add` again after editing.
- **`dvc repro` not detecting a change.** It hashes `deps`/`params`/`cmd` — if your script reads an *undeclared* input (e.g., a config file not listed in `deps`), DVC won't know to re-run. Declare every real input.
- **Remote credentials differ per environment.** `dvc remote modify myremote --local` sets machine-specific secrets (keys, tokens) in `.dvc/config.local`, which is gitignored — don't put credentials in the shared `.dvc/config`.
- **Experiments pile up.** `dvc exp show` gets slow and cluttered after hundreds of runs; periodically `dvc exp gc --workspace` or push relevant ones and prune the rest.

## Resources

- Docs: https://dvc.org/doc
- Command reference: https://dvc.org/doc/command-reference
- DVCLive: https://dvc.org/doc/dvclive
- Source: https://github.com/treeverse/dvc (formerly iterative/dvc)
