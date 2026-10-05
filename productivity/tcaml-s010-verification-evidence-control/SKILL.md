---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "core"
skill_id: "TCAML-S010"
title: "Verification & Evidence Control"
risk_area:
  - cdd
  - kyb
  - evidence
  - escalation
human_review_required: true
final_decision_allowed: false
paid_source_boundary: false
source_access_required: "not_applicable"
private_configuration_required_for:
  - client-specific Implementation Profiles
  - approved source matrix
  - evidence retention rules
  - risk appetite thresholds
  - MLRO escalation logic
---
# TCAML-S010 — Verification & Evidence Control

## Purpose

Define the practical verification, evidence, discrepancy and audit controls used by TCAML operation workflows.

This skill turns an AML operation from a generic screening task into an analyst-grade review: the agent must identify the subject, understand the relationship context, verify declared facts against approved sources, capture evidence, record limitations, handle discrepancies, prepare a review-ready case file and route red flags for human review.

## How this skill is used

This is a reusable core control layer. Operation skills call this skill whenever they perform client, company, counterparty, supplier, employee, periodic review or escalation support work.

It does not replace source skills. It tells the agent how to run and document the review. Source skills define where to check. Connector skills define how evidence is captured, stored, exported or reported.

## Practical control pillars

1. **Case setup** — assign case ID, subject type, relationship type, review purpose and applicable policy context.
2. **Subject classification** — classify the checked subject as individual, legal entity, UBO, director, employee, supplier, bank/FI, website, wallet, transaction or connected party.
3. **Declared-data inventory** — list the facts provided by the client, employee, counterparty, documents or prior case file.
4. **Verification plan** — select approved source workflows based on subject type, risk, jurisdiction, products, channels and implementation profile.
5. **Independent source verification** — compare declared facts against approved public, official, commercial or internal sources.
6. **Screening controls** — run sanctions, PEP/RCA/SOE, adverse media and watchlist checks where required.
7. **Registry and ownership controls** — check company status, officers, ownership, control chain, UBOs and connected parties where applicable.
8. **Evidence capture** — capture positive results, negative results, material search parameters, source limitations and timestamps.
9. **Discrepancy handling** — log mismatches, missing data, ambiguity and unresolved questions with status and next action.
10. **Risk factor mapping** — map findings to risk factors, manual review triggers, EDD triggers and escalation rules.
11. **Case file assembly** — prepare source check records, evidence index, discrepancy register, review summary and audit trail.
12. **Human handover** — leave final decision fields blank and route cases to the compliance team / MLRO where required.

## Stagegate control

This skill is stagegate-controlled. When used for a live operation workflow, EDD review, MLRO escalation support, case release or audit-ready handover, the agent must load `STAGEGATES.md` and stop at each gate until the exact keyword is received from the analyst.

Draft mode may be used only for planning, training or non-final draft preparation. Draft outputs must mark non-confirmed gates as `draft_only` and must not be presented as confirmed case files.

## Human-supervised boundary

The agent may collect, compare, summarize, document, draft and route. The agent must not approve or reject a subject, make final legal/regulatory/sanctions conclusions, suppress uncertainty, invent missing facts or bypass manual review triggers.
