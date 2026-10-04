---
description: Assess ISO 27701 privacy extension — PIMS requirements, GDPR/CCPA mapping
---

# ISO 27701 Assessment

Assess ISO/IEC 27701:2019 Privacy Information Management System (PIMS) compliance for "$ARGUMENTS". Evaluate PIMS requirements, controller-specific and processor-specific controls, and map controls to GDPR articles and CCPA sections.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **PIMS scope and context:**
   - Determine organization's role(s): PII controller, PII processor, or both
   - Identify PII processing activities and data flows
   - Map interested parties and their privacy requirements
   - Review existing ISO 27001 ISMS scope for PIMS extension alignment

3. **PIMS requirements assessment (Clauses 5-8):**
   - **Clause 5: PIMS-specific requirements related to ISO 27001** — assess context, leadership, planning, support, operation, performance evaluation, improvement with privacy extensions
   - **Clause 6: PIMS-specific guidance related to ISO 27002** — assess privacy-specific implementation guidance for applicable ISO 27002 controls
   - **Clause 7: Additional ISO 27002 guidance for PII controllers** — assess controller obligations
   - **Clause 8: Additional ISO 27002 guidance for PII processors** — assess processor obligations
   - Score each clause: Conforming / Minor nonconformity / Major nonconformity

4. **Controller-specific controls assessment (Annex A):**
   - **Legal basis** — assess documentation and validation of legal bases for processing (consent, contract, legitimate interest, legal obligation)
   - **Consent management** — assess consent collection, granularity, withdrawal mechanisms, consent records
   - **Data subject rights** — assess right to access, rectification, erasure, portability, restriction, objection
   - **Privacy by design and default** — assess data protection impact assessments (DPIAs), privacy-by-design principles
   - **Data sharing and transfer** — assess third-party data sharing agreements, cross-border transfer mechanisms (SCCs, BCRs, adequacy decisions)
   - Score each area: Implemented / Partially Implemented / Not Implemented

5. **Processor-specific controls assessment (Annex B):**
   - **Processing only on instruction** — assess controls ensuring processing only per controller instructions
   - **Sub-processor management** — assess sub-processor authorization, notification, contractual flow-down, due diligence
   - **Data breach notification** — assess processor-to-controller breach notification procedures, timeline, content
   - **Data return and deletion** — assess data return/deletion upon contract termination, deletion verification
   - **Audit support** — assess support for controller audits, information provision
   - Score each area: Implemented / Partially Implemented / Not Implemented

6. **GDPR mapping:**
   - Map ISO 27701 controls to GDPR articles (Articles 5-49)
   - Identify controls that directly satisfy GDPR requirements
   - Highlight GDPR requirements not fully covered by ISO 27701 controls
   - Assess GDPR-specific requirements: DPO, records of processing, DPIAs, lead supervisory authority

7. **CCPA mapping:**
   - Map ISO 27701 controls to CCPA sections (California Consumer Privacy Act / CPRA)
   - Identify controls satisfying consumer rights (right to know, delete, opt-out, non-discrimination)
   - Highlight CCPA-specific requirements not covered (sale of personal information, financial incentives, service provider obligations)

8. **Privacy program overlap assessment:**
   - Identify existing privacy program elements that already satisfy ISO 27701
   - Assess gap between current privacy program and ISO 27701 requirements
   - Document where ISO 27701 certification would provide incremental value beyond existing compliance

9. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/iso27701.md` following the assessment template structure with:
   - **PIMS Scope** — roles, data flows, interested parties
   - **PIMS Requirements Assessment** — Clauses 5-8 scored with findings
   - **Controller Controls** — Annex A controls scored with findings
   - **Processor Controls** — Annex B controls scored with findings
   - **GDPR Mapping** — control-to-article mapping with coverage analysis
   - **CCPA Mapping** — control-to-section mapping with coverage analysis
   - **Privacy Program Overlap** — existing coverage and incremental value
   - **Overall Compliance Score** — aggregate score with heatmap
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The ISO 27701 assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/iso27701.md`. Present a summary to the user highlighting:
- Organization role (controller/processor/both) and PIMS scope
- Overall PIMS compliance score
- GDPR coverage percentage via ISO 27701 controls
- Top 3 privacy control gaps
- Overlap with existing privacy program
