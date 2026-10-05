---
name: s32ct-peripherals-graft-mex
description: >
  Grafts one or more Peripherals-tool driver instances (`Spi`, `Uart`,
  `Can_43_FLEXCAN`, `Lin_43_LPUART_FLEXIO`, `Adc`, `Pwm`, `Wdg_43_*`,
  `Icu`, `Gpt`, `Mcl`, `Eth_43_GMAC`, `I2c`, ...) into an existing
  S32 Configuration Tools `.mex` by lifting the `<instance>` block from
  the matching RTD example `.mex` and surgically adapting hw-channel
  selectors and cross-references. Use for any S32 family MCU with any
  RTD / Platform SDK version. Trigger phrases: "configure Peripherals
  tool", "add Spi/Uart/Can/Lin/Adc/Pwm instance", "extend my .mex with
  driver X", "wire up driver configuration on top of my Pins routing",
  "the Peripherals tool is not generating C sources", "graft an
  <instance> block from an RTD example", "my driver instance fails
  validation with value not available". Reaches a validating `.mex` in
  3-6 iterations instead of 25+ when an RTD example exists; hand off to
  `s32ct-peripherals-author-mex` when it does not. File types: `.mex`,
  RTD example `.mex`, `.component`.
license: LA_OPT_Online Code Hosting NXP_Software_License
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(python:*), Bash(cmd:*), Bash(sh:*)
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-distributions, s32ct-pins-author-mex]'
  tags: '[s32ct, configuration-tools, graft, mex-authoring, headless, peripherals, configuration]'
---

# S32CT Peripherals - Graft `.mex` (lift and adapt)

Lift the working `<instance>` block for a driver straight out of the
matching NXP RTD example `.mex`, surgically change the small number of
fields that must differ for the user's board (hw-channel selector,
instance name, controller count), splice into the target `.mex`, then
run a systematic sanitize + validate loop. Trades authoring flexibility
for speed: 3-6 validator rounds instead of 25+, because the RTD example
is already validated by NXP and its XML shape, cross-reference paths,
`CommonPublishedInformation`, and enum casing are guaranteed accepted.

## When to use

- Use for: adding driver `<instance>` blocks to a Pins-populated `.mex`
  when a matching RTD example ships on disk; extending a `.mex` with
  several drivers at once (cost is roughly-flat because sanitize is a
  global pass); reaching a validating `.mex` quickly, then fine-tuning
  individual settings.
- Do **not** use this skill for: drivers with no shipped RTD example (custom drivers,
  `Eth_43_GMAC` on small parts) - use `s32ct-peripherals-author-mex`
  instead; Pins / Clocks / DCD / IVT / eFUSE / QuadSPI / GTM / FFC
  tools; generating driver C sources (use `s32ct-generate-code` after
  validation is clean).

## Available Capabilities

| Capability | Notes |
|---|---|
| Discover matching RTD example | Auto-picks the closest MCU-family variant (e.g. S32K344 example for an S32K312 target). See `scripts/discover.py`. |
| Extract example `<instance>` blocks | `scripts/extract_examples.py` lifts `<instance ... type_id="X">...</instance>` XML fragments verbatim. |
| Splice with re-UUID | `scripts/splice.py` inserts before `</instances>`, handles balanced-array nesting and indent, regenerates instance-level UUIDs. |
| Systematic sanitize (idempotent) | `scripts/sanitize.py` redirects `/Mcu/.../McuClockReferencePoint_*` refs, self-closes `<array>` bodies referencing absent drivers (typically `/Mcl/`), blanks singleton dangling refs. |
| Honest validation gate | `scripts/check_problems.bat` (Windows) or `scripts/check_problems.sh` (Linux/macOS) + `scripts/filter_problems.py` run the launcher with `-HeadlessTool <Tool> -ShowProblems`, capture stderr to a file, apply the 9-pattern noise filter, count real problems. |
| Multi-driver in one call | `drivers` array accepts several entries per invocation; splice + sanitize is one pass. |

## Quickstart

Follow the canonical 7-step workflow. Full detail with per-step
scripts, common failure modes, and iteration expectations lives in
`references/iteration-playbook.md`.

1. **Inventory** the target `.mex`:
   `python scripts/inventory.py <project_path>` - lists existing
   `<instance>` blocks and `McuClockReferencePoint_*` names.
2. **Discover** the RTD example per driver:
   `python scripts/discover.py --driver Spi --mcu S32K312 --sdk PlatformSDK_S32K3`.
3. **Lift** the example's `<instance>` block:
   `python scripts/extract_examples.py --driver Spi --example <path> --out work/Spi_instance.xml`. Repeat per driver.
4. **Adapt** hw-channel selectors and cross-refs per driver. Consult
   `references/per-driver-gotchas.md` for the concrete edits.
   Regenerate the instance-level UUID.
5. **Splice** into the target `.mex`:
   `python scripts/splice.py --project <project_path> --out <output_path> --instances work/*.xml`.
6. **Sanitize** cross-references (idempotent):
   `python scripts/sanitize.py --mex <output_path>`.
7. **Validate + loop**. Stage the `.mex` in the probe directory, run the
   check wrapper, filter, count. Repeat 3-6 times.

Windows (`cmd.exe`) - a no-space staging path is required because `cmd`
mishandles redirection when a quoted path contains spaces:

```bat
copy /Y <output_path> C:\tmp_mex\probe.mex
scripts\check_problems.bat probe Peripherals
python scripts/filter_problems.py --stderr C:\tmp_mex\probe_Peripherals_stderr.txt
scripts\check_problems.bat probe Pins
python scripts/filter_problems.py --stderr C:\tmp_mex\probe_Pins_stderr.txt
```

Linux / macOS (`sh`/`bash`) - `check_problems.sh` is the POSIX
counterpart and takes the same arguments:

```sh
export S32CT_PROBE_DIR="${TMPDIR:-/tmp}/s32ct_probe"
export S32CT_INSTALL=/opt/nxp/S32ConfigTools.<release>
mkdir -p "$S32CT_PROBE_DIR"

cp -f <output_path> "$S32CT_PROBE_DIR/probe.mex"
sh scripts/check_problems.sh probe Peripherals
python3 scripts/filter_problems.py \
    --stderr "$S32CT_PROBE_DIR/probe_Peripherals_stderr.txt"
sh scripts/check_problems.sh probe Pins
python3 scripts/filter_problems.py \
    --stderr "$S32CT_PROBE_DIR/probe_Pins_stderr.txt"
```

When a filtered line survives, map it to a fix via
`references/error-decision-tree.md`, apply, re-run sanitize, re-check.

## Configuration

- Launcher: `toolsc.exe` (desktop) or `s32dsc.exe` (integrated_s32ds),
  auto-discovered at MCP startup. See `s32ct-distributions`.
- Path discipline: on Windows, `cmd`'s stderr redirection fails when any
  path on the command line contains a space. Copy the `.mex` to a
  no-space path (e.g. `C:\tmp_mex\<name>.mex`) before validating. POSIX
  shells quote correctly, so `check_problems.sh` has no such
  restriction; it stages under `$S32CT_PROBE_DIR`
  (default `${TMPDIR:-/tmp}/s32ct_probe`).
- RTD example location:
  `<S32DS_INSTALL>/S32DS/software/<PLATFORM_SDK>/RTD/<Driver>_<RTD_VER>/examples/S32DS/<MCU_FAMILY>/<example_dir>/<example>.mex`.
- Driver request schema and hw-channel selector fields live in
  `references/per-driver-gotchas.md`.

## Guardrails

- **Scope.** Writes the new `.mex` (and propagates
  `ClockConfigurationMappings.txt` if present alongside) plus temp
  probe copies under a no-space directory. Reads but never writes RTD
  example `.mex`, `.component` schemas, `resource_tables/*.xml`.
  Validation invocations are read-only on the filesystem; they spawn
  one `toolsc.exe` child process per pass. No target hardware, no
  FreeMASTER, no registers.
- **Destructive actions.** Refuse to overwrite the target `output_path`
  unless `overwrite=true`. Never modify RTD example files or component
  schemas. Do not "improve" the lifted block while adapting - keep the
  single-purpose adaptation clean so bisection remains cheap.
- **Refuse and escalate.** If no RTD example exists for a requested
  driver on the target family, stop and hand off to
  `s32ct-peripherals-author-mex`. If a path with spaces is unavoidable,
  copy first; do not attempt to work around `cmd`'s parser.

## Validation loop

The only honest gate: `toolsc.exe` exits `0` almost regardless of how
many problems it logged. Trust the captured text, not the exit code.

1. Copy the target `.mex` to a no-space path.
2. Run `scripts/check_problems.bat <name> <Tool>` on Windows, or
   `scripts/check_problems.sh <name> <Tool>` on Linux/macOS - it invokes
   the launcher with `-Load ... -HeadlessTool <Tool> -Enable
   -ShowProblems` and redirects stdout / stderr to files under the probe
   directory (`C:\tmp_mex\` or `$S32CT_PROBE_DIR`).
3. Run `scripts/filter_problems.py --stderr <captured_stderr>` - it
   strips the 9 framework-noise patterns (`Cannot get container for
   IPath`, `derefAsr`, `Port_GetNumOfPinConfig`, `getTotalNumOfChans`,
   `getTotalNumOfGroups`, `getChildById`, `Missing right bracket`, the
   `SerDes` codegen note, and the `Siul2_Port ... InfoSetting` note).
4. Zero surviving lines is pass. Anything else is real - consult
   `references/error-decision-tree.md`, apply the mapped fix, re-run
   `sanitize.py`, and re-validate.
5. Repeat the loop for Pins (regression check) after Peripherals is
   clean.

Plan for 3-6 rounds on the first run with a new driver mix; on repeat
runs for the same MCU one or two rounds usually suffice.

## Out of scope

- Populating the Pins tool (that is `s32ct-pins-author-mex`).
- Populating Clocks, DCD, IVT, eFUSE, QuadSPI, GTM, FFC tools.
- Adding `McuClockReferencePoint_*` entries so redirected clock refs
  resolve to real clocks at runtime (hand off to `s32ct-clocks-info`).
- Application-level driver containers (`SpiChannel`/`Job`/`Sequence`,
  `CanHwFilter` masks, `AdcGroupDefinition` cross-refs, `LinSchedule`
  tables) - project-specific; see `s32ct-peripherals-info`.
- Generating driver C sources (that is `s32ct-generate-code` after
  validation is clean).

## See Also

- `references/per-driver-gotchas.md` - per-driver adaptation rules
  (Spi, Uart, Can, Lin, Adc, Pwm): concrete enum casings, container
  path quirks, the "empty vs absent" subtleties.
- `references/error-decision-tree.md` - map each `SEVERE: [TOOL]` /
  `SEVERE: [Generation` message pattern to a targeted fix.
- `references/iteration-playbook.md` - step-by-step recipe for rounds
  1-N; expected error class per round.
- `references/cross-reference-map.md` - systematic list of
  cross-reference families that fail by default (`/Mcl/`,
  `/Mcu/.*_CLK`, `BOARD_BootClockRUN`) and the canonical redirect for
  each.
- `s32ct-peripherals-author-mex` - sibling; authoring-from-scratch
  path when no RTD example is available.
- `s32ct-peripherals-info` - schema and resource-table lookup for
  application-level containers.
- `s32ct-pins-author-mex` - prerequisite; produces the Pins-populated
  `.mex`.
- `s32ct-clocks-info` - add `McuClockReferencePoint_*` entries so
  redirected refs resolve at runtime.
- `s32ct-generate-mex-config` - lower-level clone-and-patch operator.
- `s32ct-generate-code` - emit C sources once validation passes.
- `s32ct-distributions` - launcher and prefix selection.
