---
name: gz-init
description: Use to bootstrap, reinitialize or repair a repository's gzkit governance scaffolding.
category: governance-infrastructure
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
gz_command: init
metadata:
  skill-version: "6.4.1"
model: sonnet
---

# gz init

## Overview

`gz init` (`init` in `src/gzkit/commands/init_cmd.py`) has three modes, chosen
by the state of the working directory and the flags. It always acts on the
current directory; it never searches upward for a project.

- **First init** — no `.gzkit/` yet, or `--force`. Writes `.gzkit.json` from
  the detected project structure, the manifest, the `design/` directories
  (`prd`, `constitutions`, `adr`), the Python skeleton unless `--no-skeleton`
  (`pyproject.toml`, `README.md`, `src/<package>/__init__.py`,
  `tests/__init__.py`, then `uv sync` when `.venv` is absent), `.gitignore`,
  `.pre-commit-config.yaml` with the pre-push `gz check` gate, and
  `data/audit_thresholds.json`. In a git worktree it runs `pre-commit install`
  for every declared hook type, installs the commit-locus recorder when
  `post-commit` is declared, and registers the `gzkit-jsonl` merge driver. It
  copies the wheel's canonical skills, chores, personas, templates and rules
  into `.gzkit/`, runs the sync preflight, syncs the control surfaces, and
  offers to register PRDs and ADRs it finds. Ledger: one `project_init` and an
  `agent_sync_completed` per sync.
- **Repair** — `.gzkit/` exists, no `--force`, no `--update`. Adds what is
  missing and never overwrites: skeleton, `design/` directories, `.gitignore`,
  pre-commit config, new canonical skills, rules, personas, templates and
  chores, the chores registry merge (`--yes` accepts its prompt), the
  manifest, and `authorship.attestor_handle` when `--attestor-handle` is given.
  Then it syncs the control surfaces, listing only files the sync changes; an
  already-synced tree runs no sync and appends no ledger row. In a git
  worktree with a pre-commit config, every repair re-runs `pre-commit install`
  and rewrites the recorder hook, so it always reports at least those.
- **Update** (`--update`) — refreshes `.gzkit/` skills, rules, chores, personas
  and templates from the installed wheel by `_detect_refresh_state`:
  `IDENTICAL` is skipped; `STALE` (the copy equals a version gzkit shipped, per
  the wheel's `canonical_history.json`, or is missing) is overwritten; `EDITED`
  (any other difference, so an operator edit) is reported and left. It writes only what delivery defines: `gz upgrade`'s classifiers pick
  the skills, rules, templates and personas, chores follow first-init delivery,
  and `chores/registry.json` is merged, keeping project-local entries (`--yes`
  accepts the merge). Nothing else runs: no manifest, no sync, no ledger event.

Exit codes: 0 on success; 1 for `--update` with `--force` or
`--attestor-handle`, `--update` on an uninitialized project, a handle
containing whitespace, or a canonical-skill sync preflight failure; 3 when
`--update` leaves an `EDITED` conflict.

## Workflow

1. Choose the mode. A new repository: `uv run gz init` (default `--mode lite`),
   with `--attestor-handle <handle>` to record the operator's handle. An
   existing one: repair, or `--update` after a gzkit upgrade. `--mode` is read
   only by first init.
2. Preview with `--dry-run`. In repair and update it writes nothing and lists
   what the real run would write; for an artifact repair would newly scaffold,
   its `Would scaffold` line stands in for that artifact's mirrors
   (GHI #1098). A first-init dry run prints a fixed list of steps.
3. Run it. When repair exits 1 on the sync preflight, it has already made the
   listed repairs and left every mirror unchanged: fix the canonical skills
   under `.gzkit/skills/` and re-run.
4. After `--update`, run `uv run gz agent sync control-surfaces`: `--update`
   refreshes canon only, and the mirrors keep the old content until a sync.
   An `EDITED` conflict (exit 3) persists until the operator deletes the
   project copy and re-runs, or keeps the edit.
5. Use `--force` only for full reinitialization, and only with the operator's
   agreement. It re-copies the wheel's skills, rules, templates and chores
   over the project's copies, so operator edits to them are lost; it never
   overwrites personas and deletes nothing. It rewrites `.gzkit.json` from the
   detected structure, which drops hand-set keys such as a `vendors` block,
   custom paths, or an attestor handle not passed again. It appends another
   `project_init` event.
6. Report the mode, the listed writes, the exit code and any gate the output
   says is not installed.

## Cautions

- In gzkit's own repository the installed wheel is the editable
  `src/gzkit/`, a copy synced from `.gzkit/`. A `.gzkit/` edit not yet synced
  matches no shipped version, so `--update` reports it `EDITED` rather than
  reverting it; sync first.

## Validation

- Repair and update print each write; confirm the list matches the request.
- After a first init with the skeleton: `pyproject.toml`, `README.md`,
  `<source_root>/<package>/__init__.py` and `<tests_root>/__init__.py` exist.
- `uv run gz validate --surfaces` passes after init or a follow-up sync.

## Example

```bash
uv run gz init --mode heavy --attestor-handle <handle>   # first init
uv run gz init --dry-run        # initialized project: list the repair writes
uv run gz init                  # repair
uv run gz init --update --dry-run
uv run gz init --update         # then: uv run gz agent sync control-surfaces
```

## Related

- `gz-agent-sync` — the sync that init, repair and `--force` run, and that
  `--update` needs afterwards
- `uv run gz upgrade` — surface-only refresh with per-surface classifiers,
  `--surface` and `--force`
- `docs/user/manpages/init.md` — the full contract
