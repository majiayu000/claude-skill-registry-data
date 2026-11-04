---
name: doe-sem
description: "Knowledge base from DOE Systems Engineering Methodology (SEM) Version 3 — the DOE SDLC for IT investments. Use for staged systems lifecycle planning through maintenance, Stage Exits, Structured Walkthroughs, In-Stage Assessments, requirements traceability, and CMM-aligned process discipline. Covers SEM3 (2002) guidance only; does not replace modern DevSecOps tooling standards, DOE O 413.3B capital-asset directives, or current CIO policy supersessions."
---

<!-- argument-hint: [topic, stage, or chapter number] -->

# DOE Systems Engineering Methodology (SEM) Version 3
**Source**: DOE SEM3 / DOE G 200.1-1A (US Government work, public domain) | **Chapters**: 7

## When to use
Reach for this pack when planning or assessing a DOE-style systems development lifecycle for IT investments — especially stage gates (Stage Exits), peer Structured Walkthroughs, independent In-Stage Assessments, planning/QA/CM plan triad, requirements traceability, construction vs design boundaries, acceptance, or the nested maintenance process model.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about lifecycle stages, Stage Exit, walkthroughs, planning, requirements, design, construction, test/acceptance, or maintenance.
- **With a chapter** — ask for `ch01` through `ch07`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### What SEM is
DOE’s Systems Development Lifecycle guidance for IT investments (Office of the CIO). Version 3 renames software-centric SEM to systems engineering for IT projects and aligns practices with SEI CMM-SW Level 2/3 process areas.

### Eight lifecycle stages
1. Planning  
2. Requirements Definition  
3. Functional Design  
4. System Design  
5. Construction (formerly Programming)  
6. Integration and Testing  
7. Installation and Acceptance  
8. Maintenance (nested change lifecycle)

### Quality machinery (every development stage)
| Mechanism | Role |
|-----------|------|
| Structured Walkthrough | Peer technical review of work products |
| In-Stage Assessment | Independent QA review of stage deliverables |
| Stage Exit | Owner/stakeholder go / continue / abandon decision |

### Planning triad
Project Plan + Quality Assurance Plan + Configuration Management Plan baseline how the project will be managed, assured, and controlled.

### Traceability
Requirements Traceability Matrix links needs → requirements → design → test → acceptance evidence.

### Modern use note
Source date is September 2002. Keep stage intents, gates, and CM/QA discipline; modernize tools (cloud, CI/CD, agile increments) without dropping exits and baselining.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-sem-purpose-and-context.md) | Purpose and Context | SEM scope, v3 changes, CMM alignment, DOE CIO context |
| [ch02](chapters/ch02-lifecycle-model-and-quality-reviews.md) | Lifecycle Model & Quality Reviews | Eight stages; walkthroughs; assessments; Stage Exits; tailoring |
| [ch03](chapters/ch03-planning-stage.md) | Planning Stage | Feasibility, plans triad, risk, EA, performance measures |
| [ch04](chapters/ch04-requirements-and-functional-design.md) | Requirements & Functional Design | RTM, baselines, logical design |
| [ch05](chapters/ch05-system-design-and-construction.md) | System Design & Construction | Physical design, build, unit verification, CM |
| [ch06](chapters/ch06-integration-test-and-acceptance.md) | Integration Test & Acceptance | System test, install, owner acceptance, training |
| [ch07](chapters/ch07-maintenance-stage.md) | Maintenance | Nested change process model and metrics |

## Topic Index
- **Acceptance / owner decision** → ch06
- **CMM-SW alignment** → ch01, ch02
- **Configuration management plan** → ch03, ch05, ch07
- **Construction stage** → ch05
- **COTS considerations** → ch05, ch07
- **Enterprise Architecture (DOE EA)** → ch03
- **Feasibility analysis** → ch03
- **Functional design** → ch04
- **In-Stage Assessment** → ch02
- **Installation** → ch06
- **Integration and testing** → ch06
- **Lifecycle stages overview** → ch02
- **Maintenance process model** → ch07
- **Performance measures** → ch03, ch06
- **Planning stage** → ch03
- **Project plan** → ch03
- **Quality assurance plan** → ch03
- **Requirements definition** → ch04
- **Requirements traceability matrix (RTM)** → ch04, ch06
- **Risk management** → ch03
- **Stage Exit** → ch02, ch06
- **Structured Walkthrough** → ch02
- **System design** → ch05
- **System owner / users** → ch03, ch06
- **Tailoring by project size** → ch02, ch07

## Supporting Files
- [glossary.md](glossary.md) — SEM lifecycle terms with chapter references
- [patterns.md](patterns.md) — implementation patterns (When/How/Trade-offs)
- [cheatsheet.md](cheatsheet.md) — decision rules, stage map, tells & smells

---

## Scope & Limits
This pack covers DOE Systems Engineering Methodology Version 3 (SEM3_1231.pdf, September 2002, DOE G 200.1-1A) — the DOE SDLC for IT investments — as synthesized reference notes. Extracted page count recorded in PACK.yaml is **318**. It does **not** cover: current superseding DOE CIO directives if any; DOE O 413.3B capital asset project management in full; agile/DevSecOps toolchains as mandates; or non-IT nuclear/facility systems engineering methods. US Government public domain work. No source-material download link is published. In-PDF third-party copyright check at build found no copyright notices (IEEE/SEI are citations only).
