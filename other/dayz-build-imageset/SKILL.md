---
name: dayz-build-imageset
description: "Packs PNG sprites from a mod's .gui-sources/<setname>/ folders into a DayZ .imageset definition and .paa atlas under gui/imagesets/. Use when a mod's HUD or menu icons need to become an imageset that .layout files can reference."
argument-hint: "<ModName> | <mod-root> [--mod-name <name>] [--dry-run] [--prune]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-build-imageset

Pack a folder of PNG sprites into a DayZ imageset (atlas + `.imageset` definition file). Source images stay in `.gui-sources/`, which `/dayz-build-pbo` leaves out of the PBO (its `exclude.lst` drops `.gui-sources\`); only the packed `.paa` atlas and `.imageset` file land under `gui/imagesets/` where the engine expects them.

Layout convention:

```
<mod-root>/
  .gui-sources/
    my_icons/
      hud_health.png
      hud_stamina.png
      hud_thirst.png
    main_menu/
      ...
  gui/
    imagesets/
      my_icons.imageset      <- generated
      my_icons.paa           <- generated
      main_menu.imageset
      main_menu.paa
```

Follow `skills/_shared/dayz-conventions.md`.

## Requirements

Pillow composes the atlas. If it is missing the script exits 1 with an install hint:

```cmd
py -m pip install -r "<skill-dir>\requirements.txt"
```

## How to run

```cmd
python "<skill-dir>\build_imageset.py" <ModName> [--mod-name <name>] [--dry-run] [--prune]
python "<skill-dir>\build_imageset.py" <mod-root> [--mod-name <name>] [--dry-run] [--prune]
```

| Argument | Required? | Notes |
|---|---|---|
| `<ModName>` | one of the two | Resolves to `workspace/<ModName>/` in the project cached by `/dayz-init`, like the other `/dayz-*` skills, so it works from the repo root. |
| `<mod-root>` | one of the two | A path to a folder containing `.gui-sources/`. Any argument with a slash, backslash or drive letter, or `.` / `..`, is read as a path (use `.\MyMod` for a folder in the current directory). |
| `--mod-name <name>` | no | Root used in the `path` field of the `.imageset` (`<name>\gui\imagesets\<setname>.paa`). Defaults to the mod's `$PBOPREFIX$`, because in-PBO paths are rooted at the PBO prefix (vanilla `P:\DZ\gui.txt:1` has `prefix=gui\`, and `P:\gui\imagesets\playstation_buttons2.imageset:7` references `Gui/imagesets/...`). With no `$PBOPREFIX$` it falls back to the folder name with a `[WARN]`. |
| `--dry-run` | no | Packs in memory and prints, per set, the atlases it would write and the stale outputs it would delete (`Would remove stale ...`). Writes, converts and deletes nothing. Still needs preflight, Pillow and `ImageToPAA.exe`. With `--prune` it also lists the orphans it would delete (`Would remove orphan ...`). |
| `--prune` | no | Deletes orphan outputs: generated files in `gui/imagesets/` whose `.gui-sources/<set>/` folder no longer exists (step 5). Without it they are only reported with a `[WARN]`. Preview with `--dry-run --prune`. |

## What it does

1. Preflight gate (DayZ Tools needed for `ImageToPAA.exe`), before any other check.
2. Check that Pillow is installed and that `<mod-root>/.gui-sources/` exists with at least one subfolder.
3. Resolve `ImageToPAA.exe` from DayZ Tools.
4. For each subfolder of `<mod-root>/.gui-sources/` (folders whose name starts with a dot, such as `.git`, are skipped):
   - The folder name becomes the imageset `Name`, which `.layout` files reference as one token (`image0 "set:dayz_gui image:Close"` at `P:\gui\layouts\day_z_book.layout:141`). A folder name that is not an identifier (for example `main menu` or `main-menu`) fails that set with a `[FAIL]` asking you to rename the folder; the other sets still build.
   - Collect all `.png` files in that subfolder. Each file becomes one named sprite (the file's stem becomes the `ImageSetDefClass` name). A stem that is not an identifier (letters, digits and underscores, not starting with a digit; so no spaces or hyphens) fails that set with a `[FAIL]` naming the files to rename. A `.png` that Pillow cannot read (corrupt, truncated or 0 bytes) fails that set with a `[FAIL]` naming the file; the other sets still build. A subfolder with no `.png` files is skipped with a `[WARN]`, and its outputs from an earlier run are deleted.
   - Sort sprites by height descending and shelf-pack into the smallest power-of-two atlas that fits (each dimension picked from 256 / 512 / 1024 / 2048 / 4096; rectangular atlases allowed; ordered by area, square preferred at equal area), with a 10px gutter on all sides of every sprite.
   - If everything fits in one atlas: emit `<setname>.{paa,imageset}`.
   - If sprites won't fit in a single 4096x4096 atlas: split, next-fit in height order (a new atlas starts when the current one overflows), into multiple atlases and emit `<setname>_1.{paa,imageset}`, `<setname>_2.{paa,imageset}`, etc. Each part is its own self-contained imageset.
   - If a split would write `<setname>_N` and another source set is also named `<setname>_N` (compared ignoring case, as Windows file names are), that set fails with a `[FAIL]` before anything is converted, because the two would overwrite each other's files.
   - Compose each atlas as PNG via Pillow and convert it to `.paa` via `ImageToPAA.exe` into a temporary `.staging-*` folder inside `gui/imagesets/`, never onto the final file. The atlas fails if ImageToPAA exits non-zero or leaves no `.paa` in the staging folder.
   - Only when every atlas of the set converted are the staged `.paa` and `.imageset` files moved over the final files. If any atlas failed, no final file is replaced or deleted, so the earlier good outputs stay. The staging folder is removed either way.
   - After that move, delete this set's outputs from an earlier run that this run did not rewrite (`<setname>.*` after a split, extra `<setname>_N.*` when the part count drops). Names are compared ignoring case, so after renaming the folder `Icons` to `icons` the old `Icons_2.*` goes too. Stems matching another source set's name are left alone.
   - Each `.imageset`'s `path` references its own `.paa` via `<mod-name>\gui\imagesets\<stem>.paa`.
5. Look for orphans: `.imageset` files in `gui/imagesets/` whose stem is neither a current set name nor `<set>_N` of one (ignoring case), left behind when a set folder was deleted or renamed. `/dayz-build-pbo` would keep packing their sprites. Only files this skill wrote count: the `.imageset` must start with `ImageSetClass {`, carry `Name "<stem>"` and point at `...\gui\imagesets\<stem>.paa`, so hand-made or vanilla-style imagesets (which use `Gui/imagesets/....edds`, as at `P:\gui\imagesets\playstation_buttons2.imageset:7`) are never touched. Each orphan `.imageset` and its `<stem>.paa` are reported with a `[WARN]`, or deleted with `--prune`. This also runs when `.gui-sources/` has no set folders left, before that run fails.
6. Report a summary; exit non-zero if any imageset failed. Orphans alone do not change the exit code.

## Generated `.imageset` format

```
ImageSetClass {
 Name "my_icons"
 RefSize 512 512
 Textures {
  ImageSetTextureClass {
   mpix 0
   path "MyMod\gui\imagesets\my_icons.paa"
  }
 }
 Images {
  ImageSetDefClass hud_health {
   Name "hud_health"
   Pos 10 10
   Size 64 64
   Flags 0
  }
  ...
 }
 Groups {
 }
}
```

This matches the vanilla layout: `P:\gui\imagesets\playstation_buttons2.imageset:1-24` has the same `Name` / `RefSize` / `Textures` / `Images` / `Groups` blocks and per-sprite `Name` / `Pos` / `Size` / `Flags 0` fields.

`Pos` is the sprite's top-left in atlas pixels (after gutter); `Size` is the sprite's own dimensions (gutter is NOT included in `Size`). In the vanilla file above, `DPAD_all_directions` has `Pos 1 1` and `Size 44 44` inside a `RefSize 64 64` atlas, so `Size` is the sprite alone.

## Refuses to run if

- `/dayz-preflight` returns non-zero.
- Pillow is not installed.
- `<ModName>` is given but no project is cached by `/dayz-init`, or `workspace/<ModName>/` doesn't exist.
- `<mod-root>` isn't a directory.
- `<mod-root>/.gui-sources/` doesn't exist or has no subfolders other than dot folders.
- A set folder name is not an identifier (for example `main menu`); that set fails and the others still build.
- A set splits into `<setname>_N` and another source set is named `<setname>_N`; that set fails and the others still build.
- A sprite file name is not an identifier (for example `hud health.png` or `hud-health.png`); that set fails and the others still build.
- A `.png` cannot be read as an image (corrupt, truncated or 0 bytes); that set fails with a `[FAIL]` naming the file, and the others still build.
- A single sprite is larger than 4096x4096 minus gutter (won't fit in any allowed atlas size). Shrink it or deliver it outside an imageset.
- `ImageToPAA.exe` is missing from DayZ Tools.

## Do not

- Don't move source PNGs out of `.gui-sources/` into the mod tree; `/dayz-build-pbo` excludes only `.gui-sources\`, so PNGs anywhere else are packed into the PBO.
- Don't add gutter pixels to the per-sprite `Size` values; the engine reads `Size` as the sprite's own dimensions.
- Don't drop the 10px gutter; it prevents bleed between adjacent sprites at non-1:1 scaling.
- Don't change atlas to non-power-of-two; both width and height are POT independently (rectangular allowed). Vanilla atlases are POT (`P:\gui\imagesets\playstation_buttons2.imageset:3` is `RefSize 64 64`); that the GUI and `.paa` toolchain reject non-POT atlases is unverified.
