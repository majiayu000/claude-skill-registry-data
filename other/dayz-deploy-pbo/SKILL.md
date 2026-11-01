---
name: dayz-deploy-pbo
description: "Copies prebuilt PBOs and keys from a workspace bundle (workspace/<ModName>/Addons and Keys) to P:\\Mods\\@<ModName>\\ without AddonBuilder. Use when a mod ships only PBOs (third-party or umbrella bundles), or after /dayz-build-pbo builds a bundle's linker PBO."
argument-hint: "<ModName> [--dry-run] [--force]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-deploy-pbo

Mirror pre-compiled artifacts from a workspace bundle folder to the deploy tree: `workspace/<ModName>/Addons/*.pbo` (+ `*.bisign`) to `P:\Mods\@<ModName>\Addons\`, `Keys/*.bikey` to `P:\Mods\@<ModName>\Keys\`, plus optional `meta.cpp`/`mod.cpp`. Pure copy: no AddonBuilder, no binarization, no buildable source required (`config.cpp` and `$PBOPREFIX$` are the build path's gate, not this one). The preflight gate, project cache and ownership-marker rules come from `skills/_shared/skill_helpers.py`, shared with `/dayz-build-pbo` and `/dayz-clean-workspace`.

Follow `skills/_shared/dayz-conventions.md` and "Bundle / umbrella mods" in `skills/_shared/conventions/config.md`.

## How to run

```cmd
python "<skill-dir>\deploy.py" <ModName> [--dry-run] [--force]
```

| Argument | Required? | Notes |
|---|---|---|
| `<ModName>` | yes | Must match a bundle folder `workspace/<ModName>/` (in the project cached by `/dayz-init`) containing `Addons/` with at least one `.pbo`. Same name rule as `/dayz-new-mod`: starts with a letter, then letters, digits and underscores, at most 64 characters. |
| `--dry-run` | no | Runs every check and gate (steps 1-3 and the linker-name refusal), then prints the copy plan instead of copying: one line per file, `copy` (new), `overwrite` (an existing deployed file that differs and would be replaced in place), `newer` (the deployed file is newer than the bundle copy, so a real run refuses unless `--force`) or `unchanged`, followed by the unsigned and stale `[WARN]`s from step 8. Copies nothing, creates no folders and does not write the ownership marker. `/dayz-preflight` still runs as usual. Exits 0. Use it before redeploying over a bundle you care about. |
| `--force` | no | Overwrite deployed files even when they are newer than the bundle copy (see step 4). Nothing is backed up, so use it only when you mean to roll the deployed build back to the bundle's. |

## What it does

1. **Preflight gate** — reads the project cached by `/dayz-init`, runs `/dayz-preflight` (halts on non-zero), and confirms `P:\Mods\` is a junction to `!Workshop`.
2. **Bundle check** — verifies `workspace/<ModName>/Addons/` exists and contains at least one `.pbo`. Does not require `config.cpp`, `$PBOPREFIX$`, or the `P:\<ModName>\` junction — a pure payload bundle has no buildable source.
3. **Ownership gate** — if `P:\Mods\@<ModName>\` already exists, it must contain the `.agentic-z-scaffold` marker with matching content (the same ownership rule `/dayz-clean-workspace` uses). An unmarked dir could be a subscribed mod or hand-placed folder; deploy refuses to touch it.
4. **Newer-file guard** — before copying anything, compares every deployed file the bundle would replace with its bundle copy. If any deployed file has a later modified time than the bundle copy (by more than 2 seconds), deploy prints `[FAIL]`, lists those files, copies nothing and exits 1, so redeploying an older bundle never silently rolls back a newer build. Update the bundle, or rerun with `--force` to overwrite them anyway. A deployed file that is older than the bundle copy, or the same age with a different size, is overwritten in place with no backup; that is a normal redeploy.
5. **Copy Addons** — mirrors `Addons/*.pbo` + `Addons/*.bisign` into `P:\Mods\@<ModName>\Addons\`. Idempotent: a file already present with identical size + mtime is skipped. Purely additive: nothing in the deploy dir is ever deleted, so a linker PBO placed there by `/dayz-build-pbo` survives.
6. **Copy Keys** — mirrors `Keys/*.bikey` into `P:\Mods\@<ModName>\Keys\` (skipped entirely if the bundle has no keys).
7. **Copy metadata** — `meta.cpp` / `mod.cpp` from the bundle root into `P:\Mods\@<ModName>\`, if present.

   If any copy in steps 5-7 fails (typically a PBO held open by a running DayZ client or server), deploy prints `[FAIL] could not copy <file>: <error>` with the hint "Close DayZ or run /dayz-stop-test", writes the ownership marker so the rerun is not refused, and exits 1. Files copied before the failure stay; the rerun skips them as unchanged.
8. **Verify** — reports copied vs. unchanged counts per run, and `[WARN]`s for every `.pbo` lacking a matching `<name>.pbo.<key>.bisign`, compared case-insensitively as Windows does (signature-checking clients will reject unsigned PBOs). It also `[WARN]`s for every file the bundle no longer ships (dropped or renamed) — any `.pbo` or `.bisign` in `P:\Mods\@<ModName>\Addons\` and any `.bikey` in `P:\Mods\@<ModName>\Keys\` — with a `del` line to remove it by hand. Deploy never deletes, so a stale PBO keeps loading in game and a stale `.bikey` keeps being trusted by servers that take keys from the mod. The built linker `<ModName>.pbo` and its `<ModName>.pbo.*.bisign` are not reported when the bundle has a linker `config.cpp`.
9. **Drop ownership marker** — writes `P:\Mods\@<ModName>\.agentic-z-scaffold` (single line: the modname), exactly as `/dayz-build-pbo` does, so `/dayz-clean-workspace` treats the bundle as managed and can remove both `workspace/<ModName>/` and the deployed dir (a pure payload bundle has no `config.cpp`, so the marker is what marks it as ours). If the marker cannot be written, deploy prints `[FAIL]` and exits 1 even though the files were copied, because the next build, deploy and clean would all refuse that folder.

## Composing with /dayz-build-pbo (umbrella bundles)

A bundle may carry an optional *linker* `config.cpp` + `$PBOPREFIX$` (a content-free `CfgPatches` declaring `requiredAddons[]`). Build the linker from source first, then deploy the payload:

```cmd
python "<skill-dir>\..\dayz-build-pbo\build.py" <ModName>
python "<skill-dir>\deploy.py" <ModName>
```

Both write the same ownership marker; deploy never deletes, so the built `<ModName>.pbo` and the copied payload PBOs coexist under one `@<ModName>\Addons\`. In such a bundle a payload file may not be named `<ModName>.pbo` or `<ModName>.pbo.<key>.bisign` (deploy refuses). Order doesn't matter for correctness. `/dayz-build-pbo --clean` refuses while payload PBOs sit in `Addons\`, since its `-clear` would wipe them.

## Refuses to run if

- `<ModName>` fails the name rule (checked first, so a name such as `..\Other` never reaches the disk).
- No project is cached (run `/dayz-init`).
- `/dayz-preflight` returns non-zero, or `P:\Mods\` is not a valid junction.
- `workspace/<ModName>/` is missing, has no `Addons/` folder, or `Addons/` contains no `.pbo`.
- The bundle has a linker `config.cpp` and also ships `Addons/<ModName>.pbo` or `Addons/<ModName>.pbo.<key>.bisign` (any case). `/dayz-build-pbo` writes the linker to `P:\Mods\@<ModName>\Addons\<ModName>.pbo`, and its signature sits next to it, so the copy would overwrite them. Rename the payload file, or remove the linker `config.cpp` + `$PBOPREFIX$`. Checked before anything is copied.
- `P:\Mods\@<ModName>\` exists without the `.agentic-z-scaffold` ownership marker (or with mismatched content). Remove the dir manually if it's actually yours: `cmd /c rmdir /s /q P:\Mods\@<ModName>`.
- A deployed file the bundle would replace is newer than the bundle copy and `--force` was not passed (step 4). Nothing is copied.

## Output

Success:

```
DayZ preflight

[OK]    P:\ is mounted
...     (rest of the /dayz-preflight report)

Preflight complete.
[OK]    P:\Mods junction valid
[OK]    workspace\MyBundle\Addons\ found (with .pbo payload)
[WARN]  extras.pbo has no matching .bisign - clients with signature verification enabled will reject it.

[OK]    Deployed to P:\Mods\@MyBundle\ - 6 copied, 0 unchanged (3 .pbo, 2 .bisign, 1 .bikey)
```

Re-run with nothing changed: same shape, `0 copied, 6 unchanged`.

Dry run (`--dry-run`), after the same check lines:

```

Dry run - nothing will be written to P:\Mods\@MyBundle\
  overwrite  P:\Mods\@MyBundle\Addons\core.pbo
  unchanged  P:\Mods\@MyBundle\Addons\core.pbo.mykey.bisign
  copy       P:\Mods\@MyBundle\Addons\extras.pbo
[WARN]  extras.pbo has no matching .bisign - clients with signature verification enabled will reject it.

[OK]    Dry run: 2 would be copied, 1 unchanged. Rerun without --dry-run to deploy.
```

When a deployed file is newer than the bundle copy, its plan line reads `newer`, it is counted in neither total, and the summary is preceded by `[WARN]  1 deployed file(s) marked 'newer' are newer than the bundle copy. A real run refuses unless --force is passed.`

Newer deployed file (real run without `--force`):

```
[FAIL]  Deployed file(s) are newer than the bundle copy, so deploying would replace a
       newer build with an older one. Nothing was copied:
         P:\Mods\@MyBundle\Addons\core.pbo
       Update the bundle, or rerun with --force to overwrite them anyway.
```

Failure (any step):

```
[FAIL]  <reason>
       <hint or next step>
```

## Do not

- Don't delete or overwrite anything the bundle doesn't provide — no `-clear`-style wipe, ever. The additive copy is what lets a build-pbo linker PBO coexist with the payload.
- Don't pass `--force` by default — it exists to roll a newer deployed build back on purpose, and nothing is backed up.
- Don't require `config.cpp`/`$PBOPREFIX$` or the `P:\<ModName>\` junction — those gate the build path only.
- Don't invoke AddonBuilder or attempt to binarize — payload PBOs are already compiled (and may be large / LFS-backed; copy is the only correct operation).
- Don't repackage multiple PBOs into one prefixed PBO — each payload PBO keeps its own prefix; `@<ModName>` is just the container.
- Don't deploy into an unmarked `@<ModName>` dir — fail and let the user resolve the collision.
