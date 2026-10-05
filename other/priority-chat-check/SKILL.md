---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "operation"
skill_id: "priority-chat-check"
title: "Priority Chat Check"
risk_area:
  - general_aml
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
# Priority Chat Check

## Skill type

Operation skill.

## Purpose

Accept a limited AML check request from an approved communication channel and return only safe status information.

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

- `skills/channels/messenger-internal-review-alert`
- `skills/core/TCAML-S001-aml-screening`
- `skills/connectors/pdf-evidence-export`
- `skills/connectors/local-folder-evidence-storage`

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

- Requester not authorized
- Red flag found
- Full report required
- Client-facing wording requested

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
