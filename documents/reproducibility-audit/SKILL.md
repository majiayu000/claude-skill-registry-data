---
name: reproducibility-audit
description: Verify that results, builds, and experiments can be reproduced consistently with documented steps and deterministic inputs.
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
Assess reproducibility across code, data, and build pipelines by validating deterministic processes, pinned dependencies, and documented steps.

### Trigger Conditions
- **Positive:** scientific/ML experiment verification, release build audits, or compliance checks requiring reproducible artifacts.
- **Negative:** stylistic reviews or runtime debugging (route to style-audit or functionality-audit).

### Guardrails
- **Confidence ceiling:** Append `Confidence: X.XX (ceiling: TYPE Y.YY)` using ceilings {inference/report 0.70, research 0.85, observation/definition 0.95}.
- **Evidence & determinism:** Require commands, seeds, data sources, and hashes for artifacts; rerun steps to confirm.
- **Structure-first:** Maintain examples/tests showing successful and failing reproduction attempts.
- **Adversarial validation:** Introduce clean environments and altered dependency versions to detect hidden variability.

### Execution Phases
1. **Inventory & Scope**
   - Identify targets (builds, experiments, reports) and required inputs (code revision, data, config, seeds).
   - Note environments (OS, container, hardware) and expected outcomes.
2. **Replay & Measurement**
   - Follow documented steps exactly; log commands, outputs, and timestamps.
   - Compare generated artifacts via hashes or checksums; capture diffs.
3. **Variability Probes**
   - Change environments/dependency versions within constraints to test stability.
   - Document non-deterministic behaviors and their causes.
4. **Reporting & Remediation**
   - Summarize reproduction success/failure, missing documentation, and proposed fixes (pinning, automation scripts, data versioning).
   - Provide confidence with ceiling and attach logs/hashes.

### Output Format
- Scope, inputs, environments, and expected results.
- Step-by-step replay log with evidence (commands, outputs, hashes).
- Variability findings and fixes.
- Confidence statement using ceiling syntax.

### Validation Checklist
- [ ] Inputs and environments captured with versions/seeds.
- [ ] Replay executed with logs and hashes recorded.
- [ ] Variability probes performed; nondeterminism documented.
- [ ] Remediation steps proposed and owners identified.
- [ ] Confidence ceiling provided; English-only output.

Confidence: 0.72 (ceiling: inference 0.70) - SOP rewritten per Prompt Architect confidence discipline and Skill Forge structure-first reproducibility focus.
