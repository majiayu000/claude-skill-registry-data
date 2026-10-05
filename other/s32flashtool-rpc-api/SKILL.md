---
name: s32flashtool-rpc-api
description: Operate the S32FlashTool GUI through its RPC API using documented session, model, and action patterns.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32flashtool
  depends_on: '["s32flashtool-agent-rules-minimal", "s32flashtool-workflow-index"]'
  tags: '["s32flashtool", "gui", "rpc", "transport", "automation"]'
---

# S32FlashTool RPC API Workflow

Use the S32FlashTool GUI through its documented RPC API.

This skill is **transport-oriented**, not **operation-oriented**.

It explains:
- how to probe / launch / reuse a GUI RPC session
- the *shape* of a GUI-side workflow (set model keys, optionally initialize,
  trigger a final action)
- how a prepared `fullConfig*`-shaped payload maps to a `flash.click*`-style
  final action, at the **routing** level
- how to reason about a documented config entry that does not currently have a
  corresponding exposed final RPC action

It does **not** replace operation skills (read flash, program flash, erase
flash, read RCON, write RCON, SRAM execution).

## When to use this skill

Use this skill when:
- the user explicitly asked for **GUI**, **window**, or **RPC** control of S32FlashTool
- an operation skill selected GUI mode
- probing or reusing an already running GUI RPC session
- launching the GUI in a documented way
- setting a GUI configuration and triggering the corresponding GUI action
- determining whether a GUI config key has a matching exposed final action

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
0. search_actions(query="gui_", strategy=regex, detailed=true)
   -> confirm the current RPC surface before assuming any name below
1. hello                              # probe existing session
   -> if fail, gui.launch, then hello
2. model.setFullConfig<DocumentedFinalAction> { <keys observed in the current schema> }
3. flash.click<DocumentedFinalAction>  # per operation skill's mapping
```

Rules:
- Discover names via `search_actions`; do not trust the lists below without re-checking.
- Reuse an existing GUI when `hello` succeeds; do not launch twice.
- Only send action names and model keys observed in the current schema.
- Never silently switch to CLI mid-workflow.

## Scope

Generic S32FlashTool GUI RPC behavior:
- probing / launching / reusing the GUI RPC session
- setting model keys that the current schema declares
- calling final actions the current schema declares
- routing a prepared `fullConfig*`-shaped payload to its matching final action
- distinguishing a documented config entry from a documented final RPC action

Do not use this skill as the sole source of operation semantics.
For read/program/erase/get-id/RCON-write/SRAM workflows, also use the corresponding operation skill.

## Relationship to operation skills

This skill is transport-oriented, not operation-oriented.

Use it together with:
- `s32flashtool-read-flash`
- `s32flashtool-get-flash-id`
- `s32flashtool-upload-file-to-flash`
- `s32flashtool-write-rcon`
- `s32flashtool-sram`
- `s32flashtool-erase-flash`
- `s32flashtool-read-rcon`

Operation skills define:
- when to use GUI vs CLI
- required user inputs (as semantic labels)
- safety and confirmation requirements
- operation-specific payload fields (as semantic labels)
- validation guidance

This skill defines:
- how to reach and re-use the GUI RPC session
- how to discover the current set of documented actions and model keys
- how to route a prepared `fullConfig*` payload to the matching final action
- how to react when a documented config key has no exposed final action
- generic GUI-side behavior and constraints

## Mode ownership rule

This skill does not decide whether GUI/RPC or CLI should be used.
That decision belongs to the selected operation skill.

If the operation skill chose GUI mode, apply this transport skill.
Do not switch to CLI silently from this skill.

## Minimal rules

1. If the operation skill requires GUI, prefer RPC over CLI.
2. Always call `hello` before launching a new GUI.
3. Reuse an existing RPC session if `hello` succeeds.
4. Launch GUI only if `hello` fails and launch was requested or approved.
5. Discover model keys and action names via `search_actions` before sending.
6. Configure the matching `fullConfig*` key before the corresponding `flash.click*` action.
7. Do not call `model.get` after every `model.set` unless readback is needed.
8. Never invent an action name or model key that was not observed in the current schema.
9. Distinguish a documented config entry from a documented final RPC action.
10. Do not silently fall back to CLI from this skill.

## RPC port resolution

If `s32flashtool_folder` (the installation root) is known:

1. Read `<folder>/GUI/s32ft.ini`
2. Use default port `51236` if the user has not indicated another.
3. Reuse that port for subsequent RPC calls.

## Session workflow

### Standard session workflow
1. Resolve RPC port.
2. Call `hello`.
3. If `hello` succeeds: reuse the existing GUI RPC session.
4. If `hello` fails and launch is allowed: call `gui.launch`.
5. Poll `hello` until reachable or timeout.

### Generic RPC workflow skeleton
After the session is available:

1. Set the operation-specific `fullConfig*` key.
2. If required for the destination, call `init.clickLaunchInitialization`.
3. Call the matching final `flash.click*` action **only** if it is exposed by
   the current schema.

## Historically documented RPC surface (routing hint, not authoritative)

The names below are the surface historically exposed by the S32FlashTool GUI
RPC API. Use them as a routing hint when reading operation skills, but
**always re-validate against `search_actions(detailed=true)` before actually
sending them**. Do not assume this list is complete or unchanged.

### Historically observed actions
- session/discovery: `hello`, `gui.launch`, `model.get`
- initialization: `init.clickLaunchInitialization`
- final actions: `flash.clickUploadFileToDevice`, `flash.clickGetId`,
  `flash.clickDownloadFromDevice`, `flash.clickDownloadFromDeviceToFile`,
  `flash.clickEraseMemoryRange`

### Historically observed model keys
- transport selection: `communicationDevice`, `comPort`
- CAN: `canVendorId`, `canPortNumber`, `canSerialNumber`
- Ethernet: `ethernetHost`, `ethernetAdapterName`, `ethernetAdapterDescription`,
  `listeningIp`, `dhcpFirstIp`, `dhcpLastIp`, `tftpEnabled`, `dhcpEnabled`,
  `tftpSourceFolder`
- operation payloads: `fullConfigUploadFileToDevice`, `fullConfigUploadHexToRcon`,
  `fullConfigSram`, `fullConfigDownloadFromDevice`,
  `fullConfigDownloadFromDeviceToFile`, `fullConfigGetFlashId`,
  `fullConfigEraseFlashMemory`

If `search_actions` returns a superset (new capabilities) or a subset (removed
capabilities), follow the registry. Do not silently substitute missing actions.

## Action-to-config routing hint

When the operation skill has prepared a `fullConfig*`-shaped payload, use this
mapping to pick the corresponding final action. Treat it as routing guidance,
not as an authoritative schema:

| Operation shape | Config key (hint) | Final action (hint) |
|---|---|---|
| upload / program file to flash | `fullConfigUploadFileToDevice` | `flash.clickUploadFileToDevice` |
| read from device to console / view | `fullConfigDownloadFromDevice` | `flash.clickDownloadFromDevice` |
| read from device to file | `fullConfigDownloadFromDeviceToFile` | `flash.clickDownloadFromDeviceToFile` |
| get flash ID | `fullConfigGetFlashId` | `flash.clickGetId` |
| erase flash range | `fullConfigEraseFlashMemory` | `flash.clickEraseMemoryRange` |
| write / program hex to RCON/EEPROM | `fullConfigUploadHexToRcon` | `flash.clickUploadFileToDevice` |
| execute binary in SRAM | `fullConfigSram` | `init.clickLaunchInitialization` |
| prepare for Ethernet boot | `setFullConfigPrepareEthernetBoot` | `init.clickLaunchInitialization` |

Before sending, confirm both the key name and the action name via
`search_actions(detailed=true)`. If the registry declares a different name,
use the registry name and update the operation skill's routing note.

## Communication rules

Communication values are constrained by the schema's enums. Read them from
`search_actions(query="gui_", detailed=true)` and pick a value the schema
allows.

Historically:

### UART / serial
- `communicationDevice` accepted `COM` (not `UART`).
- `comPort` accepted values like `"COM15"` or `"COM15,ftdi"`, or `"COM15,921600,ftdi"` or `"COM15,921600"`.

### CAN
- Only the CAN model keys listed above were accepted.

### Ethernet
- Only the Ethernet model keys listed above were accepted.

If the current schema declares different or additional accepted values, use
those; do not force historical values.

### `transport` is effectively required on every `model.setFullConfig*`

The `input_schema` of the `model.setFullConfig*` family (for example
`model.setFullConfigGetFlashId`, `model.setFullConfigEraseFlashMemory`,
`model.setFullConfigUploadFileToDevice`,
`model.setFullConfigDownloadFromDevice`,
`model.setFullConfigDownloadFromDeviceToFile`,
`model.setFullConfigSram`, `model.setFullConfigUploadHexToRcon`) might declare
`transport` as optional inside the `config` object.

In practice the server rejects the call without it:

```
IDE_CALL_FAILED: "transport is mandatory and must not be missing"
```

Rules for agents using this skill:

- Always send a `transport` block on any `model.setFullConfig*` call, even
  if the current schema marks it optional.
- Pick the transport variant (`uart`, `can`, or the ethernet variant when
  the schema exposes it) that matches how the target board is actually
  connected.
- Never omit `transport` on the assumption that "optional in the schema"
  means "optional at runtime" for these actions.

The single exception is `model.setFullConfigPrepareEthernetBoot`
(see next note).

## Initialization rule

If the destination is `FLASH` or `RCON`, the workflow typically requires:
- `init.clickLaunchInitialization`

Operation skills indicate when initialization is part of the valid GUI
workflow. When it is, do not skip it.

For `SRAM`, initialization may still be part of the GUI-side workflow, but do
not assume a final SRAM execute RPC click action exists unless the schema
exposes one.

## Generic GUI patterns (routing hints)

Reusable transport patterns, always paired with an operation skill. Confirm
names against `search_actions` before sending.

### Upload-style
1. `model.set("fullConfigUploadFileToDevice", {...})`
2. if required: `init.clickLaunchInitialization`
3. `flash.clickUploadFileToDevice`

### Read-to-console
1. `model.set("fullConfigDownloadFromDevice", {...})`
2. if required: `init.clickLaunchInitialization`
3. `flash.clickDownloadFromDevice`

### Read-to-file
1. `model.set("fullConfigDownloadFromDeviceToFile", {...})`
2. if required: `init.clickLaunchInitialization`
3. `flash.clickDownloadFromDeviceToFile`

### Get-ID
1. `model.set("fullConfigGetFlashId", {...})`
2. if required: `init.clickLaunchInitialization`
3. `flash.clickGetId`

### Erase
1. `model.set("fullConfigEraseFlashMemory", {...})`
2. if required: `init.clickLaunchInitialization`
3. `flash.clickEraseMemoryRange`

### RCON write / program
1. `model.set("fullConfigUploadHexToRcon", {...})`
2. if needed by board workflow: `init.clickLaunchInitialization`
3. `flash.clickUploadFileToDevice`

### SRAM
1. `model.set("fullConfigSram", {...})`
2. `init.clickLaunchInitialization`

## GUI normalization note

The GUI may normalize numeric strings when storing/displaying values:
- `0x100` may appear as `100`
- `0x40` may appear as `40`

Treat this as normal GUI normalization unless the semantic value changed
incorrectly.

## Readback rule for model state

- Do not use `model.get` after every `model.set`.
- Use `model.get` only when readback is needed for debugging or explicit
  confirmation.
- If the user asks to inspect current GUI model state, use `model.get` with a
  key confirmed by the current schema.

## Validation loop

A valid RPC execution normally includes:
- successful `hello`, or successful `gui.launch` followed by `hello`
- successful `model.set` responses for keys accepted by the current schema
- successful click response for the final GUI action

Operation-specific success validation belongs to the operation skill.

## Error handling

If RPC interaction fails:

1. Report the exact failure clearly.
2. Check the RPC port.
3. Check whether the GUI is already running.
4. If allowed, launch the GUI and retry `hello`.
5. Re-run `search_actions(detailed=true)`; verify that the action/key the
   caller tried to send is present in the current schema.
6. Check that required communication keys were set.
7. Do not invent substitute actions.
8. If the operation skill selected GUI mode and RPC is unavailable, explain
   the situation and ask whether CLI fallback is acceptable.
9. If a config key exists but no final RPC action is exposed for it, explain
   that distinction clearly.

---

## GUI Path Rules

If the workflow started by opening or using the S32FlashTool GUI, preserve the
GUI/RPC path for subsequent device operations whenever possible.

1. Do not silently switch from GUI/RPC to CLI for ordinary follow-up steps.
2. If the requested action is not available through the GUI/RPC path (i.e.
   `search_actions` does not list it), say so explicitly and ask whether to
   fall back to CLI.
3. When preparing a programming operation on the GUI path:
   - resolve target / flash algorithm / file without guessing
   - prepare GUI model values first
   - then propose or trigger the documented GUI action
4. Do not jump directly to CLI preview/command construction if the workflow
   started on GUI.
5. Still remind the user to expect serial boot mode, and mention
   restart / re-power-cycle requirements when a new flash algorithm,
   destination, or boot configuration requires it.

---

## CLI fallback rule

If the user asked for GUI, do not switch to CLI silently.
Use CLI only if:
- the required behavior is not exposed by RPC (confirmed via `search_actions`), or
- GUI/RPC is unavailable and the user approves fallback.

Explain the fallback before doing it.

---

## Do not

- Do not send an action name or model key that is not present in the current
  `search_actions(detailed=true)` output.
- Do not launch a second GUI if `hello` already succeeds.
- Do not use generic or undocumented UI-loading commands instead of the
  documented `fullConfig*` keys.
- Do not use this skill as a substitute for operation-specific safety rules.
- Do not silently change execution mode from GUI to CLI.

---

## Quick decision summary

- **Need to operate S32FlashTool GUI through RPC?**  
  -> use this skill

- **Need to decide whether to use GUI or CLI?**  
  -> use the corresponding operation skill first

- **Need read / program / erase / RCON-write / SRAM semantics, safety, or required inputs?**  
  -> use the corresponding operation skill

- **Need to reuse an existing GUI RPC session?**  
  -> call `hello` first and reuse on success

- **Need the exact set of currently exposed actions or model keys?**  
  -> call `search_actions(query="gui_", strategy=regex, detailed=true)`

- **Need the final GUI action?**  
  -> first set the matching `fullConfig*` key, then call the mapped
     `flash.click*` action, provided the current schema exposes it

---

## Guardrails

**Scope**
- Only cover generic S32FlashTool GUI RPC behavior: probing / launching the
  session, reusing an existing session, setting model keys accepted by the
  current schema, calling final actions the current schema exposes, mapping
  `fullConfig*` payloads to the correct final action.
- Do not use as the sole source of operation semantics. Operation-specific
  safety belongs in the operation skill.

**Destructive actions**
- This skill is transport-only. It must never trigger a destructive RPC
  action without the owning operation skill's confirmation flow.
- Never launch a second GUI when `hello` already succeeds. Recovery: reuse
  the existing session.

**Refuse-and-escalate**
- If the GUI RPC session is unreachable and launch is not permitted by the
  user, stop and ask.
- If a candidate action name or model key is not present in
  `search_actions(detailed=true)`, refuse to send it. Recovery: report the
  gap and ask the user how to proceed.
- Never silently switch execution mode from GUI to CLI (or vice versa)
  within one workflow.

**Output contract**
- Report the RPC request / response pair (or a redacted summary) so callers
  can audit which schema-observed action was used.

## Attention

### 1. `model.setFullConfigPrepareEthernetBoot` does not require `transport`

`model.setFullConfigPrepareEthernetBoot` has no `transport` field in its
`input_schema` and the call succeeds without one. This is intentional:
the operation implicitly forces the Ethernet communication device and
applies the ethernet interface parameters supplied directly in the config
(`adapter`, `localIp`, `dhcpStart`, `dhcpEnd`, `tftpFolder`,
`enableTftp`, `enableDhcp`).

Rules for agents:

- Do NOT add a synthetic `transport` block to a
  `model.setFullConfigPrepareEthernetBoot` payload.
- Treat this action as the exception to the "transport mandatory" rule
  in note 1.
- The `adapter` string must match one of the ethernet adapters the tool
  enumerates live from the OS; the server rejects unknown names with
  an explicit `Available adapters:` list. Do not invent adapter names.
- `targetId` values are case-sensitive; server-side validation returns
  the exact set of legal target IDs on mismatch. Use the returned casing.
- The action is only legal on target IDs whose capability matrix includes
  the `FLASHLESS_BOOT` destination; on other targets the server returns
  the exact `Available destinations:` list.

### 2. `flash.click*` actions are polymorphic w.r.t. the active model config

The exposed final actions in the flash section
(`flash.clickUploadFileToDevice`, `flash.clickDownloadFromDevice`,
`flash.clickDownloadFromDeviceToFile`, `flash.clickGetId`,
`flash.clickEraseMemoryRange`) fire the SWT hyperlink registered in the
current flash-section view. The concrete operation the GUI actually
launches is decided by the last successful `model.setFullConfig*` call,
not only by the click action's name.


Rules for agents:

- The routing table in **Action-to-config routing hint** already encodes
  this. Trust it, but confirm the underlying click name via
  `search_actions(detailed=true)` before dispatching.
- The "same click name, different operation" pattern is not a bug and
  the operation label reported by `gui.getOperationStatus` (see next
  note) is the authoritative name of what actually ran.
- Always configure the intended `fullConfig*` key immediately before
  firing the click. Do not rely on GUI state persisting from an earlier
  workflow: if a different `fullConfig*` was set last, the polymorphic
  click will fire that operation instead.

### 3. `gui.getOperationStatus` — asynchronous progress polling

`init.click*` and `flash.click*` are dispatch-only. A successful JSON-RPC
response for those actions only means "the SWT click was posted"; it does
NOT mean the operation completed. Every click bumps an auto-incrementing
`session_id` inside the GUI and starts an asynchronous target operation
whose state is exposed by `gui.getOperationStatus`.

`model.setFullConfig*` calls do NOT create a new session and do NOT touch
`gui.getOperationStatus`. Their JSON-RPC response is
`{"key": "...", "updated": true}`.

`gui.getOperationStatus` takes no parameters and returns:

- `session_id`         — integer, auto-incremented per click
- `operation`          — GUI-owned label of what actually ran
                         (e.g. `"Get flash ID..."`,
                         `"Upload hex string to EEPROM (RCON)"`,
                         `"Execute binary on the selected target..."`)
- `operation_status`   — one of `""`, `"pending start"`, `"in execution"`,
                         `"waiting user decision"`, `"ready"`, `"cancelled"`
- `execution_result`   — `""` until `ready`, then `"success"` or `"error"`
- `execution_output`   — GUI console text (empty until `ready`)
- `recommended_update` — polling interval in seconds (observed: 2)

Rules for agents on the GUI/RPC path:

- After every `init.click*` or `flash.click*`, poll
  `gui.getOperationStatus` every `recommended_update` seconds while
  `operation_status` is `"pending start"` or `"in execution"`. Do not
  send follow-up clicks in this window.
- If `operation_status` is `"waiting user decision"`, a modal or
  confirmation is pending in the GUI. Surface this to the user, do NOT
  auto-answer, and continue polling with the recommended interval. This
  state is normal for destructive operations (erase, upload) and for
  SRAM execute.
- Treat the operation as complete only when `operation_status` becomes
  `"ready"` (then read `execution_result` and `execution_output`) or
  `"cancelled"`. Do not claim success just because the click returned.
- The authoritative name of what ran is the `operation` field, not the
  click name that was sent.
- Polling after a terminal state is idempotent: repeated calls return
  the same `session_id` snapshot until the next click. Use this to
  fetch `execution_output` at any time until the next dispatch.
- When reporting failure, quote `execution_output` verbatim: it mirrors
  the GUI console and is the same text the user would see there.
- `execution_output` may include prior transport-level context (for
  example baud-rate probes such as
  `"Initializing target (48000 Baud) ..."` when initialization failed).
  Interpret it as GUI console text, not as a schema field.

## Out of scope

- Operation-specific safety and payload semantics — see the operation skills
  (`erase-flash`, `read-flash`, `read-rcon`, `write-rcon`,
  `upload-file-to-flash`, `sram`, `get-flash-id`).
- CLI execution paths — this skill covers GUI/RPC only; the operation skill
  handles CLI.
- Deciding between GUI and CLI — belongs to the operation skill and
  `s32flashtool-workflow-index`.
- Duplicating the JSON `input_schema` of RPC actions — the authoritative
  source is `search_actions(detailed=true)`.
