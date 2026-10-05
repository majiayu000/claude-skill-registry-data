---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "core"
skill_id: "TCAML-S004"
title: "Website & Domain Review Skill"
risk_area:
  - domain_ip
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
# TCAML-S004: Website & Domain Review Skill

Maintainer: Tom Custos  
Category: Human-supervised AML operations

---

## 1. Purpose

This skill defines how an AML agent should assist with structured review of websites, domains, online business presence, legal pages, digital footprint, and web-based risk indicators.

The goal is to help compliance teams understand whether the observed online presence is consistent with the declared business activity, whether material information is missing or contradictory, and whether web evidence should be escalated for human AML review.

The agent may collect, compare, summarize, screenshot, classify, and structure website and domain evidence.

The agent must not make final legal conclusions about authorization, licensing, customer acceptance, customer refusal, or regulatory status.

---

## 2. When to use

Use TCAML-S004 when an AML workflow includes any website, domain, app, landing page, merchant page, payment page, crypto platform, online brand, or public digital footprint.

Typical use cases include:

- corporate customer onboarding;
- merchant onboarding;
- crypto exchange or wallet service review;
- payment institution or fintech counterparty review;
- affiliate, introducer, or partner review;
- supplier or vendor review;
- online casino, betting, gaming, or high-risk merchant review;
- adverse media support;
- source-of-wealth or source-of-funds support;
- periodic refresh of online businesses;
- MLRO escalation preparation.

TCAML-S004 may be used after TCAML-S003 Company & UBO Review, or independently when a website/domain is the primary subject.

---

## 3. Agent may

The agent may:

- collect website and domain identifiers;
- review visible website content;
- capture screenshots or page snapshots where permitted by implementation;
- identify legal pages, contact details, business claims, and payment claims;
- compare website content against declared business activity;
- identify missing or contradictory information;
- classify evidence quality;
- record domain age, registrar, DNS, hosting, SSL, and WHOIS indicators where available;
- review app store, social media, or public profile links where within scope;
- request TCAML-S001 screening for named entities found on the website;
- request TCAML-S002 adverse media review for brand names, domains, operators, or related persons;
- request TCAML-S003 review when a company/operator is identified;
- prepare a website and domain review output for human review.

---

## 4. Agent must not

The agent must not:

- conclude final licensing or authorization status;
- conclude that a business is legal or illegal;
- conclude that a product or service is allowed or prohibited;
- approve or refuse a merchant, customer, supplier, or counterparty;
- treat website marketing claims as verified facts without supporting evidence;
- invent operator names, ownership, licences, or addresses;
- bypass access controls, paywalls, login walls, CAPTCHAs, or technical restrictions;
- perform intrusive scanning, exploitation, credential attacks, or vulnerability testing;
- collect unnecessary personal data from website users;
- make final cybersecurity conclusions;
- replace MLRO, compliance officer, legal counsel, or technical security specialist judgment.

---

## 5. Required input

The agent must collect or mark as missing:

### Website identifiers

- primary domain;
- full URL reviewed;
- brand or trading name;
- case ID, if available;
- review date and time;
- review purpose;
- declared business activity;
- expected customer type or merchant category, if available;
- related legal entity, if known;
- relevant jurisdictions, if known.

### Website content scope

- homepage;
- about page;
- contact page;
- terms of service;
- privacy policy;
- refund/cancellation policy, where relevant;
- AML/KYC policy, where relevant;
- licence/regulatory page, where relevant;
- payment/deposit/withdrawal pages, where visible;
- supported countries or restricted jurisdictions, where visible;
- product/service pages;
- app download links, where visible;
- social media or community links, where visible.

### Domain and technical metadata, where available

- domain creation date;
- domain update date;
- registrar;
- registrant information, if public and policy-permitted;
- nameservers;
- DNS records relevant to review scope;
- SSL certificate subject and issuer;
- hosting or CDN indicator;
- redirect chain;
- related subdomains, where relevant;
- historical domain evidence, where approved sources are available.

If any required input is not available, the agent must state the limitation and its effect on confidence.

---

## 6. Recommended source categories

The agent should use approved sources appropriate to the implementation:

- live website pages;
- archived website snapshots, where policy allows;
- official domain registry or WHOIS/RDAP data;
- official regulator registers;
- company registry sources;
- SSL certificate transparency sources;
- DNS lookup sources;
- trusted commercial domain intelligence providers;
- trusted commercial risk intelligence providers;
- app store listings;
- official social media profiles linked from the website;
- reputable media and public records;
- internal merchant/customer file;
- screenshots or locally stored evidence captures.

The agent must distinguish observed website content from verified official records.

---

## 7. Evidence quality for website and domain review

Use TCAML evidence quality labels:

| Grade | Website/domain evidence type |
|---|---|
| A | Official government/regulator register, court record, official company registry, official domain registry where applicable |
| B | Website content controlled by the subject, official app store listing, official corporate page, SSL certificate data |
| C | Trusted commercial domain intelligence, licensed KYB/AML provider, trusted commercial risk database |
| D | Reputable media, public research, social media, archive snapshot, public technical lookup |
| E | User-provided statement, unverified screenshot, informal claim, unsupported marketing assertion |

Website claims should normally be treated as observed statements, not independently verified facts.

---

## 8. Workflow

### Step 1: Define review scope

Identify the website, domain, brand, declared business activity, related legal entity, and reason for review.

State whether the review is:

- website/domain-only review;
- merchant onboarding support;
- corporate KYB support;
- crypto/fintech platform review;
- affiliate/partner review;
- supplier review;
- adverse media support;
- escalation support.

### Step 2: Normalize identifiers

Record the primary domain, reviewed URLs, brand names, operator names, company names, app names, and social handles found during review.

Preserve original spelling and screenshots/page references.

### Step 3: Capture core website evidence

Review and document the visible website pages within scope.

For each material page, record:

- URL;
- page title or section;
- observed claim or fact;
- capture date/time;
- evidence reference;
- evidence quality;
- whether the content is visible publicly or only after login.

### Step 4: Identify operator and legal information

Look for:

- legal entity name;
- company number;
- registered address;
- operating address;
- licence number;
- regulator name;
- terms owner/operator;
- support contacts;
- email domain consistency;
- privacy controller;
- payment processor or merchant descriptor, if visible.

If the website does not clearly identify an operator, record this as a material limitation.

### Step 5: Compare claims against evidence

Compare observed website claims with available external evidence.

Examples:

- claimed licence vs regulator register;
- claimed company name vs company registry;
- claimed jurisdiction vs terms/contact page;
- declared business activity vs website products/services;
- stated restrictions vs actual onboarding/payment flows visible to reviewer;
- email/contact domain vs website domain;
- brand name vs operator legal entity.

Contradictions must be documented without turning them into final legal conclusions.

### Step 6: Review domain and technical indicators

Where approved sources are available, document:

- domain age;
- recent registration or ownership changes;
- privacy-protected WHOIS/RDAP;
- nameserver/provider changes;
- redirect chains;
- suspiciously similar domains;
- inconsistent SSL certificate names;
- short-lived infrastructure;
- high-risk hosting indicators, where source-supported.

Technical indicators must be treated as risk indicators for human review, not standalone proof of misconduct.

### Step 7: Identify web-based risk indicators

Record relevant indicators such as:

- no legal entity disclosed;
- no physical address or only vague address;
- no terms/privacy pages;
- inconsistent operator information;
- impossible or unverifiable licence claims;
- high-risk product claims inconsistent with declared activity;
- anonymous crypto payment flow;
- no KYC/AML information for regulated/high-risk activity;
- aggressive guaranteed-return language;
- misleading regulatory badges;
- restricted jurisdictions not disclosed;
- newly registered domain for high-risk activity;
- copied or generic legal pages;
- unresolved adverse media connected to brand/domain/operator;
- mismatch between website language, target market, and claimed jurisdiction.

The agent must tie each indicator to evidence.

### Step 8: Request linked TCAML skills where needed

Use related skills when appropriate:

- TCAML-S001 for screening named operators, directors, owners, brands, or companies;
- TCAML-S002 for adverse media on brand, domain, operator, or related persons;
- TCAML-S003 for company/UBO review when an operator entity is identified;
- TCAML-S005 for escalation memo when findings require structured human review.

### Step 9: Explain confidence and limitations

Classify confidence as Low, Medium, or High.

Lower confidence may result from:

- inaccessible pages;
- login-only content;
- missing legal pages;
- missing operator information;
- unavailable domain data;
- only website self-claims available;
- conflicting official and website information;
- outdated cached evidence;
- language translation uncertainty;
- inability to verify licence or company claims.

### Step 10: Prepare human-reviewable output

The output must include:

- case metadata;
- domain and brand identifiers;
- website pages reviewed;
- operator/legal information observed;
- domain/technical metadata;
- claims and verification status;
- risk indicators;
- evidence log;
- confidence and limitations;
- recommended human follow-up.

The output must not include final acceptance/refusal wording.

---

## 9. Website claim labels

Use the following labels for material claims found on the website:

| Label | Meaning |
|---|---|
| Observed | Claim was visible on the website but not externally verified |
| Source-supported | Claim is supported by an external source reviewed by the agent |
| Contradicted | Claim appears inconsistent with another reviewed source |
| Not verifiable | Agent could not verify the claim with available sources |
| Not reviewed | Claim was outside available scope or not checked |

---

## 10. Domain risk signal labels

Use the following labels for technical/domain observations:

| Label | Meaning |
|---|---|
| Neutral | No material risk indicator observed from available data |
| Information gap | Missing or unavailable data affects confidence |
| Inconsistency | Domain/technical data conflicts with website or case data |
| Recency signal | Domain or infrastructure appears recent or recently changed |
| Similarity signal | Domain appears similar to another brand/domain and may require review |
| Escalation signal | Source-supported technical/domain indicator should be reviewed by a human |

---

## 11. Escalation triggers

Escalation to human compliance review is recommended when any of the following are observed:

- website does not disclose a legal operator for regulated or high-risk activity;
- claimed licence cannot be matched to an official regulator source;
- website operator differs from customer-provided company data;
- payment/deposit flow appears inconsistent with declared business model;
- domain is very new for a high-risk merchant or financial activity;
- legal pages are missing, contradictory, copied, or unrelated to the brand;
- restricted/high-risk jurisdictions are targeted without clear controls;
- website claims guaranteed returns, anonymity, no-KYC access, or similar high-risk features;
- adverse media connects the domain, brand, or operator to financial crime risk;
- website contains sanctions evasion, fraud, unlicensed financial service, or deceptive marketing indicators;
- the agent cannot identify who operates the website.

Escalation means human review is required. It does not mean the agent has reached a final compliance decision.

---

## 12. Output requirements

The agent must produce:

1. case information;
2. website/domain identity;
3. pages reviewed;
4. operator/legal information;
5. domain/technical metadata;
6. claims verification table;
7. risk indicators;
8. evidence log;
9. confidence rating with reasons;
10. limitations;
11. recommended human follow-up.

The agent should use `templates/website-domain-review.md` where possible.

---

## 13. Human review

Human review is required before any operational or compliance action is taken.

The human reviewer should decide:

- whether additional documents are required;
- whether company/UBO review is required;
- whether licence verification is sufficient;
- whether adverse media review is required;
- whether the case should be escalated to MLRO;
- whether the risk is acceptable under internal policy.

The agent must preserve uncertainty and make limitations visible.

---

## 14. Limitations

Website and domain review may be incomplete because:

- pages change over time;
- content may differ by country, device, account status, or language;
- parts of the website may require login;
- domain data may be privacy-protected;
- technical lookup data may be stale or incomplete;
- screenshots may not capture dynamic content;
- translation may introduce uncertainty;
- website claims may be intentionally misleading;
- absence of a red flag is not proof of low risk.

The agent must not treat a clean website review as proof of compliance.
