---
name: mil-hdbk-516
description: "Knowledge base from MIL-HDBK-516D, 29 May 2026, Airworthiness Certification Criteria. Use for design AW criteria and MoCs across systems engineering, structures, flight technology, propulsion, air vehicle subsystems, crew systems and aerial refueling, avionics electrical and E3, computer systems and software, maintenance, armaments and stores, materials, and aerial delivery. Guidance handbook only. Not a service AW authority, not civil FAA or EASA rules, not detailed performance specs."
---

<!-- argument-hint: [airworthiness topic, certification basis, domain criteria, or chapter number] -->

# Airworthiness Certification Criteria (MIL-HDBK-516D)

**Source:** US Government work, public domain (17 U.S.C. 105); Distribution A; no printed DOPSR case. See `LICENSE`. Pin: MIL-HDBK-516D, 29 May 2026. Chapters: 12.

## When to use

Use when building or reviewing a DoD air system design airworthiness certification basis from MIL-HDBK-516D: tailoring criteria, assigning MoCs, and navigating domain sections including clusters D stands up alone (air vehicle subsystems, aerial refueling, electrical, maintenance, armaments and stores, materials, aerial delivery).

**Prerequisites:** none. Plain Markdown. No MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill

- **Without arguments**  -  load the core frameworks below.
- **With a topic**  -  ask a topic question (for example tailoring, structures MoCs, AR compatibility, CS&S multicore).
- **With a certification-planning question**  -  ask how to shape a basis, reopeners after modification, or evidence owners by domain.

## Core Frameworks & Mental Models

### Standard plus method of compliance

Each criterion pairs a design standard with MoCs (examination, analysis, demonstration, test). Argue the attribute; do not copy handbook tables.

### Tailored certification basis

Select a necessary and sufficient subset for the air system; document applicability; keep under configuration control with manuals and software loads.

### Guidance only

The handbook guides AW assessment. It is not cited as a requirement. Component AW authorities issue approvals under their process (including DoDI 5030.61).

### Design attribute focus

Criteria address design of the air system configuration for safe flight within approved usage limits. They are not a full process library and not civil certification rules.

## Chapter Index

| Ch | File | Focus |
| --- | --- | --- |
| 01 | [ch01-mil-hdbk-516-scope.md](chapters/ch01-mil-hdbk-516-scope.md) | Scope, publication classes, notes |
| 02 | [ch02-mil-hdbk-516-systems-engineering.md](chapters/ch02-mil-hdbk-516-systems-engineering.md) | SE, CM, system safety |
| 03 | [ch03-mil-hdbk-516-structures.md](chapters/ch03-mil-hdbk-516-structures.md) | Structures |
| 04 | [ch04-mil-hdbk-516-flight-technology.md](chapters/ch04-mil-hdbk-516-flight-technology.md) | Flight technology |
| 05 | [ch05-mil-hdbk-516-propulsion.md](chapters/ch05-mil-hdbk-516-propulsion.md) | Propulsion |
| 06 | [ch06-mil-hdbk-516-air-vehicle-subsystems.md](chapters/ch06-mil-hdbk-516-air-vehicle-subsystems.md) | Air vehicle subsystems |
| 07 | [ch07-mil-hdbk-516-crew-systems-aerial-refueling.md](chapters/ch07-mil-hdbk-516-crew-systems-aerial-refueling.md) | Crew systems and aerial refueling |
| 08 | [ch08-mil-hdbk-516-avionics-electrical-e3.md](chapters/ch08-mil-hdbk-516-avionics-electrical-e3.md) | Avionics, electrical, E3 |
| 09 | [ch09-mil-hdbk-516-computer-systems-software.md](chapters/ch09-mil-hdbk-516-computer-systems-software.md) | Computer systems and software |
| 10 | [ch10-mil-hdbk-516-maintenance.md](chapters/ch10-mil-hdbk-516-maintenance.md) | Maintenance |
| 11 | [ch11-mil-hdbk-516-armaments-stores.md](chapters/ch11-mil-hdbk-516-armaments-stores.md) | Armaments and stores |
| 12 | [ch12-mil-hdbk-516-materials-aerial-delivery.md](chapters/ch12-mil-hdbk-516-materials-aerial-delivery.md) | Materials and aerial delivery |

## Topic Index

- Scope and tailoring: ch01
- Systems engineering and system safety: ch02
- Structures: ch03
- Flight technology and VCF: ch04
- Propulsion: ch05
- Air vehicle subsystems: ch06
- Crew systems and passenger safety fold: ch07
- Aerial refueling: ch07
- Avionics and diagnostics: ch08
- Electrical system: ch08
- E3 / EMC: ch08
- Computer systems and software: ch09
- Maintenance products and inspections: ch10
- Armaments and stores: ch11
- Materials and corrosion / NDI: ch12
- Aerial delivery and airdrop: ch12
- Definitions and POCs: glossary.md

## Supporting Files

- `glossary.md`  -  definitions, acronyms, subject terms, Appendix A POC reference
- `cheatsheet.md`  -  quick map and do-not list
- `patterns.md`  -  When / How / Trade-offs patterns

## Scope & Limits

- Guidance only; not a contractual requirements document.
- Not a substitute for service airworthiness authority policy or decisions.
- Not civil FAA or EASA certification rules.
- Not a replacement for detailed JSSG or MIL performance specifications.
- Pack freezes 12 synthesized chapters from the D contents list; sections 14 and 18 are blank and omitted.
- Does not reproduce criterion catalogue cells, MoC matrices, or sample compliance evidence.
- Does not cover program-unique authority procedures beyond the handbook method.
