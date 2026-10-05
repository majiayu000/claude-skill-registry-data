---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "connector"
skill_id: "editable-report-builder"
title: "Editable Report Builder Connector Skill"
risk_area:
  - evidence
human_review_required: true
final_decision_allowed: false
paid_source_boundary: false
source_access_required: "not_applicable"
private_configuration_required_for:
  - client-specific Implementation Profiles
  - private source configuration
  - evidence rules
  - MLRO escalation logic
---
# Editable Report Builder Connector Skill

## Purpose

Prepare editable AML report drafts that a human reviewer can revise, approve, reject, escalate or archive according to the firm's procedure.

## When to Use

Use after source checks, evidence capture and checklist completion, but before final human review.

## Required Inputs

- case summary;
- completed checklist;
- evidence log;
- red flags and limitations;
- selected report template;
- output format requirement.

## Workflow

1. Load the relevant template.
2. Populate only evidence-supported fields.
3. Mark missing or unavailable information clearly.
4. Separate facts, allegations, observations and agent notes.
5. Leave human decision fields empty unless the implementation profile provides a human-entered value.
6. Save as editable draft and optionally export a PDF copy.

## Output

- editable draft report;
- optional PDF rendering;
- evidence cross-reference table;
- missing information section;
- human review section.

## Agent Must Not

- write final regulatory conclusions;
- fill human decision fields on behalf of the reviewer;
- remove uncertainty to make the report look cleaner;
- invent evidence where a source is missing.
