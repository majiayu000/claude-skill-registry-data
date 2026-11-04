---
name: cisa-cpg
description: "Knowledge base from CISA Cross-Sector Cybersecurity Performance Goals 2.0. Use for prioritized IT/OT baseline cyber goals aligned to NIST CSF 2.0 (including GOVERN), critical-infrastructure hygiene, MSP/supply-chain expectations, and board-friendly outcome language. Covers CPG 2.0 goals only; does not replace full CSF programs, sector-specific goals (SSGs), or CSET tooling detail."
---

<!-- argument-hint: [topic, function, or chapter number] -->

# CISA Cross-Sector Cybersecurity Performance Goals (CPG) 2.0
**Source**: CISA CPG 2.0 (US Government work, public domain) | **Chapters**: 5

## When to use
Reach for this pack when selecting or assessing a prioritized baseline of cybersecurity practices for critical infrastructure IT and OT — especially to align investments to CISA’s highest-yield goals, map goals to CSF 2.0 Functions (including GOVERN), brief executives on foundational hygiene, or plan first-mile controls (identity, segmentation, backups, logging, IR readiness) before a full framework build-out.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about GOVERN/IDENTIFY/PROTECT/DETECT/RESPOND/RECOVER goals, IT vs OT implementation, prioritization, MFA, segmentation, MSP risk, or 2.0 changes.
- **With a chapter** — ask for `ch01` through `ch05`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### What CPGs are
A streamlined, outcome-driven baseline of cybersecurity protections for IT and OT environments across U.S. critical infrastructure. They help organizations pick high-impact practices, prioritize scarce resources, and communicate value to senior leaders.

### CSF 2.0 alignment
Goals are grouped under six Functions: GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER. Version 2.0 adds GOVERN and renumbers/consolidates prior goals; former OT-only items fold into universal goals for blended environments.

### Goal card pattern
Each goal states an **outcome** plus **recommended actions** — usable by practitioners and non-technical stakeholders.

### Representative goal map (2.0)
| Function | Example goals |
|----------|----------------|
| GOVERN | 1.A responsibilities; 1.C IR plans; 1.D supply-chain reporting; 1.E MSP risk |
| IDENTIFY | 2.A/B assets; 2.C/D independent validation; 2.E network topology |
| PROTECT | 3.A–3.S identity, MFA, segmentation, training, encryption, backups, logging, edge hardening |
| DETECT | 4.A malicious code detection; 4.B adverse events |
| RESPOND | 5.A communications; 5.B reporting |
| RECOVER | 6.A execute recovery plan |

### Using CPGs
- Floor, not ceiling: prioritized subset, not complete assurance.
- Remap any 1.x trackers before claiming 2.0 coverage.
- Pair short overview materials with the full report when implementing.
- Sector-specific goals may extend the cross-sector set.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-cpg-purpose-and-2-0-changes.md) | Purpose and 2.0 Changes | Why CPGs exist; GOVERN addition; consolidations |
| [ch02](chapters/ch02-govern-and-identify-goals.md) | GOVERN + IDENTIFY | Accountability, IR plans, MSP/supply chain, assets, topology |
| [ch03](chapters/ch03-protect-goals.md) | PROTECT | Identity, MFA, segmentation, backups, logging, edge security |
| [ch04](chapters/ch04-detect-respond-recover-goals.md) | DETECT/RESPOND/RECOVER | Malware/events, communications/reporting, recovery execution |
| [ch05](chapters/ch05-it-ot-implementation-and-prioritization.md) | IT/OT Implementation | Prioritization, OT constraints, investment framing |

## Topic Index
- **Adverse event identification** → ch04
- **Asset inventory** → ch02
- **Backups and restoration** → ch03, ch04
- **Board / executive communication** → ch01, ch05
- **Change management** → ch03
- **CPG 2.0 changes from 1.x** → ch01
- **Default passwords / credential hygiene** → ch03
- **Encryption** → ch03
- **GOVERN function** → ch01, ch02
- **Incident communications / reporting** → ch04
- **Incident response plans** → ch02, ch04
- **Independent control validation** → ch02
- **Internet-facing device security** → ch03
- **IT vs OT implementation** → ch05
- **Logging** → ch03
- **Malicious code detection** → ch04
- **Managed service provider (MSP) risk** → ch02
- **MFA** → ch03
- **Network segmentation** → ch03, ch05
- **Network topology documentation** → ch02
- **Prioritization / where to start** → ch01, ch05
- **Privileged vs user accounts** → ch03
- **Recovery plan execution** → ch04
- **Sector-specific goals (SSGs)** → ch05
- **Supply chain incident / vulnerability disclosure** → ch02
- **Training** → ch03

## Supporting Files
- [glossary.md](glossary.md) — CPG / CSF terms with chapter references
- [patterns.md](patterns.md) — implementation patterns (When/How/Trade-offs)
- [cheatsheet.md](cheatsheet.md) — decision rules, goal map, tells & smells

---

## Scope & Limits
This pack covers CISA Cross-Sector Cybersecurity Performance Goals Version 2.0 (report dated December 2025 in the extracted source; aligned to NIST CSF 2.0 including GOVERN) as synthesized reference notes. Combined source_pages = 38 (36-page main report + 2-page slick sheet overview). No separate CPG 2.0 “controls-list” PDF was available at build; the main report holds the full goal inventory. Does **not** cover: full NIST CSF 2.0 catalog; sector-specific goals in depth; CSET product UI; legal interpretation of NSM-5; or organization-specific compliance scoring. US Government public domain work. No source-material download link is published.
