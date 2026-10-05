---
name: s32ct-generate-mex-config
description: >
  Generates a starter S32 Configuration Tools `.mex` project file for any
  supported NXP S32 MCU / package / RTD combination by cloning a bundled
  `<MCU>_default.mex` reference template and applying a structured JSON
  patch (peripheral instance add / remove / patch, tool enable / disable,
  pin patches, clock patches). Use when the user asks to "generate a
  starter .mex", "clone .mex template", "create S32 Configuration Tools
  project file", "scaffold .mex for MCU X", "bootstrap .mex with
  peripheral add/remove/patch", "produce .mex from JSON modifications",
  "make me a .mex for <S32 MCU>", or "fresh mex project for
  <MCU>/<package>/<RTD>". Works for any S32 MCU/RTD/package for which a
  `<MCU>_default.mex` template is present next to the skill; ships with
  `S32K312_default.mex` for `S32K312 / S32K312_172HDQFP /
  PlatformSDK_S32K3`. File types: `.mex`, JSON patch input.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-distributions, s32ct-peripherals-info]'
  tags: '[s32ct, configuration-tools, mex-authoring, headless, configuration]'
---

# S32CT Generate `.mex` Configuration

Bootstrap helper that produces a well-formed S32 Configuration Tools
`.mex` project file by cloning a bundled `<MCU>_default.mex` template and
applying a structured JSON delta (tool enable/disable, peripheral
add/remove/patch, pin and clock overrides). The output can be opened in
S32CT, fed to the `s32ct-*` CLI skills, or handed to
`s32ct-generate-code` to emit driver sources.

## When to use

- Use for: producing a starter `.mex` for an S32 MCU with specific
  peripherals enabled/disabled or specific parameter overrides, without
  hand-editing 100+ KB of XML; scaffolding a deterministic `.mex` for CI
  / test flows from a small JSON patch; emitting an input artefact for
  downstream `s32ct-*` skills.
- Do **not** use this skill for: interactively editing pin routing or clock trees (use
  `s32ct-pins-facade` / `s32ct-clocks-facade` or the GUI); generating C
  driver code from a `.mex` (use `s32ct-generate-code`); discovering what
  a peripheral exposes (`s32ct-peripherals-info`).

## Available Capabilities

| Capability | Notes |
|---|---|
| Plain clone with fresh UUID | Default when no `modifications` supplied. Sidecar `ClockConfigurationMappings.txt` propagated. |
| Tool enable/disable | Toggles top-level `<pins>`, `<clocks>`, `<peripherals>`, `<dcd>`, `<ivt>`, `<efuse>`, `<gtm>`, `<quadspi>`, `<ffc>`, `<serdes>` sections. |
| `peripherals.add` / `.remove` / `.patch` | Insert new `<instance>` blocks, drop by name, or override `<set id="...">value</set>` fields. |
| Pin and clock patches | Structured deltas into the Pins and Clocks tool sections. |
| Optional headless validation | `validate=true` runs `toolsc.exe -HeadlessTool <tool> -ShowProblems` and folds captured stderr into the report. |
| MCU-agnostic template resolution | Any `<MCU>_default.mex` dropped into the skill folder becomes available automatically. See `references/adding-new-mcu.md`. |

## Quickstart

1. Identify the target MCU. If a `<MCU>_default.mex` is not yet bundled
   for that MCU, follow `references/adding-new-mcu.md` first.
2. Assemble inputs: `output_path` (required), optional `mcu`,
   `package`, `mcu_data`, `modifications` (see
   `references/patching-recipes.md`), and flags `regenerate_uuid`
   (default `true`), `copy_sidecars` (default `true`), `overwrite`
   (default `false`), `validate` (default `false`).
3. Invoke the skill. Behaviour:
   1. Resolve template: `template_path` if supplied, else
      `<skill_dir>/<mcu>_default.mex`. Reject with a template-missing
      error and list the bundled `*_default.mex` files if not found.
   2. Load template as XML, preserving namespace and attribute order.
   3. Apply `modifications` in the order: `common`, `tools`,
      `peripherals.remove`, `peripherals.add`, `peripherals.patch`,
      `pins`, `clocks`.
   4. If `regenerate_uuid=true`, assign a fresh top-level UUID v4.
   5. Serialise to `output_path` (refuse if it exists and `overwrite`
      is false). Preserve encoding and line endings.
   6. If `copy_sidecars=true`, copy
      `ClockConfigurationMappings.txt` (and any other sibling sidecar)
      alongside.
   7. If `validate=true`, run headless validation - see below.
4. Return a Markdown report: generated file path, summary of what
   changed vs. template, validation result (if run), and next-step
   suggestions.

Example - plain clone (default MCU):

```jsonc
{ "output_path": "C:\\tmp\\S32K312_starter.mex" }
```

Example - enable boot-image tools:

```jsonc
{
  "output_path": "C:\\tmp\\S32K312_boot.mex",
  "overwrite": true,
  "modifications": {
    "tools": { "DCD": { "enabled": true }, "IVT": { "enabled": true } }
  }
}
```

More recipes in `references/patching-recipes.md`.

## Configuration

- Bundled template: `S32K312_default.mex` (S32K312 / S32K312_172HDQFP /
  PlatformSDK_S32K3, schema `mex_configuration_19`, core `M7_0`).
- Bundled sidecar: `ClockConfigurationMappings.txt` carrying the
  `,PB,ClockConfig0` mapping line.
- Launcher for optional validation: `toolsc.exe` (desktop
  distribution) or `s32dsc.exe` (integrated_s32ds distribution),
  auto-discovered by the MCP at startup. See `s32ct-distributions`.

## Guardrails

- **Scope.** Read the bundled `<MCU>_default.mex` templates, write only
  to the user-supplied `output_path` (and sibling sidecar). Never
  modify a template in place - patch a copy. No target hardware, no
  FreeMASTER, no registers touched.
- **Destructive actions.** Refuse to overwrite an existing
  `output_path` unless `overwrite=true` is explicitly set. Refuse to
  patch on unknown top-level modification keys or unknown `type_id`
  values rather than silently ignoring.
- **Refuse and escalate.** If the requested MCU has no matching
  `<MCU>_default.mex`, reject the request, list the bundled templates,
  and point the user at `references/adding-new-mcu.md`. If a supplied
  `package` / `mcu_data` disagrees with the template's `<part_number>`
  / `<mcu_data>`, reject with a comparison message rather than
  rewriting the template.

## Validation loop

1. Copy `output_path` to a no-space location (e.g. `C:\tmp_mex\`);
   `cmd`'s stderr redirection fails on paths containing spaces.
2. Run `toolsc.exe -Load <path> -HeadlessTool <Tool> -ShowProblems`
   once per tool (`Pins`, `Clocks`, `Peripherals`, `DCD`, `IVT`,
   `eFUSE`, `GTM`, `QuadSPI`, `FFC` are the accepted values).
3. Capture stdout and stderr - the *Problems View* prints to the
   originator terminal only; no log file is created by default.
   Redirect to file for durability
   (`> problems.txt 2>&1`).
4. **Ignore the exit code.** `toolsc.exe` exits `0` even when the
   Problems View contains errors. Parse the captured text.
5. Zero problem lines after noise filtering means the tool is clean.
   Any remaining `SEVERE: [TOOL]` or `SEVERE: [Generation` lines are
   real - fix and re-run.

The skill folds this loop into the report when `validate=true`. The
canonical filter-then-count noise patterns are documented in
`s32ct-peripherals-author-mex/references/error-decision-tree.md`
(section: framework-noise catalog).

## Out of scope

- Interactive pin muxing or clock tree exploration.
- Enumerating the RTD peripheral catalogue (that is
  `s32ct-peripherals-info`).
- Generating driver C sources (that is `s32ct-generate-code`).
- Applying `-ApplyUseCase` / `-ImportC` / `-SetValue` transformations
  (that is `s32ct-cli` or a per-tool facade).
- Rewriting the schema namespace, `<part_number>`, or `<mcu_data>`
  fields of a template.

## See Also

- `references/mex-schema.md` - XML schema, namespace preservation,
  per-tag semantics.
- `references/patching-recipes.md` - JSON patch shapes, application
  order, per-driver examples, error responses.
- `references/adding-new-mcu.md` - procedure for dropping a new
  `<MCU>_default.mex` template.
- `s32ct-distributions` - launcher / prefix selection for the two
  S32CT distributions.
- `s32ct-peripherals-info` - resolve `type_id` values for
  `peripherals.add`.
- `s32ct-peripherals-author-mex`, `s32ct-peripherals-graft-mex` -
  author or lift-and-adapt driver `<instance>` blocks.
- `s32ct-pins-author-mex`, `s32ct-pins-info` - author or inspect pin
  routing.
- `s32ct-generate-code` - emit driver C sources from the produced
  `.mex`.
- `s32ct-cli`, per-tool facades (`s32ct-peripherals-facade`,
  `s32ct-clocks-facade`, ...) - headless transformations after
  generation.
