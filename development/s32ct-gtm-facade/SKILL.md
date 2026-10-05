---
name: s32ct-gtm-facade
description: >
  Headless facade that fronts the GTM (Generic Timer Module) tool of NXP
  S32 Configuration Tools via `nxp_s32ct_execute_action(action_name="s32ct.gtm_edit", params={...})`.
  Triggers when users ask to apply a GTM use-case template to an existing
  `.mex`, tweak GTM data-model values via `-SetValue`, query values via
  `-GetValue`, list available GTM use-cases for an MCU (the separate
  `s32ct.gtm_list_usecases` action), create from a use-case (the separate
  `s32ct.gtm_create_from_usecase` action), or export GTM source / HTML /
  MEX. Delegates
  shared launcher plumbing (workspace `-data`, `s32ct_launcher`,
  `launcher_ini`, `timeout_s`, retry-on-`IllegalStateException`) to the
  generic `s32ct-cli` skill. Keywords: GTM, use-case, ApplyUseCase,
  SetValue, GetValue, ExportSrc, ExportHTML, ExportMEX, `.mex`.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-cli]'
  tags: '[s32ct, headless, configuration-tools, facade, gtm, use-case, code-generation]'
---

# S32CT GTM - Headless Facade

Thin per-tool facade over the generic `s32ct-cli` skill that exposes only the
flags relevant to the **GTM** tool of S32 Configuration Tools. This skill
fronts the `nxp_s32ct_execute_action` MCP tool with the `s32ct.gtm_*` actions (the
`tool_name` is pre-filled from the action). All shared launcher plumbing,
validation, and auto-retry behavior is inherited from `s32ct-cli`.

## When to use

Use this skill when:
- You need to apply a GTM use-case template (`-ApplyUseCase`) to an
  existing `.mex`, then tweak values via `-SetValue`.
- You need to query GTM data-model values via `-GetValue` (parsed and
  returned under `values` in the response).
- You need to list available GTM use-cases for an MCU
  (`s32ct.gtm_list_usecases`, no project required).
- You need to bootstrap a GTM project from a use-case
  (`s32ct.gtm_create_from_usecase`); this complements
  `s32ct-gtm-create-from-usecase` (which starts from `-EmptyConfig`).
- You need to export GTM source / HTML / MEX.

**Migration note:** The standalone `gtm` MCP tool no longer exists - it
has been replaced by the unified `nxp_s32ct_execute_action` dispatcher's `gtm`
action. Existing inputs are unchanged.

Do **not** use this skill for:
- Cross-tool operations combining flags from multiple tools -> use
  `s32ct-cli` (s32ct.configure_cli).
- Non-GTM peripheral configuration - use the matching facade.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP action | `s32ct.gtm_edit` | `nxp_s32ct_execute_action(action_name="s32ct.gtm_edit", params={...})` - edit / apply-use-case / query / export on a `.mex` |
| Companion action | `s32ct.gtm_list_usecases` | `nxp_s32ct_execute_action(action_name="s32ct.gtm_list_usecases", params={"mcu": ...})` - read-only discovery, no project needed |
| Companion action | `s32ct.gtm_create_from_usecase` | `nxp_s32ct_execute_action(action_name="s32ct.gtm_create_from_usecase", params={...})` - bootstrap from a template |
| Resource | `skill://nxp_s32ct/s32ct-gtm-facade` | Auto-loaded on trigger |

These are three **separate** registered actions, each selected by its own
`action_name`. There is no `gtm_action` sub-selector parameter.

## Quickstart

### 1. Load or bootstrap a `.mex`

```
Tool:    nxp_s32ct_execute_action
Action:  s32ct.gtm_edit
Input:   project_path="<path>.mex"   # OR empty_config=True + mcu + sdk_version
Output:  {exit_code, command, stdout_tail, stderr_tail, values, summary}
```

### 2. Edit / apply use-case / query values, and export

```python
nxp_s32ct_execute_action(
    action_name="s32ct.gtm_edit",
    params={
        "project_path": "<path>.mex",
        "apply_use_case": "<uc>.mex",              # -ApplyUseCase
        "set_values": ["key1=val1", "key2=val2"],  # -SetValue
        "get_values": ["<data-model-id>"],         # -GetValue (parsed into `values`)
        "export_kind": "ExportSrc",                # or ExportAll|ExportHTML|ExportMEX
        "output_dir": "<output-dir>",
    },
)

# List available GTM use-cases for an MCU (no project required).
# This is a different action, not a mode of s32ct.gtm_edit:
nxp_s32ct_execute_action(
    action_name="s32ct.gtm_list_usecases",
    params={
        "mcu": "S32K358",
    },
)
```

### 3. Verify the export

Check that `output_dir` contains the expected artifacts and `exit_code == 0`;
inspect `values` for any `-GetValue` results.

## Inputs

### Mode (mutually exclusive)
- `project_path` - existing `.mex` to load via `-Load`.
- `empty_config` - if `True`, `-EmptyConfig`; requires `mcu` + `sdk_version`.
- `config_name` - `-ConfigName <...>`.

### Tool-specific
- `apply_use_case` - path to a use-case `.mex` via `-ApplyUseCase`.
- `set_values` - array of `key=value` strings via `-SetValue`.
- `get_values` - array of data-model IDs via `-GetValue` (parsed into
  response `values`).

### Export
- `export_kind` in {`ExportAll, ExportSrc, ExportHTML, ExportMEX`}.
- `output_dir` - required when `export_kind` is set.

### Launcher / plumbing (shared with `s32ct-cli`)
- `data_dir` (`-data <workspace>`), `extra_args`, `s32ct_launcher`,
  `launcher_ini`, `timeout_s` (default 600).

## Output

Same as `s32ct-cli`:
`{ exit_code, command, stdout_tail, stderr_tail, values, summary }`.

## Guardrails

**Scope**
- Only drives the **gtm** action of `nxp_s32ct_execute_action`. For cross-tool
  workflows use `s32ct-cli` (s32ct.configure_cli) instead.
- Does not modify hardware or program devices.

**Destructive actions**
- Exports overwrite files in `output_dir`. Confirm the target directory
  is safe or empty before invoking with `export_kind` set.
- `-SetValue` mutates the loaded `.mex` in memory; if the project is
  saved back, source data-model values change.

**Refuse-and-escalate**
- Missing `project_path` AND missing `empty_config`/`mcu`/`sdk_version`
  combination (when calling `s32ct.gtm_edit`) -> ask which mode.
- Unknown `export_kind` value -> list allowed values.
- Unknown `action_name` -> list the three GTM actions
  (`s32ct.gtm_edit`, `s32ct.gtm_list_usecases`,
  `s32ct.gtm_create_from_usecase`).
- Retryable `IllegalStateException` -> auto-retry once, then escalate.

## Validation loop

1. `exit_code == 0`.
2. `output_dir` contains the expected artifacts for the chosen `export_kind`.
3. If `get_values` was supplied, verify each ID appears in `values`.

## Out of scope

- Interactive GUI operations - use S32 Configuration Tools directly.
- Cross-tool operations combining multiple tools' flags - use `s32ct-cli`.
- Distribution portability handled transparently; see
  `s32ct-distributions`.

## See Also

- `s32ct-cli` - generic dispatcher with the full ~50-parameter surface.
- `s32ct-distributions` - launcher selection.
- `s32ct-gtm-create-from-usecase` - bootstrapping GTM from
  `-EmptyConfig`.
