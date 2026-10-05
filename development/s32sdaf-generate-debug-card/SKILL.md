---
name: s32sdaf-generate-debug-card
description: Generate an HSE2-oriented debug card workflow artifact for S32SDAF using volkano_utils.exe and compute its authentication tag with volkano.exe using an ADK2 key. Guides the agent through debug-card input preparation, smart-card prerequisites, applet-version checks, signature encoding choices, and the distinction between generating the debug-card BLOB and signing/authenticating it.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32sdaf
  see_also: '[s32sdaf-discovery-and-status, s32sdaf-register-key, s32sdaf-hse2-authentication, s32sdaf-kb-entrypoint]'
  tags: '[s32sdaf, volkano, volkano-utils, hse2, debug-card, dcat, adk2, oid, security]'
---

# Generate and Authenticate a Debug Card

Guide the user through the two-stage S32SDAF debug-card workflow for
HSE2-oriented secure debug: (1) generate the debug card BLOB with
`volkano_utils.exe generate_debug_card`, and (2) compute the debug card
authentication tag (DCAT) with `volkano.exe get_dcat` using an `ADK2` key.
Generating the debug-card file does not itself authenticate or sign it - keep
the two stages clearly separated.

## When to use

Use this skill to generate a debug card BLOB from an input JSON/JSONC file,
compute the DCAT with `ADK2`, choose RAW vs ASN.1 signature encoding, and
verify the prerequisites for debug-card authentication (UID/OID/ADK2/applet).

Do not use it for plain challenge-response without a debug card, ADKP-only
flows, wrapping keys unrelated to debug-card signing, inventing JSON schema
fields, or assuming UID/OID/ADK2/applet exist without checking.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Command | `volkano_utils.exe generate_debug_card` | generate the debug card BLOB from input JSON/JSONC |
| Command | `volkano.exe get_dcat` | compute the DCAT using ADK2 |
| Tool | `status` | verify MCP/server configuration |
| Tool | `execute_action(action="find_installation")` | locate Volkano install |
| Tool | `execute_action(action="discover", params={...})` | inspect whether the UID is present |

If MCP wrappers for `generate_debug_card` / `get_dcat` do not yet exist, this
skill still provides the grounded documented workflow and prerequisites.

## Grounded command reference

- BLOB: `volkano_utils.exe generate_debug_card -input <input json file>`
- DCAT: `volkano.exe get_dcat -uid <UID> -oid <OID> -key [key name]
  -debug_card <input binary file> -encoding <RAW|ASN.1>` with optional
  `--append_signature` (appends signature to the debug-card file).

Expectations from the KB: `UID` and `OID` are 16 bytes; `get_dcat` requires
applet version **1.5+**; signature encoding is `RAW` or `ASN.1` (use the format
the downstream consumer expects).

## Quickstart

1. Decide whether the user wants only the BLOB, or the full signed flow.
2. If setup state is untrusted, run `s32sdaf-discovery-and-status`.
3. For DCAT, confirm 16-byte UID, 16-byte OID, a registered ADK2 key for that
   UID/OID, and applet 1.5+.
4. Generate BLOB:
   `volkano_utils.exe generate_debug_card -input <file>`.
5. Compute DCAT:
   `volkano.exe get_dcat -uid ... -oid ... -key ... -debug_card ... -encoding RAW|ASN.1`.
6. Present the BLOB path, the tag/signature, encoding, and append state.

## Workflow

1. **Confirm intent.** Only the debug card BLOB, or the full workflow including
   the authentication tag / signature.
2. **Verify readiness if needed.** Use `s32sdaf-discovery-and-status`. Confirm
   Volkano is available, the card is reachable if DCAT is needed, and the
   relevant UID exists on the card.
3. **Validate DCAT prerequisites.** 16-byte UID, 16-byte OID, a registered ADK2
   key for that UID/OID, applet 1.5+. If any are missing or unknown, stop and
   resolve first (redirect to `s32sdaf-register-key` when ADK2 is unprovisioned).
4. **Generate the BLOB.** Run `volkano_utils.exe generate_debug_card -input
   <file>`. The input file must be fully completed; do not invent missing
   values. If the file is partial, ask the user to complete it first.
5. **Compute the DCAT.** Run `volkano.exe get_dcat` with `-uid`, `-oid`,
   `-key`, `-debug_card`, `-encoding`, and optional `--append_signature`.
6. **Present the result.** Debug-card file path, authentication tag/signature,
   encoding used, whether the signature was appended, and any downstream
   assumptions the user must still verify.

The most common confusion is assuming BLOB generation is enough; the second
common failure is missing ADK2 / OID / applet 1.5+ prerequisites.

## Guardrails

**Scope** - May generate local files (debug card BLOB) and read smart-card
state for signing. It must not mutate smart-card registrations unless the agent
deliberately redirects into a registration workflow first.

**Destructive actions** - `--append_signature` modifies the debug-card file in
place; confirm that is intended before using it.

**Secrets** - Do not echo the smart-card password unnecessarily.

**Refuse-and-escalate** -
- Missing/partial input JSON/JSONC: stop; do not invent contents.
- UID/OID missing: use discovery or request the values.
- ADK2 key missing: redirect to `s32sdaf-register-key`.
- Applet < 1.5: do not proceed as if `get_dcat` works; treat 1.5+ as required.
- Unsure RAW vs ASN.1: ask which format the consumer expects; do not guess.
- Card unreachable for DCAT: report the signing step cannot proceed; verify
  connectivity via discovery/status.

## Validation loop

1. Confirm BLOB generation and authentication are treated as separate stages.
2. Confirm DCAT prerequisites (UID/OID/ADK2/applet 1.5+) are validated before
   `get_dcat`.
3. Confirm no missing UID/OID/ADK2/JSON content was guessed.
4. Generate the BLOB and (if requested) compute the DCAT.
5. Pass criterion: the user receives a clear next-step artifact set (BLOB path
   plus tag/signature and encoding) for secure debug usage.

## Out of scope

- Plain challenge-response authentication without a debug card.
- ADKP-only workflows and key wrapping unrelated to debug-card signing.
- HSE2 response calculation without a debug card (use
  `s32sdaf-hse2-authentication`).

## See Also

- Related skills: `s32sdaf-discovery-and-status` (readiness/UID inspection),
  `s32sdaf-register-key` (provision the ADK2 key), `s32sdaf-hse2-authentication`
  (HSE2 response calculation without a debug card), `s32sdaf-kb-entrypoint`
  (route broad prompts).
