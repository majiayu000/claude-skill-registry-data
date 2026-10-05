---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "core"
skill_id: "TCAML-S008"
title: "CDD / EDD Review"
risk_area:
  - cdd
  - edd
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
# TCAML-S008 — CDD / EDD Review


## Purpose

Define standard due diligence and enhanced due diligence review logic for human-supervised AML/KYC/KYB operations.

## How this skill is used

This is a source-agnostic core skill. It defines the review logic and human-supervised guardrails. Actual checks are performed through selected operation workflows, source workflows, connectors, channels and the implementation profile.

## Human-supervised boundary

The agent may collect facts, compare identifiers, structure evidence, summarize uncertainty and route cases to review. The agent must not approve/reject clients, make final legal conclusions, file regulator reports independently or replace the MLRO / compliance team.
