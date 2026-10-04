---
description: Assess NIS2 Directive (EU 2022/2555) compliance — entity classification, risk management, incident reporting, supply chain
---

# NIS2 Assessment

Assess compliance with the NIS2 Directive (EU 2022/2555) for "$ARGUMENTS". Classify the entity, evaluate the 10 minimum security measures, assess incident reporting readiness, and score supply chain security.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **Entity classification:**
   - Determine if the entity is "essential" or "important" under NIS2 Article 3
   - Assess sector classification (Annex I high-criticality vs. Annex II other critical sectors)
   - Determine size thresholds (medium: 50+ employees or EUR 10M+ turnover; large: 250+ or EUR 50M+)
   - Document classification rationale and implications for obligations

3. **Assess 10 minimum measures (Article 21):**
   - **Risk analysis and information system security policies** — assess policy existence, scope, review cadence
   - **Incident handling** — assess detection, response, and recovery capabilities
   - **Business continuity and crisis management** — assess BCP, DR plans, backup management
   - **Supply chain security** — assess vendor risk management, contractual security requirements
   - **Network and information systems security** — assess acquisition, development, vulnerability handling
   - **Vulnerability disclosure** — assess coordinated vulnerability disclosure policies
   - **Cybersecurity risk management effectiveness** — assess measurement and evaluation practices
   - **Cryptography and encryption** — assess encryption policies and implementation
   - **Human resources security** — assess security awareness, training, access control policies
   - **Access control and asset management** — assess identity management, MFA, asset inventory
   - Score each measure: Compliant / Partially Compliant / Non-Compliant with evidence

4. **Incident reporting readiness (Article 23):**
   - Assess capability to issue early warning within 24 hours of awareness
   - Assess capability to submit incident notification within 72 hours
   - Assess capability to deliver final report within 1 month
   - Evaluate CSIRT communication channels and procedures
   - Test reporting workflow against scenario

5. **Supply chain security (Article 22):**
   - Assess critical supplier identification and risk assessment
   - Evaluate contractual security requirements with suppliers
   - Assess supply chain incident notification procedures
   - Review supplier audit and monitoring practices

6. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/nis2.md` following the assessment template structure with:
   - **Entity Classification** — essential vs. important, sector, size, obligations
   - **Minimum Measures Assessment** — detailed scoring of all 10 measures
   - **Incident Reporting Readiness** — 24hr/72hr/1mo capability assessment
   - **Supply Chain Security** — supplier risk management maturity
   - **Overall Compliance Score** — aggregate score with heatmap
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The NIS2 assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/nis2.md`. Present a summary to the user highlighting:
- Entity classification result
- Overall compliance score
- Top 3 gaps requiring remediation
- Incident reporting readiness status
