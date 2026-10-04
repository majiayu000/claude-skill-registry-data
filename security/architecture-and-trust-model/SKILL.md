---
name: architecture-and-trust-model
kind: skill
status: ready
provenance:
  principles:
  - P015
  - P028
  - P045
  - P056
  - P057
  - P058
  - P059
  - P115
  - P116
  - P117
  - P118
  - P119
  - P120
  - P121
  - P164
  - P166
  - P167
  claims:
  - C00038
  - C00039
  - C00046
  - C00047
  - C00435
  - C00437
  - C00050
  - C00051
  - C00057
  - C00058
  - C00062
  - C00063
  - C00067
  - C00068
  - C00432
  - C00433
  - C00033
  - C00034
  - C00042
  - C00043
  - C00044
  - C00045
  - C00055
  - C00056
  - C00060
  - C00061
  - C00065
  - C00066
  - C00438
  - C00439
  - C00436
  - C00434
  evidence:
  - E00037
  - E00038
  - E00045
  - E00046
  - E00426
  - E00428
  - E00049
  - E00050
  - E00056
  - E00057
  - E00061
  - E00062
  - E00066
  - E00067
  - E00423
  - E00424
  - E00033
  - E00034
  - E00041
  - E00042
  - E00043
  - E00044
  - E00054
  - E00055
  - E00059
  - E00060
  - E00064
  - E00065
  - E00429
  - E00430
  - E00427
  - E00425
  source_anchors:
  - 0b6ac42ddf2e-c0000
  - ddb8b9b444ad-c0000
  authored_from_digest: cbd2c080be86e5dc2ef46162cc827f051cc41dd546de76cddbe1779d48da5de6
---

# Architecture And Trust Model

Assign each capability to the right side and concentrate trust in the host. This skill packages 17
grounded principles the mcp-protocol-advisor applies when this layer of the Model Context Protocol
is in scope. Each finding names the rule, the protocol revision it belongs to, the failure or
interoperability break it prevents, the conforming behaviour, and the trade-off or residual risk.

## When this applies

- Deciding where authorization and consent checks live.
- Implementing client-side protocol handling.
- Deciding which MCP primitive a given capability should be exposed as.
- Scoping a server's responsibilities or deployment model.
- Deciding what context to forward to a server.
- Implementing the initialization handshake.
- Performing subscriptions, tool calls, or sampling.
- Designing or implementing an MCP server that exposes capabilities to a client and model.
- Designing or reviewing an MCP integration topology.
- Routing model calls or assembling context from multiple servers.
- Mapping clients to servers.
- Making protocol or SDK design trade-offs.
- Adding new protocol features or versioning.
- A server implements a feature or a non-standard capability.
- A capability lets the model perform an action or actively retrieve information.
- A capability provides structured data or content as context to the model.
- A capability is a pre-defined template a user chooses to invoke.

## Procedure

Identify the negotiated protocol revision first, then apply the principles below that are in scope,
highest-risk first. For each one: name the rule and its revision, state the failure or
interoperability break it prevents, give the conforming behaviour, and state the trade-off or
residual risk. Never invent behaviour the spec does not define, and never weaken a consent or
security requirement below what the spec supports.

1. **P015 (high confidence).** Concentrate all security enforcement — connection permissions, consent, security policy, and user authorization — in the host process rather than in clients or servers.
2. **P028 (high confidence).** Assign the client the responsibilities of protocol/capability negotiation, bidirectional message routing, subscription and notification management, and maintaining isolation between the servers a host connects to.
3. **P045 (high confidence).** Assign each server capability to the primitive that matches its control owner: user-invoked interaction templates become prompts (user-controlled), client-managed contextual data becomes resources (application-controlled), and model-invokable actions become tools (model-controlled).
4. **P056 (high confidence).** Keep servers focused and independent: expose functionality only through MCP primitives (resources, tools, prompts), each server owning a narrow responsibility, deployable as a local process or remote service.
5. **P057 (high confidence).** Enforce least-context isolation: a server must not read the whole conversation or see into other servers, must receive only the context necessary for its task, and all cross-server interaction is mediated by the host.
6. **P058 (high confidence).** Negotiate capabilities explicitly at initialization; the declared capability set fixes which features and primitives are available for that session, and both parties must honour it throughout.
7. **P059 (high confidence).** Gate every optional protocol operation on a prior capability declaration: emit resource subscription notifications only if subscription support was declared, allow tool invocation only if the tool capability was declared, and allow a server sampling request only if the client declared sampling support.
8. **P115 (high confidence).** When building an MCP server, model all context and capabilities using the three standard server primitives — prompts, resources, and tools — rather than ad-hoc mechanisms, so clients and models can discover and use them consistently.
9. **P116 (high confidence).** Model the system as client-host-server: a single host process runs multiple client instances, and this separation is the mechanism for security boundaries and concern isolation.
10. **P117 (high confidence).** Make the host the sole owner of context aggregation and AI/LLM sampling coordination across clients.
11. **P118 (high confidence).** Give each client exactly one isolated, stateful session with a single server (1:1), so a client never multiplexes across servers.
12. **P119 (high confidence).** Optimise the protocol so servers are extremely easy to build and highly composable: push complex orchestration to the host and keep each server's interface simple and combinable.
13. **P120 (high confidence).** Design for progressive, backward-compatible evolution: keep the core protocol minimal and required, negotiate everything else, and let clients and servers evolve independently.
14. **P121 (high confidence).** Require a server to advertise every implemented feature in its declared capabilities, and use protocol extensions for any capability beyond the standard negotiated set.
15. **P164 (high confidence).** Expose executable, action-taking or side-effecting operations (such as API POST requests or file writes) as tools, because tools are the model-controlled primitive through which a model performs actions or retrieves information.
16. **P166 (high confidence).** Expose read-only contextual data (such as file contents or git history) as resources that the client attaches and manages, rather than as tools, since resources are the application-controlled primitive for providing additional context to the model.
17. **P167 (high confidence).** Expose reusable, user-invoked interaction templates (such as slash commands or menu options) as prompts, because prompts are the user-controlled primitive of pre-defined templates that guide language-model interactions.

## Anti-patterns to flag

- Using a feature the peer never advertised, or skipping the initialization handshake and capability negotiation.
- Judging behaviour against the newest specification when an older revision was negotiated, or rejecting deprecated-but-present behaviour before its removal window.
- Inventing protocol behaviour the specification does not define, or presenting a proprietary extension as standard.
- Omitting the failure a rule prevents, the applicable revision, or the trade-off and residual risk.

## Grounding

Principles: P015, P028, P045, P056, P057, P058, P059, P115, P116, P117, P118, P119, P120, P121,
P164, P166, P167. Every cited claim, evidence record, and source anchor resolves in this package's
distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). The
Model Context Protocol specification is distillation-only here: paraphrased, never quoted.

