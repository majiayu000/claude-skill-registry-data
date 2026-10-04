---
description: Assess FedRAMP/StateRAMP readiness — impact levels, control baselines, 3PAO requirements
---

# FedRAMP/StateRAMP Assessment

Assess Federal Risk and Authorization Management Program (FedRAMP) and StateRAMP readiness for "$ARGUMENTS". Determine impact level, evaluate NIST SP 800-53 control baseline, and assess ATO package readiness.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **Impact level determination:**
   - Assess confidentiality, integrity, and availability impact levels per FIPS 199
   - Determine overall impact level: Low, Moderate, or High
   - Evaluate if FedRAMP Tailored (Li-SaaS) applies for low-impact SaaS
   - Document impact level determination with rationale

3. **NIST SP 800-53 control baseline assessment:**
   - **Access Control (AC)** — account management, access enforcement, separation of duties, least privilege, session controls, remote access, MFA
   - **Audit and Accountability (AU)** — audit events, content, storage, review, analysis, reporting, reduction, generation, protection
   - **Security Assessment and Authorization (CA)** — security assessment plan, POA&M, continuous monitoring, penetration testing
   - **Configuration Management (CM)** — baseline configuration, change control, least functionality, software restrictions, configuration settings
   - **Contingency Planning (CP)** — contingency plan, training, testing, alternate processing/storage, system recovery
   - **Identification and Authentication (IA)** — user identification, authenticator management, device identification, MFA
   - **Incident Response (IR)** — incident response plan, training, testing, handling, monitoring, reporting
   - **Maintenance (MA)** — controlled maintenance, tools, remote maintenance, personnel
   - **Media Protection (MP)** — media access, marking, storage, transport, sanitization
   - **Physical and Environmental Protection (PE)** — access authorizations, monitoring, visitor control, emergency procedures
   - **Planning (PL)** — security plan, system security plan update, rules of behavior
   - **Program Management (PM)** — information security program plan, senior security officer, risk management strategy
   - **Risk Assessment (RA)** — risk assessment, vulnerability scanning, risk response
   - **System and Communications Protection (SC)** — application partitioning, boundary protection, cryptographic protection, network disconnect
   - **System and Information Integrity (SI)** — flaw remediation, malicious code protection, security alerts, software integrity, information input validation, error handling, memory protection
   - Score each control family: implemented / partially implemented / planned / not implemented

4. **3PAO requirements:**
   - Identify qualified Third Party Assessment Organization (3PAO) requirements
   - Assess readiness for initial assessment
   - Evaluate continuous monitoring program for ongoing authorization
   - Review annual assessment requirements

5. **ATO package readiness:**
   - Assess System Security Plan (SSP) completeness
   - Review Plan of Action and Milestones (POA&M)
   - Evaluate Continuous Monitoring (ConMon) program
   - Assess Incident Response Plan
   - Review Security Assessment Report readiness
   - Evaluate supply chain risk management documentation

6. **StateRAMP considerations:**
   - Identify StateRAMP-specific requirements beyond FedRAMP
   - Assess state-specific data residency requirements
   - Review StateRAMP verification levels (Ready, Authorized, Authorized+)
   - Evaluate reciprocity opportunities between FedRAMP and StateRAMP

7. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/fedramp.md` following the assessment template structure with:
   - **Impact Level Determination** — FIPS 199 analysis and overall impact level
   - **Control Baseline Assessment** — scoring per NIST 800-53 control family
   - **3PAO Readiness** — assessment organization requirements and readiness
   - **ATO Package Status** — SSP, POA&M, ConMon, and documentation readiness
   - **StateRAMP Considerations** — additional requirements and verification level
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The FedRAMP/StateRAMP assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/fedramp.md`. Present a summary to the user highlighting:
- Impact level determination (Low/Moderate/High)
- Overall control baseline compliance score
- ATO package readiness percentage
- Top 3 gaps requiring remediation
- Estimated timeline to authorization readiness
