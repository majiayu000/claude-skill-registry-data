---
name: dayz-edit-types
description: "Adds, updates or removes one <type> entry in a DayZ Central Economy types.xml (nominal, min, lifetime, restock, quantmin, quantmax, cost, category, usage, value, tag), or checks a pasted chunk of many <type> entries and merges them all, backing the file up first. Use when a mod item needs a spawn entry, a loot value needs tuning, an entry must be deleted, or the user pastes types.xml entries."
argument-hint: "<types.xml> (<ClassName> [--nominal N] [--min N] [--lifetime S] [...] | <ClassName> --remove | --merge <chunk|->) [--dry-run]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-edit-types

Edit a DayZ Central Economy `types.xml` file programmatically: add a new spawn entry, update an existing one, or remove one. When the edit changes the file, it is backed up to `types.xml.<YYYYMMDD-HHMMSS>.bak` first, and only the `<type>` blocks that changed are rewritten.

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
python "<skill-dir>\types_edit.py" <types.xml> <ClassName> [options] [--dry-run]
python "<skill-dir>\types_edit.py" <types.xml> <ClassName> --remove [--dry-run]
```

| Argument | Notes |
|---|---|
| `<types.xml>` | Path to the types.xml file. Typically `.server/<instance>/mission/db/types.xml`. |
| `<ClassName>` | The `name` attribute of the `<type>` block to upsert / remove. |
| `--remove` | Remove the entry instead of upserting. Other field flags ignored. |
| `--merge <chunk\|->` | Instead of a `<ClassName>`: check every `<type>` in a pasted chunk (a file, or `-` for stdin) and merge them all in one write. See Merge a pasted chunk below. |
| `--dry-run` | Works in every mode. Reports the change and the name warnings, then writes nothing (no backup either). Use it to preview an edit before it touches the file. |
| `--nominal N` | Target spawn count. Default for new entries: 1. |
| `--min N` | Minimum spawn count. Default for new entries: 0. |
| `--lifetime S` | Despawn timeout in seconds. Default for new entries: 14400 (4 hours, the usual vanilla loot lifetime; storage items such as barrels use 3888000). |
| `--restock S` | Restock interval in seconds. Default for new entries: 0. |
| `--cost N` | Spawn cost / weight. Default for new entries: 100. |
| `--quantmin N` | Lowest spawn quantity in percent, for a quantity item (magazine, bottle, battery): `-1` (not a quantity item) or 0 to 100. Default for new entries: -1. Vanilla example: AKM has `<quantmin>30</quantmin>` (`P:\DZ\worlds\chernarusplus\ce\db\types.xml:129`). |
| `--quantmax N` | Highest spawn quantity in percent: `-1` or 0 to 100. Default for new entries: -1 (AKM: 80, same file line 130). Pass both `--quantmin` and `--quantmax` when turning an entry into a quantity item or back: every vanilla entry has both at -1 or both set (all 2382, 2391 and 2404 entries in the chernarusplus, enoch and sakhal `types.xml`). An edit that leaves exactly one of them at -1 prints `[WARN] <ClassName>: quantmin is 50 but quantmax is -1; ...` and still goes ahead. |
| `--category CAT` | Sets `<category name="CAT"/>`. Single value (replaces any existing). |
| `--usage TAG` | Set the entry's usages to exactly the `<usage name="TAG"/>` tags given. Repeatable. Every usage not passed is removed, so to add one, pass the existing usages too. The change line names what was removed. |
| `--value TAG` | Set the entry's values to exactly the `<value name="TAG"/>` tags given. Repeatable. Every value not passed is removed. |
| `--tag TAG` | Set the entry's tags to exactly the `<tag name="TAG"/>` tags given. Repeatable. Every tag not passed is removed. |

## What it does

1. Preflight gate.
2. Read and parse `<types.xml>` (comments are kept). Locate the `<type name="<ClassName>">` block. Names match ignoring case, because DayZ class names are case-insensitive: vanilla `P:\DZ\worlds\chernarusplus\ce\db\types.xml:3036` lists `Bandana_Blackpattern` for the config class `Bandana_BlackPattern` (`P:\DZ\characters\headgear\config.cpp:3084`). So `akm` updates or removes the existing `AKM` block instead of adding a second one, and the file keeps its own spelling.
3. Upsert mode (default):
   - If the block exists, update only the fields passed. Untouched fields stay as-is.
   - If the block doesn't exist, create one. Fields not passed get the defaults above, plus the vanilla standard flags (`count_in_map=1`, everything else 0). Children are written in vanilla order: `nominal`, `lifetime`, `restock`, `min`, `quantmin`, `quantmax`, `cost`, `flags`, then `category`, `tag`, `usage`, `value`. An edit that adds a name puts it in the same place among the existing children.
4. Remove mode (`--remove`): delete the block.
5. Name check (upsert mode): the entry's `<category>`, `<usage>`, `<value>` and `<tag>` names are checked against the mission's `cfglimitsdefinition.xml`, found next to `db/` (`<types.xml>\..\..\`). A `user=` group is checked against `cfglimitsdefinitionuser.xml` when it exists; without that file `user=` groups are not checked. Each name the file does not define prints `[WARN] usage name "Militar" is not defined in cfglimitsdefinition.xml`, because the Central Economy ignores or rejects it. The edit still goes ahead. When `cfglimitsdefinition.xml` is not there (a types file kept in a mod folder), the check is skipped with a note.
6. If nothing changed (entry already matches, or the entry to remove is absent), or `--dry-run` was passed, stop: no backup, no write.
7. Otherwise copy the file to `<types.xml>.<YYYYMMDD-HHMMSS>.bak` (a new backup every run; a `-2`, `-3` counter is added within the same second) and write back only the `<type>` blocks that changed. If the file cannot be written (read-only, open in another program, disk full), the run stops with `[FAIL] Could not write <types.xml>: <reason>` and exit 1. When the file is still unchanged, the backup this run made is removed; when the write got partway, the backup is kept and the message names it so you can restore from it.

## Merge a pasted chunk

When the user pastes `types.xml` entries, save the text to a file (or pipe it on stdin with `-`) and merge it:

```cmd
python "<skill-dir>\types_edit.py" <types.xml> --merge <chunk.xml> [--dry-run]
python "<skill-dir>\types_edit.py" <types.xml> --merge - < chunk.xml
```

The chunk can be bare `<type>` blocks or a whole `<types>` file, with or without the XML declaration, saved or piped as UTF-8 (a chunk that is not UTF-8 stops with `[FAIL] The chunk from <chunk> is not UTF-8 ...` and the file unchanged). Every entry is checked before anything is written. These are errors, and any one of them stops the whole merge with the file unchanged:

- a `<type>` without a name, or a name listed twice in the chunk (in any case)
- a count, lifetime, restock or cost that is not a whole number or is negative
- `min` greater than `nominal`
- `quantmin` or `quantmax` outside -1 and 0 to 100, or `quantmin` greater than `quantmax`
- a `<flags>` value other than 0 or 1
- a `<category>`, `<usage>`, `<value>` or `<tag>` without a name
- a name the target file already lists twice (in any case)

A missing standard child (`nominal`, `lifetime`, `restock`, `min`, `quantmin`, `quantmax`, `cost`, `flags`), an unknown element, an unknown flag, or exactly one of `quantmin` and `quantmax` at -1 is a `[WARN]` and does not stop the merge. So is a category, usage, value or tag name that the mission's `cfglimitsdefinition.xml` does not define (the same name check as upsert mode, skipped with a note when that file is absent).

Then each entry is merged: a new name is added at the end, a name already in the file (matched ignoring case) has its whole block replaced where it stands under the file's spelling of the name, and an identical block is left alone. The file is backed up to `types.xml.<YYYYMMDD-HHMMSS>.bak` once and written once. `--dry-run` checks and reports the same lines and writes nothing.

```
[OK]    Checked 2 <type> entries
[OK]    Added <type name="MyMod_Vest">
[OK]    Replaced <type name="AKM">: nominal 10 -> 12, min 5 -> 6
[OK]    Backup: .server\chernarus\mission\db\types.xml.20261024-153012.bak
[OK]    Wrote .server\chernarus\mission\db\types.xml
```

Formatting: only the `<type>` blocks that changed are rewritten. Every other byte stays as it was: the XML declaration, comments inside and outside `<types>`, blank lines, line endings (LF or CRLF) and every untouched block. A one-field edit of a vanilla `types.xml` is a one-line diff. A rewritten or added block uses the file's own indentation and writes self-closing tags as vanilla does (`<category name="weapons"/>`, no space before `/>`). The file is written in the encoding its XML declaration names (UTF-8 when it names none), so an `ISO-8859-1` file stays `ISO-8859-1`; a new name that encoding cannot hold is written as a character reference such as `&#228;`. A file that cannot be patched block by block (an empty `<types/>`, or bytes that are not valid in the declared encoding) is written whole, re-indented with 4 spaces, keeping its XML declaration and encoding.

## Refuses to run if

- `/dayz-preflight` returns non-zero.
- Neither `<ClassName>` nor `--merge` is given, or both are (argparse usage error, exit 2).
- `<types.xml>` doesn't exist.
- `<types.xml>` isn't valid XML.
- The root element is not `<types>` (for example `events.xml` or `globals.xml` passed by mistake).
- `<ClassName>` appears in more than one `<type>` block, in any case (`AKM` and `akm` count as the same name); merge them by hand first. Duplicates of other names only print a `[WARN]` listing them.
- `--nominal`, `--min`, `--lifetime`, `--restock` or `--cost` is negative, or `--quantmin` / `--quantmax` is not -1 or 0 to 100 (argparse usage error, exit 2).
- `<ClassName>`, `--category`, `--usage`, `--value` or `--tag` is empty or only whitespace (argparse usage error, exit 2), the same names merge mode rejects.
- The backup cannot be made, or `<types.xml>` cannot be written (exit 1, see step 7).
- `--min` or `--nominal` would leave the entry with `min` greater than `nominal` (checked against the entry's existing or default value for the flag you did not pass). The file is left unchanged.
- `--quantmin` or `--quantmax` would leave the entry with `quantmin` greater than `quantmax` (both set, neither -1; checked the same way). The file is left unchanged.

## Output

Add a new entry:

```
[OK]    Added <type name="MyMod_Vest"> nominal=1, min=0, lifetime=14400, cost=100
[OK]    Backup: .server\chernarus\mission\db\types.xml.20261024-153012.bak
[OK]    Wrote .server\chernarus\mission\db\types.xml
```

Update an existing entry:

```
[OK]    Updated <type name="MyMod_Vest">: nominal 1 -> 5, lifetime 14400 -> 28800
[OK]    Backup: .server\chernarus\mission\db\types.xml.20261024-153012.bak
[OK]    Wrote .server\chernarus\mission\db\types.xml
```

Set the usages (the old one is named as removed):

```
[OK]    Updated <type name="AKM">: usage [Military] -> [Police] (removed Military)
[OK]    Backup: .server\chernarus\mission\db\types.xml.20261024-153012.bak
[OK]    Wrote .server\chernarus\mission\db\types.xml
```

Nothing to do:

```
[OK]    <type name="MyMod_Vest"> already matches; no change
```

## Do not

- Don't edit `<flags>` granular attributes (`count_in_cargo`, etc.) in single-entry mode; there is no option for them. Paste the whole block with the flags you want and use `--merge`.
- Don't let backups pile up unchecked: every changing run adds a `types.xml.<stamp>.bak`. Delete old ones when you no longer need them, and commit the mission folder for real history.
