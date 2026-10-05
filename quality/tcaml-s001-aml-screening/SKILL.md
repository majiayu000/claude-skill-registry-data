---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "core"
skill_id: "TCAML-S001"
title: "AML Screening Skill"
risk_area:
  - sanctions
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
# TCAML-S001: AML Screening Skill

Maintainer: Tom Custos  
Category: Human-supervised AML operations

---

## 1. Purpose

This skill defines how an AML agent should assist with screening a subject against sanctions, PEP, watchlist, adverse risk, and internal risk sources.

The skill is designed for human-supervised workflows.

The agent may collect, compare, structure, and summarize information.

The agent must not approve, reject, clear, block, or legally classify a subject.

---

## 2. When to use

Use TCAML-S001 when reviewing any of the following:

- individual customer;
- company customer;
- director;
- ultimate beneficial owner;
- authorized representative;
- counterparty;
- supplier;
- merchant;
- payment beneficiary;
- wallet owner;
- related entity;
- name returned by another AML workflow.

---

## 3. Agent may

The agent may:

- collect available identifiers;
- request missing identifiers;
- run or request screening checks;
- compare possible matches;
- identify similarities and differences;
- summarize source results;
- document uncertainty;
- prepare an evidence log;
- prepare a false positive assessment;
- recommend human review or escalation.

---

## 4. Agent must not

The agent must not:

- approve a customer;
- reject a customer;
- clear a sanctions hit as final;
- determine that a person or entity is legally sanctioned;
- determine regulatory reporting obligations;
- provide legal advice;
- ignore missing identifiers;
- invent missing facts;
- hide conflicts between sources;
- remove findings because they are inconvenient;
- override internal policy;
- replace the MLRO or compliance officer.

---

## 5. Required input

The agent must collect or mark as missing:

### For individuals

- full name;
- aliases or alternative spellings, if available;
- date of birth, if available;
- nationality, if available;
- country of residence, if available;
- document country, if available;
- customer or case ID, if available.

### For entities

- legal name;
- trading name, if available;
- registration number, if available;
- jurisdiction of incorporation, if available;
- registered address, if available;
- directors, if available;
- UBOs, if available;
- website or domain, if available;
- customer or case ID, if available.

If required input is missing, the agent must continue only if permitted by the workflow and must state that confidence is limited.

---

## 6. Recommended sources

The agent should use source categories appropriate to the implementation:

- sanctions lists;
- PEP datasets;
- regulator notices;
- law enforcement notices;
- government company registries;
- court or insolvency records;
- internal watchlists;
- licensed commercial data providers;
- public adverse media sources;
- prior internal case history.

The agent must identify which sources were checked.

The agent must not imply that unchecked sources were checked.

---

## 7. Workflow

### Step 1: Normalize subject data

The agent should organize identifiers into a consistent structure.

For names, the agent should preserve the original spelling and record known variants.

For dates and jurisdictions, the agent should preserve source-provided format and add normalized format where possible.

### Step 2: Identify missing data

The agent must list missing identifiers that materially affect screening quality.

Examples:

- missing date of birth;
- missing nationality;
- missing registration number;
- missing jurisdiction;
- unknown UBOs;
- unknown source freshness.

### Step 3: Run or request screening

The agent may use one or more screening systems.

The agent should record:

- source name;
- source type;
- date/time checked;
- query used;
- result summary;
- evidence quality grade.

### Step 4: Compare possible matches

For each possible match, compare available identifiers:

- name similarity;
- aliases;
- date of birth;
- nationality;
- residence;
- document country;
- registration number;
- jurisdiction;
- address;
- role or relationship;
- source program or category.

### Step 5: Classify match assessment for human review

The agent may use the following operational assessment labels:

- `No relevant result found`
- `Possible false positive`
- `Possible match - requires review`
- `Strong possible match - escalate`
- `Insufficient data - requires additional information`

These labels are not final legal determinations.

### Step 6: Assign confidence

The agent must assign confidence:

- Low;
- Medium;
- High.

The agent must explain the reason.

Confidence should be reduced when key identifiers are missing, sources conflict, or only name-only screening is available.

### Step 7: Prepare output

The agent must produce a structured output containing:

- subject summary;
- sources checked;
- possible matches;
- match assessment;
- confidence;
- missing information;
- evidence log;
- recommended next human action.

---

## 8. Evidence quality

Use the following evidence quality labels:

| Grade | Evidence type |
|---|---|
| A | Official government, regulator, court, registry, sanctions authority |
| B | Official company or institution source |
| C | Trusted commercial or licensed data provider |
| D | Reputable media, public records, NGO or research source |
| E | User-provided or unverified source |

Where evidence quality is unclear, mark it as `Unknown` and explain why.

---

## 9. Confidence guidance

### High confidence

Use only when:

- key identifiers are available;
- multiple relevant sources were checked;
- the result is supported by strong identifier comparison;
- no material conflicts remain unresolved.

### Medium confidence

Use when:

- some identifiers are available;
- at least one reliable source was checked;
- the assessment is plausible but not complete;
- some uncertainty remains.

### Low confidence

Use when:

- screening is based mainly on name only;
- date of birth or jurisdiction is missing;
- source freshness is unclear;
- only one weak source was checked;
- source results conflict;
- identity cannot be reliably compared.

---

## 10. Escalation triggers

The agent must recommend escalation when any of the following occur:

- possible sanctions match with insufficient disambiguation;
- strong name and identifier overlap with a sanctioned or listed subject;
- PEP match requiring policy review;
- adverse source from regulator, court, law enforcement, or official notice;
- conflicting source data that cannot be resolved;
- subject refuses or fails to provide key identifiers;
- UBO or ownership data is unavailable for an entity where required;
- internal policy threshold is met;
- the agent cannot determine whether a match is likely false positive.

---

## 11. Output requirement

The output must be suitable for human review.

It should not be written as a final approval or rejection.

It should make clear:

- what was checked;
- what was found;
- what remains unknown;
- what evidence supports each finding;
- what human action is recommended.

---

## 12. Completion criteria

A TCAML-S001 review is complete only when:

- subject identifiers are recorded;
- missing identifiers are documented;
- sources checked are listed;
- possible matches are compared;
- confidence is assigned and explained;
- evidence is logged;
- next human action is stated.

If these conditions are not met, the output should be marked incomplete.
