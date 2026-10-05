---
name: s32flashtool-rest-api
description: Operate the S32FlashTool GUI through its REST API using documented session, model, and action patterns.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "2.1.0"
  product: s32flashtool
  depends_on: ["s32flashtool-agent-rules-minimal", "s32flashtool-workflow-index"]
  tags: ["s32flashtool", "gui", "rest", "transport", "automation"]
---

# S32FlashTool REST API Workflow

Use the S32FlashTool GUI through its documented REST API.

This skill is **transport-oriented**, not **operation-oriented**.

It explains:
- how to probe the GUI REST session
- how to reuse an existing GUI REST session
- how to launch the GUI when needed and allowed
- how to set documented GUI model keys
- how to trigger documented GUI actions
- how to map a prepared `fullConfig*` payload to the correct final GUI action
- how to handle documented config entries that currently do **not** have a final exposed REST click action

It does **not** replace operation skills such as reading flash, programming flash, erasing flash, reading RCON, writing RCON, or SRAM execution.

## When to use this skill

Use this skill when:
- the user explicitly asked for **GUI**, **window**, or **REST** control of S32FlashTool
- an operation skill selected GUI mode
- probe or reuse an already running GUI REST session
- launch the GUI in a documented way
- set a documented GUI configuration and trigger the corresponding GUI action
- determine whether a GUI config key exists even if its final click action is not exposed through REST

## Do not use this skill alone when

Do **not** use this skill by itself when:
- the user's real question is about the meaning, prerequisites, or safety of a specific flash operation
- the operation skill is needed to determine required inputs
- GUI vs CLI selection has not been decided yet
- the user asked for a CLI command or CLI execution path

In those cases, first use the appropriate operation skill, then apply this skill if GUI mode is selected.

## Quickstart

Transport-only pattern for GUI operations. Always paired with an operation skill.

```
1. hello                              # probe existing session
   -> if fail, gui.launch, then hello
2. model.set { <documented model keys> }
3. flash.click<DocumentedFinalAction>  # per operation skill's mapping
```

Rules:
- `communicationDevice = COM` (never `UART`); put `COM15,ftdi` in `comPort`.
- Reuse an existing GUI when `hello` succeeds; do not launch twice.
- Only documented action names and model keys. No invented calls.
- Never silently switch to CLI mid-workflow.

## Scope

Use this skill for generic S32FlashTool GUI REST behavior:

- probing or launching the GUI REST session
- reusing an existing GUI REST session
- setting documented `model` keys
- calling documented GUI actions
- applying generic action/config mapping
- understanding the difference between:
  - a documented config/model entry, and
  - a documented exposed final REST action

Do not use this skill as the sole source of operation semantics.
For read/program/erase/get-id/RCON-write/SRAM workflows, also use the corresponding operation skill.

## Relationship to operation skills

This skill is transport-oriented, not operation-oriented.

Use it together with operation skills such as:
- `s32flashtool-read-flash`
- `s32flashtool_get_flash_id`
- `s32flashtool-upload-file-to-flash`
- `s32flashtool-write-rcon`
- `s32flashtool-sram`
- `s32flashtool-erase-flash`
- `s32flashtool-read-rcon`

Operation skills define:
- when to use GUI vs CLI
- required user inputs
- safety and confirmation requirements
- operation-specific payload fields
- validation guidance

This skill defines:
- how to connect to the GUI REST session
- which actions and model keys are documented
- how to map a prepared `fullConfig*` payload to the final GUI action when such an action exists
- how to treat config keys that are present in the GUI model but do not yet have a corresponding exposed click action
- generic GUI-side behavior and constraints

## Mode ownership rule

This skill does not decide whether GUI/REST or CLI should be used.
That decision belongs to the selected operation skill.

If the selected operation skill chooses GUI mode, apply this REST workflow skill.
Do not switch to CLI silently from this skill.

## Minimal rules

1. If the selected operation skill requires GUI, prefer REST over CLI.
2. Always call `hello` before launching a new GUI.
3. Reuse an existing REST session if `hello` succeeds.
4. Launch GUI only if `hello` fails and launch was requested or approved.
5. For serial/UART workflows, set `communicationDevice = COM`, not `UART`.
6. Configure the matching `fullConfig*` key before the corresponding `flash.click*` action.
7. Do not call `model.get` after every `model.set` unless readback is needed.
8. Use only documented keys and actions.
9. Do not invent undocumented GUI workflows.
10. Distinguish between a documented config entry and a documented final REST action.
11. Do not silently fall back to CLI from this skill.

## REST port resolution

If `s32flashtool_folder` is known:

1. Read `<folder>/GUI/s32ft.ini`
2. Use `com.nxp.s32ft.rest.api.port` if valid otherwise use `51234`
3. Reuse that known port for subsequent REST calls.

## Session workflow

### Standard session workflow
1. Resolve REST port
2. Call `hello`
3. If `hello` succeeds: reuse the existing GUI REST session
4. If `hello` fails and GUI launch is allowed: call `gui.launch`
5. Poll `hello` until reachable or timeout

### Generic REST workflow skeleton
After the session is available:
1. Set communication model keys as needed
2. Set the operation-specific `fullConfig*` key
3. If required for the selected destination, call `init.clickLaunchInitialization`
4. Call the matching final `flash.click*` action if one is documented and exposed

## Supported actions

Use only the following documented exposed actions:

- `hello`
- `model.get`
- `model.set`
- `init.clickLaunchInitialization`
- `flash.clickUploadFileToDevice`
- `flash.clickGetId`
- `flash.clickDownloadFromDevice`
- `flash.clickDownloadFromDeviceToFile`
- `flash.clickEraseMemoryRange`
- `gui.launch`

Do not invent action names beyond these documented actions.

## Supported model keys

Use only the following documented model keys:

- `communicationDevice`
- `comPort`
- `canVendorId`
- `canPortNumber`
- `canSerialNumber`
- `ethernetHost`
- `ethernetAdapterName`
- `ethernetAdapterDescription`
- `listeningIp`
- `dhcpFirstIp`
- `dhcpLastIp`
- `tftpEnabled`
- `dhcpEnabled`
- `tftpSourceFolder`
- `fullConfigUploadFileToDevice`
- `fullConfigUploadHexToRcon`
- `fullConfigSram`
- `fullConfigDownloadFromDeviceToFile`
- `fullConfigDownloadFromDevice`
- `fullConfigGetFlashId`
- `fullConfigEraseFlashMemory`

Do not invent model keys beyond these documented keys.

## Action-to-config mapping

After the operation skill determines the intended GUI action and prepares the correct `fullConfig*` payload, use the following mapping:

| Operation shape | Config key | Final action |
|---|---|---|
| upload / program file to flash | `fullConfigUploadFileToDevice` | `flash.clickUploadFileToDevice` |
| read from device to console / view | `fullConfigDownloadFromDevice` | `flash.clickDownloadFromDevice` |
| read from device to file | `fullConfigDownloadFromDeviceToFile` | `flash.clickDownloadFromDeviceToFile` |
| get flash ID | `fullConfigGetFlashId` | `flash.clickGetId` |
| erase flash range | `fullConfigEraseFlashMemory` | `flash.clickEraseMemoryRange` |
| write / program hex to RCON/EEPROM | `fullConfigUploadHexToRcon` |  `flash.clickUploadFileToDevice` |
| execute binary in SRAM | `fullConfigSram` | `init.clickLaunchInitialization` |

## Communication rules

### UART / serial
Use:
- `communicationDevice = COM`
- `comPort = "COM15"` or `comPort = "COM15,ftdi"`

Do not use:
- `communicationDevice = UART`

### CAN
Use the documented CAN-related model keys only.
Do not invent adapter properties beyond documented keys.

### Ethernet
Use the documented Ethernet-related model keys only.
Do not invent additional network configuration keys.

## Initialization rule

If the destination is `FLASH` or `RCON`, the workflow may require:
- `init.clickLaunchInitialization`

Operation skills should indicate when initialization is part of the valid GUI workflow.
When the selected operation skill includes initialization for the destination, do not skip it.

For `SRAM`, initialization may still be part of the GUI-side workflow depending on the board and operation sequence, but do not assume a final SRAM execute REST click action exists unless the action registry exposes one.

## Generic GUI patterns

These are reusable transport patterns, not substitutes for operation skills.
For operation-specific inputs, safety, and validation, use the corresponding operation skill.

### Generic pattern for upload-style GUI actions
1. set communication model keys as needed
2. `model.set("fullConfigUploadFileToDevice", {...})`
3. if required by destination: `init.clickLaunchInitialization`
4. `flash.clickUploadFileToDevice`

### Generic pattern for read-style GUI actions
1. set communication model keys as needed
2. `model.set("fullConfigDownloadFromDevice", {...})`
3. if required by destination: `init.clickLaunchInitialization`
4. `flash.clickDownloadFromDevice`

### Generic pattern for read-to-file GUI actions
1. set communication model keys as needed
2. `model.set("fullConfigDownloadFromDeviceToFile", {...})`
3. if required by destination: `init.clickLaunchInitialization`
4. `flash.clickDownloadFromDeviceToFile`

### Generic pattern for get-id GUI actions
1. set communication model keys as needed
2. `model.set("fullConfigGetFlashId", {...})`
3. if required by destination: `init.clickLaunchInitialization`
4. `flash.clickGetId`

### Generic pattern for erase GUI actions
1. set communication model keys as needed
2. `model.set("fullConfigEraseFlashMemory", {...})`
3. if required by destination: `init.clickLaunchInitialization`
4. `flash.clickEraseMemoryRange`

### Generic pattern for RCON write / program GUI actions
1. set communication model keys as needed
2. `model.set("fullConfigUploadHexToRcon", {...})`
3. if needed by the board workflow: `init.clickLaunchInitialization`
4. `flash.clickUploadFileToDevice`

### Generic pattern for SRAM GUI actions
1. set communication model keys as needed
2. `model.set("fullConfigSram", {...})`
3. `init.clickLaunchInitialization`

## GUI normalization note

The GUI may normalize numeric strings when storing or displaying values.
For example:
- `0x100` may appear as `100`
- `0x40` may appear as `40`

Treat this as normal GUI normalization unless the semantic value changed incorrectly.

## Readback rule for model state

- Do not use `model.get` as a mandatory verification step after every `model.set`.
- Use `model.get` only when readback is needed for debugging or explicit confirmation.
- If the user asks to inspect current GUI model state, use `model.get` with a documented key.

## Validation loop

A valid REST execution normally includes:
- successful `hello` response or successful `gui.launch` followed by `hello`
- successful `model.set` response for documented keys
- successful click response for the final GUI action

Operation-specific success validation belongs to the operation skill.
Examples:
- flash read output returned or saved to file
- file upload/program action reported as triggered/completed
- erase action reported as triggered/completed
- flash ID shown in console
- config-only preconfiguration accepted by `model.set`

## Error handling

If REST interaction fails:

1. Report the exact failure clearly.
2. Check the REST port.
3. Check whether the GUI is already running.
4. If allowed, launch the GUI and retry `hello`.
5. Check that the requested action and model key are documented.
6. Check that required communication keys were set.
7. Do not invent substitute actions.
8. If the operation skill selected GUI mode and REST is unavailable, explain the situation and ask whether CLI fallback is acceptable.
9. If the config key exists but no final REST action is exposed, explain that distinction clearly.

---
## GUI Path Rules

If the workflow started by opening or using the S32FlashTool GUI, preserve the GUI/REST path for subsequent device operations whenever possible.

1. Do not silently switch from GUI/REST to CLI for ordinary follow-up steps.
2. If the requested action is not available through the GUI/REST path, say so explicitly and ask whether to fall back to CLI.
3. When preparing a programming operation on the GUI path:
   - resolve target / flash algorithm / file without guessing
   - prepare GUI model values first
   - then propose or trigger the documented GUI action
4. Do not jump directly to CLI preview/command construction if the workflow started on GUI.
5. Still remind the user to expect serial boot mode, and mention restart/re-power-cycle requirements when a new flash algorithm, destination, or boot configuration requires it
---

## CLI fallback rule

If the user asked for GUI, do not switch to CLI silently.
Use CLI only if:
- the required behavior is not exposed by REST, or
- GUI/REST is unavailable and the user approves fallback

Explain the fallback before doing it.

---

## Do not

- Do not invent REST actions.
- Do not invent model keys.
- Do not use `UART` for `communicationDevice`.
- Do not launch a second GUI if `hello` already succeeds.
- Do not use generic or undocumented UI-loading commands instead of the documented `fullConfig*` keys.
- Do not use this skill as a substitute for operation-specific safety rules.
- Do not silently change execution mode from GUI to CLI.

---

## Quick decision summary

- **Need to operate S32FlashTool GUI through REST?**  
  -> use this skill

- **Need to decide whether to use GUI or CLI?**  
  -> use the corresponding operation skill first

- **Need read/program/erase/RCON-write/SRAM semantics, safety, or required inputs?**  
  -> use the corresponding operation skill

- **Need to reuse an existing GUI REST session?**  
  -> call `hello` first and reuse on success

- **Need UART in GUI mode?**  
  -> set `communicationDevice = COM`

- **Need the final GUI action?**  
  -> first set the matching `fullConfig*` key, then call the mapped `flash.click*` action only if that final action is actually documented and exposed
---

## Guardrails

**Scope**
- Only cover generic S32FlashTool GUI REST behavior: probing/launching the session, reusing an
  existing session, setting documented model keys, calling documented GUI actions, mapping
  `fullConfig*` payloads to the correct final action.
- Do not use as the sole source of operation semantics. Operation-specific safety belongs in the
  operation skill.

**Destructive actions**
- This skill is transport-only. It must never trigger a destructive REST action without the owning
  operation skill's confirmation flow.
- Never launch a second GUI when `hello` already succeeds. Recovery: reuse the existing session.

**Refuse-and-escalate**
- If the GUI REST session is unreachable and launch is not permitted by the user, stop and ask.
- If a REST action or model key is not documented, refuse to send it. Recovery: report the missing
  documentation and ask the user how to proceed.
- Never use `communicationDevice = UART`; use `COM` with values like `COM15,ftdi` in `comPort`.
- Never silently switch execution mode from GUI to CLI (or vice versa) within one workflow.

**Output contract**
- Report the REST request/response pair (or a redacted summary) so callers can audit which
  documented action was used.

## Out of scope

- Operation-specific safety and payload semantics. Those live in the operation
  skill (`erase-flash`, `read-flash`, `read-rcon`, `write-rcon`,
  `upload-file-to-flash`, `sram`, `get-flash-id`).
- CLI execution paths. This skill covers GUI/REST only; the operation skill
  handles CLI.
- Deciding between GUI and CLI. That belongs to the operation skill and
  `s32flashtool-workflow-index`.
- Inventing REST actions, model keys, or `communicationDevice` values. Use only
  documented names.
