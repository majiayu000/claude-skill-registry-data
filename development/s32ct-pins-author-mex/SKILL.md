---
name: s32ct-pins-author-mex
description: >
  Produces a S32 Configuration Tools Pins-tool .mex from a board description
  (schematic PDF or explicit routings list) plus an MCU/RTD/package triple.
  Triggers on "configure pins for board X", "generate Pins .mex from
  schematic", "route SPI/UART/CAN/LIN/ADC/PWM for evaluation board", "S32CT
  Pins .mex bring-up", "board-tailored pin routing", "auto-route peripherals
  from this schematic". Canonical entry point when the inputs are (a board) +
  (a peripheral wish-list or routings) + (MCU/RTD/package). Chains
  s32ct-pins-info to enumerate legal routings, s32ct-generate-mex-config to
  clone a reference .mex template and patch in the <pin> block, then
  s32ct-pins-facade -ShowProblems to validate with stderr capture.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-pins-info, s32ct-generate-mex-config, s32ct-pins-facade, s32ct-generate-code]'
  tags: '[s32ct, configuration-tools, mex-authoring, headless, pins]'
---

# S32CT Pins .mex Authoring

Author a Pins-tool `.mex` for a given `(MCU, package, platform_sdk)` triple
from a board description (schematic PDF or explicit routings). The skill
orchestrates three lower-level skills in order: enumerate legal routings,
clone a reference template and patch in `<pin>` entries, then validate
with stderr capture. Works for any MCU for which a reference `.mex`
template has been registered with `s32ct-generate-mex-config`.

## When to use
- Use for: "make a Pins .mex for board X with `<peripheral list>`",
  "configure pins for `<peripherals>` on this EVB", "generate the Pins
  config that matches this schematic", "bring up Pins for `<MCU>` on
  `<board>` using RTD `<version>`".
- Do **not** use this skill for: Clocks-tool authoring (`s32ct-clocks-graft-mex`),
  Peripherals-tool authoring (`s32ct-peripherals-author-mex`),
  driver-source generation (`s32ct-generate-code`), interactive routing
  exploration only (`s32ct-pins-info` alone), or targets for which no
  reference template exists (see `references/authoring-procedure.md`
  section *Extending to a new MCU/RTD/package*).

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Sub-skill | `s32ct-pins-info` | Enumerate legal `(peripheral, signal, pin)` triples. |
| Sub-skill | `s32ct-generate-mex-config` | Clone reference `.mex`, patch `<pin>` block. |
| MCP action | `nxp_s32ct_execute_action(action_name="s32ct.configure_pins", params={...})` | Headless validation (`-ShowProblems`). |
| MCP action | `nxp_s32ct_execute_action(action_name="s32ct.generate_code", params={...})` | Optional: emit `Siul2_Port_Ip_Cfg.[ch]`. |

## Quickstart

1. Collect inputs: `board_name`, `mcu`, `package`, `platform_sdk`,
   `output_path`, and either `schematic_path` (PDF/folder) **or** an
   explicit `routings` list. Optional: `peripheral_request` quota
   (e.g. `{ "SPI": 2, "UART": 2, "CAN": 2, "LIN": 2, "ADC": 2, "PWM": 1 }`).

2. Enumerate legal routings for the target and cross-check every
   candidate `(peripheral, signal, pin)`:

   ```jsonc
   // s32ct-pins-info payload
   { "mcu": "S32K312",
     "package": "S32K312_172HDQFP",
     "platform_sdk": "PlatformSDK_S32K3",
     "filter": { "peripheral": "LPSPI0" } }
   ```

3. Resolve conflicts in the fixed greedy order
   `ADC -> CAN -> LPSPI -> LPUART -> PWM`. See
   `references/authoring-procedure.md` for the full algorithm and
   `<pin>` shape.

4. Clone the reference template and patch in the `<pin>` block:

   ```jsonc
   // s32ct-generate-mex-config payload
   { "mcu": "S32K312", "package": "S32K312_172HDQFP",
     "platform_sdk": "PlatformSDK_S32K3",
     "output_path": "<output_path>",
     "modifications": { "pins": "<literal <pin> block>",
                        "common": { "description":
                          "Board-tailored: <board> - <request-summary>" } },
     "regenerate_uuid": true, "copy_sidecars": true }
   ```

5. Validate with stderr capture (exit code alone is not sufficient):

   ```jsonc
   { "action": "pins",
     "project_path": "<output_path>",
     "extra_args": ["-ShowProblems"] }
   ```

   Apply the four-step stderr filter documented in
   `references/authoring-procedure.md` (section *Validation recipe*).

6. Optional - emit driver sources:

   ```jsonc
   { "action": "generate_code",
     "project_path": "<output_path>",
     "tool_name": "Pins", "export_kind": "ExportSrc",
     "output_dir": "<dirname(output_path)>/generated_pins" }
   ```

## Configuration

Key inputs (full table in `references/authoring-procedure.md`):

| Name | Required | Notes |
|------|----------|-------|
| `board_name` | yes | Human label, used only in the report. |
| `schematic_path` | conditional | Required when `routings` is not supplied. |
| `routings` | conditional | Explicit override, bypasses schematic parsing. |
| `peripheral_request` | yes when parsing schematic | Quota per family. |
| `mcu`, `package` | yes | Case-sensitive folder names. |
| `platform_sdk` | no | Defaults to the sole subfolder when unambiguous. |
| `output_path` | yes | Absolute path for the generated `.mex`. |
| `prefer_onboard` | no | Default `true`. |
| `regenerate_uuid` | no | Default `true`. |
| `validate` | no | Default `true`. |
| `generate_sources` | no | Default `false`. |
| `overwrite` | no | Default `false`. |

## Guardrails

**Scope.** Writes only to `output_path`, its sibling
`ClockConfigurationMappings.txt`, and (when `generate_sources=true`) the
`generated_pins/` directory. Does not modify the bundled template `.mex`
or `signal_configuration.xml`. Does not touch hardware, registers,
FreeMASTER, or any running process.

**Destructive actions.** Refuses to overwrite an existing `output_path`
unless `overwrite=true`. Refuses to silently drop a requested peripheral
when no conflict-free routing exists - returns an error listing the
conflicts so the caller can reduce the request or supply an explicit
`routings` override.

**Refuse-and-escalate.** Refuses when no reference `.mex` template is
registered for the `(mcu, package, platform_sdk)` triple; escalates to
the *Extending to a new MCU/RTD/package* section of
`references/authoring-procedure.md`. Refuses when neither
`schematic_path` nor `routings` is supplied. Propagates inner-skill
errors verbatim, prefixed with the offending step.

## Validation loop

1. Run headless validation with stderr redirected to file (a one-line
   `.bat` wrapper is often needed because `cmd` evaluates `2>file` only
   with non-spaced paths - copy the `.mex` to a spaceless path first if
   the install path has spaces).
2. Grep captured stderr for `SEVERE: [TOOL]` and `SEVERE: [Generation`.
   Exit code alone is unreliable: `toolsc.exe` returns 0 even when the
   Problems View contains errors.
3. Filter out generic Eclipse/framework noise
   (`SEVERE: Cannot get container for IPath ...`,
   `SEVERE: ... SerDes Config Tool` when SerDes is not enabled,
   `SEVERE: Error in expression parsing ... featureDefined`,
   `SEVERE: Problem occurred during invocation of function derefAsr`).
   The precise filter list is in `references/authoring-procedure.md`.
4. **Pass** = filtered output is empty AND `exit_code == 0`. **Fail** =
   any line remains - surface verbatim in the *Validation result*
   section of the report and keep the file on disk.

## Out of scope

- Configuring the Clocks or Peripherals tools.
- Generating driver C sources without a preceding valid `.mex`
  (call `s32ct-generate-code` afterwards).
- Interactive routing exploration (use `s32ct-pins-info` alone).
- Authoring for MCU/package/SDK triples with no registered reference
  template - see `references/authoring-procedure.md`.
- Modifying target hardware or running code on the MCU.

## See Also

- `references/authoring-procedure.md` - full step-by-step procedure:
  schematic parsing, XML cross-check rules, conflict resolution order,
  `<pin>` element shape, `direction` defaults, template registry, the
  four-step validation recipe, error-message templates, and the
  *Extending to a new MCU/RTD/package* recipe.
- `references/agent-reasoning-notes.md` - long-form rationale: case
  rules for `peripheral=` / `signal=` / `pin_signal=` / `pin_num`,
  channel-attribute rule, why the greedy order is fixed, hand-off
  chain, performance notes on `signal_configuration.xml`.
- `references/usage-examples.md` - ready-made input payload templates
  (schematic-parsing path, explicit-routings regression path,
  new-MCU/package, adding a peripheral on top of an existing set).
- `references/worked-example.md` - verified end-to-end run on
  `S32K312MINI-EVB` with the 23-row final routing table, the CAN0 skip
  and LIN1 -> LPUART5 re-route caveats, and the validation result.
- Related skills: `s32ct-pins-info` (enumeration),
  `s32ct-generate-mex-config` (template + patch),
  `s32ct-pins-facade` (validation), `s32ct-peripherals-author-mex`
  (natural next step), `s32ct-clocks-info` /
  `s32ct-clocks-graft-mex` (needed before driver code-gen),
  `s32ct-generate-code` (emit driver sources),
  `s32ct-distributions` (install-root discovery).
