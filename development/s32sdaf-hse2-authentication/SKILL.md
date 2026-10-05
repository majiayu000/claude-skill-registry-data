---
name: s32sdaf-hse2-authentication
description: Perform S32SDAF HSE2-oriented authentication workflows by selecting the correct response-calculation scheme and key path documented by the knowledge base. Distinguishes HSE1 from HSE2, separates BootROM vs HSE-FW response schemes, and guides the agent through UID/OID/key-selection prerequisites for ADKP and ADK1-backed flows. Explicitly guards against assuming that the generic MCP get-response wrapper can represent raw Volkano HSE2 command semantics.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32sdaf
  see_also: '[s32sdaf-auth-device, s32sdaf-discovery-and-status, s32sdaf-register-key, s32sdaf-generate-debug-card]'
  tags: '[s32sdaf, volkano, hse2, authentication, challenge-response, bootrom, hse-fw, adkp, adk1, security]'
---

# HSE2 Authentication with S32SDAF

Guide the user through HSE2-capable S32SDAF challenge-response authentication,
selecting the correct scheme and key context documented by the KB. The KB
documents three schemes: `scheme_id = 1` (HSE1), `scheme_id = 2` (HSE2
BootROM-defined), and `scheme_id = 3` (HSE2 HSE-FW-defined). This skill covers
the HSE2 cases (`scheme_id = 2` and `3`).

## When to use

Use this skill when the user mentions HSE2, BootROM, HSE-FW, ADK1-backed
response calculation, or when the HSE1-vs-HSE2 distinction matters: choosing the
scheme, distinguishing BootROM from HSE-FW, deciding ADKP vs ADK1, validating
UID/challenge, clarifying when OID/key-name context is needed, and warning about
applet-version compatibility.

Do not use it for HSE1-only flows (except to compare/redirect to
`s32sdaf-auth-device`), debug-card/DCAT signing, key registration/wrapping by
themselves, or guessing scheme 2 vs 3 when the distinction matters operationally.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Command | `volkano.exe get_response` | raw HSE2 response with `-scheme_id`/`-oid`/`-key` |
| Tool | `status` | verify MCP/server readiness |
| Tool | `execute_action(action="discover", params={...})` | check UID presence and key assets |
| Tool | `execute_action(action="get_response", params={...})` | generic wrapper - UID+challenge only |
| Reference | Schemes, key paths, error catalog | `references/schemes-and-errors.md` |

**Hard wrapper limitation.** The generic MCP wrapper does not expose
`-scheme_id`, `-oid`, or `-key`. If the chosen HSE2 path needs any of them, the
wrapper is insufficient - do not claim it tested the raw HSE2 command path.

## Quickstart

1. Confirm this is truly HSE2 (else route to `s32sdaf-auth-device`).
2. Pick the scheme: BootROM -> `scheme_id = 2`; HSE-FW -> `scheme_id = 3`. If
   unknown, ask one concise question.
3. Determine key path: ADKP or ADK1 (ADK1 needs OID/key context).
4. Validate UID (hex) and challenge (valid hex, expected size); verify card and
   registration via discovery when uncertain.
5. If the mode needs selectors beyond the wrapper, use a raw-command-capable
   path or report the implementation gap; otherwise use the wrapper.
6. Present the response with scheme, key family, and any assumptions.

## Workflow

1. **Confirm HSE2.** If the user really wants HSE1 behavior, use
   `s32sdaf-auth-device` instead.
2. **Select the scheme.** `scheme_id = 2` (BootROM) or `3` (HSE-FW); ask one
   concise question if unclear. See `references/schemes-and-errors.md`.
3. **Validate prerequisites locally.** UID valid hex; challenge valid hex and
   the expected size (KB documents 32-byte challenge); determine ADKP vs ADK1;
   for ADK1 confirm OID / key-name or key-index context.
4. **Verify readiness when uncertain.** Use `s32sdaf-discovery-and-status` to
   confirm the card is reachable, the UID exists, and the expected key material
   is present.
5. **Compute the response.** First confirm the mode fits the execution surface.
   If the tooling supports the required selectors, use it; if only the generic
   wrapper (`uid`+`challenge`[+`password`/`volkano_folder`]) is available, use
   it only for HSE2 cases that need no extra selectors; otherwise stop and
   explain the wrapper cannot represent the required raw command shape. Response
   calculation supports `ADKP` and `ADK1`; `ADK2` is not supported here.
6. **Present the result** with the selected scheme, whether ADKP or ADK1 was
   used, any OID/key-name assumptions, and a reminder to send the response back
   to the target device.

## Guardrails

**Scope** - Read-oriented authentication; it should not modify smart-card
registrations. It may require authenticated card access and valid existing key
material.

**Destructive actions** - None.

**Secrets** - Do not echo the smart-card password unnecessarily.

**Refuse-and-escalate** -
- HSE2 but BootROM vs HSE-FW unknown: ask one concise question; do not guess.
- Selectors needed beyond the wrapper: do not substitute the wrapper for the
  raw command; report the implementation gap or use a raw-capable path.
- ADK1 without OID/key context: stop and resolve first.
- Applet < 1.5: treat 1.5+ as required for HSE2 schemes.
- ADK2 requested for challenge-response: redirect to
  `s32sdaf-generate-debug-card`.
- Wrapper reports a missing/invalid challenge that already passed local
  validation: suspect a wrapper-to-command mismatch, not the input.
- Full case list and failure catalog: `references/schemes-and-errors.md`.

## Validation loop

1. Confirm BootROM vs HSE-FW was chosen correctly (scheme 2 vs 3).
2. Confirm ADKP vs ADK1 was chosen correctly with any needed OID/key context.
3. Confirm no accidental fallback to HSE1 assumptions; applet 1.5+ called out.
4. Confirm wrapper-vs-raw selection was explicit for the chosen mode.
5. Pass criterion: a response artifact is returned with enough context to apply
   it, or a clear explanation that the wrapper cannot represent the required
   HSE2 raw command semantics.

## Out of scope

- HSE1-only response calculation (use `s32sdaf-auth-device`).
- Debug-card / DCAT signing (use `s32sdaf-generate-debug-card`).
- Key registration and key wrapping by themselves.

## See Also

- `references/schemes-and-errors.md` - scheme map, decision logic,
  key-selection guidance, and the full error-handling catalog.
- Related skills: `s32sdaf-auth-device` (generic/HSE1),
  `s32sdaf-discovery-and-status` (readiness), `s32sdaf-register-key`
  (provision ADKP/ADK1), `s32sdaf-generate-debug-card` (ADK2 debug-card),
  `s32sdaf-unified-get-response` (single entry point across all get_response).
