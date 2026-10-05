---
name: s32ct-clocks-facade
description: >
  Headless facade that fronts the Clocks tool of NXP S32 Configuration Tools
  via `nxp_s32ct_execute_action(action_name="s32ct.configure_clocks", params={...})`. Triggers when users ask to
  regenerate a clock tree, drive S32CT Clocks headlessly, export clock source
  code / HTML / registers / MEX from a `.mex` project, apply
  `custom_copyright` or `output_path_overrides`, or bootstrap clocks from an
  `-EmptyConfig` with `mcu` + `sdk_version`. Delegates shared launcher and
  plumbing details (workspace `-data`, `s32ct_launcher`, `launcher_ini`,
  `timeout_s`, retry-on-`IllegalStateException`) to the generic `s32ct-cli`
  skill. Covers keywords: clocks, clock tree, ExportSrc, ExportHTML,
  ExportRegisters, ExportMEX, `.mex`.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-cli]'
  tags: '[s32ct, headless, configuration-tools, facade, clocks, code-generation]'
---

# S32CT Clocks - Headless Facade

Thin per-tool facade over the generic `s32ct-cli` skill that exposes only the
flags relevant to the **Clocks** tool of S32 Configuration Tools. This skill
fronts the `nxp_s32ct_execute_action` MCP tool with `action_name="s32ct.configure_clocks"` (the
`tool_name` is pre-filled from the action). All shared launcher plumbing,
validation, and auto-retry behavior is inherited from `s32ct-cli`, which
documents the full ~50-parameter surface.

## When to use

Use this skill when:
- You need to regenerate clock-tree source code from an existing `.mex`.
- You need to bootstrap a clocks configuration from `-EmptyConfig` (requires
  `mcu` + `sdk_version`).
- You need to export Clocks artifacts: source, HTML, registers, or MEX.

**Migration note:** The standalone `clocks` MCP tool no longer exists - it
has been replaced by the standardized action surface: run it as `s32ct.configure_clocks` through `nxp_s32ct_execute_action`. Existing inputs are unchanged.

Do **not** use this skill for:
- Cross-tool operations combining flags from multiple tools -> use
  `s32ct-cli` (s32ct.configure_cli).
- Flags not exposed here (use `s32ct.configure_cli` for the full surface).

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `nxp_s32ct_execute_action` | `nxp_s32ct_execute_action(action_name="s32ct.configure_clocks", params={...})` |
| Resource | `skill://nxp_s32ct/s32ct-clocks-facade` | Auto-loaded on trigger |

## Quickstart

### 1. Load or bootstrap a `.mex`

```
Tool:    nxp_s32ct_execute_action
Action:  s32ct.configure_clocks
Input:   project_path="<path>.mex"   # OR empty_config=True + mcu + sdk_version
Output:  {exit_code, command, stdout_tail, stderr_tail, values, summary}
```

### 2. Apply Clocks-specific modifications and export

```python
nxp_s32ct_execute_action(
    action_name="s32ct.configure_clocks",
    params={
        "project_path": "<path>.mex",
        "custom_copyright": "<header>.txt",       # -CustomCopyright
        "output_path_overrides": "<rules>.txt",   # -OutputPathOverrides
        "export_kind": "ExportSrc",               # or ExportAll|ExportHTML|ExportRegisters|ExportMEX
        "output_dir": "<output-dir>",
    },
)
```

### 3. Verify the export

Check that `output_dir` contains the expected artifacts and that
`exit_code == 0`.

## Inputs

### Mode (mutually exclusive)
- `project_path` - existing `.mex` to load via `-Load`.
- `empty_config` - if `True`, start from `-EmptyConfig`; requires `mcu` +
  `sdk_version`.
- `config_name` - `-ConfigName <...>`.

### Tool-specific
- `custom_copyright` - header file inserted via `-CustomCopyright`.
- `output_path_overrides` - rules file via `-OutputPathOverrides`.

### Export
- `export_kind` in {`ExportAll, ExportSrc, ExportHTML, ExportRegisters, ExportMEX`}.
- `output_dir` - required when `export_kind` is set.

### Launcher / plumbing (shared with `s32ct-cli`)
- `data_dir` (`-data <workspace>`), `extra_args`, `s32ct_launcher`,
  `launcher_ini`, `timeout_s` (default 600).

## Output

Same as `s32ct-cli`:
`{ exit_code, command, stdout_tail, stderr_tail, values, summary }`.

## Guardrails

**Scope**
- Only drives the **clocks** action of `nxp_s32ct_execute_action`. For
  cross-tool workflows use `s32ct-cli` (s32ct.configure_cli) instead.
- Does not modify hardware or program devices.

**Destructive actions**
- Exports overwrite files in `output_dir`. Confirm the target directory
  is safe or empty before invoking with `export_kind` set.

**Refuse-and-escalate**
- Missing `project_path` AND missing `empty_config`/`mcu`/`sdk_version`
  combination -> ask the user which mode they want.
- Unknown `export_kind` value -> list the allowed enum values and ask.
- Retryable `IllegalStateException` from the launcher -> auto-retry once,
  then escalate with the stderr tail.

## Validation loop

1. `exit_code == 0`.
2. `output_dir` contains the expected artifacts for the chosen `export_kind`.
3. For source exports: files compile / parse cleanly in a follow-up step.

## Out of scope

- Interactive GUI operations - use S32 Configuration Tools directly.
- Cross-tool operations combining multiple tools' flags - use `s32ct-cli`.
- Code generation for tools other than Clocks - use the matching facade.
- Portability across `desktop` vs `integrated_s32ds` distributions is
  handled transparently by the MCP; see `s32ct-distributions` for context.

## See Also

- `s32ct-cli` - generic dispatcher with the full ~50-parameter surface.
- `s32ct-distributions` - launcher selection (desktop vs S32DS-integrated).
- `s32ct-pins-facade`, `s32ct-peripherals-facade` - sibling tool facades
  sharing the `custom_copyright` / `output_path_overrides` pattern.
