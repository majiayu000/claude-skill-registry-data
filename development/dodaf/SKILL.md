---
name: dodaf
description: "Knowledge base from DoD Architecture Framework (DoDAF) 2.02 — Volume II: Architectural Data and Models. Use for DoDAF viewpoints, DM2 meta-model, capability modeling, operational architecture, systems architecture, services architecture, data/information modeling, standards compliance, project/portfolio integration, and fit-for-purpose model selection. Does not cover DoDAF Volume I (policy/governance) or Volume III (enterprise-level guidance); also does not substitute for the live DISR or DARS registries."
---
<!-- argument-hint: [viewpoint name, model code (e.g. OV-5b, CV-1), data group, chapter number, or topic] -->
# DoD Architecture Framework (DoDAF) 2.02 — Volume II: Architectural Data and Models
**Source**: US Department of Defense (public domain, Distribution A — approved for public release) | **Chapters**: 11

## When to use
Use this skill when designing, reviewing, or querying DoDAF architectural descriptions, viewpoint models, or the DoDAF Meta-Model (DM2). It is the reference for any question about which DoDAF model to produce for a given decision-maker need, how to correctly structure DM2 data, how performers-activities-resources interrelate, or how DoDAF integrates with DoD acquisition and portfolio processes (JCIDS, DAS, PPBE, SE, OPS, CPM). Use it when selecting models, building traceability chains, specifying interfaces, or aligning architecture with standards.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks: viewpoint summary table, DM2 data groups, and the performer-activity-resource triad.
- **With a topic** — ask about capability modeling, operational architecture, service-oriented design, data models, standards compliance, project integration, DOTMLPF analysis, fit-for-purpose selection.
- **With a model code** — ask for `CV-1`, `OV-5b`, `SV-1`, `DIV-2`, `PV-3`, `StdV-1`, `SvcV-4`, etc.
- **With a chapter** — ask for `ch04` (Capability VP), `ch06` (Operational VP), `ch10` (Systems VP), etc.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### The DoDAF Meta-Model (DM2)
The DM2 is the formal ontology (based on the IDEAS Foundation) that provides standard types, relationships, and glossary terms for all DoDAF work. It is implemented in Sparx Enterprise Architect with the IDEAS add-in. All DoDAF viewpoint models are presentations over DM2 data — produce the data once in the shared data store, then present it through whichever viewpoint models serve the identified decisions.

**Fundamental principle — Fit-for-Purpose:** DoDAF does not require architects to produce all models. Models are selected based on identified decision-maker needs. AV-1 and AV-2 are required for every architecture (DARS registration). All other models are optional — justified by the decisions they support.

### The Performer-Activity-Resource Triad
The invariant kernel of every DoDAF model:
- **Performer** (who) — person in role, organization, system, or service that performs an activity.
- **Activity** (what) — transformation that consumes resources to produce resources.
- **Resource** (with what / to what) — information, materiel, or performer produced or consumed.
- **Resource Flow Triple** — the atomic interoperability unit: (producing activity) → (resource) → (consuming activity). All resource exchanges must be expressed as this triple; direct performer-to-performer transfers are not modeled.

Rules constrain Activities (never Performers directly). Performers are affected by rules only through the activities they perform.

### Eight DoDAF Viewpoints

**All Viewpoint (AV)** — AV-1 Executive Summary (architecture overview, DARS registration) and AV-2 Integrated Dictionary (vocabulary grounded in seven genus terms: activity, resource, project, location, guidance, vision, property).

**Capability Viewpoint (CV)** — Seven models for capability portfolio managers. Core concept: desired resource state (effect) achieved by activities under conditions using rules and resources. CV-1 (effects/measures) → CV-2 (hierarchy) → CV-3 (schedules) → CV-4 (dependencies) → CV-5 (deployments) → CV-6 (activities) → CV-7 (services). DOTMLPF analysis is grounded here.

**Data & Information Viewpoint (DIV)** — Three-level stack addressing the same enterprise information at increasing concreteness: DIV-1 (conceptual — what must be understood), DIV-2 (logical — what data is required), DIV-3 (physical — how data is stored/exchanged). DIV-3 must satisfy every DIV-2 requirement; may not introduce new concepts.

**Operational Viewpoint (OV)** — Nine models describing who needs to do what, technology-independent. Systems/services appear only as constraints. OV-5b is the authoritative operational activity model; OV-5a is its strict subset. OV-6a/6b/6c add rules, state transitions, and sequences.

**Project Viewpoint (PV)** — Three models integrating architecture with DAS and PPBE. PV-1 (organizations-to-projects, WBS), PV-2 (schedules, Gantt, milestones, happens-in to fiscal years), PV-3 (projects-to-capabilities). PV-1 existence predicate: every modeled project must produce guidance or resources traceable to other viewpoint models.

**Services Viewpoint (SvcV)** — Twelve models for service-oriented architectures. SvcV-1 is foundational; all others derive from it. Services are performers with self-describing ServiceDescription elements. Includes non-IT services. SvcV-5 maps to OV-5b operational activities.

**Standards Viewpoint (StdV)** — Two models: StdV-1 (current standards profile, DISR-required for IT) and StdV-2 (standards succession forecast). Standards bind to Activities, not Performers. Conditions may scope when a standard applies to an activity.

**Systems Viewpoint (SV)** — Twelve models for systems engineers. SV-1 is foundational (system inventory, interfaces); SV-4 for functional decomposition; SV-5a for OV traceability; SV-5b for capability contribution; SV-8/SV-9 for evolution planning; SV-10a/10b/10c for behavioral specification. Services may not appear in SV-1/SV-4 as primary performers.

### Eleven DM2 Data Groups

**Principle (8):** Performers, Resource Flows, Information & Data, Rules, Capabilities, Services, Projects, Organizational Structures.

**Supporting (3):** Measures (magnitude of attributes), Locations (spatial extents), Pedigrees (origin/history of resources).

Key cross-mapping: all 8 viewpoints draw on some subset of these 11 groups; the exact mapping is in Table 3.3-1 of the source document.

### Key Architecture Integration Points
- **CV↔PV integration via PV-3:** capabilities (CV) are delivered by projects (PV-3); this is the PPBE-to-operational-need link.
- **OV↔SV integration via SV-5a:** operational activities (OV-5b) are supported by system functions (SV-4); traced in SV-5a.
- **OV↔SvcV integration via SvcV-5:** operational activities (OV-5b) are supported by service functions; traced in SvcV-5.
- **StdV↔DIV integration:** DIV-3 data implementations must comply with StdV-1 metadata standards.
- **SV/SvcV↔StdV integration via StdV-2+SV-8:** standards succession timelines drive system evolution planning.

## Chapter Index

| # | File | Key content |
|---|------|-------------|
| 1 | [ch01-introduction-and-dodaf-concepts.md](chapters/ch01-introduction-and-dodaf-concepts.md) | DoDAF purpose, fit-for-purpose principle, IDEAS Foundation, DM2 overview, six DoD core processes |
| 2 | [ch02-dm2-data-groups-overview.md](chapters/ch02-dm2-data-groups-overview.md) | All 11 data groups defined, process-to-viewpoint mapping table, performer-activity-resource triad |
| 3 | [ch03-all-viewpoint-av.md](chapters/ch03-all-viewpoint-av.md) | AV-1 Executive Summary, AV-2 Integrated Dictionary, DARS registration, genus-differentia definitions |
| 4 | [ch04-capability-viewpoint-cv.md](chapters/ch04-capability-viewpoint-cv.md) | CV-1 through CV-7, desired effects, measures of effect/desire, DOTMLPF analysis, capability configurations |
| 5 | [ch05-data-information-viewpoint-div.md](chapters/ch05-data-information-viewpoint-div.md) | DIV-1/2/3 three-level stack, conceptual/logical/physical abstraction, mesodata/metadata/microdata |
| 6 | [ch06-operational-viewpoint-ov.md](chapters/ch06-operational-viewpoint-ov.md) | OV-1 through OV-6c, technology-independent operational modeling, OV-5a/5b relationship, mission threads |
| 7 | [ch07-project-viewpoint-pv.md](chapters/ch07-project-viewpoint-pv.md) | PV-1/2/3, WBS, program elements, PPBE integration, DAS milestone linkage, happensIn fiscal years |
| 8 | [ch08-services-viewpoint-svcv.md](chapters/ch08-services-viewpoint-svcv.md) | SvcV-1 through SvcV-10c, service descriptions, business vs. enabling services, SOA traceability |
| 9 | [ch09-standards-viewpoint-stdv.md](chapters/ch09-standards-viewpoint-stdv.md) | StdV-1 current profile, StdV-2 forecast, DISR requirement, standards-to-activity binding |
| 10 | [ch10-systems-viewpoint-sv.md](chapters/ch10-systems-viewpoint-sv.md) | SV-1 through SV-10c, system composition, SV-5a traceability, SV-8/9 evolution, behavioral spec |
| 11 | [ch11-dm2-data-groups-detail.md](chapters/ch11-dm2-data-groups-detail.md) | Deep reference for all 8 principle data groups, assignment vs. allocation, resource flow triple mechanics |

## Topic Index
- **Capability modeling** → ch04
- **Capability-to-project traceability** → ch04, ch07
- **Configuration items (CI/CSCI)** → ch11
- **DARS registration** → ch03
- **Data modeling (conceptual/logical/physical)** → ch05
- **DISR compliance** → ch09
- **DM2 meta-model** → ch01, ch02, ch11
- **DOTMLPF analysis** → ch04, ch11
- **Earned value management** → ch07
- **Fit-for-purpose model selection** → ch01, ch02
- **IDEAS Foundation** → ch01, ch11
- **Information modeling** → ch05
- **Interface identification** → ch10, ch08
- **JCIDS** → ch04, ch11
- **Measures (MoE, MoD, QoS)** → ch02, ch04, ch10
- **Mission threads** → ch06
- **Operational architecture** → ch06
- **Organizational relationships** → ch06, ch11
- **Portfolio management** → ch04, ch07
- **PPBE integration** → ch07
- **Project scheduling** → ch07
- **Publish-subscribe** → ch11
- **Resource flow triple** → ch02, ch11
- **Service-oriented architecture** → ch08
- **Services (non-IT)** → ch08
- **Standards compliance** → ch09
- **System functions** → ch10
- **Systems engineering** → ch10, ch11
- **Traceability (OV to SV)** → ch10
- **Viewpoint selection** → ch01, ch02
- **WBS** → ch07
- **Vocabulary / terminology** → ch03

## Supporting Files
- [glossary.md](glossary.md) — ~60 defined terms from the DM2 and DoDAF viewpoints, with precise definitions grounded in the source document
- [patterns.md](patterns.md) — 13 When/How/Trade-offs patterns covering fit-for-purpose selection, interface management, DOTMLPF analysis, capability traceability, and standards transition planning
- [cheatsheet.md](cheatsheet.md) — Quick-reference tables (viewpoints, data groups, process mapping, model derivation rules, DM2 relationships), decision rules, and tells-and-smells diagnostic guide

---
## Scope & Limits
This knowledge pack covers DoDAF 2.02 Volume II (Architectural Data and Models) only: the DM2 ontology, eight viewpoints with their models, eleven data groups, and their integration with DoD acquisition and portfolio processes. It does **not** cover DoDAF Volume I (policy, governance, and the six-step architecture development process), Volume III (enterprise-level architecture guidance), the live DISR or DARS registries, or DoDAF-aligned tools (Sparx EA, IBM Rational, etc.). The source document is US Department of Defense (public domain, Distribution A — approved for public release, Chg 1, 31 January 2015); redistribution and synthesis are permitted.
