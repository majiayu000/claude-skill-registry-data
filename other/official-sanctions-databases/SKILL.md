---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "source"
skill_id: "official-sanctions-databases"
title: "Source Skill: Official Sanctions Databases"
risk_area:
  - sanctions
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
# Source Skill: Official Sanctions Databases


This source skill describes how an AML agent should work with the **Official sanctions databases** source category inside a client-approved implementation profile.

It is a source workflow, not a bundled data subscription. It does not include credentials, paid database access, provider-specific bypass instructions or proprietary source content.

## Purpose

Guide checks against official sanctions databases and lists selected in the implementation profile.

## Category options

- OFAC sanctions lists
- UN Security Council sanctions list
- EU consolidated sanctions list
- UK sanctions list
- Local official sanctions lists
- Other

## Used for

- CDD / EDD workflows
- sanctions screening
- counterparty screening
- bank counterparty screening
- supplier review
- periodic review

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

- Treat official lists as authoritative source records, but do not let the agent make a final legal or onboarding decision.
- Document no-result checks as well as potential matches.
- Use local official sanctions lists when the relevant jurisdiction requires them.

## Red flag triggers

Route to MLRO / compliance review when any of the following appear:

- possible or confirmed sanctions match
- partial identifier match with material uncertainty
- listed vessel, aircraft, bank, entity or address exposure
- source unavailable where policy requires evidence capture

## Agent must not

- treat any source result as a final compliance decision;
- approve or reject a customer, counterparty, supplier, employee or transaction;
- hide uncertainty or omit missing source limitations;
- imply that a paid source is included when it is only a configurable client-approved source;
- bypass logins, licensing, MFA, access controls or source terms;
- disclose internal AML concerns to the checked subject.
