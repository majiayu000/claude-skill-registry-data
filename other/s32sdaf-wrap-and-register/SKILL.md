---
name: s32sdaf-wrap-and-register
description: Wrap a plain device key using the smart card's public wrapping key and then register the resulting wrapped key for a device UID. Covers wrapped-key families such as KUID, KUID_RF, KUID_PRE_FA, ODAK, ADK1, and ADK2, and uses the generic MCP register-key tool for the final registration step.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32sdaf
  see_also: '[s32sdaf-register-key, s32sdaf-export-wrapkey, s32sdaf-wrap-key, s32sdaf-discovery-and-status]'
  tags: '[s32sdaf, volkano, smartcard, wrapping, key-management, security, registration, kuid, kuid_rf, kuid_pre_fa, odak, adk1, adk2]'
---

# Wrap and Register a Key on the Smart Card

Wrap a plain key using the smart card's public wrapping key and then register
the wrapped result on the Volkano smart card. The wrap stage uses
`volkano_utils.exe -cmd wrap_key` (not `volkano.exe`); the final registration
uses the generic `execute_action(action="register_key", params={...})` tool, which covers `KUID`,
`KUID_RF`, `KUID_PRE_FA`, `ODAK`, `ADK1`, and `ADK2`.

**ADKP is the only key type that can be registered in plain form. Every
non-ADKP key type must be wrapped first.**

## When to use

Use this skill when the user has a **plain key** but needs it stored through a
**wrapped-key registration path** (typically KUID-oriented flows). It covers
exporting the public wrapping key, wrapping plain material, and registering the
wrapped result, while preserving family-specific requirements (OID, key index,
ADK2 key type, minimum applet version).

Do not use it for plain ADKP registration (use `s32sdaf-register-key`),
challenge-response authentication, deleting records, guessing whether the user
intended wrapped vs plain registration, or inventing OIDs/indexes/keys.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Tool | `status` | verify MCP server / install state |
| Tool | `execute_action(action="export_wrapkey", params={...})` | export the public wrapping key |
| Tool | `execute_action(action="wrap_key", params={...})` | wrap plain key (backed by `volkano_utils.exe -cmd wrap_key`) |
| Tool | `execute_action(action="register_key", params={...})` | generic final registration for all wrapped families |
| Tool | `execute_action(action="discover", params={...})` | inspect registered UIDs before/after mutation |
| Tool | `execute_action(action="find_installation")` | locate Volkano install |
| Reference | Per-family requirements + error handling | `references/key-families.md` |

## Quickstart

1. If readiness is unknown, run `status`.
2. If the user already has a valid 512-hex wrapped key, or wants plain ADKP,
   switch to `s32sdaf-register-key` (do not wrap again).
3. Validate UID (16/32 hex) and plain key (hex); validate family-specific
   fields per `references/key-families.md`.
4. Export the public wrapping key with `execute_action(action="export_wrapkey", params={...})`.
5. Wrap with `execute_action(action="wrap_key", params={...})`; confirm the result is 512 hex chars.
6. Register with `execute_action(action="register_key", params={...})`; optionally verify via
   `execute_action(action="discover", params={...})`.

## Workflow

1. **Confirm readiness.** Use `status`; inspect card contents with
   `execute_action(action="discover", params={...})` if unsure. For explicit applet-version proof
   (1.4+/1.5+), route through `s32sdaf-discovery-and-status` and use
   `volkano.exe --version` rather than inferring from command success.
2. **Validate inputs locally.** UID hex (16/32); plain key hex. For OID-
   sensitive or index-sensitive families, validate per
   `references/key-families.md` (ODAK/ADK1/ADK2 need a 32-hex UID; ADK1/ADK2
   need OID and key_index 0..15; ADK2 needs key type AES/ECC).
3. **Export the public wrapping key.** If not already available and trusted for
   this card, call `execute_action(action="export_wrapkey", params={...})` and capture the result.
4. **Wrap the plain key.** Call `execute_action(action="wrap_key", params={...})` with `plain_key`,
   exported `public_key`, optional `volkano_folder`. The underlying operation is
   `volkano_utils.exe -cmd wrap_key`; if the wrapper reports command-construction
   failures, treat it as a tooling defect and preserve that path. Validate the
   result is exactly 512 hex characters.
5. **Register the wrapped key.** Call `execute_action(action="register_key", params={...})` with
   `uid`, `key_type`, wrapped `key`, and optional `oid`, `key_index`,
   `adk2_key_type`, `password`, `volkano_folder`. State applet-version
   requirements explicitly when the command is gated.
6. **Verify result.** Optionally confirm with `execute_action(action="discover", params={...})`.

Show clear step boundaries (export -> wrap -> register) and never wrap a key
twice.

## Guardrails

**Scope** - Export and wrap are preparatory; the final registration is a
persistent smart-card write that creates/updates a UID record and consumes
storage capacity.

**Destructive actions** - Registration mutates the card. Confirm intent before
registering. Never invent passwords, UID, wrapping keys, OIDs, key selectors,
or key indexes.

**Secrets** - Do not echo the smart-card password unnecessarily.

**Refuse-and-escalate** -
- User already has a 512-hex wrapped key, or wants plain ADKP: stop; switch to
  `s32sdaf-register-key`.
- Wrapped result not 512 hex chars: stop before registration.
- Family selector missing/invalid (OID, key_index, adk2_key_type): stop and
  request it.
- See `references/key-families.md` for the full failure catalog.

## Validation loop

1. Confirm the user starts from a plain key intended for a wrapped family (not
   already wrapped, not plain ADKP).
2. Confirm UID/plain-key/family-specific fields validate.
3. Export wrapkey (or reuse a trusted current key), wrap, confirm 512 hex chars.
4. Register via the generic register-key tool.
5. Pass criterion: registration completes, applet constraints are stated where
   relevant, and next-step guidance (auth or debug-card) is provided.

## Out of scope

- Plain ADKP registration and registering already-wrapped material.
- Challenge-response authentication and record deletion.
- ADK2-backed debug-card / DCAT work (use `s32sdaf-generate-debug-card`).

## See Also

- `references/key-families.md` - per-family requirements, decision logic, and
  the full error-handling catalog.
- Related skills: `s32sdaf-register-key` (already-wrapped or plain ADKP),
  `s32sdaf-export-wrapkey` and `s32sdaf-wrap-key` (individual stages),
  `s32sdaf-auth-device` / `s32sdaf-hse2-authentication` (next-step auth),
  `s32sdaf-generate-debug-card` (ADK2 debug-card target),
  `s32sdaf-discovery-and-status` (readiness / applet-version proof).
