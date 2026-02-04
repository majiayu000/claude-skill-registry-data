---
name: dogfooding-system
description: Run continuous dogfooding loops that apply our own skills to themselves, measure deltas, and harvest reusable patterns.
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
Continuously exercise skills on themselves and on active projects to surface gaps, measure improvement deltas, and capture patterns for reuse across the quality suite.

### Trigger Conditions
- **Positive:** requests to self-validate skills, run continuous improvement loops, or harvest best practices from recent executions.
- **Negative:** single-run audits without feedback goals or feature work unrelated to skill quality.

### Guardrails
- **Confidence ceiling:** Report `Confidence: X.XX (ceiling: TYPE Y.YY)` using ceilings {inference/report 0.70, research 0.85, observation/definition 0.95}.
- **Structure-first:** Maintain `examples/`, `tests/`, and `resources/` that demonstrate dogfooding sessions and convergence tracking.
- **Adversarial validation:** Challenge results with boundary cases; do not declare convergence until delta <2% over two consecutive runs.
- **Logging & recall:** Tag MCP/memory artifacts with WHO/WHY to enable longitudinal analysis.

### Execution Phases
1. **Setup & Scope**
   - Choose target skill(s) and datasets; define success metrics and delta thresholds.
   - Prime memory namespace for the session and ingest prior runs.
2. **Self-Application Loop**
   - Apply the target skill to itself or to curated tasks; record findings, gaps, and fixes.
   - Iterate until improvements plateau; note failures and anti-patterns.
3. **Adversarial Probes**
   - Inject edge cases, noise, and counterexamples to stress validation paths.
   - Capture false positives/negatives and adjust guardrails.
4. **Harvest & Publish**
   - Distill reusable patterns, playbooks, and scripts; update references/resources.
   - Summarize deltas, risks, and next steps with confidence ceiling.

### Output Format
- Scope, metrics, and target skills for the session.
- Iteration log with deltas, evidence, and remediation actions.
- Adversarial probe results and adjustments.
- Convergence summary, risks, and confidence statement.

### Validation Checklist
- [ ] Targets and metrics defined; memory namespace prepared.
- [ ] At least one self-application and one adversarial probe completed.
- [ ] Deltas measured; convergence or stopping condition documented.
- [ ] Patterns harvested into references/resources.
- [ ] Confidence ceiling included; English-only output.

Confidence: 0.73 (ceiling: inference 0.70) - SOP rewritten to combine Prompt Architect confidence discipline with Skill Forge dogfooding structure.
