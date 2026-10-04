---
description: Assess ISO 27018 PII protection in public cloud
---

# ISO 27018 Assessment

Assess ISO/IEC 27018:2019 PII (Personally Identifiable Information) protection in public cloud for "$ARGUMENTS". Evaluate PII processor obligations and cloud-specific PII protections.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **PII processing context:**
   - Identify PII categories processed in the public cloud (names, emails, financial data, health data, etc.)
   - Determine role: PII controller, PII processor, or both
   - Map data flows showing where PII enters, is processed, stored, and exits the cloud environment
   - Identify applicable privacy regulations (GDPR, CCPA, etc.) that ISO 27018 supports

3. **PII processor obligations assessment (ISO/IEC 29100 principles):**
   - **Consent and choice** — assess mechanisms for obtaining and managing data subject consent
   - **Purpose legitimacy and specification** — assess documentation of processing purposes, limitation to stated purposes
   - **Data minimization** — assess collection limitation, data adequacy, relevance checks
   - **Use, retention, and disclosure limitation** — assess data retention policies, usage restrictions, third-party disclosure controls
   - **Accountability** — assess privacy governance, DPO appointment, privacy impact assessments
   - **Information security** — assess security controls protecting PII (encryption, access control, monitoring)
   - **Privacy compliance** — assess privacy policy publication, compliance monitoring, breach response
   - Score each principle: Compliant / Partially Compliant / Non-Compliant

4. **Cloud-specific PII protections assessment:**
   - **Data location disclosure** — assess transparency about where PII is stored and processed geographically
   - **Sub-processor transparency** — assess disclosure of sub-processors, notification of sub-processor changes, contractual flow-down requirements
   - **Breach notification to controllers** — assess incident notification procedures to PII controllers, timeline commitments, content requirements
   - **Data return and disposal** — assess data portability upon contract termination, secure deletion procedures, deletion certification
   - **Government access disclosure** — assess policy for handling government data access requests, transparency reporting
   - **PII transmission security** — assess encryption in transit, secure API design, data transfer mechanisms
   - Score each protection: Implemented / Partially Implemented / Not Implemented

5. **Contractual requirements review:**
   - Assess Data Processing Agreements (DPAs) for ISO 27018 alignment
   - Check contractual obligations with sub-processors
   - Verify controller notification procedures are contractually defined

6. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/iso27018.md` following the assessment template structure with:
   - **PII Processing Context** — data types, roles, data flows
   - **PII Processor Obligations** — 7 principles scored with findings
   - **Cloud-Specific PII Protections** — cloud protections scored with findings
   - **Contractual Requirements** — DPA and sub-processor agreement review
   - **Overall Compliance Score** — aggregate score with heatmap
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The ISO 27018 assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/iso27018.md`. Present a summary to the user highlighting:
- PII categories and processing role identified
- Overall PII protection maturity score
- Top 3 PII protection gaps
- Sub-processor transparency status
