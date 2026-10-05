---
name: s32sdaf-wrap-key
description: Wrap a plain device key using the smart-card public wrapping key for S32SDAF / Volkano workflows. This workflow uses volkano_utils.exe -cmd wrap_key to produce wrapped material suitable for later registration. Resolves whether the user already has a valid public wrapping key or must export it first, validates input format, and produces wrapped key material suitable for later registration.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32sdaf
  see_also: '[s32sdaf-export-wrapkey, s32sdaf-wrap-and-register, s32sdaf-register-key]'
  tags: '[s32sdaf, volkano, smartcard, wrapping, key-management, public-key, security]'
---

# Wrap a Plain Key for Later Registration

Wrap a plain key using the smart-card public wrapping key so the result can
later be registered on the card. The grounded command path for this operation
is `volkano_utils.exe -cmd wrap_key`, not `volkano.exe`. This is a preparatory
workflow for users who want wrapped output now and will register it later.

Critical rule: **ADKP is the only key type that can be registered in plain
form.** Every non-ADKP key type must be wrapped first before registration.

## When to use

Trigger this skill when the user wants to:
- wrap a plain key now but register later ("wrap this key", "prepare wrapped key
  material", "I have a plain key and need the wrapped result only")
- prepare wrapped key material outside a full wrap-and-register workflow
- verify the difference between a plain key, the smart-card public wrapping key,
  and the final wrapped key

Do not use it to register the wrapped key, register plain ADKP, delete records,
or guess the semantic key type. If the user wants wrapping followed immediately
by registration, switch to `s32sdaf-wrap-and-register`. If the input already
appears wrapped, route to `s32sdaf-register-key`.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Tool | `status` | confirm server reachable when readiness uncertain |
| Tool | `execute_action(action="find_installation")` | resolve Volkano install path when needed |
| Tool | `execute_action(action="export_wrapkey", params={...})` | export the public wrapping key if the user has none |
| Tool | `execute_action(action="wrap_key", params={...})` | wrap the plain key (backed by `volkano_utils.exe -cmd wrap_key`) |

Inputs: `plain_key` (hex), optional `public_key` (hex), optional
`volkano_folder`.

## Quickstart

1. Verify readiness with `status` if the environment is not trusted.
2. Validate `plain_key` is hex; validate `public_key` if supplied.
3. If no trusted `public_key`, export it with
   `execute_action(action="export_wrapkey", params={...})`.
4. Wrap via `execute_action(action="wrap_key", params={...})` (inputs: `plain_key`, `public_key`,
   optional `volkano_folder`).
5. Return the wrapped key as registration-ready material, distinct from the
   public wrapping key used to create it.

## Workflow

1. Treat this as a preparatory workflow that does not itself modify card
   registrations. Distinguish plain key input, public wrapping key, and wrapped
   output at every step.
2. If the user already has a valid public wrapping key, do not force another
   export.
3. Validate hex format before calling the wrap tool. If the input already looks
   like wrapped output, stop and redirect to `s32sdaf-register-key` - do not
   wrap twice.
4. Obtain the public wrapping key via `execute_action(action="export_wrapkey", params={...})` when
   it is not already available and trusted.
5. Wrap via `execute_action(action="wrap_key", params={...})`. The underlying command is
   `volkano_utils.exe -cmd wrap_key`; do not describe it as a `volkano.exe`
   operation. If the wrapper errors in a way that suggests bad command
   construction, diagnose the wrapper or provide the exact `volkano_utils.exe`
   command shape rather than switching executables.
6. Return the wrapped output and route onward: registration -> route based on goal below.

Routing:
- Register the wrapped key now -> `s32sdaf-register-key`
- Combined wrap + register in one go -> `s32sdaf-wrap-and-register`

## Guardrails

**Scope** - Preparatory / non-registration. May export the public wrapping key
and generate wrapped material; does not modify card registrations.

**Destructive actions** - None here; the registration mutation happens in a
downstream skill. Never wrap a key twice.

**Secrets** - Treat plain key, public wrapping key, and wrapped output as
sensitive; do not echo unnecessarily.

**Refuse-and-escalate** -
- Missing `plain_key`: report it is required; do not continue.
- Input already wrapped: redirect to `s32sdaf-register-key`; do not re-wrap.
- Missing/invalid public wrapping key: export it from the card, or report that
  wrapping cannot proceed without a valid one.
- Export failure: report card readiness/access issue; recommend
  `s32sdaf-discovery-and-status`.
- Wrap failure: report the plain/public key may be invalid; recommend
  re-exporting the public wrapping key. If the error indicates missing/malformed
  command dispatch, note the expected `volkano_utils.exe -cmd wrap_key` path and
  treat it as a wrapper/backend problem, not a reason to switch to `volkano.exe`.
- User wants immediate registration: switch to `s32sdaf-wrap-and-register`.

## Validation loop

1. Confirm the public wrapping key was obtained or reused correctly.
2. Confirm the plain key was wrapped successfully.
3. Pass criterion: wrapped output is clearly identified as later registration
   input, and the next workflow is identified when the user wants to continue.

## Out of scope

- Registering the wrapped key on the card (see `s32sdaf-register-key`).
- Registering plain ADKP directly (see `s32sdaf-register-key`).
- Deleting records; guessing the semantic key type.

## See Also

- `s32sdaf-export-wrapkey` - export only the public wrapping key.
- `s32sdaf-wrap-and-register` - wrap then register in one workflow.
- `s32sdaf-register-key` - register already-wrapped material.
