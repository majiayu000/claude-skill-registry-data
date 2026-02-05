---
name: connascence-quality-gate
description: Enforce connascence-based quality gates by detecting harmful coupling and demanding refactoring plans with evidence.
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
Assess code for forms of connascence (name, type, meaning, timing, algorithm, position, execution) and enforce remediation gates before merge.

### Trigger Conditions
- **Positive:** reviews focused on coupling/maintainability risk, architectural refactors, or release gates that target hidden dependencies.
- **Negative:** pure functionality debugging (use functionality-audit) or cosmetic linting only.

### Guardrails
- **Confidence ceiling:** include `Confidence: X.XX (ceiling: TYPE Y.YY)` with ceilings {inference/report 0.70, research 0.85, observation/definition 0.95}.
- **Evidence-first:** Each connascence finding must cite file:line, connascence type, and impact (risk or cost) with a proposed decoupling strategy.
- **Structure-first:** Maintain examples and tests that show both detection and approved remediation patterns.
- **Adversarial validation:** Challenge borderline cases (intentional coupling, domain invariants) and mark waivers explicitly.

### Execution Phases
1. **Context & Scope**
   - Identify modules or features under review and allowed coupling (domain invariants, protocol guarantees).
   - Exclude generated/vendor code unless coupling leaks into product code.
2. **Detection & Classification**
   - Scan for each connascence type; record evidence with severity (high if change ripple or hidden temporal ordering).
   - Note systemic patterns (shared globals, positional parameters, synchronized deployments).
3. **Remediation Design**
   - Propose refactors (interfaces, adapters, events, typed contracts, configuration) and expected impact.
   - Sequence fixes to minimize blast radius; align with product timelines.
4. **Validation & Gate Decision**
   - Require at least one mitigation path per critical finding before approval.
   - Document waivers with rationale and expiry; state confidence with ceiling.

### Output Format
- Scope summary and allowed/forbidden coupling rules.
- Finding list with connascence type, file:line evidence, impact, and remediation.
- Gate decision (approve/block/waiver) with reasoning.
- Confidence statement using ceiling syntax.

### Validation Checklist
- [ ] Scope and exemptions captured.
- [ ] Each finding includes connascence type, evidence, and remediation.
- [ ] Waivers include expiry and owner; blockers flagged.
- [ ] Examples/tests updated or queued.
- [ ] Confidence ceiling provided; English-only output.

Confidence: 0.71 (ceiling: inference 0.70) - SOP rewritten with Prompt Architect confidence discipline and Skill Forge structure-first guardrails.
