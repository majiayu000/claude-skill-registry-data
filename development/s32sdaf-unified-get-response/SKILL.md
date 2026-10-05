---
name: s32sdaf-unified-get-response
description: Provide a single operational entry point for all S32SDAF / Volkano get_response workflows, from simple UID+challenge requests through HSE2 scheme-specific requests. Resolves UID references, validates inputs, inspects smart-card state when needed, selects the correct key path, and routes execution to either the MCP wrapper or a raw-command-capable path when required.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32sdaf
  see_also: '[s32sdaf-kb-entrypoint, s32sdaf-discovery-and-status, s32sdaf-auth-device, s32sdaf-hse2-authentication, s32sdaf-register-key, s32sdaf-generate-debug-card, s32sdaf-secure-debug-session]'
  tags: '[s32sdaf, volkano, smartcard, authentication, challenge-response, get-response, hse2, adkp, kuid, adk1, security]'
---

# S32SDAF Unified Get Response

A single operational entry point for **all** S32SDAF / Volkano `get_response`
workflows, from simple UID+challenge requests through HSE2 scheme-specific
requests. Resolve UID references, validate inputs, inspect smart-card state when
needed, choose the correct key path, and route execution to either the MCP
wrapper or a raw-command-capable path. `get_response` is broader than a simple
authentication helper - it is its own operational workflow.

## When to use

Use this skill whenever the user wants to calculate a response through
`volkano.exe get_response`: generic UID+challenge, requests naming a key family
(`ADKP`, `kUID`, `ADK1`), requests naming `scheme_id` 1/2/3, UID-by-index
references (`UID#2`), cases where wrapper-vs-raw selection matters, and flows
needing OID/key-name context for ADK1.

Do not use it to register or wrap keys by themselves, delete records, change
passwords, generate debug-card artifacts, or pretend the MCP wrapper supports
raw-command selectors it does not actually expose.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Tool | `status` | verify MCP server reachability/config |
| Tool | `execute_action(action="discover", params={...})` | inspect UIDs/keys; resolve `UID#<n>` |
| Tool | `execute_action(action="get_response", params={...})` | wrapper for cases that fit its surface |
| Command | raw `volkano.exe get_response` | raw-capable path for selectors beyond the wrapper |
| Reference | Cases, decision table, error catalog | `references/cases-and-errors.md` |

Do not assume any wrapper selector (`key`, `oid`, `scheme_id`, `key_name`)
exists unless the actual tool surface confirms it. If a flow needs selectors the
wrapper lacks and no raw-capable path is available, report the implementation
gap - do not fake support.

## Quickstart

1. If readiness/card state is unknown, run `status` /
   `execute_action(action="discover", params={...})`.
2. Resolve `UID#<n>` via discovery; validate direct UID and challenge locally.
3. Determine key family (honor explicit choice) and scheme (1/2/3).
4. Decide wrapper vs raw per `references/cases-and-errors.md`.
5. Execute with the exact UID, challenge, key family, and scheme.
6. Present resolved UID, key family, scheme, execution path, and response.

## Workflow

1. **Confirm readiness.** `status`; if UID/key state uncertain,
   `execute_action(action="discover", params={...})`.
2. **Resolve UID.** Validate a direct UID locally; resolve `UID#<n>` via
   discovery. If the index is absent, stop and report it.
3. **Validate the challenge.** Valid hex, even length, expected size for the
   scheme when documented. Stop on failure; do not normalize.
4. **Determine the key path.** Explicit user choice wins; infer only
   conservatively. Never silently swap `kUID` and `ADKP`. For `ADK1`, confirm
   `oid`/`key_name` context.
5. **Determine the scheme.** `1` generic/HSE1; `2` HSE2 BootROM; `3` HSE2
   HSE-FW. If HSE2 without BootROM/HSE-FW named, ask one concise question.
6. **Verify card contents when needed.** Confirm the UID exists and the
   requested key family/OID prerequisites are present; if missing, stop and
   explain the path cannot be executed with current card contents.
7. **Select wrapper vs raw.** If all required selectors fit the wrapper, use
   `execute_action(action="get_response", params={...})`; else use a raw-capable path, or stop with
   an implementation-gap explanation. See `references/cases-and-errors.md`.
8. **Execute** with exact inputs; pass only selectors the chosen path truly
   supports.
9. **Present the result** (resolved UID, original index if any, key family,
   scheme, execution path, response, caveats/next steps).

Treat `ADK2` as out of scope for normal `get_response`; redirect to debug-card /
DCAT when appropriate.

## Guardrails

**Scope** - Read-oriented; it should not modify smart-card registrations. It may
require authenticated card access and valid existing key material.

**Destructive actions** - None.

**Secrets** - Do not echo the smart-card password unnecessarily.

**Refuse-and-escalate** -
- `UID#<n>` not present: stop; do not guess another UID.
- UID not registered: redirect to `s32sdaf-register-key`.
- Malformed challenge or wrong size for scheme: stop; do not normalize.
- Required key material missing: stop; do not silently switch families.
- Selectors exceed the wrapper and no raw path exists: report the
  implementation gap; do not claim the raw path was tested.
- Wrapper fails after local validation passed: suspect a wrapper limitation
  before blaming the input.
- ADK2 requested: redirect to `s32sdaf-generate-debug-card`.
- Full case list and failure catalog: `references/cases-and-errors.md`.

## Validation loop

1. Confirm the request is recognized as a `get_response` workflow.
2. Confirm UID index inputs are resolved and the challenge validated before
   execution.
3. Confirm correct key-family and scheme selection.
4. Confirm wrapper-vs-raw selection was made explicitly and no unsupported
   selector was silently ignored.
5. Pass criterion: a clear response the user can apply to the target device, or
   a clear explanation of the exact failure class and next step.

## Out of scope

- Registering or wrapping keys, deleting records, changing passwords.
- Generating debug-card / DCAT artifacts (use `s32sdaf-generate-debug-card`).
- Claiming raw-command execution when no raw-capable tool was used.

## See Also

- `references/cases-and-errors.md` - supported cases, input validation,
  wrapper-vs-raw decision table, error catalog, and result formatting.
- Related skills: `s32sdaf-auth-device` (narrow generic flow),
  `s32sdaf-hse2-authentication` (HSE2 reasoning), `s32sdaf-kb-entrypoint`
  (routing broad prompts), `s32sdaf-discovery-and-status` (readiness),
  `s32sdaf-register-key` (provisioning), `s32sdaf-generate-debug-card` (ADK2),
  `s32sdaf-secure-debug-session` (enable secure debugging in an S32DS launch
  config; the debugger and card compute the response automatically).
