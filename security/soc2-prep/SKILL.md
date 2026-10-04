---
description: Prepare for SOC 2 audit — policies, controls, evidence collection
---

# SOC 2 Preparation

Prepare for a SOC 2 audit for "$ARGUMENTS". Select trust services criteria, conduct gap analysis, identify required policies and controls, and design an evidence collection plan.

> **Note:** AI-generated legal content does not constitute legal advice. Consult a qualified attorney.

## Prerequisites

Check that `.metapowers/legal/$ARGUMENTS/00-assess.md` exists. If it does not exist, stop and tell the user:

> "Run an Assess skill first (e.g. `/legal:risk-assessment $ARGUMENTS`) to generate the prerequisite assessment artifact."

If the user passes `--skip-checks`, bypass this check and log the skip to `.metapowers/legal/$ARGUMENTS/skip-log.md` with a timestamp and the reason "Prerequisite check skipped for soc2-prep".

## Process

1. **Read inputs:**
   - Read `.metapowers/legal/$ARGUMENTS/00-assess.md` for risk, jurisdiction, and data practice context
   - Read any existing security or compliance artifacts in `.metapowers/legal/$ARGUMENTS/` for additional context

2. **Select trust services criteria:**
   - **Security (CC)** — mandatory for all SOC 2 reports (common criteria)
   - **Availability (A)** — recommend if SLA commitments exist, customer-facing services, uptime guarantees
   - **Processing Integrity (PI)** — recommend if data processing accuracy is critical (financial, healthcare)
   - **Confidentiality (C)** — recommend if handling confidential business information, trade secrets, or client data
   - **Privacy (P)** — recommend if processing personal information (note overlap with GDPR/CCPA)
   - Document rationale for each selected/excluded criterion based on business needs and customer expectations

3. **Conduct gap analysis against each selected criterion:**
   - Map existing controls to SOC 2 criteria points
   - Identify criteria with no existing controls (gaps)
   - Identify criteria with partial controls (weaknesses)
   - Assess control design effectiveness vs. operating effectiveness
   - Rate each gap by severity (critical, high, medium, low)

4. **Identify required policies:**
   - **Information Security Policy** — overarching security program, roles, responsibilities
   - **Access Control Policy** — user provisioning, deprovisioning, least privilege, MFA, access reviews
   - **Change Management Policy** — change request, approval, testing, deployment, rollback procedures
   - **Incident Response Policy** — detection, response, communication, post-mortem
   - **Risk Assessment Policy** — risk identification, evaluation, treatment, acceptance criteria
   - **Vendor Management Policy** — vendor assessment, monitoring, contractual requirements
   - **Data Classification Policy** — classification levels, handling requirements per level
   - **Acceptable Use Policy** — permitted use of company systems, monitoring, enforcement
   - **Business Continuity/Disaster Recovery Policy** — BCP/DR planning, testing, recovery objectives (RTO/RPO)
   - Document which policies exist, which need creation, and which need updates

5. **Map existing controls to criteria:**
   - Create a control matrix mapping each SOC 2 criterion to specific controls
   - Identify control owners for each control
   - Document control frequency (continuous, daily, weekly, monthly, quarterly, annual)
   - Note whether controls are preventive, detective, or corrective

6. **Identify control gaps:**
   - List all criteria without adequate controls
   - Recommend new controls for each gap
   - Prioritize control implementation by risk and audit timeline
   - Estimate implementation effort (quick wins vs. significant projects)

7. **Design evidence collection plan:**
   - For each control, define: what evidence is needed, how often it must be collected, who is responsible for collection, where evidence is stored
   - Types of evidence: system configurations, access logs, approval records, policy documents, training records, vulnerability scans, penetration test reports, change tickets, incident reports
   - Evidence retention requirements (minimum: audit period plus reasonable buffer)
   - Automation opportunities (GRC platform, automated screenshot collection, API-based evidence gathering)

8. **Create audit readiness timeline:**
   - Gap remediation milestones
   - Policy drafting and approval timeline
   - Control implementation and testing schedule
   - Evidence collection dry run
   - Pre-audit readiness assessment
   - Audit window (Type I vs. Type II considerations and observation period)

9. **Recommend auditor selection criteria:**
   - SOC 2 audit experience and volume
   - Industry expertise relevant to the business
   - AICPA peer review status
   - Cost and engagement model
   - Communication and reporting style
   - References from similar organizations

10. **Write the artifact** to `.metapowers/legal/$ARGUMENTS/03-comply.md` with frontmatter:

    ```
    ---
    description: SOC 2 audit preparation for $ARGUMENTS
    ---
    ```

    Include sections:
    - **Trust Services Criteria Selection** — selected criteria with rationale
    - **Gap Analysis** — criterion-by-criterion assessment
    - **Required Policies** — inventory with status (exists, needs update, needs creation)
    - **Control Matrix** — controls mapped to criteria with owners and frequency
    - **Control Gaps** — gaps with recommended controls and priority
    - **Evidence Collection Plan** — per-control evidence requirements
    - **Audit Readiness Timeline** — milestone-based preparation schedule
    - **Auditor Selection Criteria** — evaluation framework
    - **Compliance Gaps** — identified gaps with remediation recommendations

## Output

The SOC 2 preparation plan written to `.metapowers/legal/$ARGUMENTS/03-comply.md`. Present a summary to the user highlighting:
- Trust services criteria selected and rationale
- Number of gaps identified by severity
- Policies requiring creation or update
- Key control gaps and recommended remediation
- Estimated audit readiness timeline
