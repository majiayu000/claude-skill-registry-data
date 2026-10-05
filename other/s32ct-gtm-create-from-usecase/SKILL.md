---
name: s32ct-gtm-create-from-usecase
description: >
  Bootstraps a brand-new S32 Configuration Tools configuration for a
  given MCU and Platform SDK version, applies a predefined GTM use-case
  shipped with the MCU data package, and generates / exports the
  resulting GTM source code in one headless invocation. Use when the
  user says "apply the ATOM inverted PWM use-case for S32E288",
  "generate code for the TIM edge counter", "bootstrap a GTM project
  from a use-case template". Fronts
  nxp_s32ct_execute_action(action_name="s32ct.gtm_create_from_usecase", params={...})
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-distributions, s32ct-generate-code]'
  tags: '[s32ct, headless, configuration-tools, gtm, configuration, code-generation]'
---

# S32CT GTM - Create from Use-Case

Bootstraps a full GTM configuration from an NXP-provided use-case
`.mex` template without opening the GUI: starts from an empty
configuration, pins the MCU + Platform SDK version, applies the chosen
use-case, then regenerates and exports code. Chains `-EmptyConfig` /
`-MCU` / `-SDKVersion` / `-HeadlessTool GTM -ApplyUseCase` / `-Export*`.
Portable across the `desktop` and `integrated_s32ds` distributions
(see `s32ct-distributions`).

## When to use

Use this skill when:
- The user wants to bootstrap a GTM configuration from a known-good
  NXP use-case template (e.g. `atom_inverted_pwm`, `tom_simple_pwm`,
  `tim_edge_count_internal`, `clock_configuration`, `tbu_free_running`).
- No `.mex` exists yet - the target folder starts empty.
- Regenerating a full GTM setup from scratch pinned to a specific
  MCU / SDK version.

Do **not** use this skill for:
- Regenerating code from an *existing* `.mex` - use `s32ct-generate-code`.
- Editing values inside an existing `.mex` (`-SetValue` / `-GetValue`) -
  use `nxp_s32ct_execute_action(action_name="s32ct.gtm_edit", params={...})`.
- Discovering which use-cases exist for a given MCU - use
  `nxp_s32ct_execute_action(action_name="s32ct.gtm_list_usecases", params={"mcu": ...})`.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP action | `s32ct.gtm_create_from_usecase` | This skill's action: `action_name="s32ct.gtm_create_from_usecase", params={"mcu": ..., "sdk_version": ..., "usecase": ..., "output_dir": ...}` |
| Companion action | `s32ct.gtm_list_usecases` | Read-only discovery of available use-cases for `mcu` |
| Companion action | `s32ct.gtm_edit` | Operate on an existing `.mex` via `-SetValue` / `-GetValue` / `-ApplyUseCase` |
| Resource | `skill://nxp_s32ct/s32ct-gtm-create-from-usecase` | Auto-loaded on trigger |

These are three **separate** registered actions. Each is selected by its
own `action_name`; there is no dispatcher parameter that switches between
them.

### Canonical call shape

```python
nxp_s32ct_execute_action(
    action_name="s32ct.gtm_create_from_usecase",
    params={
        "mcu": "S32E288",                        # required
        "sdk_version": "s32sdk_s32ze_rtm_200",   # required
        "usecase": "atom_inverted_pwm",          # required, no .mex extension
        "output_dir": r"C:/out/s32e288_gtm",     # required
        "export_kind": "ExportAll",
        "gtm_codegen": True,
        "config_name": "bldc_gtm_init",
        "mcu_data_root": None,                   # optional override
        "platform_sdk_dir": None,                # optional override
        "usecase_mex_path": None,                # optional; bypass auto-resolution
    },
)
```

### Inputs

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mcu` | string | yes | MCU identifier (e.g. `S32E288`, `S32S247TV`); passed as `-MCU` |
| `sdk_version` | string | yes | Platform SDK version (e.g. `s32sdk_s32ze_rtm_200`); passed as `-SDKVersion` |
| `usecase` | string | yes | Use-case name **without `.mex`** extension |
| `output_dir` | string | yes | Target folder for exported artifacts |
| `mcu_data_root` | string | no | Override root of MCU data install (default from MCP config) |
| `platform_sdk_dir` | string | no | Override `PlatformSDK_*` subfolder name (default: auto-detect) |
| `usecase_mex_path` | string | no | Absolute `.mex` path; bypasses auto-resolution |
| `export_kind` | string | no | `ExportAll` (default), `ExportSrc`, `ExportHTML`, `ExportMEX` |
| `gtm_codegen` | boolean | no | Adds `-SetValue gtm_codegen=true` (default `true`) |
| `config_name` | string | no | Friendly name; passed as `-ConfigName` |
| `s32ct_launcher` | string | no | Override launcher path |
| `launcher_ini` | string | no | Override `.ini` path |

## Quickstart

### 1. Discover which use-cases are available for the MCU

```python
nxp_s32ct_execute_action(
    action_name="s32ct.gtm_list_usecases",
    params={
        "mcu": "S32E288",
    },
)
```

### 2. Apply the chosen use-case and export

```python
nxp_s32ct_execute_action(
    action_name="s32ct.gtm_create_from_usecase",
    params={
        "mcu": "S32E288",
        "sdk_version": "s32sdk_s32ze_rtm_200",
        "usecase": "atom_inverted_pwm",
        "output_dir": r"C:/out/s32e288_atom_inverted_pwm",
    },
)
```

### 3. Verify

Confirm the status message starts with `"GTM use-case '{name}' applied
for {mcu}"` and that generated files (`*.c`, `*.h`, and - for
`ExportMEX` - a `.mex`) exist under `output_dir`. See
`references/usecases.md` for full worked examples, the MCU / use-case
support notes, and the known use-case catalogue.

## Behavior

1. **Validate inputs**: `mcu`, `sdk_version`, `usecase`, `output_dir`
   non-empty; `export_kind` in the allowed set.
2. **Resolve the use-case `.mex`**:
   - If `usecase_mex_path` is provided -> use it directly (must exist).
   - Otherwise build:
     `<mcu_data_root>/processors/<mcu>/<platform_sdk_dir>/gtm/use_cases/use_cases_mexes/<usecase>.mex`
   - If `platform_sdk_dir` is not provided, auto-select the single
     `PlatformSDK_*` folder under `<mcu_data_root>/processors/<mcu>/`;
     if multiple exist, error out and ask the user to disambiguate.
   - The resolved file must exist and end in `.mex`.
3. **Resolve the launcher** - same logic as `s32ct-generate-code` (see
   `s32ct-distributions`).
4. **Build the tail** (single chain, no `;`):

   ```
   -EmptyConfig
   -MCU <mcu>
   -SDKVersion <sdk_version>
   [-ConfigName <config_name>]
   -HeadlessTool GTM -Enable
   -ApplyUseCase "<resolved_usecase_mex>"
   [-SetValue gtm_codegen=true]            # if gtm_codegen = true
   -<export_kind> "<output_dir>"
   ```

   `-EmptyConfig` ensures a brand-new config (no `-Load`). `-MCU` +
   `-SDKVersion` pin the new configuration. The GTM block enables the
   tool, applies the use-case, optionally turns on GTM-driven C code
   generation, and exports.
5. **Run** the process, capture stdout / stderr / exit code.
6. **Map** the exit code and generated-file presence to a
   human-readable status string that includes the resolved use-case
   file, MCU, SDK version, export kind, and output directory.
7. Do **not** modify the MCU data package or the use-case `.mex`
   template. Only write under `output_dir`.

## Guardrails

**Scope**
- Always starts from `-EmptyConfig` - cannot corrupt an existing `.mex`.
- Reads the MCU data package (read-only) and writes only under
  `output_dir`.

**Destructive actions**
- Overwrites previously generated files under `output_dir` (`*.c`,
  `*.h`, `*.html`, and - for `ExportMEX` - a `.mex`).
- May create `output_dir`.
- Launches an external OS process (the S32CT launcher).

**Refuse-and-escalate**
- Launcher / `.ini` missing -> return searched paths and stop.
- `mcu_data_root` does not contain `<mcu>` -> list the available
  processor folders and stop.
- Multiple `PlatformSDK_*` folders under the MCU and `platform_sdk_dir`
  not provided -> list candidates and stop.
- Use-case `.mex` not found -> return the full resolved path plus the
  list of available use-cases in that folder.
- Non-zero exit code -> surface exit code + truncated stderr/stdout tail;
  do **not** retry silently.
- `IllegalStateException: The instance data location has not been
  specified` -> hint that `-data {workspace}` is needed (the MCP handles
  this automatically for `integrated_s32ds`).

## Validation loop

1. Resolved use-case `.mex` exists on disk. **Pass** if true.
2. Process exit code is `0`. **Pass** if true.
3. `output_dir` exists after the call. **Pass** if true.
4. Expected artifacts for the chosen `export_kind` are present
   (`*.c` / `*.h` for `ExportSrc` / `ExportAll`; a `.mex` for
   `ExportMEX`). **Pass** if true.
5. Status message includes the MCU, SDK version, and resolved use-case
   file. **Pass** if true.

If any step fails, follow the *Refuse-and-escalate* rules above.

## Out of scope

- Compiling the generated code. Chain with a build skill.
- Editing an existing `.mex` - use the separate `s32ct.gtm_edit` action.
- Non-GTM tools - use `s32ct-generate-code`.
- Assuming a fixed MCU / use-case catalogue. Different MCUs and
  distributions ship different use-cases; always discover via
  `s32ct.gtm_list_usecases`.

## See Also

- `references/usecases.md` - MCU / Platform-SDK layout, use-case
  catalogue (e.g. `S32E288 / PlatformSDK_S32ZE`), and four worked
  scenarios covering `ExportAll`, `ExportSrc`, `ExportMEX`, and the
  `usecase_mex_path` bypass.
- Related skills: `s32ct-distributions` (launcher prefixes and
  `-data <workspace>` handling), `s32ct-generate-code` (regenerate from
  an existing `.mex` for any single tool).
