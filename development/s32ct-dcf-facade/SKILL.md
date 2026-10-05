---
name: s32ct-dcf-facade
description: >
  Headless facade that fronts the DCF (Device Configuration Format) tool of NXP
  S32 Configuration Tools via `nxp_s32ct_configure(action="dcf", ...)`.
  Triggers when users ask to import a binary DCF image, validate a DCF
  configuration, or export DCF artifacts as binary or C source from a
  `.mex` project on a DCF-capable SoC. Also handles bootstrapping DCF from
  `-EmptyConfig` with `mcu` + `sdk_version`. DCF is not a separate headless
  tool: it shares the DCD tool's `CmdApplication`, so the `dcf` action routes
  through `-HeadlessTool DCD` and the tool auto-selects the DCF variant from
  the loaded processor. Delegates shared launcher and plumbing (workspace
  `-data`, `s32ct_launcher`, `launcher_ini`, `timeout_s`,
  retry-on-`IllegalStateException`) to the generic `s32ct-cli` skill.
  Keywords: DCF, Device Configuration Format, DCF record, DCF client, control
  word, data word, `-ImportBin`, `-ValidateConfiguration`, ExportBin, ExportC, ExportAll,
  ExportMEX, `.bin`, `.mex`.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-cli]'
  tags: '[s32ct, headless, configuration-tools, facade, dcf, dcd, code-generation]'
---

# S32CT DCF - Headless Facade

Thin per-tool facade over the generic `s32ct-cli` skill that exposes only the
flags relevant to the **DCF** (Device Configuration Format) tool of S32
Configuration Tools. This skill fronts the `nxp_s32ct_configure` MCP tool with
`action="dcf"`. All shared launcher plumbing, validation, and auto-retry
behavior is inherited from `s32ct-cli`.

## What DCF is

DCF has the same purpose as DCD - generate an image using the format and
constraints in the Boot ROM reference manual - but instead of write/check/nop
commands it uses **records**. A DCF record is a 64-bit double-word made of a
control word (a pointer to a 32-bit DCF client register, via a 15-bit chip
select + 15-bit address field) and a data word (the value written to that
client). DCF is only available on a limited set of processors.

## How DCF relates to DCD

DCF is **not** a standalone headless tool. The S32CT DCD plugin registers a
single headless tool (`id="DCD"`, `commandline_app=CmdApplication`) whose
command-line application drives DCD, DCF **and** DCA. At runtime the active
variant is chosen automatically from the loaded processor
(`DCDUtils.getActiveToolAndController` ->
`isDCDProcessorSelected` / `isDCFProcessorSelected` / `isDCAProcessorSelected`).

Consequences:
- The `dcf` action pre-fills `tool_name="DCD"` under the hood - the launcher
  is invoked with `-HeadlessTool DCD`, and the tool responds as DCF when the
  `.mex` targets a DCF-capable SoC.
- The CLI grammar is identical to DCD: `-ImportBin`, `-ValidateConfiguration`
  (surfaced as `validate=True`), and the export verbs `-ExportBin`,
  `-ExportC`, `-ExportAll` (which also emits `-ExportMEX` in the framework).
- There are no DCF-only CLI flags beyond the shared import / validate /
  export verbs; record editing is a GUI-side / XML concern.

## When to use

Use this skill when, on a DCF-capable SoC, you need to:
- Import a binary DCF image into a `.mex` via `-ImportBin`.
- Validate a DCF configuration.
- Export DCF artifacts: binary, C source, or all.

**Migration note:** There has never been a standalone `dcf` MCP tool. Use the
unified `nxp_s32ct_configure` dispatcher's `dcf` action (or `action="dcd"`
directly, which is equivalent since both map to `-HeadlessTool DCD`).

Do **not** use this skill for:
- Cross-tool operations combining flags from multiple tools -> use
  `s32ct-cli` (action="cli").
- DCD command (write/check/nop) or DCA structure configuration - use
  `s32ct-dcd-facade` / `s32ct-dca-facade`.
- IVT / QuadSPI / eFUSE binary handling - use the matching facade.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `nxp_s32ct_configure` | `nxp_s32ct_configure(action="dcf", ...)` |
| Resource | `skill://nxp_s32ct/s32ct-dcf-facade` | Auto-loaded on trigger |

## Quickstart

### 1. Load or bootstrap a `.mex`

```
Tool:    nxp_s32ct_configure
Action:  dcf
Input:   project_path="<path>.mex"   # OR empty_config=True + mcu + sdk_version
Output:  {exit_code, command, stdout_tail, stderr_tail, values, summary}
```

### 2. Apply DCF-specific modifications and export

```python
nxp_s32ct_configure(
    action="dcf",
    project_path="<path>.mex",
    import_bin="<dcf>.bin",        # -ImportBin
    validate=True,                 # -ValidateConfiguration
    export_kind="ExportBin",       # or ExportAll|ExportC|ExportMEX
    output_dir="<output-dir>",
)
```

### 3. Verify the export

Check that `output_dir` contains the expected artifacts (e.g.
`dcfBinaryImage`, `dcfCImage.c`) and `exit_code == 0`.

## Inputs

### Mode (mutually exclusive)
- `project_path` - existing `.mex` to load via `-Load`.
- `empty_config` - if `True`, `-EmptyConfig`; requires `mcu` + `sdk_version`.
- `config_name` - `-ConfigName <...>`.

### Tool-specific
- `import_bin` - DCF binary via `-ImportBin`.
- `validate` - run `-ValidateConfiguration` on the configuration.

### Export
- `export_kind` in {`ExportAll, ExportBin, ExportC, ExportMEX`}.
- `output_dir` - required when `export_kind` is set.

### Launcher / plumbing (shared with `s32ct-cli`)
- `data_dir` (`-data <workspace>`), `extra_args`, `s32ct_launcher`,
  `launcher_ini`, `timeout_s` (default 600).

## Output

Same as `s32ct-cli`:
`{ exit_code, command, stdout_tail, stderr_tail, values, summary }`.

## Guardrails

**Scope**
- Only drives the **dcf** action of `nxp_s32ct_configure` (which maps to
  `-HeadlessTool DCD`). For cross-tool workflows use `s32ct-cli`
  (action="cli") instead.
- Applies only to SoCs that provide the DCF variant. On a DCD/DCA SoC the
  same launcher call operates on DCD/DCA instead - confirm the target SoC.
- Does not modify hardware or program devices.

**Destructive actions**
- Exports overwrite files in `output_dir`. Confirm the target directory
  is safe or empty before invoking with `export_kind` set.

**Refuse-and-escalate**
- Missing `project_path` AND missing `empty_config`/`mcu`/`sdk_version`
  combination -> ask the user which mode they want.
- Unknown `export_kind` value -> list the allowed enum values and ask.
- Retryable `IllegalStateException` -> auto-retry once, then escalate.

## Validation loop

1. `exit_code == 0`.
2. `output_dir` contains the expected artifacts for the chosen `export_kind`.
3. If `validate=True`, check `stdout_tail` / `summary` for validation OK
   ("No problems found").

## Out of scope

- Interactive GUI operations - use S32 Configuration Tools directly.
- Cross-tool operations combining multiple tools' flags - use `s32ct-cli`.
- Distribution portability (`desktop` vs `integrated_s32ds`) - handled
  transparently by the MCP; see `s32ct-distributions`.

## See Also

- `s32ct-cli` - generic dispatcher with the full ~50-parameter surface.
- `s32ct-dcd-facade`, `s32ct-dca-facade` - sibling Device-Configuration tool
  facades that share the same DCD `CmdApplication` and CLI grammar.
- `s32ct-distributions` - launcher selection.
