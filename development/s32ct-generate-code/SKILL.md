---
name: s32ct-generate-code
description: >
  Triggers headless code generation in S32 Configuration Tools for a
  single specific tool (Pins, Clocks, Peripherals, DCD, IVT, eFUSE, GTM,
  QuadSPI, or FFC) of an existing .mex project and exports the
  regenerated files to a target folder. Use when the user says
  "regenerate the pin mux", "refresh the clocks code", "export the
  peripherals HTML report", or wants to apply .mex edits to disk in a
  scoped way. Fronts nxp_s32ct_execute_action(action_name="s32ct.generate_code", params={...})
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  depends_on: '[s32ct-distributions]'
  tags: '[s32ct, headless, configuration-tools, code-generation, configuration]'
---

# S32CT Generate Code (single tool)

Regenerates driver / init code for **one** S32CT tool of an existing
`.mex` project and exports the result to a target folder. Drives the
official S32CT command-line interface via
`-HeadlessTool <Tool>` plus an export verb
(`-ExportAll` / `-ExportSrc` / `-ExportHTML` / ...), which regenerates
before exporting. Portable across the `desktop` and `integrated_s32ds`
distributions; the MCP picks the right launcher prefix transparently
(see `s32ct-distributions`).

## When to use

Use this skill when:
- The user asks to *regenerate*, *update*, *refresh*, or *export* the
  code/report of a single configuration tool after editing the `.mex`.
- Only one tool has changed and you want a scoped, predictable run.
- Integrating S32CT code generation into an MCP-driven pipeline.

Do **not** use this skill for:
- Bootstrapping a brand-new GTM configuration from a use-case template -
  use `s32ct-gtm-create-from-usecase`.
- Editing values inside a `.mex` (`-SetValue` / `-GetValue`) - use the
  GTM `edit` sub-mode or a dedicated facade.
- Full multi-tool regeneration in one shot - call this skill per tool.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `nxp_s32ct_execute_action` | `action_name="s32ct.generate_code", params={"project_path": ..., "tool_name": ..., "output_dir": ...}` |
| Resource | `skill://nxp_s32ct/s32ct-generate-code` | Auto-loaded on trigger |

### Canonical call shape

```python
nxp_s32ct_execute_action(
    action_name="s32ct.generate_code",
    params={
        "project_path": "...",     # required, absolute path to a .mex
        "tool_name": "Pins",       # required, see enum below
        "output_dir": "...",       # required, created if missing
        "export_kind": "ExportAll",
        "enable_if_disabled": True,
        "sdk_version": "...",      # optional, e.g. "s32sdk_s32k3_rtm_402"
    },
)
```

### Inputs

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `project_path` | string | yes | Absolute path to a `.mex` file |
| `tool_name` | string | yes | Exact-case name - see enum below |
| `output_dir` | string | yes | Target folder for exported artifacts |
| `export_kind` | string | no | See enum below (default `ExportAll`) |
| `enable_if_disabled` | boolean | no | Adds `-Enable` (default `true`) |
| `sdk_version` | string | no | Value for `-SDKVersion` |
| `s32ct_launcher` | string | no | Override launcher path |
| `launcher_ini` | string | no | Override `.ini` path |

### `tool_name` enum (case-sensitive on the CLI)

`Pins`, `Clocks`, `Peripherals`, `DCD`, `IVT`, `eFUSE`, `GTM`,
`QuadSPI`, `FFC`.

### `export_kind` enum

| Value | Effect |
|-------|--------|
| `ExportAll` | Union of source + reports + tool-specific dumps (default) |
| `ExportSrc` | Regenerated `*.c` / `*.h` only |
| `ExportHTML` | HTML report of the tool configuration |
| `ExportCSV` | CSV dump (Pins) |
| `ExportRegisters` | Register dump (Clocks) |
| `ExportMEX` | Writes a `.mex` to `output_dir` (original `.mex` untouched) |

## Quickstart

### 1. Confirm S32CT is discovered

```python
nxp_s32ct_execute_action(action_name="s32ct.env_status", params={})
```

### 2. Regenerate the Pins source code

```python
nxp_s32ct_execute_action(
    action_name="s32ct.generate_code",
    params={
        "project_path": r"C:/projects/motor/motor.mex",
        "tool_name": "Pins",
        "output_dir": r"C:/projects/motor/board/generated/pins",
        "export_kind": "ExportSrc",
    },
)
```

### 3. Verify

Confirm the return status starts with `"Code generation succeeded"` and
that expected files exist under `output_dir`. See
`references/examples.md` for more scenarios and full resolved CLI
command lines.

## Behavior

1. Validate inputs: `project_path` exists and ends with `.mex`;
   `tool_name` is in the allowed set; `export_kind` is in the allowed
   set.
2. Resolve the launcher and prefix per active distribution (see
   `s32ct-distributions`).
3. Build the tail (single chain, no `;`):

   ```
   -Load "<project_path>"
   [-SDKVersion <sdk_version>]
   -HeadlessTool <tool_name>
   [-Enable]                        # if enable_if_disabled = true
   -<export_kind> "<output_dir>"
   ```

4. Spawn the process, wait for completion, capture stdout / stderr /
   exit code.
5. Map exit code + stderr signals to a human-readable status string
   including the resolved CLI and the output directory.
6. Do **not** modify the source `.mex`. Only write under `output_dir`
   (except `ExportMEX`, which writes a *new* `.mex` there).

## Guardrails

**Scope**
- Reads the input `.mex`; writes only under `output_dir`.
- Regenerates exactly the tool named in `tool_name` - no others.

**Destructive actions**
- Overwrites previously generated files under `output_dir` (`*.c`,
  `*.h`, `*.html`, `*.csv`, register dumps, or a `.mex`).
- May create `output_dir`.
- Launches an external OS process (the S32CT launcher).

**Refuse-and-escalate**
- Launcher binary or `.ini` missing -> return the searched paths and
  stop.
- `project_path` missing or not a `.mex` -> stop.
- `tool_name` / `export_kind` outside the enum -> return accepted values
  and stop.
- Non-zero exit code -> surface exit code + truncated stderr/stdout tail;
  do **not** retry silently.
- `IllegalStateException: The instance data location has not been
  specified` in stderr -> hint that `-data {workspace}` is needed (the
  MCP handles this automatically for `integrated_s32ds`).
- User is actively editing the target `.mex` -> confirm before running
  (this skill can overwrite hand-modified generated files).

## Validation loop

1. Return payload starts with `"Code generation succeeded"`. **Pass** if
   true.
2. Process exit code is `0`. **Pass** if true.
3. `output_dir` exists on disk after the call. **Pass** if true.
4. Expected artifacts for the chosen `export_kind` are present and
   non-empty under `output_dir` (e.g. at least one `*.c`/`*.h` file with
   `size > 0` for `ExportSrc`, at least one `*.html` file with `size > 0`
   for `ExportHTML`). **Pass** if the file-count and size checks both
   hold; zero-byte files count as a failure.

If any step fails, follow the *Refuse-and-escalate* rules above.

## Out of scope

- Compiling the generated code. Chain with a build skill to verify.
- Regenerating multiple tools in a single call. Loop over tools
  instead.
- Editing `.mex` values (`-SetValue`) - separate skill.
- Interacting with a live target.

## See Also

- `references/examples.md` - worked scenarios (Pins/`ExportSrc`,
  Clocks/`ExportAll`, Peripherals/`ExportHTML`) with the full resolved
  desktop CLI.
- Related skills: `s32ct-distributions` (launcher prefixes and
  `-data <workspace>` handling), `s32ct-gtm-create-from-usecase`
  (GTM-specific bootstrap from a use-case template).
