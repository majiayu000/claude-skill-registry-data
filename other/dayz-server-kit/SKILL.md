---
name: dayz-server-kit
description: "Zips what a server owner needs to run a DayZ mod: types.xml entries for every spawnable class, the cfgeconomycore.xml lines that load them, the load order and the public .bikey. Never packs a .biprivatekey. Use when a mod is released, alongside /dayz-release-pack."
argument-hint: "<ModName> [--mission <folder or instance>] [--deps CF ...] [--out <folder>] [--json] | --mod-dir <folder> [...]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-server-kit

A script gathers the files and writes one zip. It starts no process and needs no DayZ Tools. The AI only reads the warnings, for example which entries are placeholders, and decides whether to rerun with a mission or real values.

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
python "<skill-dir>\server_kit.py" <ModName> [options]
python "<skill-dir>\server_kit.py" --mod-dir <folder> [options]
```

| Argument | Notes |
|---|---|
| `<ModName>` | A mod under `workspace/<ModName>/` in the project cached by `/dayz-init`. |
| `--mod-dir` | Use any folder instead. Its name is the mod name unless `<ModName>` is given too. |
| `--mission` | A mission folder, or a test server instance name from `/dayz-add-server` (`chernarus` means `.server\chernarus\mission\`), to copy real types entries from. With `--mod-dir` the instance is looked up in the current folder, then in the project cached by `/dayz-init`. |
| `--deps` | Dependency mods in load order, with or without `@` (`--deps CF`). |
| `--out` | Output folder. Default `output\<ModName>-release\`, the same folder `/dayz-release-pack` writes to. |
| `--json` | Print the report as JSON. |

## What the zip holds

`<ModName>-server-kit.zip`:

| Member | What it is |
|---|---|
| `<ModName>_ce/types.xml` | A `<type>` entry for every spawnable class (scope 2 in `CfgVehicles`, `CfgWeapons` or `CfgMagazines`) in any `config.cpp` of the mod, the root one or a sub-folder one such as `data\config.cpp`. |
| `cfgeconomycore-lines.xml` | `<ce folder="<ModName>_ce">` with `<file name="types.xml" type="types" />`. The folder is relative to the mission folder, so the owner puts `<ModName>_ce\` next to `db\`. |
| `load-order.txt` | The `-mod=` order, dependencies first, and any non vanilla `requiredAddons`. |
| `keys/<name>.bikey` | Each public key from `Keys\` in the mod or `P:\Mods\@<ModName>\Keys\`. |
| `README.txt` | What each file is for, and which entries are placeholders. |

Types entries are taken in this order, first match wins:

1. Every `<type>` in the mod's own types files: any `*.xml` under the mod folder whose root is `<types>` (not under `Addons`, `Keys`, `output` or a dot folder such as `.git`, in any letter case). An `*.xml` that holds a `<types>` tag but does not parse stops the run, so a typo never swaps a real entry for a placeholder.
2. With `--mission`: the entries for the mod's classes in `db\types.xml` and in every `type="types"` file its `cfgeconomycore.xml` lists, so a mission split by `/dayz-split-types` works. The folder must hold at least one of `db\types.xml` and `cfgeconomycore.xml`, and every listed types file must exist, or the run stops (exit 2).
3. A placeholder for each class still missing: the vanilla element order with `nominal` and `min` at 0, so the item does not spawn until the owner tunes it. Each one carries a `placeholder values` comment.

## Keys

Only `.bikey` files are packed. A `.biprivatekey` lets anyone sign PBOs as the author, so the script never reads one into the zip and refuses to write a zip that would hold one. A private key found inside the mod folder raises the `private-key-in-mod` warning: move it out of the mod.

## Warnings and exit codes

Exit 0 means the zip was written. The report says when it replaced an existing `<ModName>-server-kit.zip`. It can carry `[WARN]` lines:

| Warning | What to do |
|---|---|
| `placeholder-types` | The listed classes have no types entry in the mod (or the `--mission`), so the kit holds placeholders that do not spawn. Rerun with `--mission`, add entries to the mod's types file, or tell server owners to tune them. |
| `types-unknown-class` | A `<type>` in the mod's own types files names no class in its `config.cpp`, usually a misspelt classname. Fix the name in the types file or `config.cpp` and rerun. |
| `deps-unmapped`, `scope-unknown`, `class-duplicate`, `no-bikey`, `private-key-in-mod` | As in `/dayz-release-pack`. |

Exit 2 means it could not run and no zip was written: bad arguments, no cached project, no mod folder, no `config.cpp`, a `config.cpp` that does not parse, a mod types file that does not parse, a `--mission` that is not a folder or an instance, a `--mission` folder with neither `db\types.xml` nor `cfgeconomycore.xml` (such as the instance folder `.server\chernarus\` instead of `.server\chernarus\mission\`; the message names the `mission` subfolder when there is one), a `type="types"` file that `cfgeconomycore.xml` lists but that is missing from disk, or a `--mission` whose `cfgeconomycore.xml`, `db\types.xml` or listed types file does not parse or has a root other than `<types>`. The `[FAIL]` line names the file and the error. A failed zip write leaves any previous kit in place.

## Do not

- Don't hand out a kit with placeholder entries without telling server owners to tune them.
- Don't copy a key into the zip by hand.
