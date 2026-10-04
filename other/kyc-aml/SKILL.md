---
description: Assess KYC/AML/BSA compliance — customer identification, transaction monitoring, suspicious activity reporting
---

# KYC/AML/BSA Assessment

Assess Know Your Customer (KYC), Anti-Money Laundering (AML), and Bank Secrecy Act (BSA) compliance for "$ARGUMENTS". Evaluate customer identification, due diligence, transaction monitoring, and suspicious activity reporting programs.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **Customer Identification Program (CIP):**
   - Assess identity verification procedures for all account types (individual, business, beneficial owners)
   - Evaluate identification methods (documentary, non-documentary, combination)
   - Review minimum information collected (name, date of birth, address, identification number)
   - Assess record retention for CIP documentation (5-year requirement)
   - Evaluate procedures for customers who cannot be adequately identified

3. **Customer Due Diligence (CDD) and Enhanced Due Diligence (EDD):**
   - Assess standard CDD procedures (customer risk rating, nature and purpose of relationship)
   - Evaluate risk-based approach to CDD (low, medium, high risk categories)
   - Review EDD triggers and procedures for higher-risk customers (PEPs, high-risk jurisdictions, complex structures)
   - Assess ongoing monitoring and periodic review cadence based on risk rating
   - Evaluate beneficial ownership identification and verification (25% threshold, control prong)

4. **Beneficial ownership requirements:**
   - Assess compliance with FinCEN Beneficial Ownership Rule (CDD Rule)
   - Evaluate procedures for identifying and verifying beneficial owners of legal entity customers
   - Review Corporate Transparency Act (CTA) readiness and BOI reporting awareness
   - Assess record-keeping and update triggers for beneficial ownership changes

5. **Transaction monitoring systems and rules:**
   - Assess automated transaction monitoring system configuration and tuning
   - Evaluate alert generation rules and thresholds for unusual activity patterns
   - Review alert disposition workflow (investigation, escalation, closure, documentation)
   - Assess model risk management for monitoring systems (validation, back-testing)
   - Evaluate coverage gaps (new products, channels, customer segments)

6. **Suspicious Activity Report (SAR) filing:**
   - Assess SAR decision-making process and documentation
   - Evaluate filing timeliness (30-day initial detection, 60-day if no suspect identified)
   - Review SAR narrative quality and completeness
   - Assess continuing activity reporting procedures (90-day reviews)
   - Evaluate SAR confidentiality safeguards

7. **Currency Transaction Report (CTR) requirements:**
   - Assess CTR filing procedures for transactions exceeding $10,000
   - Evaluate aggregation rules for multiple transactions by or on behalf of the same person
   - Review exemption procedures (Phase I and Phase II exempt persons)
   - Assess timeliness of filing (15 calendar days)

8. **OFAC sanctions screening:**
   - Assess OFAC screening integration points (onboarding, transactions, periodic rescreening)
   - Evaluate screening system coverage (SDN list, sectoral sanctions, country programs)
   - Review match resolution and false positive handling procedures
   - Assess escalation procedures for potential true matches
   - Evaluate interdiction capabilities for real-time transaction blocking

9. **AML training program:**
   - Assess training scope (all employees, role-specific, board-level)
   - Evaluate training content currency and relevance
   - Review training frequency and completion tracking
   - Assess training effectiveness measurement

10. **BSA/AML officer and governance:**
    - Assess BSA/AML officer designation, qualifications, and authority
    - Evaluate reporting line and access to board/senior management
    - Review BSA/AML program documentation and board approval
    - Assess resource adequacy (staff, technology, budget)

11. **Independent testing/audit program:**
    - Assess scope and frequency of independent testing (risk-based, at minimum every 12-18 months)
    - Evaluate independence of testing function (internal audit or external party)
    - Review prior audit findings and remediation tracking
    - Assess regulatory examination history and MRA/MRIA status

12. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/kyc-aml.md` following the assessment template structure with:
    - **CIP Assessment** — identity verification coverage and adequacy
    - **CDD/EDD Program** — risk rating methodology and due diligence depth
    - **Beneficial Ownership** — identification, verification, and maintenance procedures
    - **Transaction Monitoring** — system coverage, alert management, and tuning effectiveness
    - **SAR/CTR Filing** — timeliness, quality, and process compliance
    - **OFAC Screening** — coverage, integration points, and match resolution
    - **Governance** — BSA officer, training, and independent testing
    - **Evidence Inventory** — existing evidence and evidence gaps
    - **Remediation Priorities** — ranked list of gaps to address

## Output

The KYC/AML/BSA assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/kyc-aml.md`. Present a summary to the user highlighting:
- Overall BSA/AML program maturity assessment
- Transaction monitoring coverage and alert management effectiveness
- SAR filing quality and timeliness metrics
- Top 3 gaps requiring remediation
