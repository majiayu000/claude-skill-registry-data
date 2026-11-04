---
name: dod-vva-rpg
description: "Knowledge base from the DoD M&S VV&A Recommended Practices Guide (RPG web edition). Use for verification, validation, and accreditation of models and simulations — role responsibilities (user, developer, M&S PM, V&V agent, accreditation agent), fidelity, validation fundamentals, data V&V, risk-informed accreditation, T&E/V&V integration, referent development, and conceptual-model validation. Complements nasa-ms-7009 and T&E packs; does not replace DoDI 5000.61 or Service VV&A policies."
---

<!-- argument-hint: [topic, role, or chapter number] -->

# DoD M&S VV&A Recommended Practices Guide (RPG)
**Source**: DoD VV&A RPG web edition (US Government work, public domain) | **Chapters**: 13

## When to use
Reach for this pack when planning or reviewing **Verification, Validation, and Accreditation (VV&A)** for defense modeling and simulation — assigning role responsibilities, scoping V&V to intended use, setting fidelity/referent expectations, validating results or data, or framing accreditation risk and residual uncertainty for decision authorities.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about accreditation, intended use, referent, fidelity, data V&V, residual risk, or a named role.
- **With a chapter** — ask for `ch01` through `ch13`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### VV&A triad
| Element | Question | Outcome |
|---------|----------|---------|
| Verification | Did we build the M&S right? | Evidence the implementation matches the conceptual model / specs |
| Validation | Did we build the right M&S? | Evidence of adequate accuracy vs the referent for intended use |
| Accreditation | Is it acceptable for this use? | Official determination by the Accreditation Authority |

### Intended use first
All V&V scope, fidelity, data pedigree, and accreditation criteria flow from a clear **intended use** statement. Vague use → unscoped V&V and non-defensible accreditation.

### Role set (new development)
User · Developer · M&S Program Manager · V&V Agent · Accreditation Agent — each owns distinct products and acceptance points; collapsing roles without independence controls weakens credibility.

### Referent and fidelity
Validation compares M&S behavior to a **referent** (reality, data, higher-fidelity model, or SME consensus) at the fidelity needed for the decision — not maximum fidelity everywhere.

### Risk couples to accreditation
Accepting incorrect M&S results (Type II) usually dominates. Residual risk after V&V must be explicit in the accreditation recommendation.

### Pack routing
- **nasa-ms-7009** — NASA models & simulations standard/handbook depth.
- **dote-te-guidebook / dod-te-guidebook** — enterprise T&E; use when M&S supports DT/OT evidence.
- **This pack** — DoD VV&A RPG role practices, validation fundamentals, data V&V, risk, T&E/V&V checklist, referent development, conceptual-model validation.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-key-concepts-and-vva-frame.md) | Key Concepts & VV&A Frame | RPG purpose, spectrum of M&S, process overview |
| [ch02](chapters/ch02-user-role-new-simulations.md) | User Role | Needs, intended use, acceptance criteria, SME input |
| [ch03](chapters/ch03-developer-role-new-simulations.md) | Developer Role | Design/build evidence, configuration, developer testing |
| [ch04](chapters/ch04-ms-pm-role-new-simulations.md) | M&S PM Role | Planning, resources, integration of VV&A into development |
| [ch05](chapters/ch05-vv-agent-role-new-simulations.md) | V&V Agent Role | V&V planning, independence, techniques, reporting |
| [ch06](chapters/ch06-accreditation-agent-role.md) | Accreditation Agent Role | Accreditation package, recommendation, authority support |
| [ch07](chapters/ch07-fidelity.md) | Fidelity | Fidelity dimensions, fitness for intended use |
| [ch08](chapters/ch08-validation-fundamentals.md) | Validation Fundamentals | Referent, comparison methods, credibility |
| [ch09](chapters/ch09-data-vv-new-simulations.md) | Data V&V | Data verification/validation, pedigree, uncertainty |
| [ch10](chapters/ch10-risk-and-vva.md) | Risk & VV&A | Development vs operational risk, Type I/II, mitigation |
| [ch11](chapters/ch11-te-vv-checklist.md) | T&E / V&V Checklist | Integration cases, criticality bins, V&V vs DT/OT partitions |
| [ch12](chapters/ch12-developing-the-referent.md) | Developing the Referent | Validation-referent identify/select/specify/approve |
| [ch13](chapters/ch13-conceptual-model-development-and-validation.md) | Conceptual Model | Context/concept/elements; conceptual-model V&V |

## Topic Index
| Topic | Chapters |
|-------|----------|
| Accreditation / authority decision | ch01, ch06, ch10 |
| Intended use & requirements | ch01, ch02, ch04 |
| Verification practices | ch03, ch05 |
| Validation / referent / face validation | ch07, ch08, ch12, ch13 |
| Data verification & validation | ch09 |
| Fidelity selection | ch07, ch08, ch12 |
| Risk, residual risk, Type I/II | ch10, ch06 |
| Role responsibilities (RACI-like) | ch02–ch06 |
| Independence of V&V | ch05, ch06 |
| Test & evaluation interface | ch01, ch05, ch10, ch11 |
| T&E / V&V checklist | ch11 |
| Conceptual model (simulation / federation) | ch13, ch03, ch08 |
| Decision analysis / evidence for decisions | ch06, ch08, ch10 |
| SME use | ch02, ch05, ch08, ch12 |

## Supporting Files
- [glossary.md](glossary.md) — VV&A terms used across chapters
- [patterns.md](patterns.md) — recurring practice patterns
- [cheatsheet.md](cheatsheet.md) — quick decision rules

## Scope & Limits
- Synthesized from selected **new-development** role guides plus fidelity, validation, data V&V, risk, T&E/V&V checklist, developing-the-referent, and conceptual-model special topics of the DoD VV&A RPG web edition (role set retrieved 2026-08-16; leftover chapters retrieved 2026-08-17). Not a substitute for DoDI 5000.61, Service regs, or program accreditation authority direction.
- Legacy-simulation role guides and the remaining ~14 special topics were not packaged (selection). The Use Case Overview is HTML-only on the live index and was not ingested.
- Does not reproduce long source passages; use official publications for citation in contracts or formal accreditation records.
