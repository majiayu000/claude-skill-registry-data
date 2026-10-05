---
name: huggingface-git-xet-dataset-publisher
description: >-
  Manage Hugging Face dataset Git repositories with Git Xet/LFS-compatible
  tracking, including setup, safe snapshot commits, push verification, binary
  rejection recovery, and README track-rule maintenance.
---

# Hugging Face Git Xet Dataset Publisher

Use this skill when the task is about operating a Hugging Face dataset Git
repository (for example LanceDB data snapshots), including:
- initial setup,
- bootstrap from a non-Git local folder,
- daily commits/pushes,
- binary-rejected push recovery,
- track rule maintenance in `.gitattributes` and `README.md`.

## When To Use
1. Bind a local data directory to `git@hf.co:datasets/<org_or_user>/<repo>`.
2. Configure Git Xet for large/binary dataset artifacts.
3. Commit and push snapshot updates safely.
4. Fix `pre-receive hook declined` binary rejection errors.
5. Standardize tracking rules across docs and repo config.

## Required Inputs
1. `repo_dir`: local dataset repo path (for example `/mnt/wsl/data4tb/static-flow-data/lancedb`).
2. `hf_remote`: dataset SSH remote (`git@hf.co:datasets/...`).
3. `branch`: target branch (default `main`).
4. File patterns that must be Xet-tracked (default below).

Recommended default track patterns for LanceDB-like repos:
1. `*.lance`
2. `*.txn`
3. `*.manifest`
4. `*.idx`
5. Optional extras if present in repo: `*.arrow`

## Hard Rules
1. Always run from `repo_dir` and print current branch/remote before mutation.
2. Never force-push unless user explicitly requests.
3. Before each push, verify offending binary paths are tracked (`filter=lfs`).
4. If a new binary extension appears, update both:
   - `.gitattributes` (track rule),
   - `README.md` setup instructions.
5. Treat `filter=lfs` in `.gitattributes` as expected for Git Xet on HF.
6. If source data is actively being written (for example live LanceDB), pause
   writers before snapshot commit/push to avoid inconsistent snapshots.

## Non-Git Folder Bootstrap (Given HF Remote)
Use this when `repo_dir` is just a plain folder (no `.git`) and user provides
`hf_remote`.

### Step 0: Enter source directory
1. `cd <repo_dir>`

### Step 1: Detect remote state
1. Check if remote already has `main`:
   - `git ls-remote --heads <hf_remote> main`

### Step 2A: Remote already has history (recommended in-place bootstrap)
1. Initialize and bind:
   - `git init`
   - `git remote add origin <hf_remote>`
2. Align local `main` to remote:
   - `git fetch origin main`
   - `git checkout -B main origin/main`

### Step 2B: Remote is empty (first publish)
1. Initialize and bind:
   - `git init -b main`
   - `git remote add origin <hf_remote>`

### Step 3: Enable Xet and add track rules
1. `git xet install`
2. `git xet track "*.lance" "*.txn" "*.manifest" "*.idx"`
3. Optional if present: `git xet track "*.arrow"`

### Step 4: Re-index with tracking and commit
1. Stage all:
   - `git add -A`
2. If files were previously staged/committed without tracking, re-index once:
   - `git rm -r --cached .`
   - `git add -A`
3. Commit:
   - `git commit -m "data: initial sync with xet tracking" || echo "no changes"`

### Step 5: Push
1. `git push origin main`
2. Verify:
   - `git rev-list --left-right --count origin/main...main`
   - expected after success: `0    0`

## Preflight Checklist
1. Verify tooling:
   - `git --version`
   - `git lfs version`
   - `git xet --version`
2. Verify remote:
   - `git remote -v`
3. Verify branch/divergence:
   - `git branch -vv`
   - `git fetch origin`
   - `git rev-list --left-right --count origin/main...main`
4. Verify current tracking:
   - `git check-attr filter -- <sample_file>`
   - `git lfs ls-files | head`

## Setup Workflow (First-Time)
1. Initialize or bind repo:
   - `git init -b main` (if needed)
   - `git remote add origin <hf_remote>`
   - `git fetch origin main`
   - `git switch -C main origin/main`
   - if folder is not a Git repo yet, prefer the full bootstrap section above
     (`Non-Git Folder Bootstrap (Given HF Remote)`).
2. Install/enable Xet (if not already):
   - `git xet install`
3. Add track rules:
   - `git xet track "*.lance"`
   - `git xet track "*.txn"`
   - `git xet track "*.manifest"`
   - `git xet track "*.idx"`
4. Validate:
   - `rg -n "\\*\\.(lance|txn|manifest|idx)" .gitattributes`

## Daily Snapshot Workflow
1. Confirm clean branch target:
   - `git switch main`
   - `git fetch origin`
2. Add/commit:
   - `git add -A`
   - `git commit -m "data: sync <timestamp>" || echo "no changes"`
3. Push:
   - `git push origin main`
4. Post-push sanity:
   - ensure no remote rejection,
   - ensure expected commit appears in `git log --oneline -n 3`.

## Binary Rejection Recovery Workflow
Error signature:
- `Your push was rejected because it contains binary files`
- `Offending files: .../*.idx` (or another extension)

### A) Diagnose precisely
1. Check whether offending files are tracked:
   - `git check-attr filter -- <offending_path>`
2. If `filter: unspecified`, add missing rule:
   - `git xet track "*.idx"` (or relevant extension)

### B) Recover from contaminated local history safely
Use this when local `main` has bad commits and push keeps failing.

1. Preserve local pointer:
   - `git switch -c backup/pre-xet-fix-<timestamp>`
2. Align `main` to clean remote tip:
   - `git switch -C main origin/main`
3. Re-apply current local data changes (if any), then:
   - `git add -A`
   - `git commit -m "data: sync and fix xet tracking"`
4. Push:
   - `git push origin main`

### C) Alternative clean-branch publication
Use when branch surgery on local `main` is undesirable.

1. Create clean branch from remote tip:
   - `git switch -c clean-main origin/main`
2. Bring desired files into clean branch.
3. Ensure track rules include offending extension(s).
4. Commit and publish:
   - `git push origin clean-main:main`
5. Realign local main:
   - `git switch -C main origin/main`

## README Maintenance Contract
Whenever adding a new tracked binary extension:
1. Add it to `.gitattributes` via `git xet track`.
2. Update README setup snippet so future runs include it.
3. Update storage-format description if needed (for example mention `*.idx` sidecars).

## Verification Commands (Must Run Before Final Report)
1. `git rev-list --left-right --count origin/main...main`
   - expected after success: `0    0` or `0    N` before final push.
2. `git check-attr filter -- <offending_paths>`
   - expected: `filter: lfs`
3. `git lfs ls-files | rg "\\.idx$"` (or relevant extension)
   - expected: tracked pointers listed.
4. Optional pointer inspection:
   - `git show :<path> | sed -n '1,3p'`
   - expected:
     - `version https://git-lfs.github.com/spec/v1`

## Reporting Template
Always report:
1. remote/branch operated,
2. exact tracking patterns currently active,
3. whether README was updated,
4. divergence before/after (`origin/main...main`),
5. final push result and commit hash.
