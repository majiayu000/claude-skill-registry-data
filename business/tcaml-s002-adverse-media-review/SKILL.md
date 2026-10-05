---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "core"
skill_id: "TCAML-S002"
title: "Adverse Media Review Skill"
risk_area:
  - adverse_media
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
# TCAML-S002: Adverse Media Review Skill

Maintainer: Tom Custos  
Category: Human-supervised AML operations

---

## 1. Purpose

This skill defines how an AML agent should assist with structured adverse media review for individuals, companies, directors, UBOs, counterparties, websites, merchants, and related subjects.

The goal is to help compliance teams identify, document, and summarize public risk information without turning unverified allegations into final conclusions.

The agent may collect, organize, compare, summarize, and prepare evidence for human review.

The agent must not make final compliance decisions, legal conclusions, or factual determinations that are not supported by evidence.

---

## 2. When to use

Use TCAML-S002 when an AML workflow requires review of public risk information, including:

- onboarding review;
- enhanced due diligence;
- periodic KYC refresh;
- counterparty review;
- sanctions or PEP match context;
- company, director, or UBO review;
- transaction monitoring case support;
- merchant or website risk review;
- MLRO escalation preparation.

Adverse media review may be used as a standalone skill or after TCAML-S001 AML Screening.

---

## 3. Agent may

The agent may:

- collect search terms and known identifiers;
- generate search strategies;
- search or request searches across approved sources;
- summarize relevant public findings;
- distinguish confirmed facts from allegations;
- record source dates, publication dates, and access dates;
- classify evidence quality;
- assess relevance to the subject under review;
- identify missing context;
- prepare an adverse media summary;
- recommend human review or escalation.

---

## 4. Agent must not

The agent must not:

- present an allegation as a confirmed fact;
- claim that absence of media means absence of risk;
- suppress relevant negative findings;
- rely only on headlines when article content is available;
- ignore publication date or source credibility;
- treat low-quality reposts as equal to official sources;
- translate or paraphrase in a way that changes legal meaning;
- make legal conclusions;
- decide whether a customer should be accepted or refused;
- replace MLRO or compliance officer judgment.

---

## 5. Required input

The agent must collect or mark as missing:

### For individuals

- full name;
- aliases or alternative spellings;
- date of birth, if available;
- nationality, if available;
- country of residence, if available;
- role in the case;
- related company names, if available;
- relevant jurisdictions;
- case ID, if available.

### For entities

- legal name;
- trading names;
- registration number, if available;
- incorporation jurisdiction, if available;
- operating countries;
- directors, if available;
- UBOs, if available;
- website or domain, if available;
- industry or business activity;
- case ID, if available.

If identifiers are missing, the agent must state how missing data affects search quality and confidence.

---

## 6. Search strategy

The agent should build a transparent search strategy before summarizing findings.

### Core search terms

Use combinations of:

- exact subject name;
- name variants;
- aliases;
- company names;
- director or UBO names;
- domain or brand names;
- country or jurisdiction names;
- industry terms;
- risk keywords.

### Risk keyword categories

Risk keywords may include terms related to:

- sanctions;
- fraud;
- money laundering;
- bribery and corruption;
- terrorism financing;
- organized crime;
- tax evasion;
- regulatory enforcement;
- licence suspension;
- consumer complaints;
- insolvency or bankruptcy;
- litigation;
- asset freezing;
- cybercrime;
- scams;
- illegal gambling;
- unlicensed financial services.

The agent should adapt keywords to the language and jurisdiction of the subject where appropriate.

---

## 7. Recommended source categories

The agent should use approved sources appropriate to the implementation:

- regulator notices;
- law enforcement notices;
- court records;
- official government publications;
- company registries;
- insolvency registries;
- reputable media;
- NGO or research reports;
- trusted commercial adverse media providers;
- internal case history;
- public complaint platforms, where permitted by policy.

The agent must list which sources were checked and must not imply that unchecked sources were reviewed.

---

## 8. Workflow

### Step 1: Define subject and scope

Identify the subject, related persons/entities, jurisdictions, time period, and review purpose.

The agent should state whether the review is:

- standard onboarding adverse media;
- enhanced due diligence;
- event-driven review;
- periodic refresh;
- escalation support.

### Step 2: Build search terms

Create search terms using the subject identifiers and risk keyword categories.

The output should include the main queries or query patterns used, unless internal policy restricts disclosure.

### Step 3: Collect potential findings

For each potential finding, record:

- source name;
- source type;
- title or record description;
- publication date;
- access date;
- URL or internal evidence reference;
- subject relationship;
- short summary;
- evidence quality grade.

### Step 4: Assess relevance

For each finding, assess whether it appears related to the subject under review.

Consider:

- exact name match;
- alias match;
- identifiers;
- company or role match;
- jurisdiction match;
- time period;
- source context;
- whether the finding may refer to a different person or entity.

Use one of the following relevance labels:

- `Not relevant`
- `Unclear relevance`
- `Possibly relevant`
- `Likely relevant`
- `Directly relevant`

### Step 5: Distinguish fact status

The agent must distinguish confirmed information from allegations.

Use one of the following fact-status labels:

- `Confirmed official record`
- `Regulatory or law enforcement notice`
- `Court record or proceeding`
- `Media allegation`
- `Opinion or commentary`
- `User-provided claim`
- `Unverified repost`
- `Insufficient context`

### Step 6: Classify risk theme

Classify each relevant finding by risk theme, such as:

- sanctions exposure;
- financial crime;
- fraud or scam;
- bribery or corruption;
- regulatory enforcement;
- litigation;
- insolvency;
- consumer harm;
- cybercrime;
- high-risk sector;
- reputational concern;
- other.

### Step 7: Assign severity for human review

The agent may use the following operational severity labels:

- `No relevant adverse media identified in sources checked`
- `Low concern - contextual note`
- `Medium concern - human review recommended`
- `High concern - escalate`
- `Insufficient data - additional review required`

These labels are not final compliance decisions.

### Step 8: Assign confidence

The agent must assign confidence:

- Low;
- Medium;
- High.

Confidence must be explained using specific reasons.

Confidence should be reduced when identifiers are weak, sources are low quality, relevance is unclear, or important sources could not be checked.

### Step 9: Prepare output

The agent must produce a structured output containing:

- review scope;
- sources checked;
- search terms used;
- relevant findings;
- findings excluded as not relevant;
- risk themes;
- severity for human review;
- confidence;
- limitations;
- recommended next human action.

---

## 9. Evidence quality

Use the TCAML evidence quality labels:

| Grade | Evidence type |
|---|---|
| A | Official government, regulator, court, registry, sanctions authority |
| B | Official company or institution source |
| C | Trusted commercial or licensed data provider |
| D | Reputable media, public records, NGO or research source |
| E | User-provided or unverified source |

Where evidence quality is unclear, mark it as `Unknown` and explain why.

---

## 10. Source credibility guidance

### Higher credibility indicators

- official regulator, court, or law enforcement source;
- named author or institution;
- original reporting;
- dated publication;
- supporting documents;
- multiple independent sources;
- clear subject identifiers.

### Lower credibility indicators

- anonymous blog post;
- social media claim without corroboration;
- copied article with no original source;
- missing publication date;
- sensational headline unsupported by content;
- unclear relation to the subject;
- source appears promotional, extortionate, or spam-like.

The agent should not automatically discard lower credibility sources, but must label them appropriately.

---

## 11. Recency and relevance guidance

The agent should record the publication date and explain relevance.

Older findings may remain relevant when they involve:

- sanctions;
- criminal conviction;
- regulatory enforcement;
- licence revocation;
- serious fraud;
- corruption;
- unresolved litigation;
- ongoing restrictions;
- repeated conduct pattern.

Older findings may be less relevant when they involve:

- minor resolved disputes;
- outdated allegations without follow-up;
- unrelated namesakes;
- events before current ownership or management, where clearly evidenced.

The agent must not ignore older findings solely because they are old.

---

## 12. Escalation triggers

The agent must recommend escalation when any of the following occur:

- official sanctions, enforcement, law enforcement, or court source is identified;
- finding indicates money laundering, terrorism financing, bribery, corruption, fraud, organized crime, cybercrime, or serious consumer harm;
- adverse media relates directly to the reviewed subject and is unresolved;
- multiple independent sources report similar serious allegations;
- source identifies a director, UBO, or controlling party in a high-risk matter;
- subject appears connected to banned, restricted, or unlicensed activity;
- relevance cannot be resolved but the potential risk is material;
- internal policy threshold is met.

---

## 13. Output requirement

The output must be suitable for human review.

It should make clear:

- what was searched;
- what was found;
- what was excluded and why;
- what remains unknown;
- which findings are allegations and which are official records;
- what evidence supports each finding;
- what human action is recommended.

---

## 14. Completion criteria

A TCAML-S002 review is complete only when:

- subject identifiers are recorded;
- search scope is defined;
- search terms or query patterns are documented;
- sources checked are listed;
- relevant findings are summarized;
- non-relevant findings are documented where material;
- evidence quality is labelled;
- fact status is labelled;
- confidence is assigned and explained;
- next human action is stated.

If these conditions are not met, the output should be marked incomplete.
