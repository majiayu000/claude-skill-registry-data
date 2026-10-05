---
name: s32ct-distributions
description: >
  Explains how S32 Configuration Tools ships on a host (standalone desktop
  vs. S32DS-integrated), what the MCP auto-discovers at startup, and how
  each distribution's headless CLI prefix differs. Use when the user asks
  "which S32CT is installed", "why does the command hang on -data",
  "toolsc.exe vs s32dsc.exe", or when hand-building a raw command line.
  Every other s32ct-* skill assumes this reference.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  tags: '[s32ct, headless, configuration-tools, distributions, launcher, reference]'
---

# S32CT Distributions

S32 Configuration Tools (S32CT) ships in two interchangeable forms on the
same host: the standalone **desktop** product and the **S32DS-integrated**
Eclipse plugin set. Both speak the same headless CLI grammar, but the
launcher binary, the launcher `.ini`, and the mandatory-argument shape
differ. The MCP auto-discovers both at startup and emits the correct
prefix transparently, so most agents never have to think about it. This
skill is the canonical reference for the underlying behaviour.

## When to use

Use this skill when:
- The user asks which S32CT distribution is active or installed.
- A raw command line hangs, exits with code 13, or fails without an
  error message.
- Hand-building a headless invocation outside the typed MCP wrappers.
- Writing host-portable recipes that must survive on either variant.

Do **not** use this skill for:
- Running a code-generation workflow - use `s32ct-generate-code`.
- Probing the installed version - use `s32ct-get-version`.
- Bootstrapping a GTM use-case - use `s32ct-gtm-create-from-usecase`.

## The two distributions

| Attribute | `desktop` (standalone) | `integrated_s32ds` (Eclipse plugin) |
|---|---|---|
| Typical install path | `C:/NXP/S32ConfigTools.<release>` | `C:/NXP/S32DS.<x>.<y>` |
| Launcher | `toolsc.exe` | `s32dsc.exe` |
| Launcher `.ini` | `tools.ini` | `s32ds.ini` |
| MCU data root | `%ProgramData%/NXP/mcu_data_<release>` | `<install>/eclipse/mcu_data` |
| `-data <workspace>` | optional (auto-retry on error) | **mandatory** |
| Shipped as | the S32CT product itself | part of S32 Design Studio |

Both ship every documented headless tool (Pins, Clocks, Peripherals, DCD,
IVT, eFUSE, GTM, QuadSPI, FFC) and accept the same `-HeadlessTool`,
`-Load`, `-EmptyConfig`, `-MCU`, `-SDKVersion`, `-ExportAll`,
`-ApplyUseCase`, `-SetValue`, `-GetValue` arguments.

The MCU data package shipped with each distribution **may differ in
content** - for example, some MCU folders carry GTM use-case `.mex`
templates only in the desktop variant. Always discover use-cases via
`nxp_s32ct_execute_action(action_name="s32ct.gtm_list_usecases", params={"mcu": ...})`
rather than assuming a fixed file layout.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `s32ct.env_status` | Returns active `distribution`, `version`, `selection_reason` |
| MCP tool | `s32ct.env_installs` | Lists every discovered install; flags which is selected |
| MCP tool | `s32ct.env_version` | Distribution-aware version probe |
| Resource | `s32ct://info` | JSON status + `discovered_installs` array |
| Resource | `skill://nxp_s32ct/s32ct-distributions` | Auto-loaded on trigger |

## Headless CLI prefix per distribution

Both prefixes come verbatim from the *S32CT - DS Command Line* PDF
(NXP, 2025-11-21). The MCP emits exactly these forms.

### Desktop (standalone)

```
toolsc.exe -noSplash \
          --launcher.ini <tools.ini> \
          -application com.nxp.swtools.framework.application \
          -consoleLog \
          <tool commands>
```

- `--launcher.ini <path>` is space-separated (matches the product doc).
- `-consoleLog` forces stdout/stderr flow.
- `-data <workspace>` is **not** required. The MCP auto-retries with a
  temp workspace only if a call reports
  `instance data location has not been specified`.

### Integrated S32DS

```
s32dsc.exe -noSplash \
          --launcher.ini <s32ds.ini> \
          -application com.nxp.swtools.framework.application \
          -consoleLog \
          -data <workspace> \
          <tool commands>
```

- `-noSplash` comes **first**.
- `--launcher.ini <path>` is **space-separated**, not `=`-joined.
- `-data <workspace>` is **mandatory** - without it the Eclipse launcher
  blocks on the interactive workspace-selection dialog and hangs
  silently.
- The MCP injects a stable per-host workspace automatically
  (`%LOCALAPPDATA%/S32CT-MCP/workspace` on Windows,
  `$HOME/.cache/s32ct-mcp/workspace` on POSIX).

### Why the difference matters

- Integrated `s32dsc.exe` invoked **without** `-data <ws>` -> launcher
  hangs on the workspace dialog. No error output.
- Wrong launcher + wrong `.ini` combination -> Equinox launcher rejects
  the arguments and exits with code 13 (or similar).

## MCP discovery and selection

At startup, `mcp_s32ct` runs `discover_installs()` which scans the
standard NXP roots (`C:/NXP`, `%ProgramFiles%/NXP`, `%LOCALAPPDATA%/NXP`,
`/opt/nxp`, `$HOME/NXP`) one level deep, identifies every install
matching either layout, and stores them in a stable ordering.
`select_install()` then applies:

1. **Explicit YAML override** (`s32ct.settings.installation_path`) wins.
   Accepted shapes:
   - Desktop root - `C:/NXP/S32ConfigTools.2026.R1.9`
   - S32DS root - `C:/NXP/S32DS.3.6.5` *(recommended for integrated)*
   - S32DS eclipse subfolder - `C:/NXP/S32DS.3.6.5/eclipse` *(advanced)*
2. Otherwise the newest discovered `desktop` install.
3. Otherwise the newest discovered `integrated_s32ds` install.
4. Otherwise the server still starts; the next tool call fails with an
   actionable error.

`S32CTContext` carries the resolved `distribution` (`"desktop"` |
`"integrated_s32ds"` | `"unknown"`) and the launcher pair. Every tool
implementation calls `_build_prefix(launcher, tools_ini, distribution)`
which emits the right form per the table above.

## Quickstart

### 1. Confirm the active distribution

```python
nxp_s32ct_execute_action(action_name="s32ct.env_status", params={})
# -> {"distribution": "desktop", "version": "2026.R1.9", ...}
```

### 2. List all discovered installs (optional)

```python
nxp_s32ct_execute_action(action_name="s32ct.env_installs", params={})
```

### 3. Build a raw command line by hand (only if unavoidable)

Take the `distribution`, `launcher`, and `tools_ini` from step 1 and pick
the matching prefix from the tables above. Append the `<tool commands>`
portion exactly as documented in the *S32CT - DS Command Line* PDF - it
is identical across both distributions.

Prefer the typed wrappers (`nxp_s32ct_execute_action` with the appropriate
`action=` / `tool_name=`) whenever possible; they are portable across
both distributions.

## Guardrails

**Scope**
- Read-only reference. This skill does not launch any process or write
  any file.

**Destructive actions**
- None.

**Refuse-and-escalate**
- If `s32ct.env_status` reports `distribution == "unknown"` and no
  install is discovered, stop and ask the user to install S32CT or to
  set `s32ct.settings.installation_path` explicitly.

## Validation loop

1. `nxp_s32ct_execute_action(action_name="s32ct.env_status", params={})` returns `distribution in {"desktop",
   "integrated_s32ds"}`. **Pass** if true.
2. The reported `launcher` file exists on disk. **Pass** if true.
3. The reported `tools_ini` (or `s32ds.ini`) file exists on disk.
   **Pass** if true.
4. `nxp_s32ct_execute_action(action_name="s32ct.env_version", params={})` returns a non-empty version string.
   **Pass** if true.

If any step fails, escalate to the user with the failing field and the
searched paths.

## Out of scope

- Installing or upgrading S32CT itself.
- Discovering installs beyond one level deep under the standard roots.
- Editing `.mex` projects, generating code, applying GTM use-cases -
  those are separate skills.

## See Also

- Related skills: `s32ct-get-version`, `s32ct-generate-code`,
  `s32ct-gtm-create-from-usecase`.
- Terminology tip: "integrated S32CT" / "S32CT inside Design Studio"
  -> `integrated_s32ds`; "standalone tool" / "S32ConfigTools" ->
  `desktop`.
- A host can have **both** distributions installed simultaneously; only
  one is active at a time (the `selected` one). Use
  `s32ct.env_installs` to inspect the full set.
