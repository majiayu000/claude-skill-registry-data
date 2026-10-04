---
name: webapp-security
version: "1.0.0"
description: Web application security for mid-2026 — OWASP Top 10 2025, OWASP ASVS v5, CWE root-cause coverage, AI-generated code weakness drift, server-rendered vs SPA tradeoffs, defense-in-depth across the request lifecycle
triggers:
  - webapp security
  - web application security
  - owasp top 10
  - owasp asvs
  - xss
  - csrf
  - sqli
  - sql injection
  - path traversal
  - ssrf
  - file upload
  - command injection
  - unsafe deserialization
  - broken access control
  - ai generated code
data_deps:
  - framework-control-gaps.json
atlas_refs:
  - AML.T0051
attack_refs:
  - T1190
  - T1059
  - T1505
framework_gaps:
  - OWASP-ASVS-v5.0-V14
  - OWASP-LLM-Top-10-2025-LLM01
  - NIST-800-218-SSDF
  - ISO-27001-2022-A.8.28
  - NIS2-Art21-incident-handling
  - UK-CAF-B2
  - AU-Essential-8-App-Hardening
rfc_refs:
  - RFC-8446
  - RFC-9114
  - RFC-7519
  - RFC-8725
cwe_refs:
  - CWE-22
  - CWE-77
  - CWE-78
  - CWE-79
  - CWE-89
  - CWE-94
  - CWE-200
  - CWE-269
  - CWE-287
  - CWE-352
  - CWE-434
  - CWE-502
  - CWE-732
  - CWE-862
  - CWE-863
  - CWE-918
  - CWE-1188
d3fend_refs:
  - D3-IOPR
  - D3-NTA
  - D3-CSPP
  - D3-EAL
  - D3-MFA
forward_watch:
  - NGINX Rift CVE-2026-42945 (disclosed 2026-05-13, source depthfirst) — KEV-watch predicted CISA KEV listing by 2026-05-29; AI-assisted discovery angle; track for active-exploitation confirmation and patch advisory affecting front-door web app deployments
last_threat_review: "2026-09-18"
discovery_mode: "standalone"  # operator-reached via `exceptd brief webapp-security` or `exceptd ask`; not chained into any playbook's direct.skill_chain by design
---

# Web Application Security Assessment

## Threat Context (mid-2026)

Webapps still ship CWE-79 (Cross-Site Scripting), CWE-89 (SQL Injection), and CWE-22 (Path Traversal) at rates the industry was supposed to have engineered out of existence by 2018. The reason is not mystery — it is AI codegen drift. Coding assistants (GitHub Copilot, Cursor, Windsurf, Claude Code, Codex, Gemini Code Assist) reintroduce OWASP-Top-10-class weaknesses into new code at roughly the rate human review removed them during the 2010s. Industry analysis published in early 2026 across several large-codebase studies converges on the same order of magnitude: approximately **30% of AI-suggested webapp code contains at least one Top-10-class weakness**, and approximately **60% of those weaknesses reach production unmodified** because the human developer treats the assistant's output as reviewed-by-default.

**CVE-2025-53773 (GitHub Copilot prompt-injection RCE, CVSS 7.8 / AV:L)** is the canonical mid-2026 case: the weakness propagated *through* the coding assistant rather than from a human developer. The attack vector is a hidden adversarial instruction in a PR description; when a developer asks Copilot to summarise the PR, the injected instruction runs in the developer's session context. This collapses the boundary between code review and code execution — the AI is both the reviewer and the executor, and the prompt is the payload. OWASP Top 10 2025 added **LLM01 (Prompt Injection)** as a top-tier risk for any AI-fronted webapp; ASVS v5 does not yet operationalise prompt injection as a verification surface.

**Architectural reaction: server-rendered apps regained share.** Through 2023–2025 the SPA-everything trend pushed business logic, auth state, and access decisions into the client. With AI codegen now producing client-side TypeScript at industrial volume, the per-route client attack surface compounded — every route became a potential CWE-200 (Information Exposure) and CWE-862 (Missing Authorization) carrier because client-side checks are advisory, not authoritative. Mid-2026 architectures favour **server-rendered-by-default with interactive islands**: React Server Components, Next.js App Router, Remix, Phoenix LiveView, HTMX, Rails Hotwire. Auth lives on the server. State changes traverse server actions. SPAs survive where a true client-side data model exists (collaborative editing, offline-first), and they pay for it with explicit zero-trust auth on every endpoint.

**Exploit acceleration is current operational reality, not a forecast.** Agentic exploitation frameworks emerging through 2025–2026 (PentestGPT lineage, autonomous-recon-and-exploit toolchains) compress the time from CVE disclosure to mass exploitation for known webapp weakness classes. The defender's working assumption must be: any CVE-2025/2026 RCE in a public webapp framework is being scanned for within hours of disclosure, not days (AI acceleration is current operational reality).

**Transport is no longer a choice.** RFC 8446 (TLS 1.3) is baseline; RFC 9114 (HTTP/3 over QUIC) is the production transport for any public webapp serving a global audience. Skills citing TLS 1.2 as adequate in 2026 are citing a deprecated threat model. JWT-based session tokens must be issued and validated per RFC 7519 with RFC 8725 (JWT BCP) — the BCP is non-optional because the original RFC 7519 threat model under-specified algorithm pinning, audience checks, and key confusion.

---

## Framework Lag Declaration

| Framework | Control | Why It Fails in mid-2026 |
|---|---|---|
| OWASP Top 10 2025 | LLM01 (Prompt Injection) added as #1 for AI-fronted apps | The list now names prompt injection as a webapp risk class, but most ASVS-driven verification programmes have not yet incorporated it as a tested surface. Tracked in `data/framework-control-gaps.json` as OWASP-LLM-Top-10-2025-LLM01. |
| OWASP ASVS v5.0 | V14 (Configuration) | V14 covers configuration hardening for the deployed app. It does not yet operationalise **AI-generated code as a verification surface**: there is no V14 requirement to mark AI-generated handlers, no separate verification level for AI-introduced weakness drift, no provenance attestation. Tracked as OWASP-ASVS-v5.0-V14. |
| OWASP ASVS v5.0 | V5 (Validation, Sanitization & Encoding) | Comprehensive for human-authored validation logic; assumes the developer chose the encoding. AI-suggested handlers frequently bypass the project's canonical validation library and inline ad-hoc string handling — V5 has no requirement to detect *which* validation path is used per route. |
| NIST SSDF (SP 800-218) | PW.4 / PW.7 (secure coding practices, code review) | SSDF mentions secure coding and review without naming AI-codegen as a special case. The "review" assumed in PW.7 is a human reading code; it does not require re-review when the next AI-codegen-CVE wave reveals a new weakness class in previously-shipped AI-suggested code. Tracked as NIST-800-218-SSDF. |
| ISO 27001:2022 | A.8.28 (Secure coding) | Method-agnostic — applies equally to hand-written and AI-generated code, which means it has no AI-codegen-specific control surface. Tracked as ISO-27001-2022-A.8.28. |
| EU NIS2 (2022/2555) | Art. 21(2)(e) effectiveness of cybersecurity measures | Requires policies for assessing effectiveness but does not mandate webapp pen testing, ASVS verification, or AI-codegen review cadence. An organisation can claim Art. 21(2)(e) compliance with a yearly checklist and no offensive test. |
| EU DORA (2022/2554) | Art. 24–25 ICT testing, Art. 26 TLPT | TLPT is mandatory only for in-scope financial entities and only periodically. Day-to-day webapp testing is left to the entity's "ICT risk management framework" — no specific minimum. |
| UK NCSC CAF | B4 (Vulnerability management) | Method-neutral and outcome-based — does not specify webapp testing depth, ASVS level, or AI-codegen audit. A B4-compliant org may still ship CWE-79 in AI-generated handlers. |
| AU ISM | Control 1235 (secure programming practices) | Names secure programming but predates the AI-codegen weakness-drift problem. No control distinguishing AI-suggested code from human-authored code. |
| JP FISC v9 | Secure-coding baseline | Sector-specific (banking/financial) baseline for secure development. Does not address AI-generated code provenance or re-review obligations. |
| IL INCD | Secure-coding directives (gov + critical infra) | Mandates secure-coding training and SAST/DAST in the SDLC. Does not mandate AI-codegen provenance markers or differential review. |
| SG MAS TRM | §7 software development | Sector-specific (regulated financial entities). Names secure coding lifecycle but does not address AI-codegen as a distinct risk class. |
| NYDFS 23 NYCRR 500 | §500.5 penetration testing & vulnerability assessment | Annual pen test + bi-annual vulnerability assessment is the floor. For AI-fronted apps with prompt-injection surface, "annual" is structurally inadequate against agentic-exploit timelines. |

---

## TTP Mapping (MITRE ATT&CK Enterprise + ATLAS v2026.09)

| TTP ID | Technique | Webapp Manifestation | CWE Root-Causes | Framework Coverage |
|---|---|---|---|---|
| T1190 | Exploit Public-Facing Application | Direct exploitation of an internet-exposed webapp endpoint | CWE-22, CWE-78, CWE-79, CWE-89, CWE-94, CWE-434, CWE-502, CWE-918 | Partial — ASVS V5/V7/V12 cover; framework gap for AI-codegen weakness reintroduction |
| T1059 | Command and Scripting Interpreter | Server-side RCE via webapp handler invoking a shell/interpreter | CWE-77, CWE-78, CWE-94, CWE-502 | Partial — secure coding standards address; no AI-codegen-specific control |
| T1505 | Server Software Component (web shell) | Post-exploitation web shell uploaded via dangerous file upload or path traversal | CWE-22, CWE-434, CWE-732 | Partial — D3-EAL (executable allowlisting) and write-once webroot mitigate; no framework mandates either |
| T1078 | Valid Accounts (used after credential capture / IDOR) | Authenticated-context abuse following CWE-863 / CWE-352 / CWE-1188 weaknesses | CWE-269, CWE-287, CWE-352, CWE-862, CWE-863, CWE-1188 | Partial — ASVS V3/V4 cover session/access; no control for AI-suggested authorisation logic |
| AML.T0051 | LLM Prompt Injection (for AI-fronted webapps) | Adversarial instructions in user input reaching an LLM with tool/action capability | CWE-94 (interpreted-instruction injection class) | Missing in NIST/ISO/SOC 2; OWASP LLM Top 10 2025 LLM01 names it; ASVS v5 does not yet test it |

---

## Exploit Availability Matrix

| CWE Class | Tooling Maturity (offensive) | Tooling Maturity (defensive SAST/DAST/IAST) | AI-Augmented Exploitation | Bug Bounty Market Signal (mid-2026, order-of-magnitude) | Patch Availability |
|---|---|---|---|---|---|
| CWE-89 (SQLi) | Burp Suite Pro, sqlmap, ZAP — fully mature | Semgrep, CodeQL, GitHub Advanced Security, Snyk Code — high coverage | Yes — agentic frameworks chain recon + payload generation | Critical SQLi → RCE typically tens-of-thousands USD on enterprise programmes | Instant for framework CVEs; cultural-fix lag for AI-codegen reintroduction |
| CWE-79 (XSS) | Burp, ZAP, XSStrike — mature; DOM XSS still finds in SPAs | SAST high for reflected; weaker for DOM/mutation XSS | Yes — automated payload mutation against context-aware filters | Stored XSS on auth surface mid-single-digit thousands USD | Framework patches instant; AI-codegen reintroduction recurs |
| CWE-22 (Path Traversal) | Mature (Burp, ZAP, ffuf) | SAST high coverage for direct sinks | Moderate — agentic recon enumerates upload+download pairs | Lower-mid thousands USD typical | Instant for framework; reintroduced by AI-suggested file-handler code |
| CWE-78 / CWE-77 (Command Injection) | Mature (Burp, commix) | SAST high coverage; IAST excellent | Yes — straightforward for agentic toolchains | Critical RCE order-of-magnitude tens-of-thousands USD | Patchable but reintroduced when AI suggests shell-exec helpers |
| CWE-434 (Dangerous File Upload) | Mature; chains with T1505 web shell installation | SAST moderate; DAST high; IAST excellent | Yes | Critical RCE tier when chains to webshell | Patchable per-route; reintroduced by AI-suggested upload handlers |
| CWE-918 (SSRF) | Mature (Burp Collaborator, cloud metadata endpoints) | SAST moderate; needs allow-list intent annotation | Yes — agentic frameworks chain SSRF → cloud IMDS → credential theft | High mid-tier (cloud credential theft chains push toward Critical) | Patchable; commonly reintroduced when AI suggests "fetch URL" handlers |
| CWE-502 (Unsafe Deserialization) | Mature (ysoserial, marshalsec) | SAST high in Java/.NET; weaker in dynamic-language native-format deserialisers | Yes | Critical RCE tier | Patchable but reintroduced when AI suggests "deserialise the request body" handlers without an allow-list |
| CWE-352 (CSRF) | Mature; SameSite weakens but does not eliminate | SAST low (intent-dependent); DAST moderate | Limited — defence is structural | Lower-mid thousands USD typical | Defence is architectural (CSRF tokens + SameSite + origin checks) |
| CWE-862 / CWE-863 (Missing/Incorrect Authorisation, IDOR class) | Mature (Burp Autorize) | SAST low — intent-dependent; requires per-route auth model | Yes — agentic frameworks enumerate route + token combinations | IDOR mid-tier; privilege-escalation IDOR high mid-tier | Per-route fix; reintroduced when AI suggests handlers without auth check |
| CWE-1188 (Insecure Default Initialization) | Manual review heavy | SAST moderate (config-aware) | Limited | Variable | Architectural |
| AML.T0051 (Prompt Injection, AI-fronted webapps) | Manual + emerging Garak / Promptfoo / adaptive frameworks | Prompt-injection classifiers, output guardrails — partial only | Yes — adaptive attacks succeed >85% against SOTA defences per 2026 meta-analysis | Variable — emerging programme category | No reliable patch; defence-in-depth only |

---

## Analysis Procedure

The procedure threads three foundational design principles end-to-end. They are not optional and they are not interchangeable.

**Defense in depth** — the request lifecycle is layered, no single control is trusted to fail closed:

1. **Perimeter** — WAF / CDN bot management is a signal layer, not a control layer. WAF rules detect known payload shapes (Burp default, sqlmap default) but do not catch AI-mutated payloads reliably. Treat WAF output as a tripwire feeding SIEM, never as a substitute for input validation.
2. **Transport** — TLS 1.3 (RFC 8446) baseline; HTTP/3 over QUIC (RFC 9114) for public global apps. HSTS preload. Certificate pinning where the client is a controlled mobile app, not a browser.
3. **Input validation (canonical control)** — every route declares its input schema (JSON Schema, Pydantic, Zod, ASP.NET model binding). Validation happens server-side at handler entry. Schemas pinned to project canonical types — no ad-hoc inline parsing in AI-suggested handlers.
4. **Output encoding (XSS counter)** — context-aware encoding per sink (HTML body, attribute, JS, URL, CSS). Server-rendered templates default to escape; SPA frameworks default to escape but interpolate raw HTML on developer opt-in (raw-HTML interpolation APIs and analogues are reviewed surfaces).
5. **Auth at every endpoint (no implicit trust between handlers)** — every route declares its required role/scope. There is no "internal" handler that skips auth because it is "only called by other handlers".
6. **CSRF tokens + SameSite cookies + origin checks (state-change defence)** — defence is layered because each component fails in known scenarios: SameSite=Lax permits top-level navigation; tokens fail if leaked via XSS; origin checks fail behind some proxies. Use all three.
7. **DB parameterisation (SQLi counter)** — every query parameterised. ORMs default to parameterised; raw SQL is a reviewed surface. AI-suggested handlers that build SQL strings via interpolation are blocked at PR.
8. **Server-rendered with interactive islands** — reduces the client attack surface. State changes traverse server actions. Auth decisions are server-authoritative. SPAs only where a real client-side data model exists.
9. **SAST + DAST + IAST in CI** — SAST (Semgrep, CodeQL, GitHub Advanced Security) at every PR; DAST (ZAP, Burp Enterprise) on staging; IAST in staging integration tests. Findings have an explicit fix-or-document SLA, not an indefinite backlog.
10. **Fuzz parser surfaces** — every binary/text parser exposed to user input is fuzzed (hand-off to `fuzz-testing-strategy`).

**Least privilege** — every endpoint, every service-account, every deployment principal:

- Every endpoint declares the minimum role/scope; no super-handler that "does everything".
- Service-account-style API tokens scoped per route, per action, not blanket-admin.
- AI-generated handlers default to **least privilege per ASVS V14** — no implicit elevation, no shared credential pool.
- Database principals scoped per service (no app-wide DBA credential); row-level security where the framework supports it.
- File-handler processes run with a write-once webroot and no shell.

**Zero trust** — every request is hostile until proven otherwise:

- Sessions short-lived. Refresh tokens rotated and sender-constrained (DPoP / mTLS) per RFC 9700 BCP.
- JWTs validated per RFC 7519 + RFC 8725: algorithm pinned, audience checked, expiry enforced, key resolved via JWKS with key-ID match — no algorithm-none acceptance, no algorithm confusion.
- Every state change requires explicit auth + CSRF + origin.
- Never trust client-provided role / identity / tenant; the server resolves identity from the session and authorisation from the server-side policy.
- Internal-network position grants nothing — SSRF assumes the attacker is already inside.

### The 10-step assessment

1. **Inventory routes + auth requirements + data sensitivity.** Enumerate every HTTP route (or GraphQL operation, gRPC method). For each: required role, request schema, response schema, data classification, AI-codegen provenance flag (was this handler suggested by an assistant?).
2. **Map each route to CWE-Top-25-class risk.** Score by CWE class × data sensitivity × external reachability. Apply the RWEP model — CVSS alone fails as a prioritization signal; report CVSS alongside RWEP, never alone.
3. **Audit AI-generated code separately from human-written code.** Require commit-time provenance markers (git trailer, commit-message tag, or co-author metadata) identifying AI-assisted commits. Re-review AI-suggested handlers on every AI-codegen-CVE wave (e.g. CVE-2025-53773, CVSS 7.8 / AV:L — re-review every Copilot agent-mode-generated handler in the affected window, with priority on those that read external content into the agent context). If provenance is not captured, the org cannot answer "what code do we need to re-review?" — this is a compliance-theater indicator.
4. **SAST + DAST coverage measurement.** Report: % of routes covered by SAST sinks, % covered by DAST in staging, findings-to-fix ratio over trailing 90 days. A SAST programme that finds and does not fix is theater (control existence requires an operational fix SLA, not just tooling).
5. **IAST in staging.** Instrumented runtime testing covers what SAST cannot (intent-dependent authorisation, runtime config). Required for any app handling regulated data (PII, PCI, PHI).
6. **Fuzz parser surfaces.** Hand off to `fuzz-testing-strategy` for any parser, deserialiser, or media-handler reachable from a public route. Fuzz corpus seeded from production traffic samples (sanitised).
7. **Server-rendered-by-default decision.** Justify any SPA-only route against the AI-codegen blast radius. SPAs allowed where a true client-side data model exists; not allowed by default for CRUD with auth checks.
8. **CSRF + origin + SameSite policy.** Document the per-route stance. Cookie-based session auth without SameSite=Lax or Strict + CSRF tokens is a finding. Bearer-token auth on the Authorization header is not CSRF-exempt for mixed cookie/bearer apps — verify.
9. **Output encoding policy.** Per-template-engine default-escape verification. Audit every raw-HTML opt-out (raw-interpolation APIs, `|safe`, `html_safe`, `raw()`). Each opt-out is a reviewed and documented surface.
10. **Deployment with least-privilege service identity.** Database creds scoped per service. Outbound network policy denies by default (mitigates CWE-918 SSRF → cloud metadata exfiltration chain). Filesystem writes scoped to a single ephemeral path. No shared service account across microservices.

---

## Output Format

The skill produces a Web Application Security Assessment covering OWASP ASVS-mapped per-control coverage, OWASP Top 10 + API Top 10 findings, AI/LLM Top 10 exposure for any LLM-integrated routes, dependency-risk inventory, and the prioritized remediation roadmap. The shape below is consumed downstream by `api-security` (for service-to-service routes), by `ai-attack-surface` (for any LLM-integrated component), and by `compliance-theater` (which compares the ASVS-claimed level against the deployed-control evidence). Preserve the per-control coverage rows verbatim — they are the auditable ASVS-level derivation.

```
## Web Application Security Assessment

**Assessment Date:** YYYY-MM-DD
**Scope:** [app/repo names, route count, in-scope environments]
**ASVS Target Level:** [L1 / L2 / L3, with justification by data sensitivity]

### Per-Route Risk Matrix
| Route | Auth Required | Data Class | CWE Root-Cause Risks | Current Controls | AI-Codegen Blast Radius | RWEP | Remediation |
|-------|---------------|------------|----------------------|------------------|-------------------------|------|-------------|
| POST /api/upload | role:editor | regulated | CWE-434, CWE-22, CWE-78 | content-type allowlist; magic-byte check; UUID rename | Suggested by Copilot 2025-11; not re-reviewed | [score] | [action + SLA] |

### AI-Codegen Audit Summary
- Total routes: [N]
- Routes with AI-suggested handlers (provenance-marked): [N] ([%])
- Routes with AI-suggested handlers (provenance unknown): [N] ([%]) — compliance-theater indicator if >10%
- Routes re-reviewed after most recent AI-codegen CVE wave: [N] ([%])
- AI-suggested handlers bypassing canonical validation library: [N]
- AI-suggested handlers without auth check: [N]

### ASVS Coverage Report
| ASVS Section | L1 / L2 / L3 Verified | Gaps |
|--------------|----------------------|------|
| V2 Authentication | [status] | [items] |
| V3 Session Management | [status] | [items] |
| V4 Access Control | [status] | [items] |
| V5 Validation, Sanitization & Encoding | [status] | [items] |
| V7 Error Handling & Logging | [status] | [items] |
| V8 Data Protection | [status] | [items] |
| V12 Files & Resources | [status] | [items] |
| V13 API & Web Service | [status] | [items] |
| V14 Configuration (incl. AI-codegen gap per OWASP-ASVS-v5.0-V14) | [status] | [items] |

### OWASP Top 10 2025 Coverage Card
| Rank | Category | Coverage | Notes |
|------|----------|----------|-------|
| A01 | Broken Access Control | [status] | CWE-862/863/1188 audit per route |
| A02 | Cryptographic Failures | [status] | TLS 1.3 baseline, JWT per RFC 8725 |
| A03 | Injection | [status] | CWE-79/89/77/78/94 — DB parameterisation, output encoding |
| A04 | Insecure Design | [status] | Threat-model currency (hand-off) |
| A05 | Security Misconfiguration | [status] | ASVS V14 |
| A06 | Vulnerable & Outdated Components | [status] | Hand-off to supply-chain-integrity |
| A07 | Identification & Authentication Failures | [status] | Hand-off to identity-assurance |
| A08 | Software & Data Integrity Failures | [status] | CWE-502; SLSA provenance for build outputs |
| A09 | Security Logging & Monitoring Failures | [status] | Auth-failure logging, anomaly detection |
| A10 | Server-Side Request Forgery | [status] | CWE-918; outbound network policy |
| LLM01 | Prompt Injection (for AI-fronted routes) | [status] | Per OWASP-LLM-Top-10-2025-LLM01; hand-off to ai-attack-surface |

### Framework Gaps (Global)
[Per framework in scope from the Framework Lag Declaration: specific controls that fail for AI-codegen weakness drift and prompt-injection surface.]

### Prioritised Recommendations
[Ordered by RWEP impact, with SLA. AI-codegen re-review actions called out explicitly.]
```

---

## Compliance Theater Check

Each test below distinguishes paper compliance from real posture. A "no" answer to any of (a)–(d) means the corresponding control claim is theater.

**(a) SAST findings-to-fix ratio.** "Show me the most recent SAST report for this codebase. What was the findings-to-fix ratio over the last 90 days?" If SAST runs but findings sit in a backlog with no SLA — or if the team's first response is "we have a SAST tool" without producing the ratio — the SAST control is theater (a control exists only when it has an operational SLA, not when the tool is merely owned).

**(b) Auth-failure test coverage.** "What percentage of routes have unit or integration tests that assert auth failure modes — 401 when unauthenticated, 403 when authenticated as a non-authorised role, 404-or-403 (depending on policy) when the resource exists but the caller has no access?" If the answer is qualitative ("we test auth") rather than a number, the auth-control claim is paper (CWE-862 / CWE-863 / CWE-1188 are not tested into existence by the framework alone).

**(c) AI-codegen provenance.** "Is AI-generated code marked at commit time — git trailer, commit message tag, or co-author metadata — so it can be re-reviewed at the next AI-codegen-CVE wave?" If there is no provenance signal, the org cannot answer "what code do we need to re-review when the next CVE-2025-53773-class issue lands?" — and the re-review claim is theater.

**(d) Bug-bounty time-to-fix for Critical.** "For your last 10 bug-bounty payouts (or your last 10 internal security findings classified Critical), what was the time-to-fix? Provide the dates." If the median time-to-fix for Critical exceeds 30 days, the vulnerability-management claim is theater regardless of what the policy document says. For Critical RCE in an AI-codegen reintroduction class (CWE-89, CWE-78, CWE-502, CWE-918), the operational target should be measured in hours-to-days, not weeks (control existence requires an operational SLA, not policy language).

---

## Defensive Countermeasure Mapping

Each D3FEND technique below maps an offensive finding from the assessment to a defensive control, with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and AI-pipeline applicability.

| D3FEND ID | Technique | Layer (defense in depth) | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline Applicability |
|---|---|--------------------------|-----------------------|--------------------|---------------------------|
| D3-IOPR | Input / Output Profiling (Message Analysis) | Perimeter + handler entry — request shape and content profiling against a route's declared schema | Per-route schema; no shared "generic input filter" | Every request inspected; absence of WAF alert is not absence of attack — feeds SIEM, not a fail-closed control | Applies to AI-fronted routes — anomalous prompt shape (high-entropy, instruction-pattern) is a profile signal |
| D3-NTA | Network Traffic Analysis | Network egress — webapp outbound connections profiled against intent | Per-service egress allowlist; no shared default-allow | Outbound denied by default; SSRF (CWE-918) cannot reach cloud metadata or internal-only services | Critical for AI-fronted apps — model API calls profiled for SesameOp-style covert C2 (hand-off to ai-c2-detection) |
| D3-CSPP | Client-Server Payload Profiling | Handler entry — request payload shape, header order, TLS fingerprint anomalies | Per-route baseline; no app-wide model | Anomalous request shape is suspicious even if syntactically valid | Applies to AI-fronted routes — adversarial payload shapes (long context, repeated instruction tokens) flagged |
| D3-EAL | Executable Allowlisting | Server filesystem — block T1505 web-shell installation post-CWE-22 / CWE-434 exploitation | Write-once webroot; service principal cannot execute scripts in upload directory | Even on successful upload exploit, the uploaded file cannot execute as a handler | Applies — protects AI-assistant-suggested file-upload handlers that miss the executable-extension check |
| D3-MFA | Multi-Factor Authentication (Auth Hardening) | Identity layer — phishing-resistant FIDO2 / WebAuthn passkeys | Per-principal; no shared MFA enrolment | Every authentication challenge resistant to AiTM proxy phishing; passkey-only for privileged routes | Critical — AI-assisted phishing kit development compresses time-to-weaponise; TOTP / SMS are insufficient (hand-off to identity-assurance) |

---

## Hand-Off / Related Skills

- **`attack-surface-pentest`** — operate this skill's per-route risk matrix as scoping input for offensive testing (TIBER-EU / CBEST style).
- **`fuzz-testing-strategy`** — hand off every parser, deserialiser, and media-handler surface identified in step 6 of the procedure.
- **`defensive-countermeasure-mapping`** — extend the D3FEND mapping above into a full multi-layer defensive architecture review.
- **`identity-assurance`** — operationalise D3-MFA and the auth-at-every-endpoint requirement (FIDO2 / passkey / OIDC / RFC 9700 OAuth BCP).
- **`supply-chain-integrity`** — extend OWASP Top 10 2025 A06 (Vulnerable & Outdated Components) and A08 (Software & Data Integrity Failures) into SBOM, SLSA, VEX, and Sigstore coverage.
- **`ai-attack-surface`** — for AI-fronted routes, hand off the LLM01 prompt-injection surface and MCP trust posture analysis.
- **`ai-c2-detection`** — for AI-fronted apps, integrate D3-NTA egress baselining for SesameOp-class covert C2 detection.
- **`threat-modeling-methodology`** — apply STRIDE / PASTA / LINDDUN to the per-route risk matrix for design-time coverage of OWASP Top 10 2025 A04 (Insecure Design).
