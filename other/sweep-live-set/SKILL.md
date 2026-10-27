---
name: sweep-live-set
description: >
  List every identifier still referenced by visible ACE opps in Drive: the keep-list every orphan
  sweep diffs against.
disable-model-invocation: false
---

# sweep-live-set

Build the cross-opp live-set that every per-system `/ace:sweep` consumes. The live-set is the safety mechanism: anything in a target system NOT in the live-set is a candidate orphan. This skill produces it; per-system skills consume it.

## Inputs

- `ACE_DRIVE_ROOT_FOLDER_ID` from `.env` — the Drive folder that contains every opp directory.

## Products

- `ACE/_sweep/<YYYYMMDD-HHMMSS>/live-set.yaml` — the merged `LiveSet` (schema: `lib/sweep-types.ts:LiveSet`).
- Echoes the timestamped path so the caller (the sweep procedure doc) can pass it to per-system sweep skills.

## Process

1. **Compute the timestamp** for this sweep run: UTC `YYYYMMDD-HHMMSS`.
2. **Ensure `ACE/_sweep/<timestamp>/` exists** via `drive_create_folder` under `ACE_DRIVE_ROOT_FOLDER_ID`. If `_sweep/` does not yet exist as the parent, create it first.
3. **List opps:** call `drive_list_folder` on `ACE_DRIVE_ROOT_FOLDER_ID`. For each child folder, treat it as an opp if it contains an `opp.yaml` at the root OR an `inputs/` subfolder (matches `lib/doctor-drive-layout.ts:isOppFolder`). Skip `_sweep/` and any other reserved/leading-underscore folder.
4. **For each opp:**
   a. `drive_read_file` on `<opp>/opp.yaml` (if present; else empty string).
   b. `drive_list_folder` on `<opp>/runs/` (if present; else empty list).
   c. For each run folder, `drive_read_file` on `<opp>/runs/<run-id>/run_state.yaml` (skip if absent).
   d. Call `extractOppFragment(oppSlug, oppYaml, runStateYamls)` from `lib/sweep-live-set.ts` to get a fragment.
5. **Merge fragments:** call `mergeFragments(fragments, generatedAtIso)` to produce the final `LiveSet`.
6. **Serialize as YAML** and `drive_create_file` to `ACE/_sweep/<timestamp>/live-set.yaml`.
7. **Echo the Drive path and folder id** of the live-set file to the caller.

## Implementation notes for agents

- Use `npx tsx` to invoke a one-shot script that imports `lib/sweep-live-set.ts` if you need to run the merge from the terminal; or call the functions directly via the in-process TypeScript boundary if your harness allows it. Prefer one-shot script to keep the agent-side logic to MCP calls.
- The script lives at `scripts/sweep-live-set.ts` if/when an agent needs to execute it directly. (Not in scope for this PR — agents read YAMLs via MCP and call the lib functions inline.)
- If any opp folder is missing `opp.yaml`, that's a legacy/incomplete opp — still parse its runs but use `''` for the opp.yaml input; the fragment will simply omit `connectProgramIds`.

## Failure modes

- **No opps under `ACE/`** — produce an empty live-set; downstream sweeps will flag everything as an orphan candidate. That's intentional.
- **Malformed YAML in an opp's files** — `extractOppFragment` silently treats unparseable input as `{}`. Surface a warning in the agent's chat output for each opp where this happens, but don't abort.

## Related skills

- `sweep-drive` consumes this skill's output.
- Per-system sweep skills `sweep-connect`, `sweep-ocs`, `sweep-hq`, `sweep-labs` (added in PRs 2-5) will also consume it.
