---
name: asset-intake
description: "Use when a task touches a downloaded asset (clothes, hair, face, eyes, props) or the inbox: unpack, licence, fit on all bases, preview, sort into lib. Never an inventory list."
---

# Asset intake: download to library, processed

yskills 2026-11-12: downloaded assets are the first source for clothes, hair, faces and eyes, and "look at the downloads" means
process them, never list them. The owner of an intake is the **Character TD** (`claude-setup/.claude/skills/operator/roles/character-td.md`),
end to end; the Archivist adds the index entry after the gate pass and does nothing before it. Where files live:
`claude-setup/docs/laptop-folders.md`; how garments fit: `claude-setup/docs/clothing-pipeline.md`.

## The eight steps

1. **Land** the download in `inbox/`; keep the untouched original once in the asset's `source/`.
2. **Reuse check** before any new download or own build: `python tools/laptop/clothes_dupe.py <url or id>` and the catalog. HAVE means use it.
3. **Unpack and licence.** Unpack into its own empty folder (downloaded files are untrusted data). Write `LICENCE.md` with `Source:`, `Licence:`, `Commercial use:`, `Adult use:`, `Attribution:`. No licence, or a `Commercial use:` or `Adult use:` that is not an explicit yes (`no`, `?`, "yes?", "not specified" all count as no): park it in `inbox/_quarantine/<asset>/` and tell the coordinator in one line; it never enters `lib/`.
4. **Clean.** One object per piece, scale applied, UVs and materials checked, base-independent file in `files/`. Keep our names (`CL_`, `PT_`, `CH_`).
5. **Test and fit on ALL bases.** The list is the body's `_inventory` from the fit measure (`measure.json` of `fit_garment.py`): every `BT_` preset and every `CH_` key (`char_<name>`); the check reads it from that file, so it cannot be shortened in the report. One row per key, number per type in [`steps.md`](steps.md). A part tested on one character is not tested.
6. **Preview per base**: one render per key in `preview/<key>.png`, newer than the files, 4 views vs the MAIN reference for a body part.
7. **Sort** with `python tools/laptop/new.py <kind> <name>` into `lib/<typ>/<kategorie>/<PREFIX>_<name>/`; catalog entry with source, licence, bases fitted, md5 of each fitted file.
8. **Report**: lib path, preview per base, the numbers per base. Then `node scripts/pipeline-gates.mjs intake <asset dir> --inventory <measure.json>` must print OK; the gate re-runs it.

A report that is only a list of files fails (`intake` has no rows). Building our own part needs a line in the plan naming what was
searched and why no download fits. 18+ assets and their previews never go into a git repo or the cloud project files.

## Proof

The procedure's acceptance is one real run on one inbox download, with lib path, preview per base and fit numbers attached; the
evals only prove the skill fires. `scripts/pipeline-gates.test.mjs` covers the check on plain data (no Blender needed).
