---
name: dayz-split-types
description: "Splits a monolithic DayZ types.xml into per-category files under db/types/ and registers them in cfgeconomycore.xml, backing up every changed file. Use when a mission's types.xml has grown too large to edit by hand or a server owner wants categorized economy files."
argument-hint: "<path-to-types.xml>"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-split-types

Take a monolithic `types.xml` and split it into categorized XML files under a `types/` subdirectory next to it, then point `cfgeconomycore.xml` (in the parent directory) at the non-empty ones and empty the original `types.xml`.

This skill wraps [DayZ-n-Chill/DayZ-TypeSplitterPro](https://github.com/DayZ-n-Chill/DayZ-TypeSplitterPro). The upstream `typeSplitter.py` is vendored under `vendor/`; this skill adds the CLI front-end (path argument, preflight gate, backups, the `<ce folder>` fix, emptying the original, result verification, automatic restore on failure).

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
python "<skill-dir>\split.py" <path-to-types.xml>
```

Typical:

```cmd
python "<skill-dir>\split.py" .server\chernarus\mission\db\types.xml
```

## What it does

1. Preflight gate.
2. Validate that `<types.xml>` exists, has at least one `<type>` entry, that `cfgeconomycore.xml` is one directory up (DayZ standard layout: `<mission>/cfgeconomycore.xml` + `<mission>/db/types.xml`), and that both files are writable.
3. Back up `types.xml`, `cfgeconomycore.xml` and any existing `types/` folder to `<name>.<YYYYMMDD-HHMMSS>.bak` beside them. Every run makes new backups, so reruns never replace an earlier one.
4. Copy the vendored `typeSplitter.py` next to `types.xml` (the upstream script finds `types.xml` through its own `__file__`), run it, then remove the temporary copy.
5. Fix `cfgeconomycore.xml`. The Central Economy reads a `<ce folder="...">` path relative to the mission root (unverified against the vanilla files: vanilla `P:\DZ\worlds\chernarusplus\ce\cfgeconomycore.xml:1-39` has no `<ce>` block at all; this follows the community `<ce>` convention), but upstream writes `folder="types"` while the files are in `db/types/`. The wrapper rewrites the attribute to `db/types` and copies back any other `<ce>` blocks from the backup, which upstream deletes.
6. Verify the result: `types/` exists, the category files hold exactly as many `<type>` entries as the original `types.xml`, every non-empty category file is listed under `<ce folder="db/types">`, and every listed file exists at `<mission>/<folder>/<name>`. The upstream script only logs its errors and always exits 0, so this check decides success. Fails if a category file is not listed; a listed file that does not exist (for example from a restored custom `<ce>` block) is a warning.
7. Replace `types.xml` with an empty `<types>` stub. The server always loads `db/types.xml`, so leaving the full file in place would load every type twice and edits to the split files would not be the only definition. The original is in this run's backup.
8. On any failure from step 4 on (the splitter exits non-zero, `types/` is missing, the entry count does not match, `cfgeconomycore.xml` is invalid or incomplete, `types.xml` cannot be emptied, or an unexpected error), copy `cfgeconomycore.xml` and `types.xml` back from this run's backups, delete the regenerated `types/` folder and put back the earlier one if there was one, then exit 1. The `.bak` files are kept. If the restore itself fails (a file is locked), it prints `[FAIL] Automatic restore failed` with the numbered copy and delete steps, naming each `.bak` path, to finish by hand.

## What gets created

- `<dir>/types/`, holding one file for each of the 19 categories: `ammo`, `armbands`, `ammo_boxes`, `animals`, `contamination`, `flags`, `staticObjs`, `vehicles`, `wrecks`, `zombies`, `seasonal`, `clothes`, `explosives`, `containers`, `food`, `tools`, `weapons`, `vehicleParts`, `uncategorized` (each `.xml`). Categories with no entries are still written as an empty `<types/>` file. Any existing `types/` folder is deleted and regenerated (after being backed up).
- `types.xml.<stamp>.bak`, `cfgeconomycore.xml.<stamp>.bak` and, if `types/` existed, `types.<stamp>.bak/`: backups from this run. Delete old ones when you no longer need them.
- `<mission>/cfgeconomycore.xml`: rewritten with one `<ce folder="db/types">` block listing each non-empty category file, followed by the `<ce>` blocks it had before. Upstream's formatter keeps only `<classes>` (its `<rootclass>` entries) and `<defaults>`; comments and any other element are dropped, so compare against the backup if you had hand edits.
- `<mission>/db/types.xml`: replaced with an empty `<types>` stub (see step 7). To split again, restore it from a `types.xml.<stamp>.bak` backup first.

## Refuses to run if

- `/dayz-preflight` returns non-zero (required by the Environment rule in `skills/_shared/dayz-conventions.md`).
- `<types.xml>` doesn't exist, isn't named `types.xml`, isn't valid XML, or has no `<type>` entries (already split).
- `cfgeconomycore.xml` isn't in the parent directory (the upstream tool requires that layout).
- `types.xml` or `cfgeconomycore.xml` is read-only (common for files copied from a server install). Clear it with `attrib -r <file>` and rerun. Nothing is backed up or changed.

## Output

```
[OK]    Backup: .server\chernarus\mission\db\types.xml.20261020-170428.bak
[OK]    Backup: .server\chernarus\mission\cfgeconomycore.xml.20261020-170428.bak
... (typeSplitter logging) ...

[OK]    Split into 14 non-empty category files in .server\chernarus\mission\db\types
        ammo.xml
        ammo_boxes.xml
        ... (more)
[OK]    Updated .server\chernarus\mission\cfgeconomycore.xml (<ce folder="db/types">)
[OK]    Emptied types.xml: its 2364 entries now load from db/types/ (original kept in types.xml.20261020-170428.bak)
```

On a failure after the splitter started, the last lines are the `[FAIL]` reason and:

```
[OK]    Restored cfgeconomycore.xml, types.xml and types/ from this run's backups, so the mission is as it was before the run.
```

## Attribution

The categorization logic and `cfgeconomycore.xml` formatting belong to [DayZ-n-Chill/DayZ-TypeSplitterPro](https://github.com/DayZ-n-Chill/DayZ-TypeSplitterPro). To update the vendored copy, fetch the latest upstream `typeSplitter.py` and replace `vendor/typeSplitter.py`, keeping its attribution header.

## Do not

- Don't modify the vendored `typeSplitter.py` to add features. Contribute upstream and re-vendor, so this skill stays a thin wrapper.
- Don't rely on the `.bak` files alone for a mission you care about. Commit the mission folder or copy it elsewhere first.
