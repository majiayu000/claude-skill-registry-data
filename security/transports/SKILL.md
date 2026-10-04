---
name: transports
kind: skill
status: ready
provenance:
  principles:
  - P032
  - P068
  - P071
  - P104
  - P127
  - P128
  - P130
  - P131
  - P184
  - P185
  - P192
  - P193
  - P198
  - P199
  - P200
  - P201
  - P202
  - P204
  - P205
  - P240
  - P241
  - P242
  - P243
  - P244
  - P245
  claims:
  - C00177
  - C00178
  - C00153
  - C00154
  - C00163
  - C00164
  - C00168
  - C00169
  - C00152
  - C00189
  - C00185
  - C00186
  - C00159
  - C00160
  - C00173
  - C00174
  - C00187
  - C00188
  - C00161
  - C00162
  - C00181
  - C00182
  - C00150
  - C00157
  - C00176
  - C00166
  - C00167
  - C00175
  - C00183
  - C00151
  - C00156
  - C00158
  - C00171
  - C00172
  - C00184
  evidence:
  - E00175
  - E00176
  - E00151
  - E00152
  - E00161
  - E00162
  - E00166
  - E00167
  - E00150
  - E00187
  - E00183
  - E00184
  - E00157
  - E00158
  - E00171
  - E00172
  - E00185
  - E00186
  - E00159
  - E00160
  - E00179
  - E00180
  - E00148
  - E00155
  - E00174
  - E00164
  - E00165
  - E00173
  - E00181
  - E00149
  - E00154
  - E00156
  - E00169
  - E00170
  - E00182
  source_anchors:
  - 5a86d66ae0ab-c0000
  authored_from_digest: e4276b696309bd15392cea5fa79a6cbf208d2e46f4cbe972bca713c093ceeb79
---

# Transports

Implement the stdio and Streamable HTTP transports to the negotiated revision. This skill packages
25 grounded principles the mcp-protocol-advisor applies when this layer of the Model Context
Protocol is in scope. Each finding names the rule, the protocol revision it belongs to, the failure
or interoperability break it prevents, the conforming behaviour, and the trade-off or residual risk.

## When this applies

- Implementing resumable SSE streams and message redelivery.
- Implementing the stdio transport.
- A Streamable HTTP client sends a JSON-RPC message.
- The server has opened an SSE stream for a client request.
- Implementing a non-standard or custom MCP transport.
- A client makes HTTP requests after initialization.
- Handling incoming Streamable HTTP connections.
- A client opens a server-to-client SSE stream via GET.
- Supporting peers built for the deprecated HTTP+SSE transport.
- Deploying or hardening a Streamable HTTP server.
- A server establishes stateful sessions.
- The server has assigned a session ID.
- Implementing or reviewing any MCP transport.
- Implementing a Streamable HTTP MCP server.
- The server maintains multiple concurrent SSE streams with a client.
- The POST body is a JSON-RPC response or notification.
- The POST body is a JSON-RPC request.
- The server sends messages on a GET-initiated SSE stream.
- The server terminates a session.
- Choosing which transports an MCP client or server supports.
- Handling a stdio server's stderr output.
- The server must stream multiple messages or push messages to the client.
- The server is streaming over SSE prior to the final response.
- An SSE connection drops mid-request.
- A client no longer needs its session.

## Procedure

Identify the negotiated protocol revision first, then apply the principles below that are in scope,
highest-risk first. For each one: name the rule and its revision, state the failure or
interoperability break it prevents, give the conforming behaviour, and state the trade-off or
residual risk. Never invent behaviour the spec does not define, and never weaken a consent or
security requirement below what the spec supports.

1. **P032 (high confidence).** Implement SSE resumability with per-stream cursors: attach globally unique event IDs (within the session or per client) that encode the originating stream, let clients resume via an HTTP GET carrying Last-Event-ID, and never replay messages that belonged to a different stream.
2. **P068 (high confidence).** For stdio, run the server as a client-launched subprocess, delimit messages by newlines with no embedded newlines, and never write anything to stdout or the server's stdin that is not a valid MCP message.
3. **P071 (high confidence).** A Streamable HTTP client MUST send each JSON-RPC message as its own HTTP POST to the MCP endpoint, with an Accept header listing both application/json and text/event-stream, and a body of exactly one JSON-RPC message.
4. **P127 (high confidence).** Custom transports are permitted but MUST preserve MCP's JSON-RPC message format and lifecycle requirements and SHOULD document their connection and message-exchange patterns for interoperability.
5. **P128 (high confidence).** Over HTTP the client MUST send the MCP-Protocol-Version header on all post-initialization requests (SHOULD be the negotiated version); the server SHOULD assume 2025-03-26 when the header is absent and unresolvable, and MUST return HTTP 400 for an invalid or unsupported version.
6. **P130 (high confidence).** Streamable HTTP servers MUST validate the Origin header on all incoming connections and MUST respond with HTTP 403 Forbidden when it is present and invalid, to prevent DNS rebinding attacks.
7. **P131 (high confidence).** Support an optional client-initiated GET (with an Accept header listing text/event-stream) that opens a server-to-client SSE stream without a prior POST; the server MUST answer such a GET with either text/event-stream or HTTP 405 Method Not Allowed.
8. **P192 (high confidence).** When establishing stateful sessions, assign the session ID via the MCP-Session-Id header on the InitializeResult; the ID SHOULD be globally unique and cryptographically secure and MUST contain only visible ASCII characters (0x21-0x7E).
9. **P193 (high confidence).** Once a session ID is assigned, the client MUST echo it in the MCP-Session-Id header on all subsequent requests, and a server requiring sessions SHOULD reject non-initialization requests that lack the header with HTTP 400 Bad Request.
10. **P198 (high confidence).** Encode every MCP message as UTF-8 JSON-RPC across all transports.
11. **P199 (high confidence).** A Streamable HTTP server MUST expose a single MCP endpoint path that supports both HTTP POST and GET.
12. **P200 (high confidence).** The server MUST deliver each JSON-RPC message on only one connected stream and MUST NOT broadcast the same message across multiple streams.
13. **P201 (high confidence).** When a posted body is a JSON-RPC response or notification, the server MUST return HTTP 202 Accepted with no body if accepted, or an HTTP error status (e.g. 400) if it cannot accept it.
14. **P202 (high confidence).** When a posted body is a JSON-RPC request, the server MUST answer with either text/event-stream (an SSE stream) or application/json (one object), and the client MUST support both.
15. **P204 (high confidence).** On a GET-initiated SSE stream the server MUST NOT send a JSON-RPC response except when resuming a stream tied to a previous client request.
16. **P205 (high confidence).** Honour session-termination semantics: after the server terminates a session it MUST return HTTP 404 Not Found for requests bearing that session ID, and a client receiving that 404 MUST start a fresh session with a new InitializeRequest and no session ID.
17. **P104 (medium confidence).** Manage the SSE response stream deliberately: prime reconnection with an initial empty-data event ID, optionally close the connection without terminating the stream while sending an SSE retry field (which the client MUST honour by waiting before reconnecting), and terminate the stream after delivering the JSON-RPC…
18. **P184 (medium confidence).** For backwards compatibility with the deprecated HTTP+SSE transport, servers should host both the old SSE and POST endpoints alongside the new MCP endpoint, and clients should probe with an InitializeRequest POST and fall back on HTTP 400/404/405 to a GET expecting an endpoint event.
19. **P185 (medium confidence).** Harden local Streamable HTTP servers by binding only to localhost (127.0.0.1) rather than all interfaces, and implement proper authentication for all connections.
20. **P240 (medium confidence).** Offer the two standard MCP transports and support stdio whenever possible; treat stdio as the default client choice.
21. **P241 (medium confidence).** Treat a stdio server's stderr as an optional log channel: the server MAY log UTF-8 to stderr and the client MUST NOT assume stderr output signals an error.
22. **P242 (medium confidence).** Use Server-Sent Events (SSE) when the server needs to stream multiple messages or push server-to-client messages over Streamable HTTP.
23. **P243 (medium confidence).** Before the final JSON-RPC response, the server MAY interleave JSON-RPC requests and notifications on the SSE stream, and those messages SHOULD relate to the originating client request.
24. **P244 (medium confidence).** Do not treat an SSE disconnection as request cancellation; require clients to cancel explicitly with an MCP CancelledNotification.
25. **P245 (medium confidence).** Let clients end sessions gracefully with an HTTP DELETE carrying the MCP-Session-Id header; servers MAY refuse client-initiated termination with HTTP 405 Method Not Allowed.

## Anti-patterns to flag

- Using a feature the peer never advertised, or skipping the initialization handshake and capability negotiation.
- Judging behaviour against the newest specification when an older revision was negotiated, or rejecting deprecated-but-present behaviour before its removal window.
- Inventing protocol behaviour the specification does not define, or presenting a proprietary extension as standard.
- Omitting the failure a rule prevents, the applicable revision, or the trade-off and residual risk.

## Grounding

Principles: P032, P068, P071, P104, P127, P128, P130, P131, P184, P185, P192, P193, P198, P199,
P200, P201, P202, P204, P205, P240, P241, P242, P243, P244, P245. Every cited claim, evidence
record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`,
`evidence/evidence-records.yaml`, `sources/anchors/`). The Model Context Protocol specification is
distillation-only here: paraphrased, never quoted.

