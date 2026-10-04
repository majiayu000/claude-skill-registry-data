---
description: Assess CSA STAR compliance — Cloud Controls Matrix, CAIQ
---

# CSA STAR Assessment

Assess CSA STAR (Security, Trust, Assurance, and Risk) compliance for "$ARGUMENTS". Evaluate against the Cloud Controls Matrix (CCM) v4 domains and complete a Consensus Assessments Initiative Questionnaire (CAIQ) self-assessment.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **STAR level determination:**
   - Assess current maturity to determine target STAR level:
     - Level 1: Self-Assessment (CAIQ submission)
     - Level 2: Third-Party Audit (based on SOC 2 or ISO 27001)
     - Level 3: Continuous Monitoring (future standard)
   - Document rationale for target level

3. **Cloud Controls Matrix (CCM) v4 assessment:**
   - **Application & Interface Security (AIS)** — assess application security, API security, data integrity
   - **Audit Assurance & Compliance (AAC)** — assess audit planning, independent audits, compliance mapping
   - **Business Continuity Management (BCM)** — assess business continuity planning, testing, redundancy
   - **Change Control & Configuration (CCC)** — assess change management, configuration baselines, unauthorized change detection
   - **Data Security & Privacy (DSP)** — assess data classification, handling, retention, deletion, privacy
   - **Encryption & Key Management (EKM)** — assess encryption standards, key management lifecycle
   - **Governance, Risk & Compliance (GRC)** — assess governance framework, risk management, policy management
   - **Human Resources (HRS)** — assess background checks, training, acceptable use, offboarding
   - **Identity & Access Management (IAM)** — assess identity lifecycle, authentication, authorization, privilege management
   - **Infrastructure & Virtualization (IVS)** — assess network security, virtualization hardening, workload security
   - **Interoperability & Portability (IPY)** — assess data portability, API interoperability, vendor lock-in mitigation
   - **Mobile Security (MOS)** — assess mobile device management, BYOD, mobile application security
   - **Security Incident Management (SEF)** — assess incident response, forensics, notification procedures
   - **Supply Chain Management (STA)** — assess supply chain risk, vendor assessment, data supply chain
   - **Threat & Vulnerability Management (TVM)** — assess vulnerability scanning, penetration testing, threat intelligence
   - **Universal Endpoint Management (UEM)** — assess endpoint security, patching, monitoring
   - Score each domain: Implemented / Partially Implemented / Not Implemented

4. **CAIQ self-assessment:**
   - Complete CAIQ responses for all applicable CCM controls
   - Document evidence references for each "Yes" answer
   - Provide implementation details for partial implementations
   - Document planned remediation for "No" answers

5. **ISO 27001 / SOC 2 mapping (for Level 2):**
   - Map CCM controls to existing ISO 27001 Annex A controls or SOC 2 trust services criteria
   - Identify controls already covered by existing certifications
   - Highlight incremental controls needed beyond existing certifications

6. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/csa-star.md` following the assessment template structure with:
   - **STAR Level Target** — selected level with rationale
   - **CCM Domain Assessment** — all 16 domains scored with findings
   - **CAIQ Self-Assessment Summary** — completion status and key responses
   - **Certification Mapping** — overlap with ISO 27001 / SOC 2
   - **Overall Compliance Score** — aggregate score with heatmap
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The CSA STAR assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/csa-star.md`. Present a summary to the user highlighting:
- Target STAR level and readiness
- CCM compliance percentage by domain
- Top 3 domain gaps
- Overlap with existing ISO 27001 or SOC 2 controls
