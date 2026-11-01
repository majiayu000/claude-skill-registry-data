---
name: dayz-lint
description: "Finds errors that would stop a DayZ mod loading, before it is packed: config.cpp syntax, CfgPatches, requiredAddons, $PBOPREFIX$ and its P: link, script modules, modded classes, missing files and bad suffixes. Prints PASS or FAIL with file:line findings, each with an owner and a fix. Runs first inside /dayz-gate build and /dayz-build-pbo; use it alone to check a mod while you work."
argument-hint: "<ModName> [--json] | --mod-dir <folder> [--json]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-lint

A script reads the mod's files and reports every problem it is sure of. It starts no process, needs no DayZ Tools, and takes under a second. The AI only reads the findings and hands each one to its owner.

Follow `skills/_shared/dayz-conventions.md`.

## How to run

```cmd
python "<skill-dir>\lint.py" <ModName> [--json]
python "<skill-dir>\lint.py" --mod-dir <folder> [--json]
```

| Argument | Notes |
|---|---|
| `<ModName>` | A mod under `workspace/<ModName>/` in the project cached by `/dayz-init`. A plain folder name: a name holding `/`, `\`, `:` or `..` is refused with ERROR; pass a path with `--mod-dir`. |
| `--mod-dir` | Lint any folder instead. Its name is the mod name unless `<ModName>` is given too. Paths in findings and fixes are shown from the current folder. |
| `--json` | Print the full report as JSON after the verdict line. |

You don't need to run it before a build: `/dayz-gate build` and `/dayz-build-pbo` run it first and stop on any error.

## Output and exit codes

The first line on stdout is always the verdict: `PASS` (exit 0, warnings allowed), `FAIL` (exit 1, at least one error) or `ERROR` (exit 2: bad arguments, no cached project, or the mod folder does not exist). On `ERROR` the next line says why (with `--json`, a `{"verdict": "ERROR", "error": "..."}` object), and nothing is printed on stderr first. Otherwise one line per finding and its owner:

```
FAIL
- workspace/MyVest/config.cpp:5  error cfgpatches-field: CfgPatches class MyVest: units must be an array, units[] = {...};.
    -> dayz-config-specialist: Write it as an array: units[] = {...}; weapons[] = {...}; requiredAddons[] = {...}; ...
  1 error(s), 0 warning(s)
```

With `--json`:

```json
{
  "verdict": "FAIL", "mod": "MyVest", "mod_dir": "...", "errors": 1, "warnings": 0,
  "findings": [{
    "rule": "cfgpatches-field", "severity": "error", "file": "workspace/MyVest/config.cpp", "line": 5,
    "message": "CfgPatches class MyVest: units must be an array, units[] = {...};.",
    "text": "[lint:cfgpatches-field] CfgPatches class MyVest: units must be an array, units[] = {...};.",
    "triage": {"status": "known", "id": "lint-cfgpatches-field", "meaning": "...", "fix": "...", "owner_agent": "dayz-config-specialist", "fingerprint": "..."}
  }]
}
```

Each rule has a `lint-<rule>` entry in `skills/dayz-gate/known-errors.json` with its meaning, fix and owner, so lint findings are triaged the same way as log lines. Owner `user` means the user has to act; owner `dayz-orchestrator` means a skill run fixes it. Fixes that name `workspace/<ModName>/` are rewritten to the folder actually linted. For a `--mod-dir` folder outside the cached project's `workspace\`, where `/dayz-add-scaffold` refuses to run, the `p-link`, `pboprefix-missing` and `config-missing` fixes say what to create by hand (or point at `/dayz-import-mod`) instead.

## Rules

A finding is an error only when it stops the mod packing or loading. Everything else is a warning. Errors fail the lint, and so the gate and the build. Warnings are listed and do not.

| Rule | Severity | Finds |
|---|---|---|
| `config-missing` | error | No `config.cpp`. A payload-only bundle (prebuilt `Addons\*.pbo`, no `config.cpp`) passes with a note instead. |
| `config-syntax` | error | Unbalanced braces, a missing `;` or `};`, an array without `[]`, `;` between array elements. Same grammar as the edit hook (`hooks/edit_check.py`). The structure rules below wait until the syntax is fixed. |
| `cfgpatches-missing`, `cfgpatches-empty` | error | No `class CfgPatches`, or one with no patch class inside. |
| `cfgpatches-field` | error | `units`, `weapons` or `requiredAddons` written without `[]`, so it is not an array. |
| `cfgpatches-field-missing` | warning | A patch class without `units[]` or `weapons[]`. The engine tolerates it: vanilla `DZ_data_aiconfigs` in `P:\DZ\data\aiconfigs\config.cpp` has an empty body. |
| `required-addons-missing` | error | A patch class without `requiredAddons[]`, so its config can load before the vanilla classes it changes. |
| `required-addon-name` | error | An entry that is not a class name (a path, a `.pbo`, an `@mod` folder, a space), the mod's own patch class, or a `DZ_` name that no vanilla config on `P:\DZ\` or `P:\scripts\` declares. |
| `required-addon-duplicate` | warning | The same entry twice. |
| `pboprefix-missing`, `pboprefix-mismatch` | error | No `$PBOPREFIX$`, or one that does not hold exactly the mod name, which `/dayz-build-pbo` needs. |
| `pboprefix-encoding` | error | A `$PBOPREFIX$` that is UTF-16 (what Windows PowerShell 5.1 writes for `echo <ModName> > $PBOPREFIX$`) or not valid UTF-8, so its prefix cannot be read. Save it as plain ASCII or UTF-8 holding only the mod name. The other rules still run. |
| `p-link` | error | `P:\<prefix>\` is missing, is a real folder, or points away from the mod folder. A link that reaches the mod folder through another junction (the `/dayz-import-mod` layout, `P:\<prefix>` to `workspace\<ModName>` to the source) counts as pointing at it. The fix is `/dayz-add-scaffold <ModName> --piece junction` for a mod in the cached project's `workspace\`; for a `--mod-dir` folder outside it, `/dayz-import-mod --source <folder>` or `mklink /J P:\<prefix> <folder>`. |
| `p-not-mounted` | warning | `P:\` is not mounted, so the link and the vanilla `DZ_` names were not checked. |
| `script-module-path` | error | A `CfgMods` script module lists a folder outside the mod or one that does not exist. |
| `script-module-layer` | error | A module lists another layer's folder, for example `worldScriptModule` with `3_Game`. |
| `script-module-unlisted` | warning | A `scripts/` folder holds `.c` files that no module lists. The mod still loads; the engine just ignores those files. |
| `modded-class-extends` | error | `modded class Foo extends Foo` or `modded class Foo: Foo`, a silent no-op. Also caught when the `extends` or `:` is on the next line; the finding names the line holding `modded`. Commented-out code is ignored; `//` and `/*` inside a string are not comments. |
| `script-suffix` | warning | A file under `scripts/` that is not `.c`, so it is never compiled. Dot files such as `.gitkeep` are skipped. |
| `missing-model`, `missing-texture`, `missing-file` | error | A path in `config.cpp` or a `.rvmat` that starts with the prefix but names a file that is not in the mod. Paths into vanilla or other mods are not checked. |
| `absolute-path` | error | A disk path (`P:\...`, `workspace\...`) where the game expects a path from the prefix. |
| `texture-format` | error | A `.png`, `.tga`, `.jpg`, `.jpeg`, `.bmp` or `.dds` where the game needs a `.paa`. That is the only finding for the reference: whether the image exists is not checked, since the fix replaces the path. |
| `texture-suffix` | warning | A texture in `hiddenSelectionsTextures[]` or a `.rvmat` `texture` without a role suffix such as `_co`, `_nohq` or `_smdi`. |
| `rvmat-syntax` | error | A `.rvmat` with an unclosed string or comment. |

## Inside the build check

- `/dayz-gate build` lints first. On an error it reports FAIL with the lint findings as failures (category `lint`, triaged against `known-errors.json`) and does not stop a running session or build. The JSON report gains `"lint": {"verdict", "errors", "warnings"}`; lint warnings join the report's warnings.
- `/dayz-build-pbo` lints right after it reads the project cache, before `/dayz-preflight`. On an error it prints `[FAIL]` with each `file:line` and exits 1. It leaves the `P:\<ModName>\` link to its own junction check.

## Limits

- Lint checks files, not behaviour. Script compile errors still surface in `/dayz-gate ingame`.
- Paths into vanilla or another mod are not checked, and non vanilla `requiredAddons` names are only checked for shape. `/dayz-gate ingame --deps` covers those at run time.
- `#include` files are not followed.

## Do not

- Don't edit `known-errors.json` to silence a finding; fix the mod or, if lint is wrong, the rule in `lint.py` with a test.
