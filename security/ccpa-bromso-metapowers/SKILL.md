---
description: Assess CCPA/CPRA compliance — consumer rights, opt-out, deletion, service provider agreements
---

# CCPA/CPRA Assessment

Assess California Consumer Privacy Act (CCPA) and California Privacy Rights Act (CPRA) compliance for "$ARGUMENTS". Evaluate consumer rights, opt-out mechanisms, data handling practices, and service provider agreements.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **Applicability threshold assessment:**
   - Assess annual gross revenue threshold ($25M+)
   - Evaluate personal information volume threshold (100,000+ consumers/households/devices)
   - Assess revenue derived from selling/sharing personal information (50%+ of revenue)
   - Determine if organization is a "business," "service provider," or "contractor"
   - Document applicability determination with rationale

3. **Consumer rights assessment:**
   - **Right to Know** — assess processes for disclosing categories and specific pieces of PI
   - **Right to Delete** — assess deletion request handling and exception application
   - **Right to Opt-Out of Sale/Sharing** — assess opt-out mechanisms and signal honoring
   - **Right to Correct** — assess correction request procedures
   - **Right to Limit Use of Sensitive PI** — assess sensitive PI identification and use limitation
   - Evaluate response timelines (45 days, 90-day extension)
   - Review identity verification procedures (reasonable security)
   - Assess authorized agent request handling

4. **Notice and transparency:**
   - Assess notice at collection (categories of PI, purposes, retention periods)
   - Evaluate "Do Not Sell or Share My Personal Information" link placement and functionality
   - Review financial incentive disclosures and opt-in consent
   - Assess privacy policy CCPA/CPRA-specific disclosures
   - Evaluate Global Privacy Control (GPC) signal recognition

5. **Service provider and contractor agreements:**
   - Review service provider agreements for required CCPA provisions
   - Assess contractor agreements and additional restrictions
   - Evaluate third-party data sharing agreements
   - Review subcontractor flow-down requirements
   - Assess due diligence procedures for downstream recipients

6. **Employee and B2B data obligations:**
   - Assess employee personal information handling (full CCPA rights apply)
   - Evaluate B2B contact personal information obligations
   - Review HR privacy notices and employee rights procedures

7. **Data retention and minimization:**
   - Assess data retention schedules per category of PI
   - Evaluate data minimization practices (collection limited to what is necessary)
   - Review purpose limitation compliance

8. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/ccpa.md` following the assessment template structure with:
   - **Applicability Determination** — threshold analysis and entity classification
   - **Consumer Rights Readiness** — score per right with process maturity
   - **Notice and Transparency** — collection notice, opt-out link, privacy policy status
   - **Service Provider Framework** — agreement coverage and adequacy
   - **Employee/B2B Data** — HR and B2B compliance status
   - **Data Retention** — schedule completeness and minimization practices
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The CCPA/CPRA assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/ccpa.md`. Present a summary to the user highlighting:
- Applicability determination and entity classification
- Consumer rights readiness across all six rights
- Overall compliance score
- Top 3 gaps requiring remediation
