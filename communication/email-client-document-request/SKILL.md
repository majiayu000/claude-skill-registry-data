---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "channel"
skill_id: "email-client-document-request"
title: "Email Client Document Request Channel Skill"
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
# Email Client Document Request Channel Skill

## Purpose

Draft a controlled email requesting missing documents or clarifications from a client or counterparty.

## When to Use

Use when the AML workflow identifies missing information that can be requested externally without disclosing internal AML concerns.

## Required Inputs

- recipient name or role;
- requested document list;
- deadline or expected response time;
- approved tone/template;
- case identifier for internal logging only.

## Workflow

1. Confirm that the request is permitted for external communication.
2. Use neutral wording.
3. Request only necessary documents or clarifications.
4. Avoid explaining internal risk flags.
5. Do not mention suspicious activity, sanctions concern or regulatory reporting unless the implementation profile explicitly permits such wording.
6. Log the draft or sent message.

## Safe Message Content

- missing document list;
- document format requirements;
- deadline;
- contact channel;
- neutral administrative context.

## Agent Must Not

- disclose internal red flags;
- imply suspicion;
- discuss potential regulatory reporting;
- provide final onboarding outcome.
