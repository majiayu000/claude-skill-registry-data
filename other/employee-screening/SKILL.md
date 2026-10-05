---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "operation"
skill_id: "employee-screening"
title: "Employee Screening"
risk_area:
  - employee-screening
  - privacy
  - evidence
  - escalation
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
# Employee Screening

## Skill type

Operation skill.

## Purpose

Support policy-limited AML/integrity screening for candidates, staff or role-sensitive personnel while preserving privacy, proportionality and human review boundaries.

## Practical control layer

This operation uses `skills/core/TCAML-S010-verification-evidence-control` to apply common analyst-grade controls: declared-data inventory, source plan, source check records, evidence capture, discrepancy register, risk trigger mapping, audit trail and human handover.

## Scope

- Candidates, employees, contractors and role-sensitive staff.
- Policy-limited screening, conflict/integrity checks and HR/compliance routing.
- Privacy-sensitive evidence handling and minimal necessary output.

## Skills commonly used

- `skills/core/TCAML-S010-verification-evidence-control`
- `skills/core/TCAML-S001-aml-screening`
- `skills/core/TCAML-S002-adverse-media-review`
- `skills/core/TCAML-S003-company-ubo-review` where legal entities, UBOs or controllers are involved
- `skills/core/TCAML-S005-mlro-escalation-memo` where escalation is required
- `skills/core/TCAML-S008-cdd-edd-review`
- relevant source skills under `skills/sources/`
- evidence connector skills under `skills/connectors/`

## Agent may

- Extract and organize declared data.
- Select source checks from the implementation profile.
- Run permitted checks through approved source workflows.
- Capture positive and negative evidence.
- Record discrepancies, limitations and confidence.
- Prepare review-ready summaries, workpapers and escalation drafts.

## Agent must not

- Approve or reject the subject.
- Make a final legal, sanctions or regulatory conclusion.
- Hide missing data, uncertainty or weak identifiers.
- Discuss suspicious activity, sanctions concerns or internal AML reasoning with the checked subject.
- Bypass policy-defined manual review triggers.

## Workflow

See `WORKFLOW.md`.
