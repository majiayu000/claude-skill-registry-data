---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "core"
skill_id: "TCAML-S007"
title: "Periodic Review & Re-Screening"
risk_area:
  - sanctions
  - escalation
human_review_required: true
final_decision_allowed: false
paid_source_boundary: true
source_access_required: "not_applicable"
private_configuration_required_for:
  - client-specific Implementation Profiles
  - private source configuration
  - evidence rules
  - MLRO escalation logic
---
# TCAML-S007: Periodic Review & Re-Screening


## Purpose

TCAML-S007 defines how an AML agent should assist with periodic review, re-screening and change detection for existing relationships.

The skill helps the agent compare current findings with prior evidence and route material changes to human review.

## When to Use

Use this skill for:

- scheduled customer review;
- employee re-screening;
- counterparty re-screening;
- risk-based monitoring;
- off-cycle review triggered by new information;
- refresh of outdated evidence;
- comparison against previous case records.

## Agent May

- identify due reviews;
- re-run approved source checks;
- compare old and new evidence;
- flag material changes;
- prepare a periodic review report;
- update the client master checklist;
- route changes to human review.

## Agent Must Not

- renew a relationship without human approval;
- downgrade risk without authorized review;
- ignore new red flags;
- hide differences from prior records;
- overwrite prior evidence without preserving audit trail.

## Required Inputs

- subject name;
- subject type;
- current risk category;
- previous review date;
- next review due date or schedule;
- previous evidence pack reference;
- implementation profile;
- approved source list.

## Workflow

1. Confirm review trigger: scheduled, risk-based or event-driven.
2. Load prior case summary and evidence references.
3. Re-check required sources.
4. Compare current data against prior data.
5. Identify changes in name, ownership, directors, address, website, goods, jurisdiction exposure or adverse media.
6. Mark unresolved discrepancies.
7. Capture updated evidence.
8. Prepare periodic review summary.
9. Route material changes or red flags to human review.
10. Preserve audit trail.

## Review Frequency

Review frequency should be defined by the implementation profile and may vary by:

- risk category;
- customer type;
- jurisdiction;
- product or service;
- sector;
- regulatory requirement;
- internal AML policy.

## Change Indicators

- new sanctions/PEP/adverse media result;
- ownership or control change;
- director or authorized person change;
- new high-risk jurisdiction exposure;
- website or domain change;
- new trade activity;
- new counterparty or bank exposure;
- inconsistency with prior file;
- expired documents;
- missing evidence from previous review.

## Output

The output should include:

- review trigger;
- review scope;
- prior case reference;
- source re-check table;
- changes since last review;
- red flags;
- missing information;
- evidence references;
- confidence;
- human review routing.
