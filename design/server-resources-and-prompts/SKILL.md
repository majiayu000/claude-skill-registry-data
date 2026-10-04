---
name: server-resources-and-prompts
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P021
  - P030
  - P086
  - P094
  - P097
  - P129
  - P155
  - P156
  - P162
  - P163
  - P168
  - P169
  - P170
  - P171
  - P172
  - P173
  - P174
  - P175
  - P176
  - P191
  - P225
  - P226
  - P227
  - P228
  - P230
  - P231
  - P249
  - P250
  claims:
  - C00447
  - C00448
  - C00481
  - C00482
  - C00468
  - C00469
  - C00494
  - C00495
  - C00467
  - C00490
  - C00470
  - C00477
  - C00486
  - C00487
  - C00459
  - C00460
  - C00492
  - C00493
  - C00456
  - C00457
  - C00465
  - C00466
  - C00442
  - C00443
  - C00446
  - C00451
  - C00449
  - C00450
  - C00453
  - C00454
  - C00480
  - C00496
  - C00461
  - C00464
  - C00474
  - C00475
  - C00471
  - C00476
  - C00488
  - C00489
  - C00463
  - C00441
  - C00445
  - C00452
  - C00458
  - C00473
  - C00479
  - C00444
  - C00455
  evidence:
  - E00438
  - E00439
  - E00472
  - E00473
  - E00459
  - E00460
  - E00485
  - E00486
  - E00458
  - E00481
  - E00461
  - E00468
  - E00477
  - E00478
  - E00450
  - E00451
  - E00483
  - E00484
  - E00447
  - E00448
  - E00456
  - E00457
  - E00433
  - E00434
  - E00437
  - E00442
  - E00440
  - E00441
  - E00444
  - E00445
  - E00471
  - E00487
  - E00452
  - E00455
  - E00465
  - E00466
  - E00462
  - E00467
  - E00479
  - E00480
  - E00454
  - E00432
  - E00436
  - E00443
  - E00449
  - E00464
  - E00470
  - E00435
  - E00446
  source_anchors:
  - a17e89016c56-c0000
  - 37de412ba819-c0000
  authored_from_digest: 57567876ac05bde0d55d950b1ca5d16fdeee96268206fd6227c02c988b6e7456
---

# Server Resources And Prompts

Expose resources and prompts by unique URI, declared capability, and control owner. This skill
packages 29 grounded principles the mcp-protocol-advisor applies when this layer of the Model
Context Protocol is in scope. Each finding names the rule, the protocol revision it belongs to, the
failure or interoperability break it prevents, the conforming behaviour, and the trade-off or
residual risk.

## When this applies

- Listing available prompts, especially large prompt sets.
- Discovering available resources.
- Implementing or reviewing an MCP list operation.
- The operation can return an unbounded or large result set.
- The server integrates external/internet services or large local data sets.
- A client must rank, filter, or display candidate resources.
- A server exposes resources.
- A client integrates with a resource server.
- A server accepts resource URIs or performs resource operations.
- Defining or identifying a resource.
- Choosing a URI scheme.
- The server advertises the subscribe feature.
- A client tracks live changes to specific resources.
- Choosing a scheme for a web-hosted or server-mediated resource.
- A prompts/get or prompts/list request fails.
- A resource request fails.
- A prompt message carries image or audio content.
- Designing how a host surfaces or injects resource context.
- Exposing prompts from a server to a client UI.
- The prompt list can change at runtime and the server declared listChanged.
- A client needs the rendered content of a specific prompt.
- Constructing the messages a prompt returns.
- Returning resource contents.
- Handling a prompts/get request with arguments.
- Accepting prompt arguments or emitting prompt content, especially with embedded resources.
- A family of resources is parameterized rather than enumerable.
- The server declared the listChanged capability and its resource list changes.
- Modeling filesystem-like or virtual-file resources.
- Either party is deciding whether prompt operations are available.
- Designing a server that offers reusable prompt templates to clients.
- The server implements the prompts feature.
- Authoring a prompt definition.
- A prompt message embeds a server-side resource.
- Fetching the contents of a known resource.
- Serializing a resource or resource-template definition.
- Designing how a client presents server-provided prompts.
- Metadata about audience, priority, or freshness is useful to the client.

## Procedure

Identify the negotiated protocol revision first, then apply the principles below that are in scope,
highest-risk first. For each one: name the rule and its revision, state the failure or
interoperability break it prevents, give the conforming behaviour, and state the trade-off or
residual risk. Never invent behaviour the spec does not define, and never weaken a consent or
security requirement below what the spec supports.

1. **P002 (high confidence).** Design MCP list operations that can return large result sets (resources/list, resources/templates/list, prompts/list, tools/list) to support cursor-based pagination, yielding results in smaller pages rather than all at once.
2. **P021 (high confidence).** Use the optional annotations — `audience` (user/assistant), `priority` (0.0–1.0, 1=effectively required), and `lastModified` (ISO 8601) — to filter by intended audience, prioritize what enters context, and sort/display by recency.
3. **P030 (high confidence).** Only advertise the `resources` capability when the server actually exposes resources, and within it only advertise `subscribe`/`listChanged` for features that are genuinely implemented; clients must negotiate and never assume either optional feature is present.
4. **P086 (high confidence).** Enforce resource security on the server: validate all resource URIs, apply access controls to sensitive resources, and check permissions before performing any resource operation.
5. **P094 (high confidence).** Address every resource by a unique URI: standard schemes are non-exhaustive, so custom schemes are permitted but MUST conform to RFC3986; `git://` is the defined scheme for Git version-control integration.
6. **P097 (high confidence).** Offer `resources/subscribe` only when the `subscribe` feature is advertised; on a `notifications/resources/updated` for a subscribed resource the client must re-read it via `resources/read` to get the new contents.
7. **P129 (high confidence).** Restrict the `https://` scheme to resources the client can fetch directly from the web on its own; for anything the client must read through the MCP server, prefer another or a custom scheme even when the server itself downloads the bytes.
8. **P155 (high confidence).** Return standard JSON-RPC error codes for prompt failures: -32602 for an invalid prompt name or missing required arguments, and -32603 for internal errors.
9. **P156 (high confidence).** Return standard JSON-RPC errors for resource failures — code -32002 for resource-not-found (including the offending `uri` in `data`) and -32603 for internal errors.
10. **P162 (high confidence).** Base64-encode image and audio prompt-message content and include a valid MIME type for it.
11. **P163 (high confidence).** Treat resource selection as application-driven — the host decides how resources become model context — and do not hard-code a single user-interaction model; the protocol mandates none.
12. **P168 (high confidence).** Keep prompts user-controlled: expose them for explicit user selection (e.g. slash commands or other user-initiated UI) rather than invoking them automatically.
13. **P169 (high confidence).** Advertise the `prompts.listChanged` flag to signal support for change notifications, and when it is declared, send `notifications/prompts/list_changed` whenever the available prompt set changes.
14. **P170 (high confidence).** Retrieve a concrete prompt with `prompts/get`, passing the prompt name and its arguments; support argument auto-completion through the completion API where useful.
15. **P171 (high confidence).** Model prompt messages as a `role` ("user" or "assistant") plus a `content` value of one of the supported content types.
16. **P172 (high confidence).** Emit each resource-content entry as exactly one of text (`text`) or binary (base64 `blob`), and ensure binary data is properly encoded.
17. **P173 (high confidence).** Carefully validate all prompt inputs and outputs to prevent injection attacks and unauthorized access to resources.
18. **P174 (high confidence).** Expose parameterized resources as RFC6570 URI-template resource templates discoverable via `resources/templates/list`, and wire their arguments to the completion API for auto-completion.
19. **P175 (high confidence).** Declaring the `listChanged` capability obligates the server to emit `notifications/resources/list_changed` whenever the available-resource set changes.
20. **P176 (high confidence).** Treat `file://` as filesystem-like without requiring a real physical filesystem, and optionally tag non-regular files (e.g. directories) with an XDG MIME type such as `inode/directory` when no standard MIME type applies.
21. **P191 (high confidence).** Respect capability negotiation for prompts on both the client and server sides.
22. **P225 (high confidence).** Expose reusable prompt templates through MCP's standardized prompts feature rather than ad-hoc mechanisms, so clients can discover, retrieve, and parameterize them uniformly.
23. **P226 (high confidence).** A server that supports prompts MUST declare the `prompts` capability during initialization before serving prompt requests.
24. **P227 (high confidence).** Define each prompt with a unique `name` identifier and use the optional `title`, `description`, `icons`, and `arguments` fields to make it discoverable and customizable.
25. **P228 (high confidence).** For an embedded resource in a prompt message, include a valid resource URI, the appropriate MIME type, and either text content or base64-encoded blob data.
26. **P230 (high confidence).** Retrieve resource contents through `resources/read` keyed by the resource `uri`.
27. **P231 (high confidence).** Always populate a resource's required `uri` and `name`; `title`, `description`, `icons`, `mimeType`, and `size` are optional and should be provided only when meaningful.
28. **P249 (medium confidence).** Do not hard-code or mandate a specific prompt user-interaction model; leave the client free to surface prompts through whatever interface pattern fits its product.
29. **P250 (medium confidence).** Treat content annotations (audience, priority, modification times) as optional metadata available on any prompt-message content type.

## Anti-patterns to flag

- Using a feature the peer never advertised, or skipping the initialization handshake and capability negotiation.
- Judging behaviour against the newest specification when an older revision was negotiated, or rejecting deprecated-but-present behaviour before its removal window.
- Inventing protocol behaviour the specification does not define, or presenting a proprietary extension as standard.
- Omitting the failure a rule prevents, the applicable revision, or the trade-off and residual risk.

## Grounding

Principles: P002, P021, P030, P086, P094, P097, P129, P155, P156, P162, P163, P168, P169, P170,
P171, P172, P173, P174, P175, P176, P191, P225, P226, P227, P228, P230, P231, P249, P250. Every
cited claim, evidence record, and source anchor resolves in this package's distilled spine
(`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). The Model Context
Protocol specification is distillation-only here: paraphrased, never quoted.

