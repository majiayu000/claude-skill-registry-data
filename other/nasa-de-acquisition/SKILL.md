---
name: nasa-de-acquisition
description: "Knowledge base for NASA-HDBK-1004A, approved 2026-10-26 (NASA Digital Engineering Acquisition Framework Handbook). Use when planning or reviewing acquisition of digital engineering data and models: Data Requirements Description (DRD) instrument and template library, Recommended Contract Language (RCL) selection, SOW/RFP/cost-volume placement, data rights and access, guiding principles and planning questions, configuration and data management patterns, and interoperability considerations. Guidance handbook; language binds only after incorporation into a contract instrument. Does not reproduce ISO, ASME, MIL-STD, or SAE standard text, FAR/DFARS clause text, RCL rows, matrix cells, or DRD template fields. Companion practitioner depth may sit in NASA-HDBK-1009; this pack records the pairing without reproducing it."
---

<!-- argument-hint: [DRD / RCL / contract language / data rights / guiding questions / principles / lessons / interoperability / chapter number] -->

# NASA Digital Engineering Acquisition Framework Handbook (NASA-HDBK-1004A)

**Source**: NASA, Office of the NASA Chief Engineer (US Government work, public domain) | **Chapters**: 8

## Version and jurisdiction

- **Pin**: NASA-HDBK-1004A, approved 2026-10-26.
- **Tier**: 1 public-domain US Government work (17 U.S.C. 105).
- **Public release**: cover line APPROVED FOR PUBLIC RELEASE--DISTRIBUTION IS UNLIMITED.
- **DOPSR**: no printed DOPSR case on the vetted cover text layer.
- **Licence detail**: see `LICENSE`.
- **Limits**: pack synthesizes handbook guidance in original words. Named third-party standards and clause families stay with their publishers. No download link is published.

## When to use

**Prerequisites:** none. Plain Markdown. No MCP server, API key, or licence tier needed at runtime.

Use this skill to plan, tailor, and review how a NASA program or project buys digital data and models across Pre-Phase A through Phase F: selecting DRDs, placing contract language, setting data rights and access, and feeding a Digital Engineering Ecosystem without treating the handbook as a self-executing requirement.

## How to use

- **No arguments** : load the framework path: scope, overview, lessons, principles, questions, contract-language method, RCL selection, DRD library.
- **With a topic** : ask about DRD templates, RCL selection, data rights, FAIR-oriented principles, guiding questions, CDM SOW patterns, or interoperability.
- **With a chapter** : `ch01` scope, `ch05` questions, `ch06` contract language, `ch07` RCL matrix, `ch08` DRD library.

## Core path

1. Treat the handbook as guidance; bind only through contract instruments (ch01).
2. Frame the Digital Engineering Ecosystem and planning artifacts (ch02).
3. Apply lessons: missing rights and formats become paid re-work (ch03).
4. Filter choices with guiding principles (ch04).
5. Answer guiding questions before selecting RCL (ch05).
6. Place language across SOW, DRD, solicitation, and cost volume (ch06).
7. Select and tailor RCL via the matrix method (ch07).
8. Select and tailor DRD templates from the library (ch08).

## Chapter Index

| # | Source area | Key content |
|---|-------------|-------------|
| [ch01](chapters/ch01-nasa-de-acquisition-scope.md) | Sections 1-2 | Scope, guidance status, cited-document classes |
| [ch02](chapters/ch02-nasa-de-acquisition-overview.md) | Section 4 | DE acquisition overview, Digital Engineering Ecosystem |
| [ch03](chapters/ch03-nasa-de-acquisition-lessons-learned.md) | Section 5 | Lessons and failure patterns for data acquisition |
| [ch04](chapters/ch04-nasa-de-acquisition-guiding-principles.md) | Section 6 | Guiding principles for data-centric acquisition |
| [ch05](chapters/ch05-nasa-de-acquisition-guiding-questions.md) | Section 7 | Guiding-question method before RCL selection |
| [ch06](chapters/ch06-nasa-de-acquisition-contract-language.md) | Section 8 | Contract-language method and placement |
| [ch07](chapters/ch07-nasa-de-acquisition-rcl-selection-matrix.md) | Appendix A | RCL and selection matrix method |
| [ch08](chapters/ch08-nasa-de-acquisition-drd-templates.md) | Appendix B | DRD template library and tailoring |

## Topic Index

- **Scope / guidance status / cited documents**: ch01
- **Digital Engineering Ecosystem / DE acquisition overview**: ch02
- **Lessons learned / data rights gaps / closeout risk**: ch03
- **Guiding principles / FAIR / minimum essential data**: ch04
- **Guiding questions / procurement planning method**: ch05
- **Contract language / SOW / DRD / cost volume / CDM**: ch06
- **RCL / selection matrix**: ch07
- **DRD templates / Data Type control / tailoring**: ch08
- **Interoperability / neutral formats / source-to-destination mapping**: ch06, ch02
- **Companion practitioner handbook pairing**: ch01, Version and jurisdiction

## Supporting Files

- `glossary.md` : terms and acronyms (absorbs section 3)
- `cheatsheet.md` : one-pass flow and placement map
- `patterns.md` : When / How / Trade-offs patterns
