---
name: s32ct-clocks-graft-mex
description: >
  Modifies the Clocks tool of an S32 Configuration Tools .mex for any
  S32-family MCU and any installed RTD version: changes clock
  frequencies, adds a McuClockReferencePoint, switches power modes,
  retargets AIPS_PLAT_CLK / CORE_CLK / CAN_PE_CLK / EMIOS_CLK, enables a
  PLL, configures SXOSC, sets up CLKOUT. Every trigger must name the
  Clocks tool, a `.mex` project, or a concrete S32 clock identifier.
  Triggers on "configure the Clocks tool in my .mex", "change CORE_CLK in
  the .mex clock tree", "set CAN_PE_CLK to N MHz", "apply the
  max-performance clock preset to this .mex", "low-power clock
  configuration", "add a 32 kHz SXOSC clock source", "enable the PLL",
  "MC_CGM_MUX_*", "PLL_PHI", "edit ClockConfig0". Do NOT trigger on
  generic performance, speed or power requests naming no Clocks-tool or
  `.mex` context ("make it faster", "reduce power"), nor on read-only
  clock lookups (use `s32ct-clocks-info`).

license: LA_OPT_Online Code Hosting NXP_Software_License
allowed-tools: Read, Write, Edit, Grep, Bash(python:*)
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-clocks-info, s32ct-distributions]'
  tags: '[s32ct, configuration-tools, graft, mex-authoring, headless, clocks]'
---

# S32CT Clocks Graft / Tune .mex

Edit the `<clock_configuration>` block of a `.mex` in one of three
modes: apply a validated performance preset, tweak individual
`<setting id value/>` entries, or lift a whole `<clock_configuration>`
from an example `.mex`. Optionally adds `McuClockReferencePoint_*`
entries so driver `*ClockRef` settings map to the right domain.
Sibling of `s32ct-peripherals-graft-mex`: same "lift validated XML,
adapt, validate" workflow applied to the Clocks tool.

## When to use
- Use for: user names the Clocks tool or a clock frequency; a driver's
  runtime behaviour (baud rate, PWM resolution, ADC conversion time)
  depends on a clock domain that the default
  `McuClockReferencePoint_0 -> CORE_CLK` shortcut gets wrong; peripheral
  performance higher than the template default is required; a new
  `McuClockReferencePoint_*` is needed for a driver instance.
- Do **not** use this skill for: Pins or Peripherals changes (use
  `s32ct-pins-author-mex` / `s32ct-peripherals-author-mex` /
  `s32ct-peripherals-graft-mex`); read-only queries (use
  `s32ct-clocks-info` / `s32ct.inspect_clock_outputs`);
  adding a *second* `<clock_configuration>` sibling - see
  `references/multi-config.md`.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `the s32ct.inspect_* actions` | Read `query=clock_outputs / clock_settings / clock_points / xrefs`. |
| MCP tool | `s32ct.lookup_enum_values` | Legal values for a setting on this package. |
| MCP tool | `s32ct.sanitize` | Post-lift normalisation of `Mcu/Mcl` cross-refs. |
| MCP tool | `s32ct.validate` | Validation gate. `tool_name="Clocks"` for fast iteration. |
| MCP action | `nxp_s32ct_execute_action(action_name="s32ct.generate_code", params={...})` | Emit `Mcu_Cfg.[ch]`. |
| Script | `scripts/inspect_clocks.py` | Standalone `query=clock_*` equivalent. |
| Script | `scripts/apply_settings.py` | Apply preset or `(id, value)` edits. Idempotent. |
| Script | `scripts/lift_clockconfig.py` | Extract `<clock_configuration>` from an example. |
| Script | `scripts/add_clock_point.py` | Add a `McuClockReferencePoint_*`. |

## Quickstart

*Shell: examples use Windows `cmd.exe` line continuation `^`; on POSIX shells (`bash`/`zsh`) replace `^` with `\`.*

1. Inspect the current clock state:

   ```bat
   python scripts/inspect_clocks.py project.mex --query clock_outputs
   ```

2. Choose a mode: `preset`, `tweak`, or `lift`.

3. **`mode=preset`** (most common - "make this fast"):

   ```bat
   python scripts/apply_settings.py project.mex ^
       --preset s32k312:max_performance ^
       --out    project.tuned.mex
   ```

4. **`mode=tweak`** - bump one setting:

   ```bat
   python scripts/apply_settings.py project.mex ^
       --set CORE_MFD.scale=40 ^
       --set MC_CGM_MUX_0_DIV0.scale=1 ^
       --out project.tuned.mex
   ```

5. **`mode=lift`** - graft the K344 example's clock tree:

   ```bat
   python scripts/lift_clockconfig.py project.mex ^
       --example ".../S32K344/RTD/example.mex" ^
       --out     project.tuned.mex
   ```

6. Sanitize (only after `lift`) and validate - first Clocks, then
   Peripherals + Pins for regression:

   ```
   s32ct.sanitize(project_path=project.tuned.mex)
   s32ct.validate(project_path=project.tuned.mex, tool_name="Clocks")
   s32ct.validate(project_path=project.tuned.mex)
   ```

7. Optional - add semantic clock points so driver `*ClockRef` values
   can point at the right domain:

   ```bat
   python scripts/add_clock_point.py project.tuned.mex ^
       --name LPUART_CLK  --select AIPS_SLOW_CLK ^
       --name LPSPI_CLK   --select AIPS_PLAT_CLK ^
       --name CAN_PE_CLK  --select AIPS_PLAT_CLK ^
       --name EMIOS_CLK   --select AIPS_PLAT_CLK ^
       --out  project.final.mex
   ```

Full workflows (A / B / C), setting-id conventions, and the preset
tables are in `references/`.

## Configuration

Core inputs (see `references/configuration.md` for the full input
table and the `tweak` / `clock-point` schemas):

- `project_path`, `output_path` -- absolute paths.
- `mode` -- `preset` | `tweak` | `lift`.
- `mcu`, `package` -- e.g. `S32K312`, `S32K312_172HDQFP`.
- `preset` -- one of the four presets (mode=preset).
- `tweaks` -- array of `{ type, id, value, [from, to] }` (mode=tweak).
- `example_mex` -- source `.mex` (mode=lift).
- `add_clock_points` -- optional `McuClockReferencePoint_*` entries.
- `platform_sdk` / `rtd_version` / `s32ds_install` -- auto-discovered.
- `validate`, `overwrite` -- default `true` / `false`.

Enumerate legal `tweak.id` values on this package with
`s32ct.inspect_clock_settings`.

## Guardrails

**Scope.** Writes only to `output_path`. Uses `s32ct.sanitize` to
rewrite dangling `Mcu/Mcl` references introduced by a lift. Never
touches target hardware; CLI invocations are read-only on the
filesystem apart from `output_path` and validator capture files.

**Destructive actions.** Refuses to overwrite an existing
`output_path` unless `overwrite=true`. Refuses values above declared
datasheet ceilings - the validator only enforces syntactic
correctness; pushing beyond a datasheet ceiling causes silent silicon
failure. Presets are pre-clamped; freestyle values that exceed the
clamp are rejected.

**Refuse-and-escalate.** Refuses when the `.mex` fails Pins or
Peripherals validation before editing - clocks changes on a broken
`.mex` produce misleading diffs. Refuses when a `tweak.id` does not
exist for the target package (cross-check with `the s32ct.inspect_* actions`).
Refuses to invent numeric values not present in a validated example or
documented preset - freestyle overrides need explicit user intent.

## Validation loop

1. `s32ct.inspect_clock_outputs` before editing - baseline.
2. Apply the chosen workflow (preset / tweak / lift). After a lift,
   run `s32ct.sanitize` to fix cross-references.
3. `s32ct.validate(tool_name="Clocks")` - fast iteration. Uses the
   same 4-step stderr-capture / noise-filter procedure as the driver
   graft skill; `valid: true` = filtered stderr empty AND exit_code
   == 0. The launcher (`toolsc.exe` / `s32dsc.exe` - see
   `s32ct-distributions`) always returns 0, so exit code alone is
   insufficient.
4. `s32ct.validate` without `tool_name` - full regression across
   Pins + Peripherals + Clocks. Driver instances reference clock-tree
   elements; a removed output id will break them.
5. `s32ct.inspect_clock_outputs` after editing with
   `diff_against=<baseline>` to confirm intended before/after delta.
6. **Pass** = Clocks + full regression clean AND before/after matches
   intent. **Fail** = surface filtered stderr verbatim and consult
   `references/error-decision-tree.md`.

## Out of scope

- Pins or Peripherals tool changes.
- Read-only queries about the current clock state (use
  `s32ct-clocks-info` / `the s32ct.inspect_* actions`).
- Adding a second `<clock_configuration>` sibling - see
  `references/multi-config.md`.
- Retargeting driver `*ClockRef` values themselves. This skill adds
  the semantic clock points; re-pointing each driver instance is a
  search/replace step handled by the caller (or the driver-graft
  skill).
- Datasheet-forbidden frequencies. The validator accepts syntactically
  valid but physically illegal values - the presets are pre-clamped;
  freestyle overrides beyond the clamp are refused.

## See Also

- `references/clock-anatomy.md` - S32CT clock data model: `TOP.xml`,
  `FXOSC.xml`, `MODULE_CLOCKS.xml`, `<configuration_element>`,
  `<selector>`, `<configurable_clock_source>`, and how `<setting id>`
  maps to them. Read on the first clocks task or when a new setting id
  surfaces.
- `references/performance-presets.md` - per-MCU-family preset tables
  (max-perf / mid-perf / low-power-run / safe): `(setting_id, value)`
  tuples plus before/after frequency tables.
- `references/error-decision-tree.md` - Clocks-tool validation errors
  and their fixes. Read on any unrecognised `SEVERE: [TOOL]` line.
- `references/multi-config.md` - adding a second
  `<clock_configuration>` (e.g. `LowPower`) for runtime mode switching.
- Related skills: `s32ct-peripherals-graft-mex` (driver-side
  companion), `s32ct-clocks-info` (read-only knowledge),
  `s32ct-pins-author-mex` (EXTAL/XTAL routing when enabling new
  oscillators), `s32ct-generate-code` (emit `Mcu_Cfg.[ch]`),
  `s32ct-distributions` (install-root discovery).
