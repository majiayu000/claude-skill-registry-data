---
name: sweep-opp-runs
description: >
  Prune old ACE runs in Drive: keep the newest N per opp and trash the rest after approval.
disable-model-invocation: false
---

# sweep-opp-runs

Per-opp **retention prune**, not orphan sweep. For every opp folder under `ACE/`, sort its `runs/<run-id>/` children by createdTime descending, keep the newest `N`, propose the rest as trash candidates. Human approves, atom executes via `drive_trash_file` (reversible — 30-day Drive bin).

This is purely about retention to control `/ace:status` and other listing load times. It does **not** consult the live-set; orphan opp folders are sweep-drive's job. opp-runs assumes every opp under `ACE/` is legitimate and only trims its run history.

## Inputs

- `keep` (required, int ≥ 1) — the number of newest runs to retain per opp. Sweep orchestrator surfaces this from the user; default is `3` if the user accepts the prompt without changing it.
- `sweepFolder` — the timestamped sweep folder built by the orchestrator (e.g. `ACE/_sweep/<timestamp>/`); products land here.
- `mode` — `recommend` (default) | `execute`. In `recommend` the skill is **report-only**: build + render the per-opp prune plan + return it; **no trashing**. In `execute` it trashes only `approvedIds`. The human-confirmation gate between the two is the orchestrator's job — see `agents/sweep.md § Human-confirmation gate`.
- `approvedIds` (`execute` mode only) — the exact run-folder ids the human approved in chat. Trash nothing outside this set.

There is no live-set dependency. If the orchestrator built one (because the user ran a different system first in the same `/ace:sweep all`-style invocation), ignore it.

## Products

- `ACE/_sweep/<timestamp>/opp-runs-prune.md` — human-readable plan grouped by opp.
- `ACE/_sweep/<timestamp>/opp-runs-prune.yaml` — machine-readable per-opp plan (for replay / partial approval).
- For each approved run folder: a `drive_trash_file` op.

## Process

1. **Enumerate opps.** `drive_list_folder` on `ACE_DRIVE_ROOT_FOLDER_ID`. Filter to folders only (`mimeType == application/vnd.google-apps.folder`). Skip names starting with `_` (e.g. `_sweep/`, `_archive/`, `ai-input-creation-runs/` is NOT a sweep target — it doesn't start with `_`, but it's also not an opp; the runs-folder probe in step 3 naturally skips it).
2. **Locate `runs/` per opp.** For each opp folder, `drive_list_folder` on the opp folder; find the child named exactly `runs` (folder mimeType). If none exists, skip the opp (nothing to prune).
3. **List runs.** `drive_list_folder` on the `runs/` folder. Filter to folders. These are individual run dirs (typically `YYYYMMDD-HHMMSS-<short>` or similar; do not parse the name — sort by `createdTime` from the Drive metadata, not the slug).
4. **Sort + slice.** Sort runs by `createdTime` descending (newest first). The first `keep` runs are retained. The remainder are prune candidates.
5. **Build the per-opp plan.** For each opp with >0 candidates, collect:
   - `oppSlug` — the opp folder name
   - `kept[]` — the `keep` newest runs (`id`, `name`, `createdTime`)
   - `candidates[]` — the runs to trash (`id`, `name`, `createdTime`)
6. **Render the markdown report.** Per-opp section with two short tables (kept vs candidates). Headline at the top: "Prune plan — keep newest N per opp; M opps affected; K runs to trash." Write to `ACE/_sweep/<timestamp>/opp-runs-prune.md` and the YAML peer.
7. **Recommend — stop here in `mode: recommend`.** Return the per-opp prune plan (candidates to trash, grouped by opp — each with id, name, createdTime; reversibility: 30-day Drive bin) + the report Drive link, to the orchestrator. **Trash nothing.** Do not try to prompt the human from this skill — a dispatched subagent can't reach them; the orchestrator runs the confirmation gate (see `agents/sweep.md § Human-confirmation gate`).

## Execute phase (`mode: execute` only)

Runs only when the orchestrator re-dispatches with `mode: execute` + `approvedIds` (the run-folder ids the human approved in chat). For each **approved** candidate, `drive_trash_file({ fileId: <id> })`. Trash nothing outside `approvedIds`. Report success/failure per-item, but never abort the batch on a single-item failure — log and continue. Then (sanity check) for one affected opp, `drive_list_folder` on its `runs/` again and confirm the trashed names are gone.

## Failure modes

- **`runs/` folder doesn't exist on a given opp** — skip silently. Opps that never ran a `/ace:run` have no `runs/`.
- **`keep` >= run count for an opp** — that opp has zero candidates; omit it from the report.
- **`drive_trash_file` permission error on a Shared-Drive folder** — log as "trash failed — needs admin"; continue.
- **`keep == 0`** — refuse. Retention prune always keeps at least 1 (the freshest run). Surface a clear error to the orchestrator; do not silently fall back.

## Implementation notes for agents

- Use the Drive `createdTime` field — do not parse run-id slugs for timestamps. Run-id slug format has drifted historically; the metadata is authoritative.
- This skill does **not** touch `opp.yaml`, `inputs/`, `eval-calibration/`, or any other per-opp file. Only `runs/<run-id>/` direct children get trashed.
- Run folders are deeply nested (per-phase verdicts, transcripts, screenshots). `drive_trash_file` on the run folder cascades naturally — no need to recurse.
- Drive trash is reversible for 30 days. If the human asks "what if I want it back," point them at https://drive.google.com/drive/trash and the run-id slug.

## Related skills

- `sweep-drive` handles orphan **opp** folders (the level above this skill's targets). The two are complementary: `opp-runs` controls retention inside live opps; `sweep-drive` removes opps that no longer match the live-set.
- `sweep-live-set` is **not** an input here.
