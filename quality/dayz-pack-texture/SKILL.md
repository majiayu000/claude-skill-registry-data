---
name: dayz-pack-texture
description: "Converts PNG or TGA images to DayZ .paa textures with ImageToPAA, after checking each filename has a texture-role suffix such as _co, _ca, _nohq or _smdi. Use when a mod's textures need packing for config.cpp, .rvmat or hiddenSelectionsTextures references."
argument-hint: "[--dry-run] <image_co.png|.tga> [<image2_nohq.png> ...]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-pack-texture

Convert one or more PNG/TGA images to `.paa` (DayZ's texture format) using DayZ Tools' `ImageToPAA.exe`. Each input file must end in a texture-role suffix. ImageToPAA reads the suffix to pick the compression and color space (its rules are in `<DayZ Tools>\Bin\ImageToPAA\TexConvert.cfg`). The skill accepts every suffix that has a rule there and is used by vanilla textures under `P:\DZ`:

| Suffixes | Role |
|---|---|
| `_co`, `_ca` | Color / diffuse, without and with alpha |
| `_lco`, `_lca` | Terrain layer color (satellite and mask textures), without and with alpha |
| `_nohq`, `_no`, `_non`, `_nopx` | Normal map: high quality, plain, with noise in alpha (vegetation), parallax |
| `_smdi`, `_sm` | Specular (`_smdi` is the higher-bit-depth form vanilla gear uses) |
| `_as`, `_ads`, `_adshq` | Ambient shadow (`_ads`, `_adshq`: ambient, diffuse and shadow) |
| `_mc`, `_mco` | Macro texture, multiply color |
| `_dt`, `_detail`, `_cdt`, `_dtsmdi` | Detail textures |
| `_mask`, `_sky` | Masks, sky |

Most mod gear needs only `_co` (or `_ca`), `_nohq` and `_smdi`.

A file like `vest_camo_co.png` becomes `vest_camo_co.paa` next to it. If a `.paa` of that name already exists, it is first copied to `vest_camo_co.paa.bak`, then overwritten. There is one rolling backup per texture: each repack replaces the `.bak` from the previous run, so iterating on a 2048 texture never piles up copies in `data\` (and the build's `*.bak` exclude matches it). If that conversion fails, the backup is copied back over the `.paa` automatically, so `config.cpp` and `.rvmat` never point at a broken file. To get the previous `.paa` back after a successful run, delete the new one and rename the backup before you repack again; the next repack replaces it. Keep a hand-tuned `.paa` you want to preserve outside the folder. Numbered backups (`.paa.bak.1`, `.paa.bak.2`) left by older releases of this skill are never touched; each run prints how many there are so you can delete them. Run with `--dry-run` first to see what would be written.

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
python "<skill-dir>\pack_texture.py" [--dry-run] <input1> [<input2> ...]
```

| Argument | Required? | Notes |
|---|---|---|
| `--dry-run` | no | Check that `P:\` is mounted (read-only), validate every input, resolve ImageToPAA, and list each `.paa` that would be written and each existing `.paa` that would be backed up (with the backup name, and whether it replaces a current `.bak`). Converts nothing and writes no file. It skips the full `/dayz-preflight`, because that creates the `P:\Mods` junction when it is missing. |
| `<input>` | yes (one or more) | Path to a `.png` or `.tga` file with a valid suffix in the basename. Pass each file explicitly; cmd.exe does not expand globs. |

## What it does

1. Preflight gate: `/dayz-preflight`, or with `--dry-run` only its read-only `P:\` check.
2. Validate every input before converting any, and report every problem found across all inputs in one run (then exit 1, converting nothing): the input exists and is a file (not a folder) that can be read, the extension is `.png` or `.tga` (any case), the basename ends with one of the suffixes above (any case) before the extension, and both sides of the image are powers of two. The size comes from the PNG `IHDR` chunk after the PNG signature, or from the TGA header once its color map type (0 or 1), image type (1 to 3, or 9 to 11 for RLE) and bits per pixel (8, 15, 16, 24 or 32) are valid, so a corrupt `.tga` or a renamed PNG is refused here. No two inputs may map to the same `.paa`.
3. Resolve `ImageToPAA.exe` from DayZ Tools (env / registry / Steam paths) via `find_dayz_tools()`.
4. With `--dry-run`, list what would be written and stop with exit code 0. Otherwise, for each input, copy any existing `.paa` to `<name>.paa.bak` (through a temporary file, so a failed copy leaves the previous backup intact; a `[WARN]` line counts any numbered backups from older releases), then invoke `ImageToPAA.exe <input> <output.paa>`. If the backup copy itself fails, that input is skipped and the existing `.paa` is left untouched. Streams the tool's output live. A conversion counts as failed if the tool exits non-zero, if no `.paa` appears, or if an existing `.paa` was left unchanged (its modification time did not move), so a stale file from an earlier run is never reported as packed. On a failure the backup is copied back over the `.paa` (and kept), or, when there was no `.paa` before, any partial file the failed run wrote is removed; each step is printed. If that undo fails, a `[FAIL]` line names the file to copy back by hand.
5. Report a summary of successes and failures. Exit non-zero if any failed.

## Refuses to run if

- `/dayz-preflight` returns non-zero (with `--dry-run`: `P:\` is not mounted).
- `ImageToPAA.exe` is not found under DayZ Tools.
- An input file doesn't exist, is a folder (for example a folder named `x_co.png`), or cannot be read.
- An input doesn't end in `.png` or `.tga`.
- An input's basename doesn't end with one of the suffixes above. ImageToPAA picks the compression from the suffix, and the rest of the pipeline (rvmat stages, reviewers) relies on it to tell what the texture is for. The message suggests a name from the stem: a trailing `_normal` or `_nrm` becomes `_nohq`, `_spec` or `_specular` becomes `_smdi`, `_alpha` becomes `_ca`, `_diffuse` or `_albedo` becomes `_co`, and any other name gets `_co` appended.
- Two inputs would write the same `.paa` (for example `vest_co.png` and `vest_co.tga`, or the same file passed twice), since the second conversion would silently replace the first.
- An input's width or height is not a power of two, or its size cannot be read from the header (a missing PNG signature or `IHDR` chunk, or a TGA header with an invalid color map type, image type or bits per pixel). The message names the nearest vanilla size from `skills/_shared/textures/suffixes-and-sizes.md` (for example 1000 x 1000 becomes 1024 x 1024). Nothing is converted until every input passes, and every failing input is listed in the same run.

## Output

```
DayZ preflight
... (preflight output)
Preflight complete.

[OK]   ImageToPAA: C:\...\DayZ Tools\Bin\ImageToPAA\ImageToPAA.exe

[Pack] vest_camo_co.png  ->  vest_camo_co.paa
... (ImageToPAA output) ...
[OK]   Wrote vest_camo_co.paa (123,456 bytes)

[Pack] vest_camo_nohq.png  ->  vest_camo_nohq.paa
[OK]   Backed up existing vest_camo_nohq.paa to vest_camo_nohq.paa.bak (replaced the previous backup)
... (ImageToPAA output) ...
[OK]   Wrote vest_camo_nohq.paa (98,765 bytes)

[OK]   2 of 2 textures packed.
```

## Do not

- Don't auto-rename inputs. If the user has `vest_camo.png` (no suffix), they rename it themselves so they're explicit about what role it plays.
