---
name: server-tools
kind: skill
status: ready
provenance:
  principles:
  - P014
  - P046
  - P047
  - P048
  - P053
  - P065
  - P080
  - P087
  - P096
  - P098
  - P165
  - P190
  claims:
  - C00533
  - C00534
  - C00513
  - C00514
  - C00529
  - C00530
  - C00525
  - C00526
  - C00500
  - C00501
  - C00509
  - C00510
  - C00505
  - C00506
  - C00520
  - C00521
  - C00503
  - C00504
  - C00517
  - C00518
  - C00498
  - C00499
  - C00523
  - C00524
  evidence:
  - E00524
  - E00525
  - E00504
  - E00505
  - E00520
  - E00521
  - E00516
  - E00517
  - E00491
  - E00492
  - E00500
  - E00501
  - E00496
  - E00497
  - E00511
  - E00512
  - E00494
  - E00495
  - E00508
  - E00509
  - E00489
  - E00490
  - E00514
  - E00515
  source_anchors:
  - 8ed43301d44f-c0000
  authored_from_digest: 3173af4d8766550559ed14d7d2d8e7ce8746ccc01413c4214876ec4173541fc9
---

# Server Tools

Define, discover, invoke, and harden tools with a valid schema and human consent. This skill
packages 12 grounded principles the mcp-protocol-advisor applies when this layer of the Model
Context Protocol is in scope. Each finding names the rule, the protocol revision it belongs to, the
failure or interoperability break it prevents, the conforming behaviour, and the trade-off or
residual risk.

## When this applies

- A client orchestrates tool calls on behalf of a model.
- Naming a tool exposed by an MCP server.
- Implementing a server that executes tools.
- Reporting or handling tool errors on server or client.
- Designing a client/application that lets a model invoke MCP tools.
- Authoring a tool definition.
- Implementing MCP tool discovery or invocation on client or server.
- A tool declares an outputSchema.
- Implementing an MCP server that exposes tools.
- A tool produces a result payload.
- Deciding how tools are surfaced and triggered in an MCP integration.
- A tool returns resource links or embedded resources.

## Procedure

Identify the negotiated protocol revision first, then apply the principles below that are in scope,
highest-risk first. For each one: name the rule and its revision, state the failure or
interoperability break it prevents, give the conforming behaviour, and state the trade-off or
residual risk. Never invent behaviour the spec does not define, and never weaken a consent or
security requirement below what the spec supports.

1. **P014 (high confidence).** Harden the client around tool calls: confirm sensitive operations, show tool inputs to the user before calling the server to prevent exfiltration, validate results before passing them to the LLM, apply timeouts to tool calls, and log tool usage for audit.
2. **P046 (high confidence).** Constrain tool names: keep them 1-128 characters, treat them as case-sensitive, restrict them to ASCII letters, digits, underscore, hyphen and dot (no spaces/commas/special characters), and keep them unique within a server.
3. **P047 (high confidence).** Harden the server against tool abuse: validate all tool inputs, enforce proper access controls, rate-limit tool invocations, and sanitize tool outputs.
4. **P048 (high confidence).** Separate protocol errors from tool execution errors: report execution failures (API, input-validation, business-logic) in the result with `isError: true` and reserve JSON-RPC protocol errors for unknown tools, malformed requests, and server errors; forward execution errors to the model so it can self-correct, and…
5. **P053 (high confidence).** Keep a human in the loop for tool invocations: give users the ability to deny a call, make clear which tools are exposed to the model, show a visual indicator when a tool is invoked, and present confirmation prompts for operations.
6. **P065 (high confidence).** Define every tool with a valid JSON Schema inputSchema: it must be a non-null JSON Schema object (defaulting to draft 2020-12 when no `$schema` is given), and for tools with no parameters use `{"type":"object","additionalProperties":false}`.
7. **P080 (high confidence).** Implement the tool discovery and invocation contract: support `tools/list` with optional cursor pagination for discovery and `tools/call` (tool name plus arguments) for invocation.
8. **P087 (high confidence).** Honor declared output schemas on both sides: when a tool declares an output schema the server must return structured results that conform to it and clients should validate results against it; also serialize structured content into a text content block for backwards compatibility.
9. **P096 (high confidence).** Advertise the tools capability and wire up listChanged correctly: a server exposing tools must declare the `tools` capability, and if it sets `listChanged` it must emit `notifications/tools/list_changed` whenever its tool list changes.
10. **P098 (high confidence).** Return well-formed tool results: place unstructured output in the `content` array (which may hold multiple typed items such as text, image, audio, resource links, or embedded resources) and structured output as a JSON object in `structuredContent`.
11. **P165 (high confidence).** Design tools as model-controlled while leaving the interface open: assume the model discovers and invokes tools from context, and do not assume or mandate any particular user-interaction pattern.
12. **P190 (medium confidence).** Handle resource references defensively: tools may return resource links (URIs the client can fetch or subscribe to) that are not guaranteed to appear in `resources/list`, and servers embedding resources in results should implement the `resources` capability.

## Anti-patterns to flag

- Using a feature the peer never advertised, or skipping the initialization handshake and capability negotiation.
- Judging behaviour against the newest specification when an older revision was negotiated, or rejecting deprecated-but-present behaviour before its removal window.
- Inventing protocol behaviour the specification does not define, or presenting a proprietary extension as standard.
- Omitting the failure a rule prevents, the applicable revision, or the trade-off and residual risk.

## Grounding

Principles: P014, P046, P047, P048, P053, P065, P080, P087, P096, P098, P165, P190. Every cited
claim, evidence record, and source anchor resolves in this package's distilled spine
(`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). The Model Context
Protocol specification is distillation-only here: paraphrased, never quoted.

