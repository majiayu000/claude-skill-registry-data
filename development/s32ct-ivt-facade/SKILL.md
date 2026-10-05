---
name: s32ct-ivt-facade
description: >
  Headless facade that fronts the IVT (Image Vector Table) tool of NXP
  S32 Configuration Tools via `nxp_s32ct_execute_action(action_name="s32ct.configure_ivt", params={...})`.
  Triggers when users ask to import binary IVT images, blobs
  (`-ImportBlob`), application bootloader (`-ImportAB`), DDRC init app
  (`-ImportDDRC`), auto-align segments (`-AutoAlign`), set RAM
  start/entry pointers, and export IVT artifacts (Bin, C, Blob, AB,
  Pointers, DDRC, FssFw, MEX) from a `.mex` project. Also handles
  `-CustomPointersAddrs`, `-raw_binary`, `-clockConfigData`,
  `-miniPacoStructure`, `-pre_defined_data`, `-bootDeviceId`,
  `-IvtStartAddr`, `-UpdateFilepaths`, `-filter`, `-includeMarker`,
  `-ValidateConfiguration`. Delegates shared launcher plumbing to `s32ct-cli`.
  Keywords: IVT, boot image, blob, application bootloader, DDRC, `.bin`,
  `.blob`, `.mex`.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-cli]'
  tags: '[s32ct, headless, configuration-tools, facade, ivt, boot-image, code-generation]'
---

# S32CT IVT - Headless Facade

Thin per-tool facade over the generic `s32ct-cli` skill that exposes only the
flags relevant to the **IVT** tool of S32 Configuration Tools. This skill
fronts the `nxp_s32ct_execute_action` MCP tool with `action_name="s32ct.configure_ivt"` (the
`tool_name` is pre-filled from the action). All shared launcher plumbing,
validation, and auto-retry behavior is inherited from `s32ct-cli`.

## When to use

Use this skill when:
- You need to import binary IVT images / blobs / application bootloader /
  DDRC images into a `.mex`.
- You need to auto-align segments, set RAM start/entry pointers, or set
  custom pointer addresses.
- You need to export IVT artifacts: `ExportBin`, `ExportC`, `ExportBlob`,
  `ExportAB`, `ExportPointers`, `ExportDDRC`, `ExportFssFw`, `ExportMEX`.

**Migration note:** The standalone `ivt` MCP tool no longer exists - it has
been replaced by the standardized action surface: run it as `s32ct.configure_ivt` through `nxp_s32ct_execute_action`.
Existing inputs are unchanged.

Do **not** use this skill for:
- Cross-tool operations combining flags from multiple tools -> use
  `s32ct-cli` (s32ct.configure_cli).
- Programming/flashing devices - this only produces boot images.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `nxp_s32ct_execute_action` | `nxp_s32ct_execute_action(action_name="s32ct.configure_ivt", params={...})` |
| Resource | `skill://nxp_s32ct/s32ct-ivt-facade` | Auto-loaded on trigger |

## Quickstart

### 1. Load or bootstrap a `.mex`

```
Tool:    nxp_s32ct_execute_action
Action:  s32ct.configure_ivt
Input:   project_path="<path>.mex"   # OR empty_config=True + mcu + sdk_version
Output:  {exit_code, command, stdout_tail, stderr_tail, values, summary}
```

### 2. Apply IVT-specific modifications and export

```python
nxp_s32ct_execute_action(
    action_name="s32ct.configure_ivt",
    params={
        "project_path": "<path>.mex",
        "import_bin": "<ivt>.bin",             # -ImportBin
        "auto_align": True,                    # -AutoAlign
        "start_pointer_addr": "0x34000000",    # RAM start pointer
        "entry_pointer_addr": "0x34000100",    # RAM entry pointer
        "export_kind": "ExportBin",            # or ExportAll|ExportC|ExportBlob|ExportAB|
                                               #    ExportPointers|ExportDDRC|ExportFssFw|ExportMEX
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
- `import_bin` - `-ImportBin` (IVT binary image).
- `import_blob` - `-ImportBlob` plus optional `ivt_start_addr` and
  `boot_device_id`.
- `import_ab` - `-ImportAB` (application bootloader).
- `import_ddrc` - `-ImportDDRC` (DDRC interface init app).
- `auto_align` - `-AutoAlign [<hex_addr>]` (empty string => no addr).
- `custom_pointers_addrs` - `-CustomPointersAddrs 0x100,0x200`.
- `start_pointer_addr`, `entry_pointer_addr` - RAM pointers (hex).
- `raw_binary` - `-raw_binary <path>`.
- `clock_config_data` - `-clockConfigData`.
- `mini_paco_structure` - `-miniPacoStructure`.
- `pre_defined_data` - `-pre_defined_data`.
- `boot_device_id` - `-bootDeviceId`.
- `ivt_start_addr` - `-IvtStartAddr`.
- `update_filepaths` -
  `-UpdateFilepaths {relativeToCurrentMex|absolute|keepExisting}`.
- `ivt_filter` - `-filter {UnresolvedCustomPointers|All}`.
- `include_marker` - `-includeMarker`.
- `validate` - `-ValidateConfiguration`.

### Export
- `export_kind` in {`ExportAll, ExportBin, ExportC, ExportBlob, ExportAB,
  ExportPointers, ExportDDRC, ExportFssFw, ExportMEX`}.
- `output_dir` - required when `export_kind` is set.

### Launcher / plumbing (shared with `s32ct-cli`)
- `data_dir` (`-data <workspace>`), `extra_args`, `s32ct_launcher`,
  `launcher_ini`, `timeout_s` (default 600).

## Output

Same as `s32ct-cli`:
`{ exit_code, command, stdout_tail, stderr_tail, values, summary }`.

## Guardrails

**Scope**
- Only drives the **ivt** action of `nxp_s32ct_execute_action`. For cross-tool
  workflows use `s32ct-cli` (s32ct.configure_cli) instead.
- Does not program devices - exports boot-image files only.

**Destructive actions**
- Exports overwrite files in `output_dir`. Confirm the target directory
  is safe or empty before invoking with `export_kind` set.

**Refuse-and-escalate**
- Missing `project_path` AND missing `empty_config`/`mcu`/`sdk_version`
  combination -> ask which mode.
- Unknown `export_kind`, `update_filepaths`, or `ivt_filter` value ->
  list allowed values.
- Retryable `IllegalStateException` -> auto-retry once, then escalate.

## Validation loop

1. `exit_code == 0`.
2. `output_dir` contains the expected artifacts for the chosen `export_kind`.
3. If `validate=True`, confirm validation OK in `stdout_tail`/`summary`.

## Out of scope

- Interactive GUI operations - use S32 Configuration Tools directly.
- Cross-tool operations combining multiple tools' flags - use `s32ct-cli`.
- Distribution portability handled transparently; see
  `s32ct-distributions`.

## See Also

- `s32ct-cli` - generic dispatcher with the full ~50-parameter surface.
- `s32ct-distributions` - launcher selection.
- `s32ct-dcd-facade`, `s32ct-quadspi-facade`, `s32ct-efuse-facade` -
  related boot-image tool facades.
