---
name: is-gps-200n
description: "Knowledge base from IS-GPS-200 Rev N (NAVSTAR GPS Space Segment / Navigation User Segment Interfaces). Use as a worked ICD/IS exemplar: what an interface specification is, DIST-A and IRN/CCB change control, interface definition vs identification, composite-signal criteria patterns, NAV data as payload families, and time/definition hygiene. Covers Rev N synthesized notes only; does not transcribe Apps II–IV bit fields or PRN/Gold-code tables, and does not replace faa-std-025 preparation rules."
---

<!-- argument-hint: [topic, ICD pattern, or chapter number] -->

# NAVSTAR GPS Space Segment / Navigation User Segment Interfaces (IS-GPS-200N)
**Source**: IS-GPS-200 Rev N (cover 01-AUG-2022) (US Government work, public domain, DIST-A) | **Chapters**: 6

## When to use
Reach for this pack when you need a **worked Interface Specification / ICD** — how a live IS defines RF links, identifies codes and NAV payload, writes interface-criteria shalls, and keeps time/definition hygiene — complementary to `faa-std-025` (how to *prepare* an IRD/ICD, not a live ICD).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about ICD-as-contract, IRN/CCB, L1/L2 criteria, LNAV vs CNAV families, URA/CEI, or which appendix to open.
- **With a chapter** — ask for `ch01` through `ch06`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### Document-as-contract
An IS states the Space Segment / User Segment interface. It does not alter contracts or purchase orders (cover notice). Users implement against numbered shalls; exceptions live in Appendix I letters, not in silent receiver folklore.

### Definition → identification → criteria
1. **Definition (3.1)** — what the interface *is* (L1 and L2 RF links carrying ranging codes + NAV data to a user with RF visibility).
2. **Identification (3.2)** — which codes and data families exist, and that they are CDMA-separated.
3. **Criteria (3.3)** — measurable shalls (frequency plan, levels, phasing, polarization, time).

### Change / IRN discipline
ICC prepares PIRNs; ICWG has 45 days; GPS Directorate CCB (with DOT representing civil/public interest) makes the IS effective. Rev N incorporates IRN-IS-200M-001 (RFC-467). Distribution status changed to Public Release on an earlier revision.

### Payload vs bits
Body text names LNAV D(t) and CNAV DC(t) *families*. Bit layouts, FEC polynomials, and PRN tables live in Apps II–IV — open those only when implementing a decoder, not when learning ICD structure.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-is-scope-and-change-control.md) | IS Scope and Change Control | What an IS/ICD is; DIST-A; ICC/ICWG/CCB/IRN |
| [ch02](chapters/ch02-interface-definition-and-identification.md) | Definition vs Identification | L1/L2 contract; code families; document-as-contract |
| [ch03](chapters/ch03-interface-criteria-pattern.md) | Interface Criteria Pattern | Frequency, levels, phasing, polarization as shalls |
| [ch04](chapters/ch04-nav-data-as-payload.md) | NAV Data as Interface Payload | LNAV/CNAV families, not bit fields |
| [ch05](chapters/ch05-time-and-definition-hygiene.md) | Time and Definition Hygiene | GPS time / Z-count; URA; CEI; reserved/invalid |
| [ch06](chapters/ch06-appendices-as-a-map.md) | Appendices as a Map | When to open App I–IV; do not dump payloads |

## Topic Index
- **CCB / PIRN / IRN** → ch01
- **CEI data set** → ch05
- **Change / IRN** → ch01
- **CM (configuration of the IS)** → ch01
- **CNAV / LNAV families** → ch04, ch06
- **DIST-A / public release** → ch01
- **ICD / IS** → ch01, ch02
- **Interface criteria (RF pattern)** → ch03
- **Interface definition vs identification** → ch02
- **Interface Management** → ch01, ch02
- **PRN / ranging codes (as identifiers)** → ch02, ch06
- **Requirements Traceability** → ch02, ch03
- **Reserved / invalid / dummy SV** → ch05
- **URA** → ch05
- **Z-count / GPS time** → ch05

## Supporting Files
- [glossary.md](glossary.md) — IS/ICD and GPS interface terms
- [patterns.md](patterns.md) — ICD authoring patterns with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — structure map, tells and smells

---

## Scope & Limits
This pack covers **IS-GPS-200 Rev N** (cover date 01-AUG-2022; public-release revision record) as synthesized reference notes from the official gps.gov PDF (248 pages per extraction metadata). It is an **ICD exemplar**, not a signal-processing dump: Apps II–IV bit fields, PRN/Gold-code tables, and FEC polynomials are **not transcribed**. It complements **`faa-std-025`**, which teaches IRD/ICD *preparation* rules (outlines, VRTM, FAA CM) and is not itself a live ICD — same slug-distinction pattern as dote vs dod-te-guidebook. It does **not** ingest IS-GPS-705J, IS-GPS-800J, ICD-GPS-153, or a non-existent IS-300. US Government public domain work (DIST-A). No source-material download link is published.
