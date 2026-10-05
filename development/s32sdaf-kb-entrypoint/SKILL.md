---
name: s32sdaf-kb-entrypoint
description: Automatic KB-first entrypoint and router for SDAF / S32SDAF / Volkano-related requests. Detects direct and indirect SDAF intent from broad user prompts, consults the s32sdaf knowledge base for definitions and explanations before answering, performs safe status/discovery steps when context is missing, and routes to the correct downstream workflow without requiring the user to explicitly request knowledge-base lookup.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32sdaf
  see_also: '[s32sdaf-auth-device, s32sdaf-hse2-authentication, s32sdaf-register-key, s32sdaf-wrap-and-register, s32sdaf-discovery-and-status, s32sdaf-secure-debug-session]'
  tags: '[s32sdaf, sdaf, volkano, router, discovery, knowledge-base, smartcard, authentication, registration, security, kb-first]'
---

# S32SDAF KB Entrypoint

The automatic KB-first entrypoint for any SDAF / S32SDAF / Volkano request,
even when the user does not explicitly ask to search the knowledge base or name
the correct workflow. Interpret the request, consult the `s32sdaf` KB for
meaning/terminology, run safe status/discovery when context is missing, and
route to the correct downstream skill with minimal clarification.

## When to use

Activate automatically whenever the prompt mentions or strongly implies `SDAF`,
`S32SDAF`, `Volkano`, smart card, secure debug authorization/authentication,
challenge-response, UID registration, `ADKP`, `KUID`, `KUID_RF`,
`KUID_PRE_FA`, `ODAK`, wrap key, register key, or authenticate device - or asks
a broad secure-debug onboarding/"what can I do"/"how does it work" question in
an S32SDAF context.

Do not use it to perform destructive mutations before intent is clear, to guess
missing UID/key/password/challenge values, to bypass a dedicated downstream
skill once intent is clear, or to invent acronym expansions when the KB is
available.

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| Tool | `nxp_knowledge_kb_list_corpora` | verify the `s32sdaf` corpus is available |
| Tool | `nxp_knowledge_kb_search` | search `s32sdaf` for definitions/terminology/workflow |
| Tool | `status` | verify MCP server reachability/config |
| Tool | `execute_action(action="find_installation")` | locate Volkano install |
| Tool | `execute_action(action="discover", params={...})` | inspect registered UIDs/keys |

Do not jump to write-side tools from this skill unless intent is already clear
and a downstream workflow has been selected.

## KB-first rule

For any definitional, acronym-expansion, terminology, or explanatory prompt
involving SDAF / S32SDAF / Volkano / secure debug authorization/authentication,
query the `s32sdaf` KB **before** answering. Do not expand `SDAF` from memory
when the KB is available. If the KB has no exact expansion/definition, say so
explicitly and label any additional interpretation as inference. If KB and
memory conflict, prefer the KB and say so.

## Quickstart

1. Detect SDAF/S32SDAF/Volkano intent -> activate automatically.
2. Explanatory/terminology prompt -> `nxp_knowledge_kb_search` on `s32sdaf`
   first, then answer with KB-grounded wording.
3. Operational and specific -> route immediately to the matching downstream
   skill.
4. Operational but underspecified -> run safe discovery/status, or ask one
   concise routing question.

## Workflow

1. **Detect intent automatically** without waiting for an explicit KB-search
   request.
2. **Classify explanatory vs operational.** Is the user asking for a
   definition/explanation, or to authenticate / register / wrap-and-register /
   inspect the environment?
3. **Explanatory -> KB first.** Search `s32sdaf`, prefer exact KB phrasing, add
   source references when useful. Summarize the available workflows
   (authentication, registration, wrap-and-register, discovery).
4. **Operational and specific -> route:**
   - authentication -> `s32sdaf-auth-device`
     (HSE2/scheme/OID-sensitive -> `s32sdaf-hse2-authentication`).
   - final registration-ready material -> `s32sdaf-register-key`.
   - plain key needing wrapping -> `s32sdaf-wrap-and-register`.
   - readiness / "which UIDs" / install path -> discovery/status tools.
   - debug a secured/locked device from S32DS ("Target is secured",
     Error 102/601, enable secure debugging) -> `s32sdaf-secure-debug-session`.
5. **Operational but ambiguous -> safe checks first.** Prefer
   `status`, `execute_action(action="find_installation")`, or
   `execute_action(action="discover", params={...})`, then ask one concise routing question.
6. **Keep clarification minimal** - one short, high-value question at a time,
   not a full parameter interrogation.

Preferred clarification questions:
- "Are you asking what SDAF means, or do you want to perform an operation now?"
- "Authenticate a device, register a key, or inspect what is on the card?"
- "Do you already have a wrapped key, or need a plain key wrapped first?"

## Guardrails

**Scope** - Usually read-oriented and low-risk: KB search, explanation,
workflow selection, safe discovery/readiness checks. Persistent smart-card
mutation should occur only after handing off to a downstream registration
workflow.

**Destructive actions** - Do not delete or mutate the card from this skill.

**Secrets** - Do not request or echo UID/key/password/challenge values that the
downstream workflow does not yet need.

**Refuse-and-escalate** -
- Vague request ("help with SDAF"): summarize workflows, ask one routing
  question, optionally suggest discovery first; if definitional, KB first.
- Environment/registration state unknown: prefer discovery over guessing.
- Ambiguous key path (ADKP vs wrapped vs plain-to-be-wrapped): ask one
  disambiguation question; do not guess from wording alone.
- KB hit missing/incomplete: say so, give the closest KB-grounded answer, label
  non-KB content as inference.
- User expects fully automatic execution from a vague prompt: explain that
  intent can be inferred, but UID/challenge/key/password must come from the
  user or environment.

## Validation loop

1. Confirm SDAF/S32SDAF/Volkano intent was recognized automatically.
2. For explanatory prompts, confirm the KB was consulted before answering.
3. Confirm the correct downstream skill was selected, or a safe discovery step
   chosen.
4. Confirm clarification burden stayed minimal and no unsafe mutation occurred.
5. Pass criterion: the user is either KB-grounded-answered or handed to the
   right downstream workflow with minimal friction.

## Out of scope

- Performing destructive mutations directly (delegate to downstream skills).
- Deep per-workflow execution detail (that lives in the downstream skills).
- Inventing acronym expansions or terminology when the KB is available.

## See Also

- Related skills: `s32sdaf-auth-device`, `s32sdaf-hse2-authentication`,
  `s32sdaf-register-key`, `s32sdaf-wrap-and-register`,
  `s32sdaf-discovery-and-status`, `s32sdaf-unified-get-response`,
  `s32sdaf-secure-debug-session` (debug a secured device from S32DS).
