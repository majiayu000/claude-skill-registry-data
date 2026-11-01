---
name: dayz-release-pack
description: "Writes the release texts for a DayZ mod in one go: the Steam Workshop description, a changelog entry from the mod's git history, the classname list from config.cpp and the server owner install notes. Every fact comes from the mod's files; anything the script cannot know is a warning to settle. Use when a mod is ready to publish or update on the Workshop."
argument-hint: "<ModName> [--version 1.2.0] [--since <git ref>] [--deps CF ...] [--out <folder>] [--json] | --mod-dir <folder> [...]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-release-pack

A script reads the mod and writes four files. It starts no process except `git`, needs no DayZ Tools and takes about a second. It does not gate on `/dayz-preflight`, because it reads only the mod folder and, when it exists, `P:\Mods\@<ModName>\Keys\` for the public key. The AI only reads the warnings, settles them and rereads the texts before they are published.

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
python "<skill-dir>\release_pack.py" <ModName> [options]
python "<skill-dir>\release_pack.py" --mod-dir <folder> [options]
```

| Argument | Notes |
|---|---|
| `<ModName>` | A mod under `workspace/<ModName>/` in the project cached by `/dayz-init`. |
| `--mod-dir` | Use any folder instead. Its name is the mod name unless `<ModName>` is given too. |
| `--version` | The version for the changelog heading and the Workshop text. Default `Unreleased`. |
| `--since` | Git ref the changelog starts after. Default: the latest tag when the mod folder is its own repository, and the script prints which one. When that tag is this release (it sits on HEAD, or it is `--version` or `v<version>`, as when you tag before writing the notes), the entry starts after the tag before it, and the script says so; with no tag the entry lists the whole history and warns `changelog-full-history`. Inside a bigger repository (an Agentic-Z clone) it is the newest `chore(release)` commit that touched the mod folder, and the script prints which one. With no such commit the entry lists the folder's whole history and warns `changelog-full-history`. |
| `--deps` | Dependency mods in load order, with or without `@` (`--deps CF COT`, or `--deps CF --deps COT`). Map each non vanilla `requiredAddons` entry to the Workshop mod that ships it. It takes every name after it, so give `<ModName>` first: `--deps CF MyVest` with no `<ModName>` before it is refused, and so is a `--deps` list that names the mod itself. |
| `--out` | Output folder. Default `output\<ModName>-release\` in the project, or in this repository with `--mod-dir` (never the current folder). A folder inside the mod folder is refused, because AddonBuilder would pack it and git would commit it with the source. |
| `--json` | Print the report as JSON. |

## What it writes

| File | Built from |
|---|---|
| `workshop-description.txt` | Steam BBCode: the title and summary from `mod.cpp` (`name`, `overview`) or the first paragraph of `README.md`, the spawnable items, the requirements, a server owner line with a `SERVER_KIT_LINK` placeholder for where the server kit is published, and the changes players see: every heading of the changelog except `Internal`, with breaking changes first and marked **Breaking:**. Any text from the mod or its commits that holds `[` or `]` is wrapped in `[noparse]` so Steam shows it as typed instead of reading it as a tag. |
| `changelog.md` | One entry: `## <version> (<date>)` from the commits that touched the mod folder, under `Breaking changes` (a `!` after the type, such as `feat!:`, or a `BREAKING CHANGE:` footer), `Added` (`feat:`), `Fixed` (`fix:`), `Internal` (`docs:`, `test:`, `ci:`, `build:`, `style:`, `refactor:`, `chore:`) and `Changed` (everything else). Merges and `chore(release)` commits are left out. |
| `classnames.md` | Every class in `CfgVehicles`, `CfgWeapons` and `CfgMagazines` whose scope is 2, with section, parent, display name and the config file it is in. Every `config.cpp` under the mod is read: the root one and sub-folders such as `data\config.cpp`, but not `Addons\`, `Keys\` or dot folders such as `.git\`. Scope is followed through parents in any of those files, and `public`, `protected` and `private` count as 2, 1 and 0. `requiredAddons` from all of them are merged, less the mod's own `CfgPatches` classes. |
| `server-install.md` | Copy the `@mod`, copy the `.bikey` into `keys\`, the `-mod=` load order, the types files from `/dayz-server-kit`, restart. |

It also writes `.release-pack.json`, the hash of each text it wrote, so a rerun can tell your hand edits from its own output. Leave it in the folder.

The docs writer merges `changelog.md` into `workspace/<ModName>/CHANGELOG.md` and the classnames into the README.

## Warnings

The script exits 0 with `[WARN]` lines when something needs a person or the AI:

| Warning | What to do |
|---|---|
| `summary-missing` | Neither `mod.cpp` nor `README.md` has a summary, so the Workshop text holds a placeholder line. Write one sentence there. |
| `deps-unmapped` | Printed whenever `requiredAddons` lists addons that are not vanilla, because the script cannot know which Workshop mod ships which addon. Without `--deps`: find the Workshop mod that ships each and rerun with `--deps`. With `--deps`: check that every listed addon is shipped by one of the named mods (CF ships `JM_CF_Scripts`, for example), and rerun with any missing mod added. The warning is settled once that check is done. |
| `scope-unknown` | A class sets no scope and takes it from a parent outside the mod (listed in `classnames.md` under "Scope not set"). Set an explicit scope in `config.cpp` for each listed class (`scope = 2` for spawnable items, otherwise 0 or 1) and rerun. |
| `class-duplicate` | A class is defined in more than one of the mod's `config.cpp` files. The texts use the first definition (the root file first, then by path). Keep each class in one file and rerun. |
| `server-kit-link` | Always printed. The Workshop text links the server kit as `SERVER_KIT_LINK`, because the script cannot know where you publish it. Replace it with the kit's address (for example a GitHub release), or delete that sentence if you do not publish the kit. |
| `no-bikey` | No `.bikey` in `Keys\` or `P:\Mods\@<ModName>\Keys\`. Sign the PBO before release. When `P:\` is not mounted the warning says so instead, because the deployed key could not be checked: mount it with `/dayz-workdrive` and rerun first. |
| `private-key-in-mod` | A `.biprivatekey` sits inside the mod folder. It is never written anywhere, but move it out of the mod so it can never ship. |
| `no-git` | The changelog entry is empty because git is not installed or not on `PATH` (install Git and rerun), or because the mod folder is not in a git repository. The warning says which. Write the changes by hand, or fix the cause and rerun. |
| `changelog-full-history` | No start ref was found, so the entry lists every change the mod ever had. When the only tag is this release, there is nothing earlier to start from; pass `--since <ref>` to limit the entry. When the mod folder is its own repository with no tag: tag the release (`git tag v<version>`) so the next run starts after it, or pass `--since <ref>`. Inside a bigger repository, no `chore(release)` commit touched its folder: rerun with `--since <ref>` to limit the entry, or commit the release as `chore(release): <version>` so the next run starts after it. |
| `kept-backup` | A file in the output folder was edited after the last run wrote it (for example the `SERVER_KIT_LINK` address or the summary line), so the script copied it to `<file>.bak` (then `<file>.2.bak`, never replacing an older backup) before writing the new text. A file the last run wrote and nobody edited is replaced without a backup, even when the date, classes or commits changed. Copy the edits you still want into the new file, then delete the backups. |
| `changelog-empty` | No commits touched the mod folder since the start ref, so the entry lists no changes. Commit the changes first, or pass an earlier `--since`. |

Exit 2 means it could not run: bad arguments (including a `--deps` list that took in `<ModName>` or names the mod itself), no cached project, no mod folder, no `config.cpp` anywhere under the mod, any `config.cpp` that does not parse (run `/dayz-lint`), a `--since` ref that is not in the history, or an output folder inside the mod folder. The `[FAIL]` line goes to stderr; with `--json` the error is a JSON object on stdout.

## Then

Run `/dayz-server-kit <ModName>` to zip the types entries, the `cfgeconomycore.xml` lines, the load order and the public key for server owners. It writes to the same release folder.

## Do not

- Don't publish the Workshop text with a placeholder line or a `[WARN]` still open (settle each one as the table says).
- Don't type classnames or dependencies by hand into the texts; fix the mod and rerun.
