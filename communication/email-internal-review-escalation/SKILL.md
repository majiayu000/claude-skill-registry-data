---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "channel"
skill_id: "email-internal-review-escalation"
title: "Email Internal Review Escalation Channel Skill"
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
# Email Internal Review Escalation Channel Skill

## Purpose

Draft an internal email to send an AML case to manual review, MLRO review or authorized reviewer attention.

## When to Use

Use when a selected TCAML skill or implementation profile marks a case as requiring human review.

## Required Inputs

- reviewer role or mailbox;
- case identifier;
- escalation reason;
- evidence package reference;
- urgency level;
- pending actions.

## Workflow

1. Confirm this is an internal recipient.
2. Summarize the reason for escalation in factual language.
3. Link to the evidence pack or case folder.
4. List open questions and missing information.
5. Avoid final decision language.
6. Log the communication in the case record.

## Output

- internal email draft;
- subject line;
- evidence package reference;
- next-action checklist.

## Agent Must Not

- decide the outcome;
- state that a relationship should be accepted or refused;
- bypass reviewer routing rules;
- include unnecessary personal data.
