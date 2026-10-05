---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "operation"
skill_id: "draft-regulator-response"
title: "Operation Skill: Draft Regulator Response"
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
# Operation Skill: Draft Regulator Response

Prepare reviewable draft wording for a regulator, FIU, bank, compliance partner or internal committee using case evidence and policy language.

The agent must never send this communication automatically. It is a draft-only operation for MLRO / authorized human review.

## Verification evidence control

When this operation handles case findings or review routing, use `skills/core/TCAML-S010-verification-evidence-control` to preserve source check records, evidence references, discrepancies, limitations and human decision boundaries.
