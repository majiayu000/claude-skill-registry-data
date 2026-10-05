---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "channel"
skill_id: "messenger-client-document-request"
title: "Messenger Client Document Request Channel Skill"
risk_area:
  - communication
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
# Messenger Client Document Request Channel Skill

## Purpose

Prepare short, controlled document requests for client-facing messaging channels.

## When to Use

Use only where the implementation profile permits client communication through a messenger or chat tool.

## Required Inputs

- approved channel;
- recipient identity;
- requested item list;
- case reference for internal logging;
- approved language and tone.

## Workflow

1. Confirm the channel is approved.
2. Use short administrative wording.
3. Request documents or clarifications without AML-sensitive reasoning.
4. Avoid attachments unless permitted.
5. Log the sent message or draft.
6. Update follow-up status.

## Agent Must Not

- discuss internal screening results with the external party;
- mention suspicious activity considerations;
- send sensitive case notes;
- use informal wording that changes the meaning of the request.
