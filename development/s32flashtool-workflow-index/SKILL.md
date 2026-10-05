---
name: s32flashtool-workflow-index
description: Compact routing index for choosing the correct S32FlashTool operation skill and execution mode.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32flashtool
  depends_on: '["s32flashtool-agent-rules-minimal"]'
  tags: '["s32flashtool", "routing", "index", "decision-matrix"]'
---

# S32FlashTool Workflow Index

Use this skill only to route a user request to the correct S32FlashTool skill.
Apply baseline execution and anti-guessing rules from
`s32flashtool-agent-rules-minimal/SKILL.md`.

## When to use

Use this skill when you need to choose:
- the correct **operation skill**
- whether the request is primarily **discovery**, **read-only**, **destructive**, or **GUI/RPC**
- whether `s32flashtool-rpc-api` is needed as a **companion** transport skill

## When not to use

Do not execute operations from this skill. Once routing is done, switch to the selected operation skill.

## Quickstart

On first entry into this skill pack in a session:
1. `s32flashtool-agent-rules-minimal/SKILL.md`
2. `s32flashtool-workflow-index/SKILL.md`
3. the selected operation skill
4. the selected mode reference (`references/CLI.md` or `references/GUI.md`) if needed
5. `s32flashtool-rpc-api/SKILL.md` only when GUI/RPC mode is selected
6. `s32flashtool-evidence-disciplined-technical-validation/SKILL.md` only when correctness or proof matters

Do not re-read already loaded skill/resource URIs in the same session.

## Routing rules

- If the request is ambiguous, route first to:
  - `s32flashtool-basic-use` for general help
  - `s32flashtool-identify-user-board` when the board or family is unknown
  - `s32flashtool-discover-hardware-setup` when interface, boot mode, or connection details are unclear
- If the request is informational, prefer read-only skills before any state-changing action.
- If the request changes device state, route to the matching destructive skill and require confirmation there.
- If the user explicitly asks for GUI automation or GUI-side actions, pair the selected operation skill with `s32flashtool-rpc-api`.
- Never use `s32flashtool-rpc-api` as the sole destination for a real operation.

## Decision matrix

| User intent | Canonical skill | Mode | Primary action(s) | Destructive | Discovery first |
|---|---|---|---|---|---|
| General help / getting started | `s32flashtool-basic-use` | Discovery | `search_actions` | no | usually |
| Identify board / device | `s32flashtool-identify-user-board` | Discovery | discovery workflow | no | no |
| Discover hardware setup | `s32flashtool-discover-hardware-setup` | Discovery | discovery workflow | no | no |
| Check supported devices / algorithms / interfaces | `s32flashtool-supported-devices-per-platform` | CLI discovery | `list_platform_files` | no | no |
| List ports / interfaces | `s32flashtool-list-available-serial-communication-interfaces` | CLI | `cli_build_list_interfaces` + `cli_execute` | no | maybe |
| Read CLI help / arguments | `s32flashtool-read-command-line-arguments` | CLI | `cli_execute` | no | no |
| Get installed version | `s32flashtool-get-version` | Discovery | `cli_execute` | no | no |
| Get flash ID | `s32flashtool-get-flash-id` | CLI or GUI/RPC | `cli_build_fid` + `cli_execute`, `model.setFullConfigGetFlashId` + `flash.clickGetId` | no | yes |
| Read MCU ID | `s32flashtool-read-mcuid` | CLI | `cli_build_mcuid` + `cli_execute` | no | yes |
| Read flash contents | `s32flashtool-read-flash` | CLI or GUI/RPC | `cli_build_fread` + `cli_execute`, `model.setFullConfigDownloadFromDevice(ToFile)` + `flash.clickDownloadFromDevice(ToFile)` | no | yes |
| Compare CRC against flash | `s32flashtool-compute-crc-and-compare-to-flash` | CLI | `cli_build_fcrc` + `cli_execute` | no | yes |
| Read RCON / EEPROM | `s32flashtool-read-rcon` | CLI or GUI/RPC | `cli_build_fread` + `cli_execute`, `model.setFullConfigDownloadFromDevice(ToFile)` + `flash.clickDownloadFromDevice(ToFile)` | no | yes |
| Write RCON / EEPROM | `s32flashtool-write-rcon` | GUI/RPC or CLI fallback | `model.setFullConfigUploadHexToRcon` + `flash.clickUploadFileToDevice`, `cli_build_fprogram` + `cli_execute` | yes | yes |
| Execute in SRAM | `s32flashtool-sram` | GUI/RPC or CLI | `model.setFullConfigSram`, `cli_build_boot` + `cli_execute` | no persistent flash write | yes |
| Program file to flash | `s32flashtool-upload-file-to-flash` | CLI or GUI/RPC | `cli_build_fprogram` + `cli_execute`, `model.setFullConfigUploadFileToDevice` + `flash.clickUploadFileToDevice` | yes | yes |
| Erase flash / range | `s32flashtool-erase-flash` | CLI or GUI/RPC | `cli_build_ferase` + `cli_execute`, `model.setFullConfigEraseFlashMemory` + `flash.clickEraseMemoryRange` | yes | yes |
| GUI transport / session / model / action handling | `s32flashtool-rpc-api` | GUI/RPC only | `gui_*` actions | depends | maybe |
| Evidence-driven validation | `s32flashtool-evidence-disciplined-technical-validation` | Meta | N/A | no | no |

## Output contract

Return:
- exactly one selected operation skill, or a short disambiguation prompt
- the recommended mode when relevant: `CLI` or `GUI/RPC`
- `s32flashtool-rpc-api` only as a companion when GUI/RPC mode is selected

## Guardrails

- This skill is routing-only; do not invoke MCP tools from here.
- Do not invent skill names.
- Do not route directly to `s32flashtool-rpc-api` as the sole operation skill for a real device action.
- If the request is ambiguous, ask a focused disambiguation question before routing.

## Out of scope

- Executing device operations
- Per-operation confirmation logic
- Transport payload details
- Detailed CLI or GUI sequences
