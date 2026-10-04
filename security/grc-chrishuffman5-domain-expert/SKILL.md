---
name: grc
description: "Expert routing agent for GRC and compliance automation. Classifies governance, risk, and compliance requests and delegates to the appropriate platform agent. WHEN: \"GRC\", \"compliance automation\", \"SOC 2\", \"ISO 27001\", \"risk management\", \"audit readiness\", \"vendor risk\", \"TPRM\", \"control framework\", \"compliance monitoring\", \"policy management\", \"risk register\". Do NOT use for platform-specific questions -- use the `vanta`, `drata`, `onetrust`, `archer`, or `servicenow-grc` skill."
license: MIT
---

# GRC

This skill covers Governance, Risk, and Compliance (GRC) — GRC concepts, control frameworks, compliance automation, and the major GRC platforms. It helps organizations build and maintain compliance programs, manage risk, and automate evidence collection for audits.

## How to Approach Tasks

When you receive a GRC request:

1. **Identify the technology** — Determine which GRC platform is in use (Vanta, Drata, OneTrust, ServiceNow GRC, Archer, or technology-agnostic).

2. **Classify the request type:**
   - **Framework/compliance** — Identify the framework (SOC 2, ISO 27001, HIPAA, PCI DSS, etc.) and load `references/concepts.md`
   - **Platform configuration** — Read the technology-specific sibling skill
   - **Risk management** — Load risk concepts from `references/concepts.md`
   - **Audit preparation** — Identify framework, then read the relevant sibling skill
   - **Vendor/third-party risk** — Apply TPRM guidance
   - **Policy management** — Apply policy lifecycle guidance

3. **Load context** — Read `references/concepts.md` for general GRC concepts, or read a sibling skill for platform-specific work.

4. **Route** — Identify the appropriate sibling skill using the decision tree below.

## Technology Routing

### Vanta
**Read `vanta` when:**
- Vanta platform (vanta.com)
- Automated compliance monitoring for SOC 2, ISO 27001, HIPAA, PCI DSS, etc.
- Vanta trust reports or trust center
- Vanta vendor risk management
- AI policy agent
- Keywords: "Vanta", "Vanta compliance", "Vanta SOC 2", "Vanta trust report", "Vanta integrations", "Vanta vendor risk"

### Drata
**Read `drata` when:**
- Drata platform (drata.com)
- Drata Autopilot
- Automated evidence collection
- Personnel management and background checks
- Asset inventory automation
- Keywords: "Drata", "Drata autopilot", "Drata evidence", "Drata SOC 2", "Drata personnel", "Drata asset inventory"

### OneTrust
**Read `onetrust` when:**
- OneTrust platform
- Privacy management (GDPR, CCPA, DSAR)
- Consent management
- Data mapping / RoPA
- IT risk and third-party risk management
- AI governance
- Keywords: "OneTrust", "OneTrust privacy", "consent management", "DSAR automation", "data mapping", "OneTrust vendor risk", "AI governance"

### ServiceNow GRC
**Read `servicenow-grc` when:**
- ServiceNow platform (GRC module)
- Risk Management application
- Policy and Compliance Management
- Audit Management
- Integration with ITSM, ITOM, or SecOps
- Keywords: "ServiceNow GRC", "ServiceNow risk", "Now Platform compliance", "IRM ServiceNow", "ServiceNow audit", "ServiceNow vendor risk"

### Archer (RSA)
**Read `archer` when:**
- RSA Archer platform (on-premises or Archer SaaS)
- Enterprise GRC with quantitative risk
- Highly customizable GRC data model
- Operational risk, IT risk, audit management
- Keywords: "Archer", "RSA Archer", "Archer GRC", "Archer risk", "Archer compliance", "Archer audit"

## GRC Concepts Reference

Load `references/concepts.md` for general GRC architecture, framework guidance, risk methodology, and vendor-neutral compliance program design.

## Core GRC Knowledge

### What GRC Covers

**Governance** — How the organization makes decisions about security and compliance:
- Policy management (create, approve, distribute, attest, retire policies)
- Control ownership (who is responsible for each control)
- Executive reporting (board-level risk dashboard, compliance status)

**Risk Management** — Identifying, assessing, and treating information risk:
- Risk identification (threat modeling, vulnerability management, asset inventory)
- Risk assessment (likelihood × impact = inherent risk)
- Risk treatment (mitigate, accept, transfer, avoid)
- Residual risk tracking after controls applied

**Compliance** — Demonstrating that required controls are in place and operating effectively:
- Framework mapping (SOC 2, ISO 27001, HIPAA, PCI DSS, GDPR, NIST CSF)
- Control testing (design effectiveness + operating effectiveness)
- Evidence collection and retention
- Audit management and auditor communication

### Common Compliance Frameworks

| Framework | Governing Body | Focus | Audience |
|---|---|---|---|
| SOC 2 Type II | AICPA | Trust Service Criteria (security, availability, confidentiality) | B2B SaaS companies |
| ISO 27001 | ISO/IEC | ISMS — Information Security Management System | Global; international contracts |
| HIPAA | HHS OCR | Healthcare data (PHI) protection | US healthcare organizations |
| PCI DSS | PCI SSC | Payment card data security | Organizations processing card payments |
| GDPR | EU/EEA | Personal data privacy rights | Organizations processing EU resident data |
| CCPA/CPRA | California AG | California resident privacy rights | Organizations with California customers |
| NIST CSF | NIST | Cybersecurity risk framework | US federal contractors + voluntary |
| FedRAMP | GSA | Cloud service security for US government | Cloud providers serving federal agencies |
| SOC 1 | AICPA | Internal controls over financial reporting | Companies impacting customer financial reporting |
| HITRUST CSF | HITRUST Alliance | Healthcare + security unified framework | Healthcare-adjacent organizations |
| CIS Controls | CIS | Prioritized security controls | Any organization; practical implementation |

### Control Framework Mapping

One technical control can satisfy requirements across multiple frameworks simultaneously.

**Example: Multi-tenant access control**

| Control | SOC 2 | ISO 27001 | PCI DSS | HIPAA | NIST CSF |
|---|---|---|---|---|---|
| MFA enforced on all production systems | CC6.1 | A.8.5 | Req 8.4 | §164.312(d) | PR.AC-7 |
| Access reviewed quarterly | CC6.2 | A.5.18 | Req 7.2 | §164.312(a)(2)(i) | PR.AC-4 |
| Least privilege enforced | CC6.3 | A.8.2 | Req 7.3 | §164.312(a)(1) | PR.AC-3 |

**Benefits of control mapping:**
- Single evidence artifact satisfies multiple frameworks
- Reduces audit burden (one audit, multiple reports)
- Identifies gaps: if a control is missing, it flags gaps across all mapped frameworks
- Prioritizes control implementation: controls satisfying many frameworks have highest ROI

### Risk Register Structure

A risk register is the central catalog of identified risks.

```
Risk Register Entry:
  Risk ID: RISK-2025-042
  Title: Unauthorized access to production database
  Category: Information Security / Access Control
  
  Threat: External attacker or malicious insider gains database access
  Vulnerability: Database accessible via management port; broad access granted
  Asset: Customer PII database (100,000 records)
  
  Likelihood: 3/5 (possible — no MFA on DB, some over-privileged accounts)
  Impact: 5/5 (critical — regulatory breach notification + fines + reputational damage)
  Inherent Risk Score: 15/25 (High)
  
  Controls in place:
    - Network segmentation (partially implemented)
    - Quarterly access reviews (planned, not yet active)
  Residual Risk Score: 12/25 (High — controls not fully implemented)
  
  Treatment: Mitigate
  Remediation:
    - Implement MFA on all DB admin accounts [Owner: DBA Team, Due: 2025-03-01]
    - Remove over-privileged accounts [Owner: IAM Team, Due: 2025-02-15]
    - Enable database activity monitoring [Owner: SecOps, Due: 2025-04-01]
  
  Risk Owner: CISO
  Review Frequency: Quarterly
  Last Reviewed: 2025-01-15
  Status: In Remediation
```

### Compliance Automation Architecture

Modern compliance platforms automate evidence collection via API integrations.

```
Cloud Infrastructure → GRC Platform
  AWS Config → Checks S3 bucket encryption, security groups, IAM policies
  Azure Policy → Checks VM encryption, RBAC, Defender status
  GCP Security Command Center → Checks GKE security, IAM, storage

Identity Providers → GRC Platform
  Okta → User list, MFA enrollment status, access reviews, login activity
  Entra ID → Users, groups, conditional access policies, MFA status

Endpoint Management → GRC Platform
  Intune / Jamf → Device encryption, patch status, MDM enrollment
  CrowdStrike → EDR deployment coverage

Code and SDLC → GRC Platform
  GitHub → Repo access controls, branch protection, PR review requirements
  Jira → Security ticket tracking, vulnerability remediation velocity

HR Systems → GRC Platform
  BambooHR / Workday → Employee onboarding, offboarding, role changes
  Background check providers → Verification status

Evidence generated automatically:
  "MFA enabled for all users" → API call to Okta → 100% enrollment = PASS
  "All S3 buckets encrypted" → AWS Config check → 2 failed buckets = FAIL
  "Quarterly access review complete" → IAM data → Last review: 45 days ago = PASS
```

### Audit Evidence Management

**Evidence types:**
```
Automated evidence (from API integrations):
  → Screenshots of configuration settings
  → Exported JSON/CSV of policy configurations
  → Timestamp-stamped infrastructure scans
  → Automatically re-collected each audit cycle

Manual evidence (uploaded by control owners):
  → Policy documents (PDF)
  → Meeting minutes (board/security committee)
  → Training completion records
  → Vendor contracts and SOC 2 reports
  → Penetration test reports

Evidence requirements per framework:
  SOC 2 Type II: Evidence must span the audit period (typically 12 months)
    → Continuous monitoring evidence preferred
    → Point-in-time evidence acceptable with sampling strategy
  ISO 27001: Evidence demonstrates ongoing operation of ISMS
    → Records of management reviews, internal audits, risk assessments
  PCI DSS: Evidence must demonstrate quarterly and annual requirements
    → Quarterly vulnerability scans, annual penetration tests
    → Monthly reviews for some requirements
```

### Third-Party Risk Management (TPRM)

```
TPRM Workflow:

1. Vendor Intake
   → Business team requests a new vendor
   → Security team classifies vendor: Critical / High / Medium / Low
     (based on data access, system access, criticality to operations)

2. Security Assessment
   → Critical/High vendors: Full security questionnaire (SIG, CAIQ, or custom)
   → Medium vendors: Abbreviated questionnaire + SOC 2 report review
   → Low vendors: Self-attestation + spot review

3. Initial Review
   → Review questionnaire responses
   → Review SOC 2 Type II report (check coverage period, exceptions noted)
   → Check for material findings; request remediation plan if needed
   → Decision: Approve / Approve with conditions / Reject

4. Ongoing Monitoring
   → Annual reassessment (or triggered by: breach news, contract renewal)
   → Monitor vendor security ratings (SecurityScorecard, BitSight)
   → Review updated SOC 2 reports each year
   → Monitor for vendor breach news (dark web, news alerts)

5. Offboarding
   → Confirm data deletion/return per contract
   → Revoke all access credentials
   → Retain assessment records per retention policy
```

### Policy Management Lifecycle

```
1. Draft
   → Policy owner drafts policy content
   → Legal/compliance review for regulatory alignment
   → CISO/executive review

2. Approve
   → Formal approval workflow (documented approver, date, version)
   → Publish to policy management system

3. Distribute
   → All-employee notification
   → Training materials updated
   → Policy added to new hire onboarding

4. Attest
   → Annual attestation campaign: all employees confirm they've read the policy
   → Attestation records stored as compliance evidence

5. Review and Update
   → Annual review cycle (or triggered by: regulatory change, incident, org change)
   → Version control maintained (previous versions archived)

6. Retire
   → Policy replaced or no longer needed
   → Formal retirement with documented rationale
   → Archived (not deleted — historical evidence needed)
```

### SOC 2 Readiness — Key Areas

```
SOC 2 Trust Service Criteria — Security category (required):
  CC1 — Control Environment (policies, roles, accountability)
  CC2 — Communication and Information (policies distributed, trained)
  CC3 — Risk Assessment (formal risk register, annual review)
  CC4 — Monitoring Activities (internal audits, continuous monitoring)
  CC5 — Control Activities (controls designed and operating)
  CC6 — Logical and Physical Access Controls (IAM, MFA, access reviews)
  CC7 — System Operations (change management, incident response)
  CC8 — Change Management (SDLC, deployment controls)
  CC9 — Risk Mitigation (vendor management, business continuity)

Common gaps found in first SOC 2 audits:
  → No formal risk assessment process (CC3)
  → MFA not enforced on all production systems (CC6.1)
  → No formal access review process (CC6.2)
  → No documented incident response plan or tested DR plan (CC7)
  → Change management process not formalized (CC8)
  → Vendor security reviews not documented (CC9)
```

### ISO 27001 ISMS Structure

```
ISO 27001 requires an Information Security Management System (ISMS):

Clauses 4-10 (mandatory):
  4: Context of the organization — scope, interested parties
  5: Leadership — executive commitment, roles, policy
  6: Planning — risk assessment, risk treatment plan, objectives
  7: Support — resources, awareness, communication, documented information
  8: Operation — implement and control security processes
  9: Performance evaluation — monitoring, internal audit, management review
 10: Improvement — nonconformity management, continual improvement

Annex A controls (114 controls in 14 domains — ISO 27001:2013):
  A.5: Information security policies
  A.6: Organization of information security
  A.7: Human resource security
  A.8: Asset management
  A.9: Access control
  A.10: Cryptography
  A.11: Physical and environmental security
  A.12: Operations security
  A.13: Communications security
  A.14: System acquisition, development, and maintenance
  A.15: Supplier relationships
  A.16: Information security incident management
  A.17: Business continuity management
  A.18: Compliance

ISO 27001:2022 update: 93 controls (reorganized into 4 themes)
  Organizational, People, Physical, Technological
```

## Technology Agents

Read these sibling skills for platform-specific work:

- `vanta` — Vanta (automated compliance, 400+ integrations, 35+ frameworks)
- `drata` — Drata (Autopilot, automated evidence, personnel management)
- `onetrust` — OneTrust (privacy, consent, data mapping, AI governance)
- `servicenow-grc` — ServiceNow GRC (enterprise, ITSM integration)
- `archer` — Archer/RSA (enterprise, quantitative risk, highly customizable)

## Reference Files

- `references/concepts.md` — GRC fundamentals: risk registers, control mapping, compliance automation, audit evidence, TPRM, policy lifecycle, SOC 2 readiness, ISO 27001 ISMS
