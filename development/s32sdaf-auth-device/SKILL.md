---
name: s32sdaf-auth-device
description: Perform S32SDAF / Volkano challenge-response authentication for a registered device UID. Validates UID and challenge input, confirms registration state when needed, and retrieves the authentication response for generic UID+challenge flows. If the request mentions HSE2, BootROM, HSE-FW, scheme_id, ADK1, or OID-sensitive behavior - or KUID combined with an HSE2 scheme/OID context - route to the HSE2-specific skill before invoking the generic get-response wrapper. A KUID selector by itself does not require HSE2 routing.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32sdaf
  see_also: '[s32sdaf-discovery-and-status, s32sdaf-register-key, s32sdaf-wrap-and-register, s32sdaf-hse2-authentication, s32sdaf-secure-debug-session]'
  tags: '[s32sdaf, volkano, smartcard, authentication, challenge-response, security]'
---

# Authenticate a Device with Challenge-Response

Use a registered device UID and a challenge received from the target device to
obtain the smart-card-generated authentication response. The device provides a
challenge, the smart card computes the response for a registered UID, and the
response is returned to the user for use with the target.

## When to use

Use this skill for generic UID+challenge authentication: validating UID and
challenge input, checking whether a UID is registered, and retrieving a
challenge response from the smart card. Also use it to guide the user when
registration must be completed first.

Do not use this skill for registering or wrapping keys, deleting records, or
guessing UID/challenge values. Route to `s32sdaf-hse2-authentication` when the
request mentions or implies HSE2, BootROM, HSE-FW, scheme_id, ADK1, OID, or
key-name/key-index selection - those materially affect the command and are not
covered by the generic wrapper. A KUID selector on its own stays in this
generic flow; route KUID to HSE2 only when it is combined with an HSE2
scheme_id/OID or an explicit HSE2/BootROM/HSE-FW context.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Tool | `status` | verify MCP server reachability/config |
| Tool | `execute_action(action="discover", params={...})` | confirm whether a UID is registered |
| Tool | `execute_action(action="get_response", params={...})` | retrieve response for generic UID+challenge only |
| Tool | `execute_action(action="find_installation")` | locate Volkano when path resolution is needed |

## Quickstart

1. If readiness is unknown, run `status`.
2. Validate UID (16 or 32 hex chars) and challenge (valid hex, even length).
3. If the request mentions HSE2/BootROM/HSE-FW/scheme_id/ADK1/OID (or KUID
   combined with an HSE2 scheme/OID context), stop and route to
   `s32sdaf-hse2-authentication`. KUID alone stays here.
4. If UID presence is uncertain, run `execute_action(action="discover", params={...})`.
5. Call `execute_action(get_response)(uid, challenge, [password], [volkano_folder])`.
6. Present the response and remind the user to send it back to the device.

## Workflow

1. **Confirm readiness.** If environment state is unknown, run
   `status`; inspect registered UIDs with
   `execute_action(action="discover", params={...})` if needed.
2. **Validate inputs locally.** UID must be hex, 16 chars (8-byte) or 32 chars
   (16-byte). Challenge must be valid hex with even length. Confirm the user
   understands the challenge originated from the target device.
3. **Route HSE2/selector-sensitive requests away.** Before calling the generic
   wrapper, check whether the request depends on `scheme_id`, `oid`, `key`, or
   key-name selection. If so, route to `s32sdaf-hse2-authentication`; the
   generic wrapper is not equivalent to the raw `volkano.exe get_response`.
4. **Confirm registration if uncertain.** Run `execute_action(action="discover", params={...})`.
   If the UID is missing, stop and redirect to `s32sdaf-register-key` or
   `s32sdaf-wrap-and-register`.
5. **Retrieve the response.** Only for a confirmed generic UID+challenge flow,
   call `execute_action(action="get_response", params={...})` with `uid`, `challenge`, optional
   `password`, optional `volkano_folder`.
6. **Present the result** in a copy-friendly form and explain it must be sent
   back to the target device to complete authentication.

The most common failure is wrong context (wrong UID, wrong challenge, or
unregistered device), not cryptographic execution. Discovery is the safe way
to resolve UID uncertainty.

## Guardrails

**Scope** - Read-oriented authentication. It should not modify persistent card
contents and is safe to retry when inputs are correct.

**Destructive actions** - None. This skill must not register, wrap, or delete.

**Secrets** - Never invent passwords, UID values, or challenge data. Do not
echo the password beyond what is needed to run the tool.

**Refuse-and-escalate** -
- Missing challenge: stop; the challenge must come from the target device.
- UID not registered: stop; redirect to `s32sdaf-register-key` /
  `s32sdaf-wrap-and-register`.
- HSE2/selector-sensitive request: stop; route to
  `s32sdaf-hse2-authentication`.
- Wrapper rejects an already-validated challenge (e.g. `Missing the
  challenge`): do not conclude the input is malformed. Re-check hex/even
  length, verify the request was not HSE2, and treat it as a possible
  wrapper-to-command mismatch.

## Validation loop

1. Confirm UID is hex and 16 or 32 chars; confirm challenge is valid hex with
   even length.
2. Confirm the request is genuinely generic (no HSE2/scheme/OID/key selectors).
3. Confirm UID existence via discovery when uncertain.
4. Run `execute_action(action="get_response", params={...})`.
5. Pass criterion: a response is returned and the user is clearly told to send
   it back to the target device to complete authentication.

## Out of scope

- Registering, wrapping, or deleting keys/records.
- HSE2-specific response calculation (scheme, OID, key selection).
- Guessing UID, challenge, or password values.

## See Also

- Related skills: `s32sdaf-hse2-authentication` (HSE2/selector-sensitive
  flows), `s32sdaf-register-key` and `s32sdaf-wrap-and-register` (provisioning),
  `s32sdaf-discovery-and-status` (readiness/UID inspection),
  `s32sdaf-unified-get-response` (single entry point across all get_response
  cases), `s32sdaf-secure-debug-session` (enable secure debugging in an S32DS
  launch config; the debugger and card compute the response automatically).
