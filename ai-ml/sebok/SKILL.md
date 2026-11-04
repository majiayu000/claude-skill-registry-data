---
name: sebok
description: "Knowledge base synthesized from the Guide to the Systems Engineering Body of Knowledge (SEBoK) v2.14 by the BKCASE Project. Use for the established systems-engineering canon: SE fundamentals and foundations (systems science, systems thinking, the systems approach, modelling/MBSE), the life cycle (ISO/IEC/IEEE 15288/24748/24774 process, development & agile approaches, model selection/tailoring), technical management, concept definition, architecture/realization (the Vee), V&V, maintenance/sustainment, SE standards, and the application contexts (product, service, enterprise, systems-of-systems, healthcare), plus enabling SE (business/team/individual), related disciplines, quality attributes/specialty engineering, implementation examples, and emerging knowledge. Good for grounding background, vocabulary, and prior-art positions across all eight SEBoK Parts. SCOPE LIMITS: this pack is SEBoK v2.14 only (released 2026-05-18); it synthesizes and signposts rather than reproducing the source — it does not reproduce ISO/IEC/IEEE standard text, is a curated guide (not a complete textbook), and is thin on AI-integration depth (Part 8 is a staging area, not settled practice). LICENCE: content is CC BY-NC-SA 3.0 — non-commercial use only, attribution to the BKCASE Project required, share-alike obligations carry forward."
---

<!-- argument-hint: [SE concept, life-cycle process, architecture/V&V, application context (product/service/enterprise/SoS/healthcare), standard, SEBoK Part, or chapter number] -->

# SEBoK — Guide to the Systems Engineering Body of Knowledge (v2.14)
**Source**: BKCASE Project, Trustees of the Stevens Institute of Technology | **Licence**: CC BY-NC-SA 3.0 (non-commercial) | **Chapters**: 36

## When to use
Use this skill when you need to reason about the established systems engineering canon as codified in SEBoK v2.14 (released 2026-05-18) by the BKCASE Project. This pack covers SE fundamentals and foundations (systems science, systems thinking, the systems approach, and MBSE), the full life cycle per ISO/IEC/IEEE 15288/24748/24774, technical management, concept definition, architecture and realization (the Vee), V&V, maintenance and sustainment, SE standards, and application contexts including product, service, enterprise, systems-of-systems, and healthcare. Reach for it when you need grounding in SE background, vocabulary, or prior-art positions across any of the eight SEBoK Parts.

**Prerequisites:** none, plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the Core Frameworks below: what the SEBoK is, the eight Parts, the foundations stack (systems science → systems thinking → systems approach), the life-cycle/process spine, and the application contexts.
- **With a topic** — ask about a concept (e.g. "emergence", "engineered system context"), a process (e.g. "architecture definition", "tailoring", "maintenance"), an application context (product/service/enterprise/SoS/healthcare), or a standard (15288, 24748, 24774).
- **With a SEBoK Part or chapter** — Part 1 → ch01; Foundations (Part 2) → ch02–ch07; SE & Management (Part 3) → ch08–ch19; Applications (Part 4) → ch20–ch25; Enabling SE (Part 5) → ch26–ch28; Related Disciplines (Part 6) → ch29–ch34; Examples (Part 7) → ch35; Emerging (Part 8) → ch36.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or runtime licence tier needed.

> **A guide, not the body of knowledge.** The SEBoK *curates, structures, and signposts* published SE knowledge — it discusses key ideas briefly and points to the references that treat them in depth. This pack mirrors that: synthesized reference notes, not a substitute for the primary sources or the standards themselves.

## Core Frameworks & Mental Models

### What the SEBoK is
A community-owned, semi-annually updated *guide to* the SE body of knowledge, organized into **eight Parts**. Its primary scope is the **engineered system (ES)** — a technical or socio-technical system that is the subject of an SE life cycle — viewed within its **engineered-system context** (the related engineered, social, and natural systems and environments). SE itself is defined (INCOSE 2023) as a transdisciplinary, integrative approach enabling the realization, use, and retirement of engineered systems. The economic case is empirical (COCOMO II rework data, COSYSMO, NASA overrun correlation), and "how much SE is enough" is a risk-balance between under- and over-investment.

### The eight Parts (the structural backbone)
1. **Introduction** · 2. **Foundations of SE** · 3. **SE and Management** · 4. **Applications of SE** · 5. **Enabling SE** · 6. **Related Disciplines** · 7. **Implementation Examples** · 8. **Emerging Knowledge**. Parts 2–6 are domain-independent; domain specificity enters via Part 7 examples and Part 4 domain KAs.

### Foundations stack (Part 2)
A layered scaffold from the general to the specific, and three grades of knowledge — **concept** (mental building block) → **principle** (a generalization usable for reasoning/action) → **heuristic** (works in practice; "why" not yet explained).
- **Systems science** — general principles and recurring patterns (isomorphies) common to systems of every kind (Bertalanffy, Boulding, Ashby, Beer, Forrester, Simon); the theoretical grounding.
- **Systems thinking** — the integrating paradigm: concepts, principles, patterns, balancing **holism** (the whole, because of emergence) against **reductionism** (the parts, because pure holism can't be acted on).
- **Representing systems with models / MBSE** — a model abstracts selected aspects (function, structure, behaviour, performance, cost); MBSE formalizes models across the life cycle and is a subset of digital engineering.
- **Systems approach applied to engineered systems** — a whole-system, whole-life-cycle, whole-stakeholder problem-solving framework (Hitchins' "Seven Samurai" of interacting systems; narrower vs. wider system-of-interest).

The two hardest properties — **complexity** and **emergence** — are precisely what create the need for systems thinking.

### Life-cycle & process spine (Part 3)
- **Life cycle** = the evolution of an entity from conception to retirement (24748-1); a **life cycle model** is a staged framework, selected and adapted per project, never inherited rigidly. A **stage** is bounded by milestones/**decision gates**; **technical reviews & audits** check state against criteria.
- **Development approaches**: sequential / incremental / evolutionary, with **agile** overlapping. **Agile in SE** = sense, respond, evolve across the whole life cycle ("being agile", per 24748-10), realized practically through Industrial DevOps.
- **Processes** are described uniformly (**24774**), selected from **15288**, and **tailored** with **24748-2** — applied with **concurrency, iteration, recursion**, not serially.
- **Technical Management (SEM)**: planning, assessment & control, decision management (trade studies, MODA), requirements management, risk, configuration, information, quality, measurement — distinguished from general project management by its technical focus.
- **Concept Definition** (problem space first): Business/Mission Analysis + Stakeholder Needs Definition → an integrated set of needs and Measures of Effectiveness, before System Definition.
- **Architecture → Realization → Deployment**: Architecture Definition sets functional/logical/physical views; realization runs down-and-up the **Vee** with **V&V performed concurrently and recursively** level by level.
- **Maintenance & sustainment**: planned from acquisition (15288 Cl. 6.4.1/6.4.9), run concurrently with operations; sustainment spans the long operational life (twelve product-support elements, LORA, RCM, life-cycle cost).
- **SE standards**: **ISO/IEC/IEEE 15288** is the trunk; take a full-life-cycle approach to any standard (evaluate → select → adapt → assess → improve).

### Application contexts (Part 4) — overlapping, not exclusive
- **Product SE** — end product *plus* enabling products; SE and market development run together (NPDP).
- **Service SE** — engineering a value co-creation chain with the customer as participant; services can't be inventoried.
- **Enterprise SE** — the enterprise viewed *as a system* where **people are components**, not just users.
- **Systems of Systems** — constituents are operationally and managerially independent (**Maier**); you **compose** via interfaces, you don't command.
- **Healthcare SE** — a domain extension layered over the others (devices ≈ Product SE; delivery ≈ Service SE; public health ≈ structural failure).

### Enabling, disciplines, attributes, examples, emerging (Parts 5–8)
- **Enabling SE** at three levels — business/enterprise (PDCA loop), team (capability + dynamics, IPTs, Tuckman), individual (roles + **KSAA** competency; competency ≠ performance).
- **Related disciplines** — SE's bounded overlaps with software engineering (neither a subset of the other), project management (no standard split; PMP/SEMP), industrial engineering, the physical/domain disciplines, environmental & geospatial engineering.
- **Quality attributes / specialty engineering** — the interdependent "-ilities"; engineer them together, and where they share a concern with **loss**, use a Loss-Driven view.
- **Implementation examples** — the evidence locker (GPS, Hubble vs. FBI VCF, Therac-25 …), each mapped back to the canon.
- **Emerging knowledge** — a staging area; the connective thread is transformation toward model-based, theory-grounded, AI-entangled SE (SE4AI / AI4SE).

---

## Chapter Index

| # | Part | Chapter | Key content |
|---|------|---------|-------------|
| [ch01](chapters/ch01-sebok-introduction.md) | 1 | SEBoK Introduction, Scope, Users | What the SEBoK is, eight Parts, SE definition, economic value, history, Digital Engineering, personas |
| [ch02](chapters/ch02-sebok-se-fundamentals.md) | 2 | SE Fundamentals | "What is a system?", the engineered-system context, four contexts, concept/principle/heuristic |
| [ch03](chapters/ch03-sebok-nature-of-systems.md) | 2 | The Nature of Systems | Systems across natural/social/engineered domains; fit-form-function; system classifications |
| [ch04](chapters/ch04-sebok-systems-science.md) | 2 | Systems Science | GST, cybernetics, requisite variety, isomorphies, dissipative structures, autopoiesis, panarchy |
| [ch05](chapters/ch05-sebok-systems-thinking.md) | 2 | Systems Thinking | Concepts/principles/patterns; holism vs. reductionism; the conceptagon; systems principles |
| [ch06](chapters/ch06-sebok-representing-systems-models.md) | 2 | Representing Systems with Models | What/why model; model types; MBSE; modelling languages and standards; views & viewpoints |
| [ch07](chapters/ch07-sebok-systems-approach-engineered.md) | 2 | Systems Approach to Engineered Systems | Hitchins' principles; Seven Samurai; narrower/wider SoI; hard vs. soft approach |
| [ch08](chapters/ch08-sebok-se-and-management-overview.md) | 3 | SE & Management — Overview | Part 3 framing; SE STEM overview; MBSE as the medium; document- vs. model-based |
| [ch09](chapters/ch09-sebok-life-cycle-terms-concepts.md) | 3 | Life Cycle Terms & Concepts | Life cycle, life cycle model, stage, decision gates, technical reviews & audits |
| [ch10](chapters/ch10-sebok-development-approaches.md) | 3 | Development Approaches | Sequential/incremental/evolutionary; Waterfall, Vee, Dual Vee; ICSM; DevOps; Lean SE |
| [ch11](chapters/ch11-sebok-agile-approaches.md) | 3 | Agile Approaches | Being agile vs. doing agile; eight strategic aspects; Industrial DevOps; 24748-10 |
| [ch12](chapters/ch12-sebok-life-cycle-model-selection.md) | 3 | Life Cycle Model Selection & Adaptation | Selecting/adapting model and approach; situation context; hump diagram; 24748-1 |
| [ch13](chapters/ch13-sebok-process-concepts.md) | 3 | Process Concepts | Uniform process description (24774); IPO; concurrency, iteration, recursion |
| [ch14](chapters/ch14-sebok-process-selection-tailoring.md) | 3 | Process Selection & Tailoring | Selecting from 15288; tailoring via 24748-2; rigor-balance; traceable decisions |
| [ch15](chapters/ch15-sebok-technical-management.md) | 3 | Technical Management Processes | SEM; SEMP/SEP; decision management (MODA, trade studies); risk, configuration, measurement |
| [ch16](chapters/ch16-sebok-system-concept-definition.md) | 3 | System Concept Definition | Business/Mission Analysis; Stakeholder Needs Definition; integrated needs; MOEs; green/brown-field |
| [ch17](chapters/ch17-sebok-system-architecture-realization.md) | 3 | Architecture, Realization & Deployment | Architecture Definition (functional/logical/physical); the Vee; V&V; ASoT; digital thread/twin |
| [ch18](chapters/ch18-sebok-system-maintenance.md) | 3 | System Maintenance | Maintenance concept/process; sustainment; LORA, RCM, LCC; twelve product-support elements |
| [ch19](chapters/ch19-sebok-se-standards.md) | 3 | SE Standards | 15288 as the trunk; full-life-cycle approach to a standard; SE standards taxonomy |
| [ch20](chapters/ch20-sebok-applications-overview.md) | 4 | Applications — Overview | The five contexts as overlapping frameworks; domain extension; real projects combine them |
| [ch21](chapters/ch21-sebok-product-systems-engineering.md) | 4 | Product Systems Engineering | Product system (end + enabling products); NPDP; IPDP stages; IPTs; EIA 632 |
| [ch22](chapters/ch22-sebok-service-systems-engineering.md) | 4 | Service Systems Engineering | Service systems; value co-creation; S-DL; SLA/SLM/QoS; ITIL; T-shaped professional |
| [ch23](chapters/ch23-sebok-enterprise-systems-engineering.md) | 4 | Enterprise Systems Engineering | Enterprise as a system; ESE vs. TSE; extended enterprise; enterprise architecture; opportunity |
| [ch24](chapters/ch24-sebok-systems-of-systems.md) | 4 | Systems of Systems | Maier's characteristics; constituent systems; directed/acknowledged/collaborative/virtual; Wave Model |
| [ch25](chapters/ch25-sebok-healthcare-systems-engineering.md) | 4 | Healthcare Systems Engineering | Medical devices; healthcare IT; design controls; ISO 13485/14971/62366; Lean Six Sigma |
| [ch26](chapters/ch26-sebok-enabling-businesses-enterprises.md) | 5 | Enabling Businesses & Enterprises | SE organizational strategy; capabilities; PDCA; barriers; culture; GQM; RACI |
| [ch27](chapters/ch27-sebok-enabling-teams.md) | 5 | Enabling Teams | Team capability & dynamics; IPTs; Tuckman stages; DEI; technical leadership |
| [ch28](chapters/ch28-sebok-enabling-individuals.md) | 5 | Enabling Individuals | Roles & KSAA competency; competency models; Bloom's taxonomy; ethics; competency ≠ performance |
| [ch29](chapters/ch29-sebok-related-disciplines-env-geo.md) | 6 | Environmental & Geospatial/Geodetic Engineering | Environmental Engineering (EIS, green design); GGE/PNT as a specialty discipline |
| [ch30](chapters/ch30-sebok-se-industrial-engineering.md) | 6 | SE & Industrial Engineering | SE vs. IE overlap; IISEBoK; roles across the life cycle; focus on system vs. process |
| [ch31](chapters/ch31-sebok-se-project-management.md) | 6 | SE & Project Management | PM vs. SE roles; no standard relationship; PMBOK; PMP & SEMP; project structure |
| [ch32](chapters/ch32-sebok-se-software-engineering.md) | 6 | SE & Software Engineering | SE/SwE intertwined, neither a subset; SWEBOK; aligned 15288/12207; cyber-physical systems |
| [ch33](chapters/ch33-sebok-se-physical-domain-disciplines.md) | 6 | SE & Physical/Domain Disciplines & Enterprise IT | ME/aerospace/EE/civil; Enterprise IT (EITBOK); seniority → systems engineering; IPTs |
| [ch34](chapters/ch34-sebok-se-quality-attributes.md) | 6 | SE & Quality Attributes | -ilities / specialty engineering; interdependence; Loss-Driven SE; HSI domains |
| [ch35](chapters/ch35-sebok-implementation-examples.md) | 7 | Implementation Examples | The evidence locker; Friedman-Sage; GPS/Hubble/FBI VCF; matrix of examples; OOSEM/ESEM |
| [ch36](chapters/ch36-sebok-emerging-knowledge.md) | 8 | Emerging Knowledge & Topics | Staging area; SE4AI/AI4SE; digital engineering; set-based design; ML life cycle; RE4AI |

## Topic Index

- **Agile approaches / being agile** → ch11, ch10
- **AI and systems engineering (SE4AI / AI4SE)** → ch36
- **Architecture definition (functional/logical/physical)** → ch17
- **Audits and technical reviews** → ch09
- **Authoritative source of truth / digital thread** → ch17, ch36
- **Business or mission analysis** → ch16
- **Competency (KSAA) and individuals** → ch28
- **Complexity and emergence** → ch04, ch02, ch34
- **Concept definition** → ch16
- **Concurrency, iteration, recursion** → ch13
- **Configuration management** → ch15
- **Cybernetics and requisite variety** → ch04
- **Decision management and trade studies** → ch15
- **Decision gates and stages** → ch09
- **Development approaches (sequential/incremental/evolutionary)** → ch10, ch12
- **Digital engineering** → ch36, ch01
- **Emergence** → ch04, ch02
- **Emerging knowledge and topics** → ch36
- **Enabling businesses and enterprises** → ch26
- **Enabling teams** → ch27, ch28
- **Engineered system and its context** → ch02, ch01, ch07
- **Enterprise architecture** → ch23, ch33
- **Enterprise systems engineering** → ch23
- **Environmental engineering** → ch29
- **Ethics in systems engineering** → ch28
- **Geospatial and geodetic engineering** → ch29
- **Healthcare systems engineering** → ch25
- **Heuristics, principles, concepts (grades of knowledge)** → ch02, ch05
- **History of systems engineering** → ch01
- **Holism and reductionism** → ch05
- **Human systems integration** → ch34
- **Implementation examples (case studies)** → ch35
- **Industrial engineering and SE** → ch30
- **Integrated product teams** → ch27, ch21, ch33
- **ISO/IEC/IEEE 15288 (life cycle processes)** → ch14, ch19, ch13
- **ISO/IEC/IEEE 24748 (life cycle management)** → ch12, ch11, ch14
- **ISO/IEC/IEEE 24774 (process description)** → ch13
- **Life cycle model selection and adaptation** → ch12
- **Life cycle terms and concepts** → ch09
- **Loss-driven systems engineering** → ch34
- **Maier's characteristics of systems of systems** → ch24, ch23
- **Maintenance and sustainment** → ch18
- **Measures of effectiveness (MOE)** → ch16
- **Model-based systems engineering (MBSE)** → ch06, ch08, ch36
- **Models, modelling and viewpoints** → ch06
- **Nature of systems** → ch03
- **New product development process (NPDP)** → ch21
- **Process concepts** → ch13
- **Process selection and tailoring** → ch14
- **Product systems engineering** → ch21
- **Project management and SE** → ch31
- **Quality attributes / specialty engineering / -ilities** → ch34
- **Realization, integration, transition** → ch17
- **Related disciplines (overview)** → ch29, ch30, ch33
- **Requirements management** → ch15
- **Risk management** → ch15
- **Service systems engineering** → ch22
- **Seven samurai of systems engineering** → ch07
- **Software engineering and SE** → ch32
- **Stakeholder needs definition** → ch16
- **Standards (SE) landscape** → ch19
- **Systems approach applied to engineered systems** → ch07
- **Systems engineering fundamentals** → ch02
- **Systems engineering management (SEM, SEMP)** → ch15, ch31
- **Systems engineering overview and introduction** → ch01
- **Systems of systems** → ch24
- **Systems science** → ch04
- **Systems thinking** → ch05
- **Tailoring (process)** → ch14
- **Technical management processes** → ch15
- **T-shaped professional** → ch22, ch01
- **Verification and validation (the Vee)** → ch17, ch10, ch32

## Supporting Files

- [glossary.md](glossary.md) — key SEBoK terms, alphabetical, with chapter references (synthesized definitions)
- [patterns.md](patterns.md) — ten reusable SE techniques (problem-first framing, context scoping, life-cycle/process selection, the Vee, sustainment, loss-driven attributes, SoS composition, enablement, SE/PM boundary) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — quick decision rules, the eight Parts, selection tables (development approaches, standards, application contexts), and tells & smells

---

## Scope & Limits

**Covers**: the established systems-engineering canon across all eight SEBoK Parts (v2.14) — foundations (systems science, systems thinking, the systems approach, modelling/MBSE); the life cycle and its processes (15288/24748/24774, development & agile approaches, model selection and tailoring); technical management; concept definition; architecture, realization, V&V (the Vee), and deployment; maintenance and sustainment; SE standards; the five application contexts (product, service, enterprise, systems-of-systems, healthcare); enabling SE at business/team/individual levels; related disciplines; quality attributes / specialty engineering; implementation examples; and emerging knowledge. Good for grounding background, vocabulary, and prior-art positions.

**Does not cover (or is thin on)**: it does **not reproduce** the ISO/IEC/IEEE standard text it references (15288, 12207, 24748, 24774 are named and described, not quoted — see `se-standards-signpost`); it is a **curated guide**, not a complete textbook, and signposts primary sources rather than replacing them; AI-integration depth is limited (Part 8 / ch36 is an emerging-topics staging area, not settled practice — for AI governance use `nist-ai-rmf` / `eu-ai-act`); and detailed security engineering, test & evaluation, and digital-engineering implementation live in companion packs (`nist-sse`, `dod-te-guidebook`/`faa-ams-vv`, `dod-digital-engineering`/`digital-systems-engineering`).

**Source version**: SEBoK **v2.14**, released 2026-05-18 (supersedes the prior v2.13 build). One chapter per SEBoK Knowledge Area or tightly-coherent KA group.

**Licence & attribution**: the SEBoK is published under **Creative Commons Attribution-NonCommercial-ShareAlike 3.0 (CC BY-NC-SA 3.0)**, so this pack's content carries the same licence — **non-commercial use only**, **attribution to the BKCASE Project (Trustees of the Stevens Institute of Technology) required**, and **share-alike**: derivatives must be distributed under the same licence. This overrides the repository's MIT licence for this pack's content. See `LICENSE` and `docs/LICENSING.md`.
