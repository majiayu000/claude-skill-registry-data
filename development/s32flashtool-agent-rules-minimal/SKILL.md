---
name: s32flashtool-agent-rules-minimal
description: Minimal shared rules that apply across all S32FlashTool workflows.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32flashtool
  tags: '["s32flashtool", "shared-rules", "baseline", "routing"]'
---
# S32FlashTool Minimal Agent Rules

Common workflow rules for s32flashtool skills.

## Action-based tool surface (READ FIRST)

The S32FlashTool MCP server exposes exactly two generic tools, and every capability is reached through them:

- `search_actions(query, limit?, strategy?)` -- discover the standardized
  action(s) that match an intent. Returns each matching action's name plus its
  input JSON schema.
- `execute_action(action, params)` -- run a discovered action. `params` must
  match the input schema returned by `search_actions`.

Standard flow for any operation:

1. `search_actions` with a short intent query (e.g. "program flash",
   "read mcuid", "get version", "list targets").
2. Read the returned action name and input schema.
3. `execute_action` with that action name and a `params` object.

CLI operations are a two-step, build-then-execute pattern:

1. `execute_action("cli_build_<op>", { sft_folder, cli_request: { operation, input } })`
   returns a ready `command` string (nothing runs on the target yet -- this is
   the preview).
2. Show the built `command` to the user, obtain confirmation for destructive
   operations, then `execute_action("cli_execute", { sft_folder, command })`.

GUI/RPC operations map to the RPC actions expected on from a running GUI:
`gui_launch` (static launcher), `hello` (health check), the
`model.setFullConfig*` config family (e.g. `model.setFullConfigGetFlashId`,
`model.setFullConfigUploadFileToDevice`), the `flash.click*` final actions
(e.g. `flash.clickGetId`, `flash.clickUploadFileToDevice`,
`flash.clickEraseMemoryRange`), `init.clickLaunchInitialization`, and
`gui.getOperationStatus` for asynchronous progress polling. These names are
discovered at runtime via `search_actions` with a `port`; always confirm the
exact names against the current schema.

## When to use

Apply these rules across all S32FlashTool workflows unless a skill explicitly narrows them.

## When not to use

Do not use this skill as a standalone workflow - it is a rules layer applied under every other skill.

## Schema source of truth (canonical rule)

Every action's authoritative input schema comes from the runtime registry via
`search_actions(query="<action_name>", detailed=true, limit=1)`, not from any
skill. Skills may reference action or parameter names as **routing hints**;
if a hint disagrees with the schema returned by `search_actions`, the schema
wins.

Consequences:

- Do not send a field name, enum value, or action name that is not present in
  the current `search_actions(detailed=true)` output for that action.
- Historical / documentation names (e.g. `sft_folder`, `cli_request`,
  `fullConfig*`, `flash.click*`, `communicationDevice`) are hints. Confirm at
  runtime before use.
- Where a skill uses a semantic user-facing label (e.g. `s32flashtool_folder`
  as "the installation folder"), that label maps to whatever the current
  schema names the parameter (currently `sft_folder`).

This rule applies to every consuming skill via `depends_on:
[s32flashtool-agent-rules-minimal, ...]`. Consuming skills must not restate it.

## Rules

1. Prefer the documented MCP tool for the requested operation.
2. Do not guess target, flash algorithm, interface, port, or model keys. Discover or confirm them.
3. Use absolute Windows paths for files and installation folders.
4. For destructive operations in CLI, preview first when available and require explicit user confirmation before execution.
5. Consult the relevant supported_devices documentation before hardware-specific operations.
6. Use `nxp_knowledge_kb_search` with preferably `corpus="s32flashtool"` to retrieve more relevant information, if necessary.
7. For GUI RPC serial workflows, use `communicationDevice = COM`, not `UART`. Put values like `COM15,ftdi` in `comPort`.
8. Reuse an existing GUI RPC session if `hello` succeeds; do not launch a second GUI unnecessarily.
9. Use only documented RPC actions and model keys.
10. With S32FlashTool GUI always use RPC actions.
11. Before the first preparing of any device operation (program/read/CRC/erase/boot configuration) in the current session, ask whether the user wants serial boot settings first. If the user says yes, provide serial boot guidance before preparing the GUI model or triggering GUI actions.
12. Session resource reread rule:
  - Within the current chat/session, maintain a working set of every skill/resource URI already read.
  - Read each skill/resource URI at most once per chat/session.
  - Reuse previously extracted guidance instead of rereading.
13. Operation first, mode second, transport third. Never infer payload schema from generic docs.
14. For information/identification questions, run nxp_knowledge_kb_search first. Do not invoke live target tools (read-mcuid, get-flash-id, list-interfaces, any cli_execute with a real transport, any flash.click*) unless the user explicitly asks for hardware verification, connectivity check, or a device operation.

## Quickstart

This skill is rules-only. To apply it:

1. In every operational skill that consumes it, declare in frontmatter:
   `metadata.depends_on: [s32flashtool-agent-rules-minimal, ...]`.
2. Before invoking any MCP tool, check the rules list above against the planned call (interface, port, model keys, `communicationDevice = COM`).
3. On conflict with an operation skill, defer to the operation skill and report the conflict.

## Guardrails

**Scope**
- This skill defines shared baseline rules only. It does not itself perform any operation on a target.
  When an operational step is needed, delegate to the correct operation skill via `s32flashtool-workflow-index`.
- Do not override rules stated in an operation skill. If two rules conflict, the operation skill wins;
  report the conflict to the user.

**Destructive actions**
- This skill is non-executing. It must never call MCP tools that write to a target on its own.
  If a rule here implies a destructive action, escalate to the owning operation skill and require
  explicit user confirmation there.

**Refuse-and-escalate**
- If required inputs (installation folder, interface, port, target, algorithm, model keys) are missing
  or ambiguous, stop and ask the user; do not guess. Recovery: request the specific missing value.
- If an RPC GUI session is uncertain, run `hello` first. Recovery: on failure, follow the launch
  procedure in `s32flashtool-rpc-api`.

**Resource limits**
- Read each skill/resource URI at most once per session. Recovery: reuse previously extracted guidance
  instead of rereading.

## Validation loop

Steps a consuming skill should run to confirm this baseline is honored:

1. Every consuming skill declares `depends_on: [s32flashtool-agent-rules-minimal, ...]`
   in its frontmatter. Pass if declared, fail otherwise.
2. Consuming skills do not repeat these rules verbatim in their body. Pass if the
   consuming skill defers to this skill, fail if the rule text is duplicated.
3. When a consumer invokes an MCP tool, the input keys match documented shapes
   (`communicationDevice = COM`, no invented RPC actions). Pass by inspection of
   the outgoing tool call; fail on any invented key.

## Out of scope

- Executing any MCP tool that touches a target. This skill is rules-only.
- Overriding rules stated in an operation skill. Operation skills win on conflict.
- Providing per-operation payload schemas or RPC action names. Consult the
  matching operation skill (see `s32flashtool-workflow-index`).
- Board identification, support-matrix answers, or hardware verification. Route
  to `s32flashtool-identify-user-board`, `s32flashtool-supported-devices-per-platform`,
  or the relevant operation skill.
