---
name: s32sdaf-secure-debug-session
description: Enable secure debugging in an S32DS debug configuration to debug a secured/locked S32 device. Focuses on the S32DS flow - select the launch config, enable secure debugging by editing the .launch file (or the Debugger tab), choose the Debugging type (Password or Challenge & Response), point at the smart card / Secure Keys Registry, and start the session. The debugger and smart card compute the challenge-response in the background; you do not wrap keys or compute responses by hand. Use whenever the user wants to debug a locked/secured S32 device, sees "Target is secured" / Error 102 / Error 601, or asks how to enable secure debugging in a debug configuration.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32sdaf
  see_also: '[s32ds-setup-debug-config, s32ds-build-and-debug, s32sdaf-discovery-and-status, s32sdaf-register-key, s32sdaf-kb-entrypoint, s32sdaf-unified-get-response]'
  tags: '[s32sdaf, secure-debug, s32ds, debug-configuration, challenge-response, password, unlock, security]'
---

# Enable Secure Debugging in an S32DS Debug Configuration

Debug a **secured/locked** S32 device from S32DS by enabling secure debugging in
the launch configuration and choosing the authentication type. This is the
**S32DS flow**, not manual cryptography: once secure debugging is enabled and the
smart card holds the right key, the debugger and card negotiate the unlock
(challenge-response or password) automatically at session start.

Two authentication types: **Password** (`PWD`, static secret) and **Challenge &
Response** (`CR`, dynamic; debugger reads the challenge from the SoC, the card
computes the response, the debugger sends it back).

## When to use

Use when the user wants to debug a secured/locked S32 device from S32DS, sees
"Target is secured", Error 102 (SoC still secure), or Error 601 (wrong
password/response/auth-type), or asks how to enable secure debugging and pick
Password vs Challenge & Response.

Do not use for unsecured devices (enabling secure debugging has no effect).

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Tool | `s32ds_list_actions` | discover exact S32DS action names/params (call FIRST) |
| Tool | `s32ds_execute` | S32DS dispatcher (listDebugLaunches, startDebug, buildProject) |
| Tool | `s32ds_execute` | `action="terminateDebug"` - terminate an active debug session (verify the exact name with `s32ds_list_actions()` first) |
| Tool | `s32ds_wait_for_job` | block until launch/build jobs finish |
| Tool | `status` | verify SDAF/Volkano + smart card readiness |
| Tool | `execute_action(action="discover", params={...})` | list registered UIDs/keys; confirm this SoC's UID is registered |
| Tool | `execute_action(action="register_key", params={"key_type":"ADKP", ...})` | register this SoC's UID + ADKP on the card (CR prerequisite) |
| CLI  | `gta.exe -t s32dbg:<probe>` | read the SoC UID and security status from the target |
| File edit | edit the `.launch` file | set secure-debugging attributes directly (primary path) |
| Reference | `.launch` attrs, UID read, PWD/CR, errors | `references/launch-file-editing.md` |

The S32DS MCP plugin has **no** action to write secure-debugging fields
(`listDebugLaunches` is read-only; `startDebug` takes only `name`/`build`). The
primary path is to **edit the `.launch` file directly**; the Debugger tab is a
manual fallback.

## Decision tree

```
Is the target actually secured?
├─ NO  -> stop; secure debugging is meaningless on an unlocked chip.
└─ YES -> Which authentication type was provisioned on the SoC?
    ├─ Password -> useSecureDebugging=true, secureDebuggingType=PWD, enter password.
    └─ Challenge & Response ->
        Is this SoC's UID + ADKP already registered on the smart card?
        ├─ NO  -> read UID from target (gta.exe -t s32dbg:<probe>),
        │         then register UID + ADKP
        │         (execute_action(action="register_key", params={"key_type":"ADKP", ...})).
        │         Without this the unlock CANNOT succeed (Error 102/601).
        └─ YES -> useSecureDebugging=true, secureDebuggingType=CR;
                  debugger + card compute the response at startDebug.
```

> **Critical for CR:** a `secureDebuggingType=CR` config only unlocks if the
> SoC's exact UID is registered with the correct ADKP on the card. If a session
> "starts" without a matching registered key, the chip was **already unlocked** -
> not unlocked by your CR flow. Always verify the UID is registered before
> claiming success.

## Prerequisites

- The device is secured (otherwise this skill does not apply).
- Project builds cleanly and a launch configuration exists
  (`s32ds-setup-debug-config`).
- The auth type is known and matches how the SoC was provisioned (mismatch ->
  Error 601).
- For CR: the smart card is reachable and this SoC's **UID + ADKP is registered**.
  If not, read the UID and register it (steps 4). Confirm
  readiness with the `status` tool.

## Workflow

1. **Confirm the device is secured.** If unlocked, stop and say so.
2. **Locate the launch configuration.**
   `s32ds_execute(action="listDebugLaunches", nameFilter="<project>")`. Note the
   probe address from `...core.port` (e.g. `S32 Debug Probe - Ethernet--<ip>--`
   or `... - USB----`).
3. **Determine the auth type** (`PWD` or `CR`). If unknown, ask one concise
   question - a wrong choice yields Error 601.
4. **Register the SoC's UID + ADKP (CR only, if not already registered).** Hard
   prerequisite - CR unlock fails without it.
   a. `status` to verify card readiness.
   b. `execute_action(action="discover", params={...})` (needs card password) to
      list existing keys.
      If this SoC's UID already shows `ADKP`, skip to step 5.
   c. **Read the SoC UID** with GTA - no debug session may be running (GTA starts
      its own server and collides with an active session; `terminateDebug`
      first): `gta.exe -t s32dbg:<probe>` from
      `<S32DS>/tools/S32Debugger/Debugger/Server/gta/`. `<probe>` is the probe IP
      (Ethernet) or USB string - **not** `127.0.0.1` (that loopback is the GTA
      server). `SoC Error 301`/`CC driver failure`/`327` mean the probe/target is
      unreachable, off, or the address is wrong - fix the connection first. If
      GTA still hangs/collides after `terminateDebug` (a stale server process),
      confirm no `gta.exe` remains before retrying - on Windows:
      `taskkill /F /IM gta.exe`.
   d. **Register:** `execute_action(action="register_key", params={"key_type":"ADKP",
      "uid":"<uid>", "key":"<ADKP hex>", "password":"<card password>"})` (see
      UID/ADKP length rules in `references/launch-file-editing.md`).
   e. Re-run `execute_action(action="discover", params={...})`; confirm the UID
      now shows `ADKP`.
5. **Enable secure debugging in the `.launch` file.** Set
   `useSecureDebugging=true` and `secureDebuggingType` to `PWD`/`CR` per
   `references/launch-file-editing.md`. GUI fallback: Debug Configurations ->
   Debugger tab -> Secure debugging.
6. **Persist the config.** If S32DS has it open, rebuild or restart/re-read so
   the launch uses the new attributes, not a stale cache.
7. **Start debug.**

   ```
   s32ds_execute(action="startDebug", name="<cfg>", build=<true|false>)
   s32ds_wait_for_job(jobName="Launching", timeoutMs=60000)
   ```

   - If you followed `s32ds-build-and-debug` immediately before this step and
     the build was clean, use `build=false` (avoids a redundant rebuild).
   - Otherwise use `build=true` to ensure the binary is current before flashing.

   The debugger unsecures automatically: `PWD` sends the secret; `CR` reads the
   challenge, the card computes the response. Enter the smart-card password if
   prompted.
8. **Confirm unlock.** Session connects and halts at the entry point / first
   breakpoint. Report the auth type used and unlocked state; on failure report
   the exact blocking cause (see reference errors).

## Guardrails

**Scope** - Edits a launch config and starts a debug session. It does not compute
responses or wrap keys; the debugger and card handle the unlock.

**Destructive actions** - Starting debug flashes/halts the target. Confirm the
config and build are current first.

**Secrets** - Never invent the debug password or ADKP; don't echo beyond what is
needed to populate the config or a register call.

**Refuse-and-escalate** -
- Device already unlocked: stop.
- Auth type unknown: ask; do not guess PWD vs CR.
- CR key not registered: read UID (step 4c) and register (4d), or use
  `s32sdaf-register-key`; do not start debug expecting success.
- Card/probe unreachable: report unlock cannot proceed; verify reader/probe.

## Validation loop

1. Device genuinely secured before enabling secure debugging.
2. Auth type matches SoC provisioning (PWD vs CR).
3. For CR: this SoC's UID is registered with the correct ADKP on the card.
4. `useSecureDebugging=true` and the right `secureDebuggingType` are set.
5. Session starts and halts at the first breakpoint.
6. Pass: the secured device is unlocked and debuggable, or the exact blocking
   cause is reported.

## Out of scope

- Unsecured-device debugging (use `s32ds-build-and-debug`).
- Computing responses / wrapping keys by hand.

## See Also

- `references/launch-file-editing.md` - `.launch` location, attributes, UID read
  via GTA, UID+ADKP registration, and the error catalog.
- `s32ds-setup-debug-config`, `s32ds-build-and-debug` - S32DS launch + debug.
- `s32sdaf-discovery-and-status` - verify SDAF / smart-card readiness.
- `s32sdaf-register-key` - registration of the debug key.
- `s32sdaf-kb-entrypoint` - broad SDAF intent router.
