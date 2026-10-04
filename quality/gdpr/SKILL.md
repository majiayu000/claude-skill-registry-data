---
description: Assess GDPR compliance — lawful basis, data mapping, DPIA, rights, transfers, DPO, breach notification
---

# GDPR Assessment

Assess EU General Data Protection Regulation (GDPR) compliance for "$ARGUMENTS". Evaluate lawful basis, data mapping, data subject rights, international transfers, and breach readiness.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **Lawful basis assessment (Art 6/9):**
   - Identify each processing activity and its claimed lawful basis
   - Assess validity of consent mechanisms (freely given, specific, informed, unambiguous)
   - Evaluate legitimate interest balancing tests where applicable
   - Review special category data processing (Art 9) and additional conditions
   - Document lawful basis per processing activity in a matrix

3. **Data mapping and records of processing (Art 30):**
   - Assess data inventory completeness (what personal data, categories of data subjects)
   - Map data flows (collection points, storage locations, processing systems, recipients)
   - Evaluate retention periods and deletion schedules
   - Review records of processing activities for controllers and processors
   - Identify gaps in data lineage documentation

4. **Data Protection Impact Assessment (Art 35):**
   - Identify high-risk processing requiring DPIA (profiling, large-scale monitoring, sensitive data)
   - Assess existing DPIAs for completeness and quality
   - Evaluate whether prior consultation with supervisory authority is required (Art 36)
   - Review DPIA methodology and risk scoring approach

5. **Data subject rights procedures:**
   - Assess processes for: access (Art 15), rectification (Art 16), erasure (Art 17), restriction (Art 18), portability (Art 20), objection (Art 21)
   - Evaluate response timelines (one month, extension procedures)
   - Review identity verification procedures for requests
   - Assess automated decision-making and profiling safeguards (Art 22)

6. **International transfers:**
   - Map all transfers outside the EEA
   - Assess transfer mechanisms: adequacy decisions, Standard Contractual Clauses (SCCs), Binding Corporate Rules (BCRs)
   - Evaluate Schrems II compliance (Transfer Impact Assessments, supplementary measures)
   - Review derogations relied upon (Art 49)

7. **DPO and governance:**
   - Assess whether DPO appointment is required (Art 37)
   - Evaluate DPO independence, resources, and reporting line
   - Review privacy by design and by default implementation (Art 25)

8. **Breach notification readiness:**
   - Assess breach detection capabilities
   - Evaluate notification procedures (72 hours to supervisory authority, without undue delay to data subjects)
   - Review breach severity assessment methodology
   - Check breach register maintenance

9. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/gdpr.md` following the assessment template structure with:
   - **Lawful Basis Matrix** — processing activity to legal basis mapping with validity assessment
   - **Data Mapping Assessment** — data inventory completeness and flow documentation
   - **DPIA Status** — high-risk processing identified and DPIA coverage
   - **Rights Procedures** — readiness score per right
   - **Transfer Mechanisms** — transfer map with mechanism and Schrems II compliance
   - **Governance** — DPO status, privacy by design maturity
   - **Breach Readiness** — detection, notification, and documentation capability
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The GDPR assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/gdpr.md`. Present a summary to the user highlighting:
- Overall compliance score across all assessment areas
- Lawful basis coverage and any unsupported processing activities
- Top 3 gaps requiring remediation
- International transfer risk areas
