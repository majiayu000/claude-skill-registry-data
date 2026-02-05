---
name: sop-dogfooding-pattern-retrieval
description: SOP for retrieving, curating, and applying patterns discovered through dogfooding runs.
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
Systematically collect and reuse patterns, fixes, and heuristics learned from dogfooding sessions to accelerate future quality work.

### Trigger Conditions
- **Positive:** preparing playbooks, seeding new skills with proven patterns, or responding to repeated findings across projects.
- **Negative:** net-new explorations without prior data; one-off audits without reuse goals.

### Guardrails
- **Confidence ceiling:** Provide `Confidence: X.XX (ceiling: TYPE Y.YY)` using ceilings {inference/report 0.70, research 0.85, observation/definition 0.95}.
- **Evidence-backed entries:** Each pattern must include source session, file:line or log evidence, applicability, and limitations.
- **Structure-first:** Maintain curated examples/tests that demonstrate pattern application and failure modes.
- **Versioning:** Track pattern versions and deprecate superseded items.

### Execution Phases
1. **Harvest**
   - Pull artifacts from recent dogfooding runs; tag by skill, domain, and risk class.
   - Extract candidate patterns with context and triggers.
2. **Curate & Validate**
   - Consolidate duplicates; validate on at least one fresh example.
   - Record constraints and anti-patterns.
3. **Publish & Wire-in**
   - Add patterns to references/resources; update examples/tests accordingly.
   - Communicate availability and intended use to downstream skills.
4. **Review & Confidence**
   - Schedule periodic reviews to retire stale patterns.
   - State confidence with ceiling and note coverage gaps.

### Output Format
- Pattern catalog entries with source, evidence, applicability, and limitations.
- Validation notes and example usage.
- Change log for additions/removals.
- Confidence statement using ceiling syntax.

### Validation Checklist
- [ ] Source sessions and evidence recorded.
- [ ] Patterns validated on fresh examples.
- [ ] Examples/tests updated to reflect patterns and pitfalls.
- [ ] Versioning and retirement tracked.
- [ ] Confidence ceiling provided; English-only output.

Confidence: 0.70 (ceiling: inference 0.70) - SOP rewritten to align with Prompt Architect confidence discipline and Skill Forge structure-first curation.
