---
description: Assess HITRUST CSF readiness — control requirements, assessment methodology, certification path
---

# HITRUST CSF Assessment

Assess HITRUST Common Security Framework (CSF) certification readiness for "$ARGUMENTS". Determine assessment type, evaluate control domains, and identify the certification path.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **Assessment type determination:**
   - **e1 (Essentials, 1-year)** — assess suitability for low-risk organizations (44 controls)
   - **i1 (Implemented, 1-year)** — assess suitability for moderate assurance needs (182 controls)
   - **r2 (Risk-based, 2-year)** — assess suitability for high assurance requirements (full control set)
   - Evaluate organization risk profile, regulatory requirements, and customer expectations
   - Document recommended assessment type with rationale

3. **Control domain assessment:**
   - **Access Control** — user access management, authentication, authorization, privileged access
   - **Human Resources Security** — screening, terms of employment, security awareness, termination
   - **Risk Management** — risk assessment methodology, risk treatment, risk acceptance criteria
   - **Security Policy** — information security policies, management direction, review cycle
   - **Asset Management** — asset inventory, acceptable use, information classification, media handling
   - **Communications and Operations Management** — operational procedures, change management, capacity, malware, backup, network security, media handling, exchange of information, monitoring
   - **Information Systems Acquisition, Development, Maintenance** — security requirements, secure development, test data, access control to source code
   - **Information Security Incident Management** — incident response, reporting, evidence collection
   - **Business Continuity Management** — BCM framework, BIA, BC plans, testing
   - **Compliance** — legal requirements, security reviews, audit controls
   - **Privacy Practices** — privacy program, notice, choice/consent, collection, use/retention/disposal
   - **Third-Party Assurance** — vendor risk management, third-party agreements, monitoring
   - Score each domain: 1 (policy), 2 (procedures), 3 (implemented), 4 (measured), 5 (managed)

4. **Control mapping from existing frameworks:**
   - Map existing ISO 27001 controls to HITRUST requirements
   - Map existing NIST CSF/800-53 controls to HITRUST requirements
   - Map existing SOC 2 controls to HITRUST requirements
   - Identify controls already satisfied by existing certifications
   - Identify gaps requiring additional HITRUST-specific implementation

5. **Certification path and timeline:**
   - Determine readiness timeline based on current maturity
   - Identify external assessor (authorized HITRUST assessor) requirements
   - Estimate assessment effort (internal preparation, external assessment)
   - Estimate budget (HITRUST licensing, assessor fees, remediation costs)
   - Define milestone timeline from current state to certification

6. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/hitrust.md` following the assessment template structure with:
   - **Assessment Type Recommendation** — e1/i1/r2 with rationale
   - **Control Domain Scoring** — maturity score per domain
   - **Framework Mapping** — existing controls mapped to HITRUST
   - **Gap Analysis** — controls requiring new implementation
   - **Certification Path** — timeline, assessor requirements, budget estimate
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The HITRUST CSF assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/hitrust.md`. Present a summary to the user highlighting:
- Recommended assessment type (e1/i1/r2)
- Overall control maturity score across domains
- Percentage of controls satisfied by existing framework certifications
- Top 3 gaps requiring remediation
- Estimated timeline to certification readiness
