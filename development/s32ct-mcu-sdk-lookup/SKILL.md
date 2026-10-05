---
name: s32ct-mcu-sdk-lookup
description: >
  Discovers which MCU parts and which PlatformSDK / RTD versions the installed
  NXP S32 Configuration Tools MCU data package actually supports, so the `mcu`,
  `sdk_version` and `platform_sdk` arguments required by configure, GTM and the
  other lookup actions can be resolved instead of guessed. Triggers on "which
  MCUs are available", "what parts does S32CT support", "list installed MCUs",
  "which SDK / RTD / PlatformSDK versions for S32K344", "what sdk_version
  should I use", "is S32G274A installed", "enumerate processors folder", or any
  cold-start where the user has no `.mex` yet and needs a legal `mcu` /
  `sdk_version` before an `empty_config` bootstrap or
  `s32ct.gtm_create_from_usecase`. Read-only; reads the `processors/` folder of
  the MCU data package and never launches the tool.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  tags: '[s32ct, configuration-tools, discovery, mcu, sdk, read-only]'
---

# S32CT MCU / SDK Lookup

Enumerate the MCUs and PlatformSDK folders installed in the S32 Configuration
Tools MCU data package. This is the top of the discovery chain: it answers
"which `mcu` values does this install support?" and "which SDK versions does
that part have?" so the arguments that the configure, GTM and package-scoped
lookup actions demand become known-good rather than guessed. Both actions are
read-only and never invoke the launcher.

## When to use

Use this skill when:
- The user asks which MCUs / parts are available, installed, or supported
  ("which MCUs can I configure?", "is S32K344 installed?").
- You need a legal `mcu` value before an `empty_config` bootstrap, a
  `s32ct.gtm_create_from_usecase` call, or any `s32ct.lookup_*` query.
- The user asks which SDK / RTD / PlatformSDK versions exist for a given part
  ("what sdk_version should I pass for S32K344?").
- A configure or GTM action failed with an unknown-MCU or unknown-SDK error
  and you need to surface the valid choices.

Do **not** use this skill for:
- Legal pins / drivers / enum values inside a package -> use the package-scoped
  lookups (`s32ct.lookup_drivers`, `s32ct.lookup_arrays`,
  `s32ct.lookup_enum_values`, `s32ct.lookup_pin_signal`).
- Inspecting what an existing `.mex` already contains -> use the
  `s32ct.inspect_*` actions.
- Probing whether S32CT is installed at all / which install was selected ->
  use `s32ct.env_status` / `s32ct.env_installs`.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `s32ct.lookup_mcus` | `nxp_s32ct_execute_action(action_name="s32ct.lookup_mcus", params={})` |
| MCP tool | `s32ct.lookup_sdks` | `nxp_s32ct_execute_action(action_name="s32ct.lookup_sdks", params={"mcu": "S32K344"})` |
| Resource | `skill://nxp_s32ct/s32ct-mcu-sdk-lookup` | Auto-loaded on trigger |

## Quickstart

### 1. List the installed MCUs

```
Tool:    nxp_s32ct_execute_action
Action:  s32ct.lookup_mcus
Input:   {}                                 # optional: mcu_data_root override
Output:  {kind: "list_mcus",
          result: {mcu_count, mcus: [...]},
          source: "<root>/processors"}
```

### 2. List the SDK folders for a chosen MCU

```
Tool:    nxp_s32ct_execute_action
Action:  s32ct.lookup_sdks
Input:   {"mcu": "S32K344"}                  # mcu from step 1
Output:  {kind: "list_sdks", mcu: "S32K344",
          result: {mcu, sdk_count, sdks: [...]},
          source: "<root>/processors/S32K344"}
```

### 3. Feed the result into the next action

Use the chosen `mcu` (and an SDK-derived `sdk_version` / `platform_sdk`) in a
configure bootstrap or GTM template call, for example:

```python
nxp_s32ct_execute_action(
    action_name="s32ct.gtm_create_from_usecase",
    params={"mcu": "S32K344", "sdk_version": "...", "usecase": "...",
            "output_dir": "<out>"},
)
```

## Configuration

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mcu` | string | `lookup_sdks` only | MCU folder name under `processors/`, case-sensitive (e.g. `S32K344`). Discover it with `s32ct.lookup_mcus`. |
| `mcu_data_root` | string | no | Override the MCU data root. Defaults to the root of the install selected at startup; see `s32ct.env_status`. |

## Guardrails

**Scope**
- Reads only the `processors/` folder (and its immediate `PlatformSDK_*`
  subfolders) under the resolved `mcu_data_root`. Modifies nothing; safe to
  call repeatedly.

**Destructive actions**
- None. Both actions are strictly read-only and never launch the tool.

**Refuse-and-escalate**
- No `processors/` folder under `mcu_data_root` -> the action returns a
  NOT_FOUND error naming the probed path; check `s32ct.env_status` to confirm
  an MCU data package is installed and the root is correct.
- `lookup_sdks` with an MCU that has no folder -> NOT_FOUND listing the
  available MCUs; re-run `s32ct.lookup_mcus` and pick a listed name.
- Never invent MCU or SDK names: quote only the folder names the action
  returned.

**Note on SDK names**
- `lookup_sdks` returns on-disk folder names (e.g. `PlatformSDK_S32K3`). The
  exact `-SDKVersion` string a configure action expects may differ; treat the
  result as the discovery hint, not necessarily the verbatim `sdk_version`.

## Validation loop

1. `s32ct.lookup_mcus` succeeds and `result.mcus` is non-empty (a populated
   install). An empty list or NOT_FOUND means the data package or
   `mcu_data_root` needs attention -> escalate via `s32ct.env_status`.
2. The `mcu` passed to `s32ct.lookup_sdks` appears in the step-1 list.
3. `s32ct.lookup_sdks` returns `sdk_count >= 1` for that MCU before you rely on
   a `sdk_version` / `platform_sdk` downstream.

## Out of scope

- Package-scoped legal-value queries (pins, drivers, arrays, enum values).
- Inspecting or editing a `.mex`.
- Selecting or switching the active S32CT install (restart-time concern; see
  `s32ct.env_installs`).

## See Also

- `s32ct-pins-info`, `s32ct-peripherals-info`, `s32ct-clocks-info` - per-tool
  read-only data-model queries once the `(mcu, package)` is known.
- `s32ct-gtm-create-from-usecase` - consumes the `mcu` / `sdk_version` this
  skill discovers.
- `s32ct-distributions` - how the install root (and thus `mcu_data_root`) is
  discovered and selected.
