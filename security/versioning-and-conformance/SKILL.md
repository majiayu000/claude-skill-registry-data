---
name: versioning-and-conformance
kind: skill
status: ready
provenance:
  principles:
  - P012
  - P023
  - P024
  - P027
  - P101
  - P182
  - P194
  - P234
  - P235
  - P236
  - P237
  - P238
  claims:
  - C00598
  - C00599
  - C00609
  - C00610
  - C00614
  - C00615
  - C00605
  - C00606
  - C00618
  - C00619
  - C00623
  - C00624
  - C00608
  - C00613
  - C00621
  - C00622
  - C00625
  - C00626
  evidence:
  - E00588
  - E00589
  - E00597
  - E00598
  - E00602
  - E00603
  - E00593
  - E00594
  - E00606
  - E00607
  - E00611
  - E00612
  - E00596
  - E00601
  - E00609
  - E00610
  - E00613
  - E00614
  source_anchors:
  - 4f99907b2686-c0000
  authored_from_digest: 482607948ea4f2bb7b69dd1e24a60dfc2da49662ddd1e2bfe895618fe188a727
---

# Versioning And Conformance

Judge every behaviour against the negotiated protocol revision, not the newest. This skill packages
12 grounded principles the mcp-protocol-advisor applies when this layer of the Model Context
Protocol is in scope. Each finding names the rule, the protocol revision it belongs to, the failure
or interoperability break it prevents, the conforming behaviour, and the trade-off or residual risk.

## When this applies

- Assessing whether a feature or version identifier is valid for a negotiated MCP revision..
- Auditing MCP transport implementation or advertised transport support..
- Reviewing MCP authorization, token audience, protected-resource metadata, server discovery, scope consent, or client registration behavior..
- Reviewing an MCP client or server for version-specific conformance..
- Auditing tool descriptions, tool results, resource-link handling, or tool-call error classification..
- Auditing names, titles, icons, or other user-facing metadata for MCP tools, resources, templates, or prompts..
- The implementation uses HTTP transport and negotiates MCP 2025-06-18 or a later revision..
- An implementation sends, accepts, emits, requires, or documents JSON-RPC batches..
- Auditing server-to-user elicitation or elicitation schema handling..
- Auditing declared or accepted MCP content types..
- Auditing sampling requests or tool-selection parameters against revision 2025-11-25..
- Auditing lifecycle operation behavior against revision 2025-06-18 or a later revision..

## Procedure

Identify the negotiated protocol revision first, then apply the principles below that are in scope,
highest-risk first. For each one: name the rule and its revision, state the failure or
interoperability break it prevents, give the conforming behaviour, and state the trade-off or
residual risk. Never invent behaviour the spec does not define, and never weaken a consent or
security requirement below what the spec supports.

1. **P012 (high confidence).** Preserve MCP versioning scope: treat the date identifier as changing only for backwards-incompatible updates, and do not reject deprecated-but-present behavior before its removal window has elapsed.
2. **P023 (high confidence).** Match HTTP transport expectations to the negotiated revision: HTTP plus SSE belongs to 2024-11-05, Streamable HTTP begins in 2025-03-26, and 2025-11-25 adds stricter Origin and polling-stream behavior.
3. **P024 (high confidence).** Audit authorization requirements by revision: OAuth 2.1 appears in 2025-03-26, Resource Server metadata and RFC 8707 client behavior appear in 2025-06-18, and 2025-11-25 adds the newer discovery, consent, client metadata, and RFC 9728 alignment requirements.
4. **P027 (high confidence).** Start every MCP conformance review by identifying the negotiated protocol revision, then judge transport, authorization, tools, schema, and lifecycle behavior against that revision rather than against the newest specification by default.
5. **P101 (high confidence).** Review tool behavior against revision-specific MCP capabilities: annotations start in 2025-03-26, structured outputs and resource links start in 2025-06-18, and 2025-11-25 expects tool-input validation failures to be reported as Tool Execution Errors.
6. **P182 (high confidence).** Separate human-facing and programmatic naming checks by revision: title is expected from 2025-06-18 onward, and 2025-11-25 adds broader user-facing metadata and tool-name guidance.
7. **P194 (high confidence).** For HTTP MCP sessions on revision 2025-06-18 or newer, require the implementation to send or enforce the negotiated MCP-Protocol-Version header on post-initialization requests.
8. **P234 (high confidence).** Treat JSON-RPC batching as a narrow version marker: allow it only for MCP 2025-03-26 and flag it as non-conformant for 2024-11-05 or 2025-06-18 and newer.
9. **P235 (high confidence).** Apply elicitation checks only to revisions that support them, with 2025-06-18 as the starting point and 2025-11-25 as the revision that adds URL mode, expanded enum/result schema behavior, and primitive defaults.
10. **P236 (high confidence).** Check content-type support by negotiated revision: text and image are baseline, and audio should only be expected from 2025-03-26 onward.
11. **P237 (high confidence).** Expect sampling tool-calling controls only when auditing MCP 2025-11-25 sampling behavior.
12. **P238 (high confidence).** Enforce lifecycle-operation requirements as mandatory for MCP 2025-06-18 and newer rather than treating them as advisory guidance.

## Anti-patterns to flag

- Using a feature the peer never advertised, or skipping the initialization handshake and capability negotiation.
- Judging behaviour against the newest specification when an older revision was negotiated, or rejecting deprecated-but-present behaviour before its removal window.
- Inventing protocol behaviour the specification does not define, or presenting a proprietary extension as standard.
- Omitting the failure a rule prevents, the applicable revision, or the trade-off and residual risk.

## Grounding

Principles: P012, P023, P024, P027, P101, P182, P194, P234, P235, P236, P237, P238. Every cited
claim, evidence record, and source anchor resolves in this package's distilled spine
(`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). The Model Context
Protocol specification is distillation-only here: paraphrased, never quoted.

