---
name: s32sdaf-delete-record
description: Delete a device UID record and all associated keys from a Volkano smart card for S32SDAF workflows. Resolves the exact UID to delete through discovery when needed, enforces irreversible-operation confirmation, and verifies the record is gone after deletion.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32sdaf
  see_also: '[s32sdaf-discovery-and-status, s32sdaf-register-key, s32sdaf-wrap-and-register]'
  tags: '[s32sdaf, volkano, smartcard, delete, uid, cleanup, destructive, security]'
---

# Delete a UID Record from the Smart Card

Delete one specific UID record and all of its associated keys from the Volkano
smart card. The delete tool requires an exact UID value, while real requests are
often imprecise, so this skill's main value is safe parameter resolution:
discovery, disambiguation, explicit confirmation, and post-delete verification.

## When to use

Trigger this skill when the user wants to remove an existing registration such
as an obsolete UID, a wrongly registered record, a test record, or a card entry
blocking new registration because storage is full. Typical phrasings: "delete
UID 0011...", "remove UID #3", "delete the old test record", "clean one entry so
I can register a new key".

Do not use it to delete without explicit confirmation, guess which UID to delete
when multiple candidates exist, register replacement keys, authenticate a
device, or change the smart-card password.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Tool | `status` | confirm server reachable if readiness uncertain |
| Tool | `execute_action(action="discover", params={...})` | list current UIDs; resolve which exact UID the user means |
| Tool | `execute_action(action="delete_record", params={...})` | delete the confirmed UID record (`confirmed_by_user=True`) |
| Tool | `execute_action(action="find_installation")` | resolve Volkano install path when needed |

The final deletion target must be one exact UID of 16 or 32 hex characters
(e.g. `030DC2899008D3D3`, `00112233445566770011223344556677`).

## Quickstart

1. Resolve one exact UID (use `execute_action(action="discover", params={...})` if not explicitly
   given; resolve indexes/labels against discovery output).
2. Validate the UID is hex and 16 or 32 chars.
3. Echo the exact UID, warn deletion is irreversible and removes all associated
   keys, and require explicit user confirmation.
4. Call `execute_action(action="delete_record", params={...})` with `uid`, optional `password`,
   optional `volkano_folder`, `confirmed_by_user=True`.
5. Verify with `execute_action(action="discover", params={...})` that the UID is gone.

## Workflow

1. Treat this as an irreversible smart-card mutation. Never call the delete tool
   until exactly one UID is identified.
2. If the UID is not explicitly provided, use discovery to obtain candidates
   rather than guessing.
3. If the user references an index (`UID #3`), resolve it against current
   discovery output and show the resolved UID back before deleting.
4. For partial UIDs or descriptive labels, search discovery candidates: one
   match -> confirm; multiple matches -> ask one concise clarification question.
5. Before deletion, state the exact UID, that all associated keys will be
   removed, and that the action is irreversible; proceed only after explicit
   confirmation.
6. Execute the delete, then verify via discovery when card access allows.

For card-full cleanup: inspect UIDs with discovery, ask which exact UID to
remove, and never choose a deletion target on the user's behalf without explicit
authorization of that specific UID.

## Guardrails

**Scope** - Operates on exactly one confirmed UID record on the smart card.

**Destructive actions** - Irreversible: permanently deletes the UID record and
all keys associated with it. Safe default is to stop and require explicit
confirmation of the exact UID before any delete call.

**Secrets** - Require but do not guess or echo the smart-card password.

**Refuse-and-escalate** -
- Invalid UID format: report the 16/32 hex-char requirement.
- No matching UID: present available UIDs and ask which to remove.
- Multiple candidates: do not guess; ask one clarification question listing them.
- Confirmation not given: do not call delete; restate the UID and ask.
- Card unavailable / auth failure: ask the user to verify card/reader or provide
  the correct password; recommend `s32sdaf-discovery-and-status`.
- Applet-version limitation: report deletion needs a sufficiently new applet;
  do not assume support.

## Validation loop

1. Confirm exactly one exact UID is identified.
2. Confirm explicit user confirmation was obtained before mutation.
3. Call delete once for the intended UID.
4. Pass criterion: post-delete discovery shows the UID is no longer present
   (when card access allows), and the user is told the record is gone.

## Out of scope

- Registering replacement keys (see `s32sdaf-register-key` /
  `s32sdaf-wrap-and-register`).
- Challenge-response authentication; changing the smart-card password.

## See Also

- `s32sdaf-discovery-and-status` - inspect card contents before deletion.
- `s32sdaf-register-key` - register a replacement after cleanup.
- `s32sdaf-wrap-and-register` - register wrapped material after cleanup.
