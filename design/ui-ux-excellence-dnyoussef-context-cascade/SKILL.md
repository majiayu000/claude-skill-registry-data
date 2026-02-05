---
name: ui-ux-excellence
description: Drive UI/UX audits and improvements with structured heuristics, user journeys, and validation gates.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - TodoWrite
model: claude-3-5-sonnet
x-version: 3.2.0
x-category: tooling
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


### L1 Improvement
- Recast the UX skill in Prompt Architect style with clear triggers, heuristics, and confidence ceilings.
- Added structure-first guardrails and validation steps aligned to Skill Forge.
- Clarified outputs (audit + prioritized fixes) with memory tagging.

## STANDARD OPERATING PROCEDURE

### Purpose
Evaluate and improve product UI/UX using heuristic reviews, user flows, accessibility checks, and prioritized fix plans.

### Trigger Conditions
- **Positive:** UX/UI audit, usability review, accessibility check, design critique, or journey optimization.
- **Negative:** branding-only requests (route to design specialists) or backend-only tasks.

### Guardrails
- Maintain structure-first docs (SKILL, README, examples/tests/references).
- Apply explicit heuristics: clarity, consistency, affordance, feedback, accessibility, performance.
- Confidence ceilings required; cite evidence (screens, flows, metrics).
- Memory tagging for audits and recommendations.

### Execution Phases
1. **Intent & Context** – Identify product area, target users, platforms, and success metrics.
2. **Heuristic Review** – Assess clarity, consistency, affordance, feedback, and accessibility; capture screenshots/notes.
3. **Journey Analysis** – Map critical flows; note friction points, latency, and error states.
4. **Prioritized Plan** – Rank issues by severity/impact/effort; propose design/UX changes.
5. **Validation** – Prototype or simulate fixes when possible; ensure accessibility (WCAG) and responsiveness.
6. **Delivery** – Provide findings, recommended changes, and confidence ceiling with memory keys.

### Output Format
- Audit summary, user flows assessed, key issues with evidence, and prioritized fixes.
- Accessibility/performance notes and suggested metrics to track.
- Confidence: X.XX (ceiling: TYPE Y.YY); memory namespace recorded.

### Validation Checklist
- [ ] Scope and personas defined; platforms noted.
- [ ] Heuristics applied with evidence; accessibility checked.
- [ ] Prioritized backlog includes impact/effort/owner.
- [ ] Confidence ceiling declared; memory tagged.

### Integration
- **Memory MCP:** `skills/tooling/ui-ux-excellence/{project}/{timestamp}` for audits and artifacts.
- **Hooks:** follow Skill Forge latency bounds; integrate with screenshot tooling when available.

Confidence: 0.70 (ceiling: inference 0.70) – SOP aligned to Prompt Architect clarity and Skill Forge guardrails.
