---
name: dayz-build-pbo
description: "Packs a mod from workspace/<ModName>/ into a binarized .pbo at P:\\Mods\\@<ModName>\\Addons\\ with DayZ Tools AddonBuilder. Use when a mod's source changed and you need a fresh PBO before /dayz-launch-test, or a clean rebuild to chase a stale-asset bug."
argument-hint: "<ModName> [--clean]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-build-pbo

Package a mod scaffold into a deployable `.pbo` under `P:\Mods\@<ModName>\Addons\`, where the engine loads it. Path discovery comes from `dayz-preflight/preflight.py`; the preflight gate, project cache and ownership-marker rules come from `skills/_shared/skill_helpers.py`.

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
python "<skill-dir>\build.py" <ModName> [--clean]
```

| Argument | Required? | Notes |
|---|---|---|
| `<ModName>` | yes | Must match a scaffold under `workspace/<ModName>/` in the project cached by `/dayz-init`, with the `P:\<ModName>\` junction in place. |
| `--clean` | no | Passes `-clear` to AddonBuilder, wiping `P:\Mods\@<ModName>\Addons\` before building. Use after large refactors or when chasing a stale-asset bug. Refused while `Addons\` holds any PBO other than `<ModName>.pbo` (payload copied in by `/dayz-deploy-pbo`) or any `.bisign` signature, since AddonBuilder makes neither and `-clear` would delete them. |

## What it does

1. **Project** - reads the project root cached by `/dayz-init`.
2. **Preflight gate** - runs `/dayz-preflight`; halts on non-zero, so an unmounted `P:\` is the first error shown.
3. **Workspace check** - `workspace/<ModName>/` exists and contains `config.cpp` and `$PBOPREFIX$`, and `$PBOPREFIX$` holds exactly `<ModName>` (surrounding whitespace and a BOM are ignored; case must match). The build always packs with `-prefix=<ModName>` through the `P:\<ModName>\` junction, so a different prefix means the mod's config paths expect another root; it refuses rather than build a PBO whose paths do not resolve. A payload-only bundle (prebuilt `Addons\*.pbo` and no `config.cpp`) has nothing to build, so it is refused with a pointer to `/dayz-deploy-pbo <ModName>`. This check runs before lint, so a missing file gets its own repair hint rather than a lint error.
4. **Lint gate** - runs `/dayz-lint <ModName>` and stops with `[FAIL]` and each `file:line` if it finds an error, since the mod would not load. Lint warnings print as `[WARN]` and the build goes on. The `P:\<ModName>\` link is left to step 6, which gives the repair hint.
5. **P:\Mods junction check** - `P:\Mods\` is a junction to the DayZ `!Workshop` folder.
6. **Mod junction check** - `P:\<ModName>\` is a link pointing at `workspace/<ModName>/` (created by `/dayz-new-mod` or `/dayz-import-mod`).
7. **Tools check** - resolves `AddonBuilder.exe` through `find_dayz_tools()` (env var, registry, Steam libraries).
8. **Ownership gate** - if `P:\Mods\@<ModName>\` already exists, it must contain `.agentic-z-scaffold` with content `<ModName>`. An unmarked folder could be a subscribed or hand-placed mod, so the build refuses to write into it or `-clear` it. This is the same rule `/dayz-deploy-pbo` uses.
9. **Clean gate** (`--clean` only) - refuses if `P:\Mods\@<ModName>\Addons\` holds any `.pbo` other than `<ModName>.pbo`, or any `.bisign`, and names each one. AddonBuilder makes neither, so `-clear` would delete deployed payload or a hand-made signature for good.
10. **Ownership marker** - when this run creates `P:\Mods\@<ModName>\`, it writes `.agentic-z-scaffold` there before AddonBuilder starts, so a failed first build leaves a marked folder that the next build accepts. The marker sits above `Addons\`, so `-clear` keeps it. `/dayz-clean-workspace` only removes deployed folders that carry it. If the marker cannot be written, the build prints `[FAIL]` and exits 1 without running AddonBuilder.
11. **Stage** - copies `workspace/<ModName>/` to `P:\temp\_stage\<ModName>\`, leaving out every file that matches `exclude.lst`, and prints how many files it copied and left out. A folder pattern such as `.git\*` drops every file in that folder, including files with no extension. Read-only files are staged read-only and still removed by the next build. If a file in the old stage or in the source cannot be removed or copied (a crashed AddonBuilder or Workbench still holds it), the build prints `[FAIL]` with that file's path and a hint (close the program, or `taskkill /im AddonBuilder.exe /f`) and exits 1.
12. **Build** - runs `AddonBuilder.exe P:\temp\_stage\<ModName> P:\Mods\@<ModName>\Addons -prefix=<ModName> -temp=P:\temp\<ModName> -include=<skill-dir>\include.lst [-clear]`. Binarization is on. There is no `-exclude=`: AddonBuilder 1.0.240639 crashes on it with `ArgumentNullException` in `TextureHeaderBinazrizeTask`, because it leaves its exclude-list path empty when the flag is given, so the stage step applies the list instead. The command is echoed as an `[AddonBuilder]` line with quoted arguments, so it can be pasted and re-run by hand.
13. **Verify output** - `P:\Mods\@<ModName>\Addons\<ModName>.pbo` exists and is newer than the build start. AddonBuilder can exit 0 while leaving an old PBO in place; that case fails as a stale PBO.
14. **Signature check** - AddonBuilder does not sign, so any `<ModName>.pbo.*.bisign` already in `Addons\` was made for an earlier PBO. Each one gets a `[WARN]`: re-sign the new PBO with `DayZ Tools\Bin\DsUtils\DSSignFile.exe`, or delete the old signature.
15. **Cleanup** - removes `P:\temp\<ModName>\` and the stage on success. On failure it keeps both and prints both paths for debugging.

## include.lst

`include.lst` (next to `build.py`) is passed to AddonBuilder as `-include=`. It is one line of `;`-separated wildcard patterns naming the file types AddonBuilder copies into the PBO: scripts, configs, layouts, models, textures, materials, sounds, and data files such as `.json`, `.xml`, `.csv` and `.txt`. A file whose extension is not listed is silently left out of the PBO. If your mod ships another file type, add its pattern to that line.

## exclude.lst

`exclude.lst` (next to `build.py`) is applied by `build.py` while it stages the mod: files matching its patterns (one per line, `;` starts a comment) are not copied, so they stay out of the final PBO. Each pattern matches the whole path relative to the mod root, ignoring case, and `*` crosses folders. It drops `.gui-sources\` (the sprite source PNGs for `/dayz-build-imageset`; only the packed atlas and `.imageset` under `gui/imagesets/` ship), the `workbench\` folder, Workbench plugins under `scripts\editor\`, version-control folders, binarization logs, archives, signatures and keys, and the `Source\`, `Doc\` and `Temp\` folders at the mod root. Those three are anchored to the root, so a nested folder with the same name (for example `scripts\4_World\Temp\` or `data\doc\`) still ships.

## Refuses to run if

- `<ModName>` fails the mod name pattern (a letter first, then letters, digits and underscores, at most 64 characters), so a name such as `..\Other` never reaches the disk. This check runs first.
- No project is cached (run `/dayz-init`).
- `/dayz-preflight` fails, or `P:\Mods\` is not a valid junction to `!Workshop`.
- `workspace/<ModName>/` is a payload-only bundle (prebuilt `Addons\*.pbo`, no `config.cpp`). There is nothing to build; deploy it with `/dayz-deploy-pbo <ModName>`.
- `workspace/<ModName>/`, its `config.cpp`, or its `$PBOPREFIX$` is missing (`/dayz-add-scaffold` adds the files).
- `$PBOPREFIX$` holds anything other than `<ModName>`. Set it to that single line, and make sure `config.cpp` paths use `<ModName>\` as their root.
- `P:\<ModName>\` is missing, is a real folder, or points somewhere other than `workspace/<ModName>/`. The hint points at `/dayz-add-scaffold <ModName> --piece junction`, which creates the link.
- `AddonBuilder.exe` is not found (set `DAYZ_TOOLS_PATH` or install DayZ Tools).
- `P:\Mods\@<ModName>\` exists without a matching ownership marker. If it is yours, remove it: `cmd /c rmdir /s /q P:\Mods\@<ModName>`.
- `--clean` is passed while `Addons\` holds PBOs other than `<ModName>.pbo`, or any `.bisign`.
- A file in `P:\temp\_stage\<ModName>\` or in the source cannot be removed or copied (locked by a crashed AddonBuilder or by Workbench).
- AddonBuilder exits non-zero (its exit code propagates), or produces no fresh PBO. The temp and stage dirs are kept for inspection, and both paths are printed.

## Output

```
DayZ preflight

[OK]    P:\ is mounted
...     (rest of the /dayz-preflight report)

Preflight complete.
[OK]    workspace\MyMod\ found
[OK]    $PBOPREFIX$ matches MyMod
[WARN]  lint config.cpp:9: requiredAddons lists DZ_Data twice in MyMod.
[OK]    /dayz-lint passed
[OK]    P:\Mods junction valid
[OK]    P:\MyMod junction valid
[OK]    AddonBuilder: C:\...\DayZ Tools\Bin\AddonBuilder\AddonBuilder.exe
[OK]    P:\Mods\@MyMod\ ownership marker valid

[OK]    Staged 9 files in P:\temp\_stage\MyMod (2 left out by exclude.lst)

[AddonBuilder] "C:\...\DayZ Tools\Bin\AddonBuilder\AddonBuilder.exe" P:\temp\_stage\MyMod P:\Mods\@MyMod\Addons -prefix=MyMod -temp=P:\temp\MyMod -include=...\include.lst

... AddonBuilder's own output, streamed live ...

[OK]    Built: P:\Mods\@MyMod\Addons\MyMod.pbo (12,345 bytes)
[OK]    Cleaned temp and stage dirs
```

The preflight gate runs first, then the workspace check, then the lint gate. Each `/dayz-lint` warning prints as a `[WARN]  lint` line and does not stop the build; any lint error stops it before the junction and tools checks. The ownership line appears only when `@MyMod` already exists. A `[WARN]` for each old `MyMod.pbo.*.bisign` follows the `Built:` line. If a temp or stage folder cannot be removed, a `[WARN]` names it and the `Cleaned` line is left out. Failures print `[FAIL]  <reason>` followed by an indented hint.

## Do not

- Don't write the PBO anywhere except `P:\Mods\@<ModName>\Addons\`; that is where the engine loads in-development mods.
- Don't create or repair the `P:\<ModName>\` junction here; `/dayz-new-mod` and `/dayz-import-mod` create it, and `/dayz-add-scaffold <ModName> --piece junction` repairs it.
