---
name: worktree-data-sync
description: Sync non-git data (datasets, outputs, caches, symlinked data) between git worktrees. Use proactively whenever creating or entering a worktree whose work depends on non-git-tracked data — seed the data in before dispatching or doing work there — and to seed, diff, reconcile, or tear down managed data between existing worktrees.
user-invocable: true
---

# Worktree Data Sync Skill

Non-git data sync between existing worktrees — seed, diff, apply, data teardown. Worktree lifecycle (create / enter / remove): `skills/agent-orchestration/references/worktree-harness-fallback.md`.

## When to Use

Activate the data-sync CLI below for:
- seeding non-git-controlled data from one existing worktree into another
- comparing non-git files across existing worktrees
- copying managed data between worktrees
- reconciling non-git differences after parallel work

## Command Surface

Single CLI entrypoint (`<skill-dir>` = directory containing this `SKILL.md`; `--from` defaults to the worktree containing the caller's current directory):

```bash
python3 <skill-dir>/scripts/sync_worktree_data.py --to <worktree-path> --mode <seed|diff|apply> [OPTIONS]
```

## Modes

### `--mode seed`

Materialize missing managed files in destination from source. Never overwrites existing destination files.

Per managed directory root, a stat-only preflight walk picks the cheapest path:
- **fresh, clean destination:** one `cp -c -R -p` clones the whole root (COW where the filesystem supports it, falling back to `shutil.copytree`)
- **fresh destination with cloud-placeholder (dataless) files:** only the directories holding a placeholder are recreated — placeholders become symlinks to their resolved source, siblings clone whole, loose files batch-copy
- **more than half the root's files are dataless:** seeds per-file (symlink placeholders, batch-copy the rest) and prints a suggestion to annotate the root `# data-sync:symlink`, since it never switches modes automatically
- **destination root already exists:** falls back to the per-file merge walk, copying only what's missing

Every failed path is recorded with its reason; seed prints the listing to stderr (capped, plus a total count) and exits nonzero when any path failed.

Optional: `--seed-sync-mode <auto|force-symlink|force-cow>` (default: `auto`)

- `auto`: preserve current per-path behavior (symlink-only roots get symlinks, others get copies)
- `force-symlink`: create top-level symlinks for all managed roots when the destination path does not already exist; conflicting paths are skipped
- `force-cow`: copy/COW all managed roots, including symlink-only annotated paths

`--seed-sync-mode` is valid only with `--mode seed`; the CLI rejects it elsewhere.

### `--mode diff`

Report source-to-destination differences for managed files.

Statuses:
- `new`: exists in source but missing in destination
- `modified`: exists in both but differs
- `unchanged`: identical (only shown with `--include-unmodified`)

Output options:
- human-readable report (default)
- JSON report (`--json`), compatible with apply mode

### `--mode apply`

Execute sync actions for selected changes.

Actions:
- `--action overwrite`: copy source file to destination path
- `--action rename`: copy source file to destination with suffix

Selection options:
- `--from-json <file>` from prior diff output
- `--files <path...>` for explicit relative paths
- omit both to auto-process current diff (`new` + `modified`)

No delete/discard action is provided.

## Managed Path Discovery

Discovery is stateless and source-driven. Managed roots come from:
- gitignored paths via `git ls-files --others --ignored --exclude-standard --directory`, minus a built-in denylist (below)
- tracked symlinks that resolve outside the repo
- top-level symlink safety net, skipping symlinks git already tracks (git checks those out in the destination)
- `.gitignore` symlink-only annotations

A gitignored entry whose basename matches a well-known non-data name — `.venv`, `venv`, `.direnv`, `node_modules`, `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.tox`, `.nox`, `.cache`, `.ipynb_checkpoints`, `.quarto`, `dist`, `build`, `*.egg-info`, `.DS_Store`, `.env`, `.envrc`, `.worktrees`, `.claude`, `.codex` — is excluded from managed entries. The denylist filters discovered entries only — it excludes nothing from inside an otherwise-managed root. A `# data-sync:symlink` annotation always wins over the denylist, so an annotated root stays managed even under a denylisted name.

Annotate a path as symlink-only by adding a **duplicate line** with the tag comment:

```gitignore
Data/
Data/  # data-sync:symlink
```

The first line is the actual gitignore rule; the second is the annotation the discovery script parses.
Legacy tag `# worktree:symlink` is also supported.

Symlink-only roots are symlinked in seed auto mode and excluded from diff/apply actions.

## Examples

```bash
# Seed from the current worktree into destination
python3 <skill-dir>/scripts/sync_worktree_data.py \
  --to ../MyRepo-feature \
  --mode seed

# Seed using top-level symlinks for all managed roots
python3 <skill-dir>/scripts/sync_worktree_data.py \
  --to ../MyRepo-feature \
  --mode seed \
  --seed-sync-mode force-symlink

# Seed using copy/COW for all managed roots (including symlink-only)
python3 <skill-dir>/scripts/sync_worktree_data.py \
  --to ../MyRepo-feature \
  --mode seed \
  --seed-sync-mode force-cow

# Diff explicit source -> destination
python3 <skill-dir>/scripts/sync_worktree_data.py \
  --from ../MyRepo-expA \
  --to ../MyRepo-expB \
  --mode diff --json

# Apply overwrite using diff json
python3 <skill-dir>/scripts/sync_worktree_data.py \
  --to ../MyRepo-expB \
  --mode apply \
  --from-json /tmp/changes.json \
  --action overwrite

# Apply rename for explicit files
python3 <skill-dir>/scripts/sync_worktree_data.py \
  --from ../MyRepo-expA \
  --to ../MyRepo-expB \
  --mode apply \
  --files output/result.csv notes/draft.md \
  --action rename \
  --suffix _from_expA
```

## Data Teardown

Materialized data inside a worktree (copies, COW clones, symlinks created by `--mode seed`) disappears when the worktree directory is deleted — no separate "unseed" step. The source worktree's data is untouched.

Worktree removal itself (`git worktree remove`, branch deletion, safety checks): `skills/agent-orchestration/references/worktree-harness-fallback.md` §Remove.

## See Also

- `skills/agent-orchestration/references/worktree-harness-fallback.md` — worktree lifecycle (create / enter / remove), harness tools preferred, raw-git fallback, placement conventions.
- `skills/agent-orchestration/references/parallel-dispatch.md` — when parallel subagents each need their own worktree, and how data seeding fits into that flow.
