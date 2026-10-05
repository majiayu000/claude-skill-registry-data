---
name: s32sdaf-change-password
description: Set or update the Volkano smart-card user password for S32SDAF workflows. Covers first-password initialization on a newly initialized smart card and authenticated password updates on an already-provisioned card, validates password inputs and command usage, and guides the agent through a persistent smart-card mutation using volkano.exe.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32sdaf
  see_also: '[s32sdaf-discovery-and-status, s32sdaf-register-key, s32sdaf-wrap-and-register, s32sdaf-auth-device]'
  tags: '[s32sdaf, volkano, smartcard, password, update-password, credential-management, security]'
---

# Set or Update the Smart-Card User Password

Set the first Volkano smart-card user password on a newly initialized card, or
update an existing password on an already-provisioned card. Both cases use the
`volkano.exe` command `update_pwd`; the difference is whether `-pw <current
password>` is required.

## When to use

Use this skill to set the first user password on a newly initialized smart card,
to change an existing smart-card password, or to confirm the exact command
shape, constraints, and safety rules for password initialization/update.

Do not use it for registering or wrapping keys, generating challenge responses,
deleting UID records, guessing passwords, or changing unrelated OS/IDE/Windows
credentials.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Tool | `status` | verify MCP server reachability, find default install |
| Tool | `execute_action(action="find_installation")` | resolve the Volkano install path |
| Tool | `execute_action(action="discover", params={...})` | optionally confirm card readiness |
| Tool | `execute_action(action="update_pwd", params={...})` | set/update the smart-card password |
| Command | `volkano.exe -cmd update_pwd ...` | grounded password init/update command |

The S32SDAF MCP server exposes three tools (`status`, `search_actions`,
`execute_action`). Password init/update is available through
`execute_action(action="update_pwd", params={"new_password": ...,
"current_password": ...})`: omit `current_password` for first-password
initialization, and supply it (passed as `-pw`) when updating an
already-provisioned card. The wrapper runs the documented `volkano.exe -cmd
update_pwd` command. The library API `vlk_update_password(const char* newPwd)`
mirrors this and requires authentication when a password is already provisioned.


## Grounded command reference

From the S32SDAF knowledge base (`SDAF_User_Guide.pdf`):
`update_pwd` sets or updates the smart-card user password with
`-new_pwd <new password>`. `-pw` is **not** required for the first password;
`-pw <current password>` is **mandatory** for subsequent updates.

- First-password init: `volkano.exe -cmd update_pwd -new_pwd vlk1234`
- Update existing: `volkano.exe -cmd update_pwd -new_pwd 1234 -pw vlk1234`

Password rules: must not be null; length **4 to 127 characters**.

## Quickstart

1. If readiness is unknown, run `status` (optionally
   `execute_action(action="find_installation")` / `execute_action(action="discover", params={...})`).
2. Require an explicit `new_password`; validate length 4..127.
3. Newly initialized card -> omit `-pw`. Existing password -> require and
   include `-pw <current_password>` (also 4..127).
4. Run the matching `volkano.exe -cmd update_pwd ...` form.
5. Inform the user that future authenticated operations must use the new
   password.

## Workflow

1. **Confirm readiness if needed.** Use `status`; resolve install
   path with `execute_action(action="find_installation")`; confirm card presence with
   `execute_action(action="discover", params={...})` if the card state is unknown - do not assume
   the card is initialized.
2. **Validate inputs locally.** Require `new_password`; verify length 4..127.
   For an update, require `current_password` and verify its length 4..127. Do
   not log or echo secrets.
3. **Choose the command form.** First-password initialization (newly
   initialized card, no user password yet) omits `-pw`. Updating an
   already-provisioned password includes `-pw <current_password>`.
4. **Execute.**
   - Init: `volkano.exe -cmd update_pwd -new_pwd <new_password>`
   - Update: `volkano.exe -cmd update_pwd -new_pwd <new_password> -pw <current_password>`
   Prefer an MCP wrapper if one becomes available instead of ad hoc strings.
5. **Confirm outcome.** Tell the user future authenticated Volkano operations
   must use the new password; optionally recommend a follow-up authenticated
   operation to confirm end-to-end readiness. Do not expose the password.

## Guardrails

**Scope** - Persistent smart-card credential mutation. Not a read-only
workflow; it sets or replaces the user password.

**Destructive actions** - Replacing the password causes subsequent operations
with the old password to fail. Require the user to supply the intended new
password explicitly; never guess current or new passwords.

**Secrets** - Do not log, repeat, or store passwords unnecessarily in
responses or transcripts.

**Refuse-and-escalate** -
- Missing `new_password`: stop and request it.
- Update case missing `current_password`: stop; `-pw` is mandatory for
  subsequent updates.
- Invalid length: report the 4..127 requirement.
- Incorrect current password reported by Volkano: ask for the correct one; do
  not retry with fabricated credentials.
- Card unavailable: ask the user to verify insertion/reader, recommend a
  discovery check.
- No execution surface for `update_pwd`: explain the workflow is grounded,
  provide the exact command, and recommend adding a dedicated MCP wrapper.

## Validation loop

1. Confirm init-vs-update case is correctly identified.
2. Confirm `new_password` present and 4..127; for updates confirm
   `current_password` present and 4..127.
3. Confirm the correct `volkano.exe update_pwd` command form is selected.
4. Execute (or emit) the command.
5. Pass criterion: the password is set/updated and the user is told the new
   password must be used for future authenticated operations.

## Out of scope

- Registering, wrapping, or deleting keys/records.
- Challenge-response authentication itself.
- Changing OS/IDE/Windows or other non-Volkano credentials.

## See Also

- Related skills: `s32sdaf-discovery-and-status` (readiness before change),
  `s32sdaf-register-key` / `s32sdaf-wrap-and-register` (next-step provisioning),
  `s32sdaf-auth-device` (authenticate after password setup).
