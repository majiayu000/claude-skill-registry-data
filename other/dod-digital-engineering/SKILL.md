---
name: dod-digital-engineering
description: "Knowledge base from the DoD Digital Engineering Strategy (2018, OUSD/ODASD(SE)). Use for the Department of Defense's five digital engineering goals — (1) formalize the development, integration, and use of models; (2) provide an enduring authoritative source of truth; (3) incorporate technological innovation; (4) establish supporting infrastructure and environments; (5) transform the culture and workforce — plus their focus areas, the document-to-model and design-build-test→model-analyze-build shifts, model formalisms/provenance, governance and access control of the authoritative source of truth, and the coordinate→plan→pilot→sustain rollout. A vision-and-policy strategy, deliberately non-prescriptive. Does NOT provide a how-to method, tool tutorials, MBSE/SysML mechanics, or implementation-plan content; thin on metrics, acquisition-policy detail, and step-by-step procedure. Excludes the CAC-gated Digital Engineering Body of Knowledge (DEBoK)."
---

<!-- argument-hint: [digital engineering goal (1-5), focus area, authoritative source of truth, model formalisms, governance, infrastructure, culture/workforce, next steps, chapter number] -->

# DoD Digital Engineering Strategy (2018)
**Source**: OUSD R&E / ODASD(SE) (US Government work, public domain) | **Chapters**: 7

## When to use
Use this skill when you need to reason about the Department of Defense Digital Engineering Strategy (2018, OUSD/ODASD(SE)) and its five goals: (1) formalize the development, integration, and use of models; (2) provide an enduring authoritative source of truth; (3) incorporate technological innovation; (4) establish supporting infrastructure and environments; and (5) transform the culture and workforce. This pack also covers model formalisms, provenance, governance and access control of the authoritative source of truth, and the coordinate-plan-pilot-sustain rollout sequence. It is a vision-and-policy source, not a how-to method or tool tutorial.

**Prerequisites:** none, plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill

- **Without arguments** — load the Core Frameworks below: the definition of digital engineering, the five goals, and the central mental-model shifts.
- **With a topic** — ask about a goal or focus area (e.g. "authoritative source of truth", "model formalisms", "Goal 4 infrastructure", "culture and workforce"), a shift (document-to-model, model-analyze-build), or a cited example (USS Ford, A-10, ERS, NAVAIR, Army LPDM/ePDM).
- **With a chapter** — `ch01` (intro/vision + the five goals), `ch02`–`ch06` (Goals 1–5), `ch07` (next steps + Appendix 1 summary).
- **Read it as intent, not procedure** — the Strategy is a non-prescriptive "living document"; the concrete "how" lives in DoD Component implementation plans, which this pack does not contain.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## Core Frameworks & Mental Models

### What digital engineering is

**Digital engineering** is an integrated digital approach that uses **authoritative sources of system data and models** as a **continuum across disciplines** to support lifecycle activities **from concept through disposal**. The 2018 *Digital Engineering Strategy* — authored by ODASD(SE) with government, industry, and academia stakeholders — is the governing document. It is deliberately a **vision and a compass, not a checklist**: explicitly non-prescriptive and meant to evolve, it sets shared direction while the concrete execution lives in **DoD Component / Service implementation plans**.

The driver is mission urgency: deliver capability to the warfighter faster amid exponential technology change, rising complexity, tight budgets, and compressed schedules — problems the legacy linear, document-heavy, stove-piped process handles poorly. The **system of interest** is scoped broadly: systems of systems, systems, processes, equipment, products, and parts.

### The Five Digital Engineering Goals

The entire Strategy is organized around five goals (Section IV summary; each expanded into focus areas in Section V):

1. **Formalize the development, integration, and use of models** — making modeling deliberate practice that informs enterprise- and program-level decisions. → ch02
2. **Provide an enduring, authoritative source of truth** — move the primary means of communication from documents to digital models and data. → ch03
3. **Incorporate technological innovation** to improve the engineering practice (beyond traditional model-based methods). → ch04
4. **Establish a supporting infrastructure and environments** so stakeholders can perform activities, collaborate, and communicate. → ch05
5. **Transform the culture and workforce** — equipping the Department to adopt digital engineering, and sustain it, across the lifecycle. → ch06

Read goals **1–4 as building the machine** (models, a trusted data backbone, infused technology, the environment to run them in) and **goal 5 as building the people** who run it. Adoption is the gating risk.

### Goal → focus-area structure

Each goal decomposes into numbered focus areas (Appendix 1 is the full map):

- **Goal 1**: 1.1 plan for models · 1.2 develop/integrate/curate models · 1.3 use models in decisions.
- **Goal 2**: 2.1 define the authoritative source of truth · 2.2 govern it (access, controls, governance) · 2.3 use it across the lifecycle.
- **Goal 3**: 3.1 establish an end-to-end digital engineering enterprise · 3.2 use technological innovations to improve the practice.
- **Goal 4**: 4.1 IT infrastructures · 4.2 methodologies · 4.3 secure infrastructure & protect IP.
- **Goal 5**: 5.1 improve the knowledge base · 5.2 lead & support transformation · 5.3 build & prepare the workforce.

### Key constructs

- **Authoritative source of truth (AST)** — the single, trusted central reference for models and data; captures the current state and history of the **technical baseline**, gives traceability as the system evolves, and propagates changes downstream. Its authority comes from **governance**: governance → data quality → stakeholder confidence → data-driven decisions.
- **Model formalisms** — the quality rules (syntax, semantics, lexicons, standards) that let independently authored models combine into one coherent digital representation.
- **Provenance and pedigree** — recorded model origin and lineage that, with V&V-based reviews, make a model trustworthy and reusable. Trust is engineered, not assumed.
- **Continuum of models** — the same authoritative models carried and reused concept→disposal, not rebuilt at each phase boundary.

### The mental-model shifts

- **Documents → models/data** as the primary means of communication; documents become generated *views*, and stakeholders shift from **accepting documents to accepting models**.
- **Design-build-test → model-analyze-build** — analyze and prove decisions in a **virtual environment** before physical build and fielding (virtual-first).
- **Many copies → one source of truth** — ask "is this traced from the AST?" not "which copy is current?"
- **Stove-piped IT → a consolidated, collaborative, trusted environment** (Goal 4's diagnosis and target).
- **Lock-in → standards & interfaces** — bet on the seams between tools (standards, data, formats, interfaces), not a vendor product.
- **One-time rollout → sustained socio-technical change** — **culture is the operating system** (Goal 5).

### Rollout: coordinate → plan → pilot → sustain

The Strategy sequences four next steps: **coordinate** (ODASD(SE) convenes a summit and runs the standing **Digital Engineering Working Group**), **develop implementation plans** (owned by the **DoD Components**), **implement pilot programs** (learn/measure/optimize before scaling into major programs), and **sustain** (policy, guidance, training, continuous improvement). Ownership is distributed (Components own plans); coordination is central (ODASD(SE) is a gap-closer, not a gatekeeper).

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-dod-digital-engineering-introduction-purpose-vision.md) | Introduction, Purpose & Vision | What digital engineering is; why now; the five goals introduced; the non-prescriptive "living document"; design-build-test→model-analyze-build; system of interest |
| [ch02](chapters/ch02-dod-digital-engineering-goal1-formalize-models.md) | Goal 1 — Formalize Models | Plan/develop/use models (1.1–1.3); model formalisms; provenance & pedigree; model-based reviews; the authoritative source of truth foundation; USS Ford example |
| [ch03](chapters/ch03-dod-digital-engineering-goal2-authoritative-source-of-truth.md) | Goal 2 — Authoritative Source of Truth | Define/govern/use the AST (2.1–2.3); governance, access & controls; technical baseline; document-to-model acceptance shift; Army LPDM/ePDM example |
| [ch04](chapters/ch04-dod-digital-engineering-goal3-technological-innovation.md) | Goal 3 — Technological Innovation | End-to-end digital enterprise (3.1); use of data, human-machine interaction, technology insertion (3.2); evolving digital representation; A-10 digital thread |
| [ch05](chapters/ch05-dod-digital-engineering-goal4-infrastructure-environments.md) | Goal 4 — Infrastructure & Environments | IT infrastructure (4.1); methodologies (4.2); cybersecurity & IP protection (4.3); standards-over-tools; modular/cloud; ERS example |
| [ch06](chapters/ch06-dod-digital-engineering-goal5-culture-workforce.md) | Goal 5 — Culture & Workforce | Culture as shared values/behaviors; knowledge base & standards gap (5.1); transformation as change management (5.2); preparing the workforce (5.3); enablers; NAVAIR example |
| [ch07](chapters/ch07-dod-digital-engineering-next-steps-conclusion-summary.md) | Next Steps & Appendix 1 | Coordinate→plan→pilot→sustain; ODASD(SE) coordination & DoD Components; DEWG; the goal/focus-area summary table |

## Topic Index

- **A-10 example / digital thread** → ch04
- **Access and controls** → ch03
- **Appendix 1 (goal/focus-area summary)** → ch07
- **Authoritative source of truth (AST)** → ch03, ch02
- **Continuum of models** → ch02, ch01
- **Culture (shared values and behaviors)** → ch06
- **Cybersecurity (in digital engineering)** → ch05
- **Define / govern / use the AST (2.1–2.3)** → ch03
- **Design-build-test → model-analyze-build** → ch01
- **Digital artifacts** → ch03
- **Digital engineering (definition)** → ch01
- **Digital Engineering Strategy (2018)** → ch01, ch07
- **Digital Engineering Working Group (DEWG)** → ch07
- **Document-to-model shift** → ch03
- **End-to-end digital enterprise** → ch04, ch01
- **Engineered Resilient Systems (ERS)** → ch05
- **Evolving digital representation** → ch04
- **Five goals (summary)** → ch01, ch07
- **Focus areas (structure)** → ch07
- **Formalize models (Goal 1)** → ch02
- **Governance (of the AST)** → ch03
- **Human-machine interaction** → ch04
- **Infrastructure and environments (Goal 4)** → ch05
- **Intellectual property protection** → ch05
- **LPDM / ePDM (Army example)** → ch03
- **Methodologies (Goal 4.2)** → ch05
- **Model formalisms (syntax/semantics/lexicons)** → ch02
- **Model provenance and pedigree** → ch02
- **Model-based reviews and audits** → ch02
- **NAVAIR SE Transformation** → ch06
- **Next steps (coordinate/plan/pilot/sustain)** → ch07
- **ODASD(SE) / DoD Components** → ch07, ch01
- **Pilot programs** → ch07
- **Standards and interfaces (over tools)** → ch05
- **System of interest** → ch01
- **Technical baseline** → ch03
- **Technological innovation (Goal 3)** → ch04
- **Technology insertion / infusion** → ch04
- **Transformation as change management** → ch06
- **USS Ford (CVN-78) example** → ch02
- **Workforce (build and prepare)** → ch06

## Supporting Files

- [glossary.md](glossary.md) — key terms from the Strategy, alphabetical, with chapter references
- [patterns.md](patterns.md) — practitioner patterns (plan models first, engineer model trust, define→govern→use the AST, open-but-guarded access, standards-over-tools, managed technology infusion, transform the people, pilot before scaling) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, the five goals, goal→focus-area map, the mental-model shifts, the four next steps, cited examples, tells & smells

---

## Scope & Limits

**Covers**: the *DoD Digital Engineering Strategy* (2018) in full — the definition and vision of digital engineering; the five goals and their focus areas; the document-to-model and design-build-test→model-analyze-build shifts; model formalisms, provenance/pedigree, and model-based reviews; the authoritative source of truth (define/govern/use, governance, access control, technical baseline); the end-to-end digital enterprise, data-driven decisions, human-machine interaction, and technology insertion; supporting infrastructure, methodologies, cybersecurity, and IP protection; the culture/workforce transformation and its enablers; and the coordinate→plan→pilot→sustain rollout with its cited Service examples (USS Ford, Army LPDM/ePDM, A-10, ERS, NAVAIR).

**Does not cover**: this is a **vision-and-policy strategy, deliberately non-prescriptive** — it provides *no* step-by-step method, tool tutorials, or implementation procedure. It is **thin on** quantitative metrics, detailed acquisition-policy mechanics, and the contents of DoD Component implementation plans (which it points to but does not contain). For MBSE/SysML mechanics use the `sebok` pack and SysML v2 / Cameo tooling; for SE process detail use `dau-se-guidebook`; for systems-security-engineering depth use `nist-sse`; for open/modular architecture see `dod-mosa`. The **CAC-gated Digital Engineering Body of Knowledge (DEBoK)** is intentionally **excluded** (not public).

**Source version**: *DoD Digital Engineering Strategy*, OUSD R&E / ODASD(SE), **June 2018** (Distribution Statement A — approved for public release; distribution unlimited).

**Jurisdiction**: US Government public-domain work (17 U.S.C. 105). Freely reproducible, including commercially; attribution to the DoD is a courtesy, not an obligation, and the DoD does not endorse this pack.
