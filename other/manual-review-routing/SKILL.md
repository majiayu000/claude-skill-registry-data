---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "operation"
skill_id: "manual-review-routing"
title: "Manual Review Routing"
risk_area:
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
# Manual Review Routing

## Skill type

Operation skill.

## Purpose

Route hits, possible matches, missing critical data and policy-defined red flags to a human reviewer.

## What this skill does

This skill coordinates multiple core, source, connector and channel skills to complete one end-to-end AML operation.

It does not replace a compliance officer, MLRO or authorized reviewer. It prepares documented findings and routes cases for human review when required.

## Required inputs

- Subject type and identifiers.
- Operation context.
- Applicable implementation profile.
- Required sources and source access rules.
- Evidence storage location.
- Manual review and escalation rules.

## Skills commonly used

- `skills/core/TCAML-S005-mlro-escalation-memo`
- `skills/channels/email-internal-review-escalation`
- `skills/channels/messenger-internal-review-alert`
- `templates/manual-review-queue.md`

## Agent may

- Extract relevant data from provided forms or documents.
- Run applicable source skills.
- Capture screenshots and PDF evidence.
- Update a client checklist or case record.
- Prepare a human-reviewable summary.
- Route red flags to manual review.

## Agent must not

- Approve or reject a client, employee or counterparty.
- Make a final legal, sanctions or regulatory conclusion.
- Hide missing data or uncertainty.
- Discuss suspicious activity, sanctions concerns or internal AML reasoning with a checked subject.
- Bypass policy-defined manual review triggers.

## Manual review triggers

- Hit or potential red flag
- Low confidence due to missing data
- Contradictory evidence
- Policy-defined escalation threshold reached

## Output

- Completed source check records.
- Evidence references and file paths.
- Checklist status.
- Missing information list.
- Manual review status.
- Draft summary for human review.

## Workflow

See `WORKFLOW.md`.

## Verification evidence control

When this operation handles case findings or review routing, use `skills/core/TCAML-S010-verification-evidence-control` to preserve source check records, evidence references, discrepancies, limitations and human decision boundaries.
