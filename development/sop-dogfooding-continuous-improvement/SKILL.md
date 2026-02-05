---
name: sop-dogfooding-continuous-improvement
description: SOP for running continuous improvement cycles via dogfooding and adversarial validation.
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
Provide a repeatable loop for applying our skills to themselves, measuring improvement deltas, and documenting learnings for continuous quality gains.

### Trigger Conditions
- **Positive:** periodic quality reviews, regression checks after major updates, or requests to improve a specific skill.
- **Negative:** single execution runs without improvement goals; ad-hoc debugging tasks.

### Guardrails
- **Confidence ceiling:** Add `Confidence: X.XX (ceiling: TYPE Y.YY)` with ceilings {inference/report 0.70, research 0.85, observation/definition 0.95}.
- **Structure-first:** Maintain examples/tests demonstrating the improvement loop and convergence criteria.
- **Adversarial validation:** Include boundary inputs and noisy cases before claiming convergence (<2% delta across two runs).
- **Evidence logging:** Tag artifacts with WHO/WHY and store metrics for trend analysis.

### Execution Phases
1. **Plan & Baseline**
   - Select the skill and metrics; capture current performance and known gaps.
   - Prepare memory namespace and retrieve prior runs.
2. **Self-Application & Iteration**
   - Apply the skill to itself or representative tasks; document findings and fixes.
   - Iterate until improvements plateau.
3. **Adversarial Probing**
   - Inject edge cases to test robustness; log false positives/negatives.
4. **Synthesis & Handoff**
   - Summarize deltas, remaining risks, and next steps.
   - Update references/resources and state confidence with ceiling.

### Output Format
- Baseline metrics and session goals.
- Iteration log with findings, fixes, and deltas.
- Adversarial probe outcomes and adjustments.
- Confidence statement and follow-up plan.

### Validation Checklist
- [ ] Baseline captured with metrics and scope.
- [ ] At least one self-application iteration completed.
- [ ] Adversarial probes executed; deltas measured.
- [ ] References/resources updated with learnings.
- [ ] Confidence ceiling provided; English-only output.

Confidence: 0.71 (ceiling: inference 0.70) - SOP rewritten using Prompt Architect confidence discipline and Skill Forge structure-first dogfooding pattern.
