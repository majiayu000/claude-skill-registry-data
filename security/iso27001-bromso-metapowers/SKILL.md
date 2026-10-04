---
description: Assess ISO/IEC 27001 ISMS compliance — Annex A controls, risk treatment, Statement of Applicability
---

# ISO 27001 Assessment

Assess ISO/IEC 27001:2022 Information Security Management System (ISMS) compliance for "$ARGUMENTS". Evaluate ISMS requirements (clauses 4-10), assess all 93 Annex A controls, and draft a Statement of Applicability.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **ISMS requirements assessment (Clauses 4-10):**
   - **Clause 4: Context of the organization** — assess understanding of internal/external issues, interested party requirements, ISMS scope definition
   - **Clause 5: Leadership** — assess management commitment, information security policy, roles and responsibilities
   - **Clause 6: Planning** — assess risk assessment methodology, risk treatment plan, information security objectives
   - **Clause 7: Support** — assess resources, competence, awareness, communication, documented information
   - **Clause 8: Operation** — assess operational planning, risk assessment execution, risk treatment implementation
   - **Clause 9: Performance evaluation** — assess monitoring, measurement, internal audit, management review
   - **Clause 10: Improvement** — assess nonconformity handling, corrective actions, continual improvement
   - Score each clause: Conforming / Minor nonconformity / Major nonconformity

3. **Annex A controls assessment (93 controls, 4 themes):**
   - **Organizational controls (37 controls)** — policies, roles, asset management, access control, supplier relationships, incident management, business continuity, compliance
   - **People controls (8 controls)** — screening, employment terms, awareness, disciplinary, termination, confidentiality, remote working, event reporting
   - **Physical controls (14 controls)** — physical perimeters, entry controls, securing offices, monitoring, utilities, cabling, equipment maintenance, storage media, clear desk
   - **Technological controls (34 controls)** — endpoint devices, privileged access, access restriction, source code, authentication, capacity, malware, vulnerabilities, logging, network security, web filtering, cryptography, SDLC, testing, change management, data masking, DLP, monitoring
   - Score each control: Implemented / Partially implemented / Not implemented / Not applicable

4. **Statement of Applicability (SoA) draft:**
   - For each of the 93 Annex A controls, document: applicability (yes/no), justification for inclusion/exclusion, implementation status, control description
   - Ensure all exclusions have documented justification

5. **Risk treatment plan assessment:**
   - Assess existing risk assessment methodology
   - Evaluate risk treatment decisions (accept, mitigate, transfer, avoid)
   - Check risk register completeness and currency
   - Assess residual risk acceptance process

6. **Documentation requirements check:**
   - Verify mandatory documented information exists (policies, procedures, records)
   - Assess document control processes (versioning, review, approval, distribution)
   - Identify missing or outdated documentation

7. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/iso27001.md` following the assessment template structure with:
   - **ISMS Clauses Assessment** — Clauses 4-10 scoring with findings
   - **Annex A Controls Assessment** — all 93 controls scored by theme
   - **Statement of Applicability Draft** — full SoA with applicability and status
   - **Risk Treatment Plan Review** — methodology, register, residual risk
   - **Documentation Gaps** — missing or outdated mandatory documents
   - **Overall Compliance Score** — aggregate score with heatmap
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The ISO 27001 assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/iso27001.md`. Present a summary to the user highlighting:
- ISMS maturity level across clauses 4-10
- Annex A compliance percentage by theme
- Top 5 control gaps
- Certification readiness assessment (ready / needs work / significant gaps)
