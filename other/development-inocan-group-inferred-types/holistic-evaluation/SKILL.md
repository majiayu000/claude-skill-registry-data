---
name: holistic-evaluation
description: Deliver a 360° evaluation of a codebase or feature, blending architecture, correctness, performance, security, and UX signals.
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
Synthesize multi-domain quality signals into a single assessment that highlights strengths, gaps, and prioritized actions across the stack.

### Trigger Conditions
- **Positive:** program-wide audits, pre-release hardening, or executive summaries that require broad coverage.
- **Negative:** narrow bug hunts or single-lens reviews (route to the appropriate specialized skill).

### Guardrails
- **Confidence ceiling:** Append `Confidence: X.XX (ceiling: TYPE Y.YY)` using ceilings {inference/report 0.70, research 0.85, observation/definition 0.95}.
- **Structured coverage:** Ensure each lens (architecture, correctness, security, performance, UX, docs/tests) has at least one observation or explicit “not evaluated.”
- **Evidence-first:** Provide file:line or metric references plus source standards (OWASP, budgets, style guides, SLAs).
- **Adversarial validation:** Stress-check conclusions against edge cases and potential blind spots; mark assumptions clearly.

### Execution Phases
1. **Scoping & Goals**
   - Define audiences (engineering leadership, QA, security) and decision horizon.
   - Identify critical components and recent changes.
2. **Lens-by-Lens Evaluation**
   - Architecture: cohesion/coupling, boundaries, migrations.
   - Correctness & Tests: functional behavior, coverage depth, flaky risk.
   - Security & Privacy: input validation, authZ/authN, secrets, data flows.
   - Performance & Reliability: latency budgets, resource usage, error budgets.
   - UX & Documentation: usability, accessibility, onboarding materials.
3. **Synthesis & Prioritization**
   - Group findings by severity and blast radius; highlight dependencies.
   - Recommend remediation plans with owners and timelines.
4. **Validation & Confidence**
   - Revisit high-risk areas with adversarial probes.
   - State residual risks and confidence with explicit ceiling.

### Output Format
- Scope and audience statement.
- Lens-by-lens findings with evidence and references.
- Prioritized remediation plan with owners and timelines.
- Residual risks and confidence statement with ceiling.

### Validation Checklist
- [ ] Audience and scope documented.
- [ ] Each lens evaluated or explicitly marked “not evaluated.”
- [ ] Evidence and references included for every finding.
- [ ] Prioritization and ownership assigned.
- [ ] Confidence ceiling provided; English-only output.

Confidence: 0.72 (ceiling: inference 0.70) - SOP rewritten with Prompt Architect confidence discipline and Skill Forge structured coverage.
