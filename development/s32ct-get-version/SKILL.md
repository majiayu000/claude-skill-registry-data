---
name: s32ct-get-version
description: >
  Retrieves the installed S32 Configuration Tools identity - product name,
  framework version, installation path, launcher binary presence - via the
  `s32ct.env_version` action. Passive, read-only
  diagnostic. Trigger phrases: "which S32CT version is installed", "S32
  Configuration Tools version", "is S32CT reachable", "S32CT installation
  path", "verify S32CT install", "check S32CT before generating code".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32ct
  tags: '[s32ct, diagnostics, lifecycle, headless, configuration-tools]'
---

# S32CT - Get Version

Read-only diagnostic that reports the identity of the S32 Configuration
Tools installation the MCP server is wired to: product name, framework /
product version, installation path, and launcher presence. Fronts the
standardized `s32ct.env_version` action. Companion
queries on the same tool: `s32ct.env_status` (full configuration snapshot)
and `s32ct.env_installs` (every install discovered on the host).

## When to use

Use this skill when:
- The user asks "which S32CT version is installed?" or "which S32CT
  path is the server using?".
- Another skill needs a precondition check before invoking a heavier
  S32CT action such as `s32ct-generate-code` or `s32ct-cli`.
- Diagnosing "S32CT not found" / "launcher missing" errors.

Do **not** use this skill for:
- Detecting whether S32CT is *currently running* - this skill is purely
  passive; it does not start any process.
- Enumerating multiple installs on the host - use
  `nxp_s32ct_execute_action(action_name="s32ct.env_installs", params={})` instead.
- Full config snapshot including MCU data root - use
  `nxp_s32ct_execute_action(action_name="s32ct.env_status", params={})` instead.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `nxp_s32ct_execute_action` | `nxp_s32ct_execute_action(action_name="s32ct.env_version", params={...})` |
| Resource | `skill://nxp_s32ct/s32ct-get-version` | Auto-loaded on trigger |

## Quickstart

### 1. Use the MCP-server default install

```
Tool:   nxp_s32ct_execute_action
Action:  s32ct.env_version
Output: human-readable string, e.g.
        "S32 Configuration Tools 1.7.0 (framework 12.4) at C:/NXP/S32ConfigTools"
```

### 2. Target a specific install (override)

```
nxp_s32ct_execute_action(
    action_name="s32ct.env_version",
    params={
        "installation_path": "C:/NXP/S32DS.3.5/eclipse",
        "s32ct_launcher": "C:/NXP/S32DS.3.5/eclipse/s32dsc.exe",
    },
)
```

### 3. Interpret the result

- Contains a version -> install is present and identifiable.
- Contains `"version = unknown"` -> install is present but version
  metadata could not be read; safe to proceed with caveats.
- Contains `"not found"` -> install missing; downstream skills will fail.
  Escalate before invoking them.

## Configuration

The skill uses the MCP server's configured launcher and installation
path unless overridden per-call. The relevant config keys are:

```yaml
# excerpt from the S32CT MCP server config
s32ct:
  installation_path: C:/NXP/S32ConfigTools
  s32ct_launcher:    C:/NXP/S32ConfigTools/toolsc.exe
  launcher_ini:      C:/NXP/S32ConfigTools/tools.ini
```

## Guardrails

**Scope**
- Read-only. The skill only inspects installation metadata; it does not
  launch any process, does not write any file, and does not touch a
  target device.
- Reports what is present on disk; does not verify that a project is
  loaded or that a generation will succeed.

**Destructive actions**
- None. This skill is passive.

**Refuse-and-escalate**
- If both `s32ct_launcher` and `launcher_ini` are missing AND the server
  default is not configured -> return a clear error naming both missing
  inputs; do not guess a path.
- If the launcher path exists but no version metadata can be read ->
  still return a successful result with `version = "unknown"` and the
  resolved path, rather than failing.
- Never start the S32CT application as a fallback probe - that would
  break the read-only guarantee.

## Validation loop

1. `nxp_s32ct_execute_action(action_name="s32ct.env_version", params={})` returns a non-empty string.
2. The string contains an installation path.
3. If the string contains `"not found"`, the caller escalates before
   invoking any other S32CT skill.

## Out of scope

- Starting S32 Configuration Tools.
- Enumerating multiple installs (use `s32ct.env_installs`).
- Runtime state such as "is a project loaded" or "is a build in
  progress".
- Writing to any file or launching any subprocess.

## See Also

- `references/examples.md` - worked examples for standalone install,
  S32DS-integrated install, and the misconfigured-path failure mode.
- `s32ct-distributions` - how the desktop vs. S32DS-integrated
  distribution is picked at server startup.
- `s32ct-cli` - the generic dispatcher; use `s32ct-get-version` as a
  quick precondition before invoking it.
