---
name: verification-and-quality-assurance
description: Orchestrate verification and QA activities across requirements, design, implementation, and validation with traceable evidence.
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
Plan and execute verification and QA activities that prove conformance to requirements, validate user value, and document residual risk with traceability.

### Trigger Conditions
- **Positive:** project QA planning, release readiness assessments, or end-to-end verification requests.
- **Negative:** focused PR review (use code-review-assistant) or targeted functionality debugging (use functionality-audit).

### Guardrails
- **Confidence ceiling:** Provide `Confidence: X.XX (ceiling: TYPE Y.YY)` with ceilings {inference/report 0.70, research 0.85, observation/definition 0.95}.
- **Traceability:** Map tests and findings to requirements/stories; capture evidence (logs, screenshots, metrics).
- **Structure-first:** Maintain examples/tests reflecting verification matrices, exit criteria, and defect tracking.
- **Adversarial validation:** Include negative tests, boundary cases, and failure injection where applicable.

### Execution Phases
1. **Planning & Scope**
   - Identify requirements, acceptance criteria, environments, and stakeholders.
   - Define exit criteria and defect severity model.
2. **Design & Preparation**
   - Build verification matrix linking requirements to test types (unit, integration, system, UX, security).
   - Prepare environments, data, and tooling.
3. **Execution**
   - Run prioritized tests; capture evidence and defects with severity and reproduction steps.
   - Track coverage against the verification matrix.
4. **Evaluation & Handoff**
   - Summarize results, residual risks, and open defects with owners.
   - Recommend release go/no-go or conditions; state confidence with ceiling.

### Output Format
- Verification plan with scope, exit criteria, and traceability matrix.
- Execution log with evidence and defect list.
- Coverage summary and residual risks.
- Confidence statement using ceiling syntax.

### Validation Checklist
- [ ] Requirements and exit criteria documented with owners.
- [ ] Verification matrix built and referenced during execution.
- [ ] Evidence and defects captured with severity and reproduction steps.
- [ ] Coverage and risks summarized with release recommendation.
- [ ] Confidence ceiling provided; English-only output.

Confidence: 0.73 (ceiling: inference 0.70) - SOP rewritten to reflect Prompt Architect confidence discipline and Skill Forge structure-first verification.
