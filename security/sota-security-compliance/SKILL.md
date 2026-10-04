---
name: sota-security-compliance
description: >-
  State-of-the-art security & compliance engineering (2026) for the
  cybersecurity control frameworks and product-security regulations that drive
  architecture, code, and CI gates — not the organizational policy binder. Use
  when work must satisfy or be audited against NIST CSF 2.0, SP 800-53, SP
  800-171 / CMMC, the Secure Software Development Framework (SSDF, SP 800-218),
  FedRAMP, the EU Cyber Resilience Act (CRA), or ISA/IEC 62443
  (OT/ICS/embedded). Covers control-framework-as-code crosswalks (control →
  engineering mechanism → evidence), CUI boundaries, FIPS-validated crypto,
  SBOM + coordinated vulnerability disclosure + security-update obligations,
  secure-SDLC gates, and OT zones/conduits & security levels. Complements
  sota-privacy-compliance (personal data, GDPR, SOC 2, ISO 27001). Trigger
  keywords: compliance, NIST, CSF, 800-53, 800-171, CMMC, CUI, SSDF, FedRAMP,
  CRA, Cyber Resilience Act, SBOM, VEX, CVD, IEC 62443, OT security, ICS,
  security levels, zones and conduits, FIPS 140.
---

# SOTA Security & Compliance Engineering

The engineering half of cybersecurity regulation: how to make a control framework
a property of the codebase, pipeline, and infrastructure rather than a binder of
policy documents. A control that lives in a schema, an IAM policy, a CI gate, or a
signed SBOM survives staff turnover and an assessor's sampling; a control that
lives in a wiki page does not.

This skill is the **security/regulation counterpart** to `sota-privacy-compliance`
(which owns personal-data lifecycle, GDPR, SOC 2, ISO 27001). It owns the
cybersecurity *control frameworks* and *product-security regulations* — NIST CSF
2.0, SP 800-53, SP 800-171 / CMMC, SSDF (SP 800-218), FedRAMP, the EU Cyber
Resilience Act, and ISA/IEC 62443 for OT.

> **This is engineering guidance, not legal, certification, or assessment advice.**
> Framework versions, regulation dates, and conformity routes move — every date
> and version below was verified against a primary source (NIST CSRC, EUR-Lex, the
> Federal Register, ISA/IEC) as of **July 2026** and each rules file cites it.
> Re-verify before you rely on a deadline, and route scoping/attestation decisions
> (is this system in CUI scope? which CMMC level? is our product "important" under
> the CRA?) to your assessor, sponsor, or counsel. This skill tells you how to
> build the machinery those decisions require.

## The boundary — what this skill does and does not own

Every framework here mixes **engineering controls** with **organizational
controls**. This skill owns only the first; it names the second and routes it out,
so you neither skip it nor pretend code can satisfy it.

| In scope (drives code / architecture / gates) | Out of scope (org/governance — note & route out) |
|---|---|
| System/authorization boundary definition, segmentation, zones & conduits | Security-awareness training programs, phishing simulations |
| FIPS-validated crypto selection; encryption at rest/in transit | Personnel screening, background checks, HR onboarding |
| Audit-log families, retention, tamper-evidence | Physical & environmental security (badges, data-center access) |
| SBOM generation, coordinated vuln disclosure, signed update channels | Risk-committee structure, CISO/DPO roles, board reporting |
| Secure-SDLC gates (SAST/DAST/provenance) as CI checks | Written policy authorship, management review cadence |
| Control-as-code mappings + machine-generated evidence | Legal interpretation, contract clauses, insurance |

When a framework requirement is organizational, the finding is *"owned by GRC/HR/
legal — here is the engineering hook (an event, an export, an enforcement point)
that makes it auditable,"* not silence and not a code change that pretends to
cover it.

**Related skills — reference, do not duplicate:**
- `sota-privacy-compliance` — personal-data lifecycle, GDPR/CCPA/HIPAA/PCI, SOC 2 & ISO 27001 audit-ready engineering, breach clocks, data residency
- `sota-devsecops` — the actual pipeline: SLSA/provenance, SBOM tooling, signing, dependency scanning (SSDF's PS/PW practices live here)
- `sota-secrets-management` — key management, FIPS-validated KMS, rotation
- `sota-identity-access` — NIST 800-63 assurance levels, MFA, RBAC/ABAC (the IA/AC control families)
- `sota-detection-engineering` — detective controls, NIST 800-61 incident response (the DE/RS/RC functions)
- `sota-network-security` — segmentation depth, zero-trust, egress control (SC family, 62443 conduits)
- `sota-sandboxing` / `sota-kubernetes` / `sota-cloud-infrastructure` — the CM/SC hardening controls in practice
- `sota-threat-modeling` — the risk analysis that sets 62443 target Security Levels and DPIA/PIA scope

## BUILD mode

When designing or implementing a system that must satisfy a framework:

1. **Scope the boundary first.** Before controls, decide what is *in* the assessed
   system — the authorization boundary (FedRAMP), CUI enclave (800-171/CMMC), or
   zone (62443). A tight, honest boundary is the cheapest control decision you will
   make; a flat network drags the whole estate into scope (rules/02, rules/05).
2. **Pick the framework spine, then crosswalk down.** Use NIST CSF 2.0 as the
   organizing map, then bind each outcome to a concrete mechanism from an existing
   sota-* skill and record it as code (rules/01). Do not re-implement encryption,
   RBAC, or logging here — reference where they already live.
3. **Encode controls as gates, not prose.** Encryption-required, FIPS-crypto-only,
   boundary-egress-deny, SBOM-present, no-known-exploitable-vulns-at-release become
   policy-as-code and CI checks that fail the build (rules/01 §evidence, rules/03).
4. **Build product-security obligations in from day one** where the CRA/62443
   apply: SBOM in CI, a coordinated-vulnerability-disclosure intake, a signed
   update channel, and a defined support period are architecture, not paperwork —
   brutal to retrofit (rules/04, rules/05).
5. **Emit evidence as a byproduct.** Every control's enforcing system should
   produce its own proof (a CI log, a signed attestation, an IaC diff, a KSI feed).
   If proving a control needs a screenshot, the control runs only at screenshot
   time (rules/01).
6. **Know your regime before architecture freezes** (rules/02–05): CUI → 800-171/
   CMMC + FIPS crypto + boundary; US-gov cloud → FedRAMP + 800-53 baseline;
   EU-market product → CRA; OT/industrial/embedded → 62443.

## AUDIT mode

When reviewing a codebase/infrastructure against a framework:

**Process:** (1) Establish the applicable framework(s) and the assessed boundary
(rules/02 §scope). (2) Obtain or build the control crosswalk — control → claimed
mechanism → evidence source (rules/01). (3) For each control, verify the mechanism
*actually enforces* it and the evidence is machine-generated, not asserted — test
the gate, read the policy-as-code, sample the log. (4) Separate engineering
findings from organizational ones (the boundary table above) so each lands with
the right owner. (5) Map findings to the framework's control IDs so they are
traceable to an assessor's language.

**Severity conventions:**

| Severity | Meaning | Examples |
|---|---|---|
| CRITICAL | Control absent where a regulation/contract mandates it; exploitable or ships now | CUI leaving the boundary unencrypted; product shipped with a known exploitable vuln under CRA; non-FIPS crypto protecting CUI; no vuln-reporting path with a live 24h/72h clock |
| HIGH | Control claimed but not enforced; fails on first assessment/incident | Encryption "policy" with no CI enforcement; SBOM promised but not generated; SSDF attestation signed but PW practices absent; flat network claiming a segmented CDE/zone |
| MEDIUM | Control runs but evidence is manual/stale, or crosswalk is incomplete | Evidence gathered by screenshot; control matrix maps to a wiki not a mechanism; SL-T asserted without a risk assessment behind it |
| LOW | Hardening / traceability hygiene | Control IDs not referenced in code/IaC; exception register lacks expiry; update channel unsigned but not yet required |

**Finding format:**

```
[SEVERITY] <title>
Location: <file:line / pipeline stage / IaC resource / boundary component>
Framework: <CSF 2.0 Subcat / 800-53 control / 800-171 req / SSDF task / CRA Annex I / 62443 FR — as applicable>
Owner: <engineering | GRC/org — per the boundary table>
Issue: <control missing / claimed-not-enforced / evidence-not-generated>
Impact: <assessment failure, contract loss, CRA non-conformity, incident exposure>
Fix: <concrete engineering remediation, or the hook if org-owned>
Evidence: <how you verified — the gate you ran, the log you sampled, the policy you read>
```

Group findings by control family/function, not by file — that is how assessors
and sponsors read them.

## Rules index

| File | Read this when... |
|---|---|
| [rules/01-control-frameworks-as-code.md](rules/01-control-frameworks-as-code.md) | Starting any compliance work; choosing NIST CSF 2.0 as a spine; building the control → mechanism → evidence crosswalk; deciding what to reuse from other sota-* skills vs. build; encoding controls as policy-as-code and CI gates; control-coverage metrics (numerator/denominator from evidence queries) |
| [rules/02-nist-800-53-171-cmmc-fedramp.md](rules/02-nist-800-53-171-cmmc-fedramp.md) | Handling CUI / selling to US government or defense; scoping an authorization boundary or CUI enclave; picking a 800-53 baseline; FIPS-validated crypto; CMMC level and phase-in; FedRAMP / FedRAMP 20x |
| [rules/03-ssdf-secure-sdlc.md](rules/03-ssdf-secure-sdlc.md) | Standing up or auditing a secure SDLC; mapping SSDF (SP 800-218) PO/PS/PW/RV practices to your pipeline; security requirements in supplier and outsourced-development contracts (PO.1.3); federal secure-software self-attestation; AI/model development (SP 800-218A) |
| [rules/04-eu-cyber-resilience-act.md](rules/04-eu-cyber-resilience-act.md) | Placing a product with digital elements on the EU market; SBOM, secure-by-default, no-known-exploitable-vulns; the CVD policy (RFC 9116 `security.txt`: required `Contact`/`Expires`, several contact routes, safe harbour) and signed update channel (device updates: anti-rollback security counter, authenticated update server, encrypted packages still signed over the plaintext); **triaging an inbound report** (§3a — what starts the awareness clock, ISO/IEC 30111/29147, and checking the cited code exists); **publishing your own advisory** (§3b — CVE via a CNA, required contents, OSV/CSAF so scanners match it); the 24h/72h ENISA reporting clocks; CRA timeline & conformity |
| [rules/05-iec-62443-ot-ics.md](rules/05-iec-62443-ot-ics.md) | Building or auditing OT/ICS/IIoT/embedded/industrial products; zones & conduits segmentation; Security Levels (SL-T/C/A) and the 7 Foundational Requirements; 62443-4-1 vs SSDF; 62443 as a CRA conformity route; the embedded device (§6 — ROM/eFuse-anchored secure boot chain, JTAG/SWD/UART and ROM download mode locked on production units, hardware supply-chain vetting, unit decommissioning with cryptographic erase and identity revocation) |

## Top 10 non-negotiables

1. **Scope the boundary before the controls.** The assessed system's edge —
   authorization boundary, CUI enclave, or 62443 zone — is decided, drawn, and
   enforced by segmentation before control work starts. A flat network makes the
   whole estate in scope and every control 10× more expensive.
2. **One control set, many frameworks.** Build the mechanism once and crosswalk it;
   CSF, 800-53, 800-171, SOC 2, ISO 27001, and CRA overwhelmingly ask for the same
   engineering. Per-framework silos duplicate work and drift.
3. **A control is the mechanism, not the policy.** Every control maps to a running
   system that enforces it. "We have a policy" with no enforcing mechanism is a
   finding, not a control.
4. **Evidence is a byproduct or it is theater.** Each control's enforcing system
   produces its own proof — CI log, signed attestation, IaC history, KSI feed.
   Screenshots pasted before fieldwork are the smell of a control that runs only
   then.
5. **FIPS-validated crypto where the regime demands it.** CUI, FedRAMP, and many OT
   contexts require validated modules (FIPS 140-3), not merely "encryption." A
   home-rolled or non-validated cipher protecting CUI is a critical finding.
6. **Ship no known exploitable vulnerabilities.** Under the CRA (and as basic
   hygiene) release gates block known-exploitable vulns; a monitored SLA drives
   remediation within the support period. "We'll patch it later" is a
   non-conformity, not a backlog item.
7. **SBOM, CVD, and a signed update channel are architecture.** For any product
   under the CRA/62443, generate an SBOM in CI, publish a coordinated-vulnerability-
   disclosure intake, and sign updates over a maintained channel — designed in, not
   bolted on at audit time. **An intake is only half of it**: the reporting clock runs
   from *awareness*, so the triage that decides whether a report is real, ours and
   exploitable is on the critical path and needs a written order (rules/04 §3a).
8. **Secure-SDLC practices are gates, not intentions.** SSDF PW/PS practices —
   threat modeling, SAST/DAST, provenance, protected repos, signing — are CI checks
   that fail the build. A signed attestation whose practices aren't enforced is
   the finding assessors hunt.
9. **Reporting clocks are wired into on-call, not lawyers.** Where a regime imposes
   a 24h/72h reporting clock (CRA, NIS2, DORA), detection and the reporting
   workflow are engineered and rehearsed; a clock that depends on someone noticing
   is already breached.
10. **Separate engineering findings from organizational ones.** Every control lands
    with the owner who can fix it. Blaming code for a training gap — or asking GRC
    to fix a missing CI gate — wastes both and leaves the real control unbuilt.
