---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "channel"
skill_id: "messenger-internal-review-alert"
title: "Messenger Internal Review Alert Channel Skill"
risk_area:
  - escalation
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
# Messenger Internal Review Alert Channel Skill

## Purpose

Notify an internal reviewer that a case requires attention, without sending the full case record into an uncontrolled channel.

## When to Use

Use for internal alerts in approved channels such as team chat, secure messenger or workflow notification tools.

## Required Inputs

- internal reviewer or group;
- case identifier;
- alert type;
- evidence location link or case system reference;
- urgency level.

## Workflow

1. Confirm internal channel approval.
2. Use minimal case information.
3. Include case link or folder reference.
4. State the required action.
5. Avoid detailed sensitive content unless the channel is approved for it.
6. Log that the alert was created.

## Agent Must Not

- disclose detailed sensitive findings in a general channel;
- include customer documents in plain chat unless approved;
- present the alert as final decision;
- notify external parties.
