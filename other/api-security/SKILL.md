---
name: api-security
version: "1.0.0"
description: API security for mid-2026 — OWASP API Top 10 2023, AI-API specific (rate limits, prompt-shape egress, MCP HTTP transport), GraphQL + gRPC + REST + WebSocket attack surfaces, API gateway posture, BOLA/BFLA/SSRF/Mass Assignment
triggers:
  - api security
  - owasp api top 10
  - bola
  - bfla
  - mass assignment
  - api gateway
  - rate limiting
  - graphql security
  - grpc security
  - rest security
  - websocket security
  - ai api security
  - mcp transport
  - openapi security
data_deps:
  - atlas-ttps.json
  - attack-techniques.json
  - cwe-catalog.json
  - d3fend-catalog.json
  - framework-control-gaps.json
  - rfc-references.json
atlas_refs:
  - AML.T0096
  - AML.T0013
attack_refs:
  - T1190
  - T1078
  - T1567
framework_gaps:
  - OWASP-ASVS-v5.0-V14
  - NIST-800-218-SSDF
  - ISO-27001-2022-A.8.28
  - NIST-800-53-AC-2
  - NIS2-Art21-incident-handling
  - UK-CAF-B2
  - AU-Essential-8-App-Hardening
rfc_refs:
  - RFC-8446
  - RFC-9114
  - RFC-7519
  - RFC-8725
  - RFC-6749
  - RFC-9700
  - RFC-9421
cwe_refs:
  - CWE-287
  - CWE-862
  - CWE-863
  - CWE-918
  - CWE-200
  - CWE-352
  - CWE-22
  - CWE-77
  - CWE-1188
d3fend_refs:
  - D3-IOPR
  - D3-NTA
  - D3-CSPP
  - D3-MFA
  - D3-CBAN
forward_watch:
  - NGINX Rift CVE-2026-42945 (disclosed 2026-05-13, source depthfirst) — KEV-watch predicted CISA KEV listing by 2026-05-29; track for active-exploitation confirmation and patch advisory affecting API gateway / reverse-proxy deployments
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — LiteLLM 3-bug SSRF + Code Injection chain by k3vg3n; LLM-proxy API surface; track upstream patch and CVE assignments
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — LiteLLM full SSRF + Code Injection by Out Of Bounds (Byung Young Yi); duplicate-class with the k3vg3n entry; track unified patch advisory
last_threat_review: "2026-09-18"
---

# API Security Assessment

## Threat Context (mid-2026)

APIs are now the integration substrate of every non-trivial system. The mid-2026 enterprise app is a thin shell of UI calling a fan-out of REST, GraphQL, gRPC, and WebSocket APIs — many of which themselves call **AI-API services** (OpenAI, Anthropic, Google Gemini, AWS Bedrock, Azure OpenAI) on the user's behalf. Legacy web-application firewalls were built for HTML form posts and inspect REST badly, GraphQL barely, gRPC binary framing not at all, and AI-API egress not at all. The defensive perimeter has moved from the WAF to the **API gateway and the egress policy**.

**OWASP API Top 10 2023** is a separate threat catalogue from the OWASP Web Top 10 and reorders the risk landscape around API-specific weakness classes that the web list under-represents: **API1 BOLA (Broken Object Level Authorization)**, **API2 Broken Authentication**, **API3 BOPLA (Broken Object Property Level Authorization, formerly Mass Assignment + Excessive Data Exposure)**, **API4 Unrestricted Resource Consumption**, **API5 BFLA (Broken Function Level Authorization)**, **API6 Unrestricted Access to Sensitive Business Flows**, **API7 SSRF**, **API8 Security Misconfiguration**, **API9 Improper Inventory Management**, **API10 Unsafe Consumption of APIs**. Of these, **BOLA remains #1 by exploit volume in 2025–2026 bug bounty data** — every public bounty programme above mid-size pays for at least one BOLA per quarter.

**AI-API consumption is a new egress surface.** Three distinct API attack classes against AI providers must not be conflated:

1. **AI-API rate-limit abuse / denial-of-wallet** — a stolen API key or compromised internal service burns the organisation's spend cap on a model endpoint. GPT-class and Claude-class token costs at production volume run to five-to-six figures per day per workload — a key exfiltrated on Friday and abused over a weekend is a real budget event.
2. **Prompt-injection-as-C2** — user-controlled content reaches an LLM-fronted internal API and exfiltrates data through the model's response channel (the model becomes the covert C2 channel). Hand-off to `ai-c2-detection` for SesameOp-class detection patterns.
3. **Model extraction via inference rate (AML.T0013, Discover AI Model Ontology)** — high-volume queries against a hosted model are used to reconstruct the model's behaviour, system prompt, guardrail surface, or training-data signal. Detected at egress only by per-identity rate-and-shape monitoring, not by request count alone.

**MCP transport runs over HTTP/SSE.** Anthropic's **Model Context Protocol** (MCP) — the de-facto agent-to-tool protocol adopted across the industry through 2025 — uses HTTP and Server-Sent Events as its transport. That means MCP traffic is API traffic and inherits every API attack surface: auth, rate limiting, schema validation, BOLA on tool calls, SSRF if a tool fetches URLs. Hand-off to `mcp-agent-trust` for MCP-specific semantics; the API-security posture is foundational.

**GraphQL, gRPC, and WebSocket are not REST.** Each has distinct attack profiles:

- **GraphQL** — a single endpoint multiplexes thousands of operations. **Query complexity attacks** (deep nesting, fragment expansion, aliasing) cause CPU/DB amplification — the API1/4 manifestation specific to GraphQL. **Introspection** in production leaks the entire schema. **Field-level authorisation** is the only correct authorisation layer; route-level auth is structurally insufficient because every operation hits the same route.
- **gRPC** — binary HTTP/2 framing with Protocol Buffers. WAF inspection is effectively blind. **Reflection** (`grpc.reflection.v1alpha.ServerReflection`) enabled in production exposes the full service surface. **mTLS** (per RFC 8446 with appropriate cipher choice) is the canonical auth — anything weaker is a downgrade.
- **WebSocket** — long-lived, bidirectional, **not bound by the same-origin policy**. CSRF analogues apply (cross-site WebSocket hijacking, "CSWSH"). Origin validation at the upgrade handshake is the only enforcement point; thereafter the connection is unframed by browser security primitives.

**Rate-limit policy is the new perimeter** — for DoS, for cost abuse, for credential-stuffing, for model-extraction. A flat per-IP rate limit is structurally inadequate; per-route + per-identity + per-resource + per-cost-unit is the mid-2026 baseline. **HTTP Message Signatures (RFC 9421)** standardised in 2024 are now the canonical wire-level integrity primitive for sensitive API operations where TLS alone is insufficient (multi-hop proxying, signature persistence in logs, replay protection).

**Ephemeral and serverless API runtimes** (AWS Lambda, Cloudflare Workers, Vercel Functions, Deno Deploy, Fly Machines) shift the control model: there is no long-lived session, no in-process rate-limiter, no shared cache. **Per-request controls become the canonical model** — every request carries its own token, its own context, its own auth decision; session-level controls collapse into stateless equivalents (signed tokens with short TTL per RFC 8725 BCP, gateway-enforced quotas, distributed rate-limit stores).

---

## Framework Lag Declaration

| Framework | Control | Why It Fails in mid-2026 |
|---|---|---|
| OWASP ASVS v5.0 | V14 (Configuration) | V14 hardens deployed configuration; it does not operationalise the **OWASP API Top 10 2023 weakness classes** (BOLA, BFLA, BOPLA) as a per-route verification surface. There is no V14 requirement to assert per-resource scoping on every object-ID-bearing endpoint. Tracked as OWASP-ASVS-v5.0-V14. |
| OWASP ASVS v5.0 | V13 (API & Web Service) | Covers REST broadly; under-specified for GraphQL field-level authorisation, gRPC reflection state, WebSocket origin enforcement at upgrade, and AI-API egress. |
| NIST SP 800-218 (SSDF) | PW.4 / PW.7 secure coding & review | Method-neutral on API testing. Does not name BOLA, BFLA, or BOPLA as testable surfaces; does not require contract-test / schema-fuzz coverage; does not address AI-API egress policy. Tracked as NIST-800-218-SSDF. |
| NIST SP 800-53 Rev. 5 | AC-2 (Account Management) | AC-2 covers human/service account lifecycle. It does **not** address **per-object authorisation** (BOLA) — the right principal can still access the wrong object. Tracked as NIST-800-53-AC-2. |
| ISO 27001:2022 | A.8.28 (Secure coding) | Method-agnostic — no API-specific verification surface. Tracked as ISO-27001-2022-A.8.28. |
| PCI DSS 4.0 | 6.2 / 11.4 / Req. 6.4.2 | Payment-API scope only. Outside cardholder data flows the requirements do not bind; AI-API egress is not in scope at all. |
| EU PSD2 RTS-SCA (Reg. 2018/389) | Strong customer authentication & dynamic linking | Banking-API auth surface only; mandates SCA on payer-initiated payments but is silent on BOLA per-resource scoping and on AI-API consumption inside the bank's own systems. |
| EU DORA (2022/2554) | Art. 28 ICT third-party risk; Art. 30 contractual provisions | Requires assessment of ICT third-party providers including API providers. Does not specify BOLA/BFLA testing depth; does not specifically address AI-API providers as a distinct risk class. |
| UK Open Banking Standard | FAPI 2.0 profile | Banking-API auth surface only (a PSD2 derivative). Does not bind non-banking APIs in the same organisation. |
| AU CDR (Consumer Data Right) | CDR Rules Sch. 2, InfoSec Schedule | Sector-specific (banking + energy as of 2025–2026 rollouts). Mandates API protections in scope; does not bind non-CDR APIs. |
| JP FISC v9 + FSA open-banking | Banking-API guidance | Sector-specific. Does not address GraphQL/gRPC distinct profiles or AI-API egress. |
| IL banking API directive (Bank of Israel) | Open-banking API guidance | Sector-specific. Does not bind non-banking APIs or AI-API egress. |
| SG MAS API Architectural Pattern + e-payments | API design + auth pattern | Sector-specific guidance; named pattern is reference only — no binding BOLA testing depth. |
| BR Open Finance (Bacen) | FAPI 2.0 derivative | Banking-API auth surface only. |
| IN UPI / Account Aggregator (NPCI / RBI) | Payments + AA security framework | Sector-specific payment-API + consent-API surface. AI-API egress out of scope. |
| NYDFS 23 NYCRR 500 | §500.5 penetration testing | APIs are in scope for the annual pen test where they expose covered data. "Annual" is structurally inadequate against agentic API-exploit timelines. |
| UK NCSC CAF | Principle B2 (Identity and Access Control), B4 (System Security), C1 (Security Monitoring) | Outcome-based assessment. CAF outcomes are silent on BOLA / BFLA / BOPLA as testable surfaces and silent on AI-API egress baselining. An organisation can achieve CAF outcomes at Achieved level with zero per-object authorisation testing and zero AI-API consumer monitoring. NCSC API Security Guidance (2024) recommends per-object scoping but is not a CAF outcome statement. |
| UK FCA / PRA SS1/21 (Operational Resilience) + CBEST | Important Business Service tolerance + threat-led pen testing | CBEST scenario libraries lag adversary capability 12-18 months and rarely include BOLA/BFLA-by-AI-agent or AI-API-as-C2 test cases. An FCA-attested operational-resilience programme can be "compliant" with zero exercised coverage of agentic API exploitation. |
| AU ASD Essential 8 | Strategy: Restrict Administrative Privileges + Application Control + MFA | None of the eight strategies address API-level authorisation (per-object scoping, per-field scoping) or AI-API egress monitoring. Essential 8 ML3 attestation does not bind any API security control surface. |
| AU ASD ISM | ISM-1817 (authentication and authorization of clients calling internet-facing network APIs) + ISM-1228 (event analysis) + ISM-1569 (shared responsibility model with suppliers) | ISM-1817 requires authorization as well as authentication, but at the level of the client and the API, not of each object a request names, so BOLA / BFLA exploitation passes it and produces authenticated, authorized log entries with attacker-supplied object IDs that ISM-1228 event analysis sees as normal. ISM-1569's shared responsibility model does not assign object-level authorization in a consumed AI API to either party. |
| AU APRA CPS 234 + CPS 230 | Para 27 (information security capability) + CPS 230 ICT-service-provider obligations | "Proportional capability" language. APRA-regulated entities meet CPS 234 attestation with traditional API gateway + WAF posture; per-object authorisation testing depth and AI-API consumer monitoring are not examined capability classes. CPS 230 third-party-arrangements obligations do not enumerate AI-API providers as in-scope material service providers. |

---

## TTP Mapping (MITRE ATT&CK Enterprise + ATLAS v2026.09)

| TTP ID | Technique | API Manifestation | CWE Root-Causes | Framework Coverage |
|---|---|---|---|---|
| T1190 | Exploit Public-Facing Application | Direct exploit of an exposed API endpoint — BOLA via mutated object ID, SSRF via "fetch URL" parameter, mass-assignment via injected JSON field | CWE-287, CWE-862, CWE-863, CWE-918, CWE-1188 | Partial — ASVS V13 covers REST; gaps for GraphQL/gRPC/WebSocket specifics and per-object scoping |
| T1078 | Valid Accounts | Stolen API token / OAuth refresh token / leaked service-account key reused against the API; key-exfil-then-abuse pattern dominant for AI-API rate-limit abuse | CWE-287, CWE-200 | Partial — NIST-800-53-AC-2 manages account lifecycle but not per-object authz, not key rotation cadence for AI-API keys |
| T1567 | Exfiltration Over Web Service | Sensitive data egressed via a legitimate API channel — AI-API response stream as covert C2; OAuth-token-scoped exfil over the org's own API | CWE-200, CWE-918 | Missing — no framework mandates per-identity egress baselining; D3-NTA is the operational control (see Defensive Countermeasure Mapping) |
| AML.T0096 | AI Service API (AI-API as covert C2) | LLM API used as a covert command-and-control / exfil channel — prompt content carries instructions; response carries staged data | CWE-77, CWE-200 | Missing in NIST/ISO; hand-off to `ai-c2-detection` |
| AML.T0013 | Discover AI Model Ontology (inference-API probing for system-prompt, guardrail, model-family signal) | High-volume queries against a hosted model used to reconstruct behaviour, guardrail surface, or training-data signal | CWE-200 | Missing — detected only by per-identity rate-and-shape monitoring at egress |

CWE root-causes referenced as a set (per `cwe_refs` in frontmatter, all resolved against `data/cwe-catalog.json`): CWE-287 (Improper Authentication), CWE-862 (Missing Authorization — BFLA root cause), CWE-863 (Incorrect Authorization — BOLA root cause), CWE-918 (SSRF — API7), CWE-200 (Information Exposure — BOPLA contributor), CWE-352 (CSRF — cookie-auth APIs + WebSocket CSWSH), CWE-22 (Path Traversal — API parameter sinks), CWE-77 (Command Injection — API parameter to shell), CWE-1188 (Insecure Default Initialization — default-open API state). ATT&CK Enterprise techniques (T1190, T1078, T1567) resolve against `data/attack-techniques.json`; the AML.T0096 (AI service API) and AML.T0013 (model-ontology discovery) entries resolve against `data/atlas-ttps.json`. Cross-reference every BOLA / BFLA finding against the `CWE-863` / `CWE-862` entries in `data/cwe-catalog.json` for the canonical weakness description used in operator briefings.

---

## Exploit Availability Matrix

| OWASP API Top 10 2023 Class | Offensive Tooling Maturity | Defensive Tooling Maturity | AI-Augmented Exploitation | Bug Bounty Market Signal (mid-2026, order-of-magnitude) | Live Exploitation Rate |
|---|---|---|---|---|---|
| API1 BOLA | Burp Suite (Autorize), Postman, Apidog, ZAP active scanner | SAST low (intent-dependent); IAST moderate; DAST low without spec | Yes — agentic frameworks enumerate object-ID + token combinations exhaustively | Critical BOLA on a regulated-data API: tens of thousands USD; chain-to-PII: USD 15K–50K bracket typical | Very high — dominant API bug bounty payout class through 2025–2026 |
| API2 Broken Authentication | Burp, Postman, custom OAuth-replay tooling | DAST moderate; auth-coverage measurable | Yes — credential-stuffing toolchains AI-paced | Critical auth bypass: tens of thousands USD bracket | High — credential-stuffing + token-leak chains common |
| API3 BOPLA (Mass Assignment + Excessive Data Exposure) | Burp, Schemathesis, contract-fuzz | SAST moderate (with typed handlers); contract testing high | Yes — JSON field injection via agentic mutation | Mid-tier; chains to privilege escalation push higher | High — AI-suggested handlers frequently bind whole-body to model |
| API4 Unrestricted Resource Consumption | k6, Vegeta, custom GraphQL-complexity fuzzers | API gateway rate-limit + quota enforcement (high if configured) | Yes — denial-of-wallet automation for AI-API consumption is a 2025–2026 emergence | DoS / cost-abuse: organisation-specific; AI-API key abuse can hit budget cap in hours | High — automated key-abuse is the dominant outcome of leaked AI-API keys |
| API5 BFLA | Burp Autorize, Apidog, Schemathesis | DAST moderate with spec; SAST low | Yes — agentic enumeration of role × function combinations | Critical privilege escalation: tens of thousands USD bracket | High — AI-suggested admin handlers often miss role check |
| API6 Unrestricted Sensitive Business Flow | Manual + scripting (anti-automation bypass) | Anti-automation / bot-management high if deployed; SAST very low (semantic) | Yes — agentic frameworks defeat naive anti-automation | Variable — high for fraud-relevant flows | High — bookings, refunds, account-creation flows targeted continuously |
| API7 SSRF | Burp Collaborator, mature payload corpora for cloud metadata endpoints | SAST moderate (URL-sink analysis); egress allowlist high if enforced | Yes — agentic frameworks chain SSRF → IMDS → credential theft | Mid-high tier; cloud credential-theft chains push toward Critical | High — AI-suggested "fetch URL" handlers reintroduce |
| API8 Security Misconfiguration | Nuclei templates, ZAP baseline | High — config scanners mature | Moderate | Lower tier individually; chains push higher | High prevalence; chains dominate |
| API9 Improper Inventory (shadow / zombie APIs) | API discovery tooling (Salt, Noname-class), passive traffic analysis | API gateway inventory + traffic-based discovery | Limited | Variable — shadow APIs are a finding multiplier | Very high prevalence; deprecated API endpoints continue serving traffic |
| API10 Unsafe Consumption of Third-Party APIs | Burp, custom integration fuzz | Egress allowlist; per-third-party threat model | Yes — agentic frameworks chain via third-party trust | Variable; transitive RCE chains via consumed AI-API or SaaS API are high | Emergent class through 2025–2026; AI-API consumption dominant subtype |
| AI-API rate-limit abuse / denial-of-wallet | Stolen-key abuse scripts; trivial automation | Per-identity + per-cost-unit egress quotas; budget alarms | Yes — fully automated | Direct USD loss — measurable per incident | High when keys leak; common via committed secrets, third-party breach, browser-extension exfil |
| AML.T0096 prompt-injection-as-C2 | Custom payload corpora; Promptfoo, Garak | Output guardrails, egress baselining (D3-NTA) | Yes — adaptive injection succeeds >85% against SOTA guardrails per 2026 meta-analysis | Emergent category | Active operational reality; hand-off to `ai-c2-detection` |
| AML.T0013 Discover AI Model Ontology (inference-API probing) | High-volume inference scripts; query-shape diversity tooling | Per-identity rate-and-shape monitoring at egress | Yes — agentic query diversification | Emergent | Active in adversarial-ML research; bleeding into production where hosted models expose probability vectors |

---

## Analysis Procedure

The procedure threads three foundational design principles. They are not optional.

Wire-level RFC mappings cited below resolve against `data/rfc-references.json` (RFC-7519 JWT, RFC-8725 JWT BCP, RFC-6749 OAuth 2.0, RFC-9700 OAuth Security BCP, RFC-9421 HTTP Message Signatures, RFC-8446 TLS 1.3, RFC-9114 HTTP/3); framework-gap IDs cited throughout (OWASP-ASVS-v5.0-V14, NIST-800-53-AC-2, NIST-800-218-SSDF, ISO-27001-2022-A.8.28, NIS2-Art21-incident-handling, UK-CAF-B2, AU-Essential-8-App-Hardening) resolve against `data/framework-control-gaps.json`.

**Defense in depth** — the API request lifecycle is layered. No single control is trusted to fail closed.

1. **API gateway (perimeter)** — terminates TLS (RFC 8446 baseline; HTTP/3 over QUIC per RFC 9114 for public global APIs), enforces auth, enforces rate limits per route + per identity + per cost-unit, applies threat-detection rules, captures the canonical log record. Gateways with bypass paths (a "direct backend" route that skips the gateway) are gateway-in-name-only.
2. **Schema validation (handler entry)** — every route declares its contract: OpenAPI v3.1+ for REST, AsyncAPI for event/WebSocket, Protocol Buffers for gRPC, GraphQL SDL for GraphQL. Requests are validated against the schema before any business logic runs. Unknown fields are rejected (not silently accepted) — this is the structural defence against BOPLA / mass assignment.
3. **Input validation per CWE root cause** — beyond schema shape: type ranges, regex constraints on string fields, length limits, content-type allowlists for file fields, URL allowlists for any field that becomes an outbound fetch (SSRF / API7 / CWE-918 defence).
4. **Identity assertion per request** — every request resolves to an authenticated principal. Bearer JWTs validated per RFC 7519 + **RFC 8725 (JWT BCP)**: algorithm pinned in code (no `alg: none`, no algorithm confusion), audience checked, issuer checked, expiry enforced, key resolved via JWKS with key-ID match. OAuth 2.0 flows per RFC 6749 + **RFC 9700 (OAuth 2.0 Security BCP)**: PKCE for all interactive flows, sender-constrained tokens (DPoP or mTLS) for high-value APIs, refresh-token rotation.
5. **Authorisation per object / per function (BOLA / BFLA defence)** — at the handler, after identity is resolved, the server checks: (a) does this principal have the function permission (BFLA)? (b) does this principal own / have access to *this specific object* (BOLA)? A route guard that asserts (a) without (b) is a BOLA carrier. GraphQL: field-level authorisation is mandatory.
6. **Output filtering (BOPLA defence)** — response bodies serialised through an allow-list projection (DTO / response schema) rather than dumping the model object. Sensitive fields (PII, PHI, secrets) filtered server-side, not by the client.
7. **Egress monitoring** — every outbound API call (including AI-API consumption) profiled against intent. Per-service egress allowlist; per-identity rate-and-cost baseline; AI-API destinations flagged separately from generic SaaS egress (D3-NTA; hand-off to `ai-c2-detection`).
8. **Quota enforcement** — DoS protection AND denial-of-wallet protection. Per-route, per-identity, per-cost-unit. AI-API consumption has an explicit per-user-per-day USD cap (or token cap × known unit-cost), not just a request count.

**Least privilege** — every API token, every service identity, every internal call:

- Every API token scoped per route + per resource + per action — no blanket-admin keys.
- AI-API keys scoped per workload, never broad enterprise scope. Workload keys rotated on a documented cadence; emergency rotation playbook exists and is tested.
- MCP server tokens least-privilege per tool exposed (hand-off to `mcp-agent-trust`).
- Service-to-service auth uses short-lived workload identities (SPIFFE/SPIRE, cloud-provider workload identity), not long-lived static credentials.
- Internal APIs *also* require auth — there is no "trusted internal network" carve-out.

**Zero trust** — every API request is hostile until verified:

- Mutual TLS at trust boundaries (RFC 8446 with negotiated suites; certificate-based auth = D3-CBAN).
- JWT validation strict per RFC 8725 BCP — no exceptions, no debug-mode-allows-none.
- HTTP Message Signatures (RFC 9421) for sensitive operations: write operations on regulated data, cross-tenant operations, operations crossing trust boundaries via untrusted intermediaries. RFC 9421 provides replay protection and integrity that survives proxy log-and-replay scenarios where TLS does not.
- Origin validation at WebSocket upgrade handshake; CSRF tokens or sender-constrained tokens for any cookie-authenticated API.
- Internal-network position grants nothing — SSRF assumes the attacker is already inside (per API7 / CWE-918).

**Ephemeral / serverless caveat:** session-level controls (in-process rate limiters, sticky-session anti-automation) are architecturally impossible. Replace with per-request stateless equivalents: short-TTL signed tokens (RFC 8725), gateway-enforced quotas in a distributed store (Redis-class), per-request workload identity, per-request egress allow-list. Do not require in-process state where the platform forbids it.

### The 10-step assessment

1. **Inventory every API surface.** Enumerate REST routes, GraphQL operations, gRPC services + methods, WebSocket channels, and **MCP server endpoints**. For each: protocol, auth model, request schema, response schema, data classification, AI-API consumption (which destinations), provenance (was the handler AI-suggested?). API9 (Improper Inventory Management) is detected here — shadow and zombie APIs are flagged.
2. **Schema-driven validation.** OpenAPI v3.1+, AsyncAPI, Protocol Buffers, GraphQL SDL. Schema-fuzz with Schemathesis / RESTler / equivalents. Reject unknown fields by default (structural BOPLA defence).
3. **Authentication layer audit per RFC 6749 + RFC 9700 BCP.** PKCE on every interactive flow. Refresh-token rotation. Sender-constrained tokens (DPoP / mTLS) for high-value APIs. No implicit flow. No password grant on new integrations.
4. **JWT validation strict per RFC 7519 + RFC 8725 BCP.** Algorithm pinned in code; audience, issuer, expiry, not-before enforced; JWKS with key-ID match; clock skew bounded. Reject `alg: none`, reject algorithm confusion (HS256 vs RS256 with the public key as the HMAC secret).
5. **Per-route + per-identity + per-resource rate-limits.** Documented policy. Limits informed by capacity model (DoS) AND by cost model (denial-of-wallet for AI-API consumption). API gateway as the enforcement point; in-process limits as defence-in-depth where stateful runtime supports it.
6. **BOLA + BFLA scoping audit.** For every object-ID-bearing route: assert per-object authorisation (BOLA, CWE-863). For every function-level route: assert role / scope (BFLA, CWE-862). For GraphQL: field-level authorisation, not route-level. Tool: Burp Autorize, Schemathesis with auth profiles, custom matrix scripts. The output is a coverage matrix: route × role × object-state → expected response code.
7. **GraphQL query-complexity limits.** Depth limit, breadth (alias) limit, complexity-cost calculator with budget per query, persisted-query allowlist for production clients. **Introspection disabled in production.**
8. **gRPC reflection disabled in production.** mTLS for service-to-service; per-method authorisation (BFLA in gRPC terms is per-method); deadline propagation enforced; max-message-size bounded.
9. **WebSocket origin validation at upgrade + CSRF / sender-constrained token thereafter.** Per-message authorisation if the channel multiplexes operations across resources; rate-limit per connection AND per identity (one identity cannot fan out across many connections to bypass).
10. **MCP transport audit (hand-off to `mcp-agent-trust`) and AI-API egress map (hand-off to `ai-c2-detection`).** Document every MCP server and every AI-API destination. Per-destination quota with explicit USD cap; per-identity rate-and-shape baseline; D3-NTA egress monitoring fed to SIEM. AI-API keys treated as the most sensitive credential class — rotation cadence ≤ 30 days, automated key-leak scanning on commits. The egress map cross-references the AML.T0096 / AML.T0013 catalog entries in `data/atlas-ttps.json` so that egress-baseline rules can be authored against the canonical TTP IDs rather than ad-hoc local names.

---

## Output Format

The skill produces an API Security Assessment covering REST / GraphQL / gRPC / WebSocket / MCP per-surface coverage, OWASP API Top 10 2023 + OWASP API Sec for LLM Top 10 mapping, per-endpoint authentication / authorization / rate-limit / schema-validation evidence, and the prioritized remediation roadmap. The shape below is consumed downstream by `webapp-security` (for browser-facing APIs), by `mcp-agent-trust` (for MCP surfaces), and by `compliance-theater` (which compares the deployed API controls against PCI 4.0 6.2 / OWASP ASVS L2-L3 claims). Preserve the per-endpoint control-evidence rows verbatim — they are the auditable derivation of the API-surface risk score.

```
## API Security Assessment

**Assessment Date:** YYYY-MM-DD
**Scope:** [API surfaces in scope — REST / GraphQL / gRPC / WebSocket / MCP — environments]
**OWASP API Top 10 2023 Target:** [verification level + justification by data sensitivity]

### API Inventory (by Protocol)
| Protocol | Endpoint / Service | Auth Model | Schema Source | Data Class | AI-API Consumption | Provenance | Inventory Status |
|----------|--------------------|------------|---------------|------------|--------------------|------------|------------------|
| REST | GET /api/v1/orders/{id} | OAuth bearer (JWT) | OpenAPI v3.1 | regulated (PII) | none | AI-suggested 2025-12 | active |
| GraphQL | /graphql (Query.order, Mutation.refund) | OAuth bearer (JWT) | SDL | regulated | none | human | active |
| gRPC | payments.PaymentService.* | mTLS + JWT | proto3 | regulated (PCI) | none | human | active |
| WebSocket | wss://.../stream/orders | cookie + Origin | AsyncAPI | regulated | none | human | active |
| MCP | https://mcp.internal/tools/search | OAuth bearer (JWT) | MCP tool schema | internal | Anthropic Messages API | AI-suggested | active |
| REST | /api/_internal/* | (none — shadow) | (none) | unknown | unknown | unknown | shadow — finding |

### Per-API OWASP API Top 10 2023 Risk Scorecard
| API | API1 BOLA | API2 AuthN | API3 BOPLA | API4 Quota | API5 BFLA | API6 SBF | API7 SSRF | API8 Misconfig | API9 Inventory | API10 3P | RWEP |
|-----|-----------|------------|------------|------------|-----------|----------|-----------|----------------|----------------|----------|------|
| [endpoint] | [status] | [status] | [status] | [status] | [status] | [status] | [status] | [status] | [status] | [status] | [score] |

### Authentication Coverage Matrix
| API | OAuth/RFC 9700 BCP | JWT/RFC 8725 BCP | mTLS | RFC 9421 Signatures | Sender-Constrained Tokens (DPoP/mTLS) | Notes |
|-----|--------------------|------------------|------|---------------------|---------------------------------------|-------|

### Rate-Limit Policy Ledger
| API | Per-Route Limit | Per-Identity Limit | Per-Resource Limit | Per-Cost-Unit Cap (USD/day) | Enforcement Point | Notes |
|-----|-----------------|--------------------|--------------------|-----------------------------|-------------------|-------|

### BOLA / BFLA Scoping Audit
| Route / Operation | Identity-Resolved (yes/no) | Function Auth (BFLA) | Object Auth (BOLA) | Test Method (Burp Autorize / Schemathesis / custom) | Coverage |
|-------------------|----------------------------|----------------------|--------------------|-----------------------------------------------------|----------|

### AI-API Egress Map
| Source Workload | AI-API Destination (OpenAI / Anthropic / Gemini / Bedrock / Azure OpenAI / other) | Key Scope | Key Rotation Cadence | Per-Day USD Cap | Egress Baseline (D3-NTA) | Notes |
|-----------------|-----------------------------------------------------------------------------------|-----------|----------------------|------------------|--------------------------|-------|

### MCP Transport Audit (cross-walk to mcp-agent-trust)
| MCP Server | Transport | Auth Model | Tool Inventory | Per-Tool Token Scope | Hand-Off Items |
|------------|-----------|------------|----------------|----------------------|----------------|

### Framework Gaps (Global)
[Per framework in scope from the Framework Lag Declaration — specific controls that fail for BOLA/BFLA/BOPLA, GraphQL/gRPC/WebSocket specifics, AI-API egress, and MCP transport.]

### Prioritised Recommendations
[Ordered by RWEP impact, with SLA. AI-API key rotation, BOLA scoping fixes, schema enforcement, and MCP transport hardening called out explicitly.]
```

---

## Compliance Theater Check

Each test below distinguishes paper compliance from real posture. A "no" or hand-waving answer to any of (a)–(d) means the corresponding control claim is theater.

**(a) API inventory completeness.** "List every API in your environment — REST, GraphQL, gRPC, WebSocket, MCP — including every AI-API your services consume. Produce the list now from a system of record (gateway log, service mesh, secret inventory), not from memory." If the team cannot produce an inventory, or the inventory excludes AI-API consumption, **API9 Improper Inventory Management is the posture**, regardless of policy. "We have an API catalogue" without a current list is theater — never treat a control as adequate when it cannot be demonstrated against a live inventory.

**(b) BOLA test result.** "Show your BOLA test output for the last sprint. What percentage of object-ID-bearing routes have per-object authorisation asserted by an integration test or by a contract test (Burp Autorize, Schemathesis, equivalent)?" If the answer is "we have auth on every route" without per-resource scoping verification, the auth claim is BFLA-only at best and the API1 risk is unmanaged. Per CWE-863 / CWE-862 — these are not tested into existence by route-level guards.

**(c) Rate-limit policy for AI-API consumption — denial-of-wallet exposure.** "For each AI-API your services consume (OpenAI, Anthropic, Gemini, Bedrock, Azure OpenAI, other), what is the per-user-per-day USD cost cap, where is it enforced, and when was it last tested by triggering it deliberately?" If there is no cost cap, or it has never been deliberately triggered, **denial-of-wallet exposure is open**. A leaked key over a weekend is a real budget event — not a theoretical one. Control existence requires an operational SLA, not policy language.

**(d) MCP transport policy.** "What is your MCP transport policy? Specifically: which MCP servers are sanctioned, what is the auth model on each, what is the per-tool token scope, what is on the egress allow-list, and how is anomalous MCP traffic surfaced to SIEM?" If the answer is "we just allow it through the proxy" or "we trust the agent to call only sanctioned tools," **MCP transport is unmanaged** and BOLA / SSRF on tool calls is the live risk. Hand off to `mcp-agent-trust` for the trust-model specifics; the API-security posture is the necessary precondition.

---

## Defensive Countermeasure Mapping

Each D3FEND technique below maps an offensive API-security finding to a defensive control, with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and AI-pipeline applicability (controls impossible in serverless / ephemeral contexts name an explicit scoped alternative).

| D3FEND ID | Technique | Layer (defense in depth) | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline Applicability |
|---|---|---|---|---|---|
| D3-IOPR | Input / Output Profiling (Message Analysis) | API gateway + handler entry — request and response profiled against the route's declared schema (OpenAPI / AsyncAPI / proto / GraphQL SDL) | Per-route schema; no shared "generic API filter" | Every request inspected; absence of gateway alert is not absence of attack — feeds SIEM, not a fail-closed control | Applies to AI-fronted routes — anomalous prompt shape (high-entropy, instruction-pattern tokens, unusually long context) is a profile signal; AI-API response shape profiled for staged-data exfil patterns |
| D3-NTA | Network Traffic Analysis | Egress — every outbound API call profiled against intent | Per-service egress allowlist; per-identity rate-and-cost baseline; no shared default-allow | Outbound denied by default; SSRF (API7 / CWE-918) cannot reach cloud metadata or internal-only services; AI-API destinations are explicitly enumerated, not inferred | **Critical for AI-fronted apps.** AI-API egress baselined for SesameOp-class covert C2 (hand-off to `ai-c2-detection`); denial-of-wallet detected at cost-anomaly threshold, not just request-count anomaly |
| D3-CSPP | Client-Server Payload Profiling | Handler entry — payload shape, header order, TLS fingerprint, MCP message framing anomalies | Per-route baseline; per-MCP-server baseline; no app-wide model | Anomalous payload shape suspicious even if syntactically valid (e.g., unexpected JSON field order, unusual Authorization header position, gRPC max-message-size approaching limit) | Applies to AI-fronted routes — adversarial payload shapes (repeated instruction tokens, very long context windows, Base64-encoded payloads in user-supplied fields) flagged |
| D3-MFA | Multi-Factor Authentication (auth hardening at the API gateway) | Identity layer — phishing-resistant FIDO2 / WebAuthn passkeys for human-fronted APIs; service identities for machine-to-machine | Per-principal MFA enrolment; passkey-only for privileged routes | Every interactive authentication challenge is AiTM-resistant; TOTP / SMS insufficient for privileged API surfaces | Applies — AI-assisted phishing kits compress time-to-weaponise; passkey-mandatory for any human accessing AI-API management consoles (key rotation, budget setting) |
| D3-CBAN | Certificate-Based Authentication | Service-to-service and high-value gateway boundaries — mTLS per RFC 8446 with appropriate cipher choice | Per-service workload identity (SPIFFE/SPIRE-class); no shared service certificate | Workload identity verified at every hop; certificate revocation honoured (OCSP stapling / short-lived certificates per ACME) | Applies to MCP transport — mTLS at the gateway-to-MCP-server boundary; AI-API consumption via signed-and-attested workload identity where the AI provider supports it |

D3FEND technique IDs above resolve against `data/d3fend-catalog.json`; framework-gap rationales for each layer cross-walk to the matching entries in `data/framework-control-gaps.json` (notably `OWASP-ASVS-v5.0-V14`, `NIST-800-53-AC-2`, `NIST-800-218-SSDF`, `ISO-27001-2022-A.8.28`, `NIS2-Art21-incident-handling`, `UK-CAF-B2`, and `AU-Essential-8-App-Hardening`) so the defensive layer chosen for any finding can be cross-cited to both the offensive ATT&CK / ATLAS technique (`data/attack-techniques.json`, `data/atlas-ttps.json`) and the missing framework control in one operator pass.

---

## Hand-Off / Related Skills

- **`webapp-security`** — request-lifecycle parent skill. API surfaces sit inside the webapp request lifecycle; OWASP Web Top 10 + OWASP API Top 10 are companion catalogues, not substitutes.
- **`mcp-agent-trust`** — MCP transport-specific trust model: which MCP servers are sanctioned, per-tool token scope, agent-to-tool authorisation. This skill provides the transport-layer posture; `mcp-agent-trust` provides the agent semantics.
- **`ai-c2-detection`** — AI-API egress baselining for SesameOp-class covert C2 detection. Hand off the AI-API egress map produced here.
- **`identity-assurance`** — operationalise OAuth (RFC 6749 + RFC 9700 BCP), JWT (RFC 7519 + RFC 8725 BCP), FIDO2 / passkey, and full token lifecycle. The API-security posture asserts presence of these controls; `identity-assurance` operationalises them end-to-end.
- **`dlp-gap-analysis`** — API egress is a primary DLP channel. Hand off AI-API egress patterns, response-projection (BOPLA / Excessive Data Exposure) findings, and any cross-tenant API surface.
- **`defensive-countermeasure-mapping`** — extend the D3FEND mapping above into a full multi-layer defensive architecture review.
