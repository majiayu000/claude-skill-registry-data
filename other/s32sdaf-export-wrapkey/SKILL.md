---
name: s32sdaf-export-wrapkey
description: Export the smart card's public wrapping key for S32SDAF / Volkano workflows. Resolves installation and card-readiness prerequisites, executes the read-side export operation, and explains when the exported key should be used directly versus handed off to wrap-and-register workflows.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32sdaf
  see_also: '[s32sdaf-discovery-and-status, s32sdaf-wrap-and-register, s32sdaf-register-key]'
  tags: '[s32sdaf, volkano, smartcard, wrapkey, export, public-key, wrapping, security]'
---

# Export the Smart-Card Public Wrapping Key

Export the public wrapping key from the current Volkano smart card so it can be
used to wrap plain key material before wrapped-key registration. This is a
narrow, read-oriented helper that keeps three values distinct: the public
wrapping key, the plain device key, and the final wrapped key.

## When to use

Trigger this skill when the user wants to:
- export the public wrapping key from the card ("export the wrap key", "get the
  smart-card public key for wrapping")
- prepare for an offline or later key-wrapping step
- inspect or reuse the wrapping key for `KUID` / wrapped-key onboarding
- explicitly separate `export wrapkey` from later `wrap` or `register` steps

Do not use it to wrap a plain key, register wrapped material, delete records, or
decide plain ADKP registration. If the user already has a valid public wrapping
key, do not force a re-export - route onward instead.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Tool | `status` | confirm server reachable and default installation known |
| Tool | `execute_action(action="find_installation")` | resolve Volkano install path when needed |
| Tool | `execute_action(action="export_wrapkey", params={...})` | export the public wrapping key from the card |

## Quickstart

1. If readiness is unknown, call `status` (and
   `execute_action(action="find_installation")` if the path must be resolved).
2. Call `execute_action(action="export_wrapkey", params={...})` with optional `volkano_folder` and
   `password`.
3. Present the exported value as the smart-card public wrapping key, suitable
   for wrapping plain key material - not itself the wrapped device key.

## Workflow

1. Treat this as a read-side helper; verify readiness before export if the
   environment is not yet trusted.
2. Do not invent a public key - export it from the currently selected card
   unless the user already has one.
3. Export via `execute_action(action="export_wrapkey", params={...})`. Inputs: optional
   `volkano_folder`, optional `password`.
4. Describe the result clearly so the user does not confuse the public wrapping
   key with wrapped key material.
5. Route onward if the user wants to continue:
   - plain key to wrap and register -> `s32sdaf-wrap-and-register`
   - already wrapped key to register -> `s32sdaf-register-key`

## Guardrails

**Scope** - Read-oriented. Exports public key material only; does not modify
card contents.

**Destructive actions** - None. If the user's real goal is wrapping or
registration, route to the appropriate downstream skill rather than performing
a mutation here.

**Secrets** - Require but do not echo the smart-card password; treat exported
key material as sensitive.

**Refuse-and-escalate** -
- Card unreachable: ask the user to verify card insertion and reader
  availability; recommend `s32sdaf-discovery-and-status`.
- Install path unresolved: use `execute_action(action="find_installation")`; do not
  guess a path.
- Authentication/password failure: ask for the correct password; do not guess.
- User needs more than export: explain export only yields the public wrapping
  key and route to `s32sdaf-wrap-and-register` or `s32sdaf-register-key`.

## Validation loop

1. Confirm readiness when relevant.
2. Confirm the export succeeded and returned a public wrapping key.
3. Pass criterion: the exported value is described as a public wrapping key and,
   if the user wants to continue, the correct next workflow is identified.

## Out of scope

- Wrapping a plain key (see `s32sdaf-wrap-key` / `s32sdaf-wrap-and-register`).
- Registering wrapped material (see `s32sdaf-register-key`).
- Deleting records or challenge-response authentication.

## See Also

- `s32sdaf-wrap-and-register` - continue immediately from export to wrap+register.
- `s32sdaf-register-key` - register already-wrapped key material.
- `s32sdaf-discovery-and-status` - verify readiness and card availability first.
