---
name: rseng-regulatory-compliance
description: >-
  Covers checking research code and data against data-protection and AI
  regulation: GDPR obligations in code (personal data discovery, minimization,
  pseudonymization vs anonymization, retention, data-subject rights, DPIA
  triggers), the EU AI Act (risk tiers, research carve-out, transparency
  duties), and similar regimes. Use PROACTIVELY when person-level or sensitive
  data is evident in the project, and when a project processes personal or
  sensitive data, trains or ships AI/ML systems, when the user asks about
  GDPR, the AI Act, DPIAs, consent or anonymization, or before publishing
  datasets or models derived from people. (Secrets hygiene and protective
  controls: rseng-security; sensitive-data stewardship: rseng-data-management;
  AI-use disclosure: rseng-ai-declaration.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Regulatory compliance for research code and data

Regulation reaches research software the moment code touches
personal data or ships an AI system. An agent cannot certify
compliance - that is a legal judgment owned by the institution's
data protection officer (DPO), ethics board and legal office - but
it CAN do the engineering half: find the personal data, check the
code against the obligations that have code-shaped answers, prepare
the documentation reviewers need, and flag exactly what requires a
human decision. State that division of labor explicitly whenever
this skill is used. Not legal advice.

## GDPR: what an agent can check in code and data

Personal data discovery first - obligations attach to data you HAVE:

- Scan datasets, logs, configs and repo history for personal data:
  names, emails, identifiers, IP addresses, free-text fields that
  smuggle PII, geolocation precise enough to identify. Automated PII
  detection (Presidio-class tools) finds the bulk; manual review
  covers domain-specific identifiers (patient codes, student IDs).
  Repository history counts - committed-then-deleted data is still
  there (rseng-security's leak response applies).
- Check the code paths, not just the files: what gets logged
  (debug logging of request payloads is a classic leak), what lands
  in error reports and caches, what third-party services receive
  (telemetry, cloud APIs) - each is a processing activity.

Obligations with code-shaped answers:

- Minimization: collect and keep only fields the research question
  needs; challenge every column (rseng-data-management's data
  dictionary makes this reviewable).
- Pseudonymization vs anonymization - keep the distinction sharp:
  pseudonymized data (key exists somewhere) is still personal data
  under GDPR; true anonymization is hard, and removing names is not
  it (re-identification via quasi-identifiers is the standard
  failure). Treat "anonymized" claims as claims to verify with the
  data steward, not labels to accept.
- Retention: implement it - deletion jobs, dated cohorts, expiry in
  the pipeline - a retention policy without code is a wish.
- Data-subject rights: for anything service-shaped, access/export/
  erasure must be executable; check that erasure reaches backups,
  caches, derived datasets and trained artifacts, or documents why
  it cannot.
- Security of processing: encryption in transit and at rest,
  access control, and the sensitive-data handling rules already in
  rseng-data-management and rseng-security.
- DPIA triggers: large-scale processing of special categories
  (health, biometrics, ethnicity...), systematic monitoring, new
  technologies on vulnerable groups - when the project matches,
  prepare the processing inventory and route to the DPO; do not
  improvise the assessment.

## EU AI Act: research software that is or contains AI

- Locate the project honestly on the map: the Act regulates by risk
  tier (prohibited practices, high-risk uses, transparency-tier,
  minimal). Annex-listed high-risk areas (health, education,
  employment, law enforcement...) matter the moment research
  prototypes head toward deployment.
- The scientific-research carve-out: AI developed and used SOLELY
  for scientific research and development is outside the Act's
  scope - but the exemption ends where real-world deployment
  begins. A model handed to a hospital, a public demo, a spin-off:
  each crosses the line and the obligations arrive. Flag the
  transition explicitly; it is the single most important thing for
  a research team to notice in time.
- Obligations an agent can prepare for when in or near scope:
  technical documentation and logging capability, training-data
  documentation and governance (dataset provenance -
  rseng-data-management, rseng-fair-ml), accuracy/robustness
  testing evidence (rseng-testing), transparency notices for
  AI-interacting users, and human-oversight hooks. The project's
  aidecl.yaml (rseng-ai-declaration) is a natural seed for the
  documentation trail.
- General-purpose model obligations (training-data summaries,
  copyright policy) sit with model providers - relevant when the
  research project IS training and releasing such models.

## Other regimes, same method

The pattern generalizes: identify regulated material (US HIPAA for
health data, sectoral and national laws, export controls on some
domains), find where code touches it, check the code-shaped
obligations, document, and route judgment calls to the responsible
office. When the user's jurisdiction is known, name the regime;
when not, ask - jurisdiction changes the answer.

## The compliance check, as a workflow

1. Inventory: what personal/regulated data exists, where, and which
   code processes it (a data-flow sketch pays for itself at DPIA
   time).
2. Scan: automated PII detection over data, logs and history;
   review hits.
3. Check the code-shaped obligations above; file findings as issues
   with severity (rseng-version-control-review).
4. Prepare documentation: processing inventory, retention map, AI
   Act tier assessment draft, gaps list.
5. Route: DPO/ethics/legal for judgments; record their decisions in
   the repository (rseng-documentation) and revisit at each release
   (rseng-publishing-releasing) - compliance drifts like code does.

## Working with this skill

This skill is source-independent: its authority is the regulations
themselves and the official guidance linked below. It engineers the
checkable half and routes the rest; rseng-data-management owns
sensitive-data storage practice, rseng-security owns the protective
controls, rseng-ai-declaration owns AI-use disclosure.

Learn more (verified):
  - https://eur-lex.europa.eu/eli/reg/2016/679/oj - GDPR, official
    text
  - https://eur-lex.europa.eu/eli/reg/2024/1689/oj - EU AI Act,
    official text
  - https://artificialintelligenceact.eu - AI Act explorer and
    compliance resources
  - https://www.edpb.europa.eu - European Data Protection Board
    guidance
  - https://gdpr.eu - GDPR explainers and checklists
  - https://github.com/data-privacy-stack/presidio - PII detection tooling

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ai-declaration - seeds AI Act documentation trail
- rseng-archiving - publishing datasets triggers obligations
- rseng-data-management - sensitive-data storage and stewardship
- rseng-fair-ml - training-data documentation duties
- rseng-security - encryption, access control, leak response
- rseng-testing - robustness evidence for AI Act

<!-- related-skills:end -->
