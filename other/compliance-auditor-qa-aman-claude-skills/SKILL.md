---
name: compliance-auditor
description: |
  Audit feature specs against India's Digital Personal Data Protection (DPDP) Act. Use this skill when:
  - Writing or reviewing any feature that handles user data (especially children's data)
  - Auditing a spec's Personal Information section for completeness
  - Checking a feature against DPDP Act 2023 requirements
  - Preparing compliance documentation before engineering review
  - Verifying masking, retention, and consent policies are defined for all PII
---

# Compliance Auditor — DPDP Act 2023

Audit a feature specification against India's Digital Personal Data Protection Act 2023. Identifies personal data elements, maps them to DPDP sections, checks for consent/retention/security policies, and flags compliance gaps.

## Workflow

1. **Read the feature spec** — Focus on data elements, PII sections, compliance sections
2. **Identify data elements** — Extract every data element from the spec
3. **Classify as personal data** — Determine if each element is personal data under DPDP
4. **Map to DPDP sections** — For each personal data element, identify applicable DPDP requirements
5. **Check policies** — Verify consent, purpose limitation, retention, security, and deletion policies exist
6. **Generate audit report** — Output the audit table and gap analysis

## DPDP Act 2023 — Key Provisions

### Definitions (Section 2)

| Term | DPDP Definition |
|------|----------------|
| **Personal data** | Any data about an individual who is identifiable by or in relation to such data |
| **Data Principal** | The individual whose personal data is being processed |
| **Data Fiduciary** | The entity that determines the purpose and means of processing |
| **Data Processor** | The entity that processes data on behalf of a Data Fiduciary |
| **Significant Data Fiduciary** | A Data Fiduciary notified by the government based on volume/sensitivity of data |
| **Child** | Individual below the age of 18 years |

### Obligations of Data Fiduciary (Section 8)

| # | Obligation | Check |
|---|-----------|-------|
| 1 | **Lawful purpose** — Process data only for a lawful purpose for which Data Principal has given consent | Purpose stated in spec? Consent mechanism defined? |
| 2 | **Purpose limitation** — Use data only for the purpose for which it was collected | Each data element has a stated purpose? No secondary use without fresh consent? |
| 3 | **Data minimization** — Collect only data necessary for the stated purpose | Each element justified by a spec requirement? |
| 4 | **Accuracy** — Ensure personal data is complete, accurate, and not misleading | Data validation rules defined? |
| 5 | **Retention limitation** — Retain data only as long as necessary for the stated purpose, then erase | Retention period specified per data element? Erasure procedure defined? |
| 6 | **Reasonable security safeguards** — Protect personal data with appropriate technical and organizational measures | Encryption at rest and in transit? Access control defined? |

### Consent Requirements (Section 6)

| # | Requirement | Check |
|---|------------|-------|
| 1 | **Free, specific, informed, unconditional, unambiguous** consent with clear affirmative action | Consent UI/UX defined? Not bundled with T&C? |
| 2 | **Itemized consent** — Separate consent for each purpose if multiple purposes exist | Separate consent per data processing activity? |
| 3 | **Consent withdrawal** — Data Principal can withdraw consent at any time, as easily as giving it | Withdrawal mechanism defined and accessible? |
| 4 | **Notice before consent** — Provide notice in clear, plain language describing data and purpose | Notice content defined? Available in English and scheduled Indian languages? |

### Rights of Data Principal (Section 11-14)

| # | Right | Check |
|---|------|-------|
| 1 | **Right to access** — Summary of personal data being processed and processing activities | Access/download mechanism defined? |
| 2 | **Right to correction and erasure** — Request correction of inaccurate/incomplete data, erasure of data no longer needed | Edit and delete workflows defined? |
| 3 | **Right to grievance redressal** — Nominate a grievance officer, respond within prescribed time | Grievance officer designated? Response SLA defined? |
| 4 | **Right to nominate** — Nominate another person to exercise rights in case of death/incapacity | Nomination mechanism considered? |

### Children's Data (Section 9) — CRITICAL

| # | Requirement | Check |
|---|------------|-------|
| 1 | **Verifiable guardian consent** — Before processing any child's data, obtain verifiable consent from parent/guardian | Guardian consent mechanism defined? Age verification present? |
| 2 | **No tracking or behavioral monitoring** — Must not track, monitor, or do behavioral analysis of children | Feature does not profile children beyond stated purpose? |
| 3 | **No targeted advertising** — Must not target advertising at children | No ad-related data collection or usage? |
| 4 | **No detrimental processing** — Must not process data in a manner that causes detrimental effect to a child | No public ranking, shaming, or disadvantaging features? |

### Data Breach Notification (Section 8(6))

| # | Requirement | Check |
|---|------------|-------|
| 1 | **Notify Data Protection Board** — In the event of a personal data breach, inform the Board in prescribed manner | Breach notification procedure defined? |
| 2 | **Notify affected Data Principals** — Inform each affected individual | User notification mechanism defined? |

### Penalties (Section 33)

| Violation | Maximum Penalty |
|-----------|----------------|
| Failure to take security safeguards (breach) | Rs 250 crore |
| Failure to notify breach | Rs 200 crore |
| Non-compliance with children's data provisions | Rs 200 crore |
| Non-compliance with Data Fiduciary obligations | Rs 150 crore |
| Non-compliance with additional Significant Data Fiduciary obligations | Rs 150 crore |

## Output Format

```markdown
# DPDP Compliance Audit Report

**Spec:** {spec file}
**Feature:** {feature name}
**Audited:** {DD-MM-YYYY}
**Regulation:** Digital Personal Data Protection Act, 2023 (India)

## 1. Data Element Inventory

| # | Data Element | Category | Personal Data? | Source | Purpose | Retention |
|---|-------------|----------|---------------|--------|---------|-----------|
| 1 | User name | Identity | Yes | {spec section} | Personalization | Account lifetime |
| 2 | Usage duration | Activity | Yes (linkable) | {spec section} | Analytics | 2 years |

## 2. DPDP Compliance Check

| # | Data Element | DPDP Section | Requirement | Status | Gap |
|---|-------------|-------------|-------------|--------|-----|
| 1 | User name | S.6 | Consent — free, specific, informed | Compliant | — |
| 2 | User name | S.8(3) | Retention limitation | Gap | No retention period defined |
| 3 | User name | S.8(4) | Erasure after purpose fulfilled | Gap | No erasure workflow defined |
| 4 | Child age | S.9 | Verifiable guardian consent | Compliant | — |

## 3. Children's Data Audit (Section 9)

| # | Requirement | Status | Evidence | Gap |
|---|------------|--------|----------|-----|
| 1 | Guardian consent mechanism | Compliant/Gap | {description} | {if gap} |
| 2 | No tracking/behavioral monitoring | Compliant/Gap | {description} | {if gap} |
| 3 | No targeted advertising | Compliant/Gap | {description} | {if gap} |
| 4 | No detrimental processing | Compliant/Gap | {description} | {if gap} |

## 4. Data Principal Rights Check

| # | Right | DPDP Section | Mechanism Defined? | Status |
|---|------|-------------|-------------------|--------|
| 1 | Access | S.11 | {yes/no} | Compliant/Gap |
| 2 | Correction & Erasure | S.12 | {yes/no} | Compliant/Gap |
| 3 | Grievance Redressal | S.13 | {yes/no} | Compliant/Gap |
| 4 | Nomination | S.14 | {yes/no} | Compliant/Gap |

## 5. Masking & Security Audit

| # | Data Element | Masking Required? | Masking Method | At Rest Encryption | In Transit Encryption | Status |
|---|-------------|-------------------|----------------|--------------------|-----------------------|--------|

## 6. Summary

| Status | Count |
|--------|-------|
| Compliant | {N} |
| Needs Review | {N} |
| Gap (Must Fix) | {N} |

**Penalty Exposure:** {estimated based on gap severity}

## 7. Required Actions

### Gaps (Must Fix Before Review)
1. **{Data Element} — DPDP S.{section} — {Requirement}**
   Gap: {description}
   Fix: {specific action to add to the spec}
   Penalty risk: {relevant penalty from Section 33}

### Needs Review (Discuss with Legal)
1. **{Data Element} — DPDP S.{section}**
   Question: {what needs clarification}
```

## Rules

1. **When in doubt, flag it** — Classify uncertain data as personal data and flag for review
2. **Linkable data is personal data** — Data linkable to a specific person (even via session ID) is personal data under DPDP
3. **Children = strictest requirements** — Section 9 applies to all individuals under 18. No exceptions.
4. **Analytics events are data** — Event tracking creates personal data about user behavior. Include in audit.
5. **Don't assume compliance** — If a policy isn't explicitly stated in the spec, it's a gap
6. **Consent must be granular** — Bundled consent (buried in T&C) does not satisfy Section 6
7. **Retention must be finite** — "Account lifetime" is not acceptable without a defined account deletion policy

## Anti-Patterns

- Don't skip the children's data audit — Section 9 penalties are up to Rs 200 crore
- Don't treat consent as a checkbox — DPDP requires free, specific, informed consent
- Don't assume "anonymized" data is exempt — verify the anonymization is irreversible
- Don't ignore Data Principal rights — access, correction, erasure, and grievance mechanisms are mandatory

## Quality Checklist

- [ ] Every data element from the spec is inventoried
- [ ] Personal data classification applied to each element
- [ ] DPDP sections mapped per element
- [ ] Children's data audit completed (Section 9)
- [ ] Data Principal rights check completed (Sections 11-14)
- [ ] Consent mechanism verified (Section 6)
- [ ] Retention periods specified (Section 8(3))
- [ ] Security safeguards defined (Section 8(4))
- [ ] Masking and encryption audit completed
- [ ] Gaps have specific fix recommendations with penalty references
