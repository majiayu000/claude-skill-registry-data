---
name: nist-cps
description: "Knowledge base from the NIST Framework for Cyber-Physical Systems (SP 1500-201/202/203, v1.0, 2017). Use for engineering and analyzing cyber-physical systems (CPS) and IoT: the CPS Framework's aspect × facet grid (nine aspects of concern examined through conceptualization, realization, and assurance facets), cross-property trustworthiness risk management (safety/security/privacy/reliability/resilience together), data interoperability (syntactical/semantic/contextual, canonical models, identifiers, provenance), the timing aspect (time-interval classes, time domains, time-aware networking) and secure/resilient time (GNSS jamming/spoofing, PTP/NTP attacks, holdover, the clock-error model and Allan/MTIE metrics), plus the use-case requirements method. Bridges IT and OT under a clock. Scope limits: a 2017 living/draft document, thin on post-2017 standards and on detailed control catalogs; it names but does not reproduce ISO/IEC/IEEE 42010 and 15288 process text or permission-licensed third-party figures."
---

<!-- argument-hint: [aspect/facet, trustworthiness property, data interoperability, timing/TI class, secure time, GNSS/PTP/NTP, use case, chapter number] -->

# NIST Framework for Cyber-Physical Systems (SP 1500-201/202/203)
**Source**: NIST (US Government work, public domain) | **Chapters**: 8

## When to use
Use this skill to conceptualize, realize, and assure a cyber-physical system or IoT system in a disciplined way: structuring the analysis on the CPS Framework's grid, managing the interacting trustworthiness properties as one cross-property risk problem rather than five silos, making data exchange actually interpretable across domains, treating timing as a first-class architectural and security concern, and deriving requirements from use cases. It is the CPS/IoT counterpart to the broader SE canon (`sebok`, `nasa-npr-7123`, `dau-se-guidebook`) and the security-engineering packs (`nist-sse`).

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below: the aspect × facet grid, cross-property trustworthiness, data interoperability, the timing aspect, and secure/resilient time.
- **With a topic** — ask about an aspect or facet, a trustworthiness property (e.g. "resilience vs. reliability"), data interoperability (e.g. "canonical model", "identifiers"), a timing-interval class, or secure time (e.g. "GNSS spoofing", "PTP attacks", "holdover").
- **With a chapter** — `ch02` (the Framework grid), `ch04` (cross-property risk), `ch05` (data interoperability), `ch06` (timing), `ch08` (managing and securing time).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **Three volumes, one Framework.** **Vol 1 (SP 1500-201)** defines the CPS Framework (chapters 1–3 here). **Vol 2 (SP 1500-202)** is the working-group reports — cybersecurity/privacy, data interoperability, timing, and use cases (chapters 4–7). **Vol 3 (SP 1500-203)** is the Timing Annex (chapter 8). This is a **2017 v1.0 living document**, explicitly draft in places.

## Core Frameworks & Mental Models

### What a CPS is

A **cyber-physical system** fuses computation, communication, sensing, and actuation onto physical systems to deliver functions whose correctness depends on **timing**. Its irreducible core is a **decision flow plus at least one physical flow** — an information flow (digitally measuring physical state) or an action flow (changing it). CPS scale **recursively**: the same artifact is a device, a system, or a system-of-systems depending on perspective. The genuinely new feature is the intersection of the **IT world** (data and computation), the **OT world** (control and actuation), and **timing constraints** binding them. CPS and IoT overlap heavily; the Framework is meant to apply equally to both.

### The CPS Framework — the Aspect × Facet grid

The Framework is an **analysis methodology plus shared vocabulary**, built by crossing two orthogonal structures:

- **Nine aspects** — groupings of related **concerns**: functional, business, human, trustworthiness, timing, data, boundaries, composition, lifecycle. Concerns are the driver of the whole method and are **not orthogonal** (analyzing trustworthiness forces you to weigh the trustworthiness of timing).
- **Three facets** — engineering views, each carrying its own activities and artifacts:
  - **Conceptualization** — what the CPS should be/do; produces the **CPS model**, a rooted tree of traceable **properties**.
  - **Realization** — how it is built and operated; produces the instance, designs, tests, and trade-offs.
  - **Assurance** — how much confidence, and why; produces the **assurance case** (claims, evidence, argumentation, estimate of confidence).

Every aspect is examined through every facet. Run the facets as **interchangeable modes**, not a waterfall — the same grid supports agile, reverse-engineering, service-based, and gap-analysis flows. When several concerns apply at once, the combined requirement is the **composition of concerns** = set union of the properties each demands. The Framework draws on ISO/IEC/IEEE **42010** (architecture description) and **15288** (life-cycle processes) but does not reproduce their text.

### Trustworthiness as cross-property risk

CPS trustworthiness is **greater than the sum of trustworthy parts**. Treat five top-level properties together — **cybersecurity, privacy, safety, reliability, resilience** — through one **cross-property risk management** process, not five silos. Key distinctions and levers:

- **Reliability handles *risk*** (known outcome distribution; fault tolerance). **Resilience handles *uncertainty*** (unknown distribution, often an adversary; threat tolerance). Most security/privacy challenges live in resilience.
- Treat the **risk budget** as a *common resource* every property draws on, allocated by consequence (not split equally). Expect **cyber components** to consume the largest share.
- Push each protection onto the element type — **physical, analog, or cyber** — best able to enforce it. *Stuxnet* defeated five properties engineered in isolation; a physical over-speed interlock would have stopped it regardless of any digital command.
- Cybersecurity is **necessary but not sufficient** for privacy; security measures can themselves create privacy risk.

### Data interoperability

Interoperability is about **understanding**, not just transport. Climb three rungs above physical connectivity: **syntactical** (move bytes intact) → **semantic** (agree on meaning) → **contextual** (agree on rules of use). A shared **canonical model** plus well-placed **adaptors** cuts transformations from ~n(n−1) toward n. Split data into **archival** vs. **real-time** (real-time data can expire in transit). Give each datum a unique, persistent, resolvable **identifier** (keep changeable attributes out of the name). Security = **confidentiality / integrity / availability**, with **availability** prioritized in control systems; the trust chain runs all the way down to physical **actuation**.

### Timing as a first-class concern

Timing is the **seam where cyber meets physical**, and getting it wrong is a *correctness* failure, not a performance shortfall. Express requirements as bounds on **time intervals (TIs)** between significant events, and use the **weakest class** that works:

| TI class | Holds | Use when |
|---|---|---|
| **Bounded** | under a stated max | a deadline only |
| **Deterministic** | within error of a target, local timescale | a precise relationship must repeat |
| **Accurate** | deterministic + traceable to UTC/TAI | spatial scale or regulation forces it |

Frequency, phase, and time are distinct; phase and time need signal transport plus delay compensation (so **position and time are coupled**). Modern CPUs/OSes are **not time-aware** — explicit time lives in FPGAs/ASICs, time-aware PHYs, and **time-triggered architectures**. Aim for **time-correctness by design**: reason in logical time, enforce physical time only at the boundary to physics. At scale, a **CPS Time Domain** (continuous primary timescale, prefer **holdover** over discontinuity) plus a **CPS Network Manager** schedules bounded-latency traffic.

### Secure and resilient time

Treat an accurate instant as a measured, attackable **supply chain**: source, transfer path, quality spec, failure modes, continuity plan. Distinguish **denial** (jamming — degrade to a safe fallback) from **spoofing** (counterfeit signal — confident *wrong* time, the dangerous case). Defenses span GNSS NMA, strong symmetric keys, whole-packet authentication, NTP/PTP-Annex-K/MACsec/IPsec, intrusion detection, and clock-drift correction. Resilience comes from **holdover** oscillators, **integrity monitoring** (time-to-alarm, integrity risk, alarm limit), the **detect/alarm/fail-over** triad, and **source diversity** (other GNSS, dedicated WANs, SyncE+PTP/White Rabbit, WWVB/WWV, eLORAN). Clock quality is engineered with the **clock-error model** and the **Allan-variance** family plus **MTIE** (which sizes buffers and predicts data slips).

---

## Chapter Index

| # | Vol | Section | Key content |
|---|-----|---------|-------------|
| [ch01](chapters/ch01-nist-cps-introduction-and-what-makes-cps-different.md) | 1 | Introduction: what makes CPS different | CPS definition, decision/information/action flows, recursive device/system/SoS, IT-meets-OT-under-a-clock, emergence, composability, the CPS PWG |
| [ch02](chapters/ch02-nist-cps-framework-facets-aspects-concerns.md) | 1 | The Framework: facets, aspects, concerns | The aspect × facet grid, nine aspects, three facets, properties, the assurance case, composition of concerns, 42010/15288 base |
| [ch03](chapters/ch03-nist-cps-related-standards-and-applying-the-framework.md) | 1 | Related standards & applying the Framework | The IoT/timing/security standards landscape (IoT ARM, IEEE P2413, OneM2M, TSN/PTP) and a worked emergency-response use case through the three facets |
| [ch04](chapters/ch04-nist-cps-cybersecurity-and-privacy-risk.md) | 2 | Cybersecurity & privacy (cross-property risk) | Cross-property risk management, five trustworthiness properties, risk vs. uncertainty, the risk budget, physical/analog/cyber co-design, Stuxnet, privacy |
| [ch05](chapters/ch05-nist-cps-data-interoperability.md) | 2 | Data interoperability | Syntactical/semantic/contextual, canonical models & adaptors, identifiers & provenance, data fusion, privacy-by-derivation, Fog, timestamps, CIA with availability first |
| [ch06](chapters/ch06-nist-cps-timing-and-time-awareness.md) | 2 | Timing & time-awareness | TI classes (bounded/deterministic/accurate), time domains, the CNM, time-triggered architecture, why CPUs aren't time-aware, secure timing, GNSS jamming/spoofing |
| [ch07](chapters/ch07-nist-cps-use-case-analysis-method.md) | 2 | Use-case analysis method | Two-stage CPS Examples → specific use cases, primitive requirements, the requirement-category form, coverage-gap clustering, worked examples |
| [ch08](chapters/ch08-nist-cps-managing-and-securing-time.md) | 3 | Managing & securing time (Timing Annex) | Clock-error model, Allan/MTIE metrics, time-aware networking standards, two-way transfer & reciprocity, time as a security target, holdover/backups, sector requirements |

## Topic Index

- **Actuation / trust chain to actuation** → ch05
- **Allan variance / MTIE / clock-error model** → ch08
- **Archival vs. real-time data** → ch05
- **Aspects (the nine)** → ch02
- **Assurance case / assurance facet** → ch02, ch03
- **Boundaries / scales / levels (data)** → ch05
- **Canonical model / adaptors** → ch05
- **Clock quality / metrology** → ch08
- **Composability / free composability** → ch01
- **Composition of concerns** → ch02
- **Conceptualization / realization / assurance (facets)** → ch02
- **Cross-property risk management** → ch04
- **CPS definition / what makes CPS different** → ch01
- **CPS Network Manager (CNM)** → ch06, ch08
- **CPS Time Domain** → ch06
- **Data interoperability (syntactical/semantic/contextual)** → ch05
- **Data fusion** → ch05
- **Emergent behavior** → ch01
- **Facets** → ch02
- **Fog computing** → ch05
- **GNSS jamming and spoofing** → ch06, ch08
- **Holdover** → ch06, ch08
- **Identifiers / provenance** → ch05
- **Integrity monitoring (time)** → ch08
- **IoT / IoT standards** → ch01, ch03
- **PTP / NTP / IEEE 1588 attacks and defenses** → ch06, ch08
- **Primitive requirements** → ch07
- **Privacy** → ch04, ch05
- **Reciprocity assumption (two-way time transfer)** → ch08
- **Reliability vs. resilience (risk vs. uncertainty)** → ch04
- **Risk budget** → ch04
- **Secure / resilient time** → ch06, ch08
- **Standards landscape (IoT / timing / security)** → ch03
- **Stuxnet** → ch04
- **Synchrophasors / grid timing** → ch08
- **System of systems (SoS)** → ch01
- **Time interval classes (bounded / deterministic / accurate)** → ch06
- **Time-correctness by design** → ch06
- **Time-triggered architecture** → ch06
- **Timing aspect** → ch06, ch08
- **Trustworthiness (five properties)** → ch04
- **Use-case analysis method** → ch07
- **Use cases (CPS Examples vs. specific)** → ch07

## Supporting Files

- [glossary.md](glossary.md) — key CPS Framework, trustworthiness, data, and timing terms, alphabetical, with chapter references
- [patterns.md](patterns.md) — reusable patterns (analyze on the grid, run facets as modes, cross-property risk, the interoperability ladder, TI classes, securing time, use-case requirements) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, the aspect/facet grid, trustworthiness and TI-class tables, threats & defenses for time, tells & smells

---

## Scope & Limits

**Covers**: the NIST CPS Framework per SP 1500-201 (the aspect × facet grid, nine aspects, three facets, properties, assurance case, composition of concerns); the Vol 2 working-group reports — cross-property cybersecurity/privacy risk, data interoperability, the timing aspect, and the use-case requirements method; and the Vol 3 Timing Annex (clock metrology, time-aware networking, and secure/resilient time). It bridges IT and OT under a clock and complements the broader SE and security packs.

**Does not cover in depth**: this is a **2017 v1.0 living/draft document** — it is explicit that some sections are incomplete and that standards references are *exemplary, not prescriptive*. It is therefore thin on **post-2017 standards evolution** (later TSN/DetNet, 5G timing maturation, newer privacy-engineering methodologies), on **detailed control catalogs** (it points to other NIST work for those), and on **deep domain specialization** (it gives generic facet activities to be tailored per domain). It **names but does not reproduce** ISO/IEC/IEEE **42010** and **15288** process text (third-party copyrighted — see `se-standards-signpost`; for open SE process models use `nasa-npr-7123` / `dau-se-guidebook`), nor the **permission-licensed third-party figures** in the source (the Beecham M2M map, the ETSI smart-transport illustration, and several vendor/standards-body diagrams). For systems security engineering and cyber-resiliency see `nist-sse`.

**Jurisdiction**: US Government public domain work (with named third-party ISO/IEC/IEEE and figure material not reproduced here). The Framework is voluntary guidance and broadly adoptable.
