---
description: Assess SOC 2 Type II readiness — trust services criteria
---

# SOC 2 Assessment

Assess SOC 2 Type II readiness for "$ARGUMENTS". Evaluate control design and operating effectiveness across applicable trust services criteria, and determine Type I vs. Type II readiness.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **Trust services criteria scoping:**
   - Security (CC series) — always in scope, mandatory for all SOC 2 engagements
   - Availability (A series) — assess applicability based on SLAs and uptime commitments
   - Processing Integrity (PI series) — assess applicability based on data processing accuracy requirements
   - Confidentiality (C series) — assess applicability based on confidential data handling
   - Privacy (P series) — assess applicability based on personal information processing
   - Document scoping decisions with rationale

3. **Security (Common Criteria) assessment:**
   - **CC1: Control Environment** — assess tone at top, organizational structure, security policies
   - **CC2: Communication and Information** — assess internal/external communication of security
   - **CC3: Risk Assessment** — assess risk identification, analysis, and management processes
   - **CC4: Monitoring Activities** — assess ongoing monitoring, logging, alerting
   - **CC5: Control Activities** — assess control design, implementation, and technology controls
   - **CC6: Logical and Physical Access** — assess access controls, authentication, MFA, physical security
   - **CC7: System Operations** — assess change management, incident detection, incident response
   - **CC8: Change Management** — assess change authorization, testing, deployment processes
   - **CC9: Risk Mitigation** — assess risk mitigation strategies, vendor management, insurance
   - Score each criterion: control designed effectively / operating effectively / gap

4. **Additional criteria assessment** (for each in-scope criterion):
   - Assess control design against AICPA points of focus
   - Evaluate evidence of operating effectiveness over the observation period
   - Identify controls with design gaps vs. operating gaps
   - Document compensating controls where applicable

5. **Type I vs. Type II readiness:**
   - Assess if controls are designed effectively (Type I ready)
   - Assess if controls have been operating effectively for 3-12 months (Type II ready)
   - Identify controls needing a burn-in period before Type II audit
   - Recommend observation period length

6. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/soc2.md` following the assessment template structure with:
   - **Scope Decision** — applicable trust services criteria with rationale
   - **Common Criteria Assessment** — CC1-CC9 detailed scoring
   - **Additional Criteria Assessment** — A/PI/C/P scoring (if in scope)
   - **Type I Readiness** — design effectiveness summary
   - **Type II Readiness** — operating effectiveness and burn-in status
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The SOC 2 assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/soc2.md`. Present a summary to the user highlighting:
- Trust services criteria in scope
- Type I vs. Type II readiness determination
- Overall readiness score
- Top 3 gaps requiring remediation before audit
