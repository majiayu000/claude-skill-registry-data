---
name: s32ct-ffc-facade
description: >
  Headless facade that fronts the FFC tool of NXP S32 Configuration Tools
  via `nxp_s32ct_execute_action(action_name="s32ct.configure_ffc", params={...})`. Triggers when users ask to
  import AUTOSAR ARXML (`.ecvd`) files or JSON, restrict the FFC
  `-FileType` to `all|Fss_Rem_Pm|Fss_Btm`, fill default containers, validate
  the configuration, or export ARXML / JSON / MEX from a `.mex` project.
  Delegates shared launcher and plumbing (workspace `-data`,
  `s32ct_launcher`, `launcher_ini`, `timeout_s`,
  retry-on-`IllegalStateException`) to the generic `s32ct-cli` skill.
  Keywords: FFC, AUTOSAR, ARXML, `.ecvd`, JSON, `-defaultContainers`,
  `-Validate`, ExportARXML, ExportJSON, ExportMEX.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-cli]'
  tags: '[s32ct, headless, configuration-tools, facade, ffc, autosar, code-generation]'
---

# S32CT FFC - Headless Facade

Thin per-tool facade over the generic `s32ct-cli` skill that exposes only the
flags relevant to the **FFC** tool of S32 Configuration Tools. This skill
fronts the `nxp_s32ct_execute_action` MCP tool with `action_name="s32ct.configure_ffc"` (the
`tool_name` is pre-filled from the action). All shared launcher plumbing,
validation, and auto-retry behavior is inherited from `s32ct-cli`.

## When to use

Use this skill when:
- You need to import AUTOSAR ARXML `.ecvd` files or a JSON file into FFC.
- You need to restrict the file type (`all`, `Fss_Rem_Pm`, `Fss_Btm`), fill
  default containers, or validate the FFC configuration.
- You need to export ARXML / JSON / MEX artifacts.

**Migration note:** The standalone `ffc` MCP tool no longer exists - it has
been replaced by the standardized action surface: run it as `s32ct.configure_ffc` through `nxp_s32ct_execute_action`.
Existing inputs are unchanged.

Do **not** use this skill for:
- Cross-tool operations combining flags from multiple tools -> use
  `s32ct-cli` (s32ct.configure_cli).
- Non-AUTOSAR configuration flows - use the matching tool facade.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `nxp_s32ct_execute_action` | `nxp_s32ct_execute_action(action_name="s32ct.configure_ffc", params={...})` |
| Resource | `skill://nxp_s32ct/s32ct-ffc-facade` | Auto-loaded on trigger |

## Quickstart

### 1. Load or bootstrap a `.mex`

```
Tool:    nxp_s32ct_execute_action
Action:  s32ct.configure_ffc
Input:   project_path="<path>.mex"   # OR empty_config=True + mcu + sdk_version
Output:  {exit_code, command, stdout_tail, stderr_tail, values, summary}
```

### 2. Apply FFC-specific modifications and export

```python
nxp_s32ct_execute_action(
    action_name="s32ct.configure_ffc",
    params={
        "project_path": "<path>.mex",
        "import_arxml": ["<a>.ecvd", "<b>.ecvd"],  # -ImportARXML
        "import_json": "<cfg>.json",               # -ImportJSON
        "file_type": "all",                        # all|Fss_Rem_Pm|Fss_Btm
        "default_containers": True,                # -defaultContainers
        "validate": True,                          # -ValidateConfiguration
        "export_kind": "ExportARXML",              # or ExportAll|ExportJSON|ExportMEX
        "output_dir": "<output-dir>",
    },
)
```

### 3. Verify the export

Check that `output_dir` contains the expected artifacts and `exit_code == 0`.

## Inputs

### Mode (mutually exclusive)
- `project_path` - existing `.mex` to load via `-Load`.
- `empty_config` - if `True`, `-EmptyConfig`; requires `mcu` + `sdk_version`.
- `config_name` - `-ConfigName <...>`.

### Tool-specific
- `import_arxml` - list of `.ecvd` files via `-ImportARXML`.
- `import_json` - single JSON via `-ImportJSON`.
- `file_type` - `-FileType {all|Fss_Rem_Pm|Fss_Btm}`.
- `default_containers` - `-defaultContainers`.
- `validate` - `-Validate`.

### Export
- `export_kind` in {`ExportAll, ExportARXML, ExportJSON, ExportMEX`}.
- `output_dir` - required when `export_kind` is set.

### Launcher / plumbing (shared with `s32ct-cli`)
- `data_dir` (`-data <workspace>`), `extra_args`, `s32ct_launcher`,
  `launcher_ini`, `timeout_s` (default 600).

## Output

Same as `s32ct-cli`:
`{ exit_code, command, stdout_tail, stderr_tail, values, summary }`.

## Guardrails

**Scope**
- Only drives the **ffc** action of `nxp_s32ct_execute_action`. For cross-tool
  workflows use `s32ct-cli` (s32ct.configure_cli) instead.
- Does not modify hardware or program devices.

**Destructive actions**
- Exports overwrite files in `output_dir`. Confirm the target directory
  is safe or empty before invoking with `export_kind` set.

**Refuse-and-escalate**
- Missing `project_path` AND missing `empty_config`/`mcu`/`sdk_version`
  combination -> ask the user which mode they want.
- Unknown `export_kind` or `file_type` value -> list allowed enum values.
- Retryable `IllegalStateException` -> auto-retry once, then escalate.

## Validation loop

1. `exit_code == 0`.
2. `output_dir` contains the expected artifacts for the chosen `export_kind`.
3. If `validate=True`, confirm validation success in `stdout_tail` /
   `summary`.

## Out of scope

- Interactive GUI operations - use S32 Configuration Tools directly.
- Cross-tool operations combining multiple tools' flags - use `s32ct-cli`.
- Distribution portability handled transparently; see
  `s32ct-distributions`.

## See Also

- `s32ct-cli` - generic dispatcher with the full ~50-parameter surface.
- `s32ct-distributions` - launcher selection.
- Other tool facades (`s32ct-peripherals-facade`, `s32ct-clocks-facade`,
  etc.) for sibling flows.
