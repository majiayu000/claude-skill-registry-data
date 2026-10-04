---
description: Assess ISO 22301 business continuity management compliance
---

# ISO 22301 Assessment

Assess ISO 22301 Business Continuity Management System (BCMS) compliance for "$ARGUMENTS". Evaluate business impact analysis, continuity strategies, plans, exercise program, and documentation requirements.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **BCMS context and scope (Clauses 4-5):**
   - Assess organizational context for business continuity (internal/external issues, interested parties)
   - Evaluate BCMS scope definition (organizational units, locations, products/services)
   - Review leadership commitment and BC policy
   - Assess roles, responsibilities, and authorities for business continuity
   - Evaluate resource allocation and competency requirements

3. **Business Impact Analysis (BIA):**
   - Assess BIA methodology and completeness
   - Evaluate identification of prioritized activities and their dependencies
   - Review Maximum Tolerable Period of Disruption (MTPD) for each prioritized activity
   - Assess Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO)
   - Evaluate Minimum Business Continuity Objectives (MBCO)
   - Review resource requirements for recovery (people, facilities, technology, information, suppliers)
   - Assess BIA review and update cadence

4. **Risk assessment for disruption scenarios:**
   - Assess risk assessment methodology aligned with BIA findings
   - Evaluate threat identification across categories (natural, technological, human-caused, pandemic, supply chain)
   - Review likelihood and impact scoring for disruption scenarios
   - Assess risk treatment decisions (accept, mitigate, transfer, avoid)
   - Evaluate alignment between risk assessment outcomes and continuity strategies

5. **Business continuity strategies:**
   - **Prevention and mitigation:** Assess proactive measures to reduce disruption likelihood and impact
   - **Response strategies:** Evaluate immediate response procedures for prioritized activities
   - **Recovery strategies:** Assess strategies for restoring prioritized activities within RTO
   - Evaluate strategy options analysis (cost vs. risk reduction)
   - Review resource requirements for each strategy (alternate sites, technology, staffing)
   - Assess supply chain and third-party continuity considerations

6. **Business continuity plans:**
   - **Incident response procedures:** Assess initial response, escalation, and communication procedures
   - **Crisis management:** Evaluate crisis management team structure, decision-making, and stakeholder communication
   - **Recovery procedures:** Assess step-by-step recovery plans for prioritized activities
   - Review plan activation criteria and authority
   - Evaluate plan accessibility (offline access, distributed copies, mobile access)
   - Assess plan maintenance and version control procedures

7. **Exercise program:**
   - Assess exercise program scope and frequency
   - Evaluate exercise types: desktop/tabletop exercises, simulation exercises, full-scale exercises
   - Review exercise scenarios and coverage of disruption types
   - Assess post-exercise evaluation and lessons learned documentation
   - Evaluate corrective action tracking from exercise findings
   - Review exercise participation across organizational levels

8. **Performance evaluation and improvement (Clauses 9-10):**
   - Assess monitoring, measurement, analysis, and evaluation of BCMS effectiveness
   - Evaluate internal audit program for business continuity
   - Review management review process and outcomes
   - Assess continual improvement mechanisms and corrective action procedures

9. **Documentation assessment:**
   - Evaluate BC policy documentation
   - Assess BIA results documentation and currency
   - Review risk assessment documentation
   - Evaluate recovery strategies documentation
   - Assess BC plans documentation and accessibility
   - Review exercise records and post-exercise reports
   - Evaluate change management documentation for BCMS updates

10. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/iso22301.md` following the assessment template structure with:
    - **BCMS Framework** — context, scope, policy, and governance
    - **Business Impact Analysis** — methodology, MTPD/RTO/RPO coverage, and completeness
    - **Risk Assessment** — disruption scenarios, scoring, and treatment decisions
    - **Continuity Strategies** — prevention, response, and recovery approach
    - **BC Plans** — incident response, crisis management, and recovery procedures
    - **Exercise Program** — types, frequency, coverage, and lessons learned
    - **Performance Evaluation** — audit, review, and improvement mechanisms
    - **Documentation** — completeness and currency assessment
    - **Evidence Inventory** — existing evidence and evidence gaps
    - **Remediation Priorities** — ranked list of gaps to address

## Output

The ISO 22301 assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/iso22301.md`. Present a summary to the user highlighting:
- Overall BCMS maturity and certification readiness
- BIA completeness and RTO/RPO coverage across prioritized activities
- Exercise program effectiveness and coverage
- Top 3 gaps requiring remediation
