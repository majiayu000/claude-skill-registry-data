---
name: legal-soc2-prep
description: Prepare for a SOC 2 audit — trust services criteria selection, required policies, a control matrix with owners, an evidence collection plan, a readiness timeline and auditor selection criteria. Use when the user has decided to pursue SOC 2 and needs the policy set, control matrix and timeline to get there. Not for a scored control-gap assessment; see /compliance-soc2.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: legal
  phase: 3
  artifact: 03-comply.md
---

# SOC 2 Preparation

Prepare for a SOC 2 audit for "$ARGUMENTS". Select trust services criteria, conduct gap analysis, identify required policies and controls, and design an evidence collection plan.

See also `/compliance-soc2` for a scored control-gap assessment of SOC 2 readiness and Type I vs. Type II fit.

> **Note:** AI-generated legal content does not constitute legal advice. Consult a qualified attorney.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"legal-soc2-prep","workflow":"legal","phase":3,"project":"<project>","event":"skipped","artifact":"03-comply.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 3 (Comply) of the Legal Lifecycle workflow (`legal`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `legal` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"legal-soc2-prep","workflow":"legal","phase":3,"project":"<project>","event":"refused","artifact":"03-comply.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"legal-soc2-prep","workflow":"legal","phase":3,"project":"<project>","event":"started","artifact":"03-comply.md","note":""}`.

Check that `.singularskills/legal/<project>/00-assess.md` exists. If it does not exist, stop and tell the user:

> "Run an Assess skill first (e.g. `/legal-risk-assessment <project>`) to generate the prerequisite assessment artifact."

## Process

1. **Read inputs:**
   - Read `.singularskills/legal/<project>/00-assess.md` for risk, jurisdiction, and data practice context
   - Read any existing security or compliance artifacts in `.singularskills/legal/<project>/` for additional context

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

10. **Write the artifact** — append to `.singularskills/legal/<project>/03-comply.md` under a `## SOC 2 Preparation` section. Create the file with a `# Comply — <project>` heading if it does not exist; if a `## SOC 2 Preparation` section already exists, replace only that section. The section contains:

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

The SOC 2 preparation plan appended to `.singularskills/legal/<project>/03-comply.md`. Present a summary to the user highlighting:
- Trust services criteria selected and rationale
- Number of gaps identified by severity
- Policies requiring creation or update
- Key control gaps and recommended remediation
- Estimated audit readiness timeline

**Record the run.** After you have written your section, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"legal-soc2-prep","workflow":"legal","phase":3,"project":"<project>","event":"finished","artifact":"03-comply.md","note":""}`.

This artifact is shared by every skill of phase 3 (Comply). The frontmatter is written once, by whoever creates the file: if you create it, open it with the block below (`skill` is the phase title, `started` the time of that first write; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`); if it already exists, leave the block alone except to update `finished` and to set `gate` to the worst value among the sections (`skipped` over `passed`).

```yaml
---
skill: Comply
workflow: legal
phase: 3
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

Open your `## SOC 2 Preparation` section with one italic line, `*<skill name> · <ISO timestamp> · gate: <passed|skipped>*` (your skill name is `legal-soc2-prep`).

End your section with `### Decisions` and `### Open questions` (one level under your `## SOC 2 Preparation` heading, so the section stays one block), in this shape:

```markdown
### Decisions
- <what was chosen> — <why> — <what was rejected>

### Open questions
- <what the next phase or a reviewer must settle>
```
