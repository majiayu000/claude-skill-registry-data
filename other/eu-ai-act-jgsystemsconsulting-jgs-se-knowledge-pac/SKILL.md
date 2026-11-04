---
name: eu-ai-act
description: "Knowledge base from EU Artificial Intelligence Act — Regulation (EU) 2024/1689. Use for AI system classification (high-risk vs prohibited vs general), conformity assessment procedures, GPAI model obligations, transparency and disclosure requirements, governance structure (AI Office / AI Board), penalty tiers, value-chain operator obligations, post-market monitoring, and Annex III use-case analysis. Does not cover EU liability rules for AI (separate proposed directive) or implementation guidance documents issued after July 2024."
---
<!-- argument-hint: [topic, article number, or chapter slug e.g. ch04, gpai, annex-iii, penalties, transparency] -->

# EU Artificial Intelligence Act — Regulation (EU) 2024/1689

**Source**: European Union, Official Journal (reproduction authorised with source acknowledgement, Decision 2011/833/EU) | **Chapters**: 12

## When to use

Use this skill when classifying an AI system under the EU risk framework, determining which obligations apply to a provider, deployer, importer, distributor, or GPAI model provider, or analysing penalties and enforcement. It is the primary reference for any EU market compliance question involving AI systems or foundation/GPAI models placed on the Union market from 2025 onward. Use it before advising on AI product design, contract structure between value-chain parties, or incident response procedures.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill

- **Without arguments** — load the core frameworks and classification rules.
- **With a topic** — ask about "GPAI systemic risk", "biometric ID prohibition", "conformity assessment route", "FRIA", "value chain liability", "serious incident reporting", "transparency obligations", "Annex III area 4 employment AI".
- **With a chapter** — ask for `ch03` (classification), `ch04` (requirements), `ch08` (GPAI), `ch12` (Annex III use cases).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks and Mental Models

### 1. The Four-Tier Risk Architecture

The Act organises AI systems into four tiers, each with escalating obligations:

| Tier | Trigger | Consequence |
|------|---------|-------------|
| **Prohibited** | Art 5 — 8 specific practices | Absolute ban; no compliance route; applies from 2 Feb 2025 |
| **High-risk** | Art 6 Route A (Annex I product + third-party conformity assessment) OR Route B (Annex III use-case area, unless de minimis applies) | Full Ch III obligations: RMS, data governance, docs, logging, transparency, human oversight, accuracy/robustness/cybersecurity; conformity assessment; CE marking; EU database registration |
| **Transparency-only** | Art 50 — human-AI interaction, synthetic content generation, emotion recognition, biometric categorisation, deep fakes | Disclosure and machine-readable labelling obligations; applies to any AI system, regardless of risk tier |
| **GPAI** | Ch V — AI models trained at scale displaying significant generality | Baseline obligations for all GPAI; systemic-risk tier (>10^25 FLOPs or Commission designation) adds adversarial testing, incident reporting, and cybersecurity |

### 2. Classification Decision Logic (Art 6)

**Route A (product safety)**: AI system = safety component of an Annex I-sector product AND that product requires third-party conformity assessment under sector law → HIGH-RISK.

**Route B (use-case list)**: AI system falls within an Annex III area → HIGH-RISK, unless the Art 6(3) de minimis carve-out applies. De minimis applies if the system: (a) performs a narrow procedural task, OR (b) improves the result of a previously completed human activity, OR (c) detects decision-making patterns without influencing prior human assessment, OR (d) performs a preparatory task to an Annex III assessment. **Override**: if the system performs profiling of natural persons, de minimis never applies — it is always high-risk.

Providers claiming de minimis must document the assessment and register in the EU database (Art 6(4)).

### 3. The Seven High-Risk Requirements (Art 8-15)

All seven apply cumulatively to every high-risk AI system. They must be met before placement on the market and maintained throughout the system's lifecycle:

1. **Risk Management System** (Art 9) — continuous iterative 4-step process; residual risk must be acceptable.
2. **Data Governance** (Art 10) — training/validation/testing data quality; bias detection and mitigation; strict conditions for special-category personal data use in bias correction.
3. **Technical Documentation** (Art 11) — Annex IV content; drawn up before placement; kept up to date; SMEs may use simplified form.
4. **Automatic Logging** (Art 12) — technically built into the system; biometric ID systems have enhanced minimum logging requirements.
5. **Transparency to Deployers** (Art 13) — instructions for use covering 7 content categories; enables deployer compliance with their own obligations.
6. **Human Oversight** (Art 14) — oversight measures enabling understanding, anti-bias awareness, output interpretation, override capability, and system interruption (stop button). Biometric ID: minimum two-person verification before action.
7. **Accuracy, Robustness, Cybersecurity** (Art 15) — declared accuracy metrics; resilience to errors; feedback-loop mitigation; AI-specific attack defence (data/model poisoning, adversarial examples).

### 4. Operator Roles and Liability Transfer

The Act assigns obligations by role in the supply chain:
- **Provider** (Art 16): Bears the heaviest burden — QMS, conformity assessment, CE marking, EU database registration, 10-year documentation retention, corrective actions.
- **Deployer** (Art 26): Follow instructions for use; assign and train human oversight persons; retain logs ≥6 months; notify workers; FRIA if public body; inform affected persons.
- **Importer** (Art 23): Verify conformity before placement; retain docs 10 years.
- **Distributor** (Art 24): Verify CE marking and DoC before making available.
- **Liability transfer** (Art 25): A party becomes the provider (and assumes all provider obligations) if it: affixes its name/trademark; makes a substantial modification; or changes the intended purpose to make a non-high-risk system high-risk.

### 5. GPAI Two-Tier Regime (Chapter V)

All GPAI providers: technical documentation (Annex XI), downstream provider information (Annex XII), copyright policy, training data summary. Open-source GPAI models are exempt from documentation and downstream information obligations — unless the model has systemic risk.

Systemic-risk GPAI providers additionally: adversarial testing (red-teaming), systemic risk assessment and mitigation, serious incident reporting to AI Office, cybersecurity protection. The 10^25 FLOPs training-compute threshold creates a rebuttable presumption of systemic risk. Notification to Commission required within 2 weeks of threshold being met. Commission has exclusive enforcement jurisdiction over GPAI (Art 88).

### 6. Governance Architecture

**Union level**: AI Office (Commission function, exclusive GPAI enforcement) → European AI Board (Member State representatives, advisory) → Advisory Forum (stakeholders) → Scientific Panel (independent experts, GPAI risk alerts).

**Member State level**: Notifying authority (notified body oversight) + Market surveillance authority (post-placement enforcement for non-GPAI AI systems). Each Member State designates one MSA as single point of contact.

### 7. Penalty Logic

Three national-authority tiers (Art 99): 7%/EUR 35M for prohibited practices; 3%/EUR 15M for operator/transparency obligation violations; 1%/EUR 7.5M for misleading information supply. Commission fines for GPAI violations (Art 101): 3%/EUR 15M. SMEs always pay the lower of the percentage or absolute amount. Fines are calculated on total worldwide annual turnover.

### 8. Key Application Dates

Prohibited practices applied from 2 February 2025. Full Act applies from 2 August 2026. GPAI obligations apply from 2 August 2025. Product-safety-route (Art 6(1)) AI applies from 2 August 2027.

## Chapter Index

| # | File | Key content |
|---|------|-------------|
| 1 | [ch01-general-provisions.md](chapters/ch01-general-provisions.md) | Subject matter, scope, 68 statutory definitions, AI literacy obligation |
| 2 | [ch02-prohibited-practices.md](chapters/ch02-prohibited-practices.md) | Eight prohibited AI practices; real-time RBIS conditional ban; applies from 2 Feb 2025 |
| 3 | [ch03-high-risk-classification.md](chapters/ch03-high-risk-classification.md) | Art 6 two-route classification; Art 6(3) de minimis carve-out; Art 7 dynamic amendment; Annex III overview |
| 4 | [ch04-high-risk-requirements.md](chapters/ch04-high-risk-requirements.md) | Seven requirements: RMS, data governance, technical docs, logging, transparency, human oversight, accuracy/robustness/cybersecurity |
| 5 | [ch05-obligations-operators.md](chapters/ch05-obligations-operators.md) | Provider QMS; value-chain obligations; Art 25 liability transfer; deployer FRIA; documentation retention |
| 6 | [ch06-conformity-assessment.md](chapters/ch06-conformity-assessment.md) | Conformity assessment routes; notified bodies; harmonised standards; CE marking; EU database registration; AI regulatory sandboxes |
| 7 | [ch07-transparency-obligations.md](chapters/ch07-transparency-obligations.md) | Art 50 four transparency obligations: chatbot disclosure, synthetic content labelling, emotion/biometric disclosure, deep fake disclosure |
| 8 | [ch08-general-purpose-ai.md](chapters/ch08-general-purpose-ai.md) | GPAI classification; 10^25 FLOPs threshold; baseline and systemic-risk obligations; open-source exception; codes of practice |
| 9 | [ch09-governance.md](chapters/ch09-governance.md) | AI Office; European AI Board; Advisory Forum; Scientific Panel; national competent authorities; enforcement architecture |
| 10 | [ch10-post-market-surveillance.md](chapters/ch10-post-market-surveillance.md) | EU database; post-market monitoring; serious incident reporting timelines; market surveillance powers; right to explanation; right to complain |
| 11 | [ch11-penalties-enforcement.md](chapters/ch11-penalties-enforcement.md) | Three penalty tiers; GPAI fines; codes of conduct for non-high-risk AI; Commission implementation guidelines |
| 12 | [ch12-annex-iii-high-risk-usecases.md](chapters/ch12-annex-iii-high-risk-usecases.md) | Full Annex III eight-area taxonomy with sub-category detail; classification rationale; dynamic amendment |

## Topic Index

- **AI system definition** → ch01
- **Annex III use cases / high-risk areas** → ch12, ch03
- **Biometric identification** → ch02, ch03, ch04, ch12
- **CE marking** → ch06
- **Chatbot / human-AI interaction disclosure** → ch07
- **Classification (high-risk vs not)** → ch03
- **Codes of conduct (voluntary)** → ch11
- **Codes of practice (GPAI)** → ch08
- **Conformity assessment** → ch06
- **Copyright (GPAI training data)** → ch08
- **Data governance / training data** → ch04
- **Deep fakes** → ch07
- **Deployer obligations** → ch05
- **Documentation / technical documentation** → ch04, ch05, ch06
- **Election / democracy AI** → ch12
- **Employment AI** → ch12
- **Enforcement / market surveillance** → ch10
- **EU database registration** → ch06, ch10
- **Fines / penalties** → ch11
- **FRIA (Fundamental Rights Impact Assessment)** → ch05
- **General-purpose AI (GPAI) models** → ch08, ch09
- **Governance structure** → ch09
- **Human oversight / automation bias** → ch04
- **Importer / distributor obligations** → ch05
- **Law enforcement AI** → ch02, ch12
- **Logging / record-keeping** → ch04, ch05
- **Open-source AI** → ch01, ch08
- **Post-market monitoring** → ch10
- **Prohibited practices** → ch02
- **Provider obligations** → ch05
- **Quality Management System (QMS)** → ch05
- **Real-time remote biometric identification (RBIS)** → ch02
- **Regulatory sandbox** → ch06
- **Risk management system (RMS)** → ch04
- **Scope / applicability** → ch01
- **Serious incident reporting** → ch10
- **SME provisions** → ch04, ch06, ch11
- **Social scoring** → ch02
- **Synthetic content / watermarking** → ch07
- **Systemic risk (GPAI)** → ch08
- **Transparency obligations** → ch07
- **Value chain / liability transfer** → ch05

## Supporting Files

- [glossary.md](glossary.md) — ~60 statutory and synthesised definitions from Art 3 and operative provisions.
- [patterns.md](patterns.md) — 12 when/how/trade-offs blocks covering classification, data governance, conformity assessment, incident reporting, GPAI self-assessment, and more.
- [cheatsheet.md](cheatsheet.md) — Quick-reference tables: application timeline, classification decision tree, Annex III areas, penalty tiers, requirement checklist, operator obligations, GPAI obligations matrix, serious incident reporting timelines, governance architecture.

---

## Scope and Limits

**Covers**: All 13 Chapters and key Annexes (I, III, IV, V, VIII, XI, XII) of Regulation (EU) 2024/1689 as published in the Official Journal on 12 July 2024. Includes all definitional, substantive, procedural, governance, and penalty provisions.

**Does not cover**: The proposed EU AI Liability Directive (separate instrument, not yet adopted at source knowledge date); post-July-2024 Commission guidelines, implementing acts, or delegated acts issued under the Act; national transposition measures; harmonised standards (to be developed by CEN/CENELEC); or codes of practice approved after the knowledge cutoff.

**Licence**: European Union, Official Journal, 12 July 2024. Reproduction authorised with source acknowledgement under Decision 2011/833/EU. No rights subsist in the synthesised analysis beyond the source text.
