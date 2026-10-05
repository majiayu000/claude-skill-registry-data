---
name: s32ct-clocks-info
description: >
  Looks up what clocks, oscillators, PLLs, dividers, selectors, gates,
  peripheral clock outputs and power modes are configurable on a given
  MCU/RTD/package combination, and how each is configured in the S32
  Configuration Tools Clocks tool. Triggers on questions about clock
  configuration, clock tree, oscillator setup (FXOSC/SXOSC/FIRC/SIRC), PLL
  setup, peripheral clock frequencies, clock dividers, clock selectors,
  gating, clock outputs, power modes (DRUN/STANDBY/...), or anything visible
  inside the Clocks tool of S32 Configuration Tools / S32 Design Studio for
  any S32-family MCU and any installed RTD / Platform SDK. Use before
  authoring or editing the <clocks> block of a .mex, before calling the
  Clocks CLI, or to diagnose why a clock setting is missing/invalid for a
  specific package or RTD version. Read-only.
allowed-tools: Read, Grep, Glob
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: "s32ct-distributions"
  tags: '[s32ct, configuration-tools, knowledge, discovery, clocks, read-only]'
---

# S32CT Clocks Info

Look up *what* and *how* the clock tree of a specific
`(MCU, RTD, package)` combination can be configured in the S32
Configuration Tools Clocks tool, by parsing the XML data model shipped
with the installed Real-Time Drivers / Platform SDK. Read-only -
answers questions about clock sources, PLLs, dividers, selectors, gates,
peripheral clock outputs, register writes and power modes. Companion of
`s32ct-pins-info` and `s32ct-peripherals-info` for the Clocks tool.

## When to use
- Use for: enumerating available clock sources, dividers, selectors,
  gates, fractional dividers, peripheral clock outputs; discovering the
  configurable attributes and legal values of a clock module; locating
  the register / bit-field that the Clocks tool writes for a given
  choice; mapping `clock_source -> selector -> divider -> gate ->
  peripheral_clock_output`; diagnosing why a setting is missing;
  authoring or validating the `<clocks>` block of a `.mex`.
- Do **not** use this skill for: modifying a `.mex` (use `s32ct-clocks-graft-mex`,
  `s32ct-generate-mex-config`, or the Clocks CLI); generating
  `Clock_Ip_Cfg.[ch]` driver code (use `s32ct-generate-code` with
  `tool_name="Clocks"`); pin or peripheral queries (use
  `s32ct-pins-info` / `s32ct-peripherals-info`).

## Available Capabilities

This skill is read-only. The capabilities below only inspect the Clocks
data model; none of them modify a `.mex`, generate code, or execute a
CLI.

| Type | Name | Invocation |
|------|------|------------|
| Query | Clock-tree overview | `mcu="S32K312", package="S32K312_172HDQFP"` |
| Query | Resolve a clock point / frequency | `query="CAN_PE_CLK"` |
| Reference | Full XML anatomy and filter schema | `references/clock-inspection.md` |
| Reference | Worked query examples | `references/examples.md` |
| Data | `<S32DS>/eclipse/mcu_data/processors/<mcu>/<platform_sdk>/clocks/<package>/` | The per-package XML data model consumed by this skill. |

## Post 16->5 tool mapping

Write-side and CLI actions belong to the sibling skills listed below.
They are documented here only so the agent knows where to hand off -
this skill never invokes them.

| Sibling skill id | MCP call to use |
|---|---|
| `s32ct-cli` | `nxp_s32ct_execute_action(action_name="s32ct.configure_cli", params={...})` |
| `s32ct-clocks-facade` | `nxp_s32ct_execute_action(action_name="s32ct.configure_clocks", params={...})` |
| `s32ct-generate-code` | `nxp_s32ct_execute_action(action_name="s32ct.generate_code", params={...})` |

## Quickstart

1. Resolve paths from `mcu`, `package`, and `platform_sdk` (defaults to
   the sole subfolder under `mcu_data/processors/<mcu>/` when exactly one
   exists):

   ```
   <S32DS_INSTALL>/eclipse/mcu_data/processors/<mcu>/<platform_sdk>/clocks/<package>/
   ```

2. Overview of the data model for a package:

   ```jsonc
   { "mcu": "S32K312", "package": "S32K312_172HDQFP",
     "include_register_writes": false }
   ```

   Returns the discovered XML files, clock sources, output-signal counts,
   power modes, and top-level `<configuration_element>` entries.

3. Modes and register writes for one module:

   ```jsonc
   { "mcu": "S32K312", "package": "S32K312_172HDQFP",
     "filter": { "module": "FXOSC" } }
   ```

4. What feeds a peripheral clock:

   ```jsonc
   { "mcu": "S32K312", "package": "S32K312_172HDQFP",
     "filter": { "output": "LPUART2_CLK" } }
   ```

5. Lookup by register bit-field:

   ```jsonc
   { "mcu": "S32K312", "package": "S32K312_172HDQFP",
     "filter": { "register": "FXOSC::CTRL", "bit_field": "OSCON" } }
   ```

More payloads in `references/examples.md`. Enumeration internals and the
XML/.mex mapping are in `references/clock-inspection.md`.

## Configuration

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mcu` | string | yes | Folder name under `mcu_data/processors/`. Case-sensitive. |
| `package` | string | yes | Folder name under `clocks/`. Case-sensitive. |
| `platform_sdk` | string | no | Defaults to the sole subfolder when exactly one exists. |
| `s32ds_install` | string | no | Override of the S32CT install root. MCP auto-discovers `desktop` or `integrated_s32ds` at startup - see `s32ct-distributions`. |
| `query` | string | no | Free-form question, fuzzy-matched. |
| `filter` | object | no | Structured filter (see `references/clock-inspection.md`). AND-combined. |
| `include_register_writes` | bool | no | Default `true`. Include `<assign register="..." bit_field="..."/>` rows. |
| `include_constraints` | bool | no | Default `true`. Include `<constraint>` / `<enable>` rules. |
| `max_results` | int | no | Default `200`. |

## Guardrails

**Scope.** Reads files only from
`<S32DS_INSTALL>/eclipse/mcu_data/.../clocks/<package>/`. Does not modify
any project, `.mex`, target memory, or system state. Idempotent and safe
to call multiple times.

**Destructive actions.** None. Purely read-only.

**Refuse-and-escalate.** Refuses when required MCU/SDK/package
directories are missing, when the clocks directory contains no XML, or
when a filter references an unknown key - returns an actionable error
listing available alternatives. Never invents `<configuration_element>`
ids, `<item>` values, register names, or bit-field names; quotes only
what is present in the XML.

## Validation loop

1. Resolve `mcu` -> `platform_sdk` -> `package` paths and confirm each
   directory exists. On failure, return the error template listing
   available subfolders (`s32ct-clocks-info` never raises).
2. Discover `.xml` files by listing the clocks directory. Ignore `.dsn`
   (binary GUI diagram) and other non-XML assets.
3. Parse each `.xml`. The root may be `<clocks:top_level>`,
   `<clocks:component>`, or `<clocks:power_modes>` - strip the `clocks:`
   prefix before iterating, otherwise namespace matching silently skips
   every child.
4. Build the in-memory index keyed by module id, `<clock_source id>`,
   `<output_clock_signal id>`, `<input_clock_signal id>`,
   `<configuration_element id>`, `<power_mode id>`, and every
   `<assign register bit_field/>`.
5. Apply `filter` (indexed fast path) and/or `query` (fuzzy fallback);
   walk matched nodes and emit verbatim XML excerpts. Never paraphrase
   attribute values.
6. **Pass** = every filter key resolves and the answer includes verbatim
   `<configuration_element>` / `<assign>` / `<clock_source>` /
   `<map_output>` / `<power_mode>` / `<constraint>` evidence, capped at
   `max_results` with a truncation note when needed. **Fail** = any
   filter key is unknown or matches nothing - return the "closest
   matches" error.

## Out of scope

- Modifying `.mex` files, driver sources, or any installed tooling.
- Pin-tool and Peripherals-tool queries (use `s32ct-pins-info` /
  `s32ct-peripherals-info`).
- Executing code on target hardware or reading target memory.
- Parsing `.dsn` GUI vector diagrams for authoring data.
- Guessing values not present in the XML - RTD versions and MCUs
  diverge, only the XML is authoritative.

## See Also

- `references/clock-inspection.md` - the XML data-model layout
  (`TOP.xml`, `FXOSC.xml`, `SXOSC.xml`, `MODULE_CLOCKS.xml`,
  `POWER_MODES.xml`), schema element table, filter schema, output
  format, behaviour rules, the exact XML <-> `.mex` mapping used when
  authoring the `<clocks>` block, the pre-insertion checklist, hand-off
  chain, and full error-message templates.
- `references/examples.md` - worked example payloads for the five most
  common query patterns (package overview, single-module details,
  peripheral-clock trace, register-bit lookup, power modes).
- Related skills: `s32ct-pins-info` (Pins-tool data model),
  `s32ct-peripherals-info` (Peripherals-tool data model),
  `s32ct-clocks-graft-mex` (write-side: apply presets / tweak / lift),
  `s32ct-generate-mex-config` (bake settings into a `.mex`),
  `s32ct-generate-code` (`tool_name="Clocks"` - emit
  `Clock_Ip_Cfg.[ch]` and `Clock_Ip_Cfg_Defines.h`),
  `s32ct-distributions` (install-root discovery).
