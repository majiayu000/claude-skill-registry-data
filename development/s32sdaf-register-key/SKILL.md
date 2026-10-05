---
name: s32sdaf-register-key
description: Register a device UID and associated smart-card key for S32SDAF / Volkano workflows using the current MCP tool surface. Covers plain ADKP plus wrapped and OID-sensitive families such as ODAK, ADK1, ADK2, KUID, KUID_RF, and KUID_PRE_FA, including applet-version requirements and per-family parameter validation.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32sdaf
  see_also: '[s32sdaf-wrap-and-register, s32sdaf-auth-device, s32sdaf-hse2-authentication, s32sdaf-generate-debug-card, s32sdaf-discovery-and-status]'
  tags: '[s32sdaf, volkano, smartcard, key-management, security, registration, adkp, odak, adk1, adk2, kuid, kuid_rf, kuid_pre_fa]'
---

# Register a Key on the Smart Card

Register a device UID and its associated key on a Volkano smart card. Covers
plain **ADKP** registration, wrapped families (`KUID`, `KUID_RF`,
`KUID_PRE_FA`, `ODAK`), and OID-sensitive families (`ADK1`, `ADK2`). The
preferred write tool is the generic `execute_action(action="register_key", params={...})`, which
covers all currently confirmed register commands.

**ADKP is the only key type that may be registered in plain form. All other
families use wrapped key material.**

## When to use

Use this skill to register a new UID + key, add/replace a key for an existing
UID, choose the correct registration path per family, validate UID/OID/key/
selector inputs, and surface applet-version requirements. Also use it to decide
whether the user already has final registration-ready material or must first
wrap a plain key.

Do not use it to wrap a plain non-ADKP key (use `s32sdaf-wrap-and-register`),
delete records, perform challenge-response by itself, generate a debug card by
itself, or guess passwords/UIDs/OIDs/keys/indexes.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Tool | `status` | verify MCP server reachability/config |
| Tool | `execute_action(action="discover", params={...})` | inspect registered UIDs before/after |
| Tool | `execute_action(action="register_key", params={...})` | primary generic register (all families) |
| Tool | `execute_action(action="register_key", params={"key_type":"ADKP", ...})` | compatibility wrapper for ADKP |
| Tool | `execute_action(action="register_key", params={"key_type":"kUID", ...})` | compatibility wrapper for plain KUID |
| Tool | `execute_action(action="find_installation")` | locate Volkano install |
| Reference | Per-family rules, decision logic, errors | `references/key-families.md` |

Prefer the generic register tool for new automation. For applet-gated commands
it returns a warning field. Family-specific rules (formats, OID, key_index,
adk2_key_type, applet 1.4+/1.5+) live in `references/key-families.md`.

## Quickstart

1. If readiness is unknown, run `status`; inspect with
   `execute_action(action="discover", params={...})` if needed.
2. Determine the family; validate inputs per `references/key-families.md`.
3. Plain ADKP -> `register_key(key_type="ADKP", ...)`.
4. Already-wrapped KUID/KUID_RF/KUID_PRE_FA/ODAK/ADK1/ADK2 (512 hex, with
   required selectors) -> `register_key(...)`.
5. Plain non-ADKP -> switch to `s32sdaf-wrap-and-register`.
6. Optionally verify with `execute_action(action="discover", params={...})`.

## Workflow

1. **Confirm readiness.** Use `status`; confirm what is registered
   with `execute_action(action="discover", params={...})`. For explicit applet-version proof
   (1.4+/1.5+), route through `s32sdaf-discovery-and-status` and use
   `volkano.exe --version` rather than inferring from command success.
2. **Validate inputs locally.** UID hex (16/32); wrapped keys 512 hex; OID valid
   hex/32 chars when required; ODAK/ADK1/ADK2 need a 32-hex UID; ADK1/ADK2
   key_index 0..15; ADK2 key type AES/ECC. Reject invalid formatting before any
   tool call. See `references/key-families.md`.
3. **Choose the path.**
   - Plain ADKP -> `register_key(key_type="ADKP")`.
   - Already-wrapped KUID/KUID_RF/KUID_PRE_FA/ODAK -> `register_key`.
   - Already-wrapped ADK1/ADK2 with all selectors -> `register_key`.
   - Plain non-ADKP -> switch to `s32sdaf-wrap-and-register`.
4. **Execute registration** with `uid`, `key_type`, `key` or `keybin`, and
   optional `oid`, `key_index`, `adk2_key_type`, `password`, `volkano_folder`.
5. **Verify result.** Optionally confirm the UID is present via
   `execute_action(action="discover", params={...})`; provide next-step guidance (authentication or
   debug-card generation).

Do not collapse ADK1/ADK2 semantics into generic KUID registration. Prefer
rejecting ambiguous input over guessing a key type.

## Guardrails

**Scope** - Persistent smart-card write: creates a UID record, adds/replaces
key material, and consumes limited storage. Not a read-only workflow.

**Destructive actions** - Registration mutates the card and can replace
existing key material for a UID. Confirm intent before writing. Never invent
UIDs, OIDs, keys, indexes, or passwords.

**Secrets** - Do not echo the smart-card password unnecessarily.

**Refuse-and-escalate** -
- Plain non-ADKP key: stop; switch to `s32sdaf-wrap-and-register`.
- Wrapped key not 512 hex chars, or missing family selector: stop and request
  correct input.
- ODAK with 8-byte UID: reject; requires a 16-byte UID.
- Card full: recommend discovery + deleting unused records before retry.
- Auth/password failure: report; do not retry with invented credentials.
- Full failure catalog: `references/key-families.md`.

## Validation loop

1. Confirm the correct registration path was selected for the family.
2. Confirm UID/OID/key/selector values validated before execution.
3. Confirm applet-version sensitivity was reported where relevant.
4. Execute via the generic register tool (or compat wrapper).
5. Pass criterion: registration succeeds (persistent state confirmed when
   executed) and next-step guidance is provided.

## Out of scope

- Wrapping a plain non-ADKP key (use `s32sdaf-wrap-and-register`).
- Deleting UID records; challenge-response authentication by itself.
- Generating a debug card / DCAT by itself.

## See Also

- `references/key-families.md` - per-family requirements, decision logic, and
  the full error-handling catalog.
- Related skills: `s32sdaf-wrap-and-register` (wrap plain non-ADKP first),
  `s32sdaf-auth-device` / `s32sdaf-hse2-authentication` (next-step auth),
  `s32sdaf-generate-debug-card` (ADK2 debug-card target),
  `s32sdaf-discovery-and-status` (readiness / applet-version proof).
