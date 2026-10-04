---
name: elicitation
kind: skill
status: ready
provenance:
  principles:
  - P019
  - P020
  - P039
  - P040
  - P041
  - P042
  - P054
  - P061
  - P083
  - P084
  - P085
  - P088
  - P149
  - P150
  - P151
  - P152
  - P203
  - P216
  - P217
  - P218
  - P220
  claims:
  - C00345
  - C00346
  - C00357
  - C00358
  - C00310
  - C00311
  - C00318
  - C00319
  - C00324
  - C00325
  - C00332
  - C00333
  - C00313
  - C00314
  - C00341
  - C00342
  - C00338
  - C00339
  - C00328
  - C00329
  - C00354
  - C00355
  - C00364
  - C00365
  - C00316
  - C00317
  - C00322
  - C00323
  - C00336
  - C00337
  - C00352
  - C00353
  - C00350
  - C00331
  - C00351
  - C00362
  - C00363
  evidence:
  - E00339
  - E00340
  - E00351
  - E00352
  - E00304
  - E00305
  - E00312
  - E00313
  - E00318
  - E00319
  - E00326
  - E00327
  - E00307
  - E00308
  - E00335
  - E00336
  - E00332
  - E00333
  - E00322
  - E00323
  - E00348
  - E00349
  - E00358
  - E00359
  - E00310
  - E00311
  - E00316
  - E00317
  - E00330
  - E00331
  - E00346
  - E00347
  - E00344
  - E00325
  - E00345
  - E00356
  - E00357
  source_anchors:
  - 01bfb448d361-c0000
  authored_from_digest: 6ed93a25fd922a5285343ac8a56329ac025488e04a6661834acbb1d4ddd265ca
---

# Elicitation

Keep elicitation user-controlled and route secrets through safe URL mode. This skill packages 21
grounded principles the mcp-protocol-advisor applies when this layer of the Model Context Protocol
is in scope. Each finding names the rule, the protocol revision it belongs to, the failure or
interoperability break it prevents, the conforming behaviour, and the trade-off or residual risk.

## When this applies

- The server needs third-party credentials to call an external service on the user's behalf.
- A client receives and must present a URL mode elicitation URL.
- A server needs the user to supply a secret, credential, or payment detail.
- Establishing or using an elicitation session.
- Authoring or validating a form mode requestedSchema.
- A URL-mode out-of-band interaction may complete asynchronously.
- Any elicitation request is presented to the user.
- The server must remember collected information or access status across requests.
- Producing or interpreting an elicitation response.
- Constructing a URL mode elicitation request.
- A server constructs a URL for URL mode elicitation.
- A URL mode flow performs third-party authorization or accepts user-provided information out of band.
- Presenting a form for submission or a URL for navigation.
- Constructing or parsing an elicitation/create request.
- A request cannot be processed until a URL mode elicitation is completed.
- A client surfaces elicitation requests to users.
- An elicitation cannot proceed or a request uses an undeclared mode.
- Deciding whether to use URL mode elicitation.
- Issuing or processing any elicitation request.
- Determining the identity of the user behind an elicitation.
- Exchanging form mode data with a schema.

## Procedure

Identify the negotiated protocol revision first, then apply the principles below that are in scope,
highest-risk first. For each one: name the rule and its revision, state the failure or
interoperability break it prevents, give the conforming behaviour, and state the trade-off or
residual risk. Never invent behaviour the spec does not define, and never weaken a consent or
security requirement below what the spec supports.

1. **P019 (high confidence).** For third-party authorization via URL mode, keep credentials on the server side only: never self-authorize the MCP server through URL mode, never let third-party credentials transit or be transmitted to the client, never reuse the client's credentials for the third party (forbidden token passthrough), and have the…
2. **P020 (high confidence).** Apply safe URL handling on the client: never auto pre-fetch the URL or its metadata, never open it without explicit consent, show the full URL first, open it in an isolated viewer the client/LLM cannot inspect, highlight the domain and warn on suspicious URIs (e.g. Punycode), and never render URLs clickable except…
3. **P039 (high confidence).** Never request secrets or credentials (passwords, API keys, access tokens, payment details) through form mode; route any sensitive-information exchange through URL mode so the data never enters the client, keeping it out of the LLM context and intermediaries.
4. **P040 (high confidence).** Negotiate elicitation support correctly: a client must declare the elicitation capability at initialization and support at least one mode (an empty object means form only), and a server must never send a request in a mode the client did not declare.
5. **P041 (high confidence).** Constrain form schemas to a flat object of primitive properties (string, number/integer, boolean, enum) using only the supported string formats (email, uri, date, date-time); pre-populate declared defaults when supported.
6. **P042 (high confidence).** Handle URL-mode completion notifications correctly: a server may send notifications/elicitation/complete only to the initiating client and must include the original elicitationId; clients must ignore unknown or already-completed IDs and still offer manual retry/cancel in case no notification arrives.
7. **P054 (high confidence).** Keep the user in control of every elicitation: clearly identify which server is asking, respect privacy, and always present clear decline and cancel options.
8. **P061 (high confidence).** Persist elicitation state securely bound to a verified individual user, never to a session ID alone, protect the store from unauthorized access, and for remote servers derive user identity from MCP authorization credentials (e.g. the sub claim) whenever possible.
9. **P083 (high confidence).** Implement the three-action response model (accept, decline, cancel): on form-mode accept return content matching the schema, on URL-mode accept omit content and treat it as consent to begin, not proof the interaction completed.
10. **P084 (high confidence).** Build URL mode requests completely: specify mode url, include a message, a valid url, and a unique elicitationId.
11. **P085 (high confidence).** Apply safe URL handling on the server: never place end-user PII or credentials in the URL, never issue a URL pre-authenticated to a protected resource (it enables impersonation), avoid clickable URLs inside form-field values, and use HTTPS outside development.
12. **P088 (high confidence).** Defend URL mode against cross-user phishing: verify that whoever opens the URL is the same user the elicitation was generated for before accepting any information, ensure the originator completes the flow, and make the identity check resilient to URL tampering (e.g. a server connect-URL comparing the session subject…
13. **P149 (high confidence).** Let users vet their input before it leaves: in form mode allow review and modification of responses before sending, and in URL mode display the target domain/host and obtain explicit consent before navigating.
14. **P150 (high confidence).** Form every elicitation/create request with a mode (optional for form, defaulting to form when omitted) and a human-readable message that explains why the interaction is needed; treat a missing mode as form.
15. **P151 (high confidence).** Use URLElicitationRequiredError (-32042) only when a request genuinely cannot proceed until a URL-mode elicitation completes, and populate it with the list of required elicitations, each URL mode and carrying an elicitationId.
16. **P152 (high confidence).** Give users strong runtime control: implement user-approval controls, allow declining an elicitation at any time, apply rate limiting, and present each request so it is clear what is being asked and why.
17. **P203 (high confidence).** Return the correct JSON-RPC errors: a server must return -32042 (URLElicitationRequiredError) when a request cannot proceed until an elicitation completes, and a client must return -32602 (Invalid params) when a server uses a mode the client did not declare.
18. **P216 (high confidence).** Understand URL mode's boundary: it exists for acquiring sensitive data or third-party authorization on the user's behalf, not for authorizing the client's access to the server, and the client's bearer token stays unchanged.
19. **P217 (high confidence).** Bind every elicitation request to both the client and the specific user identity.
20. **P218 (high confidence).** Never treat client-provided user identification as authoritative without server-side verification; identify users through authorization, since client-supplied identity can be forged.
21. **P220 (high confidence).** Validate elicitation data against the schema on both sides: clients should validate responses before sending and servers should validate received data against the requested schema.

## Anti-patterns to flag

- Using a feature the peer never advertised, or skipping the initialization handshake and capability negotiation.
- Judging behaviour against the newest specification when an older revision was negotiated, or rejecting deprecated-but-present behaviour before its removal window.
- Inventing protocol behaviour the specification does not define, or presenting a proprietary extension as standard.
- Omitting the failure a rule prevents, the applicable revision, or the trade-off and residual risk.

## Grounding

Principles: P019, P020, P039, P040, P041, P042, P054, P061, P083, P084, P085, P088, P149, P150,
P151, P152, P203, P216, P217, P218, P220. Every cited claim, evidence record, and source anchor
resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-
records.yaml`, `sources/anchors/`). The Model Context Protocol specification is distillation-only
here: paraphrased, never quoted.

