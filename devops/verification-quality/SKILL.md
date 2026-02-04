---
name: verification-quality
description: Verify outputs and claims for accuracy, grounding, and policy compliance with explicit evidence and confidence ceilings.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - TodoWrite
model: sonnet
x-version: 3.2.0
x-category: quality
x-vcl-compliance: v3.1.1
x-cognitive-frames:
  - HON
  - MOR
  - COM
  - CLS
  - EVD
  - ASP
  - SPC
---




## STANDARD OPERATING PROCEDURE

### Purpose
Assess whether delivered outputs are correct, well-grounded, and policy-compliant by tracing evidence, checking constraints, and calibrating confidence.

### Trigger Conditions
- **Positive:** validating generated content, checking analysis against sources, or confirming policy compliance before delivery.
- **Negative:** code execution debugging (use functionality-audit) or style-only work (use style-audit).

### Guardrails
- **Confidence ceiling:** Always emit `Confidence: X.XX (ceiling: TYPE Y.YY)` with ceilings {inference/report 0.70, research 0.85, observation/definition 0.95}.
- **Evidence mapping:** Link each claim to source evidence with citations or file:line references; flag ungrounded assertions.
- **Constraint coverage:** Verify hard/soft/inferred constraints separately; note unresolved inferences.
- **Structure-first:** Maintain examples/tests demonstrating grounding checks and policy validation.

### Execution Phases
1. **Scope & Constraints**
   - Extract requirements and constraints from the request; categorize as hard, soft, inferred.
   - Identify allowed sources and policies.
2. **Evidence Collection**
   - Gather direct evidence (files, logs, references) and map to claims.
   - Note gaps or conflicts in evidence.
3. **Assessment**
   - For each claim, rate correctness, grounding strength, and policy alignment.
   - Distinguish observation vs. inference; cap confidence accordingly.
4. **Reporting & Remediation**
   - Summarize compliant items, violations, and uncertainties with recommended actions.
   - Provide confidence with explicit ceiling and English-only output.

### Output Format
- Constraint breakdown (hard/soft/inferred) and scope.
- Claim-by-claim verification table with evidence and confidence.
- Violations or gaps with remediation steps.
- Confidence statement using ceiling syntax.

### Validation Checklist
- [ ] Constraints extracted and categorized; policies identified.
- [ ] Evidence linked to each claim; gaps flagged.
- [ ] Confidence capped by evidence type; ceilings stated.
- [ ] Remediation steps proposed for violations.
- [ ] Output in English with explicit confidence ceiling.

Confidence: 0.72 (ceiling: inference 0.70) - SOP rewritten leveraging Prompt Architect confidence and constraint extraction plus Skill Forge structure-first verification.
