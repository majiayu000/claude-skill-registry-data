---
name: sweep-drive
description: >
  Find orphaned items under ACE's Drive root and trash the ones you approve. Needs a live-set from
  sweep-live-set.
disable-model-invocation: false
---

# sweep-drive

Find Drive folders under `ACE/` that no current opp references, score them, present them to the human for triage, and trash approved items via `drive_trash_file` (reversible — 30-day Drive bin).

## Inputs

- Live-set file path/id from `sweep-live-set` skill output (a Drive path like `ACE/_sweep/<timestamp>/live-set.yaml`).
- `mode` — `recommend` (default) | `execute`. In `recommend` the skill is **report-only**: diff/score/render + return the recommended-action list; **no trashing**. In `execute` it trashes only `approvedIds`. The human-confirmation gate between the two is the orchestrator's job — see `agents/sweep.md § Human-confirmation gate`.
- `approvedIds` (`execute` mode only) — the exact folder ids the human approved in chat. Trash nothing outside this set.

## Products

- `ACE/_sweep/<timestamp>/drive-orphans.md` — human-readable triage report (markdown).
- `ACE/_sweep/<timestamp>/drive-orphans.yaml` — machine-readable `OrphanReport` (for replay / per-item approval).
- For each approved orphan: a Drive trash operation via `drive_trash_file`.
- For each approved open Google Form: a close via `forms_set_publish_settings` (before any trash).

## Process

1. **Read the live-set:** `drive_read_file` on the path produced by `sweep-live-set`. Parse it as YAML into a `LiveSet`.
2. **List `ACE/` children:** `drive_list_folder` on `ACE_DRIVE_ROOT_FOLDER_ID`. Filter to folders (mimeType `application/vnd.google-apps.folder`) and skip names starting with `_` (e.g. `_sweep/`).
3. **Diff (opp-shape is the authority, not the name):** for each folder whose name is NOT in `liveSet.oppSlugs`, **probe whether it is actually an opp folder** before treating it as a candidate. Use the same test the live-set scan uses — `isOppFolder(folderId, drive)` from `lib/doctor-drive-layout.ts` (true iff the folder contains `opp.yaml` or an `inputs/` subfolder). Record the result as `isOppShaped` on the `DriveFolderInfo`. A folder that is NOT opp-shaped (e.g. shared project folders like `documentation`, `templates`, `videos`, `labs-ai-videos`, `ai-input-creation-runs`, `rooftop-surveys`) is **not an orphaned opp** — the live-set only enumerates opp *slugs*, so a name-only diff would flag these every run. Pass `isOppShaped` through so the scorer can downgrade them to `low`.
4. **Score:** call `scoreDriveFolder(folder, liveSet, ACE_DRIVE_ROOT_FOLDER_ID)` from `lib/sweep-fingerprint.ts` for each candidate, with `folder.isOppShaped` populated from Step 3. The scorer returns `low` for shared/non-opp folders (safe-listed names + `isOppShaped === false`), `high` for confirmed opp folders not in the live-set, and falls back to name-shape heuristics only when `isOppShaped` is left undefined. Collect into an `Orphan[]`. Only `high`-confidence items (real orphaned opp folders) should be proposed for trashing.
5. **Build the `OrphanReport`** with `system: 'drive'`, `generatedAt: now ISO`, `liveSetGeneratedAt: liveSet.generatedAt`, totals, and orphans.
6. **Render the report** via `renderOrphanReport()` from `lib/sweep-report.ts`. `drive_create_file` to `ACE/_sweep/<timestamp>/drive-orphans.md`. Also serialize the YAML form to `drive-orphans.yaml` in the same folder.
7. **Recommend — stop here in `mode: recommend`.** Return the structured recommended-action list (only real orphaned opp folders — `high` confidence, opp-shaped but not in the live-set — each with id, name, confidence; reversibility: 30-day Drive bin) plus the report Drive link, to the orchestrator. **Trash nothing.** Do not try to prompt the human from this skill — a dispatched subagent can't reach them; the orchestrator runs the confirmation gate (see `agents/sweep.md § Human-confirmation gate`).

## Google Forms and `ACE/_scratch`

A run with `google_form` on (`solicitation-google-form`) leaves a **public** Google Form under its run folder. A public form keeps accepting submissions from anyone with the link until it is closed, and trashing the folder is not the same as closing it. So:

- **Open forms in closed or orphaned runs.** For every form (mimeType `application/vnd.google-apps.form`) under a recommended folder, or under a run whose `solicitation.google_form.status` is not `closed` while its solicitation is closed, recommend **closing** it: `forms_set_publish_settings({ formId, isPublished: true, isAcceptingResponses: false })`. The link keeps working and shows the form as closed (playbook/integrations/google-forms.md). Closing is reversible; it is still an approved action.
- **Close before trash.** In the execute pass, close every approved form first, then trash its folder.
- **`ACE/_scratch`** holds throwaway objects from live checks (Forms probes, PR5/PR5b). Step 2 skips `_`-prefixed folders as opp folders, so list `_scratch` on its own: recommend closing any form in it and trashing everything older than 24 hours.

## Execute phase (`mode: execute` only)

Runs only when the orchestrator re-dispatches with `mode: execute` + `approvedIds` (the folder, form and `_scratch` item ids the human approved in chat). Close each approved form first (above). Then, for each **approved** orphan, call `drive_trash_file` with `fileId: <id>`. Trash nothing outside `approvedIds`; return the per-item result. Then (sanity check) `drive_list_folder` `ACE/` again and confirm the trashed names are gone — this catches partial failures.

## Failure modes

- **Live-set path doesn't resolve:** abort with a clear "Run `sweep-live-set` first" message.
- **`drive_trash_file` fails on a Shared-Drive permission error:** report the item as "trash failed — needs admin"; don't retry, don't abort the rest of the batch.
- **An approved orphan was already deleted by something else between report and execution:** treat as success.

## Implementation notes for agents

- This skill must be invoked AFTER `sweep-live-set` in the same `/ace:sweep` run — the live-set is the safety boundary. If the live-set is more than 24 hours old, regenerate it first (active opps may have changed).
- All scoring is done locally via the `lib/sweep-fingerprint.ts` function; do not paraphrase the scoring rules into prompts.

## Related skills

- `sweep-live-set` produces the live-set this skill diffs against.
- Future: `sweep-connect`, `sweep-ocs`, `sweep-hq`, `sweep-labs` follow the same pattern for their respective systems.
