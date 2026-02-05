---
name: sop-dogfooding-quality-detection
description: SOP for detecting quality regressions during dogfooding runs and turning them into actionable fixes.
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
Identify quality regressions and latent issues while dogfooding, ensuring findings are evidenced, prioritized, and fed back into improvement loops.

### Trigger Conditions
- **Positive:** active dogfooding sessions, regression sweeps after releases, or monitoring new features for emergent issues.
- **Negative:** isolated bug triage without self-application or pattern capture.

### Guardrails
- **Confidence ceiling:** Use `Confidence: X.XX (ceiling: TYPE Y.YY)` with ceilings {inference/report 0.70, research 0.85, observation/definition 0.95}.
- **Evidence-first:** Record file:line, logs, metrics, or reproduction steps for each detected issue.
- **Structure-first:** Update examples/tests to reflect newly detected regressions and their fixes.
- **Prioritization:** Tag severity and blast radius; block release on critical regressions until resolved or waived with rationale.

### Execution Phases
1. **Observation & Capture**
   - Monitor outputs, logs, and behaviors during dogfooding; collect anomalies.
   - Normalize entries with severity, location, and reproduction notes.
2. **Validation & Classification**
   - Reproduce findings; distinguish false positives and intentional behavior.
   - Map to categories (correctness, performance, UX, security, reliability).
3. **Remediation & Feedback**
   - Propose fixes and owners; add tests to prevent recurrence.
   - Feed learnings into pattern retrieval and references.
4. **Confidence & Closure**
   - Confirm fixes or document waivers; state residual risk and confidence with ceiling.

### Output Format
- Log of detected issues with evidence and severity.
- Reproduction steps and validation results.
- Remediation plan and test updates.
- Confidence statement using ceiling syntax.

### Validation Checklist
- [ ] Evidence captured with location/steps for each issue.
- [ ] False positives filtered; categories assigned.
- [ ] Fixes/tests identified and owners named.
- [ ] Patterns/references updated where applicable.
- [ ] Confidence ceiling provided; English-only output.

Confidence: 0.70 (ceiling: inference 0.70) - SOP rewritten per Prompt Architect confidence discipline and Skill Forge structure-first detection loop.
