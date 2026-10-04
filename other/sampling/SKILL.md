---
name: sampling
kind: skill
status: ready
provenance:
  principles:
  - P003
  - P005
  - P044
  - P092
  - P093
  - P157
  - P158
  - P159
  - P160
  - P161
  - P189
  - P209
  - P219
  - P221
  - P222
  - P223
  - P224
  claims:
  - C00028
  - C00029
  - C00052
  - C00395
  - C00426
  - C00427
  - C00410
  - C00411
  - C00413
  - C00414
  - C00404
  - C00405
  - C00406
  - C00407
  - C00417
  - C00418
  - C00419
  - C00420
  - C00423
  - C00424
  - C00408
  - C00409
  - C00422
  - C00431
  - C00416
  - C00421
  - C00425
  - C00430
  evidence:
  - E00028
  - E00029
  - E00051
  - E00388
  - E00417
  - E00418
  - E00401
  - E00402
  - E00404
  - E00405
  - E00395
  - E00396
  - E00397
  - E00398
  - E00408
  - E00409
  - E00410
  - E00411
  - E00414
  - E00415
  - E00399
  - E00400
  - E00413
  - E00422
  - E00407
  - E00412
  - E00416
  - E00421
  source_anchors:
  - 37bf1590e3e5-c0000
  - 0b6ac42ddf2e-c0000
  - 3498fca5668f-c0000
  authored_from_digest: 78d58f3275e37b0eb2fae5a482f83aa7644f276fcb02368f23abec08d16333fd
---

# Sampling

Route server-originated LLM access through the client with explicit user approval. This skill
packages 17 grounded principles the mcp-protocol-advisor applies when this layer of the Model
Context Protocol is in scope. Each finding names the rule, the protocol revision it belongs to, the
failure or interoperability break it prevents, the conforming behaviour, and the trade-off or
residual risk.

## When this applies

- A server initiates a sampling / recursive LLM request through the client.
- A client is about to forward a sampling request to a model.
- A server needs an LLM completion.
- A server needs an LLM completion (text, image, or audio) inside an MCP feature.
- A server expresses model requirements for a sampling request.
- A server initiates a model generation.
- A sampling request enables tool use.
- A server wants the client's LLM to call tools during sampling.
- A client initializes an MCP session and intends to support sampling.
- A user message contains one or more tool_result blocks.
- An assistant message returns one or more tool_use blocks.
- A model may issue multiple tool calls in one turn.
- A server is constructing a createMessage request that could set includeContext.
- A server needs to control whether the model uses tools.
- Implementing or reviewing a sampling client or server.
- A server runs a multi-turn tool loop.
- A client cannot fulfill a sampling request.

## Procedure

Identify the negotiated protocol revision first, then apply the principles below that are in scope,
highest-risk first. For each one: name the rule and its revision, state the failure or
interoperability break it prevents, give the conforming behaviour, and state the trade-off or
residual risk. Never invent behaviour the spec does not define, and never weaken a consent or
security requirement below what the spec supports.

1. **P003 (high confidence).** Require explicit user approval of every LLM sampling request, let users control whether sampling occurs, the exact prompt sent, and what results the server may see, and limit server visibility into prompts by default.
2. **P005 (high confidence).** Route all server-originated LLM access through the client via sampling: let the client own model access, selection, and permissions so servers need no API keys of their own.
3. **P044 (high confidence).** Select models by preference, not by name: express costPriority, speedPriority, and intelligencePriority as normalized 0-1 values and provide advisory substring hints in order of preference; the client makes the final selection and may map hints to an equivalent provider's model.
4. **P092 (high confidence).** Request generations with a sampling/createMessage JSON-RPC request carrying messages, optional modelPreferences, an optional systemPrompt, and maxTokens; expect a result with role, content, model, and stopReason.
5. **P093 (high confidence).** Drive tool-enabled sampling as a multi-turn loop: send tools (name, description, inputSchema) and optional toolChoice, execute the tool_use returned under stopReason 'toolUse', append tool results, and repeat.
6. **P157 (high confidence).** Negotiate tool use through capabilities: a client must declare sampling.tools to receive tool-enabled sampling requests, and a server must not send tool-enabled requests to a client that has not declared it.
7. **P158 (high confidence).** A client that supports sampling must declare the sampling capability during initialization, nesting a tools object for tool-use support and a context object for context-inclusion support.
8. **P159 (high confidence).** A user message that carries tool results must contain only tool_result blocks and no text, image, or audio, so it stays compatible with provider APIs that use dedicated tool-result roles.
9. **P160 (high confidence).** Preserve tool-use/result balance: immediately follow any assistant message containing ToolUseContent with a user message made up entirely of ToolResultContent, matching each tool use's id to a tool result's toolUseId before any other message.
10. **P161 (high confidence).** Support parallel tool use by accepting an array of ToolUseContent; treat disabling parallel tool use as an optional provider-specific extension, not part of core MCP.
11. **P209 (high confidence).** Select tool behaviour with toolChoice: 'auto' (default) lets the model decide, 'required' forces at least one tool call before completing, and 'none' forbids tool use.
12. **P219 (high confidence).** Apply sampling security controls: clients implement user-approval controls, respect model-preference hints, and rate-limit; both parties validate message content, handle sensitive data appropriately, and enforce iteration limits when tools are used.
13. **P221 (high confidence).** Bound the tool loop: cap the maximum number of iterations and pass toolChoice {mode: 'none'} on the final iteration to force a final text result.
14. **P222 (high confidence).** Use only the 'user' and 'assistant' roles: return tool-use requests with the assistant role and send tool results back with the user role.
15. **P223 (high confidence).** Support multimodal sampling content: text, image (base64 data plus mimeType), and audio (base64 data plus mimeType).
16. **P224 (high confidence).** Return standard errors on sampling failures: user rejection as code -1, and a missing tool result or tool results mixed with other content as -32602 Invalid params.
17. **P189 (medium confidence).** Avoid the soft-deprecated includeContext values 'thisServer' and 'allServers' (omit includeContext so it defaults to 'none'); do not use them unless the client has declared sampling.context, since they may be removed in a future release.

## Anti-patterns to flag

- Using a feature the peer never advertised, or skipping the initialization handshake and capability negotiation.
- Judging behaviour against the newest specification when an older revision was negotiated, or rejecting deprecated-but-present behaviour before its removal window.
- Inventing protocol behaviour the specification does not define, or presenting a proprietary extension as standard.
- Omitting the failure a rule prevents, the applicable revision, or the trade-off and residual risk.

## Grounding

Principles: P003, P005, P044, P092, P093, P157, P158, P159, P160, P161, P189, P209, P219, P221,
P222, P223, P224. Every cited claim, evidence record, and source anchor resolves in this package's
distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). The
Model Context Protocol specification is distillation-only here: paraphrased, never quoted.

