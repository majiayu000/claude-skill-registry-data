---
name: digital-systems-engineering
description: "Knowledge pack from 'Towards Digital Engineering: The Advent of Digital Systems Engineering' (Huang et al., Old Dominion University, arXiv:2002.11672, 2020). Use when reasoning about digital engineering, the DoD Digital Engineering Strategy and its five goals, the Authoritative Source of Truth, digitalization vs. digitization, digital augmentation, digitalized models, provenance, unique identification, and the four-level (vision/strategy/action/foundation) DSE research framework. Covers the conceptual/vision layer of the field. SCOPE LIMITS: this is a single ~28-page vision paper, not a methods handbook — it is thin on step-by-step procedures, tooling, case studies, and quantitative evaluation, and it predates 2020 so it does not cover later digital-engineering standards or recent AI/LLM advances. Use the sebok pack for established SE canon and MBSE depth."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Digital Systems Engineering (Towards Digital Engineering)
**Source**: Huang, Gheorghe, Handley, Pazos, Pinto, Kovacic, Collins, Keating, Sousa-Poza, Rabadi, Unal, Cotter, Landaeta, Daniels — Old Dominion University | **Version**: arXiv:2002.11672 (2020 preprint; paper in press at *Int. J. System of Systems Engineering*) | **Pages**: ~28 | **Chapters**: 7 | **Licence**: CC BY 4.0 | **Generated**: 2026-06-22

## When to use
Use this skill when you need to reason about digital engineering concepts drawn from the 2020 Old Dominion University vision paper (arXiv:2002.11672, Huang et al.). This pack covers the DoD Digital Engineering Strategy and its five goals, the Authoritative Source of Truth, the distinction between digitalization and digitization, digital augmentation, digitalized models, provenance, unique identification, and the four-level (vision/strategy/action/foundation) DSE research framework. It is the right starting point for the conceptual and vision layer of digital systems engineering; pair it with the sebok pack for established SE canon and MBSE depth.

**Prerequisites:** none, plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill

- **Without arguments** — load the Core Frameworks below for reference.
- **With a topic** — ask about `digitalization`, `the Authoritative Source of Truth`, `the five DES goals`, `the four-level framework`, `digital augmentation`, `provenance`, or another indexed topic; I read the relevant `chapters/chNN-*.md` file before answering.
- **With a chapter** — ask for `ch06` to load the four-level (vision/strategy/action/foundation) framework.
- **Browse** — ask "what chapters do you have?" to see the full index.

When you ask about a topic not covered in Core Frameworks below, I read the matching `chapters/chNN-*.md` file first. Supporting files: `glossary.md` (key terms), `patterns.md` (conceptual techniques), `cheatsheet.md` (decision rules and selection tables).

**Prerequisites**: none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

---

## Core Frameworks & Mental Models

**Digital systems engineering (DSE) as an emerging field (Ch 1, 7).** DSE is framed as a new academic discipline that brings digital technologies into systems engineering to support *digital engineering* — the digital transformation of engineering practice. The paper is a vision/research charter, not a finished method: it names what must be built (theory, methods, models, tools), defines a compact vocabulary, and lays out where research issues sit. Its anchoring driver is the US DoD Digital Engineering Strategy (2018).

**The DoD Digital Engineering Strategy and its five goals as a load-bearing stack (Ch 2).** The DES aims to render systems as digital models authored, joined, and consumed across the lifecycle, connected through an Authoritative Source of Truth. Its five goals are a dependency stack, not a checklist: **G5 (culture/workforce)** and **G4 (IT infrastructure)** are the foundations; **G2 (AST repository)** builds on G4 and feeds **G1 (formalized model lifecycle, the fundamental goal)**; **G3 (end-to-end digital enterprise)** sits on top as the driving force whose pursuit of new technology issues fresh requirements downward. Skipping a lower layer leaves the upper ones unsupported.

**Authoritative Source of Truth (AST) (Ch 2, 3, 4).** A shared, governed repository hosting standardized models, data, and artifacts — the hub through which collaboration and exchange pass. It captures provenance, maintains traceability, and propagates updates to every dependent entity ("right data, right person, right use, right time"). It is governed: access-controlled, used as the technical baseline for cost/schedule/performance and technical review. The AST inherits hard problems — distributed supply-chain trust, heterogeneous access-control policies (MAC/RBAC/ABAC), and IP protection.

**Digitalize ≠ digitize (Ch 5).** The pack's pivotal distinction. To *digitalize* an artifact is to give it (1) a standard, machine-accessible representation, (2) a unique identifier, (3) standard metadata enabling automated machine operation, all (4) uniquely bound together. A merely *digitized* item may be computerized but can't be operated on automatically across machines. Digitalization is a spectrum set by four dials — representation fidelity, semantic depth, form compatibility, metadata richness — that predict how much automation is possible.

**Digital augmentation and digitalized artifacts (Ch 5, 6).** A digitalized artifact = the artifact + a digital augmentation made of three parts: a digital representation, a uniquely associated identifier, and associated metadata. **Models** get a richer metadata schema (generic attributes, I/O and parameters, provenance, utilization guide, security properties, machine-processible access-control policies) because digital representation of the system of interest is the central theme of DE. Capturing the relations among model types is the **"model of models."**

**Unique identification → traceability & accountability (Ch 5, 7).** Unique identification is a necessary component of digitalization: it underpins traceability and accountability, broadened beyond requirement traceability to include information flow, material flow, causality chains, and fault chains across the lifecycle.

**Provenance as the currency of reuse (Ch 4, 7).** Provenance is recorded lineage; it is the basis for judging an artifact's value and integrity, and it enables model reproducibility and replicability. The concept matures along a ladder — Data Provenance → Knowledge Provenance → Open Provenance Model → PROV ontology (usable for engineering artifacts).

**The centralized vs. distributed dial (Ch 3, 5, 6).** One tension recurs across standardization, trust, and access control. Centralization (one standard, one AST, one policy) is faster and more efficient near-term but concentrates risk — single point of failure, wrong-direction lock-in, stifled innovation if set too early. Distribution (evolutionary ontologies, distributed trust, heterogeneous policies) hedges those risks at the cost of near-term efficiency. The meta-principle: preserve diversity through evolution.

**Five enabling-technology clusters as a portfolio (Ch 4).** DE runs on a portfolio, not a silver bullet: **AI & ML** (central — automation, model-building), **ontologies & semantics** (shared meaning across boundaries), **provenance** (artifact lineage), **trust management** (defensible access and trust for the AST), and **computing infrastructure** (HPC/cloud/big data — a hard dependency). Each owns one stage of an artifact's journey from creation to trustworthy reuse.

**The four-level DSE research framework (Ch 6).** The master map: **Vision** (why) → **Strategy** (what moves) → **Action** (what work) → **Foundation** (what enables it), read top-down as a realization chain. Strategy = four moves (transform practice, workforce/education, infrastructure, embrace innovative tech). Action = digitalize artifacts, operate on them (Creation/Curation/Qualification/Governance/Sharing/Utilization × five lifecycle stages), run lifecycle activities, build innovative applications. Foundation = digitalization foundations, digital trust, cybersecurity, big data & ML. **DSE and MBSE are complementary, not rivals** — MBSE drives document→model-centric; DSE adds digitalization, identification, big data, and digital trust; both rest on classical systems thinking.

---

## Chapter Index

| # | Chapter | Key Frameworks |
|---|---------|----------------|
| [ch01](chapters/ch01-digital-systems-engineering-introduction-and-landscape.md) | Introduction and the Digital Engineering Landscape | Digital Engineering Strategy; Authoritative Source of Truth; Fourth Paradigm; CPS3 |
| [ch02](chapters/ch02-digital-systems-engineering-goals-of-the-de-strategy.md) | Goals of the Digital Engineering Strategy | Five DES goals as a dependency stack; AST; three core transformations |
| [ch03](chapters/ch03-digital-systems-engineering-challenges.md) | Challenges in Digital Engineering | Eight named challenges; centralized vs. distributed; MAC/RBAC/ABAC; SCI; reproducibility ladder |
| [ch04](chapters/ch04-digital-systems-engineering-key-enabling-technologies.md) | Key Enabling Technologies | Five technology clusters; provenance maturity ladder; trust management; access-control spectrum |
| [ch05](chapters/ch05-digital-systems-engineering-framework-and-core-concepts.md) | Framework and Core Concepts | Digitalize vs. digitize; four-part definition; digital augmentation; digitalized models; model of models |
| [ch06](chapters/ch06-digital-systems-engineering-four-level-framework.md) | The Four-Level Framework | Vision/Strategy/Action/Foundation; DSE vs. MBSE; operation × lifecycle matrix; six operations |
| [ch07](chapters/ch07-digital-systems-engineering-concluding-remarks-and-research-agenda.md) | Concluding Remarks and Research Agenda | Field-not-method framing; research charter; distributed digital trust; data-intensive SE |

## Topic Index

- **Access control / MAC / RBAC / ABAC / XACML** → ch04, ch03
- **AI and machine learning cluster** → ch04, ch06
- **Authoritative Source of Truth (AST)** → ch02, ch03, ch04, ch01
- **Big data / five Vs** → ch03, ch04, ch06
- **Blockchain / digital trust** → ch04, ch06, ch05
- **Centralized vs. distributed** → ch03, ch05, ch06
- **Challenges in digital engineering** → ch03
- **Computing infrastructure / HPC / cloud** → ch04, ch06
- **Core concepts / vocabulary** → ch05, ch07
- **Data-intensive systems engineering** → ch06, ch07
- **DoD Digital Engineering Strategy (DES) / five goals** → ch02, ch01, ch03
- **Digital augmentation** → ch05, ch06
- **Digital engineering landscape / Industry 4.0** → ch01, ch06
- **Digital systems engineering as a field** → ch01, ch07, ch06
- **Digital twin** → ch05, ch01
- **Digitalize vs. digitize** → ch05
- **Digitalized artifacts** → ch05, ch06
- **Digitalized models / model of models** → ch05, ch07
- **Enabling technologies** → ch04, ch01, ch05
- **Four-level framework (vision/strategy/action/foundation)** → ch06, ch07
- **Fourth Paradigm / data-intensive science** → ch01
- **MBSE relationship to DSE** → ch06
- **Ontologies and semantics** → ch04, ch05, ch06
- **Provenance** → ch04, ch07, ch02
- **Reproducibility and replicability** → ch03, ch07
- **Research agenda / open problems** → ch07, ch03, ch06
- **Scientific computing integrity (SCI)** → ch03, ch04
- **Six operations on artifacts** → ch06
- **Standardization (standards vs. ontologies)** → ch05, ch03, ch06
- **Trust management** → ch04, ch06
- **Unique identification / traceability / accountability** → ch05, ch06, ch07
- **Workforce and culture transformation** → ch02, ch03, ch06

## Supporting Files

- [glossary.md](glossary.md) — key digital-systems-engineering terms with definitions and chapter refs
- [patterns.md](patterns.md) — conceptual techniques (digitalize-don't-digitize, digital augmentation, centralization dial, provenance for reuse, the goal stack, placing problems in the four-level framework)
- [cheatsheet.md](cheatsheet.md) — decision rules, the DES goal stack, four-level framework table, access-control selection, provenance/reproducibility ladders, tells & smells

## Scope & Limits

- **Source version**: arXiv:2002.11672 (2020 preprint), the openly licensed (CC BY 4.0) version — *not* the paywalled journal edition. This pack is grounded only in the preprint; quantities, figures, and wording are paraphrased.
- **It is a single ~28-page vision paper.** It is deliberately thin on: step-by-step methods and procedures, specific tooling/standards implementations, worked case studies, and quantitative evaluation or validation. The enabling-technology survey (Ch 4) is illustrative, naming anchor references per cluster rather than offering a comprehensive review.
- **Predates 2020.** It does not cover later digital-engineering standards, post-2020 MBSE tooling, or recent AI/LLM advances; treat AI/ML claims as of their time.
- **DoD-anchored.** The DES framing is US-defense-specific; the authors generalize it into the four-level framework but note that framing's origin.
- **Use alongside**: the `sebok` pack for established SE canon, lifecycle processes, and MBSE depth; the `nist-sse` pack for systems-security-engineering treatment of the protection/access-control themes raised here. This pack's best use is the conceptual/vision layer — the precise vocabulary (digitalize, digital augmentation, digitalized model) and the structuring frameworks (five DES goals, four-level DSE map) you cite when positioning digital-engineering work.
