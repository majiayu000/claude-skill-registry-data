---
name: audit-pipeline
description: Skill guidance for audit pipeline.
---




## STANDARD OPERATING PROCEDURE

### Purpose
Run a three-stage quality pipeline that first exposes theater, then proves functionality through sandbox execution, and finally polishes style and maintainability. This skill acts as the coordinator that composes `theater-detection-audit`, `functionality-audit`, and `style-audit` into a single evidential workflow.

### Trigger Conditions
- **Positive:** requests to run a full quality sweep, hardening a codebase before release, or combining multiple audits into one run.
- **Negative:** simple linting-only asks, documentation-only reviews, or tasks better handled by a single downstream audit.

### Guardrails
- **Confidence ceiling rule (Prompt Architect):** Always include `Confidence: X.XX (ceiling: TYPE Y.YY)` using ceilings {inference/report: 0.70, research: 0.85, observation/definition: 0.95}.
- **Structure-first (Skill Forge):** Ensure `examples/` and `tests/` are populated for downstream audits; log any gaps and remediate before completion.
- **Evidence-first:** Each phase must emit file:line references, observed metrics, and explicit standards/thresholds.
- **Dogfooding loop:** Re-run phases after fixes until deltas stabilize (<2% new findings) or risks are documented.

### Execution Phases
1. **Intake & Routing**
   - Capture repository context, target branch, and release goals.
   - Confirm pipeline order (theater → functionality → style) and reroute if scope is single-phase.
2. **Phase 1 – Theater Detection Audit**
   - Invoke `theater-detection-audit` to flag stubs, placeholders, and mock responses.
   - Collect blocking items and ensure fixes or waivers before moving on.
3. **Phase 2 – Functionality Audit**
   - Run `functionality-audit` with sandbox execution; prioritize failing paths revealed in Phase 1.
   - Record test artifacts, logs, and reproduction steps.
4. **Phase 3 – Style Audit**
   - Execute `style-audit` after functionality passes to refactor safely.
   - Require each finding to include rule references and before/after guidance.
5. **Validation & Handoff**
   - Confirm all phases report evidence, confidence, and remediation paths.
   - Summarize residual risks and next actions; store artifacts in the project’s memory namespace.

### Output Format
- Summary of pipeline intent, scope, and ordering decisions.
- Phase-by-phase findings with file:line evidence, metrics, and mapped standards.
- Fix recommendations grouped by severity and dependency (blocking vs. follow-up).
- Final confidence statement with ceiling.

### Validation Checklist
- [ ] Pipeline order confirmed and documented.
- [ ] Each phase executed or consciously skipped with rationale.
- [ ] Evidence captured (file:line, metrics, standards) for every finding.
- [ ] Dogfooding loop run or convergence noted (<2% delta).
- [ ] Confidence statement uses explicit ceiling and English-only output.

Confidence: 0.70 (ceiling: inference 0.70) - SOP rewritten to align with Prompt Architect confidence discipline and Skill Forge structure-first orchestration.
