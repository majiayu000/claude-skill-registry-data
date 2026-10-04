---
description: Assess UK GDPR compliance — post-Brexit requirements, ICO guidance, international transfers
---

# UK GDPR Assessment

Assess UK General Data Protection Regulation compliance for "$ARGUMENTS". Evaluate UK-specific divergences from EU GDPR, ICO requirements, and UK international transfer mechanisms.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **UK GDPR applicability and divergences:**
   - Assess whether UK GDPR applies (UK establishment, offering goods/services to UK, monitoring UK individuals)
   - Identify areas where UK GDPR diverges from EU GDPR
   - Review ICO as the supervisory authority and its enforcement approach
   - Assess dual compliance obligations if both EU and UK GDPR apply

3. **Lawful basis and consent (UK approach):**
   - Assess lawful basis per processing activity under UK GDPR
   - Evaluate UK-specific legitimate interest balancing test (ICO three-part test)
   - Review age of consent for information society services (13 in UK vs 16 in EU)
   - Assess Age Appropriate Design Code (Children's Code) applicability

4. **International transfers (UK mechanisms):**
   - Map all transfers outside the UK
   - Assess UK adequacy decisions (which countries have UK adequacy)
   - Evaluate UK International Data Transfer Agreement (IDTA) usage
   - Review UK addendum to EU Standard Contractual Clauses
   - Assess UK Transfer Risk Assessments (TRAs)
   - Evaluate transfers between UK and EEA (bridging provisions)

5. **PECR (Privacy and Electronic Communications Regulations):**
   - Assess cookie consent compliance (PECR requirements)
   - Evaluate direct marketing consent (email, SMS, phone)
   - Review electronic communication security obligations
   - Assess cookie banner implementation and consent mechanisms

6. **UK-specific governance:**
   - Assess DPO appointment under UK GDPR
   - Review ICO registration (data protection fee)
   - Evaluate UK representative appointment (if required for non-UK organizations)
   - Assess records of processing activities

7. **Breach notification (UK requirements):**
   - Assess breach notification to ICO (72 hours)
   - Evaluate data subject notification procedures
   - Review breach severity assessment aligned with ICO guidance
   - Check breach register maintenance

8. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/uk-gdpr.md` following the assessment template structure with:
   - **UK Applicability** — territorial scope and dual compliance assessment
   - **Divergence Analysis** — UK vs EU GDPR differences with compliance impact
   - **Lawful Basis Assessment** — UK-specific approach including legitimate interest
   - **Transfer Mechanisms** — IDTA, UK addendum, adequacy, TRA status
   - **PECR Compliance** — cookies, direct marketing, electronic communications
   - **ICO Governance** — registration, DPO, representative requirements
   - **Breach Readiness** — ICO notification capability
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The UK GDPR assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/uk-gdpr.md`. Present a summary to the user highlighting:
- Overall UK GDPR compliance score
- Key divergences from EU GDPR requiring separate compliance effort
- PECR compliance status
- Top 3 gaps requiring remediation
