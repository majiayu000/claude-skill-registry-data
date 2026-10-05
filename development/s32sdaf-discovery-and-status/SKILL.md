---
name: s32sdaf-discovery-and-status
description: Perform safe read-only discovery and readiness checks for S32SDAF / Volkano environments. Verifies MCP/server readiness, locates Volkano installations when needed, inspects registered smart-card UIDs, and establishes the correct next step before authentication or key-registration workflows.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32sdaf
  see_also: '[s32sdaf-kb-entrypoint, s32sdaf-auth-device, s32sdaf-register-key, s32sdaf-wrap-and-register, s32sdaf-secure-debug-session]'
  tags: '[s32sdaf, volkano, discovery, status, smartcard, readiness, diagnostics, security]'
---

# S32SDAF Discovery and Status

A safe, read-only first-step workflow for S32SDAF / Volkano usage. Use it to
learn whether the environment is ready, where Volkano is installed, whether a
smart card is reachable, and which UIDs/keys are already present before
attempting authentication or registration. It is the default operational handoff
from `s32sdaf-kb-entrypoint` when intent is broad or setup state is unknown.

## When to use

Trigger this skill to check server reachability, discover Volkano install
locations, verify the running Volkano/applet version, or inspect registered
UIDs. Typical phrasings: "check my S32SDAF setup", "is Volkano installed?",
"which UIDs are on the card?", "can I authenticate yet, or am I missing setup?".

Do not use it to register keys, wrap keys, generate responses, delete records,
change passwords, or perform any persistent smart-card mutation.

## Available Capabilities

The S32SDAF MCP server exposes exactly three tools: `status`, `search_actions`,
and `execute_action`. Every operation below runs through `execute_action` with a
named `action` and a `params` object; discover the exact action name and its
input schema first with `search_actions`.

| Type | Name | Invocation |
|------|------|------------|
| Tool | `status` | server reachability, config status, default Volkano install |
| Tool | `search_actions` | find the action name + input schema for the task |
| Action | `find_installation` | `execute_action(action="find_installation")` - list installed Volkano locations on disk |
| Command | `volkano.exe --version` | read Volkano/DLL/applet version, max UIDs, wrapping-key availability |
| Action | `discover` | `execute_action(action="discover", params={...})` - inspect UIDs/keys registered on the smart card |

Inputs (all optional, passed inside `params`): `volkano_folder`, `password`,
plus a general intent such as "is my setup ready?".

Every `execute_action` call returns the uniform envelope:
`{success: true, result: ...}` on success, or
`{success: false, error: {code, message, details}}` on failure. Read `success`
first, then `result` or `error`.

## Quickstart

1. Call `status` first. It already returns server readiness, the default
   Volkano install, AND the full installations list + recommended path in one
   call - this is normally enough.
2. Only call `execute_action(action="find_installation")` separately if
   `status` did not return an installations list, the data looks stale, or the
   user explicitly asks to re-scan disk. Do not call it in parallel with
   `status` "just in case".
3. If UID/key presence matters, call `execute_action(action="discover", params={...})`
   (with `password` inside `params` if required).
4. Summarize: server status, install path, card discovery outcome, registered
   assets, and the recommended next step.

## Workflow

1. Treat this as a read-only diagnostic; establish readiness before recommending
   any write-side mutation, and use discovery instead of guessing UID presence.
2. Check MCP/server readiness with the `status` tool (reachability, active
   configuration, default Volkano install used when no path is given).
3. Resolve install locations with `execute_action(action="find_installation")`
   only when `status` did not already provide a usable installations list /
   recommended path (e.g. it returned null or the user wants a fresh disk
   re-scan). If `status` already answered the question, skip this call.
4. Explicitly verify version with `volkano.exe --version` when the user asks for
   the applet version or needs grounded proof for a version-gated command (e.g.
   applet 1.4+ or 1.5+) rather than inferring compatibility from command success.
5. Inspect card contents with `execute_action(action="discover", params={...})`
   to list registered UIDs and determine whether follow-up registration or
   authentication is possible.
6. Summarize the discovered state and route onward:
   - challenge-response authentication -> `s32sdaf-auth-device`
   - direct ADKP / wrapped registration -> `s32sdaf-register-key`
   - plain-key wrapping then registration -> `s32sdaf-wrap-and-register`
   - debugging a secured device from S32DS -> `s32sdaf-secure-debug-session`

Note: the smart-card UIDs listed here are the keys registered on the card, not
the SoC UID of a locked target. Read the target's SoC UID via the Secure Keys
Registry "Connect" button or headless with `gta.exe -t s32dbg:<ip>` (UID0/UID1),
then confirm a matching key is registered before a secure-debug unlock.

Preferred summary shape: **Server status** / **Volkano installation** /
**Smart-card discovery** / **Registered assets** / **Recommended next step**.

## Guardrails

**Scope** - Read-only. May inspect server state, installation presence, and
smart-card contents; must not change smart-card storage or configuration.

**Destructive actions** - None.

**Secrets** - Require but do not echo the smart-card password.

**Refuse-and-escalate** -
- Server not ready: report readiness could not be confirmed; show the active
  config if available; recommend verifying S32SDAF server configuration.
- Volkano not found: report no installation found in expected locations;
  recommend verifying installation.
- Card unavailable: ask the user to verify card insertion and reader connection.
- Auth/password failure: explain a valid password may be required; do not guess.
- No UIDs found: report the card is reachable but empty; recommend registration
  if the user intends to authenticate later.

## Validation loop

1. Check server readiness, installation path, and version when relevant.
2. Inspect card contents when relevant.
3. Pass criterion: the user is clearly told what is ready and what is missing,
   and the correct next workflow is identified without unnecessary guessing.

## Out of scope

- Any persistent smart-card mutation (registration, wrapping, deletion,
  password change).
- Generating challenge responses.

## See Also

- `s32sdaf-kb-entrypoint` - broad intent router for S32SDAF prompts.
- `s32sdaf-auth-device` - challenge-response authentication after discovery.
- `s32sdaf-register-key` - direct key registration after discovery.
- `s32sdaf-wrap-and-register` - wrap-then-register after discovery.
- `s32sdaf-secure-debug-session` - debug a secured device from S32DS after
  confirming the UID + key are registered.
