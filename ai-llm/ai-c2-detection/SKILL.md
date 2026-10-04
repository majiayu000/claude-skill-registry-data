---
name: ai-c2-detection
version: "1.0.0"
description: Detect adversary use of AI APIs as covert C2 — SesameOp pattern, PROMPTFLUX/PROMPTSTEAL behavioral signatures, response playbook
triggers:
  - ai c2
  - ai command and control
  - sesameop
  - promptflux
  - promptsteal
  - ai api abuse
  - llm c2
  - covert channel ai
  - aml.t0096
data_deps:
  - cve-catalog.json
  - d3fend-catalog.json
  - framework-control-gaps.json
  - rfc-references.json
atlas_refs:
  - AML.T0096
  - AML.T0016
attack_refs:
  - T1071
  - T1102
  - T1568
framework_gaps:
  - NIST-800-53-SI-3
  - NIST-800-53-SC-7
  - ISO-27001-2022-A.8.16
  - SOC2-CC7-anomaly-detection
  - NIS2-Art21-incident-handling
  - UK-CAF-C1
  - AU-Essential-8-App-Hardening
cwe_refs:
  - CWE-918
rfc_refs:
  - RFC-8446
  - RFC-9180
  - RFC-9458
  - RFC-9421
  - RFC-9114
  - RFC-9000
d3fend_refs:
  - D3-CA
  - D3-CSPP
  - D3-DA
  - D3-IOPR
  - D3-NI
  - D3-NTA
  - D3-NTPM
last_threat_review: "2026-09-18"
---

# AI C2 Detection

## Threat Context (mid-2026)

The AI-as-adversary reality that motivates this skill is now operationally documented: 41% of 2025 zero-days were AI-discovered (GTIG 2025), the first AI-built in-the-wild zero-day was confirmed 2026-05-11 (GTIG AI 2FA-bypass case), and Fragnesia (CVE-2026-46300, 2026-05-13) is the canonical AI-driven autonomous-discovery anchor — Zellic's agentic auditor surfaced an 18-year-old Linux kernel primitive. C2 channels riding the same agentic AI infrastructure are the next logical step; CTID Secure AI v2 (2026-05-06, replaces v1) treats AI-API C2 detection as an in-scope control class.

### SesameOp — AI APIs as Covert C2 (ATLAS AML.T0096)

The SesameOp campaign documented a technique that has since been replicated and expanded: adversaries repurposing legitimate AI agent APIs as covert command-and-control channels.

**Technical pattern:**
```
Compromised host                    Attacker
      |                                |
      |  POST /v1/messages             |
      |  {"messages": [                |
      |    {"role": "user",            |
      |     "content": "b64:<cmd>"}    |  ← Command encoded in prompt
      |  ]}                            |
      |                                |
      |  {"choices": [{                |
      |    "message": {                |
      |     "content": "b64:<data>"}   |  ← Exfiltrated data in completion
      |  }]}                           |
      |                                |
```

The malware on the compromised host:
1. Encodes commands/exfiltrated data as base64 or other encoding within semantically valid text
2. Sends "legitimate-looking" API calls to OpenAI, Anthropic, Google, or Azure AI endpoints
3. Receives attacker instructions encoded in the AI's response
4. The AI API is simply relaying encoded content — it is not the attacker's infrastructure, it's the transport

**Why traditional C2 detection fails:**
- No DGA (domain generation algorithm): the endpoint is a legitimate, well-known AI service
- No unusual TLS certificates: certs belong to OpenAI/Anthropic/Google
- No beaconing pattern: AI API calls are bursty and aperiodic, indistinguishable from legitimate developer usage
- No payload size anomaly in the traffic layer: prompt + completion sizes vary widely for legitimate workloads
- No protocol anomaly: standard HTTPS REST API calls
- No reputation signal: blocking the endpoint blocks legitimate AI usage

The only detection surfaces are:
1. Behavioral: does this host/process/user normally make AI API calls? Is the pattern consistent with legitimate usage?
2. Content: is the prompt/completion content encoded or high-entropy? (requires TLS inspection)
3. Correlation: do AI API calls correlate with file access, lateral movement, or other attack-indicative activity?
4. Process: what process is making the AI API call? Is it expected to use AI APIs?

---

### PROMPTFLUX Malware Family

PROMPTFLUX is a malware family that queries public LLMs during execution to generate novel evasion code in real-time.

**Execution pattern:**
1. Initial compromise via standard delivery (phishing, exploit)
2. Malware runs, hits an AV/EDR detection signal
3. Queries a public LLM: "Generate functionally equivalent code to [detected snippet] using different variable names and control flow that doesn't match common malware patterns"
4. LLM returns new variant
5. Malware re-deploys with new variant, bypassing static signatures
6. Repeat indefinitely

**Detection signature (behavioral, not content):**
- A process making repeated AI API calls during or immediately after security product alerts
- AI API calls from processes that are not known AI-using applications (e.g., a Chrome extension making calls to OpenAI, or a background service with no UI making API calls)
- LLM query content containing: code snippets, function names, API patterns that would be unusual for conversational use

**Why SI-3 (Malicious Code Protection) fails:**
SI-3 requires malicious code protection mechanisms that "detect and eradicate malicious code." PROMPTFLUX generates unique code per detection event. There is no signature to detect, because every variant is novel. SI-3 provides zero protection against AI-generated dynamic evasion.

---

### PROMPTSTEAL Malware Family

PROMPTSTEAL uses LLMs as live intelligence analysts for exfiltration targeting.

**Execution pattern:**
1. Compromise host, gain access to credential stores, user files, and email
2. Query LLM: "Given this list of files and email subjects, which files are most likely to contain credentials or sensitive business information?"
3. LLM prioritizes the exfiltration target list
4. Exfiltrate prioritized targets
5. Query LLM: "Given these captured credentials for [company], what systems are most likely accessible with these credentials?"
6. LLM provides lateral movement guidance

**PROMPTSTEAL turns a commodity compromise into a targeted, prioritized attack** without requiring any attacker-side human intelligence work. The LLM is doing the targeting, prioritization, and strategy work.

**Detection:**
- AI API calls from processes with access to sensitive file paths or credential stores
- AI prompts containing filenames, email subjects, or data that could be used for targeting
- Unusual AI API usage from processes associated with file scanning or credential access patterns

---

## Framework Lag Declaration

| Framework | Control | Why It Fails |
|---|---|---|
| NIST 800-53 SI-3 | Malicious Code Protection | Signature/behavioral detection for known malware. AI-generated dynamic evasion (PROMPTFLUX) produces unique code per execution. Zero signature coverage. |
| NIST 800-53 SC-7 | Boundary Protection | Egress controls block unauthorized destinations. AI API endpoints (api.openai.com, api.anthropic.com, generativelanguage.googleapis.com) are not unauthorized — they are commonly whitelisted for legitimate use. SC-7 cannot distinguish C2 traffic from legitimate AI API usage at the network layer. |
| NIST 800-53 SI-4 | System Monitoring | Monitor for attacks and indicators of attack. Current SI-4 implementations don't baseline AI API usage per process or alert on high-entropy prompt content. |
| ISO 27001:2022 A.8.16 | Monitoring Activities | Monitoring of systems, networks, and applications. No guidance for AI API behavioral baseline, no mention of AI traffic as a monitoring concern. |
| SOC 2 CC7 | System Operations (Anomaly Detection) | Detect and respond to security events. CC7 implementations baseline network traffic and system events. AI API calls are typically in the same anomaly detection blind spot as other SaaS traffic. |
| ATT&CK T1071 | Application Layer Protocol | ATT&CK documents C2 over application protocols. AI API as C2 fits the technique but detection guidance doesn't address legitimate-endpoint C2 specifically. |
| EU NIS2 | Art. 21(2)(b) (incident handling) + Art. 21(2)(g) (network and information systems security including monitoring) | "Appropriate and proportionate" monitoring language. Member-state transpositions (BSI IT-SiG 2.0, ANSSI, ENISA) do not enumerate AI-API egress baselining as an expected monitoring control. An essential entity meets the NIS2 monitoring obligation with traditional SIEM coverage while leaving AI-as-C2 entirely undetected. |
| EU DORA | Art. 10 (detection) + Art. 17 (ICT-related incident management) | Detection obligation for financial entities. RTS on threat-led penetration testing (TIBER-EU JC 2024/40) does not include AI-as-C2 scenarios in the TT&P inventory as of mid-2026. CBEST / iCAST scenario libraries lag by 12-18 months. |
| EU AI Act (Regulation 2024/1689) | Art. 15 (cybersecurity for high-risk AI systems) + Art. 72 (post-market monitoring) | High-risk AI cybersecurity language addresses adversarial robustness and integrity of the AI system itself. AI APIs being abused as a C2 channel by non-AI malware is outside the scoped attack surface — providers do not log per-prompt to detect attacker use, and operators have no mandated detection control for legitimate-endpoint C2. |
| UK NCSC CAF | Principle C1 (Security Monitoring) + Principle C2 (Proactive Security Event Discovery) | Outcome-based monitoring language. NCSC's 2024 guidance on monitoring egress to SaaS APIs recommends behavioural baselining but the CAF outcome statements are satisfied by traditional endpoint and network monitoring. An organisation can meet C1 / C2 at Achieved level with zero AI-API egress baselining. |
| UK NCSC Cyber Assessment Framework — sectoral profiles (Telecoms Security Code of Practice, Energy CAF profile) | Sector-specific monitoring obligations | Sectoral CAF profiles inherit C1/C2 outcomes; none enumerate AI API egress as an in-scope monitored channel. Telecoms operators meeting the TSA 2021 Code monitoring obligations have the same blind spot. |
| AU ASD Essential 8 | Strategy: Application Control + User Application Hardening | Application Control (allowlisting) covers what runs locally; it does not cover what allowed applications connect to. A whitelisted browser or IDE making AI API calls passes Application Control while operating as a C2 channel. Essential 8 does not include an egress-control strategy. |
| AU ASD ISM | ISM-1228 (event analysis) + ISM-1416 (software firewall restricting outbound connections) + ISM-2159 (agentic AI tool invocations and external requests centrally logged) | ISM-1416 restricts outbound connections to approved applications and services, and an AI API is usually approved, so traffic to it passes. ISM-2159 logs what an organization's own agents send, not what malware on the host sends to the same API. ISM-1228 event analysis has no indicator that separates an attacker's prompts from legitimate use of a trusted vendor. |
| AU APRA CPS 234 | Para 27(b) (capability to detect and respond to information security incidents in a timely manner) | "Timely" detection capability. APRA CPS 234 attestations are satisfied by SIEM/SOC capability over traditional indicators. AI-as-C2 detection capability is not a CPS 234 examined control. |

---

## Detection Architecture

### Layer 1: Process-Level Behavioral Baseline

Build a model of which processes are expected to make AI API calls on each host type.

**Expected AI API callers by host type:**

| Host Type | Expected AI API Callers |
|---|---|
| Developer workstation | IDE processes (cursor, code), terminal sessions, browser |
| CI/CD runner | Build tools if AI-assisted (specific known tools only) |
| Production server | Application processes if AI features are deployed (specific, named) |
| User workstation (non-dev) | Browser, Office productivity suite (if AI features enabled) |
| Database server | None expected |
| Network device | None expected |

**Alert conditions:**
- AI API calls from processes not on the expected list for that host type
- AI API calls from system services or background processes
- AI API calls at unusual hours relative to the user's normal working pattern
- Spike in AI API call frequency from a single process (PROMPTFLUX's rapid querying pattern)

### Layer 2: Behavioral Correlation

Correlate AI API calls with other security-relevant events on the same host:

```
AI API call + file_access(sensitive_path) within 5 minutes → ALERT
AI API call + credential_access event within 5 minutes → ALERT  
AI API call + network_scan event within 10 minutes → ALERT
AI API call + security_alert event within 1 minute → HIGH ALERT (PROMPTFLUX pattern)
AI API call + large_file_transfer within 10 minutes → ALERT (PROMPTSTEAL exfil)
```

### Layer 3: Traffic Content Analysis (requires TLS inspection)

If TLS inspection is deployed at the boundary:

**High-entropy content detection:**
- Calculate entropy of the `content` field in AI API requests/responses
- Flag: entropy > 6.5 bits/byte in prompt content (suggests encoding)
- Flag: base64 patterns in prompt/completion content that aren't image data
- Flag: prompt content containing recognizable file paths, usernames, or credential patterns

**Prompt pattern matching:**
- Flag: prompts containing code snippets + requests for "equivalent" or "alternative" implementations
- Flag: prompts listing filenames, email subjects, or asking for prioritization of sensitive data
- Flag: prompts requesting "code that avoids detection" or equivalent phrasing

### Layer 4: Response Monitoring

Monitor AI API responses for anomalous patterns:
- Responses containing executable code when the calling application has no known code-generation use case
- Responses containing lateral movement guidance (lists of systems, exploitation advice)
- Large response volumes from processes that normally produce small queries

---

## Incident Response Playbook — AI C2

### Detection trigger

Any of these triggers:
- Process-level anomaly: unexpected process making AI API calls
- Behavioral correlation: AI API call + security-relevant event correlation
- Content alert: high-entropy or encoded content in AI API traffic
- Threat intel match: C2 infrastructure or campaign IOC matches observed AI API destination

### Triage (0–30 minutes)

1. Identify the process making AI API calls
2. Check process legitimacy: is this a known application? Signed binary? Expected on this host?
3. Review call timing: when did these calls start? What changed on the host before?
4. Pull the last 100 API calls (prompt + response content if TLS inspection is available)
5. Check for file access and credential access events correlated in time

### Investigation (30 minutes – 4 hours)

1. If TLS inspection available: export prompt/response content for analysis
   - Decode any base64 or encoded content
   - Check prompts for: code rewrite requests (PROMPTFLUX), targeting/prioritization requests (PROMPTSTEAL), encoded commands (SesameOp)
2. Timeline reconstruction: what did this process do before and after AI API calls?
3. Lateral movement check: have other hosts shown AI API behavioral anomalies?
4. Exfiltration check: did any data leave the network via AI API responses?

### Containment

1. Block AI API destinations at the boundary for the affected host/process (scoped to minimize business disruption)
2. Preserve: full packet capture of AI API traffic from affected host, process memory dump if feasible, file system timeline
3. Rotate: credentials that may have been accessed by PROMPTSTEAL pattern
4. Isolate: host if lateral movement is confirmed or suspected

### Evidence Handling

AI API traffic logs (prompt + response) are primary evidence. Preserve:
- Network flow records (timestamps, volumes, endpoints)
- TLS inspection logs (full content if captured)
- Process execution logs
- File access logs correlated with AI API call timeline
- Credential access events

### Attribution

Map observed TTPs to:
- SesameOp campaign indicators if C2 pattern matches
- PROMPTFLUX indicators if code rewrite requests observed
- PROMPTSTEAL indicators if targeting/prioritization pattern observed
- Novel campaign if pattern doesn't match known families — document as new indicator

---

## Detection Rule Examples

### Sigma-style rule — PROMPTFLUX

```yaml
title: PROMPTFLUX Pattern - AI API Call Following Security Alert
status: experimental
logsource:
  product: endpoint
  service: process
detection:
  condition: ai_api_call and security_alert within 60s
  ai_api_call:
    TargetHostname|contains:
      - 'api.openai.com'
      - 'api.anthropic.com'
      - 'generativelanguage.googleapis.com'
      - 'api.cohere.ai'
  security_alert:
    EventID: [1116, 1117]  # Windows Defender alert example
timeframe: 60s
falsepositives:
  - Developer using AI assistant to investigate security alert (verify by user identity)
level: high
```

### Sigma-style rule — Unexpected AI API Origin

```yaml
title: AI API Call from Unexpected Process
status: experimental
logsource:
  product: network
  service: dns
detection:
  condition: ai_domain and not expected_process
  ai_domain:
    dns_query|contains:
      - 'api.openai.com'
      - 'api.anthropic.com'
  expected_process:
    ProcessName|contains:
      - 'Code.exe'
      - 'Cursor.exe'
      - 'chrome.exe'
      - 'msedge.exe'
falsepositives:
  - New AI-using applications deployed — update allowlist
level: medium
```

---

## TTP Mapping (MITRE ATLAS v2026.09 + MITRE ATT&CK)

| ID | Source | Technique | C2 Relevance | Gap Flag — Which Detection Control Fails |
|---|---|---|---|---|
| AML.T0096 | ATLAS v2026.09 | AI Service API (LLM API as covert C2) | Direct: SesameOp encodes commands and exfiltrated data in prompt and completion fields against api.openai.com, api.anthropic.com, generativelanguage.googleapis.com. AI provider domain is the relay, not the attacker C2 endpoint. | NIST-800-53-SC-7 (Boundary Protection) — AI provider domains are allowlisted in most enterprise egress for legitimate developer and product use, so boundary inspection cannot distinguish benign developer prompts from C2-encoded prompts. See SC-7 entry in `data/framework-control-gaps.json` — real requirement is SDK-level prompt logging with identity binding, anomaly detection on prompt-shape and token-volume, and an allowlist that enumerates the sanctioned business reason per identity. Boundary-only SC-7 evidence is incomplete for any org with AI API access in production. |
| AML.T0016 | ATLAS v2026.09 | Obtain Capabilities (generative AI): adversary use of public inference APIs to generate or refine malware, evasion and phishing payloads | PROMPTFLUX queries public LLMs to generate per-execution evasion code, and PROMPTSTEAL uses LLMs to prioritize exfiltration targets. Both consume public LLMs as a real-time capability service, so the inference API does weaponization work for the adversary. | NIST-800-53-SI-3 fails because there is no static signature for code a public LLM generates per event. NIST-800-53-SI-4 fails as commonly deployed because there is no AI-API behavioral baseline per process or identity. SC-7 boundary control treats the AI provider as allowlisted SaaS. |
| T1071 | ATT&CK | Application Layer Protocol (C2) | AI C2 traffic is standard HTTPS REST to api.openai.com or equivalent. Application-protocol C2 detection that looks for DGA, unusual TLS, or beaconing does not fire. | SC-7 boundary control sees only the destination domain (allowlisted) — no protocol anomaly to alert on. Detection requires identity-bound prompt content inspection, which SC-7 as written does not require. |
| T1102 | ATT&CK | Web Service (C2 via legitimate web service) | AI API endpoints are exactly the "legitimate web service used as C2" pattern that T1102 describes — but at scale and pre-allowlisted in nearly every enterprise. | SOC 2 CC7 anomaly-detection control: AI API traffic shares the SaaS blind spot — typically not baselined per process or identity. ISO 27001 A.8.16 monitoring activities: no guidance for AI-API-shaped traffic. |
| T1568 | ATT&CK | Dynamic Resolution | AI provider responses can carry encoded instructions that dynamically determine the next-hop behaviour for the malware (effectively model-mediated dynamic resolution of the next attacker instruction). | No standard DNS-tunnelling or DGA detection applies — the "resolution" happens inside an HTTPS payload to a trusted endpoint. SC-7 cannot see it without SDK-level prompt + response logging. |

---

## Exploit Availability Matrix

The threats in this skill are adversary TTPs and malware families rather than vendor vulnerabilities, so they carry no CVE IDs in `data/cve-catalog.json`. Public incident reports and ATLAS `real_world_instances` are the primary evidence base.

| Threat | CVE? | Public Incident Reporting / PoC | CISA KEV? | AI-Accelerated? | EDR / SIEM Detection Support (mid-2026) | AI Provider Abuse Signal Available? |
|---|---|---|---|---|---|---|
| SesameOp (AML.T0096) | No — adversary TTP, not vendor vuln | Yes — public campaign write-ups; ATLAS AML.T0096 lists SesameOp under `real_world_instances` | No (technique class; KEV catalogs vendor vulns only) | Yes — the entire technique is AI-API-mediated | Minimal — most EDR and SIEM products do not baseline AI API calls per process/identity or inspect prompt/response content. A handful of vendors ship experimental rules; coverage is fragmentary. | Partial — OpenAI, Anthropic, and Google publish aggregate abuse and policy-violation reports; per-tenant, per-request abuse telemetry that an enterprise SOC can subscribe to is not generally available as of 2026-05. |
| PROMPTFLUX | No — adversary malware family | Yes — public reporting documenting LLM-mediated evasion code generation per execution | No | Yes — every variant is AI-generated; the technique is AI by definition | Minimal at signature layer (zero signatures by design). Behavioural detection (AI API call within 60s of an AV/EDR alert from an unexpected process) is feasible but not shipped out-of-the-box in major EDRs. | None enterprise-subscribable; AI provider abuse teams act on their own telemetry. |
| PROMPTSTEAL | No — adversary malware family | Yes — public reporting on LLM-assisted exfiltration prioritisation and lateral-movement guidance | No | Yes — LLM is acting as the adversary's live intelligence analyst | Minimal — requires correlation of AI API calls with credential-access and file-access events. Possible to build in a SIEM; not a default rule pack. | None enterprise-subscribable. |
| AI C2 — generic (T1071 / T1102 / T1568 over AI APIs) | No | Yes — research and red-team demonstrations across all major AI providers | No | Yes | Minimal — boundary controls treat AI provider domains as allowlisted SaaS; content-layer inspection requires TLS interception plus SDK-level prompt logging, which most orgs do not run. | Partial / inconsistent across providers. |

**Interpretation:** there is no patch to apply because there is no vendor CVE for the SesameOp / PROMPTFLUX / PROMPTSTEAL class. Mitigation is detection-architectural: SDK-level prompt logging with identity binding, AI-API behavioural baselining per process, correlation with credential/file/scan events, and an explicit allowlist that enumerates the sanctioned business reason per identity (per the SC-7 real_requirement in `data/framework-control-gaps.json`).

### LLM-Gateway Credential Theft as an AI-C2 Adjacent Class

**CVE-2026-42208** — BerriAI LiteLLM Proxy Authorization-header SQL injection (CVSS 9.8 / CVSS v4 9.3 / CISA KEV-listed 2026-05-08, federal due 2026-05-29; in-wild exploitation evidence). LiteLLM is the open-source LLM-API gateway used in front of agent stacks, MCP-server fronts, and multi-model proxy deployments — exactly the egress hinge this skill's detection architecture treats as the credential boundary for hosted-model use. The proxy concatenated an attacker-controlled `Authorization` header value into a SQL query in the error-logging path, so a curl-able POST against `/chat/completions` with a SQL-injection payload returns the managed-credentials DB content without prior auth. Patched in 1.83.7+; temporary workaround `general_settings: disable_error_logs: true`. Detection-relevance for this skill: an AI-API egress baseline that records only outbound destinations misses the *inbound* SQL injection on the proxy itself; pair `D3-IOPR` (SDK-level prompt logging) with `D3-CSPP` payload profiling on the gateway's inbound request stream. Any organisation whose AI-API egress visibility treats the LLM gateway as "just a reverse proxy" will discover post-breach that the gateway held every downstream model-provider credential and was the actual covert exfiltration channel.

### RFC Transport Reality

AI provider egress is TLS 1.3 (RFC 8446) terminated at the provider, so boundary inspection at the enterprise edge does not yield prompt content; Encrypted Client Hello uses RFC 9180 (HPKE), and for ECH-enabled connections even the destination hostname is hidden from boundary inspection. Oblivious HTTP (RFC 9458, January 2024) is a published-standard covert-channel candidate — every AI request gets relayed, so the visible destination is the relay rather than the AI provider, and SC-7 boundary tooling vendors are 12–18 months behind on detection guidance for this class. AI providers increasingly serve over HTTP/3 (RFC 9114) on QUIC (RFC 9000); enterprise NGFW HTTP/3 inspection coverage as of mid-2026 is uneven, with many boundary stacks default-denying QUIC or falling back to passive observation. HTTP Message Signatures (RFC 9421) are how AI providers publish abuse signals via webhook, and subscribing requires verifying these signatures. See `data/rfc-references.json` for the canonical entries rather than restating content here.

---

## Analysis Procedure

### Step 1: Enumerate AI API egress destinations from the last 30 days

Pull from the boundary or SaaS-egress logs all connections to:
- `api.openai.com`, `api.anthropic.com`, `generativelanguage.googleapis.com`, `api.cohere.ai`, regional Azure OpenAI endpoints (`*.openai.azure.com`), AWS Bedrock endpoints (`bedrock-runtime.*.amazonaws.com`), and any internal AI gateway.

For each destination, record: source identity (user, service account, machine account), source process where available, request volume, request times, and whether the calling host is a developer workstation, a CI runner, a production server, or another class.

### Step 2: Cross-reference each calling identity against a sanctioned business reason

For each identity making AI API calls, answer: is there a documented business reason for this identity to call AI APIs? Examples of sanctioned reasons: named developer using an AI IDE, named product using a named AI feature, named CI tool with an AI-assist component. Identities making AI API calls without a sanctioned business reason are the first investigation tier — they map directly to the SC-7 gap (allowlist without per-identity business reason is theater).

### Step 3: Flag prompts with anomalous shape

Requires SDK-level prompt logging or TLS inspection. For each request, compute:
- Token volume vs. that identity's rolling baseline. Outliers above the 99th percentile are flagged.
- Time-of-day vs. that identity's documented working pattern. Off-hours calls from human-developer identities are flagged.
- Linguistic shape: prompts that are not natural language (high entropy, base64, hex, or structured token streams that do not match a known schema) are flagged. PROMPTFLUX and SesameOp both produce non-conversational prompt shapes.
- Repeated identical or near-identical prompt structures from the same identity over short windows — consistent with automated C2 polling.

### Step 4: Check for SesameOp signature shape

Specifically inspect for the SesameOp pattern: OpenAI Assistants API used with a deterministic system-prompt pattern and prompt/completion bodies carrying encoded payloads. Indicators include: a fixed system prompt that does not vary across sessions, completions containing base64 or other encodings exceeding 64 bytes, and a request cadence that is bursty but persistent across hours/days without an obvious developer-session correlation. Cross-reference identity from Step 2 — SesameOp on a service account with no sanctioned AI use is a high-confidence finding.

### Step 5: Verify SDK-level prompt logging is enabled

If SDK-level prompt logging is off, the org cannot detect AI C2 at all — Steps 3 and 4 produce empty results regardless of whether C2 is occurring. Confirm, per AI SDK in use:
- Is full prompt content logged with identity binding?
- Is full completion content logged with identity binding?
- Are logs retained long enough for incident investigation (minimum 90 days)?
- Are logs forwarded to the SIEM or detection platform?

If any answer is "no," the org's AI-C2 detection coverage is structurally zero for that SDK, and that finding is itself the most important output of this analysis.

### Step 6: Correlate AI API calls with security-relevant host events

For each flagged identity from Steps 2–4, pull the corresponding host-event timeline from EDR/sysmon: file access (especially credential stores and sensitive paths), process creation, network scans, lateral movement indicators, AV/EDR alerts. Apply the correlation windows from the Detection Architecture section (file access within 5 minutes, security alert within 1 minute — PROMPTFLUX pattern, large transfer within 10 minutes — PROMPTSTEAL pattern).

### Step 7: Produce findings

For every identity flagged in Step 2, every prompt flagged in Step 3, every SesameOp shape match in Step 4, and every correlation in Step 6, write a finding mapped to AML.T0096 / AML.T0016 / T1071 / T1102 / T1568 with the specific evidence and the SC-7 / SI-3 / SI-4 / CC7 / A.8.16 gap that allowed it to land.

---

## Defensive Countermeasure Mapping

D3FEND v1.3.0+ references from `data/d3fend-catalog.json`. Maps the SesameOp / PROMPTFLUX / PROMPTSTEAL detection surfaces to the defense-in-depth layer they actually live on.

| D3FEND ID | Name | Layer | Rationale (what it counters here) |
|---|---|---|---|
| `D3-NTA` | Network Traffic Analysis | Network egress | Establishes the AI-provider-egress baseline (per-identity volume, cadence, time-of-day) that SesameOp's persistent bursty-but-aperiodic shape violates. Primary detection control when SDK-level prompt logging is absent. |
| `D3-NTPM` | Network Traffic Policy Mapping | Network egress | Per-identity sanctioned-business-reason allowlist for AI provider domains. Implements the SC-7 real_requirement; without it, blanket domain allowlisting is theater. |
| `D3-CSPP` | Client-server Payload Profiling | Gateway / TLS-inspected proxy | The only layer that can observe prompt/completion content shape (entropy, base64 ratio, recognisable IOC tokens) without per-SDK instrumentation. Covers the QUIC / HTTP/3 case where boundary inspection sees only ciphertext. |
| `D3-IOPR` | Input/Output Profiling | SDK / application | SDK-level prompt and completion logging with identity binding. The single most-load-bearing control for AI C2 — every Step in the Analysis Procedure degrades to "structurally zero coverage" without it. |
| `D3-CA` | Connection Attempt Analysis | Network egress | Detects the AI-API connection from processes that have no business reason on this host type (e.g. a system service contacting `api.openai.com`). Cheap; deployable without TLS interception. |
| `D3-DA` | Domain Analysis | Network egress | Catches Oblivious HTTP (RFC 9458) relays and atypical AI-provider edge endpoints whose direct upstream is a sanctioned LLM provider — the SesameOp evasion shape when ECH is in play. |
| `D3-NI` | Network Isolation | Network segmentation | For non-developer host classes (databases, network gear, OT) where no AI API egress is ever sanctioned, hard-blocking the provider AS-paths removes the C2 channel entirely. |

**Defense-in-depth posture:** `D3-NTA` + `D3-CA` + `D3-NI` are the network layer; `D3-CSPP` is the gateway layer; `D3-IOPR` is the SDK layer; `D3-NTPM` is the policy layer that binds the other four to identity. No single layer is sufficient — SesameOp is invisible to network-only deployments without `D3-CSPP` or `D3-IOPR`, and `D3-IOPR` is invisible without `D3-NTPM` to give it the per-identity baseline against which Step 3 anomaly detection fires.

**Least-privilege scope:** `D3-NTPM` is implemented per-identity-per-business-reason — the developer using Cursor on a workstation is allowlisted for `api.anthropic.com`; the same developer's service account is not. `D3-IOPR` retention is scoped to the identities authorised to call AI APIs; prompts from unauthorised identities trigger Step 2 the moment they appear in the log, not after retention review.

**Zero-trust posture:** every prompt is logged and identity-bound regardless of source host trust level; `D3-CSPP` and `D3-IOPR` verify content shape on every call rather than sampling. The verification primitive at the gateway is entropy + identity + business-reason; at the SDK layer it is full prompt + identity + retention. No "trusted developer" exemption — PROMPTFLUX is delivered to developer workstations as readily as to production hosts.

**AI-pipeline applicability:** `D3-IOPR` is the only control that survives serverless / ephemeral runtimes; per-host `D3-NTA` and `D3-CA` cannot baseline a host whose lifetime is shorter than the correlation window. The scoped alternative for ephemeral workloads is workload-identity-bound `D3-IOPR` correlated by IAM role / service-account identity rather than by host — preserving the PROMPTFLUX cadence shape and PROMPTSTEAL credential-access correlation across short-lived function invocations.

---

## Compliance Theater Check

> "Your SC-7 boundary-protection evidence shows AI provider domains — `api.openai.com`, `api.anthropic.com`, `generativelanguage.googleapis.com`, Azure OpenAI endpoints, Bedrock endpoints — on the egress allowlist, with NetFlow or Zeek records demonstrating that egress is monitored. Now answer two questions. First: for each AI provider domain on the allowlist, does the allowlist entry enumerate the specific sanctioned business reason and the identities or services entitled to use it, or is the entry a blanket allow for the domain? Second: do you have SDK-level prompt and completion logging, bound to identity, retained for at least 90 days, and forwarded to the SIEM, for every place AI APIs are called in production? If the allowlist is a blanket domain allow and SDK-level prompt logging is absent, the SC-7 control is theater for AI C2 — boundary inspection of an allowlisted domain cannot distinguish a developer prompt from a SesameOp-encoded C2 prompt, and you have no content-layer evidence to fall back on. SC-7 evidence is structurally incomplete for any org using AI APIs in production unless both an identity-bound business-reason allowlist and SDK-level prompt logging are in place. The control gap is recorded in `data/framework-control-gaps.json` under NIST-800-53-SC-7 — the real requirement names exactly these components."

---

## Output Format

The skill produces a structured AI C2 Detection Assessment covering per-host AI-API egress baselines, behavioral anomaly indicators, and SesameOp-class C2-pattern findings. The shape below is consumed downstream by `incident-response-playbook` (which scopes IR against confirmed C2 indicators), by `ai-attack-surface` (which integrates the detection-gap section into the broader AI surface report), and by `compliance-theater` (which compares the AI-API monitoring coverage against any SI-4 / CC7 anomaly-detection compliance claim). Preserve the per-host egress-baseline shape verbatim — it is the load-bearing detection artifact.

```
## AI C2 Detection Assessment

**Date:** YYYY-MM-DD
**Scope:** [hosts / network segments assessed]

### Current Detection Coverage
| Detection Layer | Deployed | Coverage |
|---|---|---|
| Process-level AI API baseline | Yes/No | [% of host types covered] |
| Behavioral correlation (AI + file/cred/scan) | Yes/No | [configured correlations] |
| TLS inspection for AI traffic | Yes/No | [% of AI API traffic] |
| Response monitoring | Yes/No | [coverage] |

### Coverage Gaps
[What's missing from the detection architecture]

### Active Indicators
[If this is a live investigation: current IOCs, correlated events]

### Detection Rule Recommendations
[Specific rules to add, tuned for the org's AI tooling inventory]

### Framework Gap Declaration
[Per framework: what monitoring control exists, why it doesn't address AI C2]
```

---

## Hand-Off / Related Skills

After producing the AI C2 detection assessment, the operator should chain into the following skills. Each entry is specific to a finding class this skill produces.

- **`dlp-gap-analysis`** — AI-API-as-C2 is a DLP egress channel. The same SDK-level prompt logging recommended above (identity-bound, retained 90+ days, forwarded to SIEM) is the exact instrumentation that detects DLP egress through prompts. Treat the AI API endpoint as a sanctioned-SaaS DLP surface and apply prompt-content classifiers, not just file/email classifiers. A SesameOp-encoded payload is a DLP event the moment the prompt leaves the host.
- **`defensive-countermeasure-mapping`** — map AI C2 findings to D3FEND: D3-NTA / D3-NTPM (network traffic analysis plus policy mapping for AI provider egress, including the QUIC / HTTP/3 path called out in the RFC Transport Reality section), D3-IOPR (prompt-shape profiling per identity baseline), D3-CSPP (client-server payload profiling on prompt and completion bodies when TLS-inspected). The Layer 1–4 detection architecture maps directly to these counters.
- **`mcp-agent-trust`** — AI-API-mediated C2 frequently routes through MCP tools whose privilege scope exceeds the documented business reason. When PROMPTSTEAL-pattern correlations surface (AI API call + credential-store access + large-egress), pivot into MCP trust assessment as a compensating control: tightening MCP tool allowlists and removing shell/process-execution-capable servers reduces the blast radius of the AI agent that the C2 is steering.
- **`attack-surface-pentest`** — AI-API egress channels must be enumerated in attack-surface management and exercised in adversary-emulation engagements. Most pen-test scopes test for outbound DNS / generic HTTPS C2 and do not specifically exercise legitimate-AI-SaaS-as-C2. Without this, the SesameOp / PROMPTFLUX / PROMPTSTEAL signature shapes are detected only post-incident.
- **`compliance-theater`** — test whether the org's SC-7 boundary-protection claim is satisfied by domain allowlisting alone. It is theater: see the SC-7 boundary-protection entry in `data/framework-control-gaps.json`, which names the real requirement (identity-bound business-reason allowlist plus SDK-level prompt logging). Boundary inspection of an allowlisted AI provider domain cannot distinguish a developer prompt from a C2-encoded prompt.

For ephemeral / serverless workloads: per-host EDR-side correlation (Layer 2) is architecturally impossible when the host's lifetime is shorter than the correlation window. The scoped alternative is identity-bound prompt logging at the SDK layer combined with workload-identity correlation in the SIEM (e.g., correlate AI API calls by IAM role / service-account identity rather than by host), which preserves the SesameOp / PROMPTFLUX / PROMPTSTEAL signature shapes across short-lived function invocations.
