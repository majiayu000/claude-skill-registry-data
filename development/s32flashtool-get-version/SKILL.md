---
name: s32flashtool-get-version
description: Safely retrieve the version or identification string of the installed S32FlashTool and of the MCP server.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32flashtool
  depends_on: '["s32flashtool-agent-rules-minimal", "s32flashtool-workflow-index"]'
  tags: '["s32flashtool", "diagnostic", "version", "read-only"]'
---

# Get S32FlashTool Version

Safe, read-only probe for the installed S32FlashTool CLI and/or the MCP server
identity. No target access, no board required, no side effects.

## When to use

- Verify S32FlashTool is installed and identify its version/build.
- Verify the MCP server is reachable and check installed-vs-validated version.
- First cheap check before any hardware workflow (port discovery, flash ops,
  GUI/RPC automation).

**Not** for target connectivity, serial-boot state, MCU identity, or
target/algorithm compatibility. Use `s32flashtool-read-mcuid`,
`s32flashtool-list-available-serial-communication-interfaces`, or
`s32flashtool-supported-devices-per-platform` for those.

## Do not use this skill for

Do **not** use this skill to:
- verify target connectivity
- verify serial boot mode
- identify the MCU on the board
- prove that a target/algorithm combination is supported
- replace a communication test such as `ping`, `hello`, or `mcuid`

If the user wants hardware communication validation, use the appropriate connectivity or operation skill after this one.

## Shared references
- Apply shared rules from `s32flashtool-agent-rules-minimal/SKILL.md`.
- Use `s32flashtool-workflow-index/SKILL.md` to select the correct operation skill when version lookup is only one step in a larger workflow.

## Which action to call

`get_runtime_info` is the **default**. `cli_get_version` is a **fallback**
when only the raw CLI banner is wanted or when isolating the CLI layer for
debugging.

Cost note: both actions spawn the CLI once when `sft_folder` is supplied.
`get_runtime_info` is a strict superset at the same cost — it returns MCP
identity, `target_tool_version`, and a `tool_status: matches | mismatch`
verdict in addition to the CLI banner.

| Question | Call |
|---|---|
| Any version info; workflow starting soon | `get_runtime_info` with `sft_folder` if known, else without |
| MCP identity only, no install known | `get_runtime_info` (no `sft_folder`) — cheap, no CLI spawn |
| Raw CLI banner only (debug / narrow consumer) | `cli_get_version` with `sft_folder` |

## Parameters

- `sft_folder`: absolute path to the S32FlashTool installation root
  (e.g. `C:\NXP\S32FlashTool_2.4.3`).
  - `get_runtime_info`: optional. If not specified, only the MCP manifest is returned.
  - `cli_get_version`: optional. If not specified, falls back to the value configured in the MCP settings.

## Example responses

`get_runtime_info` with `sft_folder`:

```json
{
  "mcp_server_name": "s32flashtool",
  "mcp_server_version": "1.0.0",
  "target_tool_version": "2.4.3",
  "installed_tool": {
    "detected": true,
    "version": "2.4.3",
    "installation_path": "C:\\NXP\\S32FlashTool_2.4.3",
    "docs_path": "C:\\NXP\\S32FlashTool_2.4.3\\doc",
    "tool_status": "matches",
    "banner": "S32 Flash Tool 2.4.3. Build 260812. Copyright 2019 - 2026 NXP"
  }
}
```

`cli_get_version`:

```json
{
  "sft_folder": "C:\\NXP\\S32FlashTool_2.4.3",
  "version": "S32 Flash Tool 2.4.3. Build 260812. Copyright 2019 - 2026 NXP"
}
```

Report the version verbatim and label its source, e.g.
`Installed CLI: S32 Flash Tool 2.4.3, build 260812` or
`MCP s32flashtool 1.0.0, validated against tool 2.4.3 (installed tool matches)`.
## Validation loop

A successful execution normally returns:
- a version string, build string, or identification string
- without requiring any target communication

Agents should treat this as evidence of tool availability only.

It does **not** validate:
- serial boot mode
- board power or wiring
- COM port correctness
- target reachability
- flash algorithm compatibility

## Error handling

- Report `status`, `status_text`, and any message verbatim; do not guess a version.
- If `cli_get_version` fails, confirm `sft_folder` is correct and points at the
  installation root.
- If `get_runtime_info` returns `tool_status: mismatch`, warn the user that the
  installed tool differs from the MCP-validated version; behavior may deviate
  from documented defaults.
- A version-query failure says nothing about target reachability or wiring.

## Guardrails

- Read-only, diagnostic. Never invokes a writing tool.
- Success proves tool availability only — not board power, port correctness,
  serial-boot state, or target reachability. Follow up with a communication or
  operation skill for hardware validation.
