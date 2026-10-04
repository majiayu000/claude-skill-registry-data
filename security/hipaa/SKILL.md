---
description: Assess HIPAA compliance — Privacy Rule, Security Rule, Breach Notification, BAAs
---

# HIPAA Assessment

Assess Health Insurance Portability and Accountability Act (HIPAA) compliance for "$ARGUMENTS". Evaluate Privacy Rule, Security Rule, Breach Notification Rule, and Business Associate Agreement coverage.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **Entity classification:**
   - Determine if covered entity (health plan, healthcare clearinghouse, healthcare provider with electronic transactions)
   - Determine if business associate (handles PHI on behalf of covered entity)
   - Assess hybrid entity considerations
   - Document entity classification with rationale

3. **Privacy Rule assessment:**
   - Assess permitted uses and disclosures of Protected Health Information (PHI)
   - Evaluate minimum necessary standard implementation
   - Review individual rights: access, amendment, accounting of disclosures, restriction requests, confidential communications, right to receive notice of privacy practices
   - Assess Notice of Privacy Practices (NPP) content and distribution
   - Evaluate authorizations for uses/disclosures not otherwise permitted
   - Review de-identification methods (safe harbor vs expert determination)
   - Assess marketing and fundraising communication compliance

4. **Security Rule assessment:**
   - **Administrative safeguards:** security management process (risk analysis, risk management, sanction policy, information system activity review), assigned security responsibility, workforce security, information access management, security awareness training, security incident procedures, contingency plan, evaluation
   - **Physical safeguards:** facility access controls, workstation use, workstation security, device and media controls
   - **Technical safeguards:** access control (unique user ID, emergency access, automatic logoff, encryption), audit controls, integrity controls (mechanism to authenticate ePHI), person/entity authentication, transmission security (integrity controls, encryption)
   - Classify each safeguard as required vs addressable
   - Score each safeguard: implemented / partially implemented / not implemented

5. **Breach Notification Rule assessment:**
   - Assess breach risk assessment methodology (four-factor test)
   - Evaluate individual notification procedures (within 60 days of discovery)
   - Assess HHS/OCR notification procedures (within 60 days for breaches affecting 500+ individuals, annual log for smaller breaches)
   - Review media notification requirements (500+ in a state/jurisdiction)
   - Evaluate breach documentation and investigation processes

6. **Business Associate Agreements (BAAs):**
   - Inventory all business associates handling PHI
   - Assess BAA coverage (all BAs have current, compliant agreements)
   - Review BAA terms for required provisions
   - Evaluate BA monitoring and compliance verification procedures
   - Assess subcontractor BAA flow-down requirements

7. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/hipaa.md` following the assessment template structure with:
   - **Entity Classification** — covered entity, business associate, or hybrid determination
   - **Privacy Rule Assessment** — use/disclosure controls, individual rights, NPP status
   - **Security Rule Assessment** — administrative, physical, technical safeguard scoring
   - **Breach Notification Readiness** — risk assessment methodology, notification procedures
   - **BAA Inventory** — coverage assessment and agreement adequacy
   - **Risk Analysis** — overall risk posture and highest-risk areas
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The HIPAA assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/hipaa.md`. Present a summary to the user highlighting:
- Entity classification determination
- Privacy Rule, Security Rule, and Breach Notification readiness scores
- BAA coverage percentage
- Top 3 gaps requiring remediation
