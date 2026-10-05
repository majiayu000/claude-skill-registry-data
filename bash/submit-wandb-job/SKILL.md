---
name: submit-wandb-job
description: Submit one or more wandb-logged training/finetuning runs to the HPC scheduler. `WANDB_PROJECT` is fixed per repo (snake_case basename); `WANDB_RUN_GROUP` is picked per invocation. The training script must take the experiment/group name as a config key (e.g. Hydra `meta.experiment_name=<group>`); the skill passes it on the command line. The working tree is committed first so each run pins to a real SHA. Delegates SLURM/PBS templating to `cluster-instructions`. Use when the user asks to submit, queue, launch, or kick off a wandb training/finetuning job.
argument-hint: "[N (jobs, default 1)] [--group <name>] [--one-off] [--skip-commit-check]"
allowed-tools: Bash, Read, Grep, Glob, Write, Edit, Skill, AskUserQuestion
---

# Submit wandb Job

Enforces a wandb/commit contract on top of `cluster-instructions`. For training/finetuning runs that log to wandb — not eval-only jobs.

## Contract

| Env var | Value | Scope |
|---|---|---|
| `WANDB_PROJECT` | `.env: WANDB_PROJECT` or snake_case repo basename | constant per repo |
| `WANDB_RUN_GROUP` | user, per invocation (`tmp` for one-offs) | one per invocation |
| `WANDB_NAME` | `<group>__<tag>` | one per job |

The skill exports these env vars in the job script. **The experiment/group name must be a config key in the training script** (e.g. Hydra `meta.experiment_name`, or whatever the project's equivalent is) — the user's command should include the override (e.g. `... meta.experiment_name=<group>`) so the training code receives the same value the skill sets in `WANDB_RUN_GROUP`. If the training script hardcodes the experiment name or the wandb project, that's a real bug in the project — surface it and ask the user to fix it; don't paper over it from this skill.

## Step 0 — Pre-flight

```bash
git rev-parse --show-toplevel    # → REPO_ROOT; bail if not a git repo
git symbolic-ref -q HEAD         # → branch ref; empty + non-zero exit = detached
git status --porcelain           # → DIRTY (string)
```

Also read `.env` (walking up from `$PWD` to `$REPO_ROOT`) and capture `JOBS_DIR` and `LOGS_DIR` if defined — Step 2 and Step 5 both need them. Fall back to `$REPO_ROOT/jobs` and `$REPO_ROOT/logs` respectively if unset.

Refuse on: not a git repo. On detached HEAD (Step 0's `git symbolic-ref` returned non-zero), ask once whether to proceed against the bare SHA — abort if the user says no.

## Step 1 — Project (constant)

`.env: WANDB_PROJECT` if set, else snake_case of `basename $REPO_ROOT` (lowercase, `-` → `_`, strip non-`[a-z0-9_]`, collapse `_`). Show it to the user. If they override, ask whether to persist the override into `.env` (so it stays constant next time) — don't write silently.

## Step 2 — Group

If `--one-off` was passed, set `group = tmp` and skip the picker. If `--group <name>` was passed or the user named a group in the conversation, use that.

Otherwise gather candidates and ask:

- `$JOBS_DIR/<project>/*/` — prior groups from this skill (skip if `JOBS_DIR` is unset).
- `$LOGS_DIR/wandb/run-*/files/config.yaml` — grep `group:`, dedupe, cap at 10 most recent (skip if `LOGS_DIR` is unset).
- A fresh slug from a salient piece of the user's command, only if the command actually hints at one.

Present via `AskUserQuestion` with up to 3 existing groups + `tmp` as a first-class option + Other. If one existing group is a strong semantic match for what the user is running ("another seed for the dropout sweep" + an existing `mlm_tune_dropout`), recommend it explicitly. If there are no candidates at all, ask freeform.

Validate: `[A-Za-z0-9_.-]+`, non-empty, no whitespace.

## Step 3 — Commit gate

If `DIRTY` is empty: capture `HEAD_SHA`, continue.

If `DIRTY` non-empty and `--skip-commit-check`: capture `HEAD_SHA`, set `commit_pinned=false`, continue (warn in the final report).

Otherwise show `git status --short` + `git diff --stat`, then ask **once** via `AskUserQuestion`:

- **Commit (recommended)** — `git add -u`, propose a one-liner from the diff, `git commit` (let hooks run; never `--no-verify`). Re-stage and retry once if hooks rewrite. Verify clean, then capture new `HEAD_SHA`.
- **Bypass** — `commit_pinned=false`. Report will flag it.
- **Cancel** — abort.

Don't include untracked files unless the user says so.

## Step 4 — Per-job details

Ask for `N` if not in `$ARGUMENTS` (default 1). For each job collect:

- **Command** — full invocation (user usually states it; ask if not). Skill is agnostic to Hydra/argparse/CLI shape — don't parse it, but do check that the command sets the experiment/group name as a config key (e.g. `meta.experiment_name=<group>`). If it doesn't, ask the user to add it before continuing — the `WANDB_RUN_GROUP` env var alone won't reach a Hydra config.
- **Tag** — short, used in `WANDB_NAME` and the script filename (`lr1e-3`, `seed42`). Default to `j<i>` or a salient `=value` from the command if the user omits one. Validate the same way as the group: `[A-Za-z0-9_.-]+`, non-empty, no whitespace.

If `N > 1` and the user hasn't said how the jobs differ, ask — don't invent ablations.

## Step 5 — Cluster + paths

Invoke `cluster-instructions` (Skill tool) for scheduler detection and templates. Don't submit from this skill directly. `mkdir -p $JOBS_DIR/<project>/<group>/logs` (using the `JOBS_DIR` resolved in Step 0). The `<project>` outer level matches `monitor-jobs`' documented `$JOBS_DIR/<project>/` layout; `<group>` nests inside so related runs cluster on disk too.

## Step 6 — Generate scripts

One script per job at `$JOBS_DIR/<project>/<group>/<group>__<tag>.{sh,batch}`. Use the scheduler header from `cluster-instructions`. Before the user's command:

```bash
export WANDB_PROJECT="<project>"
export WANDB_RUN_GROUP="<group>"
export WANDB_NAME="<group>__<tag>"
cd "$REPO_ROOT"
```

Logs to `logs/<group>__<tag>.out` (PBS) or `logs/<group>__<tag>_%j.out` (SLURM), relative to the submission dir — matches `monitor-jobs` expectations.

Show the scripts (`cat`) and pause for confirmation if `N > 3` or `commit_pinned=false`. Otherwise just submit.

## Step 7 — Submit

`sbatch` / `qsub` per script. Capture job IDs as you go. On any failure, stop — don't retry, don't continue to the next job. If jobs *k+1..N* failed but jobs *1..k* already made it into the queue, list those job IDs and ask via `AskUserQuestion` whether to `scancel` / `qdel` them or leave them running. Don't auto-cancel; the user may want the already-submitted runs to proceed.

## Step 8 — Report

```markdown
## Submitted <N> job(s) to <cluster>

- **project**: `<project>`   **group**: `<group>`
- **commit**: `<short-SHA>` — `<subject>`    <!-- or "dirty submit — not pinned" if commit_pinned=false -->
- **logs**: `<absolute path>`

| # | Job ID | Tag | Script | Log |
|---|---|---|---|---|

Monitor: `/softnano:monitor-jobs`.
```

Repeat the dirty-submit warning at the bottom if applicable.

## Hard rules

- Never edit the user's training code to fit the env contract — if it hardcodes the project or experiment name, surface it and let the user fix it.
- Wandb auth (`WANDB_API_KEY` / `~/.netrc`) is not this skill's problem — let the job fail at runtime if it's missing.
