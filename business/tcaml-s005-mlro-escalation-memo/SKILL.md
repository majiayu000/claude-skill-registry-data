---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "core"
skill_id: "TCAML-S005"
title: "MLRO Escalation Memo Skill"
risk_area:
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
# TCAML-S005: MLRO Escalation Memo Skill

Maintainer: Tom Custos  
Category: Human-supervised AML operations

---

## 1. Purpose

This skill defines how an AML agent should prepare a structured escalation memo for an MLRO, compliance officer, or authorized reviewer.

The purpose is to convert case findings into a concise, evidence-backed, human-reviewable package that explains:

- why the case is being escalated;
- what was reviewed;
- what was found;
- what remains uncertain;
- what evidence supports each finding;
- what human action is requested.

The agent may organize, summarize, cross-reference, draft, and highlight findings.

The agent must not make the final compliance decision, approve or refuse a customer, override policy, or present a recommendation as a binding determination.

---

## 2. When to use

Use TCAML-S005 when an AML workflow produces findings that require human review or formal escalation.

Typical use cases include:

- possible sanctions or PEP match requiring review;
- adverse media finding requiring assessment;
- unclear or contradictory company ownership information;
- missing UBO information;
- high-risk jurisdiction exposure;
- website/domain red flags;
- regulatory or licensing claim that cannot be verified;
- unusual source-of-funds or source-of-wealth issue;
- internal policy trigger;
- periodic review escalation;
- unresolved false positive assessment;
- case where multiple medium-risk indicators combine into a material concern.

TCAML-S005 should be used after one or more prior TCAML skills have produced structured outputs, but it may also be used with internal case notes or external analyst findings.

---

## 3. Agent may

The agent may:

- collect outputs from TCAML-S001, S002, S003, S004, and other case sources;
- summarize case context;
- identify and group escalation triggers;
- prioritize findings by relevance and severity;
- cross-reference evidence IDs and source references;
- list missing information and review limitations;
- identify conflicts between sources;
- draft a memo for MLRO review;
- propose non-binding human review options;
- prepare a decision section for the human reviewer to complete;
- produce a structured output for case management systems.

---

## 4. Agent must not

The agent must not:

- make the final MLRO decision;
- approve a customer, transaction, counterparty, merchant, or relationship;
- reject a customer, transaction, counterparty, merchant, or relationship;
- state that a match is conclusively true or false without human review;
- state that a person or entity is legally sanctioned unless supported by an authoritative source and reviewed by a human;
- state that adverse media proves wrongdoing unless supported by official records and reviewed by a human;
- conclude that a company structure is lawful or unlawful;
- conclude that a website, product, or service is legal, illegal, licensed, unlicensed, compliant, or non-compliant;
- hide missing information, conflicts, weak evidence, or uncertainty;
- invent case facts, reviewer decisions, dates, sources, policies, or evidence;
- replace MLRO, compliance officer, legal counsel, or authorized reviewer judgment.

---

## 5. Required input

The agent must collect or mark as missing:

### Case metadata

- case ID;
- subject name;
- subject type;
- customer/counterparty/internal reference number, if available;
- prepared by;
- prepared date/time;
- escalation owner or target reviewer, if known;
- jurisdiction or business unit, if known;
- review purpose;
- applicable internal policy trigger, if known.

### Subject identifiers

For individuals:

- full name;
- aliases or alternate spellings;
- date of birth, if available;
- nationality/citizenship, if available;
- residence or address, if available;
- identification number, if available and policy-permitted.

For companies/entities:

- legal name;
- trading name or brand;
- registration number;
- jurisdiction of incorporation;
- registered address;
- operating address;
- directors, shareholders, controllers, and UBO candidates, where available;
- website/domain, where relevant.

### Source materials

- screening output;
- adverse media output;
- company and UBO review output;
- website and domain review output;
- evidence log;
- source checklist;
- false positive assessment, if available;
- internal notes or analyst comments;
- relevant policy references;
- customer-provided documents, if within scope.

### Escalation reason

At least one escalation reason must be stated.

Examples:

- possible sanctions match;
- possible PEP exposure;
- adverse media finding;
- unresolved identity ambiguity;
- missing or opaque ownership information;
- nominee/trust/foundation/control complexity;
- website/domain contradiction;
- regulator/licence claim not verified;
- internal policy threshold reached;
- high-risk jurisdiction exposure;
- material information conflict.

If the escalation reason is not clear, the agent must state that clarification is required.

---

## 6. Recommended source categories

The agent should use approved sources and prior outputs appropriate to the implementation:

- TCAML-S001 screening result;
- TCAML-S002 adverse media review result;
- TCAML-S003 company and UBO review result;
- TCAML-S004 website and domain review result;
- official sanctions/PEP/regulatory sources;
- official government, court, registry, or regulator records;
- trusted commercial AML/KYB data provider reports;
- internal onboarding or monitoring file;
- customer-provided documents;
- internal policy documents;
- prior analyst notes;
- screenshots or locally stored evidence captures.

The agent must separate official records, commercial data, website claims, media allegations, internal notes, and user-provided statements.

---

## 7. Evidence quality

Use TCAML evidence quality labels:

| Grade | Evidence type |
|---|---|
| A | Official government, regulator, court, registry, sanctions authority, official legal filing |
| B | Official company, bank, institutional, website, app store, or customer-controlled source |
| C | Trusted commercial AML/KYB/screening/domain intelligence provider |
| D | Reputable media, public research, NGO source, public technical lookup, archive snapshot |
| E | User-provided statement, unsupported internal note, unverified screenshot, informal claim |

The escalation memo should prioritize higher-quality evidence, but lower-quality evidence may still be recorded if it explains why further review is required.

---

## 8. Workflow

### Step 1: Confirm escalation scope

Identify the case, subject, review purpose, escalation reason, and intended human reviewer.

State whether the memo is based on:

- screening only;
- adverse media only;
- company/UBO review;
- website/domain review;
- multiple TCAML skill outputs;
- internal analyst notes;
- mixed sources.

### Step 2: Collect prior findings

Gather all relevant findings from source materials.

For each finding, preserve:

- finding ID;
- originating skill or source;
- evidence reference;
- evidence quality;
- relevance;
- confidence;
- limitation or missing data, if any.

### Step 3: Group findings by issue type

Group findings into clear sections, such as:

- sanctions/PEP screening;
- adverse media;
- company ownership and control;
- website/domain and digital footprint;
- jurisdiction exposure;
- source-of-funds/source-of-wealth issue;
- internal policy trigger;
- missing information;
- conflicting information.

### Step 4: Distinguish facts, claims, allegations, and analyst observations

The memo must label the nature of each material statement.

Use these labels:

- official record;
- source-supported fact;
- subject-provided claim;
- website/self-published claim;
- media allegation;
- analyst observation;
- unresolved conflict;
- missing information.

### Step 5: Prioritize material findings

Prioritize findings based on:

- source quality;
- relevance to subject;
- recency;
- severity;
- number of corroborating sources;
- identifier strength;
- unresolved uncertainty;
- internal policy trigger.

The agent should not inflate severity to make the memo more persuasive. The memo should be balanced and evidence-led.

### Step 6: Explain uncertainty

For each material uncertainty, record:

- what is unknown;
- why it matters;
- what source was checked;
- what additional information would reduce uncertainty;
- whether the uncertainty affects confidence.

### Step 7: Draft executive summary

The executive summary should be short, neutral, and decision-supportive.

It should include:

- subject and case context;
- reason for escalation;
- most material findings;
- key missing information;
- requested human action.

It must not include final acceptance/refusal language.

### Step 8: Draft non-binding human review options

The agent may suggest review options such as:

- request additional identifiers;
- request additional documents;
- perform enhanced due diligence;
- review possible match manually;
- obtain legal/compliance opinion;
- pause workflow pending human review;
- document false positive rationale if confirmed by reviewer;
- escalate to second-level compliance review;
- close escalation if the reviewer determines no further action is required.

These options must be clearly labelled as non-binding and for human review.

### Step 9: Prepare human decision section

The memo must include a section reserved for the MLRO or authorized reviewer.

The agent must leave the final decision fields blank unless the human reviewer has already provided an explicit decision and the implementation is allowed to record it.

### Step 10: Record audit metadata

Record:

- date/time prepared;
- agent/system version, if available;
- data sources used;
- reviewed skill outputs;
- evidence IDs;
- known limitations;
- reviewer status.

---

## 9. Escalation trigger categories

### Mandatory human review triggers

A case should be escalated when any of the following are present:

- possible sanctions match;
- possible PEP match where internal policy requires review;
- close name match with insufficient identifiers;
- adverse media that may be directly relevant to AML risk;
- official enforcement, regulatory, criminal, court, or insolvency record relevant to the subject;
- missing or unclear UBO information;
- ownership/control conflict across sources;
- high-risk jurisdiction exposure under internal policy;
- website/domain contradiction relevant to activity, operator, licence, or payments;
- internal policy rule requiring MLRO or second-line review.

### Optional human review triggers

A case may be escalated when there are:

- multiple weak indicators that become material together;
- unclear adverse media relevance;
- domain or website age inconsistent with business claims;
- unsupported licence or regulatory claims;
- complex group structure;
- nominee, trust, foundation, or bearer share indicators;
- missing customer responses;
- reviewer uncertainty.

---

## 10. Confidence

The escalation memo must include an overall confidence label:

- Low;
- Medium;
- High.

Confidence refers to the completeness and reliability of the memo, not to the final case decision.

### Low confidence examples

- material identifiers are missing;
- only name-only screening is available;
- ownership chain is incomplete;
- key source pages are inaccessible;
- adverse media relevance is unclear;
- evidence comes mainly from user-provided or unverified sources;
- contradictions are unresolved.

### Medium confidence examples

- key identifiers are available but some supporting evidence is missing;
- multiple source types were reviewed;
- some findings remain unresolved;
- evidence quality is mixed;
- analyst review is required for final interpretation.

### High confidence examples

- key identifiers are complete;
- material findings are supported by official or trusted sources;
- evidence references are clear;
- limitations are minor;
- findings are ready for human decision-making.

High confidence does not mean the customer, counterparty, or activity is acceptable. It only means the memo is well-supported.

---

## 11. Output requirements

The agent must produce a structured memo with these sections:

1. Case details;
2. Escalation reason;
3. Executive summary;
4. Source materials reviewed;
5. Key findings;
6. Evidence table;
7. Missing information and limitations;
8. Risk observations;
9. Conflicting information;
10. Non-binding human review options;
11. Decision section for human reviewer;
12. Audit metadata.

Each key finding must include:

- finding ID;
- category;
- finding statement;
- evidence reference;
- evidence quality;
- relevance;
- confidence;
- human review need.

---

## 12. Human review

The memo must be reviewed by an MLRO, compliance officer, or authorized reviewer before any final case action is taken.

The reviewer should complete:

- final decision;
- rationale;
- required follow-up;
- reviewer name/role;
- decision date;
- policy reference, if applicable.

The agent may store or format the reviewer decision only after it has been provided by the human reviewer.

---

## 13. Limitations

TCAML-S005 does not define:

- legal advice;
- regulatory interpretation;
- customer acceptance criteria;
- risk appetite;
- final risk scoring policy;
- SAR/STR filing decision;
- account closure decision;
- law enforcement notification decision;
- data retention requirements;
- jurisdiction-specific compliance rules.

Those remain the responsibility of the regulated business, MLRO, compliance officer, legal counsel, or authorized reviewer.
