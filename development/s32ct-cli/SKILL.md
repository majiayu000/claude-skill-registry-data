---
name: s32ct-cli
description: >
  Generic dispatcher wrapper around the S32 Configuration Tools headless CLI.
  Fronts all 9 S32CT tools (Pins, Clocks, Peripherals, DCD, IVT, eFUSE, GTM,
  QuadSPI, FFC) behind the unified `nxp_s32ct_execute_action(action_name="s32ct.configure_cli", params={...})`
  entry point. Trigger phrases include "run S32CT headless", "call -SetValue",
  "-GetValue", "-ImportBin", "-ImportBlob", "-ExportBlob", "-ExportMEX",
  "-ExportAB", "-ValidateConfiguration", "apply use-case then tweak",
  "modify a .mex programmatically", "read data-model values back". Also the
  fallback for headless flags no facade wraps (`-ApplyUseCase`, the
  `-Import*` and `-Migrate*` families, `extra_args`) - see
  `references/tool-flags.md` for the full matrix. Do NOT use for read-only
  lookups (`s32ct-*-info`), single-tool work an `s32ct-*-facade` covers,
  code generation (`s32ct-generate-code`), or scaffolding a new `.mex`
  (`s32ct-generate-mex-config`). Works on both `desktop` and
  `integrated_s32ds` distributions.

license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-distributions]'
  tags: '[s32ct, headless, cli, dispatcher, configuration, code-generation]'
---

# S32CT CLI Dispatcher (full surface)

Generic, fully-parameterized wrapper around the S32 Configuration Tools
headless CLI covering all 9 tools. Superset of `s32ct-generate-code` and
`s32ct-gtm-create-from-usecase`. Post 16->5 tool refactor, the standalone
`cli` MCP tool no longer exists - this is the `cli` action of the unified
`nxp_s32ct_execute_action` dispatcher. Every other action (`pins`, `clocks`,
`peripherals`, `dcd`, `ivt`, `efuse`, `gtm`, `quadspi`, `ffc`,
`generate_code`) is a thin pre-fill over the same implementation.

## When to use

Use this skill when:
- Modifying an existing `.mex` programmatically (`-SetValue`, `-ExportMEX`).
- Reading live data-model values back (`-GetValue`).
- Combining `-ApplyUseCase` with fine-grained `-SetValue` in one run.
- Driving any of the 9 tools with a flag the per-tool skill doesn't expose
  (e.g. `-ValidateConfiguration`, `-ImportBlob`, `-ExportAB`).
- Importing binary blobs, IVT images, DCD images, QuadSPI images.
- Exporting application bootloader, blob, DDRC, FSS firmware, ELF, ARXML,
  JSON, source, HTML report, registers dump, CSV, MEX.
- Migrating Peripherals-tool components to a target SDK version.
- Applying custom copyright headers and output-path overrides.

Do **not** use this skill for:
- Plain regeneration of one tool from an existing `.mex` - use
  `nxp_s32ct_execute_action(action_name="s32ct.generate_code", params={...})` (simpler schema).
- Starting from a GTM use-case template - use
  `nxp_s32ct_execute_action(action_name="s32ct.gtm_create_from_usecase", params={...})`.
- Multi-tool runs in one invocation - only one tool block per call; loop
  the caller instead.
- Read-only data-model inspection - see `s32ct-peripherals-info`,
  `s32ct-pins-info`, `s32ct-clocks-info`.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Action | Load-and-edit `.mex` | `nxp_s32ct_execute_action(action_name="s32ct.configure_cli", params={"project_path": ..., "tool_name": ..., "set_values": [...], "export_kind": "ExportMEX", "output_dir": ...})` |
| Action | Empty-config bootstrap | `nxp_s32ct_execute_action(action_name="s32ct.configure_cli", params={"empty_config": True, "mcu": ..., "sdk_version": ..., "tool_name": ...})` |
| Action | Read values | `nxp_s32ct_execute_action(action_name="s32ct.configure_cli", params={"project_path": ..., "tool_name": ..., "get_values": [...]})` |
| Action | Validate headlessly | `nxp_s32ct_execute_action(action_name="s32ct.configure_cli", params={"project_path": ..., "tool_name": ..., "validate": True})` |
| Action | Import + export | `nxp_s32ct_execute_action(action_name="s32ct.configure_cli", params={..., "import_bin": ..., "export_kind": ..., "output_dir": ...})` |
| Reference | Per-tool flag matrix | `references/tool-flags.md` |

## Quickstart

1. Modify an existing GTM project and persist as `.mex`:
   ```python
   nxp_s32ct_execute_action(
       action_name="s32ct.configure_cli",
       params={
           "project_path": "C:/out/gtm_demo/S32E2XX.mex",
           "tool_name": "GTM",
           "set_values": ["tom0_ch1_en=true", "tom1_ch2_en=true"],
           "export_kind": "ExportMEX",
           "output_dir": "C:/out/gtm_demo",
       },
   )
   ```

2. Read data-model values back:
   ```python
   nxp_s32ct_execute_action(
       action_name="s32ct.configure_cli",
       params={
           "project_path": "C:/out/gtm_demo/S32E2XX.mex",
           "tool_name": "GTM",
           "get_values": ["atom0_ch2_en", "atom0_ch2_period"],
       },
   )
   ```

3. Apply a use-case AND tweak a value in one run:
   ```python
   nxp_s32ct_execute_action(
       action_name="s32ct.configure_cli",
       params={
           "empty_config": True,
           "mcu": "S32E288",
           "sdk_version": "PlatformSDK_S32ZE",
           "tool_name": "GTM",
           "apply_use_case": "C:/uc/atom_inverted_pwm.mex",
           "set_values": ["gtm_codegen=true", "atom0_ch2_period=0xBB80"],
           "export_kind": "ExportAll",
           "output_dir": "C:/out/gtm_custom",
       },
   )
   ```

4. Validate an existing IVT configuration:
   ```python
   nxp_s32ct_execute_action(
       action_name="s32ct.configure_cli",
       params={
           "project_path": "C:/projects/bldc/bldc.mex",
           "tool_name": "IVT",
           "validate": True,
       },
   )
   ```

5. Import a binary IVT image and export blob:
   ```python
   nxp_s32ct_execute_action(
       action_name="s32ct.configure_cli",
       params={
           "empty_config": True,
           "mcu": "S32S247TV",
           "sdk_version": "s32sdk_s32s_rtm_100",
           "tool_name": "IVT",
           "import_bin": "C:/in/ivt_image.bin",
           "auto_align": "0x34000000",
           "export_kind": "ExportAll",
           "output_dir": "C:/out/ivt_export",
       },
   )
   ```

See `references/tool-flags.md` for the complete flag matrix and 10 worked
examples covering GTM, IVT, eFUSE, FFC, Peripherals, Pins.

## Shared parameters (framework level)

Independent of `tool_name`:

| Name | Maps to |
|------|---------|
| `project_path` OR `empty_config`+`mcu`+`sdk_version` | `-Load` / `-EmptyConfig -MCU -SDKVersion` (mutually exclusive) |
| `config_name` | `-ConfigName` |
| `custom_copyright` | `-CustomCopyright` |
| `output_path_overrides` | `-OutputPathOverrides` |
| `data_dir` | `-data <workspace>` (auto-injected on retry) |
| `extra_args` | verbatim tail - escape hatch |
| `s32ct_launcher`, `launcher_ini` | launcher / ini overrides |
| `timeout_s` (default 600) | process timeout |

## Export verbs

`export_kind` in `{ ExportAll, ExportSrc, ExportHTML, ExportCSV,
ExportRegisters, ExportMEX, ExportBin, ExportC, ExportBlob, ExportAB,
ExportPointers, ExportDDRC, ExportFssFw, ExportConfig, ExportELF,
ExportARXML, ExportJSON }`. When set, `output_dir` is required (created
if missing). `ExportMEX` is the supported way to persist `.mex` changes.

## Configuration

```yaml
# One tool block per invocation. tool_name in
#   Pins | Clocks | Peripherals | DCD | IVT | eFUSE | GTM | QuadSPI | FFC
# enable_tool defaults to true when tool_name is set.
```

## Guardrails

**Scope** - Writes files under `output_dir` when an export verb is set, and
may overwrite prior outputs there. Does not modify the loaded `project_path`
in place; `.mex` changes are persisted via `export_kind="ExportMEX"`. Does
not touch the live target.

**Destructive actions** - `ExportMEX` overwrites any existing `.mex` of the
same name in `output_dir`. Import verbs (`ImportBin`, `ImportBlob`,
`ImportAB`, `ImportDDRC`, `ImportARXML`, `ImportJSON`) mutate the in-memory
data model before export.

**Refuse-and-escalate** - Refuse when `project_path` and `empty_config` are
both set (mutually exclusive), when `empty_config=True` without `mcu` +
`sdk_version`, when `export_kind` is set without `output_dir`, when an
enum value (`tool_name`, `export_kind`, `update_filepaths`, `ivt_filter`,
`file_type`) is outside its allowed set, or when any file input path does
not exist. In each case emit a clear error before spawning the launcher
and list the allowed set.

**Launcher behavior** - Portable across both S32CT distributions.
`desktop` uses `toolsc.exe`; `integrated_s32ds` uses `s32dsc.exe` and
requires `-data <workspace>` (auto-injected). On
`IllegalStateException: instance data location has not been specified`
the wrapper retries once with a temp `-data`; second failure surfaces
the raw exit code. See `s32ct-distributions` for details.

## Output shape

Returns `{ exit_code, command, stdout_tail, stderr_tail, values, summary }`
as a JSON string. `values` is populated only when `get_values` is non-empty;
the parser handles bordered tables, pipe rows, `key=value`, and
whitespace-aligned forms. Non-zero `exit_code` yields a clear failure
`summary` plus truncated stderr.

## Validation loop

1. Confirm exactly one of `project_path` or `empty_config=True` is set.
2. If `empty_config=True`, confirm `mcu` and `sdk_version` are supplied.
3. Confirm every file input (`apply_use_case`, `import_*`, `raw_binary`,
   `clock_config_data`, `mini_paco_structure`, `pre_defined_data`,
   `custom_copyright`, `output_path_overrides`, `sdk_path`,
   `import_project`) exists on disk.
4. Confirm all enum-valued parameters match their allowed set.
5. Confirm `output_dir` is set when `export_kind` is set.
6. Run the launcher. If exit is non-zero and stderr contains
   `IllegalStateException: instance data location has not been specified`,
   retry once with a temporary `-data` directory.
7. Pass criterion: `exit_code == 0` AND (if `export_kind` was set) the
   expected output exists under `output_dir` AND (if `get_values` was
   non-empty) `values` contains one entry per requested id.

## Out of scope

- Multi-tool orchestration in one call (loop the caller).
- Modifying the live target device (use `nxp_s32flashtool`).
- Interactive GUI operations.
- Editing pointer addresses inside IVT `<ivt_pointer>` rows via
  `-SetValue` - those must be edited in the `.mex` XML directly; see
  `s32ct-ivt-build-blob`.

## See Also

- `references/tool-flags.md` - Per-tool flag matrix for all 9 tools
  (Pins, Clocks, Peripherals, DCD, IVT, eFUSE, GTM, QuadSPI, FFC), the
  full command-chain build order, and 10 worked examples.
- Related skills:
  - `s32ct-generate-code` - simpler regen from an existing `.mex`.
  - `s32ct-gtm-create-from-usecase` - GTM use-case starter.
  - `s32ct-peripherals-info`, `s32ct-pins-info`, `s32ct-clocks-info` -
    read-only data-model inspectors.
  - `s32ct-ivt-build-blob` - coordinated `.mex` edits for `-ExportBlob`.
  - `s32ct-distributions` - `desktop` vs `integrated_s32ds` launcher
    conventions.
