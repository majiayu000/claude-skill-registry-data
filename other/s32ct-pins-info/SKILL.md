---
name: s32ct-pins-info
description: >
  Looks up what pins, pads, signals, signal routings, pin multiplexing,
  pin properties and package pinouts are available in the S32 Configuration
  Tools Pins-tool data model for any NXP S32-family MCU (S32K1, S32K3,
  S32G2/G3, S32M, S32R, S32E, S32Z, S32S, ...) on any installed RTD / Platform
  SDK and any package variant. Triggers on "pin configuration", "pin info",
  "which pins exist on package X", "which pins can carry signal Y", "where
  can LPUART2_TX / LPSPI0_SCK / CAN0_TX / eMIOS_0_CH3 / ADC1_P7 go", "pin
  properties of PTA10", "pin-to-peripheral mapping", "signal routing", "pad
  multiplex", "alternate functions / altN", "pin features / pull / drive
  strength", "package pinout", "Pins tool", "Siul2_Port_Ip_Cfg generation",
  or anything that needs signal_configuration.xml. Read-only canonical
  bridge between the installed RTD pin database and a Pins-tool .mex.
allowed-tools: Read, Grep, Glob
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: "s32ct-distributions"
  tags: '[s32ct, configuration-tools, knowledge, discovery, pins, read-only]'
---

# S32CT Pins Info

Look up *what* pins are available on a given `(MCU, RTD, package)` triple
and *how* each pin can be configured in the S32 Configuration Tools
Pins tool, by parsing the `signal_configuration.xml` shipped with the
installed Platform SDK / RTD. Pure read/inspection skill - does not
modify any project, `.mex`, target memory, or system state. Legacy
alias `freemaster.get_pin_info` is kept for back-compat but the skill is
unrelated to FreeMASTER.

## When to use
- Use for: enumerating pins on a package; finding legal routings for a
  peripheral signal (e.g. "where can `LPSPI0_SCK` go?"); listing the
  configurable attributes of a single pin (mode digital/analog, pulls,
  drive strengths, open-drain, slew rate, direction); validating a
  routing before authoring a `.mex`; diagnosing why a routing is
  missing (wrong package variant, RTD version, or signal not exposed).
- Do **not** use this skill for: editing a `.mex` (use `s32ct-pins-author-mex` /
  `s32ct-generate-mex-config` / `s32ct-pins-facade`); generating
  `Siul2_Port_Ip_Cfg.[ch]` / `Tspc_Port_Ip_Cfg.[ch]` (use
  `s32ct-generate-code`); peripheral or clock queries (use
  `s32ct-peripherals-info` / `s32ct-clocks-info`).

## Available Capabilities

This skill is read-only. The capabilities below only inspect the Pins
data model; none of them modify a `.mex`, generate code, or execute a
CLI.

| Type | Name | Invocation |
|------|------|------------|
| Query | Package overview | `mcu="S32K312", package="S32K312_172HDQFP", include_routings=false` |
| Query | Legal routings for a signal | `filter={ "signal": "LPUART2_TX" }` |
| Query | Pin properties + routings | `filter={ "pin": "PTA10" }` |
| Query | Signals of a peripheral instance | `filter={ "peripheral": "LPSPI0" }` |
| Reference | Full XML anatomy and filter schema | `references/pin-inspection.md` |
| Reference | Authoring a `<pin>` entry (hand-off prep) | `references/authoring-pin-reference.md` |
| Data | `<S32DS>/eclipse/mcu_data/processors/<mcu>/<platform_sdk>/<package>/signal_configuration.xml` | The per-package XML consumed by this skill. |

## Post 16->5 tool mapping

Write-side and CLI actions belong to the sibling skills listed below.
They are documented here only so the agent knows where to hand off -
this skill never invokes them.

| Sibling skill id | MCP call to use |
|---|---|
| `s32ct-cli` | `nxp_s32ct_execute_action(action_name="s32ct.configure_cli", params={...})` |
| `s32ct-pins-facade` | `nxp_s32ct_execute_action(action_name="s32ct.configure_pins", params={...})` |
| `s32ct-generate-code` | `nxp_s32ct_execute_action(action_name="s32ct.generate_code", params={...})` |

## Quickstart

1. Resolve paths from `mcu`, `package`, and `platform_sdk` (defaults to
   the sole subfolder under `mcu_data/processors/<mcu>/` when exactly
   one exists):

   ```
   <S32DS_INSTALL>/eclipse/mcu_data/processors/<mcu>/<platform_sdk>/<package>/signal_configuration.xml
   ```

2. Package overview:

   ```jsonc
   { "mcu": "S32K312",
     "package": "S32K312_172HDQFP",
     "include_routings": false }
   ```

3. Where can a signal go?

   ```jsonc
   { "mcu": "S32K312", "package": "S32K312_172HDQFP",
     "filter": { "signal": "LPUART2_TX" } }
   ```

4. Pin properties + all its legal routings:

   ```jsonc
   { "mcu": "S32K312", "package": "S32K312_172HDQFP",
     "filter": { "pin": "PTA10" } }
   ```

5. All signals exposed by a peripheral instance:

   ```jsonc
   { "mcu": "S32K312", "package": "S32K312_172HDQFP",
     "filter": { "peripheral": "LPSPI0" } }
   ```

More payloads in `references/usage-examples.md`. Full XML anatomy,
namespace pitfall, filter schema, output format and behaviour rules are
in `references/pin-inspection.md`. Authoring `<pin>` entries in a
`.mex` is in `references/authoring-pin-reference.md`.

## Configuration

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mcu` | string | yes | Folder name under `mcu_data/processors/`. Case-sensitive. |
| `package` | string | yes | Package folder name. Case-sensitive. |
| `platform_sdk` | string | no | Defaults to the sole subfolder when unambiguous. |
| `s32ds_install` | string | no | Override of the S32CT install root. MCP auto-discovers at startup - see `s32ct-distributions`. |
| `query` | string | no | Free-form question, fuzzy-matched. |
| `filter` | object | no | Structured filter (`pin`, `peripheral`, `peripheral_type`, `signal`, `direction`, `mode`, `property`, `property_value`). AND-combined. See `references/pin-inspection.md`. |
| `include_routings` | bool | no | Default `true`. Include the legal routing list when describing a pin or signal. |
| `max_results` | int | no | Default `200`. |

## Guardrails

**Scope.** Reads only `signal_configuration.xml` and its parent
directories under `<S32DS_INSTALL>/eclipse/mcu_data/.../<package>/`. Does
not modify any project, `.mex`, target memory, or system state.
Idempotent - safe to call repeatedly.

**Destructive actions.** None. Purely read-only.

**Refuse-and-escalate.** Refuses when required MCU / SDK / package
directories are missing, when `signal_configuration.xml` is absent or
unparseable, or when a filter key is unknown - returns actionable
error messages listing the available alternatives. Never invents pin
names, signal ids, or routings: only what appears verbatim in the XML
is quoted.

## Validation loop

1. Resolve `mcu` -> `platform_sdk` -> `package` paths and confirm each
   directory exists. On failure return the appropriate error template
   listing available subfolders - the skill never raises.
2. Parse `signal_configuration.xml` handling the namespace pitfall:
   only the root `<pinsmodel:signal_configuration>` carries the
   `pinsmodel:` prefix; every child element is in the *default* (empty)
   namespace. Strip or normalise the prefix on the root before XPath
   iteration, otherwise child lookups silently return nothing.
3. Build the in-memory index (pin `name`+`coords`, peripheral instance
   id, peripheral_type id, peripheral_signal id - always lower-case in
   XML) and apply `filter` (indexed fast path) and/or `query` (fuzzy
   fallback).
4. Walk matched nodes and quote evidence verbatim from `<pin>`,
   `<assign>`, `<peripheral_signal_ref>`,
   `<functional_property>` - never paraphrase attribute values.
5. **Pass** = every filter key resolves and the answer includes the
   verbatim XML excerpts, capped at `max_results` with a truncation
   note when needed. **Fail** = any filter key is unknown or matches
   nothing - return the "closest matches" error template.

## Out of scope

- Modifying `.mex` files, generating driver sources, or launching the
  Pins tool CLI (siblings: `s32ct-pins-author-mex`,
  `s32ct-pins-facade`, `s32ct-generate-code`).
- Clocks and Peripherals tool queries (use `s32ct-clocks-info`,
  `s32ct-peripherals-info`).
- Executing code on target hardware or reading target memory.
- Parsing `.dsn` GUI vector diagrams.
- Guessing pin names or signal ids not present in the XML - packages
  and RTD versions differ; the XML is the sole source of truth.

## See Also

- `references/pin-inspection.md` - full XML anatomy of
  `signal_configuration.xml` (top-level children, illustrative bulk
  counts, `<pin>` shape with `name`+`coords`,
  `<peripheral_signal_ref>` structure), the namespace pitfall, filter
  schema, output format, behaviour rules, reasoning notes on
  case-sensitivity and the channel rule, and the full error-message
  templates.
- `references/authoring-pin-reference.md` - how to turn an XML lookup
  into a `<pin>` entry in a `.mex`: required shape, attribute mapping
  (`peripheral` / `signal` / `pin_num` / `pin_signal`),
  `<pin_features>` table (`direction`, `pull_select`, `pull_enable`,
  `slew_rate`, `drive_strength`, `open_drain`), channel-vs-no-channel
  `signal=` joining rule, verified end-to-end example
  (`LPSPI0_SOUT -> PTB1` and `SIUL2 gpio,0 -> PTA0`), the 3-item
  pre-insertion checklist, and the hand-off chain.
- `references/usage-examples.md` - ready-made input payloads for the
  five common query patterns.
- Related skills: `s32ct-clocks-info` (Clocks-tool data model),
  `s32ct-peripherals-info` (Peripherals-tool data model),
  `s32ct-pins-author-mex` (board-level reference pin definitions),
  `s32ct-generate-mex-config` (bake pin choices into a `.mex`),
  `s32ct-generate-code` (emit `Siul2_Port_Ip_Cfg.[ch]` /
  `Tspc_Port_Ip_Cfg.[ch]`), `s32ct-distributions` (install-root
  discovery).
