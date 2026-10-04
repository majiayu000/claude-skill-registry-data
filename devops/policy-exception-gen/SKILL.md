---
name: policy-exception-gen
version: "1.0.0"
description: Generate defensible policy exceptions for architectural realities — ephemeral infra, AI pipelines, ZTA, no-reboot patching, with compensating controls and auditor-ready justification
triggers:
  - policy exception
  - exception request
  - control exception
  - ephemeral exception
  - serverless exception
  - ai pipeline exception
  - zero trust exception
  - compensating control
data_deps:
  - atlas-ttps.json
  - cve-catalog.json
  - exploit-availability.json
atlas_refs: []
attack_refs: []
framework_gaps: []
forward_watch:
  - New ephemeral compute paradigms (WASM, MicroVMs)
  - EU CRA exceptions for AI pipeline components
  - NIST SP 800-204 series updates for microservices
  - FedRAMP updates for container/serverless authorization
last_threat_review: "2026-09-28"
---

# Policy Exception Generation

Policy exceptions document why a standard control cannot be implemented as specified and what compensating controls provide equivalent or superior protection. A good exception is:
- Specific about why the standard control doesn't apply
- Honest about the residual risk
- Concrete about the compensating controls (not vague "enhanced monitoring")
- Time-bounded or tied to an architectural condition
- Signed off by a named risk owner

This skill generates exception templates for architectural realities that current frameworks don't accommodate.

---

## Frontmatter Scope

The `atlas_refs`, `attack_refs`, and `framework_gaps` arrays are intentionally empty. Exceptions are generated *against* whatever control the operator names at invocation time — the input is the framework-control ID, and the output is a templated exception keyed to that ID. Pinning a fixed subset here would constrain the skill's input domain to the wrong dimension; any framework gap any other skill produces is a legitimate exception-template input.

---

## Threat Context (mid-2026)

Most non-trivial mid-2026 production architectures break the literal reading of at least one major framework control. Serverless functions break asset-inventory language; immutable container images break in-place patch-window language; LLM API dependencies break change-management language; Zero Trust environments break network-segmentation language. Where the organization has no defensible exception process, only two outcomes remain: (1) the organization claims compliance falsely (theater) or (2) the audit blocks the architecture entirely.

Concrete instances:

- **NIST 800-53 SI-2 vs. ephemeral containers.** SI-2 frames patching as in-place flaw remediation within an "organizationally defined time period." Ephemeral container workloads with immutable images are not patched in place — a vulnerable image is rebuilt and redeployed. Without an exception, an auditor reading SI-2 literally would mark a correctly-operating immutable infrastructure pipeline as non-compliant.
- **NIST 800-53 CM-3 vs. external LLM provider updates.** CM-3 requires change review, approval, testing, and documentation for changes to production systems. OpenAI, Anthropic, and Google deploy LLM behavioral updates without operator notification or consent. Without an exception, every external model update is technically an uncontrolled production change.
- **PCI DSS 6.3.3 patch deadline vs. Lambda.** AWS Lambda runtime is patched by AWS on its schedule; the customer cannot apply a patch within 30 days of disclosure independent of the provider.
- **NIS2 Art. 21 asset register vs. autoscaled serverless.** NIS2 expects an accurate asset register; ephemeral function instances do not have persistent identifiers to register.

Concurrent with these architectural lags, real-world TTPs continue to target the underlying systems. A defensible exception is the only mechanism that lets an organization (a) acknowledge the framework lag honestly, (b) document the compensating controls that disrupt the residual TTPs, and (c) survive both the audit and the threat. An undefended exception — a sticky note that says "doesn't apply, we use Lambda" — is theater. This skill produces the defensible variant.

---

## Framework Lag Declaration

Per-framework lag statements for each exception category in this skill:

| Framework | Control | Lag (what the control language does not accommodate) |
|---|---|---|
| NIST 800-53 | SI-2 (Flaw Remediation) | "Organizationally defined time periods" for in-place patching are architecturally impossible for ephemeral containers, immutable images, and serverless runtimes. The control assumes a persistent patchable asset. |
| NIST 800-53 | CM-3 / CM-8 (Configuration Change Control / Component Inventory) | CM-3 assumes the org controls all production changes; CM-8 assumes inventoriable assets. External LLM provider model updates violate CM-3; autoscaled serverless violates CM-8. |
| NIST 800-53 | SC-7 (Boundary Protection) | Drafted around perimeter and zone-based segmentation. Zero Trust Architecture (NIST SP 800-207) replaces perimeter segmentation with identity-centric controls; SC-7 evidence (firewall rules, zone diagrams) is not the operative control surface in ZTA. |
| ISO 27001:2022 | A.5.9 (Inventory of information and other associated assets) | Asset-inventory language predates serverless and autoscaled container workloads. Ephemeral function instances cannot be individually inventoried. |
| ISO 27001:2022 | A.8.8 (Management of Technical Vulnerabilities) | "Appropriate timescales" is undefined and does not contemplate live kernel patching as a required capability. Critical no-reboot systems require an explicit exception process. |
| ISO 27001:2022 | A.8.32 (Change management) | Same gap as NIST CM-3 — external LLM model updates fall outside the operator's change-management scope. |
| PCI DSS 4.0 | 6.3.3 (Patches) | 30-day window assumes operator control over patch application. Cloud provider runtimes (Lambda, Cloud Functions) are patched by the provider on the provider's schedule. |
| PCI DSS 4.0 | 12.3.4 (Inventory of system components) | Persistent-asset assumption — fails for autoscaled ephemeral compute. |
| PCI DSS 4.0 | 1.3 (Network segmentation) | Implicit perimeter-trust model; ZTA evidence shape does not match the language. |
| NIS2 | Art. 21 (Cybersecurity risk-management measures) | Asset register and patch management language predates serverless; ephemeral nodes cannot be inventoried as the article assumes. |
| EU DORA | Art. 8 (ICT-related risk and ICT asset management) + Art. 9 (protection and prevention) + Art. 28 (ICT third-party risk) | Financial-entity asset register and patch-management obligations mirror the NIS2 lag: ephemeral compute has no clean register fit, and Art. 28 ICT third-party register is silent on LLM API providers and developer-environment MCP servers. ESAs RTS on subcontracting (JC 2024/53) does not enumerate AI/ML SaaS classes. |
| EU AI Act (Regulation 2024/1689) | Art. 13 (transparency / instructions for use) + Art. 15 (cybersecurity for high-risk AI) | Drafted around vendor-provided AI systems with documented change-management. External provider model updates that change behavior mid-deployment have no exception language; high-risk AI Art. 15 cybersecurity expectations assume operator control over the model. |
| UK NCSC CAF | Principle A2 (Risk Management), A4 (Supply Chain), B4 (System Security) | Outcome-based assessment. NCSC Cloud Security Principles and ZT Architecture Design Principles (NCSC 2024) recognize ephemeral and identity-centric architectures, but the CAF outcome statements do not enumerate ZTA / ephemeral / AI-model-update as explicit deviation classes. Exception language must map the operator's compensating-control bundle to the CAF principle's outcome rather than to a prescriptive control. |
| UK Cyber Essentials Plus | Patch management + Secure Configuration criteria | 14-day patch SLA assumes persistent assets the operator patches. Ephemeral / immutable / provider-patched runtimes (Lambda, Cloud Run, Cloudflare Workers) fall outside the criterion as written. The CE+ assessor expects a documented justification when a service does not fit the standard model. |
| AU ASD Essential 8 | Patch Applications + Patch Operating Systems + Application Control (ML1-ML3) | Patch-window language assumes a persistent OS / application installation the operator patches. Ephemeral container workloads with immutable images and serverless runtimes break the model. Application Control (allowlisting) does not contemplate AI-coding-assistant tool-use chains where the AI agent dynamically composes the executed action. |
| AU ASD ISM | ISM-1143 (patch management processes) + ISM-1876 and ISM-1877 (48-hour windows) + ISM-1809 (compensating controls for unsupported products) + ISM-1569 (shared responsibility model) | ISM-1809 is the ISM's own exception mechanism, but it covers only products their vendor no longer supports. ISM-1569 assigns responsibilities between supplier and customer without exception language for a provider-controlled runtime, and the patching windows assume the operator applies the patch. |
| AU APRA CPS 234 | Para 27 (information security capability) + Para 36 (control testing) | "Capability commensurate with vulnerabilities and threats" language. AI-pipeline and ZTA architectures are not enumerated as in-scope capability classes; an APRA-regulated entity must document the architectural deviation explicitly to avoid a control-testing finding. |

This skill's exceptions exist precisely because the framework language has not caught up to the architecture. The exceptions do not claim the threat goes away — they document the compensating controls that handle the residual TTPs (see TTP Mapping).

---

## TTP Mapping (MITRE ATLAS v2026.09 and ATT&CK)

A granted exception does not remove the threat — it shifts the burden onto compensating controls. For each exception in this skill, the residual TTPs the compensating controls MUST still disrupt:

| Exception | Residual TTPs the exception must still address | Compensating coverage requirement |
|---|---|---|
| Exception 1 — Ephemeral Infrastructure Asset Inventory | T1525 (Implant Internal Image), T1610 (Deploy Container), T1611 (Escape to Host), T1078.004 (Valid Cloud Accounts) | Image scanning in CI, IaC drift detection, cloud-asset-inventory API alerts on resources not in IaC registry |
| Exception 2 — AI Pipeline Change Management | AML.T0020 (Training Data Poisoning), AML.T0018 (Manipulate AI Model), AML.T0051 (LLM Prompt Injection — emergent behavior on model upgrade), AML.T0054 (LLM Jailbreak) | Behavioral regression test suite, model version pinning, model fingerprinting on canonical prompts, provider changelog review |
| Exception 3 — Zero Trust Architecture Network Segmentation | T1021 (Remote Services), T1570 (Lateral Tool Transfer), T1078 (Valid Accounts), T1199 (Trusted Relationship) | Workload identity (SPIFFE/SPIRE), per-request mTLS, device-posture verification, east-west behavioral analytics |
| Exception 4 — Critical Systems No-Reboot Kernel Patching | T1068 (Exploitation for Privilege Escalation — Copy Fail class), T1548.001 (Setuid and Setgid), T1611 (Escape to Host) | Live kernel patch deployed and verified (`kpatch list` / `canonical-livepatch status`), eBPF/auditd exploitation-pattern rules, network-layer isolation if no live patch available, scheduled reboot window |

The TTP source-of-truth is `data/atlas-ttps.json` (MITRE ATLAS v2026.09, September 2026) supplemented by ATT&CK Enterprise. No orphaned controls: no exception in this skill is granted without an enumerated residual-TTP set; an exception with no listed residual is theater.

---

## Exploit Availability Matrix

For each residual TTP an exception leaves in scope, the compensating control bundle must be RWEP-justified — i.e., proportionate to the public exploit availability for the associated CVE class. Pull the RWEP scoring from `data/cve-catalog.json` and `data/exploit-availability.json` before granting the exception.

| Residual TTP | Evidence CVE / class | CVSS | RWEP tier | KEV | Public PoC | AI-accelerated | Live-patchable | Implication for compensating bundle |
|---|---|---|---|---|---|---|---|---|
| T1068 (Privilege Escalation — Copy Fail class) | CVE-2026-31431 | 7.8 | 90 | Yes (2026-05-01) | Yes (732 bytes, deterministic) | Yes | Yes (kpatch/livepatch) | Live patch within 4 hours OR network isolation — anything weaker is non-defensible |
| T1190 (Exploit Public-Facing Application — IPsec subsystem) | CVE-2026-43284 (Dirty Frag) | 8.8 | 53 | No | Yes (chain component) | Yes (AI-assisted discovery) | Limited (kpatch RHEL-only) | eBPF kernel-text integrity monitoring + maintenance-window reboot SLA |
| AML.T0051 (LLM Prompt Injection — emergent on model upgrade) | CVE-2025-53773 (Copilot YOLO-mode RCE) | 7.8 (AV:L) | 30 | No | Yes | Yes | Yes (SaaS push / IDE update) | Behavioral regression suite + system-prompt hardening + tool allowlist |
| AML.T0010 (ML Supply Chain Compromise — MCP) | CVE-2026-30615 (Windsurf MCP local-vector RCE) | 8.0 (AV:L) | 35 | No | Yes | No | Yes (IDE update) | MCP server allowlist + signed-manifest enforcement + per-server auth |
| T1525 / T1610 (Implant Internal Image / Deploy Container) | Image-supply-chain class | Varies | High | N/A | Operational | Yes | N/A (image rebuild) | CI image scanning gate at CVSS ≥ 7.0, SBOM per image, image-registry signing |

An exception that names a residual TTP without a compensating-control bundle of equal or greater RWEP-justified strength is theater. The compliance-theater skill's universal test (demand the bypassing TTP for any claimed compensating control) should be run against the bundle before the exception is approved.

---

## Exception Template Library

### Exception 1: Ephemeral Infrastructure — Asset Inventory

**Standard control:** NIST 800-53 CM-8 / ISO 27001 A.5.9 / PCI DSS 12.3.4 / NIS2 Art. 21  
**Control requirement:** Maintain an accurate, complete inventory of all information system components.

**Why standard control is architecturally impossible:**

Serverless functions (AWS Lambda, Azure Functions, GCP Cloud Run, Cloudflare Workers) do not have persistent identities. A Lambda function invocation exists for milliseconds to minutes. During peak load, thousands of instances may start and stop continuously. Individual instances cannot be:
- Scanned by vulnerability scanners (no persistent IP, no agent installation target)
- Listed in a CMDB (no stable identifier)
- Patched as individual assets (runtime is managed by the provider)
- Audited individually (no OS-level access)

Container workloads with Kubernetes auto-scaling have the same property: pods start and stop, have ephemeral IPs, and are indistinguishable from each other.

**Residual risk:** Traditional asset inventory enables: vulnerability scanning, configuration auditing, unauthorized asset detection, and change tracking. Each must be addressed by alternative means.

**Compensating controls:**

| Risk Area | Compensating Control |
|---|---|
| Vulnerability scanning | Container/function image scanning in CI pipeline (Trivy, Grype, Snyk) before deployment. Every image scanned before any deployment. |
| Configuration auditing | Infrastructure-as-Code (IaC) is the authoritative configuration source. IaC is version-controlled, reviewed, and drift-detected. Policy-as-Code (OPA, Conftest) enforces configuration standards at deployment time. |
| Unauthorized asset detection | Cloud asset inventory APIs (AWS Config, Azure Resource Graph, GCP Asset Inventory) list deployed functions/containers at the infrastructure level. Alerts on resources not in the IaC registry. |
| Change tracking | IaC commits are the change record. Every change to infrastructure is a pull request with review and approval. Runtime state drift from IaC baseline triggers alerts. |
| SBOM | Software Bill of Materials generated per image at build time. SBOM stored and associated with deployed image hash. |

**Exception language:**
```
CONTROL EXCEPTION REQUEST

Control: [CM-8 / A.5.9 / PCI 12.3.4]
System: [system name]
Exception Type: Architectural — ephemeral compute
Risk Owner: [name, title]
Review Date: [annual or on architecture change]

The [system name] uses serverless/container compute where individual runtime 
instances are ephemeral and cannot be individually inventoried, scanned, or 
patched as required by [control ID].

This exception is granted on the basis that the following compensating controls 
provide equivalent or superior assurance:

1. Image scanning: [tool] scans all container/function images before deployment. 
   No image with CVSS ≥ 7.0 vulnerabilities deploys to production.
2. IaC as authoritative inventory: all infrastructure is defined in [IaC tool] 
   in [repo]. The IaC repository IS the asset inventory.
3. IaC drift detection: [tool] alerts within [time] of any runtime state 
   deviation from IaC-defined state.
4. Cloud-native asset listing: [cloud provider] asset inventory API is queried 
   daily and compared against IaC registry. Unrecognized resources trigger alerts.
5. SBOM per image: SBOMs are generated at build time and stored at [location].

Residual risk: Runtime configuration drift between IaC updates is detected 
within [SLA] rather than continuously. Individual instance-level forensics 
post-incident requires cloud provider support.

Approved by: [name]
Date: [date]
```

---

### Exception 2: AI Pipeline — Change Management

**Standard control:** NIST 800-53 CM-3 / ISO 27001 A.8.32 / SOC 2 CC8 / PCI DSS 6.5  
**Control requirement:** All changes to information systems undergo a change management process including review, approval, testing, and documentation.

**Why standard control doesn't fully apply to LLM dependencies:**

Organizations using LLM APIs (OpenAI, Anthropic, Google, Azure OpenAI) are dependent on externally managed model updates that occur:
- Without operator notification or consent
- On the provider's schedule, not the organization's change management calendar
- In ways that may alter model behavior, output characteristics, and safety properties
- Continuously (model improvements, safety mitigations, capability changes)

The organization cannot apply its change management process to a change it does not control and is not notified of.

**What the org can control:**
- Model version pinning (where the API supports it)
- Behavioral regression testing after detected model changes
- System prompt stability (changes to system prompts go through change management)
- Application code that interfaces with the LLM API (fully under change management)

**Compensating controls:**

| Risk Area | Compensating Control |
|---|---|
| Uncontrolled behavioral changes | Pin model versions where supported (e.g., `gpt-4o-2024-11-20` not `gpt-4o`). Operator receives advance notice of version deprecation. |
| Behavioral regression | Automated behavioral test suite runs nightly against current model. Tests cover: safety-relevant outputs, accuracy on business-critical tasks, rejection of known adversarial prompts. Alert on regression. |
| Safety property changes | Weekly review of provider changelogs and safety announcements. Document any safety-relevant model changes in risk register. |
| Undetected changes (provider doesn't announce) | Model fingerprinting: track model response consistency on canonical test prompts. Deviation > threshold triggers review. |

**Exception language:**
```
CONTROL EXCEPTION REQUEST

Control: [CM-3 / A.8.32 / CC8]
System: [AI system name]
Exception Type: Architectural — externally managed AI model dependency
Risk Owner: [name, title]
Review Date: [annual or on provider change]

The [AI system] depends on [provider] LLM API. Model updates by [provider] 
occur without operator advance notice or consent and cannot be subject to 
the organization's change management process.

This exception covers: LLM model version updates made by [provider].
This exception does NOT cover: system prompt changes, application code changes, 
integration changes — these remain subject to standard change management.

Compensating controls:
1. Model version pinning: [model ID] is pinned to [specific version]. 
   Any version upgrade requires change management approval.
2. Behavioral regression testing: automated suite ([count] tests) runs on 
   [schedule]. Regression alerts require [process] review before continued use.
3. Provider changelog monitoring: [responsible role] reviews provider 
   release notes [weekly]. Safety-relevant changes logged in risk register.
4. Model fingerprinting: canonical prompt set tracked. Unexplained deviation 
   triggers unplanned review.

Approved by: [name]
Date: [date]
```

---

### Exception 3: Zero Trust Architecture — Network Segmentation

**Standard control:** NIST 800-53 SC-7 / ISO 27001 A.8.22 / PCI DSS 1.3  
**Control requirement:** Implement network segmentation between security zones using firewalls, DMZs, and network access controls.

**Why standard control concept changes in ZTA:**

Zero Trust Architecture eliminates the concept of a trusted network perimeter. In a ZTA:
- All traffic is treated as potentially hostile regardless of network segment
- Network segmentation is replaced by identity-centric access controls
- Per-request authentication and authorization replace zone-based trust
- Micro-segmentation at the workload level replaces macro network zones

A traditional network segmentation audit (checking that the PCI zone is separated from the general corporate network) is not meaningful when all traffic is authenticated at the application layer and network location provides no trust signal.

**What ZTA provides instead:**

| Segmentation Control | ZTA Equivalent |
|---|---|
| Firewall between zones | Per-request mutual TLS with certificate-based workload identity |
| Trusted internal network | Continuous device posture verification; no implicit trust by location |
| DMZ | Identity and access policies at service mesh layer; all services authenticated |
| Network ACLs | Service-level authorization policies (SPIFFE/SPIRE, Istio, etc.) |

**Compensating controls:**
1. Workload identity: all services have cryptographic identities (SPIFFE SVIDs or equivalent). No service-to-service communication without mutual authentication.
2. Per-request authorization: every API call is authenticated and authorized. Authorization policies are version-controlled and reviewed.
3. Device posture: continuous assessment of device health before granting network access. Non-compliant devices blocked at identity layer.
4. Lateral movement monitoring: behavioral analytics on east-west traffic patterns. Anomalous service-to-service communication triggers alerts.

**Exception language:**
```
CONTROL EXCEPTION REQUEST

Control: [SC-7 / A.8.22 / PCI DSS 1.3]
System: [zero trust environment scope]
Exception Type: Architectural — Zero Trust Architecture
Risk Owner: [name, title]
Review Date: [annual or on ZTA architecture change]

The [environment] implements Zero Trust Architecture which eliminates 
traditional network perimeter segmentation in favor of identity-centric controls.

Traditional segmentation compliance evidence (zone diagrams, firewall rule reviews) 
is not applicable to this architecture. Alternative evidence provided:

1. Workload identity: [implementation] provides cryptographic identity for all 
   services. See [attestation/config].
2. Per-request authorization: all service-to-service calls authenticated via 
   [method]. Authorization policies at [location].
3. Device posture: [system] continuously assesses device health. 
   Non-compliant devices blocked. Policy at [location].
4. Lateral movement monitoring: [system] alerts on anomalous east-west traffic.

Reference: NIST SP 800-207 (Zero Trust Architecture) documents this architecture 
as a valid implementation of layered access control.

Approved by: [name]
Date: [date]
```

---

### Exception 4: Critical Systems — No-Reboot Kernel Patching

**Standard control:** NIST 800-53 SI-2 / ISO 27001 A.8.8 / PCI DSS 6.3.3 / NIS2 Art. 21  
**Control requirement:** Apply security patches within required timelines (30 days for Critical, or within 1 month per PCI).

**Why standard control applies but requires qualification:**

Production systems that cannot tolerate a reboot (high-availability databases, real-time processing systems, 24/7 operating environments) cannot apply kernel security patches within required timelines without service disruption. A standard "patch and reboot" process may require a maintenance window that is:
- Hours to days away
- Subject to change control that extends the timeline
- Contractually or legally restricted (SLAs with customers)

This is not a reason to leave systems unpatched — it is a reason to require live kernel patching as a capability. The exception documents the live patching deployment and the timeline to full patch.

**This is a time-limited exception** — once the maintenance window occurs, the full patch is applied and the exception closes.

**Compensating controls (for the period between live patch and reboot):**
1. Live kernel patch deployed: kpatch / livepatch / kGraft deployed and verified applied. (`kpatch list` / `canonical-livepatch status`)
2. Enhanced monitoring: eBPF/auditd exploitation detection rules active for the vulnerability class.
3. Network isolation: if live patch is not available for the specific CVE, network-level isolation of affected systems.
4. Maintenance window scheduled: specific date/time documented. Patch + reboot completed at that window closes the exception.

**For CISA KEV class (Copy Fail CVE-2026-31431):** This exception is only valid if live patch has been deployed. If live patch is not available and the system cannot be rebooted: isolate at the network layer until the reboot window, and escalate to risk committee as an open CISA KEV with no adequate compensating control.

**Exception language:**
```
CONTROL EXCEPTION REQUEST

Control: [SI-2 / A.8.8 / PCI 6.3.3]
CVE: [CVE-ID]
System: [system name]
Exception Type: Operational — maintenance window required for reboot
Duration: [current date] to [scheduled maintenance window date]
Risk Owner: [name, title]

[System name] requires a reboot to apply [CVE-ID] kernel patch. A reboot 
requires maintenance window approval. The next approved maintenance window 
is [date].

Live kernel patch status: [Deployed / Not available for this CVE]
If live patch deployed: [kpatch list output / livepatch status]
If live patch not available: [compensating network controls]

Detection controls active during exception period:
- [auditd rules for exploitation pattern]
- [eBPF monitoring for privilege escalation attempts]
- [network isolation scope if applicable]

This exception expires on [maintenance window date]. If not patched by that 
date, escalate to [risk committee].

Approved by: [name]
Date: [date]
```

---

## Analysis Procedure

### Step 1: Identify the architectural reality

Determine which exception category applies:
- Ephemeral compute (serverless/container at scale)?
- Externally managed AI model dependency?
- Zero Trust Architecture replacing traditional segmentation?
- Critical system no-reboot window?
- Other (describe the architectural constraint)

### Step 2: Identify the specific control

Find the exact control ID and control text. Do not use paraphrases — cite the actual requirement.

### Step 3: Document why the control doesn't apply as written

Be specific. "We use serverless" is not sufficient. Explain exactly what property of the architecture makes the control unapplicable as written.

### Step 4: Define compensating controls

Each compensating control must:
- Address a specific risk that the standard control was designed to address
- Be concrete (tool name, configuration, SLA)
- Be independently verifiable
- Have a named owner

"Enhanced monitoring" without specifics is not a compensating control.

### Step 5: Assign a risk owner

The risk owner must be named and must have the organizational authority to accept the residual risk. Security team cannot be the risk owner — that's the team identifying the risk, not accepting it.

### Step 6: Set an expiration

Exceptions should expire:
- On a specific date (for time-limited conditions like maintenance windows)
- On an architectural change (for ZTA/ephemeral — review if architecture changes)
- Annually (minimum review cycle for standing exceptions)

---

## Output Format

Produce a complete, signed exception document using the applicable template above, populated with:
- Specific control ID and text
- Specific system or environment scope
- Specific architectural constraint
- Specific compensating controls with tool names and SLAs
- Residual risk statement
- Named risk owner
- Expiration date or condition

---

## Compliance Theater Check

A granted exception without a documented compensating-control bundle that is RWEP-justified against the residual TTPs is theater. The exception process becomes a rubber stamp that converts an audit blocker into a paper compliance claim with no real protection.

Run this test against the organization's exception register:

> **Pull the last 5 granted exceptions. For each exception, demand: (a) the residual attacker TTPs it leaves in scope (with ATLAS / ATT&CK IDs resolving in `data/atlas-ttps.json`), (b) the specific compensating-control bundle that disrupts each residual TTP, and (c) the RWEP-justified strength of that bundle against the public exploit availability for those TTPs (sourced from `data/cve-catalog.json` and `data/exploit-availability.json`).**

Decision rule, per exception:

- All three present → exception is defensible. Record CLEAR.
- Residual TTPs absent → the exception was granted without analyzing what threats it leaves in play. THEATER FLAG. Re-open the exception and require TTP enumeration.
- Compensating controls vague ("enhanced monitoring", "additional logging", "team awareness") → the bundle is not concrete enough to disrupt anything. THEATER FLAG. Require tool names, configuration, SLA, and a named owner.
- RWEP-justification absent → the bundle may exist but is unscored against current exploit availability. THEATER FLAG. The most dangerous form is a bundle that handles 2018 threat-model TTPs while the residual includes CVE-2026-31431 / 30615 / 2025-53773 class threats.

Specific high-confidence theater signals for this skill's four exception categories:

| Exception category | Theater signal | What a defensible variant looks like |
|---|---|---|
| Ephemeral Infrastructure Asset Inventory | "We use Lambda so CM-8 doesn't apply" with no IaC-as-inventory or image-scanning evidence | IaC repo named, image-scanning tool named, SBOM storage location named, cloud-asset-inventory alert rule named |
| AI Pipeline Change Management | "External provider, out of scope" with no model version pin, no behavioral regression suite, no changelog review | Pinned model ID, named regression suite with test count and schedule, named reviewer for provider changelogs, model-fingerprinting prompt set |
| Zero Trust Architecture Segmentation | "We're zero trust" with no SPIFFE/mTLS evidence and no east-west behavioral analytics | Workload identity implementation named, mTLS configuration evidence, device-posture system named, lateral-movement detection rules cited |
| Critical Systems No-Reboot Kernel Patching | "Can't reboot, will catch up later" with no live patch, no eBPF rules, no maintenance window | `kpatch list` / `canonical-livepatch status` output, named eBPF / auditd rules for the exploitation pattern, scheduled maintenance date, escalation contact if missed |

When this check fires on any exception, hand off to the compliance-theater skill to record the systemic finding (this is Pattern 3 / 4 / 5 / 6 territory depending on category) and to framework-gap-analysis to determine whether the framework lag warrants escalation to the global-grc skill for cross-jurisdictional review.

---

## Defensive Countermeasure Mapping

Every defensible exception names the residual TTPs in scope and the compensating-control bundle that disrupts them. The mapping below converts the compensating-control language ("eBPF monitoring", "workload identity", "image-scanning") into the D3FEND technique IDs that audit reviewers can verify against `data/d3fend-catalog.json`. An exception template that cites vague compensating controls without a D3FEND ID fails the Compliance Theater Check above.

| Exception category | Residual offensive TTP | D3FEND ID | Defensive technique (compensating control) | Defense-in-depth layer |
|---|---|---|---|---|
| Ephemeral Infrastructure (CM-8 / A.5.9) | T1610 (Deploy Container), T1525 (Implant Internal Image) | `D3-EFA` | Executable File Analysis (image-registry scanning, SBOM per image) | Build / registry — pre-deployment image integrity verification |
| Ephemeral Infrastructure | T1525 | `D3-EAL` | Executable Allowlisting (signed-image-only deploy gate) | Cluster admission — only signed images reach the runtime |
| AI Pipeline Change Management (CM-3 / A.8.32) | AML.T0018 (Manipulate AI Model), AML.T0020 (Training Data Poisoning) | `D3-FAPA` | File Access Pattern Analysis (training-data and model-artifact access baselining) | Data tier — detect anomalous access to corpora and weights |
| AI Pipeline Change Management | AML.T0018 | `D3-IOPR` | Input/Output Profiling (behavioral regression suite, model-fingerprinting prompt set) | SDK / application — detect model substitution and drift |
| Zero Trust Architecture Segmentation (SC-7 / A.8.22) | T1021 (Remote Services), T1570 (Lateral Tool Transfer) | `D3-NTPM` | Network Traffic Policy Mapping (SPIFFE / mTLS workload identity enforcement) | Network — per-workload-identity policy on east-west flows |
| Zero Trust Architecture Segmentation | T1021 / T1570 | `D3-NTA` | Network Traffic Analysis (east-west behavioral analytics) | Network — detect lateral movement that policy alone cannot prevent |
| Zero Trust Architecture Segmentation | T1078 (Valid Accounts) | `D3-CBAN` | Certificate-based Authentication (mTLS workload certificates) | Identity — workload identities are certificate-bound, not perimeter-bound |
| No-Reboot Kernel Patching (SI-2 / A.8.8) | T1068 (Exploitation for Privilege Escalation) | `D3-SCA` | System Call Analysis (eBPF / auditd rules for the exploitation primitive) | Kernel — detect the LPE primitive while live-patch is in flight |
| No-Reboot Kernel Patching | T1068 | `D3-KBPI` | Kernel-Based Process Isolation | Kernel — reduce blast radius until the live patch deploys |
| No-Reboot Kernel Patching | T1068 (post-exploit persistence) | `D3-PA` | Process Analysis (anomalous-uid / capability-set detection) | Endpoint — catch successful LPE before it persists |

**Defense-in-depth posture:** an exception that names a single D3FEND technique is insufficient — the residual TTP set is multi-stage, and the compensating-control bundle must cover the chain. The Output Format's "Compensating Controls" field must enumerate at least two D3FEND techniques per residual TTP, drawn from different defense-in-depth layers (network + endpoint, build + admission, SDK + gateway). An exception with only one layer cited is theater for the multi-stage attack chain.

**Least-privilege scope:** D3FEND technique deployment is scoped to the exception's affected asset class. `D3-EAL` admission rules are per-cluster (production ≠ staging ≠ developer). `D3-NTPM` workload-identity policies are per-namespace. `D3-FAPA` training-data baselines are per-corpus-per-principal. The exception document must record the scope alongside the technique ID — "we deploy `D3-EAL` cluster-wide" is too coarse; "we deploy `D3-EAL` on `prod-*` clusters with signed-image-only admission" is auditable.

**Zero-trust posture:** the exception is defensible only when the cited D3FEND techniques are deployed, monitored, and tested against the residual TTPs at exception-grant time and re-verified at the documented review cadence. An exception with deployed techniques but no test evidence (chaos-engineering exercise, red-team result, detection-rule firing on a controlled trigger) is unverified. The "Review Cadence" field in the Output Format must specify the re-verification test, not just the calendar date.

**AI-pipeline applicability (some controls are architecturally impossible in serverless / ephemeral contexts):** for AI Pipeline Change Management exceptions, `D3-EAL` and `D3-EFA` do not apply to serverless inference endpoints — the scoped alternative is `D3-CSPP` at the inference gateway plus provider-signed-image attestation in the model-card. `D3-FAPA` on ephemeral RAG indices degrades to per-query retrieval logging via `D3-IOPR` plus index-build provenance signed at construction. These degradations must be enumerated in the exception's "Compensating Controls" field; an AI-pipeline exception that copies a non-AI exception template is incomplete.
