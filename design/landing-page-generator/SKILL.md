---
name: landing-page-generator
description: Research-to-release SOP for high-conversion landing pages with validated copy, design, and deployment steps.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
model: sonnet
x-version: 3.2.0
x-category: delivery
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
Produce deployable landing pages that convert, using evidence-based research, structured copy, consistent design, and validated builds.

### Trigger Conditions
- **Positive:** requests for marketing/landing pages, CRO experiments, new product launches, or redesigns requiring copy + build + deploy.
- **Negative:** app-level feature builds (route to `feature-dev-complete`) or doc-only needs (route to `documentation`).

### Guardrails
- **Structure-first:** keep `examples/`, `tests/`, `resources/`, `references/` alongside `SKILL.md`.
- **Constraint extraction:** HARD (brand, CTA, compliance, timelines), SOFT (tone, visuals), INFERRED (audience segments) — confirm inferred.
- **Confidence ceilings:** `{inference/report:0.70, research:0.85, observation/definition:0.95}` for claims on conversion tactics and implementation safety.
- Separate **copy before design**; one page = one primary CTA; avoid leaking secrets in examples.

### Execution Phases
1. **Research & Positioning**
   - Gather audience insights, competitors, and current CRO patterns; log sources in `references/`.
   - Define single CTA, value props, and objections to address.
2. **Copy & IA**
   - Draft messaging using frameworks (AIDA/PAS/FAB); map sections and hierarchy.
   - Confirm tone/voice; store drafts and snippets in `examples/`.
3. **Design System Alignment**
   - Extract brand tokens (color, typography, spacing) from sources; avoid copying content.
   - Plan layout wireframe; capture assets in `resources/`.
4. **Build**
   - Implement page with accessibility and performance budget; keep code + tests paired.
   - Set analytics/feature flags if applicable; add screenshot baselines.
5. **Validate & Iterate**
   - Run lint/tests in `tests/`; verify responsive/RTL/localization if in scope.
   - Check lighthouse/perf; confirm tracking events.
6. **Deploy & Document**
   - Prepare deploy steps + rollback; publish release notes and QA checklist.
   - Record evidence, risks, and **Confidence: X.XX (ceiling: TYPE Y.YY)**.

### Output Format
- Constraints and decisions (HARD/SOFT/INFERRED) with confirmations.
- Copy outline, design tokens, build status, and validation results.
- Deploy/rollback plan and evidence links.
- Confidence statement with ceiling.

### Validation Checklist
- [ ] CTA and success metrics defined; constraints confirmed.
- [ ] Copy reviewed; design tokens captured; layout agreed.
- [ ] Tests + accessibility/performance checks recorded in `tests/`.
- [ ] Assets and research stored in `resources/` and `references/`.
- [ ] Deployment + rollback documented; confidence ceilings attached.

### MCP / Memory Tags
- Namespace: `skills/delivery/landing-page-generator/{project}/{page}`
- Tags: `WHO=landing-page-generator-{session}`, `WHY=skill-execution`, `WHAT=cro+delivery`

Confidence: 0.70 (ceiling: inference 0.70) - SOP applies skill-forge structure-first and prompt-architect constraint/ceiling guidance.
