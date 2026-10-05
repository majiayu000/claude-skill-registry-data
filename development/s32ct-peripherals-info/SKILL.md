---
name: s32ct-peripherals-info
description: >
  Read-only inspector for the S32 Configuration Tools Peripherals tool.
  Answers what and how a peripheral (driver component) can be configured
  for any S32 family MCU (S32K1, S32K3, S32G, S32R, S32M, S32Z, S32E, S32S,
  S32N) and any installed RTD / Platform SDK, by parsing the on-disk
  `.component` descriptors and per-package `resource_tables/*.xml`
  enumerations shipped with S32 Design Studio. Trigger phrases: "peripheral
  configuration", "driver configuration", "RTD component settings",
  "configure CAN baud rate", "ADC channels available", "list valid LPSPI
  instances", "what values can <setting> take", "quick selection presets",
  "AUTOSAR mode vs IP mode", "how does a configured peripheral land in the
  .mex <instance> block". Never answers from memory - always cites the
  parsed source files. Never edits `.mex`, target memory, or generated
  code.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  tags: '[s32ct, peripherals, knowledge, discovery, read-only, configuration]'
---

# S32CT Peripherals Info (read-only inspector)

Looks up *what* and *how* a peripheral can be configured in the S32
Configuration Tools Peripherals tool by parsing two on-disk authoritative
sources shipped with S32 Design Studio: (1) the peripheral's `.component`
descriptor - the schema (modes, config sets, structs, arrays, settings,
quick-selection presets, dynamic-enum *references*); and (2) the
per-package `resource_tables/<Driver>.xml` (and `.../RTD/<Driver>.xml`)
files - the package-specific *allowed values* for every `<dynamic_enum>`.
Post 16->5 refactor, sibling skills invoke via the unified
`nxp_s32ct_execute_action` dispatcher; this inspector remains a pure read.

## When to use

Use this skill when:
- Discovering which parameters, sub-containers and quick-selection presets
  a peripheral exposes in the Peripherals tool.
- Resolving a `<dynamic_enum ref="..."/>` in a `.component` to its
  package-specific allowed-value list (from `resource_tables/<Driver>.xml`).
- Explaining the mapping between a `.component` file and the `<instance>`
  block it produces inside a `.mex` project.
- Locating the official RTD reference manual PDF for a peripheral.
- Diagnosing why a parameter or value is missing / rejected in the
  Peripherals tool (wrong RTD version, wrong MCU package, peripheral not
  installed, dynamic-enum value not present on this package).

Do **not** use this skill for:
- Editing a `.mex` - use `s32ct-generate-mex-config` or
  `s32ct-peripherals-facade` (= `nxp_s32ct_execute_action(action_name="s32ct.configure_peripherals", params={...})`).
- Generating driver code - use `s32ct-generate-code` (=
  `nxp_s32ct_execute_action(action_name="s32ct.generate_code", params={...})`).
- Anything write-side or target-mutating.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Query | Peripheral overview | `peripheral_name="Mcu"` (no `query`) |
| Query | Specific parameter | `peripheral_name="Mcu", query="McuTimeout"` |
| Query | Resolve `<dynamic_enum>` | `peripheral_name="Spi", query="SpiPhyUnitMapping", package="S32K312_172HDQFP"` |
| Query | Locate RTD PDF | `peripheral_name="Mcu", include_doc_link=true` |
| Query | `.mex` `<instance>` shape | `peripheral_name="Port", include_mex_shape=true, mcu="S32K312"` |
| Reference | Per-driver inspection & resolution | `references/per-driver-inspection.md` |
| Reference | Authoring an `<instance>` block | `references/authoring-instance-reference.md` |

## Post 16->5 tool mapping

| Sibling skill id | MCP call to use |
|---|---|
| `s32ct-cli` | `nxp_s32ct_execute_action(action_name="s32ct.configure_cli", params={...})` |
| `s32ct-peripherals-facade` | `nxp_s32ct_execute_action(action_name="s32ct.configure_peripherals", params={...})` |
| `s32ct-generate-code` | `nxp_s32ct_execute_action(action_name="s32ct.generate_code", params={...})` |

## Quickstart

1. Overview of a peripheral (returns modes, top-level config sets, quick
   selections, sub-containers):
   ```yaml
   peripheral_name: Mcu
   platform_sdk: PlatformSDK_S32K3
   ```

2. Look up a specific parameter and its default:
   ```yaml
   peripheral_name: Mcu
   query: McuTimeout
   ```

3. Resolve a `<dynamic_enum>` to package-specific allowed values:
   ```yaml
   peripheral_name: Spi
   query: SpiPhyUnitMapping
   mcu: S32K312
   package: S32K312_172HDQFP
   ```
   Returns `LPSPI_0..LPSPI_6` on S32K312_172HDQFP (from
   `resource_tables/Spi.xml`). Different packages may expose fewer.

4. Get the official PDF reference:
   ```yaml
   peripheral_name: Mcu
   include_doc_link: true
   ```
   Returns absolute path under
   `<S32DS_INSTALL>/S32DS/software/<platform_sdk>/RTD/Mcu_TS_.../doc/RTD_MCU_UM.pdf`.

5. See how the peripheral lands in a `.mex`:
   ```yaml
   peripheral_name: Port
   include_mex_shape: true
   mcu: S32K312
   ```

See `references/per-driver-inspection.md` for the full inputs table,
resolution algorithm, resource-table anatomy, worked examples, and the
error-message catalog.

## Inputs (summary)

| Name | Required | Default |
|------|----------|---------|
| `peripheral_name` | yes | - |
| `platform_sdk` | no | sole folder under `mcu_data/components/`, or matched by `mcu` family |
| `mcu` | no | sole processor installed for that `platform_sdk` |
| `package` | no | sole package under `<mcu>/<platform_sdk>/` |
| `s32ds_install` | no | auto-discovered active install (`desktop` or `integrated_s32ds`) |
| `query` | no | if empty, returns structured overview |
| `include_mex_shape` | no | `false` |
| `include_doc_link` | no | `true` |
| `include_resource_table` | no | `true` (or implied by `query`) |

## Output

A Markdown string with four sections:

1. **Resolved sources** - absolute paths to the `.component` file, the
   matching `resource_tables/<Driver>.xml` (and/or `RTD/<Driver>.xml`)
   when used, the doc PDF (when `include_doc_link`), and the reference
   `.mex` (when `include_mex_shape`).
2. **Answer** - human-readable response.
3. **Evidence** - short XML excerpts (`<config_set>`, `<quick_selection>`,
   `<set id=...>`, `<mode>`, `<dynamic_enum>`, matching `<array>` /
   `<setting>` entries from the resource table) quoted verbatim.
4. **References** - PDF path and `<instance>` excerpt if requested.

## Configuration

```yaml
# Idempotent, filesystem-read only. No side effects.
# Case-sensitive on disk: peripheral folder names follow RTD naming
# (e.g. Can_43_FLEXCAN, Lpuart_Uart, Wdg_43_Instance1, Qspi_Ip).
```

## Guardrails

**Scope** - Read-only. Filesystem reads and XML parsing only. Does not
modify target variables, system memory, project files, `.mex`
configurations, or any installed tooling. Idempotent.

**Refuse-and-escalate** - Returns clear, actionable errors (never raises)
when the `.component` file, platform SDK, MCU, package, or dynamic-enum
reference cannot be resolved. Each error lists the checked absolute path
and either the closest matches or the list of installed alternatives
(from the on-disk `dir` listing). Downstream authoring must be routed
to a write-side skill:
- Edit a `.mex` -> `s32ct-generate-mex-config` or
  `s32ct-peripherals-facade`.
- Generate code -> `s32ct-generate-code`.
- Board-level orchestration -> `s32ct-peripherals-author-mex`.

**Data authority** - Two authoritative sources. Schema lives in the
`.component` XML; package-specific allowed values for `<dynamic_enum>`
live in the per-package resource tables. A correct answer cites both.
Never answer from memory; RTD versions, MCU variants and package
pinouts differ.

## Validation loop

1. `<s32ds_install>/eclipse/mcu_data/components/<platform_sdk>/` exists;
   otherwise list installed SDKs.
2. `<peripheral_name>/<peripheral_name>.component` exists under that
   SDK; otherwise list nearest sibling folders (case-sensitive).
3. When `mcu` and `package` are needed:
   `mcu_data/processors/<mcu>/<platform_sdk>/<package>/` exists;
   otherwise list available MCUs / packages.
4. Component XML parses without error.
5. Every `<dynamic_enum ref="Driver.Path"/>` in the filtered result
   resolves against `resource_tables/<Driver>.xml` (or `.../RTD/<Driver>.xml`).
6. When `include_doc_link=true`, `doc/index.md` parses and its
   `component-doc-link` resolves to an existing PDF.
7. When `include_mex_shape=true`, the bundled `<MCU>_default.mex` exists
   (fall back gracefully with a "how to generate one" pointer).
8. Pass criterion: output contains the four sections above and every
   quoted excerpt has an absolute source path.

## Out of scope

- Writing or patching `.mex` files.
- Applying settings to a project or running the Peripherals CLI.
- Generating source code, headers, or drivers.
- Modifying installed RTD / Platform SDK content.
- Any interaction with the live target device.

## See Also

- `references/per-driver-inspection.md` - Full inspection procedure,
  resource-table anatomy, `<dynamic_enum>` resolution algorithm, common
  driver families, error-message catalog, and worked examples.
- `references/authoring-instance-reference.md` - Rules for adding a new
  `<instance>` block to a `.mex` (attribute mapping, template mirroring,
  6-item pre-insertion checklist, end-to-end Wdg_43_Instance1 example).
  Load this whenever the consumer is about to patch a `.mex`.
- Related skills:
  - `s32ct-pins-info`, `s32ct-clocks-info` - sibling read-only
    inspectors for the Pins and Clocks tools.
  - `s32ct-generate-mex-config`, `s32ct-peripherals-facade`,
    `s32ct-peripherals-author-mex` - write-side authoring / apply.
  - `s32ct-generate-code`, `s32ct-cli` - code generation and generic
    dispatcher.
  - `s32ct-distributions` - `desktop` vs `integrated_s32ds` install
    layout and where the MCP auto-discovers each.
