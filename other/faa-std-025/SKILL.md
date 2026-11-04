---
name: faa-std-025
description: "Knowledge base from FAA-STD-025f (Preparation of Interface Documentation). Use for IRD/ICD family definitions, common format and content, IRD shall-requirements, ICD design characteristics, verification/VRTM, and CM/revision/approval of FAA Enterprise Subsystem interfaces. Covers rev F preparation rules only; does not replace FAA-STD-005 drawing/spec prep, Order 1800.66 full CM procedures, or non-FAA interface standards."
---

<!-- argument-hint: [topic, document type, or chapter number] -->

# FAA-STD-025f — Preparation of Interface Documentation
**Source**: FAA-STD-025f (US Government work, public domain) | **Chapters**: 6

## When to use
Reach for this pack when authoring or reviewing **Interface Requirements Documents (IRD)** or **Interface Control Documents (ICD)** for FAA Enterprise Subsystems / NAS interfaces — including choosing IRD vs ICD, filling required outlines, specifying security/physical/power interface shalls, building a VRTM, or routing revisions under configuration management.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about IRD vs ICD, TBS, facility IRDs, VRTM, security shalls, power factors, or approval roles.
- **With a chapter** — ask for `ch01` through `ch06`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### IRD / ICD pair
| Artifact | Answers | Verb | Baseline role |
|----------|---------|------|---------------|
| IRD | What must the interface satisfy? | shall | FAA-controlled requirements baseline |
| ICD | How is it implemented / as-built? | is/are | Developer deliverable design record |

Facility interfaces: IRD only (no ICD). Orphan ICDs (no parent IRD) must carry both shall and is/are — discouraged.

### Interface-type outlines
Use the standard decision tree, then the matching TOC:
- Facility / analog / discrete family
- General service / web service family

Shared rules: front matter, explicit N/A, incorporation by reference, TBS only where allowed.

### Common technical spine
1. Scope template + responsibility lists
2. Referenced documents (versioned, accessible, tailored)
3. Functions / demarcation / security / physical / power
4. Type-specific protocol or facility slots
5. Verification responsibility + VRTM (1:1 with shalls)

### Verification levels
Subsystem/Service (Development) → Integration → Site. SEM T&E guidance tailored into the VRTM; special conformance/interoperability for ATN/IPS.

### CM and timing
- Start IRD early; before SOW finalization when used in procurement.
- Approve IRD before ICD when both required.
- Revise by superseding full document under FAA Order 1800.66 (no legacy side "Interface Revision" form).
- Facility IRD maturity: Initial → Primary → Intermediate → Final.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-scope-and-document-family.md) | Scope and Document Family | FESS applicability, IRD vs ICD, TBS, baselining |
| [ch02](chapters/ch02-general-format-and-common-content.md) | General Format and Common Content | Outlines, front matter, scope templates, references |
| [ch03](chapters/ch03-ird-content-requirements.md) | IRD Content Requirements | Functional/security/physical/power and typed IRDs |
| [ch04](chapters/ch04-icd-content-requirements.md) | ICD Content Requirements | Design characteristics, as-built, orphan ICD rule |
| [ch05](chapters/ch05-verification-and-traceability.md) | Verification and Traceability | VRTM, levels, methods, ATN/IPS special tests |
| [ch06](chapters/ch06-revisions-cm-and-approval.md) | Revisions, CM, and Approval | 1800.66 revisions, roles, facility iterations |

## Topic Index
- **Analog / discrete interfaces** → ch01, ch03, ch04
- **Application process / protocols** → ch03, ch04
- **As-built / form-fit-function** → ch01, ch04
- **Configuration Management / Order 1800.66** → ch02, ch06
- **Demarcation point** → ch03
- **Facility IRD (no ICD)** → ch01, ch03, ch06
- **Front matter / TOC outlines** → ch02
- **Interface Control Document (ICD)** → ch01, ch04
- **Interface Management** → ch01, ch06
- **Interface Requirements Document (IRD)** → ch01, ch03
- **Interface Working Group roles** → ch06
- **N/A and TBS language** → ch01, ch02
- **Power / connectors / grounding / EMC** → ch03, ch04
- **Requirements Traceability / VRTM** → ch05
- **Security requirements at interfaces** → ch03, ch04
- **Service / web service interfaces** → ch03, ch04
- **Verification levels (dev/integration/site)** → ch05
- **Verb discipline (shall vs is/are)** → ch01, ch04

## Supporting Files
- [glossary.md](glossary.md) — IRD/ICD and interface terms
- [patterns.md](patterns.md) — implementation patterns with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, maps, tells & smells

---

## Scope & Limits
This pack covers **FAA-STD-025f (November 30, 2007)** — Preparation of Interface Documentation — as synthesized reference notes from the everyspec mirror of Rev F (64 pages per extraction metadata). It does **not** cover: full text of FAA-STD-005 / FAA-STD-002 / FAA-G-2100; the complete FAA Order 1800.66 CM procedure set; non-FAA interface control standards (e.g., generic MIL ICD practices beyond this FAA standard); or program-specific IRD/ICD instances. US Government public domain work. No source-material download link is published.
