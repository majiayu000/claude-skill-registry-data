---
name: mil-std-40051
description: "Knowledge base from MIL-STD-40051E w/Change 1, 30 July 2025, Preparation of Digital Technical Information for Technical Manuals. One volume covers page-based and electronic manuals (IETM and ETM). Use for scope, applicable-document classes, general and detailed requirements, content-selection method, operator/maintenance/parts families, special TM types (destruction, BDAR, PMC, LO, ammunition, software, hand receipts, data sheets, TBs), and change/revision control. Does not copy matrix cells, plate exemplars, or sample pages."
---

<!-- argument-hint: [TM, IETM, ETM, work package, content selection, change package, DMWR, BDAR, PMC, or a chapter number] -->

# Preparation of Digital Technical Information for Technical Manuals (MIL-STD-40051E)

**Source:** Public domain US Government work (17 U.S.C. 105); Distribution A; no printed DOPSR case. See `LICENSE`. Pin: MIL-STD-40051E w/Change 1, 30 July 2025.

## When to use

Use this skill when authoring, tailoring, reviewing, or training on military technical manuals under the consolidated E Change 1 practice: page-based and electronic outputs, work-package structure, content selection, core and special TM types, and change control.

**Prerequisites:** none. Plain Markdown. No MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill

- **Without arguments** - load the one-volume spine, WP model, and matrix-first tailoring below.
- **With a topic question** - ask about IETM/ETM rules, work packages, content selection, operator/maintenance/parts families, special types, or change packages.
- **With a manual-type question** - ask for a TM type (operator, troubleshooting, maintenance, parts, BDAR, PMC, LO, software, hand receipt, TB) and follow the matching chapter.

## Core Frameworks & Mental Models

### One volume, two outputs

E Change 1 is a single standard practice for page-based and electronic manuals. IETM and ETM name output-specific rules. Unqualified requirements apply to both.

### Matrix then author

Appendix A content selection (with MATDEV) decides which objects a TM carries. Sections 4 and 5 supply structure and detailed method. Appendices B-Q specialize by family.

### Work package atom

Narrative and task content divides into WPs with stable identifiers. Prefer WP citations over fragile page numbers.

### Safety and change layers

Warning summary plus step-adjacent WARNING/CAUTION/NOTE (and HAZMAT). Change packages and revisions keep effectivity visible, including list-of-effective pages/WPs for electronic deliveries.

## Chapter Index

| File | Job |
| --- | --- |
| [ch01-mil-std-40051-scope.md](chapters/ch01-mil-std-40051-scope.md) | Scope, applicability, consolidation |
| [ch02-mil-std-40051-applicable-documents.md](chapters/ch02-mil-std-40051-applicable-documents.md) | Applicable-document classes |
| [ch03-mil-std-40051-general-requirements.md](chapters/ch03-mil-std-40051-general-requirements.md) | General requirements, IETM, WPs |
| [ch04-mil-std-40051-detailed-requirements.md](chapters/ch04-mil-std-40051-detailed-requirements.md) | Detailed preparation method |
| [ch05-mil-std-40051-content-selection.md](chapters/ch05-mil-std-40051-content-selection.md) | Content-selection method |
| [ch06-mil-std-40051-operator-maintenance-parts.md](chapters/ch06-mil-std-40051-operator-maintenance-parts.md) | Operator, maintenance, parts families |
| [ch07-mil-std-40051-special-tm-types.md](chapters/ch07-mil-std-40051-special-tm-types.md) | Special TM types H-Q |
| [ch08-mil-std-40051-changes-notes.md](chapters/ch08-mil-std-40051-changes-notes.md) | Changes, revisions, notes |

## Topic Index

- Scope / consolidation / service prefixes: ch01
- Applicable documents / order of precedence: ch02
- IETM functionality / work packages / style spine: ch03
- Front matter / notices / detailed method: ch04
- Content selection matrix / tailoring: ch05
- Operator / troubleshooting / maintenance / parts / supporting info: ch06
- Destruction / BDAR / PMC / LO / ammunition / software / hand receipts / TBs: ch07
- Change packages / revisions / acquisition notes: ch08

## Supporting Files

- `glossary.md`
- `cheatsheet.md`
- `patterns.md`

## Scope & Limits

One-volume E Change 1 practice for page-based and electronic manuals. Does not copy content-selection matrix cells, plate exemplars, or sample pages. Does not quote cited military standards or statutes. Does not limit the pack identity to paper delivery.
