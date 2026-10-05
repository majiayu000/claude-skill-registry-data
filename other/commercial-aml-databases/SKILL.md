---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "source"
skill_id: "commercial-aml-databases"
title: "Source Skill: Commercial AML Databases"
risk_area:
  - general_aml
human_review_required: true
final_decision_allowed: false
paid_source_boundary: true
source_access_required: "client_valid_access"
private_configuration_required_for:
  - client-specific Implementation Profiles
  - private source configuration
  - evidence rules
  - MLRO escalation logic
---
# Source Skill: Commercial AML Databases


This source skill describes how an AML agent should work with the **Commercial AML databases** source category inside a client-approved implementation profile.

It is a source workflow, not a bundled data subscription. It does not include credentials, paid database access, provider-specific bypass instructions or proprietary source content.

## Purpose

Guide use of licensed commercial AML databases and specialist screening sources where the client has valid access.

## Category options

- LSEG World-Check
- Dow Jones Risk & Compliance
- LexisNexis / WorldCompliance
- Moody’s GRID
- ComplyAdvantage
- AML Watcher
- OpenSanctions
- Other

## Used for

- sanctions screening
- PEP / RCA / SOE screening
- adverse media review
- EDD review
- periodic review
- client onboarding
- counterparty screening

## Required inputs

Collect the fields required by the operation workflow and the implementation profile. Depending on the subject, this may include:

- case ID;
- subject type;
- full legal name or entity name;
- aliases or trading names;
- date of birth or incorporation date where available;
- nationality, residence, incorporation jurisdiction or operating jurisdiction;
- registration number, licence number, LEI, SWIFT/BIC, domain, IP address, goods code, wallet address or other source-specific identifier;
- source list and evidence requirements defined by the implementation profile.

## Workflow

1. Load the applicable operation workflow and implementation profile.
2. Confirm the selected source is approved for this client, case type and jurisdiction.
3. Confirm the client has valid access where the source is commercial, licensed or subscription-based.
4. Run the source check using the permitted browser, API, registry, database, search or evidence workflow.
5. Capture both positive/potential-result and negative/no-material-result evidence where policy requires it.
6. Record query terms, filters, source URL/reference, access date/time, result summary and limitations.
7. Compare identifiers without relying on name similarity alone.
8. Label evidence quality: official source, licensed source, public search, client-provided, unverified public source or missing/inaccessible.
9. Route red flags, ambiguity, source conflicts or unavailable required sources to MLRO / compliance review.

## Evidence requirements

Record:

- source category;
- exact source used;
- access method if relevant;
- query terms and filters;
- source URL, record ID or source reference;
- screening date/time;
- result status: no material result, possible match, confirmed source hit, unclear, missing/inaccessible;
- identifiers compared;
- screenshot/PDF/export evidence reference;
- limitations and confidence notes;
- escalation reason if any.

## Important notes

- Third-party databases and paid source subscriptions are not included by default.
- OpenSanctions must not be presented as a bundled free/open business source unless the specific deployment scope and licensing basis support that statement.
- Use only client-approved sources where access and workflow are permitted by provider terms and internal policy.

## Red flag triggers

Route to MLRO / compliance review when any of the following appear:

- database hit requiring human interpretation
- sanctions, PEP, SOE, serious adverse media or enforcement signal
- conflicting database records
- missing identifiers where a material result remains unresolved
- provider access, licensing or terms limitation

## Agent must not

- treat any source result as a final compliance decision;
- approve or reject a customer, counterparty, supplier, employee or transaction;
- hide uncertainty or omit missing source limitations;
- imply that a paid source is included when it is only a configurable client-approved source;
- bypass logins, licensing, MFA, access controls or source terms;
- disclose internal AML concerns to the checked subject.
