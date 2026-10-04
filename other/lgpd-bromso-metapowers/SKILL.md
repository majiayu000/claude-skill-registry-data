---
description: Assess Brazil LGPD compliance — legal bases, data subject rights, DPO, ANPD requirements
---

# LGPD Assessment

Assess Brazil Lei Geral de Protecao de Dados (LGPD) compliance for "$ARGUMENTS". Evaluate legal bases, data subject rights, DPO requirements, and ANPD obligations.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **Legal bases assessment (10 bases):**
   - Map each processing activity to one of LGPD's 10 legal bases: consent, legal obligation, public administration, research, contract, exercise of rights, life protection, health protection, legitimate interest, credit protection
   - Assess consent mechanisms (free, informed, unambiguous, specific purpose)
   - Evaluate legitimate interest use and balancing report (LIA) where applicable
   - Review special categories of sensitive personal data and additional protections
   - Document legal basis per processing activity

3. **Data subject rights assessment:**
   - Assess procedures for each right: confirmation of processing, access, correction, anonymization/blocking/deletion of unnecessary data, portability, deletion of data processed with consent, information about shared entities, information about consent denial consequences, consent revocation
   - Evaluate response timelines and channel accessibility
   - Review identity verification procedures
   - Assess free-of-charge access requirements

4. **DPO (Encarregado) requirements:**
   - Assess whether DPO/Encarregado appointment is required
   - Evaluate DPO qualifications and independence
   - Review DPO contact information public availability
   - Assess DPO responsibilities and reporting structure

5. **ANPD registration and compliance:**
   - Assess ANPD registration requirements and status
   - Review records of processing activities
   - Evaluate incident notification procedures (reasonable timeframe to ANPD and data subjects)
   - Assess privacy impact report (RIPD / Relatorio de Impacto a Protecao de Dados Pessoais) requirements

6. **International transfers:**
   - Map all transfers outside Brazil
   - Assess transfer mechanisms: countries with adequate protection level, contractual clauses, BCRs, international cooperation, ANPD authorization
   - Evaluate adequacy of transfer safeguards
   - Review data localization requirements if applicable

7. **Security and governance:**
   - Assess technical and administrative security measures
   - Evaluate privacy by design implementation
   - Review data retention and deletion policies
   - Assess anonymization and pseudonymization practices

8. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/lgpd.md` following the assessment template structure with:
   - **Legal Basis Matrix** — processing activity to legal basis mapping
   - **Data Subject Rights** — readiness score per right
   - **DPO/Encarregado** — appointment status and compliance
   - **ANPD Compliance** — registration, records, incident notification
   - **RIPD Status** — privacy impact report coverage
   - **International Transfers** — transfer map and mechanism assessment
   - **Security Measures** — technical and administrative safeguard assessment
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The LGPD assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/lgpd.md`. Present a summary to the user highlighting:
- Overall LGPD compliance score
- Legal basis coverage across processing activities
- DPO and ANPD compliance status
- Top 3 gaps requiring remediation
