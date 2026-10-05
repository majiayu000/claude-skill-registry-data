---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "core"
skill_id: "TCAML-S003"
title: "Company & UBO Review Skill"
risk_area:
  - kyb
  - ubo
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
# TCAML-S003: Company & UBO Review Skill

Maintainer: Tom Custos  
Category: Human-supervised AML operations

---

## 1. Purpose

This skill defines how an AML agent should assist with structured review of legal entities, directors, ownership chains, control persons, and ultimate beneficial owners.

The goal is to help compliance teams understand who owns or controls a company, what evidence supports that understanding, which related parties require screening, and what information remains missing or uncertain.

The agent may collect, organize, compare, summarize, map, and prepare evidence for human review.

The agent must not make final legal conclusions about ownership, control, customer acceptance, customer refusal, or regulatory status.

---

## 2. When to use

Use TCAML-S003 when an AML workflow requires review of a legal entity, including:

- corporate customer onboarding;
- KYB review;
- enhanced due diligence;
- merchant onboarding;
- supplier or vendor review;
- crypto business counterparty review;
- payment institution counterparty review;
- periodic corporate KYC refresh;
- transaction monitoring case support;
- MLRO escalation preparation.

TCAML-S003 may be used after TCAML-S001 AML Screening and TCAML-S002 Adverse Media Review, or as the entry point for corporate cases.

---

## 3. Agent may

The agent may:

- collect company identifiers and registration evidence;
- request or review company registry extracts;
- organize directors, officers, shareholders, controllers, and UBOs;
- map ownership chains and intermediate entities;
- identify missing ownership or control information;
- compare user-provided documents against registry or official sources;
- screen the company, directors, shareholders, controllers, and UBOs using TCAML-S001;
- request adverse media review using TCAML-S002 where relevant;
- identify risk indicators for human review;
- classify evidence quality;
- explain confidence and limitations;
- prepare a company and UBO review output for human review.

---

## 4. Agent must not

The agent must not:

- approve or reject a company;
- determine legal ownership as a final conclusion;
- determine beneficial ownership as a final conclusion;
- treat user-provided ownership charts as verified unless supported by evidence;
- invent missing shareholders, directors, or UBOs;
- ignore missing ownership layers;
- ignore nominee, trustee, bearer share, or complex control indicators where relevant;
- ignore contradictions between documents and registries;
- screen only the company when related persons require review;
- make legal or regulatory conclusions;
- replace MLRO, compliance officer, or legal counsel judgment.

---

## 5. Required input

The agent must collect or mark as missing:

### Company identifiers

- legal name;
- trading name or brand name, if available;
- registration number;
- incorporation jurisdiction;
- incorporation date, if available;
- legal form;
- registered address;
- operating address, if different;
- website or domain;
- business activity;
- industry or merchant category;
- case ID, if available.

### Ownership and control information

- shareholders or members;
- ownership percentages, if available;
- intermediate holding companies;
- ultimate beneficial owners;
- directors;
- officers or authorized signatories;
- controllers or persons with significant control;
- trusts, foundations, nominees, or other arrangements, if relevant;
- source of ownership information.

### Review context

- review purpose;
- applicable internal UBO threshold, if defined;
- relevant jurisdictions;
- expected countries of operation;
- expected source of funds or source of wealth, if required by policy;
- documents provided by the customer;
- sources available to the agent.

If required identifiers or ownership details are missing, the agent must state how this affects confidence and whether additional information is required.

---

## 6. Recommended source categories

The agent should use approved sources appropriate to the implementation:

- company registry extract;
- beneficial ownership registry, where available;
- regulator register;
- licensed corporate data provider;
- official company documents;
- certificate of incorporation;
- articles or memorandum of association;
- shareholder register;
- ownership chart;
- board resolution or authorized signatory document;
- audited financial statements, where relevant;
- stock exchange filing, where relevant;
- trust deed or foundation document, where permitted by policy;
- internal customer file;
- screening engine results;
- adverse media sources.

The agent must distinguish official registry evidence from user-provided documents and unverified statements.

---

## 7. Evidence quality for company review

Use TCAML evidence quality labels:

| Grade | Company review evidence type |
|---|---|
| A | Official government registry, regulator register, court record, official beneficial ownership register |
| B | Official company document, audited filing, stock exchange filing, bank/reference institution document |
| C | Trusted commercial corporate data provider or licensed screening provider |
| D | Reputable media, NGO/research source, public website content |
| E | User-provided document, self-declaration, informal ownership chart, unverified source |

The agent should not treat Grade E evidence as independently verified.

---

## 8. Workflow

### Step 1: Define entity and review scope

Identify the legal entity, review purpose, jurisdictions, business activity, and internal policy requirements.

The agent should state whether the review is:

- standard KYB onboarding;
- enhanced due diligence;
- merchant onboarding;
- supplier or counterparty review;
- periodic refresh;
- escalation support.

### Step 2: Collect and normalize identifiers

Collect legal name, registration number, jurisdiction, address, website, and trading names.

Normalize names carefully but preserve the original spelling from official documents.

### Step 3: Verify company existence and status

Where sources are available, record:

- registry status;
- active/inactive/dissolved status;
- incorporation date;
- registered office;
- legal form;
- regulator or licence status, if applicable;
- evidence reference.

If registry verification is not available, state the limitation.

### Step 4: Build ownership and control map

Record all known ownership and control layers:

- direct shareholders;
- indirect shareholders;
- intermediate holding companies;
- UBOs;
- directors;
- officers;
- authorized signatories;
- controllers or persons with significant control.

For each party, record source, ownership percentage, role, jurisdiction, and evidence quality.

### Step 5: Identify UBO candidates

Identify potential UBOs based on available information and the applicable internal threshold.

The agent should use cautious wording:

- `UBO candidate identified based on available evidence`;
- `Potential control person identified`;
- `Ownership path appears to lead to the following individual, subject to human review`.

The agent must not write final legal determinations such as `confirmed UBO` unless the workflow explicitly permits that label after human review.

### Step 6: Screen related parties

For each relevant party, perform or request screening under TCAML-S001:

- company;
- trading names;
- directors;
- UBO candidates;
- major shareholders;
- intermediate holding entities;
- controllers;
- authorized signatories where required by policy.

If screening is not performed for a related party, record why.

### Step 7: Review adverse media where relevant

Use or request TCAML-S002 for the company and material related parties where required by policy.

Adverse media review is especially relevant for:

- high-risk industries;
- complex ownership chains;
- offshore structures;
- inconsistent information;
- regulatory exposure;
- prior screening hits;
- politically exposed persons;
- material ownership or control uncertainty.

### Step 8: Identify risk indicators

Record risk indicators without turning them into final decisions.

Possible indicators include:

- missing or unverifiable UBO information;
- nominee shareholders or nominee directors;
- complex ownership without clear business rationale;
- multiple offshore layers;
- bearer shares or unclear shareholding rights;
- recently incorporated company with high-risk activity;
- mismatch between business activity and website/payment flows;
- inconsistent names, addresses, or registration numbers;
- dissolved, struck-off, inactive, or suspended company status;
- high-risk jurisdiction exposure;
- sanctions, PEP, or adverse media hits on related parties;
- refusal or inability to provide ownership documents;
- circular ownership or opaque trust/foundation structures;
- unusual authorized signatory or control arrangement.

### Step 9: Explain confidence and limitations

Assign confidence to the company and UBO assessment:

- `High`: official sources support company status and ownership, key parties are identified, related-party screening is complete, and no material contradictions remain.
- `Medium`: core company information is supported, but some ownership/control information is user-provided, stale, incomplete, or not independently verified.
- `Low`: company status, ownership, UBOs, or control persons cannot be verified, or material contradictions exist.

Confidence must include reasons.

### Step 10: Prepare human-reviewable output

The output should include:

- company profile;
- evidence sources checked;
- ownership and control map;
- UBO candidates;
- related-party screening summary;
- adverse media summary where applicable;
- risk indicators;
- missing information;
- confidence and limitations;
- recommended human action.

Human review is required before final acceptance, refusal, escalation, or regulatory conclusion.

---

## 9. Escalation triggers

The agent should recommend escalation or additional review when:

- UBO cannot be identified;
- ownership chain is incomplete;
- official registry data conflicts with customer-provided documents;
- a director, shareholder, controller, or UBO candidate has a sanctions/PEP/adverse media hit;
- company status is dissolved, struck off, suspended, inactive, or materially unclear;
- business activity appears inconsistent with declared activity;
- high-risk jurisdiction exposure is identified;
- nominee, trust, foundation, or bearer share structures are present and not adequately explained;
- ownership structure appears circular or unusually complex;
- required documents are missing or stale;
- source reliability is too low for the review purpose.

Escalation language must be framed as a recommendation for human review, not as a final decision.

---

## 10. Limitations

The agent must clearly state limitations, including:

- unavailable registries;
- paid sources not checked;
- stale documents;
- missing ownership percentages;
- missing IDs for directors or UBOs;
- language limitations;
- inability to verify nominee or trust arrangements;
- inability to verify private company shareholders in certain jurisdictions;
- reliance on user-provided documents;
- lack of human review.

---

## 11. Relationship to other TCAML skills

TCAML-S003 should connect to:

- `TCAML-S001 AML Screening` for company and related-party screening;
- `TCAML-S002 Adverse Media Review` for company, director, shareholder, and UBO adverse media checks;
- `TCAML-S004 Website & Domain Review` when business model or digital footprint is material;
- `TCAML-S005 MLRO Escalation Memo` when findings require escalation.
