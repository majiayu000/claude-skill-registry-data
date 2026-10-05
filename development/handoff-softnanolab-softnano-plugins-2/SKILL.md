---
name: handoff
description: Package an in-progress task on this cluster so a Claude agent on another cluster (MMM Young, CX3, HX1, Isambard) can pick it up, or resume a task handed off to this cluster. Use when the user says hand off / migrate / continue this on <cluster>, or asks you to pick up an existing handoff.
argument-hint: "[resume [branch-or-path]] | [target-cluster] [notes]"
allowed-tools: Bash, Read, Grep, Glob, Write, Edit
---

# Handoff

Move an in-flight task between clusters. Two modes:

- **Mode A — create** (default): gather the real state of the work here, write `HANDOFF.md`, commit the WIP, push a branch.
- **Mode B — resume** (`$ARGUMENTS` starts with `resume`): find a handoff on this cluster, verify the environment against it, continue the task.

**The reader is another Claude agent, not a human.** Write imperatives, verified facts, and runnable commands. No narrative, no reassurance, no "we should probably". A fact you did not confirm with a command is marked `UNVERIFIED` — never asserted.

## Input

<args>
$ARGUMENTS
</args>

- Starts with `resume` → Mode B. The rest is an optional branch name or path to a handoff file.
- Anything else → Mode A. First token is the target cluster if it matches one of `cx3`, `hx1`, `mmm`, `mmm-old`, `isambard`; the remainder is free-text notes about what to prioritise. If no target is given, ask which cluster before writing the doc — the environment and data sections cannot be written without it.

---

# Mode A — create a handoff

## Step 0: Pre-flight

```bash
git rev-parse --is-inside-work-tree
git rev-parse --abbrev-ref HEAD
git remote -v
gh auth status
hostname -f 2>/dev/null || hostname
pwd
```

Run the `cluster-instructions` skill to identify the **source** cluster and its scheduler. Read the target cluster's file from that skill (`cx3.md`, `mmm-slurm.md`, `mmm-sge.md`, `isambard.md`) before writing the environment section — the module and venv recipes go in the doc verbatim, not from memory.

Hard stops:

- Not a git repo, or no `origin` remote — git is the transport. Fall back to Step 5's no-remote path only if the user confirms.
- Current branch is `main`/`master` with uncommitted work — do not push `main`. Create a `handoff/<slug>` branch in Step 5.

## Step 1: Gather facts

Do not write a single line of the document from memory of this conversation alone. Everything except the task narrative comes from a command.

**Git state**

```bash
git status --porcelain
git log --oneline -10
git log --oneline @{upstream}..HEAD 2>/dev/null || echo "no upstream"
git diff --stat $(git merge-base HEAD origin/main)..HEAD
git diff --stat            # unstaged
git stash list
git worktree list
```

**Scheduler state** — jobs still running here are the most dangerous thing to get wrong.

```bash
squeue -u "$USER" 2>/dev/null || qstat -u "$USER" 2>/dev/null || echo "no scheduler"
```

For each live job, capture: job ID, the submit script path, elapsed/remaining walltime, what it writes, and the tail of its log. Use the `monitor-jobs` skill if the jobs are non-trivial.

**W&B state**

```bash
ls -dt "$LOGS_DIR"/wandb/run-*/ 2>/dev/null | head -5
grep -rho "wandb.ai/[^ ]*" "$JOBS_DIR" --include="*.log" 2>/dev/null | tail -5
```

Record project, run group, and run IDs, plus which run each live job is writing to.

**Environment and data**

```bash
sed -E 's/^([A-Z_]*(TOKEN|KEY|SECRET|PASSWORD)[A-Z_]*)=.*/\1=<redacted>/' .env 2>/dev/null
du -sh "$DATA_DIR"/* 2>/dev/null
ls -lh "$LOGS_DIR"/*/*/checkpoints/last.ckpt 2>/dev/null | tail -10
python --version; uv --version 2>/dev/null; module list 2>&1 | head
```

**Task narrative** — the only part you author: what is done, what is half-done, what the next concrete action is. Ground each claim in a commit, a file, or a job ID.

## Step 2: Decide what travels

| Thing | Default | Rule |
|---|---|---|
| Source code | git branch | Always. Commit WIP even if broken — say it's broken in the doc. |
| Datasets | rebuild on target | If a build script exists (`scripts/data_processing/*`), give the rebuild command. Only transfer when there is no deterministic rebuild path. |
| Checkpoints | transfer the minimum | Usually just `last.ckpt` for the run being continued. State the size. |
| Logs / W&B run dirs | do not transfer | Reachable from the W&B UI. |
| Secrets | never | The target has its own `.env`. |
| Live jobs | stay put | Never migrate a running job silently — see below. |

If a transfer exceeds ~5 GB, put the size in the doc and flag it as a decision for the user rather than assuming it should be copied.

Transfer commands go in the doc as literal, runnable lines — `rsync -avP`, `rclone copy`, or `scp` with the SSH alias from the target's cluster-instructions file (`mmm`, `mmm-old`, `hx1`). Note in the doc which direction actually has network reachability; Imperial and UCL clusters are not always mutually reachable, and the transfer may have to be driven from a third machine.

**Live jobs are not migrated.** For each one, record an explicit action for the receiving agent: `let it finish` (default), `kill after target reproduces it`, or `already dead`. The receiving agent must never relaunch a job that is still running here — duplicate runs corrupt W&B history and burn allocation. Only kill jobs on the source cluster if the user asks.

## Step 3: Redaction

Before writing, confirm the doc contains no `WANDB_API_TOKEN`, `NOTION_API_TOKEN`, API keys, passwords, or SSH private key material. Env vars appear as **names and meanings**, never values, except for non-secret paths. This file gets committed and pushed — treat it as public to the repo's collaborators.

Also strip source-cluster absolute paths from anything the target will run. `$DATA_DIR/pdb` travels; `/rds/general/user/hxa/home/MENTOS/DATA/pdb` does not.

## Step 4: Write the document

Read `handoff-template.md` from this skill's directory and fill every section. Delete a section only if it is genuinely empty (write `None` rather than dropping the heading — a missing heading reads as "not considered").

Write it to `HANDOFF.md` at the repo root. Root, not a subdirectory: the receiving agent should hit it on `ls` without being told where to look.

## Step 5: Commit and push

```bash
SLUG=<short-kebab-task-slug>
git checkout -b "handoff/$SLUG"      # skip if already on a feature branch worth keeping
git add -A                            # review `git status` first — never add data, checkpoints, or logs
git add HANDOFF.md
git commit -m "WIP handoff: <task> (<source-cluster> → <target-cluster>)"
git push -u origin "handoff/$SLUG"
```

Rules: never push `main`, never force-push, never amend a commit that is already pushed. If untracked files are large or clearly not source, leave them out and note in the doc how to regenerate them.

If there is no reachable remote, fall back in this order: (1) write the doc to a filesystem both clusters mount, (2) `git bundle create` plus an `rsync` line in the report, (3) print the doc for the user to paste. Say which fallback you used.

## Step 6: Report

```markdown
## Handoff written: <task>

- Source: <cluster> (<scheduler>) → Target: <cluster> (<scheduler>)
- Branch: `handoff/<slug>` @ <short-sha> — pushed to origin
- Document: `HANDOFF.md` (<n> sections)
- Live jobs left running here: <ids or none>
- Transfers required before work resumes: <none | list with sizes>

On the target cluster, run:

    git fetch origin && git checkout handoff/<slug>
    /softnano:handoff resume
```

State any open question the receiving agent cannot answer alone.

---

# Mode B — resume a handoff

## Step 0: Locate it

In order: the ref or path in `$ARGUMENTS`; then `HANDOFF.md` in the current checkout; then

```bash
git fetch origin
git branch -r --list "origin/handoff/*" --sort=-committerdate
```

If several match, list them with dates and ask which. Never guess between two handoffs.

## Step 1: Read before touching

Read the whole document first. Do not run, edit, or submit anything until you have. In particular read the live-jobs and W&B sections before submitting any job — the most likely failure mode of a handoff is launching a duplicate of something already running on the source cluster.

## Step 2: Verify the environment

Run the document's verification checklist, plus:

```bash
hostname -f; pwd
git log --oneline -3
cat .env 2>/dev/null | cut -d= -f1        # which vars exist here
ls "$DATA_DIR" "$LOGS_DIR" "$JOBS_DIR" 2>&1 | head
```

Use `cluster-instructions` to confirm which cluster this is and to get the correct module/venv recipe — the source cluster's recipe in the doc is context, not instructions to run here.

Report every mismatch (missing dataset, absent env var, different Python version) as a checklist with pass/fail. Do not paper over a failure by improvising a path; a wrong `DATA_DIR` produces a run that trains on the wrong thing and looks fine.

## Step 3: Translate the scheduler

Job scripts in the doc are written for the source scheduler. Rebuild them from the target's template in `cluster-instructions` (`cx3.md` for CX3/HX1 PBS, `mmm-slurm.md` / `mmm-sge.md` for MMM, `isambard.md` for Isambard). Carry over the *intent* — GPUs, walltime, node count, env vars — not the directives.

## Step 4: W&B continuity

Follow the doc's instruction. Default when it is silent: **start a new run** and record the parent run ID in the config or notes. Resuming an existing run ID from a second cluster while the original may still be writing corrupts the history.

## Step 5: Confirm, then continue

Summarise for the user: what the task is, what verified clean, what did not, and the next action from the doc. Get a go-ahead if anything failed verification or if the next action costs GPU time. Then do the work.

Delete `HANDOFF.md` in the first commit of real work — it is a transport artifact, not documentation. It must not survive into a PR.

---

## Hard rules

- Never write secrets into the handoff document.
- Never push `main`, never force-push, never amend a pushed commit.
- Never relaunch a job that the doc says is still running on the source cluster.
- Never kill or requeue source-cluster jobs without the user asking.
- Never carry a source-cluster absolute path into a target-cluster command.
- Anything unverified is labelled `UNVERIFIED` in the doc. A confident wrong fact is worse for the receiving agent than an admitted gap.
