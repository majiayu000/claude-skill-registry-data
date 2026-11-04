---
name: dod-mq-bok
description: "Knowledge base from the DoD M&Q BoK (the Manufacturing and Quality Engineering Body of Knowledge), v3.0 of July 2025, published by OUSD(R&E). Use for the manufacturing-and-quality view of the defense acquisition life cycle: what M&Q engineers do across the Adaptive Acquisition Framework phases (Pre-MDD, Materiel Solution Analysis, Technology Maturation and Risk Reduction, Engineering and Manufacturing Development, Production and Deployment, Operations and Support); the twelve M&Q threads (A–L) built on the '5 Ms'; manufacturing feasibility and producibility; Manufacturing Readiness Levels and assessments; Key/Critical Characteristics and process capability (Cp/Cpk, SPC); the standards stack (AS6500, AS9100/ISO 9001, AS9103, AS9145); technical reviews (ASR/PDR/CDR/PRR) and milestone gates; DCMA surveillance; industrial base and supply chain; and sustainment (LCSP, IPS, ILA, ISR). Scope is DoD acquisition M&Q practice on the Major Capability Acquisition path — it is a best-practice compilation, not policy, and is thin on detailed shop-floor process engineering, contract law, and the full text of the cited industry standards (which it names but does not reproduce)."
---

<!-- argument-hint: [acquisition phase, M&Q thread, MRL/MRA, producibility, Key Characteristic, process capability, technical review/milestone, DCMA, sustainment, standard number, chapter number] -->

# DoD Manufacturing and Quality Engineering Body of Knowledge (M&Q BoK)
**Source**: OUSD(R&E) Systems Engineering and Architecture (US Government work, public domain; Distribution A) | **Version**: 3.0, July 2025 | **Chapters**: 6

## When to use
Use this skill to reason about **manufacturing and quality (M&Q) engineering across the defense acquisition life cycle** — what an M&Q practitioner should do, when, and with which frameworks, from before a program exists (Pre-MDD) through fielding and sustainment (O&S). It answers the recurring M&Q question "*Can it be built?*" and frames producibility, manufacturing risk, readiness, and quality as activities that must start at the front end, not bolt on at production. It complements the broader SE/acquisition packs (`dau-se-guidebook`, `nasa-npr-7123`, `gao-tra`, `dod-mosa`) with the M&Q lens specifically.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below: the AAF lifecycle phases, the twelve M&Q threads, MRLs, the "Can it be built?" feasibility logic, Key Characteristics / process capability, and the standards stack.
- **With a phase** — route to the chapter for that phase: Pre-MDD `ch01`, MSA `ch02`, TMRR `ch03`, EMD `ch04`, P&D `ch05`, O&S `ch06`.
- **With a topic** — use the Topic Index below (e.g. "producibility", "MRL target", "Key Characteristic", "PDR", "DCMA", "LCSP", a standard number).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **One scaffold, six phases.** Every chapter is one **acquisition life-cycle phase**, and every chapter is internally organized by the same **twelve M&Q threads (A–L)**. So you navigate by *phase* (which chapter) and by *thread* (which topic area within it).

## Core Frameworks & Mental Models

### What M&Q engineering is, and its one governing question
Manufacturing and Quality engineering is the specialty discipline that makes sure a defense system can actually be **produced** (manufacturing's role — producibility) and that it is **reliable and conforming** (quality's role). The BoK is a compilation of best practices and lessons learned that **supports but does not supersede** DoD policy, guidance, or law. Its unifying test recurs in every phase: **"Can it be built?"** — can this solution be produced with available capability while meeting quality, rate, cost, and schedule. A second recurring truth: M&Q **influences, it does not have authority** — the practitioner sits on the technical IPT and embeds credible M&Q inputs into documents and decisions others own.

### The Adaptive Acquisition Framework lifecycle (the chapter spine)
The 2025 BoK is rewritten around the **Adaptive Acquisition Framework (AAF)**, implemented by **DoDI 5000.02**. It documents the **Major Capability Acquisition (MCA)** path in detail but states the practices tailor to the other pathways (Urgent Capability Acquisition, Middle Tier of Acquisition rapid prototyping/fielding, etc.). The six MCA phases — one per chapter — and their M&Q centre of gravity:

| Phase | Ends at | M&Q focus | Headline reviews |
|---|---|---|---|
| **Pre-MDD** | Materiel Development Decision (MDD) | feasibility of each concept; producibility into the draft ICD and AoA guidance | — |
| **MSA** (Materiel Solution Analysis) | Milestone A | choose a producible concept; translate KPP/KSA → Key Characteristics; industrial-base assessment | ASR |
| **TMRR** (Tech Maturation & Risk Reduction) | Milestone B | drive risk down; competitive prototyping; mature processes | SRR, SFR, **PDR** |
| **EMD** (Engineering & Manufacturing Development) | Milestone C | influence design, prepare for production, execute plans; pilot line | **CDR**, TRR, SVR/FCA, PCA, **PRR** |
| **P&D** (Production & Deployment) | Full-Rate Production decision | LRIP → FRP; demonstrate rate maturity | MRA at MRL 9/10 |
| **O&S** (Operations & Support) | disposal | sustainment, supply chain, obsolescence, O&S cost | **ISR**, ILA |

### The Twelve M&Q Threads (A–L) — the constant within every chapter
Each chapter walks the same twelve threads, each built on the **"5 Ms"** (Manpower, Machines, Materials, Methods, Measurement), on MRL criteria, and on three DoD-unique functions (acquisition, contracting, surveillance):

The three DoD-unique functions — **A** (DoD Acquisition System), **B** (Defense Contracting), and **C** (Surveillance) — sit alongside the engineering and resource threads: **E** Design, **F** Cost and Funding, **D** the Technology and Industrial Base, and **G** Materials Management; and the factory-and-system threads: **H** Process Capability and Control, **I** Quality Management, **J** the Manufacturing Workforce, **K** Facilities, and **L** Manufacturing Management and Control.

Within each thread the BoK lists **Activities → Tasks** (which M&Q leads or supports) **→ Tools → Resources**. Use the threads as a tailorable per-phase checklist.

### Readiness and risk: MRLs, assessments, and the RIO engine
- **Manufacturing Readiness Levels (MRLs, 1–10)** are the BoK's named best-practice yardstick for manufacturing risk, assessed via a **Manufacturing Readiness Assessment (MRA)** against MRL criteria. Targets are tied to phase events (broadly MRL 4 by Milestone A, MRL 6 by Milestone B/PDR, MRL 7–8 across EMD/CDR, MRL 8 by Milestone C/PRR, MRL 9–10 in production). MRLs run parallel to **Technology Readiness Levels / the TRA**, which gauge Critical Technology Element maturity.
- The **DoD Risk, Issue, and Opportunity (RIO)** five-step process — Plan, Identify, Analyze (likelihood × consequence), Mitigate (accept/avoid/transfer/control), Monitor — is the recurring risk engine. Missing a target triggers a **Manufacturing Maturation Plan (MMP)**.
- An **Independent Technical Risk Assessment (ITRA)** (per the **DTRAM** methodology, 10 U.S.C. §2448b) renders an *independent* judgment at Milestones A/B/C and the FRP decision — it leverages but does not merely echo the program's TRAs/MRAs.

### Quality and process capability
- Translate validated **KPPs/KSAs into Key Characteristics (KC)** — and **Critical Characteristics (CC)** where variation risks loss of life or catastrophic failure — using the **Pareto principle** (a few features dominate performance). Each KC is driven by a **Key Manufacturing Process (KMP)**.
- A process must be both **capable** (meets spec — Cp/Cpk, with AS9103 naming a KC target of **Cpk ≥ 1.33**) and **in control** (statistically predictable — SPC/control charts); **Pp/Ppk** describe actual performance over time. Reduce variation with a **Variability Reduction Program** (Process Control Plans, FMEA, Six Sigma/DMAIC).
- **Quality** = the degree to which a product's attributes satisfy a need, managed through a **Quality Management System (QMS)** — typically ISO 9001 or AS9100. *A conforming management system does not by itself guarantee a conforming product.*

### The standards stack
**AS6500** (Manufacturing Management Program — the system benchmark; implemented via **MIL-HDBK-896**), **AS9100 / ISO 9001** (QMS), **AS9103** (Variation Management of Key Characteristics), **AS9145** (APQP/PPAP), **AS9102** (First Article Inspection), **AS5553 / AS6174** (counterfeit avoidance), **IEEE 15288.1/.2** (SE on defense programs / technical reviews and audits), **MIL-STD-881** (WBS). *(The BoK names and applies these; it does not reproduce their text — and neither does this pack.)*

### Surveillance, industrial base, and sustainment
- **DCMA** provides contract administration and surveillance, delegated via MOA/LOD/QALI, and runs a **Detection-to-Prevention (D2P)** posture: verify process capability and management-system health with data rather than re-inspecting end items.
- The **National Technology and Industrial Base (NTIB)** (US, Canada, UK, Australia) must be considered in MDAP planning — including single points of failure (sole/single/fragile/foreign sources), surge capacity, and supply-chain resilience.
- After fielding, sustainment is governed by the **Life Cycle Sustainment Plan (LCSP)**, the twelve **Integrated Product Support (IPS) Elements**, the **In-Service Review (ISR)**, and periodic **Independent Logistics Assessments (ILA)** — with explicit attention to **O&S cost**, the usual dominant share of life-cycle cost.

### The digital thread
Throughout, **digital engineering** carries M&Q data: the **digital thread** links requirements → design → production → V&V → sustainment → cost, via **Technical Data Packages (TDP)**, **Product Lifecycle Management (PLM)**, and **Product Manufacturing Information (PMI)** (GD&T, BOM, material specs embedded in 3D CAD).

---

## Chapter Index

| # | AAF Phase | Ends at | Key content |
|---|-----------|---------|-------------|
| [ch01](chapters/ch01-dod-mq-bok-pre-mdd.md) | Pre-Materiel Development Decision (Pre-MDD) | MDD | Front-end M&Q before a program exists; feasibility of each concept; producibility into ICD/AoA guidance; JCIDS chain; CTEs; NTIB; early research budget activities (6.1/6.2/6.3) |
| [ch02](chapters/ch02-dod-mq-bok-msa.md) | Materiel Solution Analysis (MSA) | Milestone A | "Can it be built?"; AoA support; KPP/KSA → Key Characteristics; Acquisition Strategy/SEP; producibility framework; cost estimating; the ASR |
| [ch03](chapters/ch03-dod-mq-bok-tmrr.md) | Technology Maturation & Risk Reduction (TMRR) | Milestone B | Driving risk down to commit to EMD; competitive prototyping; SRR/SFR/**PDR**; MTA rapid prototyping; process capability and yield; APQP/Lean |
| [ch04](chapters/ch04-dod-mq-bok-emd.md) | Engineering & Manufacturing Development (EMD) | Milestone C | Influence design / prepare for production / execute plans; **CDR**, SVR/FCA, PCA, **PRR**; the pilot line and FAI/FAT; KC management cycle; producibility toolkit |
| [ch05](chapters/ch05-dod-mq-bok-prod-deploy.md) | Production & Deployment (P&D) | FRP decision | LRIP → Full-Rate Production; MRA at MRL 9/10; DCMA Manufacturing Systems Risk Assessment; QMS clause structure; counterfeit avoidance |
| [ch06](chapters/ch06-dod-mq-bok-ops-support.md) | Operations & Support (O&S) | disposal | Sustainment governance: LCSP, the 12 IPS Elements, **ISR**, ILA; SCOR supply chain; DMSMS/obsolescence; workforce competency; O&S cost control |

## Topic Index

- **5 Ms (Manpower/Machines/Materials/Methods/Measurement)** → ch02, ch01
- **Acquisition Strategy** → ch02, ch03
- **Adaptive Acquisition Framework (AAF) / DoDI 5000.02** → ch01, ch04
- **Alternative Systems Review (ASR)** → ch02
- **Analysis of Alternatives (AoA)** → ch02, ch01, ch03
- **APQP / AS9145 / PPAP** → ch03, ch04
- **AS6500 (Manufacturing Management Program)** → ch04, ch05
- **AS9100 / ISO 9001 (QMS)** → ch05, ch04
- **AS9103 (Variation Management of Key Characteristics)** → ch04, ch03
- **Counterfeit parts avoidance (AS5553/AS6174)** → ch06, ch05
- **Critical Characteristic (CC)** → ch04, ch05
- **Critical Design Review (CDR)** → ch04
- **Critical Technology Element (CTE)** → ch01, ch03
- **DCMA surveillance / Detection to Prevention (D2P)** → ch01, ch02
- **DCMA Manufacturing Systems Risk Assessment** → ch05
- **Digital thread / digital engineering / TDP / PMI** → ch01, ch03
- **DOTMLPF** → ch01
- **DTRAM (Defense Technical Risk Assessment Methodology)** → ch03, ch04
- **Engineering and Manufacturing Development (EMD)** → ch04
- **Facilities (Thread K)** → ch04, ch06
- **First Article Inspection / Test (FAI/FAT)** → ch04
- **FMEA** → ch04, ch03
- **Full-Rate Production (FRP)** → ch05, ch04
- **Independent Logistics Assessment (ILA)** → ch06, ch04
- **Independent Technical Risk Assessment (ITRA)** → ch04, ch03
- **In-Service Review (ISR)** → ch06
- **Integrated Product Support (IPS) Elements** → ch06
- **Integrated Product Team (IPT)** → ch03
- **JCIDS / ICD / CDD** → ch02, ch01
- **Key Characteristic (KC)** → ch04, ch02
- **Lean / Six Sigma / DMAIC** → ch04, ch03
- **Life Cycle Sustainment Plan (LCSP)** → ch06, ch05
- **Low-Rate Initial Production (LRIP)** → ch05
- **Manufacturing feasibility ("Can it be built?")** → ch02, ch01
- **Manufacturing Maturation Plan (MMP)** → ch03, ch04
- **Manufacturing Readiness Assessment (MRA)** → ch04, ch05
- **Manufacturing Readiness Level (MRL) targets** → ch04, ch05
- **Materiel Development Decision (MDD)** → ch01
- **Materiel Solution Analysis (MSA)** → ch02
- **Milestone A** → ch02, ch03
- **Milestone B** → ch03, ch04
- **Milestone C** → ch04, ch05
- **Mission Engineering (ME)** → ch01
- **National Technology and Industrial Base (NTIB)** → ch01, ch06
- **Pilot line / production-representative environment** → ch04, ch05
- **Pre-Materiel Development Decision (Pre-MDD)** → ch01
- **Preliminary Design Review (PDR)** → ch03
- **Process capability (Cp/Cpk, Pp/Ppk)** → ch04, ch03
- **Producibility** → ch04, ch02
- **Production and Deployment (P&D)** → ch05
- **Production Readiness Review (PRR)** → ch04, ch03
- **Quality Management System (QMS)** → ch05, ch04
- **Risk, Issue, and Opportunity (RIO) management** → ch05, ch04
- **SCOR supply-chain model** → ch06
- **Statistical Process Control (SPC)** → ch03, ch04
- **Systems Engineering Plan (SEP)** → ch02, ch03
- **Technology Maturation and Risk Reduction (TMRR)** → ch03
- **Technology Readiness Assessment (TRA)** → ch03, ch02
- **Twelve M&Q Threads (A–L)** → ch02, ch03
- **Variability Reduction Program** → ch03, ch04
- **Workforce (Thread J)** → ch06, ch04
- **Yield (First Pass / Rolling Throughput / Final)** → ch03, ch02

## Supporting Files

- [glossary.md](glossary.md) — key M&Q acquisition terms (phases, MRLs, KC/CC, the standards, reviews, sustainment), alphabetical, with chapter references
- [patterns.md](patterns.md) — eight reusable M&Q practices (front-end injection, the twelve-thread checklist, MRL-target management, KC variation control, the pilot line, the RIO/ITRA loop, process-based surveillance, LCSP sustainment) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, the lifecycle→M&Q-focus table, the twelve threads, the standards stack, the RIO engine, process-capability vocabulary, and tells & smells

---

## Scope & Limits

**Covers**: the manufacturing-and-quality engineering view of the defense acquisition life cycle per the DoD M&Q BoK v3.0 (July 2025) on the **Major Capability Acquisition** path — the six AAF phases (Pre-MDD → O&S); the twelve M&Q threads (A–L) and the "5 Ms"; manufacturing feasibility and producibility; Manufacturing Readiness Levels and assessments and their phase targets; Key/Critical Characteristics and process capability/control (Cp/Cpk, Pp/Ppk, SPC, yield); the named standards stack (AS6500, AS9100/ISO 9001, AS9103, AS9145, AS9102, AS5553/AS6174, IEEE 15288.1/.2, MIL-STD-881); milestone gates and technical reviews (ASR/SRR/SFR/PDR/CDR/SVR/FCA/PCA/PRR); the RIO risk process, ITRA/DTRAM, and Manufacturing Maturation Plans; DCMA surveillance and Detection-to-Prevention; the industrial base / NTIB and supply chain; the digital thread; and sustainment (LCSP, IPS Elements, ISR, ILA, SCOR, DMSMS).

**Does not cover in depth / is thin on**: this is a **best-practice compilation, not policy** — it does not supersede DoDI 5000.02, JCIDS, or law, and defers to them. It documents the **MCA path** primarily, treating the other AAF pathways (UCA, MTA) as tailored/compressed variants rather than covering them fully. It is light on **detailed shop-floor process engineering** (specific manufacturing processes, machine setups, metallurgy) and on **contract law / FAR-DFARS mechanics** beyond naming the relevant parts. It **names but does not reproduce** the cited industry standards (AS6500, AS9100, AS9103, IEEE 15288, etc.), which are third-party copyrighted — go to the standards themselves for normative text. One internal inconsistency to note: the source gives **conflicting MRL targets for the FRP decision (MRL 9 vs MRL 10)** — treat the higher band as gating.

**Jurisdiction / authority**: US Department of Defense acquisition. The BoK is a US Government work in the public domain (Distribution A, approved for public release, DOPSR Case #25-T-2448); its guidance is best practice for DoD programs and informative — not binding — outside that context.

**Source version**: DoD M&Q BoK — the Manufacturing and Quality Engineering Body of Knowledge — **v3.0**, dated **July 2025**, from OUSD(R&E) Systems Engineering and Architecture.
