---
name: ai-attack-surface
version: "1.0.0"
description: Comprehensive AI/ML attack surface assessment mapped to MITRE ATLAS v2026.09 with explicit framework gap flags
triggers:
  - ai attack surface
  - prompt injection
  - llm security
  - ai security assessment
  - model security
  - ai threat model
  - ai red team
  - promptsteal
  - promptflux
data_deps:
  - d3fend-catalog.json
atlas_refs:
  - AML.T0043
  - AML.T0051
  - AML.T0054
  - AML.T0020
  - AML.T0096
  - AML.T0016
  - AML.T0017
  - AML.T0013
  - AML.T0018
attack_refs:
  - T1566
  - T1059
  - T1190
framework_gaps:
  - ALL-AI-PIPELINE-INTEGRITY
  - ALL-PROMPT-INJECTION-ACCESS-CONTROL
  - ISO-27001-2022-A.8.28
  - ISO-IEC-23894-2023-clause-7
  - NIST-800-53-AC-2
  - NIST-800-53-SI-3
  - OWASP-LLM-Top-10-2025-LLM01
  - OWASP-LLM-Top-10-2025-LLM02
  - SOC2-CC6-logical-access
  - EU-AI-Act-Art-15
  - UK-CAF-A1
  - AU-Essential-8-App-Hardening
cwe_refs:
  - CWE-1039
  - CWE-1426
  - CWE-94
d3fend_refs:
  - D3-IOPR
  - D3-NTA
  - D3-EAL
  - D3-FAPA
  - D3-CSPP
forward_watch:
  - NGINX Rift CVE-2026-42945 (disclosed 2026-05-13, source depthfirst) — KEV-watch predicted CISA KEV listing by 2026-05-29; AI-assisted discovery angle; track for active-exploitation confirmation and patch advisory
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — LiteLLM 3-bug SSRF + Code Injection chain by k3vg3n; expect coordinated CVE assignments and upstream patch; track KEV add post-embargo
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — LiteLLM full SSRF + Code Injection by Out Of Bounds (Byung Young Yi); duplicate-class with the k3vg3n entry; track unified patch advisory
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — LM Studio 5-bug exploit chain by STARLabs SG; impacts local AI runtime trust; track patch and MCP integration advisories
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — OpenAI Codex CWE-150 improper neutralization by Compass Security; AI coding-agent surface; forward-watch only (no coding-agent-security skill yet)
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — Chroma vector DB CWE-190 + CWE-362 chain by haehae; impacts RAG vector store integrity; track patch and downstream RAG advisory
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — NVIDIA Megatron Bridge overly permissive allowed list by Satoki Tsuji; AI training-stack supply-chain exposure; track patch and SBOM advisory
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — NVIDIA Megatron Bridge path traversal by haehae; AI training-stack file-system trust boundary; track patch and SBOM advisory
last_threat_review: "2026-09-28"
---

# AI Attack Surface Assessment

## Threat Context (mid-2026)

The AI attack surface is not speculative. It is actively exploited. The following are confirmed, documented threats as of mid-2026.

### 1. Prompt Injection as Enterprise RCE

**CVE-2025-53773** — Hidden prompt injection in GitHub Copilot agent mode coerces the assistant to write `"chat.tools.autoApprove": true` into `.vscode/settings.json`, flipping every subsequent tool call into auto-approval. CVSS 7.8 (AV:L — local-vector through developer-side IDE interaction; RWEP 30). The attack embeds adversarial instructions in any agent-readable content (source comments, README, PR descriptions, retrieved docs, MCP tool responses). Once the YOLO-mode flag lands, the next shell tool call executes attacker-chosen commands in the developer's user context.

This is not a chatbot trick. This is enterprise RCE via a developer tool used by hundreds of millions of developers. The attack surface is any system that:
- Feeds external content (user input, web content, documents, PR descriptions, emails, calendar events) into an LLM prompt
- Where that LLM has tools, actions, or code execution capability

**Attack success rates against SOTA defenses:** A 2026 meta-analysis of 78 studies found adaptive prompt injection strategies succeed against state-of-the-art defenses at rates exceeding 85%. No current framework has adequate controls for this.

**ATLAS ref:** AML.T0054 (LLM Jailbreak) and AML.T0051 (LLM Prompt Injection)

### 2. MCP Supply Chain — Architectural RCE

The Model Context Protocol (MCP) introduced an architectural vulnerability affecting every major AI coding assistant: Cursor, VS Code + GitHub Copilot, Windsurf, Claude Code, Gemini CLI.

**CVE-2026-30615** — Windsurf MCP. CVSS 8.0 (AV:L — local-vector RCE requiring attacker-controlled HTML the MCP client processes; RWEP 35). The vulnerability allows a malicious or compromised MCP server to drive code execution in the context of the AI assistant once a victim installs it. 150M+ combined downloads across MCP-capable assistants share the same architectural attack surface.

This is a supply chain attack surface. Every MCP server a user installs is a potential RCE vector. Trust boundaries that exist for npm packages do not exist for MCP servers because most MCP clients do not enforce signed manifests or tool allowlists.

**ATLAS ref:** AML.T0010 (AI Supply Chain Compromise)

### 3. AI-Assisted Exploit Development

41% of 2025 zero-days were discovered by attackers using AI-assisted reverse engineering (GTIG 2025 annual). Copy Fail (CVE-2026-31431) was discovered by an AI system in approximately one hour. The first documented AI-built in-the-wild zero-day surfaced 2026-05-11 (GTIG AI 2FA-bypass case), and Fragnesia (CVE-2026-46300, Linux LPE) was disclosed 2026-05-13 by William Bowling / Zellic with explicit credit to Zellic's AI-agentic code-auditing tool — the anchor case for autonomous AI vulnerability discovery in load-bearing OSS (18-year-old kernel code path). The Dirty Frag pair (CVE-2026-43284 / CVE-2026-43500) was disclosed 2026-05-08 and industry analysis (Sysdig, Help Net Security) assesses AI-assisted discovery as likely given the 9-year exposure window. The exceptd catalog's 2026 AI-discovery rate is now 40%, tracking the GTIG 41% reference. Defensive posture is calibrated to CTID Secure AI v2 (released 2026-05-06) — Secure AI v1 is superseded.

The implication: the time between a vulnerability's introduction into a codebase and its reliable exploitation has compressed from months or years to hours or days for AI-capable threat actors. Patch management SLAs designed for human-speed exploit development are structurally inadequate.

**ATLAS ref:** AML.T0017 (Develop Capabilities)

### 4. AI Credential Phishing Acceleration

Credential theft driven by AI increased 160% in 2025. 82.6% of phishing emails now contain AI-generated content undetectable by grammar/style checks. Traditional phishing detection heuristics (poor grammar, unusual phrasing, template patterns) are no longer reliable detectors.

**ATLAS ref:** AML.T0016 (Obtain Capabilities), covering public AI APIs misused to generate phishing payloads

### 5. AI as Covert C2 — SesameOp

Adversaries are repurposing legitimate AI agent APIs as covert command-and-control channels (ATLAS AML.T0096). The SesameOp campaign demonstrated this technique:
- C2 commands encoded in prompt fields
- Exfiltrated data returned in completion fields
- Traffic pattern is indistinguishable from legitimate AI API usage
- Evades all traditional C2 detection (DGA, beaconing, protocol anomalies)

### 6. PROMPTFLUX and PROMPTSTEAL Malware Families

Two malware families actively query LLMs during execution:
- **PROMPTFLUX**: Queries public LLMs for evasion guidance in real time — "generate code equivalent to [flagged signature] that doesn't match this detection pattern"
- **PROMPTSTEAL**: Uses LLMs to analyze captured credentials and PII, structure exfiltration, and select targets — treats the LLM as a live intelligence analyst

Traditional AV and EDR detection cannot match this because the malicious behavior is dynamically generated per-execution.

### 7. RAG Data Exfiltration

Attackers manipulating vector embeddings to force retrieval mechanisms to surface and leak proprietary data chunks. Covered separately in rag-pipeline-security skill.

### 8. Model Poisoning

Training pipeline targeting has moved beyond data injection to directly biasing model behavior. Supply chain logistics and classification systems that use ML models for decisions are at risk of subtle model poisoning that influences decisions in the attacker's favor over time.

**ATLAS ref:** AML.T0020 (Training Data Poisoning)

### 9. AI-Speed Reconnaissance

AI-assisted reconnaissance is observed at 36,000 probes per second per campaign. Traditional rate-based detection (100–1,000 req/s threshold alerts) does not fire at legitimate-looking distributed AI-directed probe rates until significant reconnaissance has already occurred.

### 10. LLM-Gateway Credential Theft as AI Attack Surface

**CVE-2026-42208** — BerriAI LiteLLM Proxy authorization-header SQL injection (CVSS 9.8 / CVSS v4 9.3 / CISA KEV-listed 2026-05-08, due 2026-05-29). LiteLLM is the open-source LLM-API gateway used in front of agent stacks, MCP-server fronts, and multi-model proxy deployments — exactly the trust hinge that this skill's threat-context section treats as the credential boundary for hosted-model use. The proxy concatenated an attacker-controlled `Authorization` header value into a SQL query in the error-logging path, so a single curl-able POST against `/chat/completions` with a SQL-injection payload returns the managed-credentials DB content without prior auth. Patched in 1.83.7+; temporary workaround `general_settings: disable_error_logs: true`. Any organisation whose AI attack-surface inventory treats the LLM gateway as "just a reverse proxy" misses that the gateway holds every downstream model-provider credential.

### 11. AI-Discovered + AI-Weaponized Supply-Chain Worms

**CVE-2026-45321** — Mini Shai-Hulud TanStack npm worm (CVSS 9.6, ~150M weekly downloads across 42 @tanstack/* packages, KEV-listed 2026-05-27). Disclosed 2026-05-11. The attack chain — Pwn-Request via `pull_request_target` on TanStack's bundle-size workflow, pnpm-store cache poisoning under the `actions/cache` key, and OIDC-token theft on the next main push — is engineering-grade and weaponizes three independently-benign primitives. While attribution (TeamPCP) records no AI-assisted exploit development for this specific instance, the worm pattern is exactly what AML.T0017-class capability development now produces at AI cadence: chained CI/CD primitives that no individual component owner recognises as exploitable. Treat the @tanstack/* surface as an exemplar of the broader AML.T0010 (AI Supply Chain Compromise) threat applied to JS toolchains that the AI assistant ecosystem depends on.

---

## Framework Lag Declaration

| Framework | Control | Why It Fails for AI Threats |
|---|---|---|
| NIST 800-53 | AC-2 (Account Management) | Controls account lifecycle for human users and service accounts. Does not address LLM agent identity, tool authorization, or prompt injection as an access control bypass. An attacker who injects a prompt that causes a model to call `delete_file()` bypasses AC-2 entirely — the API call is authorized by the model's service account, not the attacker's. |
| NIST 800-53 | SI-3 (Malicious Code Protection) | Designed for signature-based malware detection. PROMPTFLUX generates unique evasion code per execution by querying an LLM. SI-3 has no control surface for AI-generated dynamic malware. |
| NIST 800-53 | SI-10 (Information Input Validation) | Input validation for web forms and API endpoints. Does not address prompt injection, where the "input" is semantically legitimate text that contains adversarial instructions for the model. |
| ISO 27001:2022 | A.8.28 (Secure coding) | Secure coding practices for software development. No reference to AI/ML system security, prompt injection, or model integrity. |
| ISO 27001:2022 | A.8.30 (Outsourced development) | Third-party development controls. Does not address MCP server trust, unsigned manifests, or supply chain attacks on AI tool ecosystems. |
| SOC 2 | CC6 (Logical and Physical Access) | Access control via IAM, authentication, authorization. Prompt injection is an access control failure that routes around CC6 entirely — the authorized model account takes the action, not the attacker. Audit trails show the model's service account performed the action. |
| SOC 2 | CC7 (System Operations) | Anomaly detection for system operations. No guidance for AI API baseline, AI C2 detection, or PROMPTFLUX behavioral patterns. |
| PCI DSS 4.0 | 6.4.1 | Web application protection (WAF). WAFs operate on HTTP request/response patterns. They have no semantic understanding of prompt injection embedded in JSON `message` fields. |
| MITRE ATT&CK | Enterprise | Does not include prompt injection as a technique. AI-as-C2 (SesameOp) is not in ATT&CK as of mid-2026. ATLAS v2026.09 covers these but is not part of SOC detection engineering programs that are ATT&CK-mapped. |
| NIST AI RMF | MEASURE 2.5 | Measure AI risks during operation. Provides a framework for thinking about AI risk but no specific controls for prompt injection, MCP supply chain, or AI-as-C2. |
| EU NIS2 | Art. 21(2)(d) (supply-chain security) + Art. 21(2)(e) (security in acquisition, development and maintenance) | "Appropriate and proportionate" supply-chain language. Member-state transpositions (BSI IT-SiG 2.0, ANSSI) do not enumerate MCP servers or LLM API providers as in-scope supply-chain components. An essential entity can meet NIS2 supplier-management obligations with traditional SaaS vendor reviews while having zero coverage of AI-assistant tool ecosystems. |
| EU DORA | Art. 8 (ICT asset management) + Art. 28 (ICT third-party register) + Art. 30 (key contractual provisions) | Financial-entity ICT third-party language scoped to traditional ICT providers. LLM API providers acting as data processors for prompt content and developer-environment MCP servers are not enumerated as ICT third-party service providers. ESAs RTS on subcontracting (JC 2024/53) is silent on AI/ML SaaS dependency classes. |
| EU AI Act (Regulation 2024/1689) | Art. 15 (accuracy, robustness, cybersecurity) for high-risk AI + Art. 9 (risk management) | High-risk AI cybersecurity language refers to "state of the art" without naming prompt injection, MCP supply chain, or AI-as-C2 as scoped attack classes. Conformity assessments (Annex VI/VII) accept documentation completeness; harmonized standards (CEN-CENELEC JTC 21) through 2026-2027 may operationalize this. |
| UK NCSC CAF | Principle A4 (Supply Chain), B2 (Identity and Access Control), B4 (System Security), C1 (Security Monitoring) | Outcome-based language. NCSC's 2024 guidance on securing AI systems and the DSIT AI Cyber Code of Practice (2025) name the attack classes at the principle level (prompt injection, model supply chain, monitoring), but the CAF outcome statements are unchanged. An organisation achieves CAF outcomes at Achieved level with zero MCP-trust controls and zero prompt-injection detection. |
| UK DSIT AI Cyber Code of Practice (2025) | 13 principles for secure AI development and deployment | Principles-based. Names training-data integrity, model-deployment security, monitoring, and supply chain — but as principles, not testable controls. No technical floor for prompt-injection defence, MCP allowlisting, or AI-as-C2 detection. |
| AU ASD Essential 8 | Strategy: Application Control + User Application Hardening + Restrict Administrative Privileges | Application Control (allowlisting) covers what runs locally; it does not cover AI-assistant tool-use chains where the AI agent dynamically composes the executed action. None of the eight strategies address prompt injection, model supply chain, or LLM-as-C2 channel. |
| AU ASD ISM | ISM-2156, ISM-2157 and ISM-2158 (agentic AI: minimum tools, task-scoped authorization, retrieved content treated as untrusted) + ISM-1924 (prompt injection) + ISM-1452 (supply chain risk assessment) + ISM-1228 (event analysis) | The ISM names agentic AI directly, so the gap is narrower than a missing control. ISM-1452's supplier assessment gives no method for rating an LLM API or MCP server provider, and ISM-1228's event analysis has no indicator for AI API egress used as C2 or for an action a prompt injection coerced, because both produce ordinary, authorized traffic. |
| AU Voluntary AI Safety Standard (10 guardrails, 2024) | Guardrails 5 (test and monitor), 6 (transparency), 8 (record-keeping) | Voluntary, principles-language. Operationally identical to the UK DSIT AI Cyber Code lag — names the right concerns at the principle layer without testable controls for prompt injection, MCP trust, or AI-as-C2 detection. |
| AU APRA CPS 234 | Para 27 (information security capability proportional to vulnerabilities and threats) + APRA CPG 235 (managing data risk) | "Proportional" capability language. APRA-regulated entities deploying AI assistants meet CPS 234 attestation with traditional information-security capability; AI-specific attack surface is not an examined capability class. APRA Information Paper on AI (2024) names the risks at the supervisory level without altering CPS 234 obligations. |

---

## TTP Mapping (MITRE ATLAS v2026.09)

| ATLAS ID | Technique | Framework Coverage | Gap Description | Exploitation Example |
|---|---|---|---|---|
| AML.T0054 | LLM Jailbreak | Missing in all major frameworks | No control covers adversarial-instruction injection that bypasses guardrails and coerces the model into attacker-chosen actions | CVE-2025-53773 (GitHub Copilot YOLO-mode RCE) |
| AML.T0010 | AI Supply Chain Compromise | Partial (ISO A.8.30) | A.8.30 covers outsourced development; does not cover MCP server trust, package signing for AI tools | CVE-2026-30615 (Windsurf MCP) |
| AML.T0096 | AI Service API (C2) | Missing in all major frameworks | No framework has a control for AI API traffic as C2 channel | SesameOp campaign |
| AML.T0020 | Training Data Poisoning | Partial (NIST AI RMF) | NIST AI RMF identifies the risk; no specific technical control | Supply chain logistics model poisoning |
| AML.T0043 | Craft Adversarial Data | Partial (SI-10) | SI-10 covers web input validation; not semantic injection in LLM prompts | RAG vector manipulation |
| AML.T0051 | LLM Prompt Injection | Missing in all major frameworks | Zero controls in NIST, ISO, SOC 2, PCI for prompt injection | CVE-2025-53773, indirect injection via retrieved docs |
| AML.T0013 | Discover AI Model Ontology | Partial (awareness only) | No framework requires monitoring for adversary mapping of deployed model family, guardrail surface, or system-prompt structure via inference-API probing | Reconnaissance step preceding PROMPTSTEAL-class targeting; AML-model registry exposure |
| AML.T0017 | Develop Capabilities | Missing (misuse dimension) | Frameworks don't address adversary AI-assisted exploit development | Copy Fail AI discovery (41% of 2025 0-days) |
| AML.T0016 | Obtain Capabilities | Missing (misuse dimension) | Frameworks don't address adversary use of public AI APIs to craft malware/phishing payloads | PROMPTFLUX, PROMPTSTEAL, phishing generation |
| AML.T0018 | Manipulate AI Model | Partial (NIST AI RMF) | No technical control requirements for model integrity verification | Training pipeline poisoning |

---

## Exploit Availability Matrix

| Vulnerability | CVSS | RWEP | KEV | PoC | AI-Accelerated | Active Exploitation |
|---|---|---|---|---|---|---|
| CVE-2025-53773 (Copilot YOLO-mode RCE) | 7.8 | 30 | No | Yes — demonstrated | Yes (AI tooling enables) | Suspected |
| CVE-2026-30615 (Windsurf MCP local-vector RCE) | 8.0 | 35 | No | Partial | No | Suspected |
| SesameOp (AI C2 technique) | N/A | N/A | N/A | Yes (ATLAS documented) | Yes | Confirmed campaign |
| PROMPTFLUX family | N/A | N/A | N/A | Behavioral signatures | Yes | Active |
| PROMPTSTEAL family | N/A | N/A | N/A | Behavioral signatures | Yes | Active |

---

## Analysis Procedure

### Step 1: Inventory the AI surface

For the target environment, identify:
- Which LLM APIs are in use? (OpenAI, Anthropic, Google, Azure OpenAI, local models)
- Which AI coding assistants are deployed? (GitHub Copilot, Cursor, Windsurf, Claude Code, Gemini CLI)
- Which MCP servers are installed? (list via IDE settings or `~/.cursor/mcp.json`, `~/.vscode/mcp.json`)
- Does any application take user input and include it in an LLM prompt without semantic sanitization?
- Does any application use RAG? (vector store + retrieval)
- Are any AI model APIs accessible from the internet?
- What service accounts do AI agents run under? What permissions do those accounts have?

### Step 2: Assess prompt injection exposure

For each system that feeds external content into LLM prompts:

**Injection surface score:**
- External content in prompts (user input, documents, emails, web content, PR descriptions): +High
- LLM has tool use / function calling capability: +Critical multiplier
- LLM can take actions on behalf of users (file ops, API calls, code execution): +Critical multiplier
- No semantic input sanitization: +High
- No output monitoring: +Medium
- Attack success rate against SOTA defenses: 85%+ (meta-analysis baseline)

**Current defense adequacy:**
- Prompt injection classifiers reduce success rate; do not eliminate it
- System prompt hardening reduces success rate; does not eliminate it
- No defense achieves <15% bypass rate against adaptive adversaries (2026 data)
- Defense-in-depth is the only viable strategy: minimize tool permissions + monitor outputs + rate-limit + log all prompts

### Step 3: Assess MCP trust posture

For each installed MCP server:
- Is the server package signed? Verify manifest signature.
- Is there an explicit tool allowlist? (`allowed_tools` in MCP client config)
- Does the MCP server require authentication? (bearer token or equivalent)
- What permissions does the MCP server's process run with?
- Are MCP server outputs sanitized before returning to the model?

**MCP risk score:**
- Unsigned server + no allowlist + no auth: Critical
- Signed server + allowlist + bearer auth: Low-Medium
- Any MCP server with filesystem or shell access + unsigned: Critical

### Step 4: Assess AI C2 exposure

Check for SesameOp-style C2 indicators:
- Are AI API calls logged with full prompt + response content?
- Is there a behavioral baseline for normal AI API usage per host/user/process?
- Do alert thresholds exist for unusual AI API call patterns?
- Are AI API calls correlated with other host activity (file access, lateral movement)?
- Is high-entropy content in prompt fields flagged?

### Step 5: Assess credential/phishing risk

For organizations with AI-generated phishing threat:
- Have phishing detection systems been updated for AI-generated content? (grammar checks are inadequate)
- Are behavioral signals (link patterns, sender reputation, context anomalies) the primary detection mechanism?
- Is MFA resistant to phishing (hardware key or passkey)? SMS/TOTP are vulnerable to AI-generated real-time phishing.

### Step 6: Generate framework gap report

For each identified risk, declare the framework gap:
- Which control nominally applies?
- Why it is insufficient for this specific AI attack pattern?
- What a real control would require?

---

## Output Format

The assessment produces a structured AI Attack Surface Assessment report. The shape below is consumed downstream by `mcp-agent-trust` (which converts the MCP Trust Assessment section into per-server policy), by `rag-pipeline-security` (which picks up any RAG-pipeline entries from the Surface Inventory), and by `incident-response-playbook` (which scopes IR against the prompt-injection and AI-C2 exposure bands). CSAF-style auditor evidence bundles consume the Framework Gaps and ATLAS TTP Coverage Gaps sections verbatim — preserve the framework-control IDs as cited.

```
## AI Attack Surface Assessment

**Assessment Date:** YYYY-MM-DD
**Scope:** [systems/applications assessed]

### Surface Inventory
| Component | Type | External Input | Tool Use | Risk Level |
|-----------|------|---------------|----------|------------|
| [name] | [LLM app / MCP server / coding assistant] | [Yes/No] | [Yes/No] | [Critical/High/Medium/Low] |

### Prompt Injection Exposure
[Per component: injection surface score, current defenses, estimated bypass rate, recommended controls]

### MCP Trust Assessment
[Per installed MCP server: signed/unsigned, allowlist status, auth status, risk level]

### AI C2 Indicators
[Logging coverage, baseline status, detection gaps]

### Credential/Phishing Risk
[Detection system currency, MFA phishing resistance]

### ATLAS TTP Coverage Gaps
[Per TTP: covered/partial/missing in deployed security tools]

### Framework Gaps
[Per framework in scope: specific controls that fail for AI threats, with explanation]

### Prioritized Recommendations
[Ordered by RWEP impact: specific, actionable, accounts for real deployment constraints]
```

---

## Defensive Countermeasure Mapping

D3FEND v1.3.0+ references from `data/d3fend-catalog.json`. The AI attack surface enumerated above lands on five primary defensive techniques. Each entry below identifies which ATLAS TTP class the countermeasure addresses and the defense-in-depth layer it occupies.

| D3FEND ID | Name | Layer | Rationale (what it counters here) |
|---|---|---|---|
| `D3-IOPR` | Input/Output Profiling | SDK / application | SDK-level prompt and completion inspection — the foundational control for AML.T0051 (prompt injection), AML.T0096 (LLM C2), AML.T0054 (jailbreak). Without per-call I/O profiling, every detection step below is degraded. |
| `D3-CSPP` | Client-server Payload Profiling | LLM / MCP gateway | Gateway-layer inspection of tool-call args and prompt/completion bodies. Necessary when the AI client (mobile app, browser extension, IDE) cannot host `D3-IOPR` instrumentation in-process — the gateway becomes the only content-aware control. |
| `D3-EAL` | Executable Allowlisting | Endpoint / managed host | Restricts which AI-tool binaries (IDE assistants, browser extensions, MCP servers) can execute on managed endpoints. Direct counter to AML.T0010 (ML supply-chain compromise) for tooling shipped as native binaries; precondition for managed-endpoint clipboard- and code-completion controls. |
| `D3-FAPA` | File Access Pattern Analysis | Endpoint / data tier | Detects RAG-corpus and training-data abuse by pattern-matching the file-access shape of AML.T0018 (model poisoning at training time) and AML.T0020 (RAG retrieval abuse). Anchors the data-tier defence against poisoning that prompt-layer controls cannot see. |
| `D3-NTA` | Network Traffic Analysis | Network egress | Per-identity baseline of model-API and MCP-server egress. Catches the AML.T0016 generative-AI misuse pattern (PROMPTFLUX-style rapid querying) and the AML.T0096 covert-C2 destination shape when SDK instrumentation is partial or missing. |

**Defense-in-depth posture:** `D3-EAL` is the prerequisite endpoint layer (only sanctioned AI clients run); `D3-FAPA` is the data-tier layer (RAG and training corpora); `D3-IOPR` and `D3-CSPP` are the content-aware application and gateway layers; `D3-NTA` is the network-observability backstop. Skills that recommend a single layer alone are flagged as incomplete during Analysis Procedure Step 7.

**Least-privilege scope:** every AI principal (human developer, agent identity, MCP server) has the minimum set of model-API, MCP-tool, and RAG-corpus authorisations required for its sanctioned use case. `D3-EAL` allowlists are per-host-class (developer ≠ production ≠ CI); `D3-FAPA` access-pattern baselines are per-corpus-per-principal; `D3-IOPR` logs include the principal identity on every prompt/completion pair.

**Zero-trust posture:** every prompt is verified content-shape and origin-identity before downstream tool invocation; every RAG retrieval is clearance-checked at retrieval time (not just at index time); every MCP tool call has its args inspected at the gateway before reaching the tool. No "trusted prompt" exemption — AML.T0051 indirect prompt injection enters via documents and tool outputs, not just user prompts.

**AI-pipeline applicability:** `D3-EAL` is not applicable to serverless inference endpoints (no executable to allowlist on the consumer side). The scoped alternative is `D3-CSPP` at the gateway plus signed-image attestation at the provider — the model-serving container is the executable surface, and its provenance is the prerequisite. `D3-FAPA` on ephemeral RAG indices degrades to per-query retrieval logging (`D3-IOPR`) plus index-build provenance signed at construction.

---

## Compliance Theater Check

> "Your security awareness training includes phishing detection. 82.6% of phishing emails now contain AI-generated content indistinguishable by grammar or style checks. Open your most recent phishing simulation report: what percentage of simulated phishes used AI-generated content? If zero, the simulation is testing resistance to 2021 phishing, not 2026 phishing. If your detection rule set has not been updated to reflect AI-generated content as the baseline, the control is theater for the threat it claims to address."

> "Your access control logs show no unauthorized access events involving your AI systems. Run this check: are your AI agent service account API calls logged with full request/response bodies? Are those logs monitored for behavioral anomalies? If AI API traffic is treated as trusted internal traffic with no behavioral monitoring, an attacker using AI-as-C2 (SesameOp technique) would not appear in your unauthorized access event log at all. Absence of evidence is not evidence of absence when the detection surface doesn't exist."
