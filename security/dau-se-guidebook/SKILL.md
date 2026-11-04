---
name: dau-se-guidebook
description: "Knowledge base from the DoD Systems Engineering Guidebook (September 2026, DOPSR Case # 26-T-2032). Use for the DoD SE process model (16 processes: 8 technical management + 8 technical, mapped by method to ISO/IEC/IEEE 15288), SE Modernization (digital engineering, MBSE, MOSA, Agile), engineering resources and enablers, event-driven technical reviews and audits (ASR/SRR/SFR/PDR/CDR/SVR/FCA/PRR/PCA), the Systems Engineering Plan (SEP), TPMs and leading indicators, and the 24 design considerations. Acquisition-program oriented. Guidance not policy. Not the SoS guide."
---

<!-- argument-hint: [SE process, review/audit, SEP, TPM, design consideration, digital engineering, MOSA, Agile, chapter number] -->

# DoD Systems Engineering Guidebook (September 2026)

**Source:** US Government work, public domain (17 U.S.C. 105); Distribution A; September 2026 (DOPSR Case # 26-T-2032). See `LICENSE`.

## When to use

Use this skill for DoW/DoD acquisition SE practice under the September 2026 guidebook: the 16 SE processes, SE Modernization, engineering resources, technical reviews and audits, the SEP, and the 24 design considerations. It is guidance under policy issuances such as DoDI 5000.88 and DoDI 5000.02, not a substitute for those issuances, and not the updated SoS guide.

**Prerequisites:** none. Plain Markdown. No MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill

- **Without arguments** - load the process model, modernization spine, review sequence, and design-consideration set below.
- **With a topic** - ask about a process, a review/audit, the SEP, TPMs, a modernization theme (DE, MBSE, MOSA, Agile), or a design consideration.
- **With a program-planning question** - ask how to scale SE to an AAF pathway, staff technical leadership, or gate knowledge at PDR/CDR-class events.

## Core Frameworks & Mental Models

### Sixteen SE processes (8 + 8)

Technical management: Technical Planning, Decision Analysis, Technical Assessment, Requirements Management, Risk Management, Configuration Management, Technical Data Management, Interface Management.

Technical: Stakeholder Requirements Definition, Requirements Analysis, Architecture Design, Implementation, Integration, Verification, Validation, Transition.

Applied iteratively along a V-style life cycle. Mapped by method to ISO/IEC/IEEE 15288 process intent. Scaled to pathway, complexity, and risk.

### SE Modernization

New top-level section: tools and models, digital engineering, MBSE, mission engineering, software engineering with Agile/DevSecOps, MOSA, and SE in Agile development. Authoritative digital baselines beat document handoffs.

### Reviews and audits

Event-driven sequence: ASR, SRR, SFR, PDR, CDR, SVR/FCA, PRR, PCA. Entrance and exit logic first; criteria tables are not copied cell by cell here.

### Design considerations

Twenty-four items from accessibility through system security engineering. Screen all for relevancy; record drivers in the SEP; trade them as a coupled set.

## Chapter Index

| File | Job |
|---|---|
| [ch01-dau-se-guidebook-introduction.md](chapters/ch01-dau-se-guidebook-introduction.md) | Purpose, audience, policy relation, life-cycle framing |
| [ch02-dau-se-guidebook-system-level.md](chapters/ch02-dau-se-guidebook-system-level.md) | System-level context; SoS move noted |
| [ch03-dau-se-guidebook-se-modernization.md](chapters/ch03-dau-se-guidebook-se-modernization.md) | DE, MBSE, mission engineering, SWE, MOSA, Agile |
| [ch04-dau-se-guidebook-engineering-resources.md](chapters/ch04-dau-se-guidebook-engineering-resources.md) | Resources, workforce, lessons, contracting role |
| [ch05-dau-se-guidebook-technical-reviews-audits.md](chapters/ch05-dau-se-guidebook-technical-reviews-audits.md) | Reviews and audits, entrance/exit logic |
| [ch06-dau-se-guidebook-technical-management.md](chapters/ch06-dau-se-guidebook-technical-management.md) | Eight technical management processes and SEP |
| [ch07-dau-se-guidebook-technical-processes.md](chapters/ch07-dau-se-guidebook-technical-processes.md) | Eight technical processes; 15288 mapping method |
| [ch08-dau-se-guidebook-design-considerations.md](chapters/ch08-dau-se-guidebook-design-considerations.md) | Twenty-four design considerations |

## Topic Index

- Introduction / policy / life cycle: ch01
- System-level / FoS / SoS framing: ch02
- Digital engineering / MBSE / MOSA / Agile: ch03
- Resources / IPT / qualifications / contracting: ch04
- ASR / SRR / SFR / PDR / CDR / SVR / FCA / PRR / PCA: ch05
- SEP / TPM / risk / CM / data / interfaces: ch06
- Requirements / architecture / integration / V&V / transition: ch07
- Design considerations (24): ch08

## Supporting Files

- `glossary.md`
- `cheatsheet.md`
- `patterns.md`

## Scope & Limits

Guidance, not policy. Not a substitute for DoDI 5000.88, DoDI 5000.02, or other cited issuances. Not the updated SoS guide after the Section 2 content move. Does not reproduce review-criteria tables, SEP template cells, 15288 mapping tables, or design-consideration checklists cell by cell. Thin on detailed cost estimating, contracting law, and non-DoD commercial life cycles.
