---
name: s32ct-pins-facade
description: >
  Headless facade that fronts the Pins tool of NXP S32 Configuration Tools
  via `nxp_s32ct_execute_action(action_name="s32ct.configure_pins", params={...})`. Triggers when users ask to
  regenerate pin-mux source code, import existing `.c` pin definitions via
  `-ImportC`, apply `custom_copyright` or `output_path_overrides`, or export
  pin artifacts as source, CSV, HTML, registers, or MEX from a `.mex`
  project. Also handles bootstrapping Pins from `-EmptyConfig` with `mcu` +
  `sdk_version`. Delegates shared launcher plumbing (workspace `-data`,
  `s32ct_launcher`, `launcher_ini`, `timeout_s`,
  retry-on-`IllegalStateException`) to `s32ct-cli`. Keywords: pins, pin-mux,
  ImportC, ExportSrc, ExportCSV, ExportHTML, ExportRegisters, ExportMEX,
  `.mex`, `.c`.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-cli]'
  tags: '[s32ct, headless, configuration-tools, facade, pins, code-generation]'
---

# S32CT Pins - Headless Facade

Thin per-tool facade over the generic `s32ct-cli` skill that exposes only the
flags relevant to the **Pins** tool of S32 Configuration Tools. This skill
fronts the `nxp_s32ct_execute_action` MCP tool with `action_name="s32ct.configure_pins"` (the
`tool_name` is pre-filled from the action). All shared launcher plumbing,
validation, and auto-retry behavior is inherited from `s32ct-cli`.

## When to use

Use this skill when:
- You need to regenerate pin-mux source from a `.mex`.
- You need to import existing `.c` pin definitions via `-ImportC` before
  regeneration.
- You need to bootstrap Pins from `-EmptyConfig` (requires `mcu` +
  `sdk_version`).
- You need to export Pins artifacts: source, CSV, HTML, registers, or MEX.

**Migration note:** The standalone `pins` MCP tool no longer exists - it
has been replaced by the standardized action surface: run it as `s32ct.configure_pins` through `nxp_s32ct_execute_action`. Existing inputs are unchanged.

Do **not** use this skill for:
- Cross-tool operations combining flags from multiple tools -> use
  `s32ct-cli` (s32ct.configure_cli).
- Clocks / Peripherals regeneration - use the matching facade.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `nxp_s32ct_execute_action` | `nxp_s32ct_execute_action(action_name="s32ct.configure_pins", params={...})` |
| Resource | `skill://nxp_s32ct/s32ct-pins-facade` | Auto-loaded on trigger |

## Quickstart

### 1. Load or bootstrap a `.mex`

```
Tool:    nxp_s32ct_execute_action
Action:  s32ct.configure_pins
Input:   project_path="<path>.mex"   # OR empty_config=True + mcu + sdk_version
Output:  {exit_code, command, stdout_tail, stderr_tail, values, summary}
```

### 2. Apply Pins-specific modifications and export

```python
nxp_s32ct_execute_action(
    action_name="s32ct.configure_pins",
    params={
        "project_path": "<path>.mex",
        "import_c": ["<a>.c", "<b>.c"],           # -ImportC
        "custom_copyright": "<header>.txt",        # -CustomCopyright
        "output_path_overrides": "<rules>.txt",    # -OutputPathOverrides
        "export_kind": "ExportSrc",                # or ExportAll|ExportCSV|ExportHTML|
                                                   #    ExportRegisters|ExportMEX
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
- `import_c` - paths to existing `.c` files imported via `-ImportC` before
  regeneration.
- `custom_copyright` - header file inserted via `-CustomCopyright`.
- `output_path_overrides` - rules file via `-OutputPathOverrides`.

### Export
- `export_kind` in {`ExportAll, ExportSrc, ExportCSV, ExportHTML,
  ExportRegisters, ExportMEX`}.
- `output_dir` - required when `export_kind` is set.

### Launcher / plumbing (shared with `s32ct-cli`)
- `data_dir` (`-data <workspace>`), `extra_args`, `s32ct_launcher`,
  `launcher_ini`, `timeout_s` (default 600).

## Output

Same as `s32ct-cli`:
`{ exit_code, command, stdout_tail, stderr_tail, values, summary }`.

## Guardrails

**Scope**
- Only drives the **pins** action of `nxp_s32ct_execute_action`. For cross-tool
  workflows use `s32ct-cli` (s32ct.configure_cli) instead.
- Does not modify hardware or program devices.

**Destructive actions**
- Exports overwrite files in `output_dir`. Confirm the target directory
  is safe or empty before invoking with `export_kind` set.

**Refuse-and-escalate**
- Missing `project_path` AND missing `empty_config`/`mcu`/`sdk_version`
  combination -> ask which mode.
- Unknown `export_kind` value -> list allowed values.
- Retryable `IllegalStateException` -> auto-retry once, then escalate.

## Validation loop

1. `exit_code == 0`.
2. `output_dir` contains the expected artifacts for the chosen `export_kind`.
3. For source exports: files compile / parse cleanly in a follow-up step.

## Out of scope

- Interactive GUI operations - use S32 Configuration Tools directly.
- Cross-tool operations combining multiple tools' flags - use `s32ct-cli`.
- Distribution portability handled transparently; see
  `s32ct-distributions`.

## See Also

- `s32ct-cli` - generic dispatcher with the full ~50-parameter surface.
- `s32ct-distributions` - launcher selection.
- `s32ct-clocks-facade`, `s32ct-peripherals-facade` - sibling
  regeneration facades sharing the `custom_copyright` /
  `output_path_overrides` pattern.
