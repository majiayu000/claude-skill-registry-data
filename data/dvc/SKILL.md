---
name: dvc
description: >
  Interactive runner for DVC (Data Version Control) data-management commands in this
  Orbit Wars repo. Triggered explicitly by the user with /dvc. Presents the available
  DVC operations (status / dag / diff / metrics show / pull / push / fetch / add /
  commit) via a concise user question, confirms riskier ones, and executes them with the
  repo-specific conventions baked in (uv via the backend venv, shared cache at
  /Users/user/project/orbit-wars/.dvc/cache, S3 remote `s3` with AWS profile
  `orbit-wars`). Use whenever the user types /dvc or asks to run DVC commands such
  as "push my data", "pull the latest weights", "show DVC status", "what changed in
  the pipeline outputs", or "register this directory with DVC", and they have not
  already specified the exact subcommand themselves.
---

# DVC Data Management Skill

Run DVC commands interactively in the Orbit Wars repo. The user invokes this with `/dvc` when they want to inspect, sync, or register data without remembering the specific subcommand.

## When this skill is in charge

- The user typed `/dvc` (explicit trigger), or
- The user asked for a DVC operation in plain language and didn't pre-select the subcommand (e.g. "sync my data", "push the weights")

If the user already wrote a specific command (`dvc push`, `dvc status -c`), just run it directly — no need for the menu.

## Repo conventions to remember

These keep the commands working correctly without relitigating them every run:

- DVC binary: `backend/.venv/bin/dvc` (the venv has `dvc[s3]` installed). Calling plain `dvc` from outside `backend/` may not be on PATH; the venv path is reliable from any cwd.
- Run from the **repo root** (`/Users/user/project/orbit-wars.worktrees/<branch>/` or the main repo). `dvc.yaml` lives at the root.
- Default remote is `s3` with profile `orbit-wars` (configured in `.dvc/config.local`). No `--remote` flag needed.
- Shared cache is `/Users/user/project/orbit-wars/.dvc/cache` so multiple worktrees deduplicate — but **don't run two `dvc repro` / `dvc push` simultaneously** (lock contention). For pull/status the read concurrency is fine.
- `data/` contents are DVC-managed; only `*.dvc` stubs and `.gitignore` are committed to git. `dvc add` / `dvc commit` autostage stubs into git.

## Interaction flow

The skill walks the user through three quick decisions: **category → command → arguments**, then confirms before executing risky ones.

User-facing strings (a concise user question labels and descriptions, end-of-run summaries) should be in **Japanese** to match this project's response-language convention. The internal reasoning and SKILL.md instructions stay in English.

### Step 1 — Pick a category

Ask one question with these options:

- **状態確認** (status / dag / diff / metrics show) — read-only, fast, free
- **同期** (pull / push / fetch) — talks to S3, may transfer data
- **管理** (add / commit) — registers / updates DVC tracking

Skip directly to the matching subcommand if the user's `/dvc` invocation already named one (e.g. `/dvc push` or "I want to push").

### Step 2 — Pick the specific command

Show only the commands inside the chosen category. Each option's description tells the user what it actually does and any caveats:

**状態確認**:
- `dvc status` — local workspace vs cache differences
- `dvc status --cloud` — local cache vs S3 remote (does my push need to run?)
- `dvc dag` — render the stage dependency graph
- `dvc diff [<rev>]` — diff outs against a git rev (default: HEAD)
- `dvc metrics show` — print metrics file contents (eval_metrics.json etc.)

**同期**:
- `dvc pull` — fetch missing outs from S3 to local cache + workspace
- `dvc fetch` — like pull but only into cache (no workspace materialization)
- `dvc push` — upload locally-changed outs to S3 (large transfer possible)

**管理**:
- `dvc add <path>` — start tracking a directory/file outside `dvc.yaml` (creates `<path>.dvc`)
- `dvc commit [<stage>]` — record current outs to `dvc.lock` without re-running stages (use after manual edits the user trusts)

### Step 3 — Gather arguments

Ask only when the chosen command needs a target:

- `dvc status` (no flag) — no extra question
- `dvc status --cloud` — no extra question
- `dvc dag` — no extra question (output is text)
- `dvc diff` — ask for the git ref (default: HEAD)
- `dvc metrics show` — no extra question
- `dvc pull` / `dvc fetch` — ask whether to pull everything or a specific path/stage; default = everything
- `dvc push` — same shape as pull
- `dvc add` — ask for the path (free text). Resolve relative to repo root.
- `dvc commit` — ask which stage(s); default = all stages with `--force`

### Step 4 — Confirm before executing if it could surprise the user

Re-confirm with a yes/no a concise user question **only** for these cases — they either move data on the network, change git-tracked files, or are hard to undo:

- `dvc push` — uploads to S3, possibly large. Run `dvc status --cloud` first if you can do it cheaply, and quote how many objects are out of sync; otherwise just confirm the action.
- `dvc add <path>` — creates a `.dvc` stub and may modify `.gitignore` under the path.
- `dvc commit --force` — overwrites recorded hashes; the user is asserting the current outs are intentional.

For everything else, announce what you're about to run and execute. The user already chose it.

### Step 5 — Run

Execute via Bash with cwd at the repo root:

```bash
backend/.venv/bin/dvc <subcommand> [args]
```

For long-running operations (`dvc push`, `dvc pull` of a fresh checkout, `dvc add` on a multi-GB directory), use Bash with `run_in_background: true`. The user gets a notification on completion. Don't poll in a loop.

After completion, show a one-line summary (e.g. "1423 files pushed", "remote in sync", or the truncated tail of stderr on failure). For `dvc dag` and `dvc metrics show`, just print the output verbatim.

## Why this skill exists (not just "run dvc")

Three reasons the menu is worth the few seconds:

1. **The repo has tribal knowledge** — venv path, profile, lock-contention rule, autostage behaviour. Hardcoding these into the skill saves the user from "command not found" / "no credentials" / wrecking a parallel job.
2. **A handful of DVC commands are destructive or expensive** — `commit --force`, `push` of a multi-GB dataset. A 5-second confirmation prevents an irreversible mistake.
3. **The user wants to pick from a list, not memorize flags** — that's the explicit ask. Driving the choice with a concise user question lets them scan options instead of recalling syntax.

## Examples

**Example 1 — explicit trigger, no subcommand**

User: `/dvc`

You: ask Step 1 (category), then Step 2 (subcommand), then Step 3 if needed, confirm if Step 4 applies, then run.

**Example 2 — natural-language**

User: "push my changes to S3"

You: skip Step 1 (category is 同期). Skip Step 2 (subcommand is `push`). Step 4 confirms ("Push current cache to S3?"), then run `backend/.venv/bin/dvc push`.

**Example 3 — already specific**

User: "run `dvc status --cloud`"

You: don't run the menu — just execute it (no confirmation needed for read-only). Print the output.

**Example 4 — ambiguous**

User: "is my data up to date?"

You: this needs a read of remote vs local. Run `backend/.venv/bin/dvc status --cloud` directly and report. No menu — the question maps to one specific command.

## Failure modes to handle

- **`dvc: command not found`** — fall back to `uv run --directory backend dvc ...`. If that also fails, tell the user `dev/setup` (uv sync) is needed.
- **`Unable to locate credentials`** — point the user at `dev/dvc setup` to wire up the AWS profile and `~/.aws/credentials`.
- **`failed to commit - ... is outside of git repository`** — the worktree's `data/` is still a symlink to the main repo. Suggest the migration steps documented in `docs/plans/dvc-data-control/03-architecture.md` rather than improvising.
- **lock contention** (`Unable to acquire lock`) — another DVC process (probably another worktree) is running. Don't retry blindly; tell the user, suggest waiting or `ps -ef | grep dvc`.

When a command fails, paste the last 10–20 lines of stderr verbatim. Don't paraphrase — the actual DVC error message usually tells the user exactly what to fix.
