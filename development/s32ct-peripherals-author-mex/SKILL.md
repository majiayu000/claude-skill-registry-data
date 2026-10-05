---
name: s32ct-peripherals-author-mex
description: >
  Authors a fully-validated S32 Configuration Tools Peripherals-tool
  block on top of an existing Pins-tool routing for any S32 MCU
  (S32K1/K3, S32G2/G3, S32Z2, S32M, S32N, S32R, S32V, S32E, ...) and any
  installed RTD version, using the 5-source rule (`.component` schema
  plus `resource_tables/*.xml` plus `quick_selection` plus RTD example
  `.mex` plus existing `.mex`). Use when the user asks to "configure
  Peripherals tool in .mex", "add Spi/Uart/Can/Lin/Adc/Pwm instance",
  "author AUTOSAR driver configuration in S32 Configuration Tools",
  "add per-controller config container", "configure CanController /
  SpiPhyUnit / UartChannel / AdcHwUnit / PwmEmios", "validate .mex with
  -ShowProblems", or "my .mex will not generate driver C sources".
  Encodes the critical caveat that `-ShowProblems` returns exit code
  zero even on 25+ errors, so the workflow gates on stderr, not on
  exit code. File types: `.mex`, `.component`, `resource_tables/*.xml`,
  RTD example `.mex`.
license: LA_OPT_Online Code Hosting NXP_Software_License
allowed-tools: Read, Write, Edit, Grep, Bash(python:*), Bash(cmd:*), Bash(sh:*)
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-distributions, s32ct-pins-author-mex]'
  tags: '[s32ct, configuration-tools, mex-authoring, headless, peripherals, configuration]'
---

# S32CT Peripherals - Author `.mex` (from scratch)

Board-level driver `<instance>` authoring for the Peripherals tool of
S32 Configuration Tools. Composes driver blocks (Spi / Uart / Can /
Lin / Adc / Pwm / Wdg / ...) with per-controller configuration
containers on top of a Pins-populated `.mex`. Encodes the trap that
`toolsc.exe` exits `0` on 25 real validation errors.

## When to use

- Use for: composing a Peripherals-tool block on top of a
  Pins-populated `.mex`; authoring drivers where no RTD example ships
  on disk; fine-grained per-setting control; recovering from a
  suspicious "validation passed" report from a lower-level wrapper.
- Do **not** use this skill for: drivers where an RTD example is available - prefer
  the faster sibling `s32ct-peripherals-graft-mex` (3-6 rounds instead
  of 25+); Pins / Clocks / DCD / IVT / eFUSE / GTM / QuadSPI / FFC
  tools (each has its own skill); generating driver C sources (use
  `s32ct-generate-code` after validation is clean); application-level
  containers (`SpiChannel`/`Job`/`Sequence`, `CanHwFilter` masks,
  `AdcGroupDefinition`) - project-specific; see
  `s32ct-peripherals-info`.

## Available Capabilities

| Capability | Notes |
|---|---|
| 5-source authoring | Compose `<instance>` blocks from `.component` schema, resource tables, `<quick_selection>` defaults, RTD example `.mex`, and the target `.mex`. See `references/authoring-procedure.md`. |
| Per-driver programmatic emitters | `scripts/build_peripherals.py` - reference emitter for the six standard drivers with `CommonPublishedInformation` and correct enum casing. |
| Splice into target `.mex` | `scripts/splice_peripherals.py` - replaces any prior peripherals block. |
| Structural diagnostics | `scripts/dump_resources.py`, `scripts/inspect_required.py`, `scripts/compare_children.py`, `scripts/find_bad_names.py`. |
| Honest validation gate | `scripts/check_problems.bat` (Windows) / `scripts/check_problems.sh` (Linux/macOS) - runs the launcher with `-Load ... -HeadlessTool Peripherals -Enable -ShowProblems`, captures stderr to a file for the noise filter to consume. |
| Optional code generation | Run `s32ct-generate-code` Peripherals `ExportSrc` after validation is clean; verify each named controller appears in its `.ecvd`. |

## Quickstart

1. Confirm the `.mex` already has the Pins entries for the peripherals
   to configure (use `s32ct-pins-author-mex` first if not).
2. Resolve MCU / package / platform-SDK / RTD version; auto-discovery
   is available at MCP startup. See `s32ct-distributions`.
3. Follow the 7-step recipe:
   1. Inventory routed peripherals from the existing Pins entries.
   2. Per driver: look up schema (`.component`), enums
      (`resource_tables/[RTD/]<Driver>.xml`), defaults
      (`<quick_selection>`), shape (RTD example `.mex`).
   3. Programmatically emit one `<instance>` per driver into
      `peripherals_block.xml` (use `scripts/build_peripherals.py` as
      the template).
   4. Splice into the target `.mex`
      (`scripts/splice_peripherals.py`).
   5. Validate - stage the `.mex`, then run
      `scripts/check_problems.bat <mex> Peripherals` (Windows) or
      `sh scripts/check_problems.sh <mex> Peripherals` (Linux/macOS),
      and filter the noise.
   6. Iterate until the filtered stderr is empty (3-5 rounds is
      typical the first time).
   7. Optional: run `s32ct-generate-code` Peripherals `ExportSrc`.
4. Emit the Markdown report: driver instance table, validation result,
   code-generation result, known caveats. Full input/output schema and
   verification-scope caveats in `references/authoring-procedure.md`.

Full driver-specific edits (XML shapes, ModuleIds, enum casings, the
10 critical pitfalls) live in `references/per-driver-reference.md`.
Read that file before writing the first `<setting>` for any driver you
have not previously hand-authored.

## Configuration

Placeholders resolved from the active MCP install:

- `<MCU>` - e.g. `S32K312`, `S32G274A`, `S32M276`.
- `<PACKAGE>` - e.g. `S32K312_172HDQFP`, `S32G2_BGA257`.
- `<PLATFORM_SDK>` - e.g. `PlatformSDK_S32K3`, `PlatformSDK_S32G2`.
- `<RTD_VERSION>` - e.g. `TS_T40D34M70I1R0`, `TS_T40D11M40I0R0`.
- `<S32DS_INSTALL>` / `<S32CT_INSTALL>` - auto-discovered by the MCP
  at startup (both `desktop` and `integrated_s32ds` distributions
  supported). See `s32ct-distributions`.

Data reachable on disk:

- `<S32DS_INSTALL>/eclipse/mcu_data/components/<PLATFORM_SDK>/<driver_folder>/<driver_folder>.component`
- `<S32DS_INSTALL>/eclipse/mcu_data/processors/<MCU>/<PLATFORM_SDK>/<PACKAGE>/resource_tables/[RTD/]<Driver>.xml`
- `<S32DS_INSTALL>/S32DS/software/<PLATFORM_SDK>/RTD/<Driver>_<RTD_VERSION>/examples/S32DS/<MCU_FAMILY>/<Example>/<Example>.mex`

## Guardrails

- **Scope.** Read-only: `signal_configuration.xml`, `.component`
  files, `resource_tables/*.xml`, RTD example `.mex`, the
  `<MCU>_default.mex` template. Read-write: the user's `.mex` and any
  output folders named by the user. No network, no telemetry, no
  hardware, no registers.
- **Destructive actions.** Splice replaces any prior peripherals
  block in the target `.mex` - the user should have chosen an
  `output_path` deliberately. Freshly generate a UUID v4 for every new
  `<instance>`; the example's UUID collides otherwise.
- **Refuse and escalate.** If the requested driver has a shipped RTD
  example, prefer `s32ct-peripherals-graft-mex` and stop. If the
  Pins-tool entries are missing, hand off to `s32ct-pins-author-mex`
  first. Never report "validated" without having parsed the filtered
  stderr; the exit code lies.

## Validation loop

`-ShowProblems` returns `exit_code = 0` even when the Problems View
contains 25 errors. The MCP wrapper's `stderr_tail` field is also
truncated at ~3 KB. Trust the captured text, not the exit code, and
not `stderr_tail`.

1. **Windows only: copy the `.mex` to a no-space path.** `cmd`'s
   redirection parser fails on paths containing spaces inside quoted exe
   paths. POSIX shells quote correctly, so `check_problems.sh` accepts
   any path and stages under `$PROBE_DIR`
   (default `${TMPDIR:-/tmp}/s32ct_probe_out`).

2. **Run the launcher with explicit stderr capture** via
   `scripts/check_problems.bat` (Windows) or
   `scripts/check_problems.sh` (Linux/macOS). See either script for the
   canonical invocation; both take the same arguments and write the same
   capture files. `<LAUNCHER>` is `toolsc[.exe]` on `desktop` and
   `s32dsc[.exe]` on `integrated_s32ds` - see `s32ct-distributions`.

3. **Filter framework noise.** A catalog of the ~7 SEVERE lines that
   appear on any clean project (`Cannot get container for IPath ...`,
   `SerDes Config Tool` script warning, `derefAsr` TypeErrors,
   `Siul2_Port InfoSetting` messages, `Port_GetNumOfPinConfig` /
   `getTotalNumOfChans` / `getTotalNumOfGroups` `getChildren`/
   `getChildById` errors) lives in
   `references/error-decision-tree.md`. Drop those before
   interpreting the output.

4. **Pass criterion.** After filtering, the remaining `SEVERE: [TOOL]`
   and `SEVERE: [Generation` lines must be empty. Real problems look
   like:

   ```
   SEVERE: [TOOL] The resource "Can_43_FLEXCAN" from functional group
   "BOARD_InitPeripherals" has the following error: <human-readable text>.
   ```

5. **Never report "validated"** without executing step 4. When a real
   line survives, pattern-match against
   `references/error-decision-tree.md` before changing anything else.

## Out of scope

- Pins, Clocks, DCD, IVT, eFUSE, GTM, QuadSPI, FFC tool authoring.
- Application-level containers (SpiChannel/Job/Sequence,
  CanHardwareObject filters, UartDma refs, LinClockRef alternates,
  AdcGroupDefinition cross-refs) - see `s32ct-peripherals-info`.
- Driver C-source generation - `s32ct-generate-code` Peripherals
  `ExportSrc`.
- Adding `McuClockReferencePoint_*` entries so
  `LinClockRef`/`CanCpuClockRef` refs resolve at runtime - hand off to
  `s32ct-clocks-info`.
- Using the MCP `s32ct-peripherals-facade` wrapper for `-ShowProblems`
  (its `stderr_tail` is truncated and hides errors).

## See Also

- `references/per-driver-reference.md` - verified XML shapes for Spi,
  Uart, Can_43_FLEXCAN, Lin_43_LPUART_FLEXIO, Adc, Pwm; surprise enum
  strings; ModuleIds; the 10 critical pitfalls.
- `references/error-decision-tree.md` - `SEVERE: [TOOL]` / `SEVERE:
  [Generation` patterns mapped to fixes, plus the framework-noise catalog
  (Appendix) listing the ~7 SEVERE lines that appear on any clean project
  and must be filtered before interpreting output.
- `references/authoring-procedure.md` - the 5-source rule, 7-step
  recipe, inputs, outputs, verification scope, safety classification.
- `s32ct-peripherals-graft-mex` - faster sibling when an RTD example
  exists; prefer it whenever available.
- `s32ct-peripherals-info` - application-level container authoring.
- `s32ct-pins-author-mex`, `s32ct-pins-info` - Pins-tool skills.
- `s32ct-clocks-info` - clock reference points.
- `s32ct-generate-mex-config` - generic clone-and-patch operator.
- `s32ct-generate-code` - code generation after green validation.
- `s32ct-cli` - generic CLI wrapper.
- `s32ct-distributions` - launcher and prefix selection.
