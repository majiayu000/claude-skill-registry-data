---
name: base-protocol-and-messages
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P004
  - P007
  - P010
  - P013
  - P016
  - P026
  - P052
  - P055
  - P060
  - P062
  - P063
  - P064
  - P066
  - P103
  - P111
  - P112
  - P113
  - P114
  - P122
  - P123
  - P183
  - P195
  - P196
  - P239
  claims:
  - C00005
  - C00008
  - C00090
  - C00091
  - C00025
  - C00512
  - C00010
  - C00011
  - C00018
  - C00019
  - C00097
  - C00098
  - C00017
  - C00020
  - C00024
  - C00026
  - C00070
  - C00071
  - C00074
  - C00075
  - C00077
  - C00078
  - C00080
  - C00081
  - C00094
  - C00095
  - C00105
  - C00106
  - C00085
  - C00086
  - C00001
  - C00002
  - C00003
  - C00004
  - C00088
  - C00089
  - C00006
  - C00007
  - C00083
  - C00084
  - C00103
  - C00104
  - C00108
  - C00109
  - C00102
  - C00110
  - C00016
  evidence:
  - E00005
  - E00008
  - E00089
  - E00090
  - E00025
  - E00503
  - E00010
  - E00011
  - E00018
  - E00019
  - E00096
  - E00097
  - E00017
  - E00020
  - E00024
  - E00026
  - E00069
  - E00070
  - E00073
  - E00074
  - E00076
  - E00077
  - E00079
  - E00080
  - E00093
  - E00094
  - E00104
  - E00105
  - E00084
  - E00085
  - E00001
  - E00002
  - E00003
  - E00004
  - E00087
  - E00088
  - E00006
  - E00007
  - E00082
  - E00083
  - E00102
  - E00103
  - E00107
  - E00108
  - E00101
  - E00109
  - E00016
  source_anchors:
  - 37bf1590e3e5-c0000
  - a504a3403936-c0000
  - 8ed43301d44f-c0000
  authored_from_digest: 59f2a08caa6f29e118cc717e035e673b63d75d7df8c06c39f07b38b14133a440
---

# Base Protocol And Messages

Build on the JSON-RPC base protocol and shape every MCP message to spec. This skill packages 25
grounded principles the mcp-protocol-advisor applies when this layer of the Model Context Protocol
is in scope. Each finding names the rule, the protocol revision it belongs to, the failure or
interoperability break it prevents, the conforming behaviour, and the trade-off or residual risk.

## When this applies

- Establishing or reviewing the transport and handshake layer of an MCP connection.
- Defining the transport/message layer or session lifecycle.
- Designing or reviewing MCP wire messages.
- Processing JSON Schemas within MCP messages.
- Auditing schema definitions, validators, or schema dialect assumptions against revision 2025-11-25..
- Consuming tool metadata such as descriptions or annotations from a server.
- A client consumes annotation metadata attached to a tool.
- Deciding where a feature belongs or reviewing a server/client feature surface.
- Any MCP operation that accesses user data or performs an action on the user's behalf.
- A host is about to share user or resource data with a server or any external destination.
- Attaching or reading _meta metadata on MCP interactions.
- Building, deploying, or reviewing the security posture of an MCP host, client, or server.
- A host or client is about to invoke an MCP tool on the user's behalf.
- Reviewing or building any MCP client or server implementation.
- Constructing or validating MCP requests.
- Returning a successful MCP operation result.
- Returning an MCP error.
- Validating a schema carried in an MCP message.
- Fetching or rendering an MCP icon from metadata.
- Choosing an authentication/authorization approach for an MCP transport.
- Designing how an LLM application will consume external context, data, or tools.
- Implementing or reviewing conformance of an MCP client or server.
- Referencing or validating against the MCP protocol schema.
- Designing or documenting the architecture and responsibilities of an MCP deployment.
- Sending or receiving MCP notifications.
- A client that renders MCP icons.
- Rendering icons that may be oversized or carry executable content.
- Exposing or consuming MCP icons.
- Accepting an icon file for rendering.
- Implementing a production-grade MCP client or server.

## Procedure

Identify the negotiated protocol revision first, then apply the principles below that are in scope,
highest-risk first. For each one: name the rule and its revision, state the failure or
interoperability break it prevents, give the conforming behaviour, and state the trade-off or
residual risk. Never invent behaviour the spec does not define, and never weaken a consent or
security requirement below what the spec supports.

1. **P001 (high confidence).** Build on the MCP base protocol: exchange JSON-RPC 2.0 messages over stateful connections and complete client/server capability negotiation before using any feature.
2. **P004 (high confidence).** Handle JSON Schema dialects explicitly: default to 2020-12 when no $schema is declared, allow a $schema field to select another dialect, support at least 2020-12 while documenting any additional dialects, and prefer 2020-12.
3. **P007 (high confidence).** Treat tool annotations as untrusted input: a client must not rely on tool annotations for security decisions unless they come from a trusted server.
4. **P010 (high confidence).** Assign each capability to the correct side of the connection: Servers expose Resources, Prompts, and Tools to clients; Clients expose Sampling, Roots, and Elicitation to servers.
5. **P013 (high confidence).** Require explicit, informed user consent before exposing or accessing user data: the host must obtain consent before exposing user data to a server, must not transmit resource data elsewhere without consent, and must protect user data with appropriate access controls while keeping the user in control of what is shared.
6. **P016 (high confidence).** Respect the _meta reserved namespace: make no assumptions about values at MCP-reserved keys, form prefixes as dot-separated slash-terminated labels (preferring reverse-DNS), keep prefixes with a second label of modelcontextprotocol or mcp reserved for MCP, and bound non-empty key names with alphanumeric characters.
7. **P026 (high confidence).** Because MCP cannot enforce its security principles at the protocol level, the implementor must own robust consent and authorization flows, access controls and data protection, clear security documentation, privacy-by-design, and clear UIs for reviewing and authorizing activity.
8. **P052 (high confidence).** Treat tools as arbitrary code execution: obtain explicit per-tool user consent before invoking any tool and ensure the user understands what the tool does before authorizing it.
9. **P055 (high confidence).** Require every MCP implementation to support the base protocol and lifecycle-management layers; treat the other layers (authorization, server features, client features, utilities) as optional capabilities selected to fit the application.
10. **P060 (high confidence).** Enforce MCP request-id rules: every request carries a string or integer id, the id is never null (unlike base JSON-RPC), and an id is never reused by the same requestor within a session.
11. **P062 (high confidence).** Shape MCP result responses correctly: echo the request's id and always include a result field (whose contents may be any JSON object).
12. **P063 (high confidence).** Shape MCP error responses correctly: echo the request id (except when a malformed request makes the id unreadable), include an error field with a code and message, and use integer error codes.
13. **P064 (high confidence).** Validate schemas against their declared or default dialect, require schemas to be valid for that dialect, and fail gracefully with an explicit unsupported-dialect error rather than silently proceeding.
14. **P066 (high confidence).** Treat icon metadata and bytes as untrusted: restrict icon URIs to HTTPS or data: schemes, reject unsafe schemes (javascript:, file:, ftp:, ws:) and cross-origin redirects, and fetch icons without credentials.
15. **P111 (high confidence).** Adopt MCP as the standardized protocol layer for connecting LLM applications to external data and tools, instead of building bespoke per-integration connectors.
16. **P112 (high confidence).** Treat the normative TypeScript schema (schema.ts) as the source of truth, and honour BCP-14/RFC-2119 keywords as binding requirements only where they appear in all capitals.
17. **P113 (high confidence).** Treat the TypeScript schema as the single source of truth for MCP messages and structures, and treat the JSON Schema as a generated artifact derived from it.
18. **P114 (high confidence).** Model the three MCP participant roles distinctly — Hosts initiate connections, Clients are the connectors embedded in the host, and Servers provide context and capabilities.
19. **P122 (high confidence).** Handle MCP notifications as one-way messages: a notification carries no id and its receiver sends no response.
20. **P123 (high confidence).** For clients that render icons, support at least image/png and image/jpeg, and additionally support image/svg+xml and image/webp where feasible.
21. **P195 (high confidence).** Require each Icon object to provide a src URI that is an HTTP/HTTPS URL or a data URI.
22. **P196 (high confidence).** Validate icon content by type: detect the real content type via magic bytes, reject on mismatch or unknown type, and enforce a strict allowlist of image types rather than trusting the advertised MIME type.
23. **P103 (medium confidence).** Scope authorization to transport: HTTP-based transports should conform to the MCP authorization spec, STDIO transports should skip it and instead take credentials from the environment, and peers may still negotiate custom auth strategies.
24. **P183 (medium confidence).** Defend icon consumption against resource exhaustion and executable content: guard oversized images/dimensions/frames (optionally capping size), and exercise caution with formats that can embed scripts (e.g. SVG), sanitizing or disallowing risky file types.
25. **P239 (medium confidence).** Provide the cross-cutting MCP utilities — configuration, progress tracking, cancellation, error reporting, and logging — as part of a complete, operable implementation.

## Anti-patterns to flag

- Using a feature the peer never advertised, or skipping the initialization handshake and capability negotiation.
- Judging behaviour against the newest specification when an older revision was negotiated, or rejecting deprecated-but-present behaviour before its removal window.
- Inventing protocol behaviour the specification does not define, or presenting a proprietary extension as standard.
- Omitting the failure a rule prevents, the applicable revision, or the trade-off and residual risk.

## Grounding

Principles: P001, P004, P007, P010, P013, P016, P026, P052, P055, P060, P062, P063, P064, P066,
P103, P111, P112, P113, P114, P122, P123, P183, P195, P196, P239. Every cited claim, evidence
record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`,
`evidence/evidence-records.yaml`, `sources/anchors/`). The Model Context Protocol specification is
distillation-only here: paraphrased, never quoted.

